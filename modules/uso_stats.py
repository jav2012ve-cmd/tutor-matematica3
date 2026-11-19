"""
Contador de accesos anónimo: registra qué módulos se usan y cuántas consultas
hay en cada uno. No identifica al usuario.

Además, opcionalmente registra un evento detallado en Supabase (tabla
app_usage_event) con JSON: temas, modalidad de quiz, tema detectado, etc.

Las retroalimentaciones de experiencia (opciones a–e) van a la tabla
``app_user_feedback_report`` vía RPC ``insert_user_feedback_report`` (ver
``supabase_user_feedback.sql``), con respaldo local ``data/user_feedback_reports.jsonl``.

Prioridad de almacenamiento:
1. Supabase (PostgREST) si hay SUPABASE_URL + clave service_role.
2. Archivo local data/uso_stats.json para contadores; data/usage_events.jsonl
   como respaldo de eventos si Supabase no acepta el detalle.

Se usa HTTP directo (requests).
"""
from __future__ import annotations

import base64
import json
import os
from datetime import datetime, timezone
from typing import Any, Optional

import requests

from modules import temario

MODULOS = (
    "Entrenamiento",
    "Respuesta Guiada",
    "Quiz",
    "Tutor Preguntas Abiertas",
    "Corrección de Manuscritos",
)

STATS_TEMA_NO_ESPECIFICADO = "(No especificado)"

_TABLE_NAME = "app_module_usage"
_TABLE_TOPIC = "app_topic_usage"
_RPC_INCREMENT = "increment_module_usage"
_RPC_INSERT_EVENT = "insert_usage_event"
_RPC_USER_FEEDBACK = "insert_user_feedback_report"
_RPC_TOPICS_BATCH = "increment_topic_usage_batch"
_TIMEOUT_SEC = 12

# Misma semántica que public.app_user_feedback_report.tipo_reporte (SQL).
_CODIGO_A_TIPO_REPORTE: dict[str, str] = {
    "a": "ok_sin_incidencias",
    "b": "latex_visual_sin_impacto_funcional",
    "c": "latex_afecto_funcionalidad",
    "d": "contenido_respuestas_incorrectas",
    "e": "imagen_manuscrito_no_reconocido",
}


def _ruta_archivo() -> str:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    carpeta = os.path.join(base, "data")
    os.makedirs(carpeta, exist_ok=True)
    return os.path.join(carpeta, "uso_stats.json")


def _ruta_eventos_jsonl() -> str:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    carpeta = os.path.join(base, "data")
    os.makedirs(carpeta, exist_ok=True)
    return os.path.join(carpeta, "usage_events.jsonl")


def _ruta_user_feedback_jsonl() -> str:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    carpeta = os.path.join(base, "data")
    os.makedirs(carpeta, exist_ok=True)
    return os.path.join(carpeta, "user_feedback_reports.jsonl")


def _ruta_topic_archivo() -> str:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    carpeta = os.path.join(base, "data")
    os.makedirs(carpeta, exist_ok=True)
    return os.path.join(carpeta, "topic_usage.json")


def _credenciales_supabase() -> tuple[Optional[str], Optional[str]]:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get(
        "SUPABASE_KEY"
    )
    if url and key:
        return url.strip(), key.strip()
    try:
        import streamlit as st

        sec = st.secrets
        u = str(sec["SUPABASE_URL"]).strip()
        k = None
        try:
            k = str(sec["SUPABASE_SERVICE_ROLE_KEY"]).strip()
        except (KeyError, TypeError):
            pass
        if not k:
            try:
                k = str(sec["SUPABASE_KEY"]).strip()
            except (KeyError, TypeError):
                pass
        if u and k:
            return u, k
    except Exception:
        pass
    return None, None


