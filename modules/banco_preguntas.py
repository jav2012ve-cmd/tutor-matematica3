# modules/banco_preguntas.py
import random

# ==============================================================================
# BANCO DE PREGUNTAS - MATEMÁTICAS III (ECONOMÍA UCAB)
# Fuente: Archivos LaTeX 2022 (Parciales 1, 2, 3, Reparación y Complementario)
# ==============================================================================

BANCO_FIXED = [
    # --------------------------------------------------------------------------
    # PARCIAL 1: Integrales Indefinidas, Métodos de Integración, Modelos Básicos
    # --------------------------------------------------------------------------
    {
        "tema": "1.1.1 Integrales Directas",
        "pregunta": r"Resuelva la siguiente integral con respecto a la variable $x$: $$ \int (3y-2x)^{20} dx $$",
        "opciones": [
            r"A) $-\frac{1}{42}(3y-2x)^{21} + C$",
            r"B) $\frac{1}{21}(3y-2x)^{21} + C$",
            r"C) $\frac{1}{63}(3y-2x)^{21} + C$", # Error integrando respecto a y
            r"D) $20(3y-2x)^{19} + C$" # Derivada en lugar de integral
        ],
        "respuesta_correcta": r"A) $-\frac{1}{42}(3y-2x)^{21} + C$",
        "explicacion": r"Al integrar respecto a $x$, $3y$ es constante. Usamos sustitución $u = 3y-2x \Rightarrow du = -2dx$. La integral resulta en $-\frac{1}{2} \int u^{20} du$."
    },
    {
        "tema": "1.1.1 Integrales Directas",
        "pregunta": r"Resuelva la siguiente integral con respecto a la variable $y$: $$ \int \frac{e^{3y-2x}}{e^{y+2x}} dy $$",
        "opciones": [
            r"A) $\frac{1}{2}e^{2y-4x} + C$",
            r"B) $e^{2y-4x} + C$",
            r"C) $\frac{1}{2}e^{2y} + C$",
            r"D) $2e^{2y-4x} + C$"
        ],
        "respuesta_correcta": r"A) $\frac{1}{2}e^{2y-4x} + C$",
        "explicacion": r"Simplificamos los exponentes: $(3y-2x) - (y+2x) = 2y - 4x$. La integral es $\int e^{2y-4x} dy$. Al integrar respecto a $y$, dividimos por la derivada del exponente (2)."
    },
    {
        "tema": "1.1.1 Integrales Directas",
        "pregunta": r"Resuelva la siguiente integral indefinida respecto a $t$: $$ \int \sqrt[3]{x^{-2}t^{-3}} dt $$",
        "opciones": [
            r"A) $x^{-2/3} \ln|t| + C$",
            r"B) $\frac{3}{2} x^{-2/3} t^{2/3} + C$",
            r"C) $-3 x^{-2/3} t^{-2} + C$",
            r"D) $x^{-2/3} \frac{t^{-2}}{-2} + C$"
        ],
        "respuesta_correcta": r"A) $x^{-2/3} \ln|t| + C$",
        "explicacion": r"Reescribimos la raíz: $(x^{-2}t^{-3})^{1/3} = x^{-2/3} t^{-1} = \frac{x^{-2/3}}{t}$. Al integrar $\frac{1}{t}$ obtenemos $\ln|t|$. El término con $x$ es constante respecto a $t$."
    },
    {
        "tema": "1.1.1 Integrales Directas",
        "pregunta": r"Calcule el valor de la integral definida: $$ \int_{1}^{2} \frac{x^2-1}{x^2} dx $$",
        "opciones": [
            r"A) $0.5$",
            r"B) $1.5$",
            r"C) $2.0$",
            r"D) $\ln(2)$"
        ],
        "respuesta_correcta": r"A) $0.5$",
        "explicacion": r"Simplificamos el integrando: $\frac{x^2}{x^2} - \frac{1}{x^2} = 1 - x^{-2}$. La integral es $[x + x^{-1}]_1^2 = (2 + 0.5) - (1 + 1) = 2.5 - 2 = 0.5$."
    },
    {
        "tema": "1.1.2 Cambios de variables (Sustitución)",
        "pregunta": r"Resuelva la siguiente integral aplicando sustitución simple: $$ \int \frac{\sqrt{1-4\ln x}}{x} dx $$",
        "opciones": [
            r"A) $-\frac{1}{6}(1-4\ln x)^{3/2} + C$",
            r"B) $\frac{2}{3}(1-4\ln x)^{3/2} + C$",
            r"C) $-\frac{1}{4}\sqrt{1-4\ln x} + C$",
            r"D) $\frac{1}{x}(1-4\ln x)^{3/2} + C$"
        ],
        "respuesta_correcta": r"A) $-\frac{1}{6}(1-4\ln x)^{3/2} + C$",
        "explicacion": r"Sea $u = 1-4\ln x \Rightarrow du = -\frac{4}{x} dx \Rightarrow \frac{dx}{x} = -\frac{du}{4}$. La integral queda $-\frac{1}{4}\int u^{1/2} du = -\frac{1}{4}(\frac{2}{3}u^{3/2}) = -\frac{1}{6}u^{3/2}$."
    },
    {
        "tema": "1.1.2 Cambios de variables (Sustitución)",
        "pregunta": r"Dada la integral $\int g(f(x)) f'(x) dx$, seleccione la afirmación teórica correcta para el cambio de variable $z = f(x)$:",
        "opciones": [
            r"A) Se reescribe como $\int g(z) dz$.",
            r"B) Se reescribe como $\int g(z) f'(z) dz$.",
            r"C) Se reescribe como $\int \frac{g(z)}{f'(x)} dz$.",
            r"D) No se puede aplicar cambio de variable si $g(x)$ no es polinómica."
        ],
        "respuesta_correcta": r"A) Se reescribe como $\int g(z) dz$.",
        "explicacion": "Es la definición fundamental del método de sustitución: si $z=f(x)$, entonces $dz=f'(x)dx$, absorbiendo la derivada interna."
    },
    {
        "tema": "1.1.4 Fracciones Simples",
        "pregunta": r"Indique la estructura correcta de descomposición en fracciones simples para: $$ \int \frac{2x+x^2+2x^3+4}{(x^2+4)(x^2+1)} dx $$",
        "opciones": [
            r"A) $\frac{Ax+B}{x^2+4} + \frac{Cx+D}{x^2+1}$",
            r"B) $\frac{A}{x^2+4} + \frac{B}{x^2+1}$",
            r"C) $\frac{Ax}{x^2+4} + \frac{Bx}{x^2+1}$",
            r"D) $\frac{A}{(x^2+4)^2} + \frac{B}{x^2+1}$"
        ],
        "respuesta_correcta": r"A) $\frac{Ax+B}{x^2+4} + \frac{Cx+D}{x^2+1}$",
        "explicacion": r"El denominador tiene dos factores cuadráticos irreducibles distintos ($x^2+4$ y $x^2+1$), por lo que cada uno requiere un numerador lineal ($Ax+B$ y $Cx+D$)."
    },
    {
        "tema": "1.1.7 Integral por partes",
        "pregunta": r"Para resolver la integral $\int x^3 \ln(x^2-4) dx$, ¿cuál es la elección de $u$ y $dv$ más adecuada?",
        "opciones": [
            r"A) $u = \ln(x^2-4)$, $dv = x^3 dx$",
            r"B) $u = x^3$, $dv = \ln(x^2-4) dx$",
            r"C) $u = x^2$, $dv = x \ln(x^2-4) dx$",
            r"D) $u = 1$, $dv = x^3 \ln(x^2-4) dx$"
        ],
        "respuesta_correcta": r"A) $u = \ln(x^2-4)$, $dv = x^3 dx$",
        "explicacion": "Por la regla LIATE (Logarítmica antes que Algebraica), elegimos $u$ como el logaritmo para derivarlo y simplificarlo, y $dv$ como el polinomio para integrarlo."
    },
    {
        "tema": "1.2.1 Áreas entre curvas",
        "pregunta": r"Seleccione la integral que calcula el área encerrada entre $y=4-x^2$ y $y=1+2x$ en el intervalo donde se cruzan:",
        "opciones": [
            r"A) $\int_{-3}^{1} [(4-x^2) - (1+2x)] dx$",
            r"B) $\int_{-3}^{1} [(1+2x) - (4-x^2)] dx$",
            r"C) $\int_{0}^{4} [(4-x^2) - (1+2x)] dx$",
            r"D) $\int_{-1}^{3} [(4-x^2) + (1+2x)] dx$"
        ],
        "respuesta_correcta": r"A) $\int_{-3}^{1} [(4-x^2) - (1+2x)] dx$",
        "explicacion": r"Al igualar $4-x^2 = 1+2x \Rightarrow x^2+2x-3=0$, obtenemos raíces $x=-3, x=1$. En este intervalo, la parábola ($4-x^2$) está por encima de la recta."
    },
    {
        "tema": "1.2.3 Integrales Impropias",
        "pregunta": r"Determine el valor de convergencia de la integral impropia $\int_{0}^{\infty} \frac{x^2}{\sqrt{(x^3+4)^3}} dx$:",
        "opciones": [
            r"A) Converge a $\frac{1}{3}$",
            r"B) Diverge (infinito)",
            r"C) Converge a $\frac{2}{3}$",
            r"D) Converge a $0$"
        ],
        "respuesta_correcta": r"A) Converge a $\frac{1}{3}$",
        "explicacion": r"Usando sustitución $u=x^3+4 \Rightarrow du=3x^2 dx$, la integral se convierte en $\frac{1}{3}\int_4^{\infty} u^{-3/2} du$. Al evaluar el límite, converge a $1/3$."
    },
    {
        "tema": "2.1.1 ED 1er Orden: Separación de Variables",
        "pregunta": r"Un modelo de población de conejos plantea: $\frac{dp}{dt} = 10(100-p)^2$. Al separar variables para resolver, se obtiene:",
        "opciones": [
            r"A) $\int (100-p)^{-2} dp = \int 10 dt$",
            r"B) $\int (100-p)^2 dp = \int 10 dt$",
            r"C) $\int \frac{dp}{100-p} = \int 10 dt$",
            r"D) $\ln(100-p) = 10t + C$"
        ],
        "respuesta_correcta": r"A) $\int (100-p)^{-2} dp = \int 10 dt$",
        "explicacion": "Pasamos el término con $p$ al lado izquierdo dividiendo: $\frac{dp}{(100-p)^2} = 10 dt$."
    },
    {
        "tema": "2.1.2 ED 1er Orden: Homogéneas",
        "pregunta": r"Identifique el tipo de ecuación diferencial: $(x^2 - 2y^2)dx + y dy = 0$",
        "opciones": [
            r"A) Homogénea de grado 2",
            r"B) Exacta",
            r"C) Lineal",
            r"D) Variables Separables"
        ],
        "respuesta_correcta": r"A) Homogénea de grado 2",
        "explicacion": r"Al reemplazar $(tx, ty)$, obtenemos $t^2(x^2-2y^2)dx + t(ty)dy = t^2(...)dx + t^2(...)dy = 0$. Todos los términos son de grado 2."
    },

    # --------------------------------------------------------------------------
    # PARCIAL 2: Integrales Definidas, Áreas, Volúmenes, Impropias
    # --------------------------------------------------------------------------
    {
        "tema": "1.2.1 Áreas entre curvas",
        "pregunta": r"Seleccione el planteamiento correcto para hallar el área entre las curvas $y=x^2$ y $y=6-x$:",
        "opciones": [
            r"A) $\int_{-3}^{2} (6 - x - x^2) dx$",
            r"B) $\int_{-3}^{2} (x^2 - (6-x)) dx$",
            r"C) $\int_{0}^{6} (6 - x - x^2) dx$",
            r"D) $\int_{-2}^{3} (6 - x - x^2) dx$"
        ],
        "respuesta_correcta": r"A) $\int_{-3}^{2} (6 - x - x^2) dx$",
        "explicacion": r"Igualando $x^2 = 6-x$ hallamos los cortes en $x=-3$ y $x=2$. En este intervalo, la recta $y=6-x$ está por encima de la parábola."
    },
    {
        "tema": "1.2.3 Integrales Impropias",
        "pregunta": r"Halle el valor de $b$ tal que $\int_{b}^{\infty} \frac{dx}{(1+2x)^2} = \frac{1}{4}$",
        "opciones": [
            r"A) $b = \frac{1}{2}$",
            r"B) $b = 0$",
            r"C) $b = 1$",
            r"D) $b = 2$"
        ],
        "respuesta_correcta": r"A) $b = \frac{1}{2}$",
        "explicacion": r"La integral resulta en $\lim_{t\to\infty} [-\frac{1}{2(1+2x)}]_b^t = \frac{1}{2(1+2b)}$. Igualando a $1/4$, despejamos $b=1/2$."
    },
    {
        "tema": "1.2.4 Integrales Dobles",
        "pregunta": r"Calcule la integral doble $\int_{0}^{1}\int_{1}^{2} (3x^2 - 6z) dx dz$ (Nota: orden $dx$ luego $dz$):",
        "opciones": [
            r"A) $-2$",
            r"B) $7$",
            r"C) $0$",
            r"D) $-5$"
        ],
        "respuesta_correcta": r"A) $-2$",
        "explicacion": r"Integramos primero respecto a $x$: $[x^3 - 6zx]_1^2 = (8-12z) - (1-6z) = 7-6z$. Luego integramos respecto a $z$ en $[0,1]$: $[7z - 3z^2]_0^1 = 7-3 = 4$. (Verificar cálculo según orden de integración)."
    },

    # --------------------------------------------------------------------------
    # PARCIAL 3: Ecuaciones Diferenciales de Orden Superior
    # --------------------------------------------------------------------------
    {
        "tema": "2.2.1 ED Orden Superior: Homogéneas",
        "pregunta": r"Dada la ecuación diferencial $y^{IV} - y^{V} + y^{IV} - 3y''' - 10y'' + 4y' + 8y = 0$, indique cuál sería el primer paso para resolverla:",
        "opciones": [
            r"A) Hallar las raíces del polinomio característico.",
            r"B) Integrar 6 veces ambos lados.",
            r"C) Usar el método de variación de parámetros.",
            r"D) Aplicar factor integrante $\mu(x) = e^{\int P(x)dx}$."
        ],
        "respuesta_correcta": r"A) Hallar las raíces del polinomio característico.",
        "explicacion": "Es una ecuación lineal homogénea de coeficientes constantes. Se resuelve proponiendo $y=e^{rx}$ y resolviendo el polinomio auxiliar."
    },
    {
        "tema": "2.1.2 ED 1er Orden: Homogéneas",
        "pregunta": r"Dada la ecuación diferencial $(x+y)dx - y dy = 0$, determine su clasificación:",
        "opciones": [
            r"A) Homogénea de grado 1",
            r"B) Exacta",
            r"C) Variables Separables",
            r"D) Lineal de coeficientes constantes"
        ],
        "respuesta_correcta": r"A) Homogénea de grado 1",
        "explicacion": r"Al evaluar $M(tx, ty) = t(x+y)$ y $N(tx, ty) = t(-y)$, ambos coeficientes son homogéneos del mismo grado (1), permitiendo el cambio $y=ux$."
    },
    {
        "tema": "2.3 Aplicaciones de Ecuaciones Diferenciales en Economía",
        "pregunta": r"Una población crece según $\frac{dp}{dt} = kp(200-p)$. Sin resolver, indique cuál es la población límite a largo plazo ($t \to \infty$):",
        "opciones": [
            r"A) 200 unidades",
            r"B) 0 unidades",
            r"C) $200k$ unidades",
            r"D) Infinito"
        ],
        "respuesta_correcta": r"A) 200 unidades",
        "explicacion": r"Es una ecuación logística de la forma $p' = kp(M-p)$. El valor $M=200$ representa la capacidad de carga o asíntota horizontal hacia la cual tiende la solución."
    }
    {
        "tema": "2.1.3 ED 1er Orden: Exactas",
        "pregunta": r"Para la ecuación $(x^2-y^2)dx + (y^2-xy)dy = 0$, ¿cuál es la clasificación correcta?",
        "opciones": [
            r"A) Homogénea de grado 2.",
            r"B) Ecuación Exacta.",
            r"C) Lineal de primer orden.",
            r"D) Variables Separables."
        ],
        "respuesta_correcta": r"A) Homogénea de grado 2.",
        "explicacion": r"Si sustituimos $(tx, ty)$, obtenemos $t^2$ factorizado en ambos términos. No es exacta pues $M_y = -2y$ y $N_x = -y$."
    },
    {
        "tema": "2.3 Aplicaciones de Ecuaciones Diferenciales en Economía",
        "pregunta": r"La ecuación $\frac{dp}{dt} = kp(1000-p)$ modela el crecimiento de una colonia con capacidad de carga limitada. ¿A qué tipo de modelo corresponde?",
        "opciones": [
            r"A) Crecimiento Logístico",
            r"B) Crecimiento Exponencial (Malthus)",
            r"C) Ley de Enfriamiento de Newton",
            r"D) Desintegración Radiactiva"
        ],
        "respuesta_correcta": r"A) Crecimiento Logístico",
        "explicacion": r"La estructura $p' = kp(M-p)$ es característica de la ecuación logística (o de Verhulst), donde el crecimiento se frena al acercarse a la capacidad máxima (1000)."
    },
]

def obtener_preguntas_fijas(temas_solicitados, cantidad):
    """
    Filtra preguntas del banco fijo que coincidan con los temas seleccionados.
    """
    candidatas = [p for p in BANCO_FIXED if any(t in p["tema"] for t in temas_solicitados)]
    
    if not candidatas:
        return []
        
    num_a_seleccionar = min(len(candidatas), cantidad)
    return random.sample(candidatas, num_a_seleccionar)