"""
Menú anónimo de retroalimentación por funcionalidad (experiencia / LaTeX / errores).
"""

from __future__ import annotations

import re

import streamlit as st

from modules import uso_stats

_OPCIONES_BASE: list[tuple[str, str]] = [
    ("a", "a) App funcionó sin errores"),
    ("b", "b) App presentó algún error de LaTeX que no afectó la funcionalidad"),
    ("c", "c) App presentó errores de LaTeX que perjudicaron la funcionalidad"),
    ("d", "d) App ofreció respuestas erradas"),
]

_OPCION_IMAGEN = (
    "e",
    "e) App no pudo reconocer la información cargada en el manuscrito (imagen)",
)


def _clave_widget(funcionalidad: str, key_suffix: str) -> str:
    raw = f"retro_fb_{funcionalidad}_{key_suffix or 'default'}"
    return re.sub(r"[^0-9a-zA-Z_]", "_", raw)[:80]


def render_seccion_retroalimentacion(
    funcionalidad: str,
    *,
    incluir_opcion_imagen_manuscrito: bool = False,
    key_suffix: str = "",
) -> None:
    """
    Muestra un expander con radio + botón para registrar la experiencia (anónimo).

    ``funcionalidad``: etiqueta estable para logs (ej. ``Entrenamiento``).
    ``incluir_opcion_imagen_manuscrito``: añade la opción e) solo en flujos con carga de imagen.
    """
    opts = list(_OPCIONES_BASE)
    if incluir_opcion_imagen_manuscrito:
        opts.append(_OPCION_IMAGEN)

    base = _clave_widget(funcionalidad, key_suffix)
    labels = [lab for _, lab in opts]
    code_by_label = {lab: code for code, lab in opts}

    with st.expander("📋 Tu experiencia con esta funcionalidad", expanded=False):
        st.caption(
            "Anónimo y opcional, pero **muy importante** para la cátedra: cada registro ayuda a "
            "priorizar correcciones de LaTeX, calidad de respuestas del tutor y lectura de manuscritos o fotos. "
            "Si puedes, indícalo al terminar la sesión."
        )
        seleccion = st.radio(
            "Indica la opción que mejor describe tu caso:",
            options=labels,
            key=f"{base}_radio",
            horizontal=False,
        )
        if st.button(
            "Registrar retroalimentación",
            key=f"{base}_btn",
            type="secondary",
            width="stretch",
        ):
            codigo = code_by_label.get(seleccion or "", "")
            if codigo:
                uso_stats.registrar_retroalimentacion_experiencia(
                    funcionalidad,
                    codigo,
                    incluir_opcion_e_permitida=incluir_opcion_imagen_manuscrito,
                )
                st.success("Gracias. Se guardó tu retroalimentación.")
