"""
Contador de accesos anónimo: registra qué módulos se usan y cuántas consultas
hay en cada uno. No identifica al usuario.

Además, opcionalmente registra un evento detallado en Supabase (tabla
app_usage_event) con JSON: temas, modalidad de quiz, tema detectado, etc.

Prioridad de almacenamiento:
1. Supabase (PostgREST) si hay SUPABASE_URL + clave service_role.
2. Archivo local data/uso_stats.json para contadores; data/usage_events.jsonl
   como respaldo de eventos si Supabase no acepta el detalle.

Se usa HTTP directo (requests).
"""
from __future__ import annotations

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
    "Sube tu examen en PDF",
)

STATS_TEMA_NO_ESPECIFICADO = "(No especificado)"

_TABLE_NAME = "app_module_usage"
_TABLE_TOPIC = "app_topic_usage"
_RPC_INCREMENT = "increment_module_usage"
_RPC_INSERT_EVENT = "insert_usage_event"
_RPC_TOPICS_BATCH = "increment_topic_usage_batch"
_TIMEOUT_SEC = 12


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


def _headers_rest(api_key: str) -> dict[str, str]:
    return {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


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


def _cargar_supabase() -> Optional[dict[str, int]]:
    url, key = _credenciales_supabase()
    if not url or not key:
        return None
    base = url.rstrip("/")
    endpoint = f"{base}/rest/v1/{_TABLE_NAME}?select=module,count"
    try:
        r = requests.get(endpoint, headers=_headers_rest(key), timeout=_TIMEOUT_SEC)
        if r.status_code != 200:
            return None
        rows = r.json()
        out = _base_vacia()
        for row in rows:
            mod = row.get("module")
            if mod in MODULOS:
                out[mod] = int(row.get("count") or 0)
        return out
    except (requests.RequestException, ValueError, TypeError):
        return None


def _registrar_supabase(modulo: str) -> tuple[bool, Optional[str]]:
    url, key = _credenciales_supabase()
    if not url or not key:
        return False, None
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
        return False, f"HTTP {r.status_code}: {body}"
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
    elif modulo == "Sube tu examen en PDF":
        for t_raw in detalle.get("temas_detectados") or []:
            t = temario.normalizar_tema_curso(t_raw)
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
            ok_ev, _err_ev = _insert_event_supabase(modulo, detalle)
            if not ok_ev:
                _append_evento_local(modulo, detalle)
        else:
            _append_evento_local(modulo, detalle)

    topic_keys = _extraer_topic_keys_validos(modulo, detalle)
    if topic_keys:
        if url and key:
            if not _increment_topics_supabase(topic_keys):
                _increment_topics_local(topic_keys)
        else:
            _increment_topics_local(topic_keys)


def obtener_estadisticas() -> dict[str, int]:
    """Devuelve los contadores actuales (solo lectura)."""
    remote = _cargar_supabase()
    if remote is not None:
        return remote
    return _cargar_archivo().copy()


def obtener_estadisticas_temas() -> dict[str, int]:
    """
    Conteos por tema del temario (0 si no hay registro).
    Origen: Supabase ``app_topic_usage`` o archivo local ``data/topic_usage.json``.
    """
    base: dict[str, int] = {t: 0 for t in temario.LISTA_TEMAS}
    url, key = _credenciales_supabase()
    if url and key:
        try:
            b = url.rstrip("/")
            endpoint = f"{b}/rest/v1/{_TABLE_TOPIC}?select=topic_key,count"
            r = requests.get(endpoint, headers=_headers_rest(key), timeout=_TIMEOUT_SEC)
            if r.status_code == 200:
                for row in r.json() or []:
                    k = row.get("topic_key")
                    if k in base:
                        base[k] = int(row.get("count") or 0)
                return base
        except (requests.RequestException, ValueError, TypeError):
            pass
    path = _ruta_topic_archivo()
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                local = json.load(f)
            for t in temario.LISTA_TEMAS:
                if t in local:
                    base[t] = int(local[t] or 0)
        except (json.JSONDecodeError, OSError, TypeError):
            pass
    return base


def obtener_eventos_recientes(limit: int = 150) -> list[dict[str, Any]]:
    """
    Devuelve eventos recientes de uso (modo + payload).
    Prioriza Supabase (tabla app_usage_event); si no está disponible, usa JSONL local.
    """
    lim = max(1, min(int(limit or 150), 5000))
    out: list[dict[str, Any]] = []

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
                for row in rows:
                    out.append(
                        {
                            "timestamp": row.get("created_at"),
                            "modo": row.get("modo"),
                            "payload": row.get("payload") or {},
                        }
                    )
                return out
        except (requests.RequestException, ValueError, TypeError):
            pass

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
