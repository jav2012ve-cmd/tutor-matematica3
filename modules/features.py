"""
Banderas de coste / modos caros vía Streamlit Secrets o variables de entorno.

Por defecto los modos siguen habilitados (comportamiento actual).
Para un curso grande, el profesor puede desactivar los más costosos en Secrets.

Parsing cuidadoso: en Secrets TOML puede llegar bool nativo; en env siempre str.
"""

from __future__ import annotations

import os
from typing import Any, Optional

import streamlit as st

# Mensajes en español si el alumno llega a un modo desactivado.
MSG_TUTOR_ABIERTAS_OFF = (
    "⛔ **Tutor: Preguntas Abiertas** está desactivado temporalmente "
    "por control de costes de la cátedra. Usa **Entrenamiento** o **Autoevaluación (Quiz)**."
)
MSG_MANUSCRITOS_OFF = (
    "⛔ **Corrección de Manuscritos** está desactivada temporalmente "
    "por control de costes de la cátedra. Usa **Entrenamiento** o **Autoevaluación (Quiz)**."
)
MSG_RESPUESTA_GUIADA_IMAGEN_OFF = (
    "📸 La **carga de fotos** en Respuesta Guiada está desactivada por control de costes. "
    "Puedes seguir escribiendo el enunciado en texto."
)


def _leer_raw(nombre: str) -> Any:
    """Lee un valor de Secrets (si existe) o del entorno. None si no está definido."""
    try:
        if nombre in st.secrets:
            return st.secrets[nombre]
    except Exception:
        pass
    if nombre in os.environ:
        return os.environ.get(nombre)
    return None


def _como_bool(valor: Any, default: bool) -> bool:
    """
    Interpreta bools de Streamlit Secrets / env.
    Acepta: True/False, 1/0, "true"/"false", "yes"/"no", "on"/"off", "1"/"0".
    """
    if valor is None:
        return default
    if isinstance(valor, bool):
        return valor
    if isinstance(valor, (int, float)) and not isinstance(valor, bool):
        return bool(valor)
    s = str(valor).strip().lower()
    if s in ("", "none", "null"):
        return default
    if s in ("1", "true", "t", "yes", "y", "on", "si", "sí"):
        return True
    if s in ("0", "false", "f", "no", "n", "off"):
        return False
    return default


def _flag_desactivar(
    disable_key: str,
    feature_key: Optional[str] = None,
) -> bool:
    """
    True si el modo debe desactivarse.

    Prioridad:
    1. DISABLE_* definido → su valor (true = off)
    2. FEATURE_* definido → false = off, true = on
    3. Sin definir → feature habilitada (no desactivar)
    """
    raw_disable = _leer_raw(disable_key)
    if raw_disable is not None:
        return _como_bool(raw_disable, default=False)

    if feature_key:
        raw_feature = _leer_raw(feature_key)
        if raw_feature is not None:
            # FEATURE_*=false → desactivar
            return not _como_bool(raw_feature, default=True)

    return False


def tutor_abiertas_desactivado() -> bool:
    """Desactiva el chat de Tutor: Preguntas Abiertas."""
    return _flag_desactivar("DISABLE_TUTOR_ABIERTAS", "FEATURE_TUTOR_ABIERTAS")


def manuscritos_desactivado() -> bool:
    """Desactiva Corrección de Manuscritos."""
    return _flag_desactivar("DISABLE_MANUSCRITOS", "FEATURE_MANUSCRITOS")


def respuesta_guiada_imagen_desactivada() -> bool:
    """
    Desactiva solo la carga de imagen en Respuesta Guiada.
    El flujo por texto sigue disponible.
    """
    return _flag_desactivar(
        "DISABLE_RESPUESTA_GUIADA_IMAGEN",
        "FEATURE_RESPUESTA_GUIADA_IMAGEN",
    )


def hay_restricciones_coste() -> bool:
    """True si al menos una bandera de coste está activa."""
    return (
        tutor_abiertas_desactivado()
        or manuscritos_desactivado()
        or respuesta_guiada_imagen_desactivada()
    )


def resumen_restricciones() -> list[str]:
    """Lista corta de modos restringidos (para nota admin / sidebar)."""
    items: list[str] = []
    if tutor_abiertas_desactivado():
        items.append("Tutor: Preguntas Abiertas")
    if manuscritos_desactivado():
        items.append("Corrección de Manuscritos")
    if respuesta_guiada_imagen_desactivada():
        items.append("Fotos en Respuesta Guiada")
    return items
