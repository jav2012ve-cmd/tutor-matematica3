LISTA_TEMAS = [
    "1.1.1 Integrales Directas", 
    "1.1.2 Cambios de variables (Sustitución)",
    "1.1.3 División de Polinomios",
    "2.3 Aplicaciones de Ecuaciones Diferenciales en Economía"
]

# ... (Mantén la LISTA_TEMAS igual) ...

CONTENIDO_TEORICO = {
    "1.1.1 Integrales Directas": {
        # ... (Mantén lo que ya tienes aquí) ...
        "definicion": r"f(x) = \int g(x) dx \iff \frac{d}{dx}[f(x)] = g(x)",
        "propiedades": [
            r"\int [f(x) \pm g(x)] dx = \int f(x) dx \pm \int g(x) dx",
            r"\int C \cdot f(x) dx = C \int f(x) dx"
        ],
        "tabla_col1": [
            r"\int x^n dx = \frac{x^{n+1}}{n+1}, \quad n \neq -1",
            r"\int \frac{1}{x} dx = \ln|x|",
            r"\int e^{ax+b} dx = \frac{1}{a}e^{ax+b}",
            r"\int \ln x dx = x\ln x - x"
        ],
        "tabla_col2": [
            r"\int a^x dx = \frac{1}{\ln a}a^x",
            r"\int \frac{dx}{x^2 + a^2} = \frac{1}{a}\arctan\left(\frac{x}{a}\right)",
            r"\int \frac{dx}{\sqrt{a^2-x^2}} = \arcsin\left(\frac{x}{a}\right)",
            r"\int \frac{dx}{\sqrt{x^2 \pm a^2}} = \ln|x + \sqrt{x^2 \pm a^2}|"
        ]
    }, # <--- ¡NO OLVIDES ESTA COMA!

    "1.1.2 Cambios de variables (Sustitución)": {
        "definicion": r"\int f(g(x)) \cdot g'(x) \, dx = \int f(u) \, du",
        "propiedades": [
            r"\text{Paso 1: Elegir } u = g(x)",
            r"\text{Paso 2: Calcular } du = g'(x) dx"
        ],
        # Reutilizamos las claves de tabla para mostrar pasos o ejemplos clave
        "tabla_col1": [
            r"\text{Si } \int e^{3x} dx, \quad u=3x, \, du=3dx",
            r"\Rightarrow \frac{1}{3} \int e^u du"
        ],
        "tabla_col2": [
            r"\text{Si } \int 2x(x^2+1)^5 dx, \quad u=x^2+1",
            r"\Rightarrow \int u^5 du = \frac{u^6}{6} + C"
        ]
    }
}
PROMPT_QUIZ = """
INSTRUCCIONES PARA EL QUIZ:
1. Genera un examen corto de 4 preguntas de selección simple (A, B, C).
2. DISTRIBUCIÓN DE TEMAS:
   - 1 Pregunta de Integrales Indefinidas (Cálculo).
   - 1 Pregunta de Aplicación Económica de Integrales (Excedentes o Áreas).
   - 1 Pregunta teórica de Ecuaciones Diferenciales.
   - 1 Pregunta de resolución de Ecuaciones Diferenciales.
3. FORMATO:
   - Enuncia la pregunta claramente.
   - Da las 3 opciones.
   - NO indiques la respuesta correcta todavía.
   - Al final, escribe: "Responde con las letras (ej: 1A, 2B...)"
4. EVALUACIÓN:
   - Cuando el usuario responda, corrige una por una y explica brevemente los errores si los hay.
"""



# ... (Mantén el CONTEXTO_BASE igual) ...
CONTEXTO_BASE = """
Actúa como un profesor titular de la cátedra de Matemáticas III de la carrera de Economía 
en la Universidad Católica Andrés Bello (UCAB). 
TU ENFOQUE:
1. Tus dos pilares fundamentales son: CÁLCULO INTEGRAL y ECUACIONES DIFERENCIALES.
2. Cuando expliques, trata de buscar aplicaciones económicas.
3. Sé riguroso pero cercano. Usa LaTeX.
"""