def _rol_jwt_supabase(api_key: str) -> Optional[str]:
    """
    Lee el claim ``role`` del JWT de Supabase sin verificar la firma.
    Solo para diagnóstico (anon vs service_role). No expone el secreto.
    """
    try:
        parts = (api_key or "").split(".")
        if len(parts) < 2:
            return None
        payload_b64 = parts[1] + "=" * ((4 - len(parts[1]) % 4) % 4)
        data = json.loads(base64.urlsafe_b64decode(payload_b64.encode("ascii")))
        role = data.get("role")
        return str(role) if role else None
    except Exception:
        return None


def _headers_rest(api_key: str) -> dict[str, str]:
    return {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _aviso_clave_anon(role: Optional[str]) -> Optional[str]:
    if role == "anon":
        return (
            "La clave configurada es de rol `anon`. Con RLS activo y sin políticas "
            "SELECT, PostgREST puede devolver tablas vacías (HTTP 200) mientras las "
            "escrituras fallan o no persisten. Usa `SUPABASE_SERVICE_ROLE_KEY` "
            "(service_role) en Secrets."
        )
    return None


def _base_vacia() -> dict[str, int]:
    return {m: 0 for m in MODULOS}


def _cargar_archivo() -> dict[str, int]:
    ruta = _ruta_archivo()
    if not os.path.isfile(ruta):
        return _base_vacia()
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
        for m in MODULOS:
            data.setdefault(m, 0)
        return data
    except (json.JSONDecodeError, OSError):
        return _base_vacia()


def _guardar_archivo(data: dict[str, int]) -> None:
    try:
        with open(_ruta_archivo(), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError:
        pass


def _sanitize_payload(d: Any) -> dict[str, Any]:
    """Convierte a estructura JSON-serializable y acota tamaños."""

    def norm(v: Any) -> Any:
        if v is None or isinstance(v, (bool, int, float)):
            return v
        if isinstance(v, str):
            return v[:2000]
        if isinstance(v, list):
            out = []
            for x in v[:80]:
                if isinstance(x, dict):
                    out.append(_sanitize_payload(x))
                else:
                    out.append(norm(x))
            return out
        if isinstance(v, dict):
            return _sanitize_payload(v)
        return str(v)[:500]

    if not isinstance(d, dict):
        return {}
    return {str(k)[:120]: norm(val) for k, val in d.items()}


def _append_evento_local(modo: str, detalle: dict[str, Any]) -> None:
    try:
        line = json.dumps(
            {
                "ts": datetime.now(timezone.utc).isoformat(),
                "modo": modo,
                "payload": _sanitize_payload(detalle),
            },
            ensure_ascii=False,
        )
        with open(_ruta_eventos_jsonl(), "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def _cargar_supabase() -> tuple[Optional[dict[str, int]], Optional[str]]:
    """
    Devuelve (contadores, error).
    Contadores vacíos con error=None significa lectura OK y tabla sin filas útiles.
    """
    url, key = _credenciales_supabase()
    if not url or not key:
        return None, None
    aviso_anon = _aviso_clave_anon(_rol_jwt_supabase(key))
    base = url.rstrip("/")
    endpoint = f"{base}/rest/v1/{_TABLE_NAME}?select=module,count"
    try:
        r = requests.get(endpoint, headers=_headers_rest(key), timeout=_TIMEOUT_SEC)
        if r.status_code != 200:
            body = (r.text or "")[:300]
            err = f"HTTP {r.status_code}: {body}"
            if aviso_anon:
                err = f"{aviso_anon} Detalle lectura: {err}"
            return None, err
        rows = r.json()
        out = _base_vacia()
        for row in rows:
            mod = row.get("module")
            if mod in MODULOS:
                out[mod] = int(row.get("count") or 0)
        if aviso_anon and sum(out.values()) == 0:
            return out, aviso_anon
        return out, None
    except (requests.RequestException, ValueError, TypeError) as e:
        return None, str(e)


def _registrar_supabase(modulo: str) -> tuple[bool, Optional[str]]:
    url, key = _credenciales_supabase()
    if not url or not key:
        return False, None
    aviso_anon = _aviso_clave_anon(_rol_jwt_supabase(key))
    base = url.rstrip("/")
    endpoint = f"{base}/rest/v1/rpc/{_RPC_INCREMENT}"
    try:
        r = requests.post(
            endpoint,
            headers={**_headers_rest(key), "Prefer": "return=minimal"},
            json={"p_module": modulo},
            timeout=_TIMEOUT_SEC,
        )
        if r.status_code in (200, 204):
            return True, None
        body = (r.text or "")[:300]
        err = f"HTTP {r.status_code}: {body}"
        if aviso_anon:
            err = f"{aviso_anon} Detalle escritura: {err}"
        return False, err
    except requests.RequestException as e:
        return False, str(e)


def _extraer_topic_keys_validos(
    modulo: str, detalle: Optional[dict[str, Any]]
) -> list[str]:
    """Temas del temario presentes en ``detalle`` (uno o varios), sin duplicados."""
    if not detalle:
        return []
    valid = set(temario.LISTA_TEMAS)
    raw: list[str] = []
    if modulo in ("Entrenamiento", "Quiz"):
        for x in detalle.get("temas") or []:
            if isinstance(x, str) and x.strip() in valid:
                raw.append(x.strip())
    elif modulo == "Respuesta Guiada":
        t = temario.normalizar_tema_curso(detalle.get("tema_detectado"))
        if t:
            raw.append(t)
    elif modulo in ("Tutor Preguntas Abiertas", "Corrección de Manuscritos"):
        t = temario.normalizar_tema_curso(detalle.get("tema_catedra"))
        if t:
            raw.append(t)
    seen: set[str] = set()
    out: list[str] = []
    for t in raw:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def _increment_topics_supabase(topics: list[str]) -> bool:
    if not topics:
        return True
    url, key = _credenciales_supabase()
    if not url or not key:
        return False
    base = url.rstrip("/")
    endpoint = f"{base}/rest/v1/rpc/{_RPC_TOPICS_BATCH}"
    try:
        r = requests.post(
            endpoint,
            headers={**_headers_rest(key), "Prefer": "return=minimal"},
            json={"p_topics": topics},
            timeout=_TIMEOUT_SEC,
        )
        return r.status_code in (200, 204)
    except requests.RequestException:
        return False


def _increment_topics_local(topics: list[str]) -> None:
    path = _ruta_topic_archivo()
    data: dict[str, int] = {}
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            data = {}
    for t in topics:
        data[t] = int(data.get(t, 0) or 0) + 1
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError:
        pass


def _insert_user_feedback_supabase(
    funcionalidad: str, codigo: str
) -> tuple[bool, Optional[str]]:
    url, key = _credenciales_supabase()
    if not url or not key:
        return False, None
    base = url.rstrip("/")
    endpoint = f"{base}/rest/v1/rpc/{_RPC_USER_FEEDBACK}"
    try:
        r = requests.post(
            endpoint,
            headers={**_headers_rest(key), "Prefer": "return=minimal"},
            json={
                "p_funcionalidad": (funcionalidad or "")[:120],
                "p_codigo": (codigo or "").strip().lower()[:1],
            },
            timeout=_TIMEOUT_SEC,
        )
        if r.status_code in (200, 204):
            return True, None
        body = (r.text or "")[:400]
        return False, f"HTTP {r.status_code}: {body}"
    except requests.RequestException as e:
        return False, str(e)


def _append_user_feedback_local(funcionalidad: str, codigo: str) -> None:
    tipo = _CODIGO_A_TIPO_REPORTE.get((codigo or "").strip().lower())
    if not tipo:
        return
    try:
        line = json.dumps(
            {
                "ts": datetime.now(timezone.utc).isoformat(),
                "funcionalidad": (funcionalidad or "")[:120],
                "codigo_opcion": codigo.strip().lower()[:1],
                "tipo_reporte": tipo,
            },
            ensure_ascii=False,
        )
        with open(_ruta_user_feedback_jsonl(), "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def _insert_event_supabase(modulo: str, payload: dict[str, Any]) -> tuple[bool, Optional[str]]:
    url, key = _credenciales_supabase()
    if not url or not key:
        return False, None
    base = url.rstrip("/")
    endpoint = f"{base}/rest/v1/rpc/{_RPC_INSERT_EVENT}"
    clean = _sanitize_payload(payload)
    try:
        r = requests.post(
            endpoint,
            headers={**_headers_rest(key), "Prefer": "return=minimal"},
            json={"p_modo": modulo, "p_payload": clean},
            timeout=_TIMEOUT_SEC,
        )
        if r.status_code in (200, 204):
            return True, None
        body = (r.text or "")[:400]
        return False, f"HTTP {r.status_code}: {body}"
    except requests.RequestException as e:
        return False, str(e)


def _session_set_supabase_warn(msg: str) -> None:
    try:
        import streamlit as st

        st.session_state["_uso_stats_supabase_warn"] = msg
    except Exception:
        pass


def _session_clear_supabase_warn() -> None:
    try:
        import streamlit as st

        st.session_state.pop("_uso_stats_supabase_warn", None)
    except Exception:
        pass


def registrar_retroalimentacion_experiencia(
    funcionalidad: str,
    opcion: str,
    *,
    incluir_opcion_e_permitida: bool = False,
) -> None:
    """
    Registra la opción elegida por el usuario (a–e) sin incrementar contadores de módulo.

    Supabase: tabla ``app_user_feedback_report`` (RPC ``insert_user_feedback_report``).
    Local: ``data/user_feedback_reports.jsonl`` con ``tipo_reporte`` normalizado.
    """
    op = (opcion or "").strip().lower()
    if op not in ("a", "b", "c", "d", "e"):
        return
    if op == "e" and not incluir_opcion_e_permitida:
        return
    func = (funcionalidad or "")[:120]
    url, key = _credenciales_supabase()
    ok_db = False
    if url and key:
        ok_db, _err = _insert_user_feedback_supabase(func, op)
    if not ok_db:
        _append_user_feedback_local(func, op)


def registrar_uso(modulo: str, detalle: Optional[dict[str, Any]] = None) -> None:
    """
    Incrementa el contador del módulo y, si se pasa ``detalle``, inserta un
    evento en ``app_usage_event`` (requiere ejecutar ``supabase_usage_events.sql``).
    """
    if modulo not in MODULOS:
        return
    url, key = _credenciales_supabase()
    ok_inc, err_inc = _registrar_supabase(modulo)
    if ok_inc:
        _session_clear_supabase_warn()
    elif url and key and err_inc:
        _session_set_supabase_warn(
            f"No se pudo guardar el contador en Supabase ({modulo}). {err_inc} "
            "Revisa Secrets y `supabase_schema.sql` / `supabase_grants.sql`."
        )

    if not ok_inc:
        data = _cargar_archivo()
        data[modulo] = data.get(modulo, 0) + 1
        _guardar_archivo(data)

    if detalle:
        if url and key:
            ok_ev, err_ev = _insert_event_supabase(modulo, detalle)
            if not ok_ev:
                _append_evento_local(modulo, detalle)
                # No pisa el aviso de contador si ya falló el incremento.
                if ok_inc and err_ev:
                    _session_set_supabase_warn(
                        f"Contador OK, pero falló el evento detallado en Supabase "
                        f"({modulo}). {err_ev} Ejecuta `supabase_usage_events.sql` "
                        "(o `supabase_usage_events_add_payload.sql` si falta `payload`)."
                    )
        else:
            _append_evento_local(modulo, detalle)

    topic_keys = _extraer_topic_keys_validos(modulo, detalle)
    if topic_keys:
        if url and key:
            if not _increment_topics_supabase(topic_keys):
                _increment_topics_local(topic_keys)
                if ok_inc:
                    _session_set_supabase_warn(
                        "Contador de módulo OK, pero falló `increment_topic_usage_batch`. "
                        "Ejecuta `supabase_topic_usage.sql` (y el seed) en Supabase."
                    )
        else:
            _increment_topics_local(topic_keys)


def _cargar_temas_local() -> dict[str, int]:
    base: dict[str, int] = {t: 0 for t in temario.LISTA_TEMAS}
    path = _ruta_topic_archivo()
    if not os.path.isfile(path):
        return base
    try:
        with open(path, "r", encoding="utf-8") as f:
            local = json.load(f)
        for t in temario.LISTA_TEMAS:
            if t in local:
                base[t] = int(local[t] or 0)
    except (json.JSONDecodeError, OSError, TypeError):
        pass
    return base


def _cargar_eventos_local(lim: int) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    path = _ruta_eventos_jsonl()
    if not os.path.isfile(path):
        return out
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in reversed(lines[-lim:]):
            try:
                rec = json.loads(line.strip())
                out.append(
                    {
                        "timestamp": rec.get("ts"),
                        "modo": rec.get("modo"),
                        "payload": rec.get("payload") or {},
                    }
                )
            except (json.JSONDecodeError, TypeError):
                continue
    except OSError:
        return []
    return out


def obtener_estadisticas() -> dict[str, int]:
    """Devuelve los contadores actuales (solo lectura)."""
    remote, err = _cargar_supabase()
    local = _cargar_archivo()
    if remote is not None:
        remote_total = sum(int(remote.get(m, 0) or 0) for m in MODULOS)
        local_total = sum(int(local.get(m, 0) or 0) for m in MODULOS)
        if remote_total == 0 and local_total > 0:
            prefijo = f"{err} " if err else ""
            _session_set_supabase_warn(
                prefijo
                + "Supabase devolvió contadores en 0, pero hay respaldo local. "
                "Se muestran datos locales. En Streamlit Cloud el disco es efímero: "
                "si las escrituras a Supabase fallan (clave `anon`, RPC/grants), "
                "el panel admin verá vacío tras reiniciar. "
                "Revisa service_role y `supabase_schema.sql` / `supabase_grants.sql`."
            )
            return local.copy()
        if err:
            _session_set_supabase_warn(err)
        return remote
    if err:
        _session_set_supabase_warn(
            f"No se pudieron leer contadores desde Supabase. {err} "
            "Mostrando respaldo local si existe."
        )
    return local.copy()


def obtener_estadisticas_temas() -> dict[str, int]:
    """
    Conteos por tema del temario (0 si no hay registro).
    Origen: Supabase ``app_topic_usage`` o archivo local ``data/topic_usage.json``.
    """
    base_local = _cargar_temas_local()
    url, key = _credenciales_supabase()
    if url and key:
        try:
            b = url.rstrip("/")
            endpoint = f"{b}/rest/v1/{_TABLE_TOPIC}?select=topic_key,count"
            r = requests.get(endpoint, headers=_headers_rest(key), timeout=_TIMEOUT_SEC)
            if r.status_code == 200:
                base: dict[str, int] = {t: 0 for t in temario.LISTA_TEMAS}
                for row in r.json() or []:
                    k = row.get("topic_key")
                    if k in base:
                        base[k] = int(row.get("count") or 0)
                if sum(base.values()) == 0 and sum(base_local.values()) > 0:
                    _session_set_supabase_warn(
                        "Tabla `app_topic_usage` vacía o invisible; mostrando "
                        "respaldo local de temas. Ejecuta `supabase_topic_usage.sql` "
                        "y usa clave service_role."
                    )
                    return base_local
                return base
            body = (r.text or "")[:300]
            _session_set_supabase_warn(
                f"No se pudo leer `app_topic_usage` (HTTP {r.status_code}: {body}). "
                "Mostrando respaldo local si existe."
            )
        except (requests.RequestException, ValueError, TypeError) as e:
            _session_set_supabase_warn(
                f"Error leyendo temas en Supabase: {e}. Mostrando respaldo local."
            )
    return base_local


def obtener_eventos_recientes(limit: int = 150) -> list[dict[str, Any]]:
    """
    Devuelve eventos recientes de uso (modo + payload).
    Prioriza Supabase (tabla app_usage_event); si no está disponible o viene
    vacío con respaldo local, usa JSONL local.
    """
    lim = max(1, min(int(limit or 150), 5000))
    local_out = _cargar_eventos_local(lim)

    url, key = _credenciales_supabase()
    if url and key:
        try:
            b = url.rstrip("/")
            endpoint = (
                f"{b}/rest/v1/app_usage_event"
                f"?select=created_at,modo,payload&order=created_at.desc&limit={lim}"
            )
            r = requests.get(endpoint, headers=_headers_rest(key), timeout=_TIMEOUT_SEC)
            if r.status_code == 200:
                rows = r.json() or []
                out: list[dict[str, Any]] = []
                for row in rows:
                    out.append(
                        {
                            "timestamp": row.get("created_at"),
                            "modo": row.get("modo"),
                            "payload": row.get("payload") or {},
                        }
                    )
                if not out and local_out:
                    aviso = _aviso_clave_anon(_rol_jwt_supabase(key))
                    prefijo = f"{aviso} " if aviso else ""
                    _session_set_supabase_warn(
                        prefijo
                        + "`app_usage_event` está vacío en Supabase; mostrando eventos "
                        "locales. Ejecuta `supabase_usage_events.sql` y verifica "
                        "service_role / grants."
                    )
                    return local_out
                return out
            body = (r.text or "")[:300]
            _session_set_supabase_warn(
                f"No se pudieron leer eventos (HTTP {r.status_code}: {body}). "
                "Mostrando respaldo local si existe."
            )
        except (requests.RequestException, ValueError, TypeError) as e:
            _session_set_supabase_warn(
                f"Error leyendo eventos en Supabase: {e}. Mostrando respaldo local."
            )

    return local_out


def diagnostico_almacenamiento() -> dict[str, Any]:
    """
    Estado del backend para el panel admin. No incluye valores secretos.
    """
    url, key = _credenciales_supabase()
    info: dict[str, Any] = {
        "supabase_configurado": bool(url and key),
        "url_host": None,
        "clave_rol": None,
        "lectura_modulos_ok": None,
        "filas_modulos": None,
        "total_modulos_remoto": None,
        "total_modulos_local": sum(_cargar_archivo().values()),
        "eventos_remotos": None,
        "eventos_locales": len(_cargar_eventos_local(5000)),
        "temas_remotos_total": None,
        "temas_locales_total": sum(_cargar_temas_local().values()),
        "error": None,
        "recomendacion": None,
    }
    if not url or not key:
        info["recomendacion"] = (
            "Sin SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY: en Streamlit Cloud los "
            "contadores locales se pierden al reiniciar/dormir la app."
        )
        return info

    try:
        from urllib.parse import urlparse

        host = urlparse(url).netloc or None
        info["url_host"] = host
    except Exception:
        info["url_host"] = "(url presente)"

    role = _rol_jwt_supabase(key)
    info["clave_rol"] = role or "desconocido"
    if role == "anon":
        info["recomendacion"] = (
            "Sustituye la clave `anon` por `service_role` en Secrets "
            "(SUPABASE_SERVICE_ROLE_KEY)."
        )

    remote, err = _cargar_supabase()
    if err and remote is None:
        info["lectura_modulos_ok"] = False
        info["error"] = err
        if not info["recomendacion"]:
            info["recomendacion"] = (
                "Revisa Secrets, ejecuta los SQL (`supabase_schema.sql`, "
                "`supabase_grants.sql`, `supabase_usage_events.sql`, "
                "`supabase_topic_usage.sql`) y confirma la URL del proyecto."
            )
        return info

    info["lectura_modulos_ok"] = True
    if remote is not None:
        info["total_modulos_remoto"] = sum(remote.values())
        info["filas_modulos"] = sum(1 for m in MODULOS if int(remote.get(m, 0) or 0) > 0)
    if err:
        info["error"] = err

    # Conteo remoto de eventos / temas (solo metadatos).
    try:
        b = url.rstrip("/")
        r_ev = requests.get(
            f"{b}/rest/v1/app_usage_event?select=id&limit=1",
            headers={**_headers_rest(key), "Prefer": "count=exact"},
            timeout=_TIMEOUT_SEC,
        )
        if r_ev.status_code == 200:
            # Content-Range: 0-0/123 o */0
            cr = r_ev.headers.get("Content-Range") or r_ev.headers.get("content-range")
            if cr and "/" in cr:
                total = cr.split("/")[-1]
                info["eventos_remotos"] = int(total) if total.isdigit() else 0
            else:
                info["eventos_remotos"] = len(r_ev.json() or [])
        elif r_ev.status_code == 404:
            info["eventos_remotos"] = None
            info["error"] = (info.get("error") or "") + (
                " Tabla/app_usage_event no encontrada; ejecuta supabase_usage_events.sql."
            ).strip()
    except (requests.RequestException, ValueError, TypeError):
        pass

    try:
        b = url.rstrip("/")
        r_t = requests.get(
            f"{b}/rest/v1/{_TABLE_TOPIC}?select=topic_key,count",
            headers=_headers_rest(key),
            timeout=_TIMEOUT_SEC,
        )
        if r_t.status_code == 200:
            info["temas_remotos_total"] = sum(
                int(row.get("count") or 0) for row in (r_t.json() or [])
            )
    except (requests.RequestException, ValueError, TypeError):
        pass

    if (
        info.get("total_modulos_remoto") == 0
        and info.get("eventos_remotos") in (0, None)
        and not info.get("recomendacion")
    ):
        info["recomendacion"] = (
            "Backend alcanzable pero sin uso persistido. Genera una interacción "
            "real (p. ej. Entrenamiento) y recarga el panel. Si sigue en 0, "
            "prueba en SQL: SELECT public.increment_module_usage('Entrenamiento');"
        )
    return info


_TABLE_USER_FEEDBACK = "app_user_feedback_report"


def obtener_reportes_retroalimentacion(limit: int = 200) -> list[dict[str, Any]]:
    """
    Reportes tipados de experiencia (a–e): Supabase ``app_user_feedback_report``
    o archivo local ``data/user_feedback_reports.jsonl``.
    """
    lim = max(1, min(int(limit or 200), 3000))
    out: list[dict[str, Any]] = []

    url, key = _credenciales_supabase()
    if url and key:
        try:
            b = url.rstrip("/")
            endpoint = (
                f"{b}/rest/v1/{_TABLE_USER_FEEDBACK}"
                f"?select=created_at,funcionalidad,codigo_opcion,tipo_reporte"
                f"&order=created_at.desc&limit={lim}"
            )
            r = requests.get(endpoint, headers=_headers_rest(key), timeout=_TIMEOUT_SEC)
            if r.status_code == 200:
                for row in r.json() or []:
                    out.append(
                        {
                            "timestamp": row.get("created_at"),
                            "funcionalidad": row.get("funcionalidad"),
                            "codigo_opcion": row.get("codigo_opcion"),
                            "tipo_reporte": row.get("tipo_reporte"),
                        }
                    )
                return out
        except (requests.RequestException, ValueError, TypeError):
            pass

    path = _ruta_user_feedback_jsonl()
    if not os.path.isfile(path):
        return out
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in reversed(lines[-lim:]):
            try:
                rec = json.loads(line.strip())
                out.append(
                    {
                        "timestamp": rec.get("ts"),
                        "funcionalidad": rec.get("funcionalidad"),
                        "codigo_opcion": rec.get("codigo_opcion"),
                        "tipo_reporte": rec.get("tipo_reporte"),
                    }
                )
            except (json.JSONDecodeError, TypeError):
                continue
    except OSError:
        return []
    return out
