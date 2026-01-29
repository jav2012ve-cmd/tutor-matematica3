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
elif ruta == "c) Autoevaluación (Quiz)":
    st.markdown("### 📝 Centro de Evaluación")

    # --- PANTALLA 1: CONFIGURACIÓN (Si no hay quiz activo) ---
    if not st.session_state.quiz_activo:
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏆 Generar Primer Parcial (8 preguntas)"):
                st.session_state.config_temas = temario.TEMAS_PARCIAL_1
                st.session_state.config_cant = 8
                st.session_state.trigger_quiz = True
                
        with col2:
            if st.button("🏆 Generar Segundo Parcial (8 preguntas)"):
                st.session_state.config_temas = temario.TEMAS_PARCIAL_2
                st.session_state.config_cant = 8
                st.session_state.trigger_quiz = True
        
        st.divider()
        st.write("O selecciona temas específicos:")
        temas_custom = st.multiselect("Selecciona temas:", temario.LISTA_TEMAS)
        
        if st.button("▶️ Iniciar Quiz Personalizado (5 preguntas)"):
            if not temas_custom:
                st.error("Selecciona al menos un tema.")
            else:
                st.session_state.config_temas = temas_custom
                st.session_state.config_cant = 5
                st.session_state.trigger_quiz = True

        # --- LÓGICA DE GENERACIÓN ---
        if st.session_state.get("trigger_quiz"):
            with st.spinner("🧠 El profesor está redactando tu examen..."):
                try:
                    prompt_quiz = temario.generar_prompt_quiz(
                        st.session_state.config_temas, 
                        st.session_state.config_cant
                    )
                    respuesta = model.generate_content(prompt_quiz)
                    datos_quiz = limpiar_json(respuesta.text)
                    
                    # Inicializamos el Quiz
                    st.session_state.preguntas_quiz = datos_quiz
                    st.session_state.indice_pregunta = 0
                    st.session_state.respuestas_usuario = []
                    st.session_state.quiz_activo = True
                    st.session_state.trigger_quiz = False # Reset trigger
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generando el quiz. Intenta de nuevo. Detalles: {e}")

    # --- PANTALLA 2: RESPONDIENDO EL QUIZ ---
    else:
        # Verificamos si terminamos
        total_preguntas = len(st.session_state.preguntas_quiz)
        
        if st.session_state.indice_pregunta < total_preguntas:
            # Recuperamos la pregunta actual
            pregunta_actual = st.session_state.preguntas_quiz[st.session_state.indice_pregunta]
            
            # Barra de progreso
            progreso = (st.session_state.indice_pregunta + 1) / total_preguntas
            st.progress(progreso, text=f"Pregunta {st.session_state.indice_pregunta + 1} de {total_preguntas}")
            
            st.markdown(f"#### {pregunta_actual['pregunta']}")
            
            # Botones de opción
            opcion_elegida = st.radio("Selecciona una opción:", pregunta_actual['opciones'], key=f"radio_{st.session_state.indice_pregunta}")
            
            if st.button("Responder"):
                es_correcta = (opcion_elegida == pregunta_actual['respuesta_correcta'])
                
                # Feedback inmediato
                if es_correcta:
                    st.success("✅ ¡Correcto!")
                    puntos = 20 / total_preguntas
                else:
                    st.error(f"❌ Incorrecto. La respuesta era: {pregunta_actual['respuesta_correcta']}")
                    st.info(f"💡 Explicación: {pregunta_actual['explicacion']}")
                    puntos = 0
                
                # --- CORRECCIÓN AQUÍ ---
                # Hacemos el redondeo fuera del diccionario para evitar el error
                puntos_redondeados = round(puntos, 2)

                # Guardamos resultado
                st.session_state.respuestas_usuario.append({
                    "pregunta": pregunta_actual['pregunta'],
                    "elegida": opcion_elegida,
                    "correcta": pregunta_actual['respuesta_correcta'],
                    "puntos": puntos_redondeados
                })
                # -----------------------
                
                # Avanzamos y recargamos
                time.sleep(2) 
                st.session_state.indice_pregunta += 1
                st.rerun()
                
        # --- PANTALLA 3: RESULTADOS FINALES ---
        else:
            st.balloons()
            st.header("📊 Resultados del Examen")
            
            score_total = sum(item['puntos'] for item in st.session_state.respuestas_usuario)
            st.metric(label="Calificación Final", value=f"{score_total}/20 Puntos")
            
            # Tabla de detalles
            st.write("### Detalle de respuestas:")
            for i, item in enumerate(st.session_state.respuestas_usuario):
                color = "🟢" if item['puntos'] > 0 else "🔴"
                st.write(f"{color} **P{i+1}:** {item['pregunta']}")
                st.caption(f"Tu respuesta: {item['elegida']} | Correcta: {item['correcta']}")
                st.divider()
            
            # Botón para generar reporte TXT
            reporte_texto = f"REPORTE DE CALIFICACIONES - MATEMÁTICAS III\n"
            reporte_texto += f"Calificación: {score_total}/20\n\n"
            for item in st.session_state.respuestas_usuario:
                reporte_texto += f"Pregunta: {item['pregunta']}\n"
                reporte_texto += f"Respuesta: {item['elegida']} (Puntos: {item['puntos']})\n---\n"
                
            st.download_button(
                label="📥 Descargar Reporte",
                data=reporte_texto,
                file_name="reporte_quiz.txt",
                mime="text/plain"
            )
            
            if st.button("🔄 Comenzar Nuevo Quiz"):
                st.session_state.quiz_activo = False
                st.session_state.indice_pregunta = 0
                st.session_state.respuestas_usuario = []
                st.rerun()