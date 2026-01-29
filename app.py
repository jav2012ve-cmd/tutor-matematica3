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
# =======================================================
# LÓGICA C: AUTOEVALUACIÓN (Quiz)
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
                st.rerun()
                
        with col2:
            if st.button("🏆 Generar Segundo Parcial (8 preguntas)", use_container_width=True):
                st.session_state.config_temas = temario.TEMAS_PARCIAL_2
                st.session_state.config_cant = 8
                st.session_state.trigger_quiz = True
                st.rerun()

        # Opción Personalizada
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
                    from modules import banco_muestras
                    
                    prompt_quiz = temario.generar_prompt_quiz(
                        st.session_state.config_temas, 
                        st.session_state.config_cant
                    )
                    respuesta = model.generate_content(prompt_quiz)
                    datos_quiz = limpiar_json(respuesta.text)
                    
                    # Inicializamos variables
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
        total = len(st.session_state.preguntas_quiz)
        actual = st.session_state.indice_pregunta
        
        if actual < total:
            pregunta_data = st.session_state.preguntas_quiz[actual]
            
            st.progress((actual) / total, text=f"Pregunta {actual + 1} de {total}")
            st.markdown(f"#### {pregunta_data['pregunta']}")
            
            # Verificamos si ya respondió esta pregunta
            ya_respondido = len(st.session_state.respuestas_usuario) > actual
            
            # --- ESTADO A: Aún no responde ---
            if not ya_respondido:
                opcion = st.radio(
                    "Selecciona:", 
                    pregunta_data['opciones'], 
                    key=f"radio_{actual}",
                    index=None
                )
                
                if st.button("Responder", type="primary"):
                    if opcion:
                        # --- CORRECCIÓN CRÍTICA: Comparar solo la letra ---
                        letra_usuario = opcion.strip()[0].upper()
                        letra_correcta = pregunta_data['respuesta_correcta'].strip()[0].upper()
                        es_correcta = (letra_usuario == letra_correcta)
                        # --------------------------------------------------

                        pts = round(20 / total, 2) if es_correcta else 0
                        
                        st.session_state.respuestas_usuario.append({
                            "pregunta": pregunta_data['pregunta'],
                            "elegida": opcion,
                            "correcta": pregunta_data['respuesta_correcta'],
                            "explicacion": pregunta_data['explicacion'],
                            "puntos": pts,
                            "es_correcta": es_correcta
                        })
                        st.rerun()
                    else:
                        st.warning("⚠️ Por favor selecciona una opción.")
            
            # --- ESTADO B: Ya respondió (Mostrar Feedback) ---
            else:
                ultimo_dato = st.session_state.respuestas_usuario[actual]
                
                st.info(f"Tu respuesta: **{ultimo_dato['elegida']}**")
                
                if ultimo_dato['es_correcta']:
                    st.success("✅ ¡Correcto!")
                else:
                    st.error(f"❌ Incorrecto. La correcta era: {ultimo_dato['correcta']}")
                
                with st.expander("💡 Ver Explicación", expanded=True):
                    st.write(ultimo_dato['explicacion'])
                
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
            
            # Encabezado de Nota
            col_nota, col_info = st.columns([1, 2])
            with col_nota:
                st.metric("Calificación Final", f"{nota_final} / 20 pts")
            with col_info:
                st.info("💡 **Para guardar tu reporte:** Presiona `Ctrl + P` (o Cmd + P) en tu navegador y selecciona 'Guardar como PDF'.")

            st.divider()
            st.subheader("📄 Detalle del Examen")

            # --- RENDERIZADO PARA IMPRESIÓN (SIN EXPANDERS) ---
            # Mostramos todo "abierto" para que al imprimir salga completo
            for i, r in enumerate(st.session_state.respuestas_usuario):
                st.markdown(f"#### 🔹 Pregunta {i+1} ({r['puntos']} pts)")
                
                # Enunciado (LaTeX se renderiza perfecto aquí)
                st.markdown(r['pregunta'])
                
                # Respuestas
                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    if r['es_correcta']:
                        st.success(f"✅ **Tu respuesta:** {r['elegida']}")
                    else:
                        st.error(f"❌ **Tu respuesta:** {r['elegida']}")
                
                with col_res2:
                    if not r['es_correcta']:
                        st.warning(f"✔ **Correcta:** {r['correcta']}")
                    else:
                        st.write("") # Espacio vacío si acertó

                # Explicación (Separada para forzar renderizado LaTeX correcto)
                st.markdown("**📝 Explicación:**")
                st.write(r['explicacion']) 
                st.markdown("---")

            # --- BOTÓN DE REINICIO ---
            # Lo ponemos al final y centrado
            st.write("")
            col_b, _, _ = st.columns([1, 2, 1])
            with col_b:
                if st.button("🔄 Comenzar Nuevo Examen", type="primary"):
                    st.session_state.quiz_activo = False
                    st.session_state.indice_pregunta = 0
                    st.session_state.respuestas_usuario = []
                    st.rerun()