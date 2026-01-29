import streamlit as st
import json
import time
from PIL import Image
from modules import ia_core, interfaz, temario

# --- 1. CONFIGURACIÓN ---
interfaz.configurar_pagina()

if not ia_core.configurar_gemini():
    st.stop()

model, nombre_modelo = ia_core.iniciar_modelo()

# --- 2. GESTIÓN DE ESTADO (MEMORIA) ---
# Aquí guardamos las variables que deben sobrevivir a las recargas de página
if "quiz_activo" not in st.session_state:
    st.session_state.quiz_activo = False
if "preguntas_quiz" not in st.session_state:
    st.session_state.preguntas_quiz = []
if "indice_pregunta" not in st.session_state:
    st.session_state.indice_pregunta = 0
if "respuestas_usuario" not in st.session_state:
    st.session_state.respuestas_usuario = [] # Guardaremos {pregunta, elegida, correcta, puntos}
if "messages" not in st.session_state:
    st.session_state.messages = []

# Función auxiliar para limpiar JSON de la IA
def limpiar_json(texto):
    texto = texto.replace("```json", "").replace("```", "").strip()
    return json.loads(texto)

# --- 3. INTERFAZ ---
ruta, tema_actual = interfaz.mostrar_sidebar()
interfaz.mostrar_bienvenida()

# =======================================================
# LÓGICA A: ENTRENAMIENTO (Mantenemos igual)
# =======================================================
if ruta == "a) Entrenamiento (Temario)":
    st.header(f"📘 {tema_actual}")
    if tema_actual in temario.CONTENIDO_TEORICO:
        data = temario.CONTENIDO_TEORICO[tema_actual]
        st.markdown("#### Definición")
        st.latex(data["definicion"])
        # ... (puedes completar con el código de tablas que ya tenías)
    else:
        st.info(f"Explorando el tema: {tema_actual}")
        
    # Chat simple para este modo
    prompt = st.chat_input("Dudas sobre este tema...")
    if prompt:
        res = model.generate_content(f"Explica {tema_actual}: {prompt}")
        st.write(res.text)

# =======================================================
# LÓGICA B: CONSULTAS (Mantenemos igual)
# =======================================================
elif ruta == "b) Respuesta Guiada (Consultas)":
    st.info("Sube tu ejercicio o escribe tu duda.")
    prompt = st.chat_input("Escribe tu consulta...")
    if prompt:
        res = model.generate_content(f"Ayuda al alumno con esto: {prompt}")
        st.markdown(res.text)

