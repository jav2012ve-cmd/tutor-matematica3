import streamlit as st
from PIL import Image
# Importamos nuestros módulos propios
from modules import ia_core, interfaz, temario

# 1. Configuración Inicial
interfaz.configurar_pagina()

if not ia_core.configurar_gemini():
    st.stop()

model, nombre_modelo = ia_core.iniciar_modelo()

# 2. Inicialización de Sesión
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hola. Soy tu tutor virtual de Matemáticas III. ¿En qué trabajaremos hoy?"
    })

if "modo_actual" not in st.session_state:
    st.session_state.modo_actual = None

# 3. Interfaz Lateral y Navegación
ruta, tema_actual = interfaz.mostrar_sidebar()

# 4. Interfaz Principal
interfaz.mostrar_bienvenida()

if ruta is None:
    st.info("⬅️ Selecciona una opción en el menú para comenzar.")
    st.stop()

# --- LÓGICA DE CONTENIDO ---
contexto_sistema = temario.CONTEXTO_BASE

if ruta == "a) Entrenamiento (Temario)":
    if tema_actual in temario.CONTENIDO_TEORICO:
        data = temario.CONTENIDO_TEORICO[tema_actual]
        st.subheader(tema_actual)
        st.markdown("#### 1. Definición")
        st.latex(data["definicion"])
        
        st.markdown("#### 2. Propiedades")
        c1, c2 = st.columns(2)
        with c1: st.latex(data["propiedades"][0])
        with c2: st.latex(data["propiedades"][1])
        
        st.markdown("#### 3. Fórmulas")
        with st.expander("Ver Tabla", expanded=True):
            tc1, tc2 = st.columns(2)
            with tc1: 
                for eq in data["tabla_col1"]: st.latex(eq)
            with tc2: 
                for eq in data["tabla_col2"]: st.latex(eq)
    
    if tema_actual.startswith("1.1.1"):
        prompt_inicio = "Actúa como Profesor. Propón UN ejercicio sencillo de tabla directa."
    else:
        prompt_inicio = f"Explica la aplicación económica de {tema_actual}."
        
    contexto_sistema += f"\nTema actual: {tema_actual}"

elif ruta == "b) Respuesta Guiada (Consultas)":
    st.info("Sube tu ejercicio o escribe tu duda.")
    contexto_sistema += "\nModo: Resolución de dudas y guía paso a paso."

else:
    contexto_sistema += "\nModo: Generar Quiz de 8 preguntas variadas."

st.divider()

# --- CHAT BOT ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

imagen_upload = None
if ruta == "b) Respuesta Guiada (Consultas)":
    imagen_upload = st.file_uploader("Adjuntar imagen", type=["png", "jpg", "jpeg"])

prompt = st.chat_input("Escribe aquí...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
        if imagen_upload:
            st.image(imagen_upload, width=300)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            full_prompt = f"SISTEMA: {contexto_sistema}\n\nUSUARIO: {prompt}"
            if imagen_upload:
                img = Image.open(imagen_upload)
                response = model.generate_content([full_prompt, img])
            else:
                chat = model.start_chat(history=[])
                response = chat.send_message(full_prompt)
            
            placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            placeholder.error(f"Error: {e}")