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
if "quiz_activo" not in st.session_state:
    st.session_state.quiz_activo = False
if "preguntas_quiz" not in st.session_state:
    st.session_state.preguntas_quiz = []
if "indice_pregunta" not in st.session_state:
    st.session_state.indice_pregunta = 0
if "respuestas_usuario" not in st.session_state:
    st.session_state.respuestas_usuario = [] 
if "messages" not in st.session_state:
    st.session_state.messages = []

# Función auxiliar para limpiar JSON
def limpiar_json(texto):
    texto = texto.replace("```json", "").replace("```", "").strip()
    return json.loads(texto)

# --- 3. INTERFAZ ---
ruta, tema_actual = interfaz.mostrar_sidebar()
interfaz.mostrar_bienvenida()

# =======================================================
# LÓGICA A: ENTRENAMIENTO (Temario)
# =======================================================
if ruta == "a) Entrenamiento (Temario)":
    st.header(f"📘 {tema_actual}")
    if tema_actual in temario.CONTENIDO_TEORICO:
        data = temario.CONTENIDO_TEORICO[tema_actual]
        st.markdown("#### Definición")
        st.latex(data["definicion"])
        # Aquí puedes agregar más visualización teórica si quieres
    else:
        st.info(f"Explorando el tema: {tema_actual}")
        
    # Chat simple para este modo
    prompt = st.chat_input("Dudas sobre este tema...")
    if prompt:
        with st.spinner("Pensando..."):
            res = model.generate_content(f"Explica {tema_actual}: {prompt}")
            st.write(res.text)

# =======================================================
# LÓGICA B: CONSULTAS (Respuesta Guiada)
# =======================================================
elif ruta == "b) Respuesta Guiada (Consultas)":
    st.info("Sube tu ejercicio o escribe tu duda.")
    
    # Historial de Chat (Solo visualización)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Escribe tu consulta...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Analizando..."):
                res = model.generate_content(f"Ayuda al alumno con esto: {prompt}")
                st.markdown(res.text)
                st.session_state.messages.append({"role": "assistant", "content": res.text})

