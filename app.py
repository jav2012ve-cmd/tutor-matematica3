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
# LÓGICA C: AUTOEVALUACIÓN (Quiz) - MODO HÍBRIDO AUTOMÁTICO
# =======================================================
elif ruta == "c) Autoevaluación (Quiz)":
    st.markdown("### 📝 Centro de Evaluación")

    # --- PANTALLA 1: CONFIGURACIÓN ---
    if not st.session_state.quiz_activo:
        # Mensaje simplificado (ya no hay botones de selección de fuente)
        st.info("Configura tu prueba (El sistema combinará ejercicios oficiales y generados por IA):")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏆 Generar Primer Parcial (Simulacro)", use_container_width=True):
                st.session_state.config_temas = temario.TEMAS_PARCIAL_1
                # Usamos 5 para probar rápido, puedes subirlo a 8 o 10 luego
                st.session_state.config_cant = 5 
                st.session_state.trigger_quiz = True
                st.rerun()
                
        with col2:
            if st.button("🏆 Generar Segundo Parcial (Simulacro)", use_container_width=True):
                st.session_state.config_temas = temario.TEMAS_PARCIAL_2
                st.session_state.config_cant = 5
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
                    st.session_state.trigger_quiz = True
                    st.rerun()

        # --- LÓGICA DE GENERACIÓN (MEZCLA 50/50) ---
        if st.session_state.get("trigger_quiz"):
            with st.spinner("Compilando examen (Balanceando 50% Banco Oficial / 50% IA)..."):
                try:
                    import random
                    from modules import banco_preguntas
                    
                    lista_final_preguntas = []
                    cantidad_total = st.session_state.config_cant
                    temas = st.session_state.config_temas

                    # 1. CALCULAR CUOTAS (Regla: 50% y 50%. Si es impar, 1 más a la IA)
                    cuota_banco = cantidad_total // 2
                    cuota_ia = cantidad_total - cuota_banco

                    # 2. OBTENER DEL BANCO FIJO (Intentar llenar la cuota)
                    # Solicitamos exactamente la cuota calculada
                    preguntas_banco = banco_preguntas.obtener_preguntas_fijas(temas, cuota_banco)
                    lista_final_preguntas.extend(preguntas_banco)
                    
                    # 3. AJUSTAR FALTANTES (Fallback)
                    # Si el banco no tenía suficientes (ej. pedimos 2 y solo halló 1),
                    # sumamos lo que falta a la cuota de la IA para llegar al total.
                    encontradas_banco = len(preguntas_banco)
                    faltantes_banco = cuota_banco - encontradas_banco
                    
                    total_a_generar_ia = cuota_ia + faltantes_banco
                    
                    # 4. GENERAR CON IA
                    if total_a_generar_ia > 0:
                        prompt_quiz = temario.generar_prompt_quiz(temas, total_a_generar_ia)
                        respuesta = model.generate_content(prompt_quiz)
                        preguntas_ia = limpiar_json(respuesta.text)
                        lista_final_preguntas.extend(preguntas_ia)
                    
                    # 5. MEZCLAR Y GUARDAR
                    random.shuffle(lista_final_preguntas)
                    
                    # Recorte de seguridad (por si la IA generó de más)
                    lista_final_preguntas = lista_final_preguntas[:cantidad_total]

                    # Guardar en estado
                    st.session_state.preguntas_quiz = lista_final_preguntas
                    st.session_state.indice_pregunta = 0
                    st.session_state.respuestas_usuario = []
                    st.session_state.quiz_activo = True
                    st.session_state.trigger_quiz = False
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Ocurrió un error generando el examen: {e}")
                    st.session_state.trigger_quiz = False

    # --- PANTALLA 2 (RESPONDER) y 3 (RESULTADOS) ---
    else:
        total = len(st.session_state.preguntas_quiz)
        actual = st.session_state.indice_pregunta
        
        # Si aún quedan preguntas
        if actual < total:
            pregunta_data = st.session_state.preguntas_quiz[actual]
            
            st.progress((actual) / total, text=f"Pregunta {actual + 1} de {total}")
            st.markdown(f"#### {pregunta_data['pregunta']}")
            
            # Verificamos si ya respondió esta pregunta
            ya_respondido = len(st.session_state.respuestas_usuario) > actual
            
            # -- Estado: Usuario Responde --
            if not ya_respondido:
                # Usamos radio sin index por defecto para obligar a elegir
                opcion = st.radio(
                    "Selecciona:", 
                    pregunta_data['opciones'], 
                    key=f"radio_{actual}",
                    index=None
                )
                
                if st.button("Responder", type="primary"):
                    if opcion:
                        # --- CORRECCIÓN DE LETRAS (A vs A) ---
                        letra_usuario = opcion.strip()[0].upper()
                        letra_correcta = pregunta_data['respuesta_correcta'].strip()[0].upper()
                        es_correcta = (letra_usuario == letra_correcta)
                        # -------------------------------------

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
            
            # -- Estado: Feedback --
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

        # --- PANTALLA 3: RESULTADOS (Vista de Impresión) ---
        # --- PANTALLA 3: RESULTADOS (Vista de Impresión) ---
        else:
            # st.balloons()  <-- ELIMINADA POR SERIEDAD ACADÉMICA
            
            # Encabezado de resultados
            if nota_final >= 10:
                st.success("✅ Examen Finalizado")
            else:
                st.warning("⚠️ Examen Finalizado")
            
            # Cálculo de nota
            suma_puntos = sum(r['puntos'] for r in st.session_state.respuestas_usuario)
            nota_final = round(suma_puntos, 2)
            
            # --- BLOQUE DE NOTA SUPERIOR ---
            col_nota_top, col_info_top = st.columns([1, 2])
            with col_nota_top:
                st.metric("Calificación Final", f"{nota_final} / 20 pts")
            with col_info_top:
                st.info("💡 **Para guardar reporte:** Presiona `Ctrl + P` en tu navegador y selecciona 'Guardar como PDF'.")

            st.divider()
            st.subheader("📄 Detalle del Examen")

            # Renderizado del detalle
            for i, r in enumerate(st.session_state.respuestas_usuario):
                st.markdown(f"#### 🔹 Pregunta {i+1} ({r['puntos']} pts)")
                st.markdown(r['pregunta']) # Enunciado LaTeX
                
                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    if r['es_correcta']:
                        st.success(f"✅ **Tu respuesta:** {r['elegida']}")
                    else:
                        st.error(f"❌ **Tu respuesta:** {r['elegida']}")
                
                with col_res2:
                    if not r['es_correcta']:
                        st.warning(f"✔ **Correcta:** {r['correcta']}")

                st.markdown("**📝 Explicación:**")
                st.write(r['explicacion']) 
                st.markdown("---")

            # --- BLOQUE DE NOTA INFERIOR ---
            st.markdown("### 🏁 Resumen Final")
            col_nota_bot, col_info_bot = st.columns([1, 2])
            with col_nota_bot:
                st.metric("Calificación Final ", f"{nota_final} / 20 pts")
            with col_info_bot:
                st.info("💡 **Recordatorio:** Presiona `Ctrl + P` para guardar esta pantalla como tu constancia.")

            st.divider()

            # Botón de reinicio
            col_b, _, _ = st.columns([1, 2, 1])
            with col_b:
                if st.button("🔄 Comenzar Nuevo Examen", type="primary"):
                    st.session_state.quiz_activo = False
                    st.session_state.indice_pregunta = 0
                    st.session_state.respuestas_usuario = []
                    st.rerun()