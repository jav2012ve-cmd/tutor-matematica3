"""
Cliente Gemini vía SDK **google-genai** (GA).

El paquete `google-generativeai` está en desuso; ver guía oficial:
https://ai.google.dev/gemini-api/docs/migrate

Plan de mantenimiento:
- Mantener `google-genai` actualizado (revisar notas de versión en GitHub).
- La clave sigue siendo `GOOGLE_API_KEY` (Streamlit secrets / entorno); el SDK
  también acepta `GEMINI_API_KEY` automáticamente si no hay `GOOGLE_API_KEY`.
- Si el modelo configurado se retira, hay cadena de fallback + list_models.
"""

from __future__ import annotations

import os
from typing import Any, Optional

import streamlit as st
from google import genai
from google.genai import types

# gemini-2.0-flash se retiró el 2026-06-01; ver changelog de Gemini API.
_MODELO_FLASH_DEFAULT = "gemini-3.5-flash"

# Orden de preferencia si el modelo activo deja de existir.
_CADENA_FALLBACK = (
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash",
)

# IDs retirados o próximos a retirar: no deben usarse aunque estén en secrets.
_MODELOS_RETIRADOS = frozenset(
    {
        "gemini-2.0-flash",
        "gemini-2.0-flash-001",
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash-lite",
        "gemini-2.0-flash-lite-001",
        "gemini-1.5-flash",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash-latest",
        "gemini-1.5-pro",
        "gemini-1.5-pro-001",
        "gemini-1.5-pro-latest",
        "gemini-pro",
        "gemini-pro-vision",
    }
)


def _normalizar_id_modelo(nombre: str) -> str:
    return (nombre or "").strip().split("/")[-1]


def _es_modelo_retirado(nombre: str) -> bool:
    short = _normalizar_id_modelo(nombre).lower()
    if short in _MODELOS_RETIRADOS:
        return True
    # Cualquier variante 2.0-flash* queda cubierta aunque Google añada sufijos.
    return short.startswith("gemini-2.0-flash") or short.startswith("gemini-1.5-")


def es_error_modelo_no_disponible(exc: BaseException) -> bool:
    """True si la API indica que el model id ya no existe / no está disponible."""
    msg = str(exc).lower()
    marcadores = (
        "not_found",
        "404",
        "is no longer available",
        "model not found",
        "was not found",
        "not supported",
        "does not exist",
    )
    return any(m in msg for m in marcadores)


def _obtener_api_key() -> Optional[str]:
    api_key = None
    try:
        if "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
    except (Exception, FileNotFoundError):
        pass
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        try:
            if "GEMINI_API_KEY" in st.secrets:
                api_key = st.secrets["GEMINI_API_KEY"]
        except (Exception, FileNotFoundError):
            pass
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
    return api_key


def configurar_gemini() -> bool:
    if _obtener_api_key():
        return True
    st.error(
        "⚠️ **Falta la API Key de Google (Gemini).**\n\n"
        "Para que el tutor funcione, configura la clave:\n\n"
        "• **En local:** crea el archivo `.streamlit/secrets.toml` (carpeta del proyecto) con:\n"
        "  `GOOGLE_API_KEY = \"tu-clave-aqui\"`\n\n"
        "• **Variable de entorno:** también puedes definir `GOOGLE_API_KEY` en tu sistema.\n\n"
        "• **En Streamlit Cloud:** en la app → Settings → Secrets, añade `GOOGLE_API_KEY`.\n\n"
        "Obtén la clave en [Google AI Studio](https://aistudio.google.com/apikey)."
    )
    return False


def _modelo_soporta_generate_content(methods: Optional[list[str]]) -> bool:
    if not methods:
        return True
    return "generateContent" in methods


def _puntuar_candidato_flash(short: str) -> int:
    """Prioriza modelos flash actuales; penaliza retirados."""
    s = short.lower()
    if _es_modelo_retirado(s):
        return -100
    if "embed" in s:
        return -50
    score = 0
    if "flash" in s:
        score += 10
    if "3.5" in s:
        score += 30
    elif "3.1" in s:
        score += 20
    elif "3-" in s or s.startswith("gemini-3"):
        score += 15
    elif "2.5" in s:
        score += 8
    if "lite" in s:
        score += 2
    return score


