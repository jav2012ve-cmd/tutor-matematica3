"""
Cliente Gemini vía SDK **google-genai** (GA).

El paquete `google-generativeai` está en desuso; ver guía oficial:
https://ai.google.dev/gemini-api/docs/migrate

Plan de mantenimiento:
- Mantener `google-genai` actualizado (revisar notas de versión en GitHub).
- La clave sigue siendo `GOOGLE_API_KEY` (Streamlit secrets / entorno); el SDK
  también acepta `GEMINI_API_KEY` automáticamente si no hay `GOOGLE_API_KEY`.
- Si `list_models` falla o cambia el API, el tutor usa un modelo flash por defecto.
"""

from __future__ import annotations

import os
from typing import Any, Optional

import streamlit as st
from google import genai
from google.genai import types


def _obtener_api_key() -> Optional[str]:
    api_key = None
    try:
        if "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
    except (Exception, FileNotFoundError):
        pass
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY")
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


def obtener_modelo_robusto(client: genai.Client) -> str:
    """
    Elige un modelo con `generateContent`, priorizando variantes *flash* en el catálogo.
    Si la lista falla, devuelve un id estable conocido por la API de desarrollador.
    """
    preferido: Optional[str] = None
    respaldo: Optional[str] = None
    try:
        for m in client.models.list(config=types.ListModelsConfig(page_size=200)):
            if not _modelo_soporta_generate_content(m.supported_actions):
                continue
            name = (m.name or "").strip()
            if not name:
                continue
            short = name.split("/")[-1]
            if respaldo is None:
                respaldo = short
            if "flash" in short.lower():
                preferido = short
                break
        if preferido:
            return preferido
        if respaldo:
            return respaldo
    except Exception:
        pass
    return "gemini-2.0-flash"


def _modelo_preferido_configurado() -> Optional[str]:
    """
    Permite fijar modelo sin sondear catálogo remoto en el arranque.
    Mejora la estabilidad de despliegue en Streamlit Cloud.
    """
    m = (os.environ.get("GEMINI_MODEL") or "").strip()
    if m:
        return m
    try:
        if "GEMINI_MODEL" in st.secrets:
            sec = str(st.secrets["GEMINI_MODEL"]).strip()
            if sec:
                return sec
    except (Exception, FileNotFoundError):
        pass
    return None


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

    def generate_content(self, prompt_parts: Any) -> Any:
        return self._client.models.generate_content(
            model=self._model_name,
            contents=prompt_parts,
            config=self._gen_config,
        )


def iniciar_modelo():
    api_key = _obtener_api_key()
    if not api_key:
        st.error("No hay API key de Gemini configurada.")
        return None, None
    try:
        client = genai.Client(api_key=api_key)
        # Evita depender de `list_models()` al arrancar; si no hay override,
        # usamos un modelo flash estable.
        nombre_modelo = _modelo_preferido_configurado() or "gemini-2.0-flash"
        gen_cfg = types.GenerateContentConfig(
            temperature=0.1,
            top_p=0.95,
        )
        model = _GeneradorGeminiCompat(client, nombre_modelo, gen_cfg)
        return model, nombre_modelo
    except Exception as e:
        st.error(f"Error iniciando modelo: {e}")
        return None, None
