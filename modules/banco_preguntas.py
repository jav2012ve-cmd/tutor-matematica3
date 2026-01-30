import random

# ESTRUCTURA:
# Cada ejercicio debe tener: "tema", "pregunta" (LaTeX soportado), 
# "opciones" (Lista de 4), "respuesta_correcta" (Texto exacto de la opción correcta) y "explicacion".

BANCO_FIXED = [
    {
        "tema": "1.1.1 Integrales Directas",
        "pregunta": r"Dada la integral $\int (3x^2 - 2x + 5) dx$, seleccione la primitiva correcta:",
        "opciones": [
            r"A) $x^3 - x^2 + 5x + C$",
            r"B) $3x^3 - 2x^2 + 5x + C$",
            r"C) $x^3 - x^2 + 5 + C$",
            r"D) $6x - 2 + C$"
        ],
        "respuesta_correcta": r"A) $x^3 - x^2 + 5x + C$",
        "explicacion": "Aplicando la regla de la potencia: $\\int 3x^2 dx = x^3$, $\\int -2x dx = -x^2$ y $\\int 5 dx = 5x$."
    },
    {
        "tema": "2.1.1 ED 1er Orden: Separación de Variables",
        "pregunta": r"¿Cuál es la solución general de la ecuación diferencial $y' = 2x$?",
        "opciones": [
            r"A) $y = x^2 + C$",
            r"B) $y = 2x + C$",
            r"C) $y = x^2$",
            r"D) $y = \frac{x^2}{2} + C$"
        ],
        "respuesta_correcta": r"A) $y = x^2 + C$",
        "explicacion": "Separando variables $dy = 2x dx$, integrando ambos lados obtenemos $y = x^2 + C$."
    },
    # --- AQUÍ PUEDES PEGAR MÁS EJERCICIOS DE TU BANCO ---
]

def obtener_preguntas_fijas(temas_solicitados, cantidad):
    """
    Filtra preguntas del banco fijo que coincidan con los temas seleccionados.
    Si no hay suficientes, devuelve todas las que encuentre.
    """
    # 1. Filtrar por temas seleccionados
    candidatas = [p for p in BANCO_FIXED if any(t in p["tema"] for t in temas_solicitados)]
    
    # 2. Si no hay preguntas de esos temas, devolvemos una lista vacía
    if not candidatas:
        return []
        
    # 3. Seleccionar al azar la cantidad solicitada (o todas si hay menos)
    num_a_seleccionar = min(len(candidatas), cantidad)
    return random.sample(candidatas, num_a_seleccionar)