def obtener_modelo_robusto(client: genai.Client) -> str:
    """
    Elige un modelo con `generateContent`, priorizando variantes *flash* vigentes.
    Si la lista falla, devuelve el default estable.
    """
    mejor: Optional[str] = None
    mejor_score = -10**9
    respaldo: Optional[str] = None
    try:
        for m in client.models.list(config=types.ListModelsConfig(page_size=200)):
            if not _modelo_soporta_generate_content(m.supported_actions):
                continue
            name = (m.name or "").strip()
            if not name:
                continue
            short = _normalizar_id_modelo(name)
            if _es_modelo_retirado(short):
                continue
            if respaldo is None:
                respaldo = short
            score = _puntuar_candidato_flash(short)
            if score > mejor_score:
                mejor_score = score
                mejor = short
        if mejor and mejor_score >= 0:
            return mejor
        if respaldo:
            return respaldo
    except Exception:
        pass
    return _MODELO_FLASH_DEFAULT


def _modelo_preferido_configurado() -> Optional[str]:
    """
    Permite fijar modelo sin sondear catálogo remoto en el arranque.
    Mejora la estabilidad de despliegue en Streamlit Cloud.
    Ignora IDs retirados para no reproducir el fallo 404.
    """
    candidatos: list[str] = []
    m = (os.environ.get("GEMINI_MODEL") or "").strip()
    if m:
        candidatos.append(m)
    try:
        if "GEMINI_MODEL" in st.secrets:
            sec = str(st.secrets["GEMINI_MODEL"]).strip()
            if sec:
                candidatos.append(sec)
    except (Exception, FileNotFoundError):
        pass
    for raw in candidatos:
        short = _normalizar_id_modelo(raw)
        if _es_modelo_retirado(short):
            st.warning(
                f"⚠️ `GEMINI_MODEL={short}` ya no está disponible en la API de Gemini. "
                f"Se usará `{_MODELO_FLASH_DEFAULT}` (o un fallback)."
            )
            continue
        return short
    return None


def _config_generacion() -> types.GenerateContentConfig:
    return types.GenerateContentConfig(
        temperature=0.1,
        top_p=0.95,
    )


class _GeneradorGeminiCompat:
    """
    Expone `generate_content(...)` como el antiguo `GenerativeModel` para no
    tocar el resto de `app.py` ni el registro CSV.
    """

    def __init__(
        self,
        client: genai.Client,
        model_name: str,
        gen_config: types.GenerateContentConfig,
    ) -> None:
        self._client = client
        self._model_name = model_name
        self._gen_config = gen_config

    @property
    def model_name(self) -> str:
        return self._model_name

    def cambiar_modelo(self, nuevo: str) -> None:
        self._model_name = _normalizar_id_modelo(nuevo)

    def generate_content(self, prompt_parts: Any) -> Any:
        return self._client.models.generate_content(
            model=self._model_name,
            contents=prompt_parts,
            config=self._gen_config,
        )


def _siguientes_fallbacks(actual: str) -> list[str]:
    actual_n = _normalizar_id_modelo(actual)
    vistos = {actual_n}
    out: list[str] = []
    for cand in _CADENA_FALLBACK:
        if cand not in vistos and not _es_modelo_retirado(cand):
            out.append(cand)
            vistos.add(cand)
    return out


def intentar_fallback_modelo(model: Any, client: Optional[genai.Client] = None) -> Optional[str]:
    """
    Cambia el wrapper al siguiente modelo de la cadena (o al descubierto vía list).
    Devuelve el nuevo id o None si no hay alternativa.
    """
    if model is None or not hasattr(model, "cambiar_modelo"):
        return None
    actual = getattr(model, "model_name", "") or ""
    for cand in _siguientes_fallbacks(actual):
        model.cambiar_modelo(cand)
        return cand
    cli = client or getattr(model, "_client", None)
    if cli is not None:
        descubierto = obtener_modelo_robusto(cli)
        if descubierto and descubierto != _normalizar_id_modelo(actual):
            model.cambiar_modelo(descubierto)
            return descubierto
    return None


def iniciar_modelo():
    api_key = _obtener_api_key()
    if not api_key:
        st.error("No hay API key de Gemini configurada.")
        return None, None
    try:
        client = genai.Client(api_key=api_key)
        # Evita depender de `list_models()` al arrancar; si no hay override,
        # usamos un modelo flash estable.
        nombre_modelo = _modelo_preferido_configurado() or _MODELO_FLASH_DEFAULT
        model = _GeneradorGeminiCompat(client, nombre_modelo, _config_generacion())
        return model, nombre_modelo
    except Exception as e:
        st.error(f"Error iniciando modelo: {e}")
        return None, None