# =======================================================
# LÓGICA C: AUTOEVALUACIÓN (¡NUEVO!)
# =======================================================
# =======================================================
# LÓGICA C: AUTOEVALUACIÓN (MEJORADO)
# =======================================================
elif ruta == "c) Autoevaluación (Quiz)":
    st.markdown("### 📝 Centro de Evaluación")

    # --- PANTALLA 1: CONFIGURACIÓN (Solo si NO hay quiz activo) ---
    if not st.session_state.quiz_activo:
        st.info("Selecciona el tipo de prueba para comenzar:")
        
        # Botones grandes para los Parciales
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏆 Generar Primer Parcial (8 preguntas)", use_container_width=True):
                st.session_state.config_temas = temario.TEMAS_PARCIAL_1
                st.session_state.config_cant = 8
                st.session_state.trigger_quiz = True
                st.rerun() # Forzamos recarga para ocultar opciones inmediatamente
                
        with col2:
            if st.button("🏆 Generar Segundo Parcial (8 preguntas)", use_container_width=True):
                st.session_state.config_temas = temario.TEMAS_PARCIAL_2
                st.session_state.config_cant = 8
                st.session_state.trigger_quiz = True
                st.rerun()

        # Opción Personalizada "Escondida" en un desplegable para no ensuciar
        with st.expander("⚙️ Opciones Personalizadas (Avanzado)"):
            st.write("Selecciona temas específicos:")
            temas_custom = st.multiselect("Temas:", temario.LISTA_TEMAS)
            if st.button("▶️ Iniciar Quiz Personalizado"):
                if not temas_custom:
                    st.error("Selecciona al menos un tema.")
                else:
                    st.session_state.config_temas = temas_custom
                    st.session_state.config_cant = 5
                    st.session_state.trigger_quiz = True
                    st.rerun()

        # --- LÓGICA DE GENERACIÓN (Invisible al usuario) ---
        if st.session_state.get("trigger_quiz"):
            with st.spinner("🧠 El profesor está redactando tu examen..."):
                try:
                    # Usamos el nuevo cerebro de muestras
                    from modules import banco_muestras
                    
                    prompt_quiz = temario.generar_prompt_quiz(
                        st.session_state.config_temas, 
                        st.session_state.config_cant
                    )
                    respuesta = model.generate_content(prompt_quiz)
                    datos_quiz = limpiar_json(respuesta.text)
                    
                    # Inicializamos variables de estado del Quiz
                    st.session_state.preguntas_quiz = datos_quiz
                    st.session_state.indice_pregunta = 0
                    st.session_state.respuestas_usuario = []
                    st.session_state.quiz_activo = True
                    st.session_state.trigger_quiz = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generando: {e}")
                    st.session_state.trigger_quiz = False

    # --- PANTALLA 2: RESPONDIENDO EL QUIZ ---
    else:
        # Barra de progreso superior
        total = len(st.session_state.preguntas_quiz)
        actual = st.session_state.indice_pregunta
        
        if actual < total:
            pregunta_data = st.session_state.preguntas_quiz[actual]
            
            # Mostramos progreso
            st.progress((actual) / total, text=f"Pregunta {actual + 1} de {total}")
            st.markdown(f"#### {pregunta_data['pregunta']}")
            
            # --- ESTADO A: Usuario aún no responde ---
            # Verificamos si ya tenemos respuesta para este índice
            ya_respondido = len(st.session_state.respuestas_usuario) > actual
            
            if not ya_respondido:
                # Mostramos opciones (usamos key dinámico para resetear selección)
                opcion = st.radio(
                    "Selecciona:", 
                    pregunta_data['opciones'], 
                    key=f"radio_{actual}",
                    index=None
                )
                
                if st.button("Responder", type="primary"):
                    if opcion:
                        # Calculamos puntos
                        es_correcta = (opcion == pregunta_data['respuesta_correcta'])
                        pts = round(20 / total, 2) if es_correcta else 0
                        
                        # Guardamos
                        st.session_state.respuestas_usuario.append({
                            "pregunta": pregunta_data['pregunta'],
                            "elegida": opcion,
                            "correcta": pregunta_data['respuesta_correcta'],
                            "explicacion": pregunta_data['explicacion'],
                            "puntos": pts,
                            "es_correcta": es_correcta
                        })
                        st.rerun() # Recargamos para mostrar feedback
                    else:
                        st.warning("Por favor selecciona una opción.")
            
            # --- ESTADO B: Usuario ya respondió (Feedback estático) ---
            else:
                # Recuperamos la última respuesta guardada
                ultimo_dato = st.session_state.respuestas_usuario[actual]
                
                # Deshabilitamos el radio mostrando qué eligió
                st.info(f"Tu respuesta: **{ultimo_dato['elegida']}**")
                
                if ultimo_dato['es_correcta']:
                    st.success("✅ ¡Correcto!")
                else:
                    st.error(f"❌ Incorrecto. La respuesta correcta es: {ultimo_dato['correcta']}")
                
                # Explicación pedagógica (siempre visible ahora)
                with st.expander("💡 Ver Explicación del Profesor", expanded=True):
                    st.write(ultimo_dato['explicacion'])
                
                # BOTÓN SIGUIENTE (El usuario controla el tiempo)
                if st.button("Siguiente Pregunta ➡️", type="primary"):
                    st.session_state.indice_pregunta += 1
                    st.rerun()

        # --- PANTALLA 3: RESULTADOS FINALES ---
        else:
            st.balloons()
            st.success("¡Examen Finalizado!")
            
            # Cálculo de nota
            suma_puntos = sum(r['puntos'] for r in st.session_state.respuestas_usuario)
            nota_final = round(suma_puntos, 2)
            st.metric("Calificación Final", f"{nota_final} / 20 pts")
            
            # --- GENERACIÓN DE DOCUMENTOS ---
            from fpdf import FPDF
            
            # 1. GENERADOR DE PDF (Reporte Rápido)
            def generar_pdf_reporte():
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, "Reporte de Autoevaluación - Matemáticas III", ln=True, align="C")
                pdf.set_font("Arial", "", 12)
                pdf.ln(10)
                pdf.cell(0, 10, f"Calificación: {nota_final}/20", ln=True)
                pdf.ln(5)
                
                for i, r in enumerate(st.session_state.respuestas_usuario):
                    pdf.set_font("Arial", "B", 11)
                    # Limpiamos un poco el texto para evitar errores de caracteres raros en PDF simple
                    pregunta_limpia = r['pregunta'].encode('latin-1', 'replace').decode('latin-1')
                    pdf.multi_cell(0, 10, f"P{i+1}: {pregunta_limpia}")
                    
                    pdf.set_font("Arial", "", 10)
                    estado = "CORRECTO" if r['es_correcta'] else "INCORRECTO"
                    pdf.cell(0, 10, f"Estado: {estado} | Puntos: {r['puntos']}")
                    pdf.ln(10)
                
                return pdf.output(dest="S").encode("latin-1")

            # 2. GENERADOR DE LATEX (Constancia Oficial Estilo UCAB)
            def generar_latex_constancia():
                tex = r"""
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{amssymb}
\begin{document}
\begin{center}
    Universidad Católica Andrés Bello \\
    Escuela de Economía - Matemáticas III \\
    \textbf{CONSTANCIA DE AUTOEVALUACIÓN}
\end{center}

\vspace{0.5cm}
\noindent \textbf{Calificación:} """ + str(nota_final) + r"""/20 pts \\
\vspace{0.5cm}

\section*{Detalle de la Prueba}
\begin{enumerate}
"""
                for r in st.session_state.respuestas_usuario:
                    # Escapamos caracteres peligrosos de LaTeX si es necesario
                    tex += r"\item \textbf{Pregunta:} " + r['pregunta'] + "\n"
                    tex += r"\begin{itemize}" + "\n"
                    tex += r"\item \textit{Respuesta del Estudiante:} " + r['elegida'] + "\n"
                    tex += r"\item \textit{Respuesta Correcta:} " + r['correcta'] + "\n"
                    tex += r"\item \textit{Puntos:} " + str(r['puntos']) + "\n"
                    tex += r"\end{itemize}" + "\n\n"

                tex += r"""
\end{enumerate}
\end{document}
"""
                return tex

            # --- BOTONES DE DESCARGA ---
            col_descarga1, col_descarga2 = st.columns(2)
            
            with col_descarga1:
                try:
                    pdf_bytes = generar_pdf_reporte()
                    st.download_button(
                        label="📄 Descargar Reporte (PDF)",
                        data=pdf_bytes,
                        file_name="reporte_notas.pdf",
                        mime="application/pdf",
                        type="primary"
                    )
                except Exception as e:
                    st.warning(f"Instala 'fpdf' para generar PDF. Error: {e}")

            with col_descarga2:
                latex_str = generar_latex_constancia()
                st.download_button(
                    label="📜 Descargar Constancia (LaTeX)",
                    data=latex_str,
                    file_name="constancia_evaluacion.tex",
                    mime="text/plain"
                )

            st.divider()
            
            # Tabla Resumen en Pantalla
            st.write("### 📊 Detalle de Resultados")
            for i, r in enumerate(st.session_state.respuestas_usuario):
                icono = "✅" if r['es_correcta'] else "❌"
                with st.expander(f"{icono} Pregunta {i+1} ({r['puntos']} pts)"):
                    st.write(f"**P:** {r['pregunta']}")
                    st.write(f"**Tuya:** {r['elegida']} | **Correcta:** {r['correcta']}")
                    st.caption(f"Explicación: {r['explicacion']}")

            if st.button("🔄 Comenzar Nuevo Examen"):
                st.session_state.quiz_activo = False
                st.session_state.indice_pregunta = 0
                st.session_state.respuestas_usuario = []
                st.rerun()