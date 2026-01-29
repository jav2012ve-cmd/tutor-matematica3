# modules/banco_muestras.py

# ==============================================================================
# BANCO DE ESTILOS REALES - MATEMÁTICAS III (ECONOMÍA UCAB)
# Fuente: Taller 1, Taller 2 y Parciales (2025-2026)
# ==============================================================================

EJEMPLOS_ESTILO = r"""
EJEMPLO 1 (TIPO: Dinámica de Precios con Expectativas - Ecuación Diferencial 2do Orden):
"Si $Q_{D} = 4p'' - 2p' + 3p - 7t$ representa la demanda, donde $p'(t)$ es la variación del precio y $p''(t)$ son las expectativas de cambio.
La Oferta es $Q_{O} = 3p'' - 3p' + 15p - 5$.
Si las condiciones iniciales son $p(0)=2$ y $p'(0)=4$:
1. Halle la función de precios $p(t)$.
2. Explique su comportamiento a corto, mediano y largo plazo (¿es estable?)."

EJEMPLO 2 (TIPO: Crecimiento Poblacional - Modelo Logístico Modificado):
"Una colonia de bacterias crece según la expresión:
$$ \frac{dp}{dt} = k \cdot t \left( 1000 - \frac{p}{2} \right) $$
Si la población inicial es 50 y al cabo de 2 horas es 300:
¿Cuál es el comportamiento de $p(t)$ a largo plazo? ¿Existe un límite de saturación?"

EJEMPLO 3 (TIPO: Excedentes del Consumidor y Productor):
"Dadas las funciones de oferta y demanda:
$$ \text{Demanda: } f(x) = 14 - \frac{x^2}{9} $$
$$ \text{Oferta: } g(x) = x^2 + 4 $$
1. Encuentre el punto de equilibrio.
2. Calcule el Excedente del Consumidor y del Productor.
3. Identifique gráficamente el Gasto Real."

EJEMPLO 4 (TIPO: Volúmenes de Revolución - Ejes desplazados):
"Grafique y plantee (NO calcule) la integral para hallar el volumen del sólido generado por la región limitada por:
$$ f(x) = 4 - x^2, \quad y = 3, \quad x = 0 $$
Al girar alrededor del eje $y = 2$.
Explique la geometría del método utilizado (Arandelas o Discos)."

EJEMPLO 5 (TIPO: Función de Densidad de Probabilidad):
"Sea la función $f(x) = 4x^2 e^{-2x}$ para $x \in [0, \infty)$.
1. Confirme matemáticamente si cumple las condiciones para ser una función de densidad de probabilidad (FDP).
2. Calcule la probabilidad $P(1 \leq x \leq 5)$."

EJEMPLO 6 (TIPO: Ley de Enfriamiento de Newton):
"Un cuerpo a 100°C se enfría a 80°C en 10 minutos, estando en un cuarto a 25°C.
1. Encuentre la temperatura después de 20 minutos.
2. ¿En qué momento exacto la temperatura será de 40°C?"

EJEMPLO 7 (TIPO: Datación Carbono 14 - Análisis de Sensibilidad):
"Un hueso fósil contiene el 17% de su Carbono-14 original (vida media 5730 años).
1. Estime la antigüedad.
2. Repita el cálculo suponiendo que conserva el 18%.
¿Qué concluye sobre la sensibilidad de la datación ante pequeños errores de medición?"

EJEMPLO 8 (TIPO: Ecuación Diferencial Exacta):
"Resuelva la siguiente ecuación diferencial:
$$ (2x - y^3 + y \ln y) dy + y dx = 0 $$
Verifique si es exacta. Si no lo es, busque un factor integrante."
"""