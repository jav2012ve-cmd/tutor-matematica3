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

def generar_tutor_paso_a_paso(pregunta_texto, tema):
    """
    Toma una pregunta y genera:
    1. Estrategias (1 correcta, 2 distractores).
    2. Paso intermedio.
    3. Solución final.
    """
    prompt = f"""
    Actúa como un profesor experto de cálculo. Para el siguiente ejercicio de {tema}:
    "{pregunta_texto}"
    
    Genera un objeto JSON estricto con esta estructura para guiar al estudiante:
    {{
        "estrategias": [
            "Descripción breve de la estrategia CORRECTA (ej. Usar partes con u=x)",
            "Estrategia plausible pero INCORRECTA o menos eficiente",
            "Otra estrategia incorrecta"
        ],
        "indice_correcta": 0,
        "feedback_estrategia": "Explicación breve de por qué esa es la mejor ruta.",
        "paso_intermedio": "Ecuación LaTeX del resultado a mitad de camino (ej. después de integrar pero antes de evaluar)",
        "resultado_final": "Ecuación LaTeX del resultado final"
    }}
    El orden de las estrategias en la lista debe ser aleatorio, ajusta el "indice_correcta" según corresponda.
    Solo devuelve el JSON.
    """
    try:
        response = model.generate_content(prompt)
        return limpiar_json(response.text)
    except:
        return None
# --- 3. INTERFAZ ---
ruta, tema_actual = interfaz.mostrar_sidebar()
interfaz.mostrar_bienvenida()