# =======================================================
# LÓGICA C: AUTOEVALUACIÓN (Quiz) - VERSIÓN HÍBRIDA
# =======================================================
elif ruta == "c) Autoevaluación (Quiz)":
    st.markdown("### 📝 Centro de Evaluación")

    # --- PANTALLA 1: CONFIGURACIÓN ---
    if not st.session_state.quiz_activo:
        st.info("Configura tu prueba:")
        
        # 1. SELECCIÓN DE FUENTE (NUEVO)
        origen_datos = st.radio(
            "Origen de las preguntas:",
            ["🤖 Generar con IA (Infinitas)", "uD83D\uDCC1 Banco de Preguntas Oficial (Fijas)"],
            horizontal=True
        )
        
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏆 Generar Primer Parcial (Simulacro)", use_container_width=True):
                st.session_state.config_temas = temario.TEMAS_PARCIAL_1
                st.session_state.config_cant = 5 # Bajamos a 5 para probar rápido
                st.session_state.origen_seleccionado = origen_datos
                st.session_state.trigger_quiz = True
                st.rerun()
                
        with col2:
            if st.button("🏆 Generar Segundo Parcial (Simulacro)", use_container_width=True):
                st.session_state.config_temas = temario.TEMAS_PARCIAL_2
                st.session_state.config_cant = 5
                st.session_state.origen_seleccionado = origen_datos
                st.session_state.trigger_quiz = True
                st.rerun()

        with st.expander("⚙️ Personalizado"):
            temas_custom = st.multiselect("Temas:", temario.LISTA_TEMAS)
            if st.button("▶️ Iniciar Quiz Custom"):
                if not temas_custom:
                    st.error("Selecciona tema.")
                else:
                    st.session_state.config_temas = temas_custom
                    st.session_state.config_cant = 5
                    st.session_state.origen_seleccionado = origen_datos
                    st.session_state.trigger_quiz = True
                    st.rerun()

        # --- LÓGICA DE GENERACIÓN (MODIFICADA) ---
        if st.session_state.get("trigger_quiz"):
            with st.spinner("Preparando evaluación..."):
                try:
                    nuevas_preguntas = []
                    
                    # CASO A: BANCO FIJO
                    if "Banco" in st.session_state.origen_seleccionado:
                        from modules import banco_preguntas
                        nuevas_preguntas = banco_preguntas.obtener_preguntas_fijas(
                            st.session_state.config_temas,
                            st.session_state.config_cant
                        )
                        if not nuevas_preguntas:
                            st.warning("⚠️ No encontré preguntas fijas para esos temas. Generando con IA...")
                            # Fallback a IA si no hay preguntas fijas
                            st.session_state.origen_seleccionado = "IA" 
                    
                    # CASO B: GENERACIÓN IA (O Fallback)
                    if "IA" in st.session_state.origen_seleccionado or not nuevas_preguntas:
                        from modules import banco_muestras
                        prompt_quiz = temario.generar_prompt_quiz(
                            st.session_state.config_temas, 
                            st.session_state.config_cant
                        )
                        respuesta = model.generate_content(prompt_quiz)
                        nuevas_preguntas = limpiar_json(respuesta.text)
                    
                    # Guardar en estado
                    st.session_state.preguntas_quiz = nuevas_preguntas
                    st.session_state.indice_pregunta = 0
                    st.session_state.respuestas_usuario = []
                    st.session_state.quiz_activo = True
                    st.session_state.trigger_quiz = False
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.session_state.trigger_quiz = False

    # --- PANTALLA 2 (RESPONDER) y 3 (RESULTADOS) ---
    # (El resto del código se mantiene IGUAL porque la estructura de datos es idéntica)
    else:
        # ... (Mantén aquí todo el código original desde el 'else:' de la línea 106 de tu app.py original)
        # ... (Incluyendo lógica de radio buttons, feedback, resultados, balloons, etc.)
        # ... COPIA Y PEGA EL RESTO DEL ARCHIVO ORIGINAL AQUÍ ...
        
        # Como referencia, el código que sigue es el de renderizado visual
        # que NO necesita cambios porque 'st.session_state.preguntas_quiz'
        # ya tiene los datos cargados (sea de IA o de tu Banco).
        
        total = len(st.session_state.preguntas_quiz)
        actual = st.session_state.indice_pregunta
        
        # Si aún quedan preguntas
        if actual < total:
            pregunta_data = st.session_state.preguntas_quiz[actual]
            
            st.progress((actual) / total, text=f"Pregunta {actual + 1} de {total}")
            st.markdown(f"#### {pregunta_data['pregunta']}")
            
            ya_respondido = len(st.session_state.respuestas_usuario) > actual
            
            if not ya_respondido:
                opcion = st.radio("Selecciona:", pregunta_data['opciones'], key=f"radio_{actual}", index=None)
                if st.button("Responder", type="primary"):
                    if opcion:
                        letra_usuario = opcion.strip()[0].upper()
                        letra_correcta = pregunta_data['respuesta_correcta'].strip()[0].upper()
                        es_correcta = (letra_usuario == letra_correcta)
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
                        st.warning("⚠️ Selecciona una opción.")
            else:
                ultimo_dato = st.session_state.respuestas_usuario[actual]
                st.info(f"Tu respuesta: **{ultimo_dato['elegida']}**")
                if ultimo_dato['es_correcta']: st.success("✅ ¡Correcto!")
                else: st.error(f"❌ Incorrecto. La correcta era: {ultimo_dato['correcta']}")
                with st.expander("💡 Ver Explicación", expanded=True): st.write(ultimo_dato['explicacion'])
                if st.button("Siguiente Pregunta ➡️", type="primary"):
                    st.session_state.indice_pregunta += 1
                    st.rerun()
        else:
            st.balloons()
            st.success("¡Examen Finalizado!")
            suma_puntos = sum(r['puntos'] for r in st.session_state.respuestas_usuario)
            nota_final = round(suma_puntos, 2)
            col_nota_top, col_info_top = st.columns([1, 2])
            with col_nota_top: st.metric("Calificación Final", f"{nota_final} / 20 pts")
            with col_info_top: st.info("💡 **Para guardar reporte:** Presiona `Ctrl + P`.")
            st.divider()
            st.subheader("📄 Detalle del Examen")
            for i, r in enumerate(st.session_state.respuestas_usuario):
                st.markdown(f"#### 🔹 Pregunta {i+1} ({r['puntos']} pts)")
                st.markdown(r['pregunta']) 
                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    if r['es_correcta']: st.success(f"✅ **Tu respuesta:** {r['elegida']}")
                    else: st.error(f"❌ **Tu respuesta:** {r['elegida']}")
                with col_res2:
                    if not r['es_correcta']: st.warning(f"✔ **Correcta:** {r['correcta']}")
                st.markdown("**📝 Explicación:**")
                st.write(r['explicacion']) 
                st.markdown("---")
            col_b, _, _ = st.columns([1, 2, 1])
            with col_b:
                if st.button("🔄 Comenzar Nuevo Examen", type="primary"):
                    st.session_state.quiz_activo = False
                    st.session_state.indice_pregunta = 0
                    st.session_state.respuestas_usuario = []
                    st.rerun()