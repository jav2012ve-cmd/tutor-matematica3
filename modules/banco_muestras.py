# modules/banco_muestras.py

# ==============================================================================
# BANCO DE ESTILOS REALES - MATEMÁTICAS III (ECONOMÍA UCAB)
# Fuente: Primeros y Segundos Parciales (2024-2026)
# Contenido: Integrales, Ecuaciones Diferenciales, Modelado y Multivariable
# ==============================================================================

EJEMPLOS_ESTILO = r"""
--- SECCIÓN 1: CÁLCULO INTEGRAL Y APLICACIONES (PRIMER PARCIAL) ---

EJEMPLO 1 (TIPO: Integral con "Trampa" de Variables):
"Calcule la siguiente integral indefinida. Fíjese bien en el diferencial:
$$ \int (ax^3 + by^4)^{20} x^2 y^3 dy $$
(Nota: Aquí la variable es 'y', 'x' actúa como constante)."

EJEMPLO 2 (TIPO: Planteamiento de Área - Sin Cálculo):
"Grafique y plantee (NO NECESITA CALCULAR) las integrales necesarias para hallar el área encerrada por las funciones en el intervalo $x \in [-5,5]$:
$$ f(x) = \frac{x^2}{2} + x + 2 $$
$$ g(x) = 2x + 2 $$
Debe plantear la suma de integrales si las curvas se cruzan."

EJEMPLO 3 (TIPO: Cambio de Variable Dirigido):
"Aplique el cambio de variable $z = 2 - x^3$ y escriba la integral resultante en términos de $z$. 
Instrucción: NO LA RESUELVA, solo llegue hasta la expresión simplificada en $z$.
Integral:
$$ \int_{-2}^{1} (1-x) x^2 \sqrt{2-x^3} dx $$"

EJEMPLO 4 (TIPO: Estadística - Función de Densidad):
"Sea la función $f(x) = x e^{-x}$ definida para $x \in [0, \infty)$.
1. Confirme matemáticamente (usando integral impropia) si es una función de densidad (PDF).
2. Calcule la probabilidad $P(x \geq 2 \vee x \leq 5)$."

EJEMPLO 5 (TIPO: Excedentes y Gasto Real):
"Dadas las funciones de precio:
$$ \text{Oferta: } p(q) = \frac{q^2}{16} + 14 $$
$$ \text{Demanda: } p(q) = 16 - \frac{q}{4} $$
1. Calcule el punto de equilibrio.
2. Identifique y calcule el Excedente del Productor, del Consumidor y el Gasto Real."

EJEMPLO 6 (TIPO: Integral Impropia Logarítmica):
"Analice la convergencia y calcule si es posible:
$$ \int_{2}^{\infty} \frac{\ln x + 1}{x \ln^3 x} dx $$"

EJEMPLO 7 (TIPO: Volúmenes - Ejes No Tradicionales):
"Plantee las integrales (NO CALCULE) para hallar el volumen del sólido generado al girar la región acotada por $y=-x^2+4x$ y $y=-x+4$.
Eje de giro: La recta vertical $x = -3$."

EJEMPLO 8 (TIPO: Conceptual):
"Responda Verdadero o Falso:
La integral $\int g(f(x)) \cdot f'(x) dx$ puede reescribirse directamente como $\int g(z) dz$ aplicando el cambio $z=f(x)$."

--- SECCIÓN 2: ECUACIONES DIFERENCIALES Y MODELADO (SEGUNDO PARCIAL) ---

EJEMPLO 9 (TIPO: Dinámica de Precios con Expectativas - 2do Orden):
"Si $Q_{D} = 4p'' + 2p' + 3p - 7e^{-t}$ representa la demanda, donde $p'$ es la variación del precio y $p''$ son las expectativas.
La Oferta es $Q_{O} = 3p'' - p' + p - 4$.
Condiciones iniciales: $p(0)=2$ y $p'(0)=4$.
1. Halle la función de precios $p(t)$.
2. Explique su comportamiento a corto, mediano y largo plazo."

EJEMPLO 10 (TIPO: Ecuación de Bernoulli):
"Resuelva la siguiente ecuación diferencial (identifique si es Bernoulli):
$$ 6(1+y)x' + 12x = x^2 y^2 $$"

EJEMPLO 11 (TIPO: Modelado de Temperatura Variable):
"La relación entre la temperatura $T$ y el tiempo $t$ es:
$$ \frac{dT}{dt} = \frac{T - T_a}{t+1} $$
Donde $T_a$ es la temperatura ambiente. Encuentre la relación $T = f(t)$. Si $T_0=10^\circ C$, ¿qué comportamiento se observa?"

EJEMPLO 12 (TIPO: Integrales Dobles - Planteamiento):
"Utilice la región $R$ definida por el cruce de las funciones (grafique primero) para plantear las integrales (NO CALCULE) que permitan hallar:
$$ \iint_{R} (x-y) dA $$"

EJEMPLO 13 (TIPO: Ecuación Diferencial Exacta):
"Resuelva y compruebe si es exacta:
$$ (5\ln y + 108xy + 36x^2 + 81y^2 + 5) dy + (12x^2 + 72xy + 54y^2) dx = 0 $$"

EJEMPLO 14 (TIPO: Crecimiento Poblacional Modificado):
"La población de una colonia crece según:
$$ \frac{dP}{dt} = \left( 100 - \frac{P}{4} \right) t $$
Si $P(0)=100$, halle la función $P(t)$."

EJEMPLO 15 (TIPO: Teoría de ED de Orden Superior):
"Verdadero o Falso: Si el polinomio característico de una ecuación de orden superior es $D^2 + 9$, entonces su solución general es $y = C_1 \cos(3x) + C_2 \sin(3x)$."

EJEMPLO 16 (TIPO: ED Homogénea o Factor Integrante):
"Resuelva la siguiente ecuación diferencial:
$$ xy dy + (y^2 + x^2) dx = 0 $$"
"""