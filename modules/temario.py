# modules/temario.py
from modules import banco_muestras # <--- NUEVA LÍNEA IMPORTANTE
# --- LISTAS DE TEMAS ---
TEMAS_PARCIAL_1 = [
    "1.1.1 Integrales Directas",
    "1.1.2 Cambios de variables (Sustitución)",
    "1.1.3 División de Polinomios",
    "1.1.4 Fracciones Simples",
    "1.1.5 Integral por partes",
    "1.2.1 Áreas entre curvas",
    "1.2.2 Excedentes del consumidor y productor",
    "1.2.3 Integrales Impropias", 
    "1.2.4 Volúmenes de Sólidos de Revolución",
    "1.2.5 Integrales Dobles"
]

TEMAS_PARCIAL_2 = [
    "2.1.1 ED 1er Orden: Separación de Variables",
    "2.1.2 ED 1er Orden: Homogéneas",
    "2.1.3 ED 1er Orden: Exactas",
    "2.1.4 ED 1er Orden: Lineales",
    "2.1.5 Aplicaciones de Ecuaciones Diferenciales en Economía",
    "2.2.1 ED Orden Superior: Homogéneas",
    "2.2.2 ED Orden Superior: No Homogéneas",
    "2.2.3 Aplicaciones de Ecuaciones Diferenciales de Orden superior"   
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
    
    REGLAS OBLIGATORIAS:
    1. CADA pregunta debe tener EXACTAMENTE 4 OPCIONES (A, B, C, D).
    2. Las opciones deben ser plausibles (distractores matemáticos comunes).
    3. NO incluyas notas aclaratorias o pistas en el enunciado. Sé directo y riguroso.
    
    TEMAS A EVALUAR: 
    {', '.join(temas_seleccionados)}.
    
    ESTILO (Referencia):
    Usa estos ejemplos para calibrar el tono, PERO GENERA TUS PROPIOS EJERCICIOS:
    --- INICIO EJEMPLOS ---
    {banco_muestras.EJEMPLOS_ESTILO}
    --- FIN EJEMPLOS ---
    
    FORMATO DE SALIDA (JSON PURO):
    [
        {{
            "pregunta": "Enunciado LaTeX...",
            "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."],
            "respuesta_correcta": "La opción correcta literal",
            "explicacion": "Explicación paso a paso..."
        }},
        ...
    ]
    """