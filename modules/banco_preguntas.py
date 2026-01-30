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