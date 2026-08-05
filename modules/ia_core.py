import streamlit as st
import google.generativeai as genai

def configurar_gemini():
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        return True
    else:
        st.error(
            "⚠️ **Falta la API Key de Google (Gemini).**\n\n"
            "Para que el tutor funcione, configura la clave en los Secrets de Streamlit:\n"
            "  `GOOGLE_API_KEY = \"tu-clave-aqui\"`\n\n"
            "Obtén la clave en [Google AI Studio](https://aistudio.google.com/apikey)."
        )
        return False

def obtener_modelo_robusto():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'flash' in m.name: 
                    return m.name
        for m in genai.list_models():
             if 'generateContent' in m.supported_generation_methods: 
                 return m.name
        return "gemini-1.5-flash"
    except Exception:
        return "gemini-1.5-flash"

def iniciar_modelo():
    if not configurar_gemini():
        return None, None
    
    nombre_modelo = obtener_modelo_robusto()
    try:
        model = genai.GenerativeModel(
            model_name=nombre_modelo,
            generation_config={"temperature": 0.3}
        )
        return model, nombre_modelo
    except Exception as e:
        st.error(f"Error iniciando modelo: {e}")
        return None, None
