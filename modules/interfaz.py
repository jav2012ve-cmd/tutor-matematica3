import os
from datetime import datetime

import streamlit as st
from modules.temario import LISTA_TEMAS
from modules import uso_stats, imagen_carga

# Nombre de la aplicación (pestaña del navegador, títulos principales)
APP_DISPLAY_NAME = "Matemáticas III - Economía UCAB - Periodo Intensivo Agosto 2026 - Versión del tutor 7.0"

# Infografía de bienvenida (relativa a la raíz del proyecto, junto a app.py)
_ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
INFOGRAFIA_BIENVENIDA = os.path.join(_ASSETS_DIR, "infografia_asistente_v2.png")

def inyectar_estilo_matematico():
    """
    CSS para mejorar renderizado KaTeX y evitar que el texto matemático se rompa.
    Se ejecuta una sola vez por sesión.
    """
    if st.session_state.get("estilo_matematico_inyectado"):
        return
    st.session_state["estilo_matematico_inyectado"] = True

    st.markdown(
        """
        <style>
        /* Ajustes generales para textos con LaTeX en Markdown */
        .stMarkdown p {
            line-height: 1.6;
            overflow-wrap: anywhere;
            word-break: break-word;
        }

        /* KaTeX */
        .katex {
            font-size: 1.1em;
            max-width: 100%;
            overflow-x: auto;
            white-space: normal;
        }

        /* Contenedor que Streamlit usa para st.latex */
        .stLatex, .stLatex > div {
            max-width: 100%;
            overflow-x: auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def configurar_pagina():
    st.set_page_config(
        page_title=APP_DISPLAY_NAME,
        page_icon="📈",
        layout="wide"
    )

def _render_estadisticas_sidebar() -> None:
    """Contadores de uso y cobertura por tema (sin notas técnicas de backend)."""
    with st.expander("📊 Uso de la app"):
        warn = st.session_state.get("_uso_stats_supabase_warn")
        if warn:
            st.warning(warn)
        stats = uso_stats.obtener_estadisticas()
        if any(stats.get(m, 0) > 0 for m in uso_stats.MODULOS):
            for mod in uso_stats.MODULOS:
                n = stats.get(mod, 0)
                st.caption(f"**{mod}:** {n} consultas")
            st.caption("_Anónimo, sin identificar usuarios._")
        else:
            st.caption("_Aún no hay registros de uso._")

    with st.expander("📈 Cobertura por tema (temario)"):
        por_tema = uso_stats.obtener_estadisticas_temas()
        filas = sorted(
            [{"tema": t, "n": por_tema.get(t, 0)} for t in LISTA_TEMAS],
            key=lambda x: (-x["n"], x["tema"]),
        )
        con_uso = sum(1 for r in filas if r["n"] > 0)
        st.caption(f"Temas con al menos un registro: **{con_uso}** / {len(LISTA_TEMAS)}")
        for r in filas:
            pref = "●" if r["n"] > 0 else "○"
            st.caption(f"{pref} **{r['n']}** — {r['tema']}")


def mostrar_sidebar():
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/f/f0/Logo_UCAB_H.png", width=200)
        st.markdown("### 🏛️ Escuela de Economía")
        
        seleccion_visual = st.radio(
            "1. Selecciona tu Modo de Estudio:",
            ["a) Entrenamiento (Temario)", 
             "b) Respuesta Guiada (Consultas)", 
             "c) Autoevaluación (Quiz)",
             "d) Tutor: Preguntas Abiertas",
             "e) Corrección de Manuscritos",
             "f) Administrador (Métricas)"],
            index=None,
            key="radio_seleccion"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Iniciar"):
                if seleccion_visual:
                    # Al cambiar de modo, limpiar estado de los otros modos para evitar datos residuales
                    if seleccion_visual != st.session_state.get("modo_actual"):
                        st.session_state.quiz_activo = False
                        st.session_state.preguntas_quiz = []
                        st.session_state.indice_pregunta = 0
                        st.session_state.respuestas_usuario = []
                        if "trigger_quiz" in st.session_state:
                            st.session_state.trigger_quiz = False
                        st.session_state.entrenamiento_activo = False
                        st.session_state.consulta_step = 0
                        st.session_state.consulta_data = None
                        st.session_state.consulta_validada = False
                        st.session_state.historial_tutor_abierto = []
                        st.session_state.manuscrito_correccion = None
                    st.session_state.modo_actual = seleccion_visual
                st.rerun()
        with col2:
            if st.button("🔄 Reiniciar"):
                st.session_state.modo_actual = None
                st.session_state.messages = []
                st.rerun()
        
        st.divider()
        
        tema_seleccionado = None
        if st.session_state.get("modo_actual") == "a) Entrenamiento (Temario)":
            st.write("### 📘 Temario Detallado")
            if "tema_seleccionado" not in st.session_state:
                st.session_state.tema_seleccionado = LISTA_TEMAS[0]
            
            tema_seleccionado = st.selectbox("Selecciona el punto:", LISTA_TEMAS)
            st.session_state.tema_seleccionado = tema_seleccionado

        st.divider()
        with st.expander("📖 Ayuda / Modos"):
            _mb_ayuda = max(1, imagen_carga.MAX_UPLOAD_BYTES // (1024 * 1024))
            st.caption(
                f"Fotos en **Respuesta guiada** y **Manuscritos**: hasta {_mb_ayuda} MB por archivo; "
                "la app optimiza la imagen antes de enviarla a la IA. "
                "Al terminar, usa la retroalimentación anónima al pie de cada modo si algo falló o fue útil."
            )
            st.markdown("""
            **a) Entrenamiento:** Serie de ejercicios paso a paso (estrategia → hito → resultado); en temas con datos en el banco, **apoyo gráfico** 2D/3D en el hito intermedio.  
            **b) Respuesta Guiada:** Subes foto o texto de un ejercicio y el tutor te guía; apoyo gráfico inferido del enunciado (áreas, volúmenes, PDF).  
            **c) Autoevaluación:** Simulacro de parcial (Primer, Segundo o temas personalizados).  
            **d) Tutor abierto:** Chat sobre teoría y ejercicios; gráficos automáticos para áreas, probabilidad/PDF e integrales dobles.  
            **e) Corrección de Manuscritos:** Sube tu resolución escrita; la app identifica el enunciado, valora tu solución y sugiere ajustes (mismo tope de tamaño que en la foto guiada).
            **f) Administrador:** Métricas globales, carga de PDFs de exámenes/guías y sugerencias de quiz específico.
            """)

        _render_estadisticas_sidebar()

        return st.session_state.get("modo_actual"), tema_seleccionado

def mostrar_bienvenida():
    """Muestra la presentación inicial solo cuando aún no se ha seleccionado un modo."""
    st.title(APP_DISPLAY_NAME)

    _mb_foto = max(1, imagen_carga.MAX_UPLOAD_BYTES // (1024 * 1024))
    st.success(
        f"**Versión 7.0** — **Apoyo gráfico ampliado:** motor unificado de figuras Plotly en **Tutor Preguntas Abiertas**, "
        "**Respuesta guiada** y **Entrenamiento** para **áreas**, **probabilidad/PDF** e **integrales dobles** "
        "(región 2D + superficie 3D con proyección destacada sobre R). "
        "La inferencia lee **z**, **intervalos** y **curvas** del enunciado para mostrar la región correcta. "
        f"Se mantienen las mejoras de la v6.1: fotos hasta **{_mb_foto} MB** con optimización previa y "
        "**retroalimentación anónima** al pie de cada modo."
    )

    if os.path.isfile(INFOGRAFIA_BIENVENIDA):
        st.image(
            INFOGRAFIA_BIENVENIDA,
            width="stretch",
            caption=(
                "Ruta técnica (Gemini, Streamlit, Python, GitHub, Supabase, informe PDF) "
                "y ruta didáctica (modos de estudio, entrada por imagen, LaTeX)."
            ),
        )
    else:
        st.caption("_No se encontró la infografía en `assets/infografia_asistente_v2.png`._")

    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 25px; border-radius: 10px; border-left: 5px solid #00aeef; margin-bottom: 20px;">
        <h4 style="margin-top: 0; color: #0066cc;">🏛️ Bienvenidos al Tutor Inteligente de la Cátedra</h4>
        <p style="color: #0066cc;">Este ecosistema está diseñado para fortalecer el dominio de <strong>Cálculo Integral</strong> y <strong>Ecuaciones Diferenciales</strong> en tu formación como economista.</p>
        <p style="color: #0066cc;"><strong>Modos de estudio:</strong></p>
        <ul style="margin-bottom: 10px; color: #0066cc;">
            <li><strong>a) Entrenamiento:</strong> Serie de ejercicios paso a paso (estrategia → hito → resultado). En temas con apoyo en el banco, el hito incluye <strong>figura interactiva</strong> 2D y, en integrales dobles, vista <strong>3D</strong> del volumen.</li>
            <li><strong>b) Respuesta Guiada:</strong> Sube foto o texto de un ejercicio y el tutor te guía. Apoyo gráfico inferido del enunciado (áreas, excedentes, volúmenes, PDF).</li>
            <li><strong>c) Autoevaluación:</strong> Simulacro de parcial (Primer, Segundo o temas personalizados).</li>
            <li><strong>d) Tutor Preguntas Abiertas:</strong> Chat sobre teoría y ejercicios de la cátedra, con gráficos automáticos para áreas, probabilidad e integrales dobles.</li>
            <li><strong>e) Corrección de Manuscritos:</strong> Sube tu resolución escrita; la app identifica el enunciado, valora tu solución (correcto / parcial / incorrecto) y sugiere ajustes.</li>
            <li><strong>f) Administrador:</strong> Métricas globales, carga de PDFs (exámenes/guías), detección de temas y propuesta de quiz específico (acceso restringido).</li>
        </ul>
        <p style="color: #0066cc;">Dos pilares del curso: <strong>Cálculo Integral</strong> (métodos de integración, excedentes, áreas, volúmenes) y <strong>Ecuaciones Diferenciales</strong> (primer orden, orden superior, modelos económicos).</p>
    </div>
    
    <p style="color: #0066cc;"><strong>🛠️ Recursos</strong></p>
    <ul style="color: #0066cc;">
        <li>Temario y banco alineados por tema; informe en PDF al terminar la autoevaluación.</li>
        <li><strong>Gráficos interactivos (v7.0):</strong> Plotly en Entrenamiento, Respuesta Guiada y Tutor Abierto — áreas, PDF, regiones 2D y superficies 3D con proyección sobre R.</li>
        <li><strong>Integrales dobles (v7.0):</strong> inferencia de región y <strong>z = f(x,y)</strong> desde el texto; vista 3D con superficie en contexto y zoom.</li>
        <li><strong>Carga de fotos (v6.1):</strong> tope de <strong>""" + str(_mb_foto) + """ MB</strong> por imagen en <strong>Respuesta guiada</strong> y <strong>Corrección de manuscritos</strong>; optimización automática antes de la IA.</li>
        <li><strong>Retroalimentación (v6.1):</strong> menú anónimo al pie de cada modo; ayuda a la cátedra a corregir LaTeX, contenidos y reconocimiento de manuscritos.</li>
        <li><strong>Ejes y lectura matemática (v6.0+):</strong> ejes claros, guías visuales y mejor salida LaTeX en preguntas y explicaciones.</li>
    </ul>
    <hr style="margin-top: 20px; margin-bottom: 20px;">
    """, unsafe_allow_html=True)

    with st.expander("Novedades de hoy (actualización v7.0)", expanded=True):
        st.markdown(
            f"""
- **Motor gráfico unificado (v7.0):** en **Tutor Preguntas Abiertas** y **Respuesta guiada** se generan figuras según el tema: **áreas entre curvas**, **densidad f(x)** con intervalo sombreado, **integrales dobles** con región en el plano **xy** y vista **3D** del volumen bajo **z = f(x,y)**.

- **Vista 3D enriquecida (v7.0):** la superficie se muestra en un **dominio ampliado** (contexto tenue) y se **resalta la proyección sobre la región R**; plano base más grande que R con **zoom** por rueda del mouse.

- **Inferencia desde el enunciado (v7.0):** reconoce expresiones como **z = x² − y² + 2**, regiones entre **y = x²** y **y = 2x**, rectángulos **−3 < x < 2**, **0 < y < 3** y PDFs típicos del curso — sin depender solo de coincidencias del banco.

- **Entrenamiento 1.2.6 (v7.0):** más ejercicios con metadatos gráficos (paraboloides, regiones tipo II, volúmenes sobre rectángulos y entre curvas); tutor paso a paso con planteamientos integrales y LaTeX corregido.

- **Límite y optimización de imágenes (v6.1):** en **Respuesta guiada** y **Corrección de manuscritos** archivos de hasta **{_mb_foto} MB**; compresión antes de la IA.

- **Retroalimentación de experiencia (v6.1):** bloque anónimo **«Tu experiencia con esta funcionalidad»** en todos los modos.
            """
        )
    
    st.info("👆 **Elige un modo en el menú de la izquierda y pulsa *Iniciar* para comenzar.**")


def mostrar_cintillo_cierre():
    """Cintillo institucional de cierre para toda la app."""
    anio = datetime.now().year
    st.markdown(
        f"""
        <div style="margin-top: 28px; padding: 14px 18px; border-top: 1px solid #d9e2ec; background-color: #f8fafc; border-radius: 8px;">
            <p style="margin: 0; color: #16324f; font-size: 0.95rem; line-height: 1.45;">
                <strong>Universidad Católica Andrés Bello - Venezuela</strong> · Escuela de Economía · Cátedra de Matemáticas III
            </p>
            <p style="margin: 6px 0 0 0; color: #486581; font-size: 0.85rem; line-height: 1.4;">
                Plataforma de apoyo académico para formación en Cálculo Integral y Ecuaciones Diferenciales.
                Uso didáctico y de acompañamiento al aprendizaje. © {anio}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
