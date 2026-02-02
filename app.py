import streamlit as st
import json
import time
import re   
from PIL import Image
from modules import ia_core, interfaz, temario, banco_preguntas

# --- 1. CONFIGURACIÓN ---
interfaz.configurar_pagina()

if not ia_core.configurar_gemini():
    st.stop()

model, nombre_modelo = ia_core.iniciar_modelo()

# --- FUNCIONES DE SEGURIDAD Y UTILIDADES (CORREGIDAS) ---

def generar_contenido_seguro(prompt, intentos_max=3):
    """
    Intenta llamar a la IA. Si falla por error 429 (Quota), espera y reintenta.
    """
    errores_recientes = ""
    for i in range(intentos_max):
        try:
            # CORRECCIÓN: Llamamos a 'model', NO a la función misma (evita recursión infinita)
            return model.generate_content(prompt)
        except Exception as e:
            errores_recientes = str(e)
            if "429" in str(e):
                tiempo_espera = 4 * (i + 1)
                st.toast(f"🚦 Tráfico alto en la IA. Reintentando en {tiempo_espera}s...", icon="⏳")
                time.sleep(tiempo_espera)
            else:
                time.sleep(1)
    
    st.error(f"❌ No se pudo conectar tras {intentos_max} intentos. Error: {errores_recientes}")
    return None

def limpiar_json(texto):
    """ Limpia el JSON y repara errores de LaTeX """
    if not texto: return []
    texto = texto.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        try:
            # CORRECCIÓN: Parche para que las fórmulas LaTeX (con \) no rompan el JSON
            texto_reparado = texto.replace("\\", "\\\\")
            return json.loads(texto_reparado)
        except:
            return [] 

def generar_tutor_paso_a_paso(pregunta_texto, tema):
    """ Genera la tutoría asegurando el formato LaTeX """
    prompt = f"""
    Actúa como un profesor experto de cálculo. Para el siguiente ejercicio de {tema}:
    "{pregunta_texto}"
    
    Genera un objeto JSON estricto.
    IMPORTANTE: Usa DOBLE BARRA (\\\\) para comandos LaTeX (ej. \\\\frac, \\\\int).
    
    Estructura JSON:
    {{
        "estrategias": ["Estrategia Correcta", "Estrategia Incorrecta 1", "Estrategia Incorrecta 2"],
        "indice_correcta": 0,
        "feedback_estrategia": "Explicación breve.",
        "paso_intermedio": "Ecuación LaTeX (con \\\\) del hito",
        "resultado_final": "Ecuación LaTeX (con \\\\) del resultado"
    }}
    Orden aleatorio en estrategias. Solo devuelve el JSON.
    """
    response = generar_contenido_seguro(prompt)
    if response:
        return limpiar_json(response.text)
    return None

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

# --- 3. INTERFAZ ---
ruta, tema_actual = interfaz.mostrar_sidebar()
interfaz.mostrar_bienvenida()

