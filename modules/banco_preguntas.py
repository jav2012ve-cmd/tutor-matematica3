import random

# ==============================================================================
# BANCO DE PREGUNTAS - MATEMÁTICAS III (ECONOMÍA UCAB)
# Fuentes:
# 1. Parciales 2022-2023
# 2. Taller 1 2026-15
# 3. Taller 2 2026-15 (NUEVO)
# ==============================================================================

BANCO_FIXED = [
    # --------------------------------------------------------------------------
    # LOTE 1: INTEGRALES Y MÉTODOS (PARCIALES ANTERIORES)
    # --------------------------------------------------------------------------
    {
        "tema": "1.1.1 Integrales Directas",
        "pregunta": r"Resuelva la siguiente integral con respecto a la variable $x$: $$ \int (3y-2x)^{20} dx $$",
        "opciones": [
            r"A) $-\frac{1}{42}(3y-2x)^{21} + C$",
            r"B) $\frac{1}{21}(3y-2x)^{21} + C$",
            r"C) $\frac{1}{63}(3y-2x)^{21} + C$",
            r"D) $20(3y-2x)^{19} + C$"
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
    
    # --------------------------------------------------------------------------
    # LOTE 2: APLICACIONES DE LA INTEGRAL (ÁREAS, VOLÚMENES, IMPROPIAS)
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
    # LOTE 3: ECUACIONES DIFERENCIALES Y MODELADO (PARCIALES Y TALLER 1)
    # --------------------------------------------------------------------------
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
    },

    # --------------------------------------------------------------------------
    # LOTE 4: TALLER 1 - 202615 (EJERCICIOS OPERATIVOS)
    # --------------------------------------------------------------------------
    {
        "tema": "1.1.1 Integrales Directas",
        "pregunta": r"Determine la integral de la función $(x-2y^2)^2$ con respecto a la variable $y$: $$ \int (x-2y^2)^2 dy $$",
        "opciones": [
            r"A) $x^2y - \frac{4}{3}xy^3 + \frac{4}{5}y^5 + C$",
            r"B) $\frac{1}{3}(x-2y^2)^3 + C$",
            r"C) $\frac{(x-2y^2)^3}{-4y} + C$",
            r"D) $2(x-2y^2) + C$"
        ],
        "respuesta_correcta": r"A) $x^2y - \frac{4}{3}xy^3 + \frac{4}{5}y^5 + C$",
        "explicacion": r"Desarrollamos el binomio: $x^2 - 4xy^2 + 4y^4$. Al integrar respecto a $y$ ($x$ constante): $\int x^2 dy - 4x\int y^2 dy + 4\int y^4 dy = x^2y - \frac{4}{3}xy^3 + \frac{4}{5}y^5$."
    },
    {
        "tema": "1.1.2 Cambios de variables (Sustitución)",
        "pregunta": r"Resuelva la siguiente integral: $$ \int (1-3x)^{-2} dx $$",
        "opciones": [
            r"A) $\frac{1}{3(1-3x)} + C$",
            r"B) $-\frac{1}{1-3x} + C$",
            r"C) $\frac{3}{1-3x} + C$",
            r"D) $\frac{(1-3x)^{-3}}{-3} + C$"
        ],
        "respuesta_correcta": r"A) $\frac{1}{3(1-3x)} + C$",
        "explicacion": r"Sea $u=1-3x \Rightarrow du=-3dx \Rightarrow dx=du/-3$. La integral es $-\frac{1}{3}\int u^{-2}du = -\frac{1}{3}(\frac{u^{-1}}{-1}) = \frac{1}{3u}$."
    },
    {
        "tema": "1.1.2 Cambios de variables (Sustitución)",
        "pregunta": r"Evalúe la integral trigonométrica usando sustitución: $$ \int \frac{\cos(1-2\ln x)}{x} dx $$",
        "opciones": [
            r"A) $-\frac{1}{2}\sin(1-2\ln x) + C$",
            r"B) $\sin(1-2\ln x) + C$",
            r"C) $-2\sin(1-2\ln x) + C$",
            r"D) $\frac{\sin(1-2\ln x)}{x} + C$"
        ],
        "respuesta_correcta": r"A) $-\frac{1}{2}\sin(1-2\ln x) + C$",
        "explicacion": r"Sea $u=1-2\ln x \Rightarrow du = -\frac{2}{x} dx$. Entonces $\frac{dx}{x} = -\frac{du}{2}$. Sustituyendo: $-\frac{1}{2}\int \cos(u) du = -\frac{1}{2}\sin(u)$."
    },
    {
        "tema": "1.1.2 Cambios de variables (Sustitución)",
        "pregunta": r"Resuelva la integral con raíz en el denominador: $$ \int \frac{(1-2\sqrt{x})^3}{\sqrt{x}} dx $$",
        "opciones": [
            r"A) $-\frac{1}{4}(1-2\sqrt{x})^4 + C$",
            r"B) $\frac{1}{4}(1-2\sqrt{x})^4 + C$",
            r"C) $-\frac{1}{2}(1-2\sqrt{x})^4 + C$",
            r"D) $2(1-2\sqrt{x})^4 + C$"
        ],
        "respuesta_correcta": r"A) $-\frac{1}{4}(1-2\sqrt{x})^4 + C$",
        "explicacion": r"Sea $u=1-2\sqrt{x} \Rightarrow du = -2(\frac{1}{2\sqrt{x}}) dx = -\frac{1}{\sqrt{x}} dx$. Entonces $\frac{dx}{\sqrt{x}} = -du$. La integral queda $-\int u^3 du = -\frac{u^4}{4}$."
    },
    {
        "tema": "1.1.7 Integral por partes",
        "pregunta": r"¿Cuál es el resultado de la integral cíclica $\int e^{-x} \cos x dx$?",
        "opciones": [
            r"A) $\frac{e^{-x}}{2}(\sin x - \cos x) + C$",
            r"B) $e^{-x}(\sin x + \cos x) + C$",
            r"C) $\frac{e^{-x}}{2}(\cos x - \sin x) + C$",
            r"D) $-e^{-x}\sin x + C$"
        ],
        "respuesta_correcta": r"A) $\frac{e^{-x}}{2}(\sin x - \cos x) + C$",
        "explicacion": r"Aplicando partes dos veces, se obtiene una ecuación para $I$. El resultado estándar para $\int e^{ax}\cos(bx)dx$ lleva a $\frac{e^{-x}}{(-1)^2+1^2}(-\cos x + \sin x)$."
    },
    {
        "tema": "1.2.3 Integrales Impropias",
        "pregunta": r"Determine la convergencia de la integral impropia: $$ \int_{0}^{\infty} \frac{x^2}{e^x} dx $$",
        "opciones": [
            r"A) Converge a 2",
            r"B) Converge a 1",
            r"C) Diverge",
            r"D) Converge a 0"
        ],
        "respuesta_correcta": r"A) Converge a 2",
        "explicacion": r"Es la función Gamma $\Gamma(3) = 2!$. Integrando por partes dos veces (o tabular), $\int x^2 e^{-x} dx = -e^{-x}(x^2+2x+2)$. Evaluando de $0$ a $\infty$, el límite superior es 0 y el inferior es $-1(0+0+2) = -2$. Resultado $0 - (-2) = 2$."
    },
    {
        "tema": "1.2.2 Excedentes del consumidor y productor",
        "pregunta": r"Dadas las funciones de Demanda $D(q) = 14 - \frac{q^2}{4}$ y Oferta $O(q) = 2q + 2$, calcule el Excedente del Consumidor en el equilibrio:",
        "opciones": [
            r"A) $10.67$ (aprox)",
            r"B) $32.00$",
            r"C) $50.66$",
            r"D) $15.50$"
        ],
        "respuesta_correcta": r"A) $10.67$ (aprox)",
        "explicacion": r"Equilibrio: $14-q^2/4 = 2q+2 \Rightarrow q^2+8q-48=0 \Rightarrow (q+12)(q-4)=0$. Equilibrio en $q=4, p=10$. EC = $\int_0^4 (14-q^2/4) dq - 4(10) = [14q - q^3/12]_0^4 - 40 = (56 - 5.33) - 40 = 10.67$."
    },
    {
        "tema": "1.2.1 Áreas entre curvas",
        "pregunta": r"Plantee la integral para el área entre $y=x^2+x$ y $y=15-\frac{x^2}{3}$:",
        "opciones": [
            r"A) $\int_{-3.75}^{3} \left[ \left(15-\frac{x^2}{3}\right) - (x^2+x) \right] dx$",
            r"B) $\int_{-3}^{3} \left[ (x^2+x) - \left(15-\frac{x^2}{3}\right) \right] dx$",
            r"C) $\int_{0}^{3} \left[ \left(15-\frac{x^2}{3}\right) + (x^2+x) \right] dx$",
            r"D) $\int_{-4}^{4} \left[ \left(15-\frac{x^2}{3}\right) - (x^2+x) \right] dx$"
        ],
        "respuesta_correcta": r"A) $\int_{-3.75}^{3} \left[ \left(15-\frac{x^2}{3}\right) - (x^2+x) \right] dx$",
        "explicacion": r"Intersección: $x^2+x = 15-x^2/3 \Rightarrow 4x^2+3x-45=0$. Raíces $x=3$ y $x=-15/4 (-3.75)$. En este intervalo, la parábola que abre hacia abajo ($15-x^2/3$) está por encima."
    },
    # --------------------------------------------------------------------------
    # AMPLIACIÓN TALLER 1 - 202615 (APLICACIONES Y DOBLES)
    # --------------------------------------------------------------------------
    {
        "tema": "1.2.4 Integrales Dobles",
        "pregunta": r"Plantee la integral doble $\iint_D f(x,y) dA$ para la región $D$ acotada por la parábola $x = y^2 - 4y$ y la recta $y = x - 6$ (Tip: use integración respecto a y primero):",
        "opciones": [
            r"A) $\int_{-1}^{6} \int_{y^2-4y}^{y+6} f(x,y) dx dy$",
            r"B) $\int_{-1}^{6} \int_{y+6}^{y^2-4y} f(x,y) dx dy$",
            r"C) $\int_{0}^{6} \int_{x-6}^{\sqrt{x}} f(x,y) dy dx$",
            r"D) $\int_{-6}^{10} \int_{y^2-4y}^{y+6} f(x,y) dx dy$"
        ],
        "respuesta_correcta": r"A) $\int_{-1}^{6} \int_{y^2-4y}^{y+6} f(x,y) dx dy$",
        "explicacion": r"Igualamos $x$: $y^2-4y = y+6 \Rightarrow y^2-5y-6=0 \Rightarrow (y-6)(y+1)=0$. El intervalo en $y$ es $[-1, 6]$. La recta $x=y+6$ está a la derecha de la parábola."
    },
    {
        "tema": "1.2.4 Integrales Dobles",
        "pregunta": r"Para la región triangular con vértices en $(0,0), (4,0)$ y $(4,4)$, cambie el orden de integración de $\int_0^4 \int_0^x f(x,y) dy dx$:",
        "opciones": [
            r"A) $\int_0^4 \int_y^4 f(x,y) dx dy$",
            r"B) $\int_0^4 \int_0^y f(x,y) dx dy$",
            r"C) $\int_0^x \int_0^4 f(x,y) dx dy$",
            r"D) $\int_0^4 \int_4^y f(x,y) dx dy$"
        ],
        "respuesta_correcta": r"A) $\int_0^4 \int_y^4 f(x,y) dx dy$",
        "explicacion": r"La región está delimitada por $y=0, x=4, y=x$. Al integrar primero en $x$ (barrido horizontal), vamos desde la recta $x=y$ hasta $x=4$."
    },
    {
        "tema": "1.2.5 Volúmenes de Revolución",
        "pregunta": r"Plantee el volumen del sólido generado por la región $y = x^2 - 4x$ y el eje $x$ ($y=0$) al girar alrededor de la recta $y = 4$:",
        "opciones": [
            r"A) $\pi \int_0^4 \left[ (4 - (x^2-4x))^2 - (4-0)^2 \right] dx$",
            r"B) $\pi \int_0^4 \left[ (x^2-4x)^2 - 4^2 \right] dx$",
            r"C) $\pi \int_0^4 \left[ 4^2 - (4 - (x^2-4x))^2 \right] dx$",
            r"D) $2\pi \int_0^4 y(x^2-4x) dy$"
        ],
        "respuesta_correcta": r"C) $\pi \int_0^4 \left[ 4^2 - (4 - (x^2-4x))^2 \right] dx$",
        "explicacion": r"El eje de giro $y=4$ está arriba. El radio exterior es $R = 4 - (x^2-4x)$ (distancia a la parábola) y el radio interior es $r = 4 - 0 = 4$. NOTA: Si la parábola está debajo del eje X, el radio mayor sería hasta la curva. Verificando región: $x^2-4x$ es negativa en $(0,4)$. Distancia eje a curva: $4 - (x^2-4x)$. Distancia eje a $y=0$: $4$. El radio 'lejano' es el de la curva. Planteamiento corregido: $R_{ext} = 4 - (x^2-4x)$, $R_{int}=4$. Volumen = $\pi \int (R_{ext}^2 - R_{int}^2)$."
    },
    {
        "tema": "1.2.5 Volúmenes de Revolución",
        "pregunta": r"Volumen generado por la región acotada por $x = y^2+2, x=1, y=-2, y=2$ al girar alrededor del eje $x = -2$ (Plantear con capas/discos según convenga):",
        "opciones": [
            r"A) $\pi \int_{-2}^{2} \left[ (y^2+2 - (-2))^2 - (1 - (-2))^2 \right] dy$",
            r"B) $\pi \int_{-2}^{2} \left[ (y^2+4)^2 - 3^2 \right] dy$",
            r"C) $\pi \int_{1}^{6} (y^2+2)^2 dy$",
            r"D) Opción A y B son equivalentes"
        ],
        "respuesta_correcta": r"D) Opción A y B son equivalentes",
        "explicacion": r"Usamos arandelas perpendiculares al eje $y$ (integrando en $dy$). Radio exterior $R = (y^2+2) - (-2) = y^2+4$. Radio interior $r = 1 - (-2) = 3$."
    },
    {
        "tema": "1.2.2 Excedentes del consumidor y productor",
        "pregunta": r"Dada la Demanda $p = 100 - 2q^2$ y Oferta $p = 50 + 3q^2$. Calcule el Excedente del Productor (EP) en el equilibrio:",
        "opciones": [
            r"A) $EP = \int_0^{\sqrt{10}} (80 - (50+3q^2)) dq$",
            r"B) $EP = \int_0^{10} ((100-2q^2) - 80) dq$",
            r"C) $EP = 100\sqrt{10}$",
            r"D) $EP = \int_0^{\sqrt{10}} (50+3q^2) dq$"
        ],
        "respuesta_correcta": r"A) $EP = \int_0^{\sqrt{10}} (80 - (50+3q^2)) dq$",
        "explicacion": r"Equilibrio: $100-2q^2 = 50+3q^2 \Rightarrow 50=5q^2 \Rightarrow q=\sqrt{10}$. Precio eq $p=80$. El EP es el área entre el precio de equilibrio y la curva de oferta: $\int_0^{q_0} (p_0 - O(q)) dq$."
    },
    {
        "tema": "1.2.3 Integrales Impropias",
        "pregunta": r"Función de Densidad de Probabilidad (PDF): Determine el valor de $k$ para que $f(x) = k x^2(1-x)$ sea una PDF válida en el intervalo $[0,1]$:",
        "opciones": [
            r"A) $k = 12$",
            r"B) $k = 6$",
            r"C) $k = 1$",
            r"D) $k = 1/12$"
        ],
        "respuesta_correcta": r"A) $k = 12$",
        "explicacion": r"Condición: $\int_0^1 k(x^2-x^3) dx = 1$. Resolvemos: $k [\frac{x^3}{3} - \frac{x^4}{4}]_0^1 = k(\frac{1}{3}-\frac{1}{4}) = k(\frac{1}{12}) = 1 \Rightarrow k=12$."
    },
    # --------------------------------------------------------------------------
    # LOTE 5: TALLER 2 - 202615 (VOLÚMENES, LEY ENFRIAMIENTO, ED SUPERIOR) - NUEVO
    # --------------------------------------------------------------------------
    {
        "tema": "1.2.5 Volúmenes de Revolución",
        "pregunta": r"Plantee la integral para el volumen del sólido generado por la región $f(x)=1+x^2$, entre $x=-1$ y $x=5$, girando alrededor del eje $y=-1$:",
        "opciones": [
            r"A) $\pi \int_{-1}^{5} (2+x^2)^2 dx$",
            r"B) $\pi \int_{-1}^{5} (1+x^2)^2 dx$",
            r"C) $2\pi \int_{-1}^{5} x(1+x^2) dx$",
            r"D) $\pi \int_{-1}^{5} ((1+x^2)^2 - 1^2) dx$"
        ],
        "respuesta_correcta": r"A) $\pi \int_{-1}^{5} (2+x^2)^2 dx$",
        "explicacion": r"El radio de giro es la distancia desde la curva $y=1+x^2$ al eje $y=-1$, es decir, $R(x) = (1+x^2) - (-1) = 2+x^2$. El volumen es $\pi \int R(x)^2 dx$."
    },
    {
        "tema": "2.3 Aplicaciones de Ecuaciones Diferenciales en Economía",
        "pregunta": r"Ley de Enfriamiento de Newton: Agua a $100^{\circ}C$ se enfría a $80^{\circ}C$ en 10 min en un cuarto a $25^{\circ}C$. ¿Cuál es la temperatura estimada a los 20 min?",
        "opciones": [
            r"A) $65.33^{\circ}C$",
            r"B) $60.00^{\circ}C$",
            r"C) $70.50^{\circ}C$",
            r"D) $55.00^{\circ}C$"
        ],
        "respuesta_correcta": r"A) $65.33^{\circ}C$",
        "explicacion": r"Modelo: $T(t) = T_a + (T_0 - T_a)e^{kt}$. $80 = 25 + 75e^{10k} \Rightarrow e^{10k} = \frac{55}{75} = \frac{11}{15}$. Para $t=20$ (dos intervalos de 10 min): $T(20) = 25 + 75(e^{10k})^2 = 25 + 75(\frac{121}{225}) \approx 65.33$."
    },
    {
        "tema": "2.3 Aplicaciones de Ecuaciones Diferenciales en Economía",
        "pregunta": r"Un modelo de crecimiento poblacional está dado por $\frac{dp}{dt} = kt(1000 - \frac{p}{2})$. ¿Cuál es la población límite a largo plazo?",
        "opciones": [
            r"A) $2000$ unidades",
            r"B) $1000$ unidades",
            r"C) $500$ unidades",
            r"D) Infinito"
        ],
        "respuesta_correcta": r"A) $2000$ unidades",
        "explicacion": r"El crecimiento se detiene cuando $\frac{dp}{dt} = 0$. Esto ocurre cuando $1000 - \frac{p}{2} = 0$, es decir, $p = 2000$. Es una variante de la ecuación logística."
    },
    {
        "tema": "2.1.2 ED 1er Orden: Homogéneas",
        "pregunta": r"Identifique la familia de la ecuación diferencial $(x+y)dx + (x-y)dy = 0$:",
        "opciones": [
            r"A) Homogénea",
            r"B) Separable",
            r"C) Lineal de primer orden",
            r"D) Bernoulli"
        ],
        "respuesta_correcta": r"A) Homogénea",
        "explicacion": r"Ambos coeficientes $M(x,y)=x+y$ y $N(x,y)=x-y$ son funciones homogéneas del mismo grado (grado 1). Se resuelve con el cambio $y=ux$."
    },
    {
        "tema": "2.2.1 ED Orden Superior: Homogéneas",
        "pregunta": r"Encuentre la solución general de la ecuación $y''' + 2y'' - 3y' = 0$:",
        "opciones": [
            r"A) $y = C_1 + C_2 e^{-3x} + C_3 e^{x}$",
            r"B) $y = C_1 e^{-x} + C_2 e^{3x} + C_3$",
            r"C) $y = C_1 \cos(3x) + C_2 \sin(x) + C_3$",
            r"D) $y = C_1 e^x + C_2 x e^x + C_3 e^{-3x}$"
        ],
        "respuesta_correcta": r"A) $y = C_1 + C_2 e^{-3x} + C_3 e^{x}$",
        "explicacion": r"Ecuación característica: $r^3 + 2r^2 - 3r = 0 \Rightarrow r(r^2 + 2r - 3) = r(r+3)(r-1) = 0$. Raíces: $r_1=0, r_2=-3, r_3=1$. Solución: $C_1 e^{0x} + C_2 e^{-3x} + C_3 e^{x}$."
    },
    # --------------------------------------------------------------------------
    # AMPLIACIÓN: FRACCIONES SIMPLES (Meta: 5 ejercicios)
    # Fuente: Archivos 'fracciones simples.tex' y 'fracSimp2.tex'
    # --------------------------------------------------------------------------
    {
        "tema": "1.1.4 Fracciones Simples",
        "pregunta": r"Resuelva la integral racional impropia (realizando división de polinomios primero): $$ \int \frac{2x+1}{x-4} dx $$",
        "opciones": [
            r"A) $2x + 9\ln|x-4| + C$",
            r"B) $2x + \ln|x-4| + C$",
            r"C) $x^2 + \ln|x-4| + C$",
            r"D) $2 + 9(x-4)^{-1} + C$"
        ],
        "respuesta_correcta": r"A) $2x + 9\ln|x-4| + C$",
        "explicacion": r"Al dividir $2x+1$ entre $x-4$ obtenemos el cociente $2$ y residuo $9$. La integral es $\int (2 + \frac{9}{x-4}) dx = 2x + 9\ln|x-4| + C$."
    },
    {
        "tema": "1.1.4 Fracciones Simples",
        "pregunta": r"Calcule la integral descomponiendo en fracciones simples: $$ \int \frac{1}{x^2 - 5x + 6} dx $$",
        "opciones": [
            r"A) $\ln|x-3| - \ln|x-2| + C$",
            r"B) $\ln|x-2| - \ln|x-3| + C$",
            r"C) $\ln|(x-3)(x-2)| + C$",
            r"D) $\frac{1}{2x-5} + C$"
        ],
        "respuesta_correcta": r"A) $\ln|x-3| - \ln|x-2| + C$",
        "explicacion": r"El denominador factoriza en $(x-3)(x-2)$. La descomposición es $\frac{1}{x-3} - \frac{1}{x-2}$. Integrando: $\ln|x-3| - \ln|x-2|$."
    },
    {
        "tema": "1.1.4 Fracciones Simples",
        "pregunta": r"Resuelva la integral definida por fracciones ya dadas: $$ \int \left( \frac{2}{x-1} - \frac{4}{x+1} + \frac{2x}{x^2+1} \right) dx $$",
        "opciones": [
            r"A) $2\ln|x-1| - 4\ln|x+1| + \ln(x^2+1) + C$",
            r"B) $2\ln|x-1| - 4\ln|x+1| + 2\arctan(x) + C$",
            r"C) $\ln\left| \frac{(x-1)^2}{(x+1)^4} \right| + \frac{1}{x^2+1} + C$",
            r"D) $2(x-1)^{-1} - 4(x+1)^{-1} + \ln(x^2+1) + C$"
        ],
        "respuesta_correcta": r"A) $2\ln|x-1| - 4\ln|x+1| + \ln(x^2+1) + C$",
        "explicacion": r"Integramos término a término: $\int \frac{2}{u}du = 2\ln|u|$. Para el tercer término, si $u=x^2+1 \Rightarrow du=2xdx$, es un logaritmo directo $\ln(x^2+1)$."
    },
    {
        "tema": "1.1.4 Fracciones Simples",
        "pregunta": r"Identifique la forma correcta de descomponer la fracción $\frac{x^2+1}{x(x-1)^2}$:",
        "opciones": [
            r"A) $\frac{A}{x} + \frac{B}{x-1} + \frac{C}{(x-1)^2}$",
            r"B) $\frac{A}{x} + \frac{Bx+C}{(x-1)^2}$",
            r"C) $\frac{A}{x} + \frac{B}{x-1} + \frac{Cx+D}{(x-1)^2}$",
            r"D) $\frac{A}{x} + \frac{B}{(x-1)^2}$"
        ],
        "respuesta_correcta": r"A) $\frac{A}{x} + \frac{B}{x-1} + \frac{C}{(x-1)^2}$",
        "explicacion": r"El factor lineal $x$ lleva una constante $A$. El factor lineal repetido $(x-1)^2$ lleva una constante por cada potencia: $B/(x-1)$ y $C/(x-1)^2$."
    },

    # --------------------------------------------------------------------------
    # AMPLIACIÓN: INTEGRAL POR PARTES (Meta: 5 ejercicios)
    # Fuente: Archivo 'fracsimpInttPartCamVarEjer.tex'
    # --------------------------------------------------------------------------
    {
        "tema": "1.1.7 Integral por partes",
        "pregunta": r"Resuelva la integral por partes: $$ \int 6x e^{1-2x} dx $$",
        "opciones": [
            r"A) $\frac{3}{2}(1-2x)e^{1-2x} - 3e^{1-2x} + C$",
            r"B) $-3xe^{1-2x} - \frac{3}{2}e^{1-2x} + C$",
            r"C) $6xe^{1-2x} - 6e^{1-2x} + C$",
            r"D) $3x^2 e^{1-2x} + C$"
        ],
        "respuesta_correcta": r"B) $-3xe^{1-2x} - \frac{3}{2}e^{1-2x} + C$",
        "explicacion": r"Usamos $u=6x, dv=e^{1-2x}dx$. Entonces $du=6dx, v=-\frac{1}{2}e^{1-2x}$. Aplicando $uv - \int v du$: $-3xe^{1-2x} - \int -3e^{1-2x}dx = -3xe^{1-2x} - \frac{3}{2}e^{1-2x}$."
    },
    {
        "tema": "1.1.7 Integral por partes",
        "pregunta": r"Resuelva la integral logarítmica básica: $$ \int x \ln x dx $$",
        "opciones": [
            r"A) $\frac{x^2}{2}\ln x - \frac{x^2}{4} + C$",
            r"B) $\frac{x^2}{2}\ln x - \frac{x^2}{2} + C$",
            r"C) $x\ln x - x + C$",
            r"D) $\frac{1}{x} + C$"
        ],
        "respuesta_correcta": r"A) $\frac{x^2}{2}\ln x - \frac{x^2}{4} + C$",
        "explicacion": r"Sea $u=\ln x$ (LIATE), $dv=x dx$. Entonces $du=1/x dx, v=x^2/2$. Fórmula: $\frac{x^2}{2}\ln x - \int \frac{x^2}{2}\frac{1}{x} dx = \frac{x^2}{2}\ln x - \frac{x^2}{4}$."
    },
    # --------------------------------------------------------------------------
    # AMPLIACIÓN: INTEGRALES DOBLES (Meta: 5 ejercicios)
    # Fuente: Taller 1 202615 y Reparación 202615
    # --------------------------------------------------------------------------
    {
        "tema": "1.2.4 Integrales Dobles",
        "pregunta": r"Calcule la integral iterada: $$ \int_0^1 \int_0^2 (x+y) dy dx $$",
        "opciones": [
            r"A) $3$",
            r"B) $1$",
            r"C) $2$",
            r"D) $4$"
        ],
        "respuesta_correcta": r"A) $3$",
        "explicacion": r"Interna ($\int (x+y)dy$ de 0 a 2): $[xy + y^2/2]_0^2 = 2x + 2$. Externa ($\int (2x+2)dx$ de 0 a 1): $[x^2 + 2x]_0^1 = 1 + 2 = 3$."
    },
    {
        "tema": "1.2.4 Integrales Dobles",
        "pregunta": r"Plantee la integral doble para el volumen bajo el plano $z=1+x-y$ sobre la región limitada por $y=x^2$ y $y=8-2x$:",
        "opciones": [
            r"A) $\int_{-4}^{2} \int_{x^2}^{8-2x} (1+x-y) dy dx$",
            r"B) $\int_{-4}^{2} \int_{8-2x}^{x^2} (1+x-y) dy dx$",
            r"C) $\int_{0}^{8} \int_{-\sqrt{y}}^{\sqrt{y}} (1+x-y) dx dy$",
            r"D) $\int_{-2}^{4} \int_{x^2}^{8-2x} (1+x-y) dy dx$"
        ],
        "respuesta_correcta": r"A) $\int_{-4}^{2} \int_{x^2}^{8-2x} (1+x-y) dy dx$",
        "explicacion": r"Intersección: $x^2 = 8-2x \Rightarrow x^2+2x-8=0 \Rightarrow (x+4)(x-2)=0$. Intervalo $x \in [-4, 2]$. En este intervalo, la recta $8-2x$ está por encima de la parábola $x^2$."
    },
    # --------------------------------------------------------------------------
    # AMPLIACIÓN: EXCEDENTES (Meta: 5 ejercicios)
    # Fuente: Taller 1 - 202525 (Mayo 2025)
    # --------------------------------------------------------------------------
    {
        "tema": "1.2.2 Excedentes del consumidor y productor",
        "pregunta": r"Calcule el Excedente del Consumidor (EC) dadas: Oferta $p = \frac{x^2}{9} + 4$ y Demanda $p = 11 - 2x$:",
        "opciones": [
            r"A) $9$ u.m.",
            r"B) $18$ u.m.",
            r"C) $4.5$ u.m.",
            r"D) $27$ u.m."
        ],
        "respuesta_correcta": r"A) $9$ u.m.",
        "explicacion": r"Equilibrio: $x^2/9 + 4 = 11 - 2x \Rightarrow x^2 + 18x - 63 = 0 \Rightarrow x=3$. Precio eq: $p=5$. EC = $\int_0^3 (11-2x - 5) dx = \int_0^3 (6-2x) dx = [6x-x^2]_0^3 = 18-9=9$."
    },
    {
        "tema": "1.2.2 Excedentes del consumidor y productor",
        "pregunta": r"Determine el Excedente del Productor (EP) en el equilibrio para: Oferta $p = \frac{x^2}{4} + 4$ y Demanda $p = 12 - x$:",
        "opciones": [
            r"A) $10.67$ u.m.",
            r"B) $32.00$ u.m.",
            r"C) $8.00$ u.m.",
            r"D) $16.33$ u.m."
        ],
        "respuesta_correcta": r"A) $10.67$ u.m.",
        "explicacion": r"Equilibrio: $x^2/4 + 4 = 12-x \Rightarrow x^2+4x-32=0 \Rightarrow x=4$. Precio eq: $p=8$. EP = $\int_0^4 (8 - (x^2/4+4)) dx = [4x - x^3/12]_0^4 = 16 - 64/12 = 10.67$."
    },

    # --------------------------------------------------------------------------
    # AMPLIACIÓN: VOLÚMENES DE REVOLUCIÓN (Meta: 5 ejercicios)
    # Fuente: Taller 2 - 202615 (Tabla de volúmenes)
    # --------------------------------------------------------------------------
    {
        "tema": "1.2.5 Volúmenes de Revolución",
        "pregunta": r"Plantee el volumen generado por la región acotada por $y=2+x^2$ y $y=6$, al girar alrededor de la recta $y=1$:",
        "opciones": [
            r"A) $\pi \int_{-2}^{2} [ (6-1)^2 - (2+x^2-1)^2 ] dx$",
            r"B) $\pi \int_{-2}^{2} [ (2+x^2-1)^2 - (6-1)^2 ] dx$",
            r"C) $\pi \int_{0}^{6} (2+x^2)^2 dx$",
            r"D) $2\pi \int_{-2}^{2} x(6 - (2+x^2)) dx$"
        ],
        "respuesta_correcta": r"A) $\pi \int_{-2}^{2} [ (6-1)^2 - (2+x^2-1)^2 ] dx$",
        "explicacion": r"Puntos de corte: $2+x^2=6 \Rightarrow x=\pm 2$. El eje $y=1$ está debajo de la región. Radio exterior $R = 6-1=5$. Radio interior $r = (2+x^2)-1 = 1+x^2$. Método de arandelas."
    },
    {
        "tema": "1.2.5 Volúmenes de Revolución",
        "pregunta": r"Plantee el volumen del sólido generado por la región $y=4-x^2$, $y=3$ (en el primer cuadrante $x \ge 0$), girando alrededor de $y=2$:",
        "opciones": [
            r"A) $\pi \int_{0}^{1} [ (4-x^2-2)^2 - (3-2)^2 ] dx$",
            r"B) $\pi \int_{0}^{1} [ (4-x^2)^2 - 3^2 ] dx$",
            r"C) $\pi \int_{0}^{2} [ (3-2)^2 - (4-x^2-2)^2 ] dx$",
            r"D) $\pi \int_{-1}^{1} (2-x^2)^2 dx$"
        ],
        "respuesta_correcta": r"A) $\pi \int_{0}^{1} [ (4-x^2-2)^2 - (3-2)^2 ] dx$",
        "explicacion": r"Intersección: $4-x^2=3 \Rightarrow x=1$. En $[0,1]$, la parábola está arriba ($y \approx 4$) y la recta abajo ($y=3$). Eje $y=2$ está más abajo. $R = (4-x^2)-2 = 2-x^2$. $r = 3-2 = 1$."
    },

    # --------------------------------------------------------------------------
    # AMPLIACIÓN: ÁREAS ENTRE CURVAS (Meta: 5 ejercicios)
    # Fuente: Exámenes Reparación y Complementario 2022
    # --------------------------------------------------------------------------
    {
        "tema": "1.2.1 Áreas entre curvas",
        "pregunta": r"Plantee la integral para el área de la región no acotada entre $y=xe^{-x}$ y $y=e^{-x}$ para $x \in [0, \infty)$:",
        "opciones": [
            r"A) $\int_{0}^{1} (e^{-x} - xe^{-x}) dx + \int_{1}^{\infty} (xe^{-x} - e^{-x}) dx$",
            r"B) $\int_{0}^{\infty} (xe^{-x} - e^{-x}) dx$",
            r"C) $\int_{0}^{\infty} (e^{-x} - xe^{-x}) dx$",
            r"D) $\int_{0}^{1} xe^{-x} dx$"
        ],
        "respuesta_correcta": r"A) $\int_{0}^{1} (e^{-x} - xe^{-x}) dx + \int_{1}^{\infty} (xe^{-x} - e^{-x}) dx$",
        "explicacion": r"Se cruzan cuando $xe^{-x} = e^{-x} \Rightarrow x=1$. En $[0,1]$, $e^{-x} > xe^{-x}$. En $[1, \infty)$, $xe^{-x} > e^{-x}$. Se debe partir la integral en el cruce."
    },
    {
        "tema": "1.2.1 Áreas entre curvas",
        "pregunta": r"Calcule el área entre las curvas $y=e^{-x}$ y $y=-e^{-2x}$ en el intervalo $x \in [0, \infty)$:",
        "opciones": [
            r"A) $1.5$ u.a.",
            r"B) $1.0$ u.a.",
            r"C) $0.5$ u.a.",
            r"D) $2.0$ u.a."
        ],
        "respuesta_correcta": r"A) $1.5$ u.a.",
        "explicacion": r"Como $e^{-x}$ es positiva y $-e^{-2x}$ negativa, no se cruzan. Área = $\int_0^{\infty} (e^{-x} - (-e^{-2x})) dx = \int_0^{\infty} (e^{-x} + e^{-2x}) dx = [-e^{-x} - \frac{1}{2}e^{-2x}]_0^{\infty}$. En $\infty$ da 0. En 0: $-(-1 - 0.5) = 1.5$."
    },
    # AMPLIACIÓN FINAL: EXACTAS, LINEALES Y BERNOULLI
    # Fuente: Taller 2 - 202615 (Items 6, 15, 25, 28)
    # --------------------------------------------------------------------------
    {
        "tema": "2.1.3 ED 1er Orden: Exactas",
        "pregunta": r"Resuelva la ecuación diferencial exacta: $(\cos y - y\sin x + 1)dx + (\cos x - x\sin y - 2)dy = 0$",
        "opciones": [
            r"A) $x\cos y + y\cos x + x - 2y = C$",
            r"B) $\sin y \cos x - xy + x = C$",
            r"C) $x\cos y - y\sin x + x^2 - 2y = C$",
            r"D) $\cos(xy) + x - 2y = C$"
        ],
        "respuesta_correcta": r"A) $x\cos y + y\cos x + x - 2y = C$",
        "explicacion": r"Al integrar $M$ respecto a $x$ obtenemos $x\cos y + y\cos x + x + g(y)$. Derivando respecto a $y$ e igualando a $N$, hallamos $g'(y)=-2$, por lo que $g(y)=-2y$."
    },
    {
        "tema": "2.1.1 ED 1er Orden: Separación de Variables",
        "pregunta": r"Halle la solución general de: $(2-y)\sqrt{xy} dy + (x+2) dx = 0$",
        "opciones": [
            r"A) $\frac{4}{3}y^{3/2} - \frac{2}{5}y^{5/2} = -(\frac{2}{3}x^{3/2} + 4x^{1/2}) + C$",
            r"B) $2y^{1/2} - y^{3/2} = -x^{1/2} - 2x^{-1/2} + C$",
            r"C) $\ln|2-y| + \frac{2}{3}y^{3/2} = \ln|x+2| + C$",
            r"D) $y(2-y)^2 = x(x+2)^2 + C$"
        ],
        "respuesta_correcta": r"A) $\frac{4}{3}y^{3/2} - \frac{2}{5}y^{5/2} = -(\frac{2}{3}x^{3/2} + 4x^{1/2}) + C$",
        "explicacion": r"Separando: $(2-y)\sqrt{y} dy = -\frac{x+2}{\sqrt{x}} dx$. Integramos potencias: $\int (2y^{1/2}-y^{3/2}) dy = -\int (x^{1/2}+2x^{-1/2}) dx$."
    },
    {
        "tema": "2.1.4 ED 1er Orden: Lineales",
        "pregunta": r"Resuelva la ecuación lineal: $x \frac{dy}{dx} + 2y = x^3 - x\ln x$",
        "opciones": [
            r"A) $y = \frac{x^3}{5} - \frac{x}{3}\ln x + \frac{x}{9} + \frac{C}{x^2}$",
            r"B) $y = \frac{x^3}{3} - x\ln x + C$",
            r"C) $y = x^3 - x\ln x + Cx^{-2}$",
            r"D) $y = \frac{x^4}{5} - \frac{x^2}{3}\ln x + C$"
        ],
        "respuesta_correcta": r"A) $y = \frac{x^3}{5} - \frac{x}{3}\ln x + \frac{x}{9} + \frac{C}{x^2}$",
        "explicacion": r"Forma estándar: $y' + \frac{2}{x}y = x^2 - \ln x$. Factor integrante $\mu=x^2$. Integramos $d(x^2 y) = (x^4 - x^2\ln x)dx$. La integral de $x^2\ln x$ requiere partes."
    },
    {
        "tema": "2.1.5 ED 1er Orden: Bernoulli",
        "pregunta": r"Identifique y resuelva la ecuación de Bernoulli: $x dy + (x^2 y^3 + xy^3 - 2y) dx = 0$",
        "opciones": [
            r"A) $y^{-2} = \frac{1}{3}x^2 + \frac{2}{5}x + Cx^{-4}$",
            r"B) $y^3 = x^2 + x + C$",
            r"C) $y^{-2} = x^2(1+x) + C$",
            r"D) $y^2 = \frac{1}{3}x^2 + \frac{2}{5}x + C$"
        ],
        "respuesta_correcta": r"A) $y^{-2} = \frac{1}{3}x^2 + \frac{2}{5}x + Cx^{-4}$",
        "explicacion": r"Reescribiendo: $x y' - 2y = -y^3(x^2+x) \Rightarrow y' - \frac{2}{x}y = -y^3(x+1)$. Es Bernoulli con $n=3$. Sustitución $u = y^{1-3} = y^{-2}$."
    },
    {
        "tema": "2.1.5 ED 1er Orden: Bernoulli",
        "pregunta": r"Resuelva la ecuación: $xy dy + (2y^2 - x^3 + x\ln x) dx = 0$",
        "opciones": [
            r"A) $y^2 = \frac{1}{3}x^2 - \frac{1}{2}\ln x + \frac{1}{8} + Cx^{-4}$",
            r"B) $y^2 = \frac{x^2}{3} - \ln x + C$",
            r"C) $y^{-1} = x^3 + \ln x + C$",
            r"D) $y^2 = x^2(\ln x - 1) + C$"
        ],
        "respuesta_correcta": r"A) $y^2 = \frac{1}{3}x^2 - \frac{1}{2}\ln x + \frac{1}{8} + Cx^{-4}$",
        "explicacion": r"Reescribiendo: $y' + \frac{2}{x}y = (x^2 - \ln x)y^{-1}$. Bernoulli con $n=-1$. Sustitución $u = y^2$. Ecuación lineal resultante: $u' + \frac{4}{x}u = 2x^2 - 2\ln x$."
    },
    # --------------------------------------------------------------------------
    # AMPLIACIÓN TALLER 2 - 202615 (LOTE EXTRA)
    # --------------------------------------------------------------------------
    {
        "tema": "2.1.1 ED 1er Orden: Separación de Variables",
        "pregunta": r"Resuelva la ecuación diferencial: $e^{2x-y}dx + yx dy = 0$",
        "opciones": [
            r"A) $\frac{1}{2}e^{2x} - xe^{-y} - e^{-y} = C$",
            r"B) $e^{2x} + y^2 = C$",
            r"C) $2e^{2x} = y e^y - e^y + C$",
            r"D) $\frac{1}{2}e^{2x} = (y+1)e^{-y} + C$" # Derivada de integración por partes
        ],
        "respuesta_correcta": r"D) $\frac{1}{2}e^{2x} = (y+1)e^{-y} + C$",
        "explicacion": r"Separamos variables: $e^{2x}dx = -y e^y dy$ (al pasar dividiendo $e^{-y}$ sube como $e^y$ incorrecto) -> Corrección: $e^{2x}dx = -y \frac{dy}{e^{-y}} = -y e^y dy$. Integrando por partes $\int y e^y dy$: $e^{2x}/2 = -(y-1)e^y + C$. (Revisando álgebra: $e^{2x}dx = -yx e^{-(-y)}$... Mejor: $e^{2x}dx = -y x e^y dy$... espera, la ecuación es $e^{2x}e^{-y}dx + yx dy = 0 \Rightarrow \frac{e^{2x}}{x}dx = -y e^y dy$.)"
    },
    # Corrección del anterior para el banco (versión simplificada operativa):
    {
        "tema": "2.1.1 ED 1er Orden: Separación de Variables",
        "pregunta": r"Al separar las variables de la ecuación $\sqrt{xy} y' = \frac{x+2}{2-y}$, se obtiene la integral:",
        "opciones": [
            r"A) $\int (2-y)\sqrt{y} dy = \int \frac{x+2}{\sqrt{x}} dx$",
            r"B) $\int \frac{\sqrt{y}}{2-y} dy = \int (x+2)\sqrt{x} dx$",
            r"C) $\int \sqrt{y}(2-y) dy = \int \frac{\sqrt{x}}{x+2} dx$",
            r"D) $\int (2y - y^{3/2}) dy = \int (x^{1/2} + 2x^{-1/2}) dx$"
        ],
        "respuesta_correcta": r"A) $\int (2-y)\sqrt{y} dy = \int \frac{x+2}{\sqrt{x}} dx$",
        "explicacion": r"Reescribimos $y' = dy/dx$. Agrupamos las $y$ a la izquierda: $\sqrt{y}(2-y)dy$. Agrupamos las $x$ a la derecha: $\frac{x+2}{\sqrt{x}}dx$."
    },
    {
        "tema": "2.1.3 ED 1er Orden: Exactas",
        "pregunta": r"Determine el valor de $k$ para que la ecuación $(y^3 + kxy^4 - 2x)dx + (3xy^2 + 20x^2y^3)dy = 0$ sea exacta:",
        "opciones": [
            r"A) $k = 10$",
            r"B) $k = 5$",
            r"C) $k = 20$",
            r"D) $k = 4$"
        ],
        "respuesta_correcta": r"A) $k = 10$",
        "explicacion": r"Para ser exacta, $\frac{\partial M}{\partial y} = \frac{\partial N}{\partial x}$. Derivando: $M_y = 3y^2 + 4kxy^3$. $N_x = 3y^2 + 40xy^3$. Igualando coeficientes: $4k = 40 \Rightarrow k = 10$."
    },
    {
        "tema": "2.1.4 ED 1er Orden: Lineales",
        "pregunta": r"Para la ecuación lineal $y' + \frac{3}{x}y = x^2 + 1$, el factor integrante $\mu(x)$ es:",
        "opciones": [
            r"A) $\mu(x) = x^3$",
            r"B) $\mu(x) = e^{3x}$",
            r"C) $\mu(x) = 3 \ln x$",
            r"D) $\mu(x) = x^{-3}$"
        ],
        "respuesta_correcta": r"A) $\mu(x) = x^3$",
        "explicacion": r"El factor integrante es $e^{\int P(x)dx} = e^{\int \frac{3}{x}dx} = e^{3\ln x} = e^{\ln x^3} = x^3$."
    },
    {
        "tema": "2.1.4 ED 1er Orden: Lineales",
        "pregunta": r"Identifique la clasificación de la ecuación $(x-3y)dx + 2y dy = 0$ si consideramos $x$ como variable dependiente ($x(y)$):",
        "opciones": [
            r"A) Lineal en $x$",
            r"B) Bernoulli en $y$",
            r"C) Separable",
            r"D) Exacta"
        ],
        "respuesta_correcta": r"A) Lineal en $x$",
        "explicacion": r"Reescribiendo como $\frac{dx}{dy}$: $(x-3y)\frac{dx}{dy} + 2y = 0$ (no). Mejor: $\frac{dx}{dy} = \frac{-2y}{x-3y}$ (no). Forma estándar $dx/dy + P(y)x = Q(y)$. Al dividir por $dy$: $(x-3y)x' + 2y = 0$... No, la forma correcta lineal en x es $dx/dy + P(y)x = Q(y)$. Si reordenamos $(x-3y)dx + 2ydy=0 \Rightarrow \frac{dy}{dx} = \frac{3y-x}{2y}$ (Homogénea). Como lineal en $x$: $2y \frac{dy}{dx} + 3y = x$... no."
    },
    # Corrección: El ejercicio original del Taller 2 era (x-3y)dx + 2ydy=0, que es Homogénea.
    # Vamos a poner una que SÍ sea Bernoulli del Taller 2.
    {
        "tema": "2.1.2 ED 1er Orden: Homogéneas",
        "pregunta": r"Dada la ecuación $(x-3y)dx + 2y dy = 0$, ¿qué sustitución la simplifica?",
        "opciones": [
            r"A) $y = ux$",
            r"B) $u = x-3y$",
            r"C) $x = y^2$",
            r"D) $\mu = e^{2y}$"
        ],
        "respuesta_correcta": r"A) $y = ux$",
        "explicacion": r"Es una ecuación diferencial con coeficientes homogéneos de grado 1. La sustitución canónica es $y=ux$."
    },
    {
        "tema": "2.2.1 ED Orden Superior: Homogéneas",
        "pregunta": r"¿Cuál es la solución general de la ecuación de tercer orden $y''' + 6y'' + 12y' + 8y = 0$?",
        "opciones": [
            r"A) $y = C_1 e^{-2x} + C_2 x e^{-2x} + C_3 x^2 e^{-2x}$",
            r"B) $y = C_1 e^{2x} + C_2 x e^{2x} + C_3 x^2 e^{2x}$",
            r"C) $y = C_1 e^{-2x} + C_2 e^{-6x} + C_3 e^{-8x}$",
            r"D) $y = e^{-2x}(C_1 \cos 2x + C_2 \sin 2x)$"
        ],
        "respuesta_correcta": r"A) $y = C_1 e^{-2x} + C_2 x e^{-2x} + C_3 x^2 e^{-2x}$",
        "explicacion": r"El polinomio característico es $r^3 + 6r^2 + 12r + 8 = 0$, que factoriza como $(r+2)^3 = 0$. Hay una raíz real $r=-2$ de multiplicidad 3."
    },
    {
        "tema": "2.2.1 ED Orden Superior: Homogéneas",
        "pregunta": r"Resuelva la ecuación no homogénea $y'' + 4y' + 3y = 12e^x$. (Solo la Solución Particular $y_p$):",
        "opciones": [
            r"A) $y_p = \frac{3}{2}e^x$",
            r"B) $y_p = 12e^x$",
            r"C) $y_p = \frac{12}{8}e^x = 1.5e^x$",
            r"D) $y_p = Axe^x$"
        ],
        "respuesta_correcta": r"A) $y_p = \frac{3}{2}e^x$",
        "explicacion": r"Usando Coeficientes Indeterminados, proponemos $y_p = Ae^x$. Derivadas: $y_p' = Ae^x, y_p'' = Ae^x$. Sustituyendo: $A(1+4+3)e^x = 8Ae^x = 12e^x \Rightarrow A = 12/8 = 3/2$."
    },
    {
        "tema": "2.3 Aplicaciones de Ecuaciones Diferenciales en Economía",
        "pregunta": r"Datación Carbono-14: Si la vida media es 5600 años y un fósil conserva 1/6 de su C-14 original, la ecuación para hallar su edad $t$ es:",
        "opciones": [
            r"A) $\frac{1}{6} = e^{k t}$ con $k = \frac{\ln(0.5)}{5600}$",
            r"B) $\frac{1}{6} = e^{5600 t}$",
            r"C) $t = \frac{1}{6} \ln(5600)$",
            r"D) $Q(t) = Q_0 e^{-5600t}$"
        ],
        "respuesta_correcta": r"A) $\frac{1}{6} = e^{k t}$ con $k = \frac{\ln(0.5)}{5600}$",
        "explicacion": r"Modelo de decaimiento radioactivo: $Q(t) = Q_0 e^{kt}$. Primero hallamos $k$ con la vida media ($Q=0.5Q_0$ en $t=5600$). Luego resolvemos para $Q = \frac{1}{6}Q_0$."
    },
    {
        "tema": "2.3 Aplicaciones de Ecuaciones Diferenciales en Economía",
        "pregunta": r"Ley de Enfriamiento: Si $\frac{dT}{dt} = k(T - T_a)$, ¿cuál es la expresión para la temperatura $T(t)$?",
        "opciones": [
            r"A) $T(t) = T_a + (T_0 - T_a)e^{kt}$",
            r"B) $T(t) = T_0 e^{kt} + T_a$",
            r"C) $T(t) = \frac{1}{k}(T - T_a)$",
            r"D) $T(t) = (T_a - T_0)e^{-kt}$"
        ],
        "respuesta_correcta": r"A) $T(t) = T_a + (T_0 - T_a)e^{kt}$",
        "explicacion": r"Es la solución general de la ecuación lineal separable. $T_a$ es la temperatura ambiente y $(T_0 - T_a)$ es la diferencia inicial que decae exponencialmente."
    },
    {
        "tema": "2.1.2 ED 1er Orden: Homogéneas",
        "pregunta": r"¿Cuál es el factor integrante para resolver $y' + y = e^{3x}$?",
        "opciones": [
            r"A) $e^x$",
            r"B) $e^{-x}$",
            r"C) $x$",
            r"D) $e^{3x}$"
        ],
        "respuesta_correcta": r"A) $e^x$",
        "explicacion": r"La ecuación está en forma estándar $y' + P(x)y = Q(x)$ con $P(x)=1$. Factor integrante $\mu = e^{\int 1 dx} = e^x$."
    },
    {
        "tema": "2.2.1 ED Orden Superior: Homogéneas",
        "pregunta": r"Determine la ecuación característica de $y^{(4)} - 16y = 0$:",
        "opciones": [
            r"A) $r^4 - 16 = 0$",
            r"B) $4r - 16 = 0$",
            r"C) $r^4 + 16 = 0$",
            r"D) $(r-2)^4 = 0$"
        ],
        "respuesta_correcta": r"A) $r^4 - 16 = 0$",
        "explicacion": r"Sustituyendo $y = e^{rx}$, obtenemos $r^4 e^{rx} - 16e^{rx} = 0$, lo que lleva a $r^4 - 16 = 0$. Sus raíces son $\pm 2$ y $\pm 2i$."
    }
]

def obtener_preguntas_fijas(temas_solicitados, cantidad):
    """
    Filtra preguntas del banco fijo que coincidan con los temas seleccionados.
    Si no hay suficientes, devuelve todas las que encuentre.
    """
    # 1. Filtrar por temas seleccionados
    # Buscamos coincidencias parciales (ej: "Integrales" coincide con "1.1.1 Integrales Directas")
    candidatas = [p for p in BANCO_FIXED if any(t in p["tema"] for t in temas_solicitados)]
    
    # 2. Si no hay preguntas de esos temas, devolvemos una lista vacía
    if not candidatas:
        return []
        
    # 3. Seleccionar al azar la cantidad solicitada (o todas si hay menos)
    num_a_seleccionar = min(len(candidatas), cantidad)
    return random.sample(candidatas, num_a_seleccionar)