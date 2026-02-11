import streamlit as st
from modules.temario import LISTA_TEMAS

def configurar_pagina():
    st.set_page_config(
        page_title="Matemáticas III - Economía UCAB",
        page_icon="📈",
        layout="wide"
    )

def mostrar_sidebar():
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/f/f0/Logo_UCAB_H.png", width=200)
        st.markdown("### 🏛️ Escuela de Economía")
        
        seleccion_visual = st.radio(
            "1. Selecciona tu Modo de Estudio:",
            ["a) Entrenamiento (Temario)", 
             "b) Respuesta Guiada (Consultas)", 
             "c) Autoevaluación (Quiz)",
             "d) Tutor: Preguntas Abiertas"],
            index=None,
            key="radio_seleccion"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Iniciar"):
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

        return st.session_state.get("modo_actual"), tema_seleccionado

def mostrar_bienvenida():
    st.title("Matemáticas III - Economía UCAB")
    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #00aeef;">
        <h4>👋 Bienvenidos al curso</h4>
        <p>Centrado en: <strong>Cálculo Integral</strong> y <strong>Ecuaciones Diferenciales</strong>.</p>
    </div>
    <hr>
    """, unsafe_allow_html=True)