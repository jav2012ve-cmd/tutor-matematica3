# modules/temario.py
from modules import banco_muestras # <--- NUEVA LÍNEA IMPORTANTE
# --- LISTAS DE TEMAS ---
TEMAS_PARCIAL_1 = [
    "1.1.1 Integrales Directas",
    "1.1.2 Cambios de variables (Sustitución)",
    "1.1.3 División de Polinomios",
    "1.1.4 Fracciones Simples",
    "1.1.7 Integral por partes",
    "1.2.1 Áreas entre curvas",
    "1.2.2 Excedentes del consumidor y productor"
]

TEMAS_PARCIAL_2 = [
    "2.1.1 ED 1er Orden: Separación de Variables",
    "2.1.2 ED 1er Orden: Homogéneas",
    "2.1.3 ED 1er Orden: Exactas",
    "2.1.4 ED 1er Orden: Lineales",
    "2.2.1 ED Orden Superior: Homogéneas",
    "2.3 Aplicaciones de Ecuaciones Diferenciales en Economía"
]

# Unimos todo para el menú general
LISTA_TEMAS = TEMAS_PARCIAL_1 + TEMAS_PARCIAL_2

# --- CONTENIDO TEÓRICO (Resumido para el ejemplo) ---
CONTENIDO_TEORICO = {
    "1.1.1 Integrales Directas": {
        "definicion": r"f(x) = \int g(x) dx \iff \frac{d}{dx}[f(x)] = g(x)",
        "propiedades": [
            r"\int [f(x) \pm g(x)] dx = \int f(x) dx \pm \int g(x) dx",
            r"\int C \cdot f(x) dx = C \int f(x) dx"
        ],
        "tabla_col1": [
            r"\int x^n dx = \frac{x^{n+1}}{n+1}",
            r"\int e^{x} dx = e^{x}"
        ],
        "tabla_col2": [
            r"\int \frac{1}{x} dx = \ln|x|",
            r"\int \sin(x) dx = -\cos(x)"
        ]
    }
    # ... (Puedes ir agregando el resto poco a poco)
}

CONTEXTO_BASE = """
Actúa como un profesor titular de Matemáticas III (Economía UCAB).
Tus pilares son Cálculo Integral y Ecuaciones Diferenciales.
Sé riguroso pero cercano.
"""

# --- NUEVO: Prompt Estructurado para el Quiz ---
# --- NUEVO: Prompt Estructurado con "Few-Shot Learning" ---
def generar_prompt_quiz(temas_seleccionados, cantidad):
    return f"""
    ACTÚA COMO PROFESOR DE MATEMÁTICAS III PARA ECONOMISTAS.
    
    TU TAREA:
    Genera un examen de {cantidad} preguntas de selección simple.
    
    TEMAS A EVALUAR: 
    {', '.join(temas_seleccionados)}.
    
    ESTILO Y DIFICULTAD (IMPORTANTE):
    A continuación te muestro ejemplos reales de cómo evaluamos en este curso. 
    Usa estos ejemplos como referencia para calibrar la dificultad y el tono de tus preguntas.
    No copies los ejemplos, crea nuevos basados en esa lógica.
    
    --- INICIO DE EJEMPLOS REALES ---
    {banco_muestras.EJEMPLOS_ESTILO}
    --- FIN DE EJEMPLOS REALES ---
    
    FORMATO DE SALIDA OBLIGATORIO (JSON):
    Responde EXCLUSIVAMENTE con un JSON válido. Sin texto extra.
    
    Estructura del JSON:
    [
        {{
            "pregunta": "Enunciado claro y riguroso...",
            "opciones": ["Opción A", "Opción B", "Opción C"],
            "respuesta_correcta": "La opción correcta literal",
            "explicacion": "Justificación matemática paso a paso..."
        }},
        ...
    ]
    """