# =======================================================
# LÓGICA A: MODO ENTRENAMIENTO (Dojo Matemático)
# =======================================================
if ruta == "a) Entrenamiento (Temario)":
    st.markdown("### 🥋 Dojo de Matemáticas (Entrenamiento Guiado)")
    st.info("Resolución paso a paso: **1. Elegir Estrategia** -> **2. Hito Intermedio** -> **3. Resultado Final**.")

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
                # CORRECCIÓN: Usamos una bandera para el rerun fuera del try/except
                cargar_exito = False 
                with st.spinner("Preparando tu serie de ejercicios..."):
                    try:
                        import random
                        lista_entrenamiento = []
                        
                        # 1. Banco de Preguntas (Protegido)
                        try:
                            preguntas_banco = banco_preguntas.obtener_preguntas_fijas(temas_entrenamiento, 2)
                            if preguntas_banco:
                                lista_entrenamiento.extend(preguntas_banco)
                        except Exception as e:
                            print(f"Aviso: Banco no disponible {e}")

                        # 2. Generación IA (Protegida)
                        faltantes = 5 - len(lista_entrenamiento)
                        if faltantes > 0:
                            prompt_train = temario.generar_prompt_quiz(temas_entrenamiento, faltantes)
                            respuesta_ia = generar_contenido_seguro(prompt_train)
                            
                            if respuesta_ia:
                                preguntas_ia = limpiar_json(respuesta_ia.text)
                                if preguntas_ia: 
                                    lista_entrenamiento.extend(preguntas_ia)
                        
                        if not lista_entrenamiento:
                            st.error("No se encontraron preguntas. Intenta con otro tema.")
                        else:
                            random.shuffle(lista_entrenamiento)
                            st.session_state.entrenamiento_lista = lista_entrenamiento[:5]
                            st.session_state.entrenamiento_idx = 0
                            st.session_state.entrenamiento_step = 1
                            st.session_state.entrenamiento_data_ia = None
                            st.session_state.entrenamiento_validado = False 
                            st.session_state.entrenamiento_activo = True
                            cargar_exito = True

                    except Exception as e:
                        st.error(f"Error técnico al iniciar: {e}")
                
                # Ejecutamos el rerun FUERA del try para evitar el TypeError
                if cargar_exito:
                    st.rerun()

    # --- PANTALLA DE EJERCICIOS (El Dojo) ---
    else:
        idx = st.session_state.entrenamiento_idx
        lista = st.session_state.entrenamiento_lista
        
        if idx < len(lista):
            ejercicio = lista[idx]
            
            st.progress((idx + 1) / 5, text=f"Ejercicio {idx + 1} de 5")
            st.markdown(f"**Tema:** `{ejercicio.get('tema', 'General')}`")
            st.markdown(f"### {ejercicio['pregunta']}")
            st.divider()

            # --- LLAMADA A LA IA TUTOR ---
            if st.session_state.entrenamiento_data_ia is None:
                with st.spinner("🧠 El profesor está analizando el mejor camino de resolución..."):
                    datos_tutor = generar_tutor_paso_a_paso(ejercicio['pregunta'], ejercicio.get('tema', 'Cálculo'))
                    if datos_tutor:
                        st.session_state.entrenamiento_data_ia = datos_tutor
                        st.rerun()
                    else:
                        st.error("Error conectando con el tutor IA. Saltando ejercicio.")
                        st.session_state.entrenamiento_idx += 1
                        time.sleep(2)
                        st.rerun()
            
            tutor = st.session_state.entrenamiento_data_ia
            step = st.session_state.entrenamiento_step

            # PASO 1: ESTRATEGIA
            if step == 1:
                st.markdown("#### 1️⃣ Paso 1: Selección de Estrategia")
                st.write("Antes de calcular, ¿cuál crees que es el camino correcto?")
                
                opcion_estrategia = st.radio("Selecciona el método:", tutor['estrategias'], index=None, key=f"radio_estrat_{idx}")
                
                if st.button("Validar Estrategia", key=f"btn_val_{idx}"):
                    if opcion_estrategia:
                        idx_seleccionado = tutor['estrategias'].index(opcion_estrategia)
                        if idx_seleccionado == tutor['indice_correcta']:
                            st.session_state.entrenamiento_validado = True 
                        else:
                            st.error("❌ Mmm, no es el mejor camino.")
                            st.warning(f"Pista: {tutor['feedback_estrategia']}")
                    else:
                        st.warning("Debes seleccionar una opción.")

                if st.session_state.get("entrenamiento_validado", False):
                    st.success("✅ ¡Exacto! Esa es la ruta.")
                    st.info(f"👨‍🏫 **Feedback:** {tutor['feedback_estrategia']}")
                    
                    if st.button("Ir al Paso Intermedio ➡️", type="primary", key=f"btn_go_step2_{idx}"):
                        st.session_state.entrenamiento_step = 2
                        st.session_state.entrenamiento_validado = False
                        st.rerun()

            # PASO 2: HITO INTERMEDIO
            if step == 2:
                st.success(f"✅ Estrategia: {tutor['estrategias'][tutor['indice_correcta']]}")
                st.markdown("#### 2️⃣ Paso 2: Ejecución Intermedia")
                st.write("Aplica la estrategia. Deberías llegar a una expresión similar a esta:")
                
                st.info(f"**Hito Intermedio:**\n\n$${tutor['paso_intermedio']}$$")
                st.write("¿Lograste llegar a este punto o algo equivalente?")
                
                col_si, col_no = st.columns(2)
                with col_si:
                    if st.button("👍 Sí, lo tengo", key=f"btn_si_{idx}"):
                        st.session_state.entrenamiento_step = 3
                        st.rerun()
                with col_no:
                    if st.button("👎 No, necesito ayuda", key=f"btn_no_{idx}"):
                        st.error("Revisa tus derivadas/integrales básicas o el álgebra.")

            # PASO 3: FINAL
            if step == 3:
                st.success(f"✅ Estrategia Correcta | ✅ Hito Intermedio Alcanzado")
                st.markdown("#### 3️⃣ Paso 3: Resolución Final")
                st.write("El resultado definitivo es:")
                
                st.success(f"### {tutor['resultado_final']}")
                with st.expander("Ver explicación completa"):
                    st.write(ejercicio.get('explicacion', 'Procedimiento estándar aplicado correctamente.'))

                if st.button("Siguiente Ejercicio ➡️", type="primary", key=f"btn_next_{idx}"):
                    st.session_state.entrenamiento_idx += 1
                    st.session_state.entrenamiento_step = 1
                    st.session_state.entrenamiento_data_ia = None 
                    st.session_state.entrenamiento_validado = False
                    st.rerun()

        else:
            st.success("🎉 ¡Entrenamiento completado!")
            if st.button("🔄 Volver al Inicio", key="btn_reset_entrenamiento"):
                st.session_state.entrenamiento_activo = False
                st.session_state.entrenamiento_idx = 0
                st.rerun()