# =======================================================
# LÓGICA A: MODO ENTRENAMIENTO (Dojo Matemático - 3 Momentos)
# =======================================================
if ruta == "a) Entrenamiento (Temario)":
    st.markdown("### 🥋 Dojo de Matemáticas (Entrenamiento Guiado)")
    st.info("Resolución paso a paso: **1. Elegir Estrategia** -> **2. Hito Intermedio** -> **3. Resultado Final**.")

    # Inicializar variables de sesión exclusivas para este modo si no existen
    if "entrenamiento_activo" not in st.session_state:
        st.session_state.entrenamiento_activo = False

    # --- PANTALLA 0: CONFIGURACIÓN ---
    if not st.session_state.entrenamiento_activo:
        temas_entrenamiento = st.multiselect(
            "🎯 Selecciona los temas a practicar:",
            options=temario.LISTA_TEMAS,
            placeholder="Ej. Ecuaciones Diferenciales Lineales..."
        )

        if st.button("⚡ Iniciar Sesión (5 Ejercicios)", type="primary", use_container_width=True):
            if not temas_entrenamiento:
                st.error("⚠️ Selecciona al menos un tema.")
            else:
                with st.spinner("Preparando tu serie de ejercicios..."):
                    try:
                        import random
                        from modules import banco_preguntas
                        
                        lista_entrenamiento = []
                        # Regla: 2 Banco + 3 IA
                        # Intentamos sacar 2 del banco
                        preguntas_banco = banco_preguntas.obtener_preguntas_fijas(temas_entrenamiento, 2)
                        lista_entrenamiento.extend(preguntas_banco)
                        
                        # Rellenamos con IA hasta llegar a 5
                        faltantes = 5 - len(lista_entrenamiento)
                        if faltantes > 0:
                            prompt_train = temario.generar_prompt_quiz(temas_entrenamiento, faltantes)
                            respuesta_ia = model.generate_content(prompt_train)
                            preguntas_ia = limpiar_json(respuesta_ia.text)
                            lista_entrenamiento.extend(preguntas_ia)
                        
                        random.shuffle(lista_entrenamiento)
                        
                        # Configurar la sesión de entrenamiento
                        st.session_state.entrenamiento_lista = lista_entrenamiento[:5]
                        st.session_state.entrenamiento_idx = 0
                        st.session_state.entrenamiento_step = 1  # 1: Estrategia, 2: Intermedio, 3: Final
                        st.session_state.entrenamiento_data_ia = None # Datos del tutor (estrategias, pasos)
                        st.session_state.entrenamiento_activo = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al iniciar: {e}")

    # --- PANTALLA DE EJERCICIOS (El Dojo) ---
    else:
        # Recuperar ejercicio actual
        idx = st.session_state.entrenamiento_idx
        lista = st.session_state.entrenamiento_lista
        
        if idx < len(lista):
            ejercicio = lista[idx]
            
            # Encabezado
            st.progress((idx + 1) / 5, text=f"Ejercicio {idx + 1} de 5")
            st.markdown(f"**Tema:** `{ejercicio.get('tema', 'General')}`")
            st.markdown(f"### {ejercicio['pregunta']}")
            st.divider()

            # --- LLAMADA A LA IA TUTOR (Solo la primera vez por ejercicio) ---
            if st.session_state.entrenamiento_data_ia is None:
                with st.spinner("🧠 El profesor está analizando el mejor camino de resolución..."):
                    datos_tutor = generar_tutor_paso_a_paso(ejercicio['pregunta'], ejercicio.get('tema', 'Cálculo'))
                    if datos_tutor:
                        st.session_state.entrenamiento_data_ia = datos_tutor
                        st.rerun()
                    else:
                        st.error("Error conectando con el tutor IA. Saltando ejercicio.")
                        st.session_state.entrenamiento_idx += 1
                        st.rerun()
            
            # Recuperamos los datos generados por la IA
            tutor = st.session_state.entrenamiento_data_ia
            step = st.session_state.entrenamiento_step

            # ====================================================
            # MOMENTO 1: IDENTIFICAR PROCEDIMIENTO
            # ====================================================
            if step == 1:
                st.markdown("#### 1️⃣ Paso 1: Selección de Estrategia")
                st.write("Antes de calcular, ¿cuál crees que es el camino correcto?")
                
                # Radio button para seleccionar estrategia
                opcion_estrategia = st.radio(
                    "Selecciona el método:",
                    tutor['estrategias'],
                    index=None,
                    key=f"estrat_{idx}"
                )
                
                if st.button("Validar Estrategia"):
                    if opcion_estrategia:
                        # Buscar el índice de la opción seleccionada
                        idx_seleccionado = tutor['estrategias'].index(opcion_estrategia)
                        
                        if idx_seleccionado == tutor['indice_correcta']:
                            st.success("✅ ¡Exacto! Esa es la ruta.")
                            st.info(f"👨‍🏫 **Feedback:** {tutor['feedback_estrategia']}")
                            if st.button("Ir al Paso Intermedio ➡️", type="primary"):
                                st.session_state.entrenamiento_idx += 1
                                st.session_state.entrenamiento_step = 1
                                st.session_state.entrenamiento_data_ia = None 
                                st.session_state.entrenamiento_validado = False
                                st.rerun()
                        else:
                            st.error("❌ Mmm, no es el mejor camino.")
                            st.warning("Pista: Revisa bien las condiciones del problema.")
                    else:
                        st.warning("Selecciona una opción.")

            # ====================================================
            # MOMENTO 2: RESULTADO INTERMEDIO
            # ====================================================
            if step == 2:
                # Recordatorio de la estrategia
                st.success(f"✅ Estrategia: {tutor['estrategias'][tutor['indice_correcta']]}")
                
                st.markdown("#### 2️⃣ Paso 2: Ejecución Intermedia")
                st.write("Aplica la estrategia seleccionada. Deberías llegar a una expresión similar a esta:")
                
                st.info(f"**Hito Intermedio:**\n\n$${tutor['paso_intermedio']}$$")
                
                st.write("¿Lograste llegar a este punto o algo equivalente?")
                
                col_si, col_no = st.columns(2)
                with col_si:
                    if st.button("👍 Sí, lo tengo"):
                        st.session_state.entrenamiento_step = 3
                        st.rerun()
                with col_no:
                    if st.button("👎 No, necesito ayuda"):
                        st.error("Revisa tus derivadas/integrales básicas o el álgebra.")

            # ====================================================
            # MOMENTO 3: RESULTADO FINAL
            # ====================================================
            if step == 3:
                st.success(f"✅ Estrategia Correcta | ✅ Hito Intermedio Alcanzado")
                st.markdown("#### 3️⃣ Paso 3: Resolución Final")
                st.write("Finalmente, simplifica y evalúa si es necesario. El resultado definitivo es:")
                
                st.success(f"### {tutor['resultado_final']}")
                
                with st.expander("Ver explicación completa del ejercicio"):
                    st.write(ejercicio.get('explicacion', 'Procedimiento estándar aplicado correctamente.'))

                if st.button("Siguiente Ejercicio ➡️", type="primary"):
                    st.session_state.entrenamiento_idx += 1
                    st.session_state.entrenamiento_step = 1
                    st.session_state.entrenamiento_data_ia = None # Limpiar para el siguiente
                    st.rerun()

        else:
            # --- FIN DE LA SERIE ---
            st.success("🎉 ¡Entrenamiento de 5 ejercicios completado!")
            st.write("Has practicado la toma de decisiones estratégicas y la resolución técnica.")
            
            # BOTÓN DE REINICIO TOTAL
            if st.button("🔄 Volver al Inicio (Reiniciar Todo)", type="primary"):
                st.session_state.clear()  # <--- ESTO BORRA TODA LA MEMORIA
                st.rerun()                # <--- ESTO RECARGA LA APP DESDE CERO

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
        else:
            # 1. PRIMERO calculamos la nota (para que la variable exista)
            suma_puntos = sum(r['puntos'] for r in st.session_state.respuestas_usuario)
            nota_final = round(suma_puntos, 2)

            # 2. AHORA sí podemos usar 'nota_final' en el condicional
            if nota_final >= 10:
                st.success(f"✅ Examen Finalizado - Aprobado con {nota_final}")
            else:
                st.warning(f"⚠️ Examen Finalizado - Nota: {nota_final}")
            
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