# =======================================================
# LÓGICA B: CONSULTAS (Respuesta Guiada)
# =======================================================
elif ruta == "b) Respuesta Guiada (Consultas)":
    st.info("Sube tu ejercicio o escribe tu duda.")
    
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
                res = generar_contenido_seguro(f"Ayuda al alumno con esto: {prompt}")
                if res:
                    st.markdown(res.text)
                    st.session_state.messages.append({"role": "assistant", "content": res.text})
                else:
                    st.error("El tutor está ocupado. Intenta de nuevo.")

# =======================================================
# LÓGICA C: AUTOEVALUACIÓN (Quiz)
# =======================================================
elif ruta == "c) Autoevaluación (Quiz)":
    st.markdown("### 📝 Centro de Evaluación")

    # --- PANTALLA 1: CONFIGURACIÓN ---
    if not st.session_state.quiz_activo:
        st.info("Configura tu prueba (El sistema combinará ejercicios oficiales y generados por IA):")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏆 Generar Primer Parcial (Simulacro)", use_container_width=True):
                st.session_state.config_temas = temario.TEMAS_PARCIAL_1
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

        # --- LÓGICA DE GENERACIÓN ---
        if st.session_state.get("trigger_quiz"):
            # Usamos bandera para evitar error de rerun dentro de try
            quiz_generado = False
            with st.spinner("Compilando examen (Balanceando 50% Banco Oficial / 50% IA)..."):
                try:
                    import random
                    lista_final_preguntas = []
                    cantidad_total = st.session_state.config_cant
                    temas = st.session_state.config_temas

                    cuota_banco = cantidad_total // 2
                    cuota_ia = cantidad_total - cuota_banco

                    # 1. Banco
                    try:
                        preguntas_banco = banco_preguntas.obtener_preguntas_fijas(temas, cuota_banco)
                        if preguntas_banco:
                            lista_final_preguntas.extend(preguntas_banco)
                    except: pass
                    
                    # 2. IA
                    falta = cantidad_total - len(lista_final_preguntas)
                    if falta > 0:
                        prompt_quiz = temario.generar_prompt_quiz(temas, falta)
                        respuesta = generar_contenido_seguro(prompt_quiz)
                        if respuesta:
                            preguntas_ia = limpiar_json(respuesta.text)
                            if preguntas_ia:
                                lista_final_preguntas.extend(preguntas_ia)
                    
                    random.shuffle(lista_final_preguntas)
                    lista_final_preguntas = lista_final_preguntas[:cantidad_total]

                    if not lista_final_preguntas:
                         st.error("No se pudieron generar preguntas.")
                         st.session_state.trigger_quiz = False
                    else:
                        st.session_state.preguntas_quiz = lista_final_preguntas
                        st.session_state.indice_pregunta = 0
                        st.session_state.respuestas_usuario = []
                        st.session_state.quiz_activo = True
                        st.session_state.trigger_quiz = False
                        quiz_generado = True
                    
                except Exception as e:
                    st.error(f"Error generando examen: {e}")
                    st.session_state.trigger_quiz = False
            
            if quiz_generado:
                st.rerun()

    # --- PANTALLA 2 (RESPONDER) y 3 (RESULTADOS) ---
    else:
        total = len(st.session_state.preguntas_quiz)
        actual = st.session_state.indice_pregunta
        
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
                
                if ultimo_dato['es_correcta']:
                    st.success("✅ ¡Correcto!")
                else:
                    st.error(f"❌ Incorrecto. La correcta era: {ultimo_dato['correcta']}")
                
                with st.expander("💡 Ver Explicación", expanded=True):
                    st.write(ultimo_dato['explicacion'])
                
                if st.button("Siguiente Pregunta ➡️", type="primary"):
                    st.session_state.indice_pregunta += 1
                    st.rerun()

        else:
            # PANTALLA 3: RESULTADOS
            suma_puntos = sum(r['puntos'] for r in st.session_state.respuestas_usuario)
            nota_final = round(suma_puntos, 2)

            if nota_final >= 10:
                st.success(f"✅ Examen Finalizado - Aprobado con {nota_final}")
            else:
                st.warning(f"⚠️ Examen Finalizado - Nota: {nota_final}")
            
            col_nota_top, col_info_top = st.columns([1, 2])
            with col_nota_top:
                st.metric("Calificación Final", f"{nota_final} / 20 pts")
            with col_info_top:
                st.info("💡 **Recordatorio:** Presiona `Ctrl + P` para guardar.")

            st.divider()
            st.subheader("📄 Detalle del Examen")

            for i, r in enumerate(st.session_state.respuestas_usuario):
                st.markdown(f"#### 🔹 Pregunta {i+1} ({r['puntos']} pts)")
                st.markdown(r['pregunta']) 
                
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

            st.markdown("### 🏁 Resumen Final")
            col_nota_bot, col_info_bot = st.columns([1, 2])
            with col_nota_bot:
                st.metric("Calificación Final ", f"{nota_final} / 20 pts")
            
            st.divider()

            if st.button("🔄 Comenzar Nuevo Examen", type="primary"):
                st.session_state.quiz_activo = False
                st.session_state.indice_pregunta = 0
                st.session_state.respuestas_usuario = []
                st.rerun()