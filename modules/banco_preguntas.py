import random

# ==============================================================================
# BANCO DE PREGUNTAS - MATEMÁTICAS III (ECONOMÍA UCAB)
# Versión: 88 Ejercicios (Blindada con Triple Comilla Total)
# ==============================================================================

BANCO_FIXED = [
    # --- CÁLCULO INTEGRAL: MÉTODOS BÁSICOS ---
    {
        "tema": "1.1.1 Integrales Directas",
        "pregunta": r"""Resuelva la siguiente integral con respecto a la variable $x$: $$ \int (3y-2x)^{20} dx $$""",
        "opciones": [
            r"""A) $-\frac{1}{42}(3y-2x)^{21} + C$""",
            r"""B) $\frac{1}{21}(3y-2x)^{21} + C$""",
            r"""C) $\frac{1}{63}(3y-2x)^{21} + C$""",
            r"""D) $20(3y-2x)^{19} + C$"""
        ],
        "respuesta_correcta": r"""A) $-\frac{1}{42}(3y-2x)^{21} + C$""",
        "explicacion": r"""Al integrar respecto a $x$, $3y$ es constante. Usamos sustitución $u = 3y-2x \Rightarrow du = -2dx$. La integral resulta en $-\frac{1}{2} \int u^{20} du$."""
    },
    {
        "tema": "1.1.1 Integrales Directas",
        "pregunta": r"""Resuelva la integral respecto a $y$: $$ \int \frac{e^{3y-2x}}{e^{y+2x}} dy $$""",
        "opciones": [
            r"""A) $\frac{1}{2}e^{2y-4x} + C$""",
            r"""B) $e^{2y-4x} + C$""",
            r"""C) $\frac{1}{2}e^{2y} + C$""",
            r"""D) $2e^{2y-4x} + C$"""
        ],
        "respuesta_correcta": r"""A) $\frac{1}{2}e^{2y-4x} + C$""",
        "explicacion": r"""Simplificamos exponentes: $(3y-2x) - (y+2x) = 2y - 4x$. Integramos $e^{2y-4x}$ respecto a $y$ dividiendo por 2."""
    },
    {
        "tema": "1.1.1 Integrales Directas",
        "pregunta": r"""Resuelva respecto a $t$: $$ \int \sqrt[3]{x^{-2}t^{-3}} dt $$""",
        "opciones": [
            r"""A) $x^{-2/3} \ln|t| + C$""",
            r"""B) $\frac{3}{2} x^{-2/3} t^{2/3} + C$""",
            r"""C) $-3 x^{-2/3} t^{-2} + C$""",
            r"""D) $x^{-2/3} \frac{t^{-2}}{-2} + C$"""
        ],
        "respuesta_correcta": r"""A) $x^{-2/3} \ln|t| + C$""",
        "explicacion": r"""Reescribimos: $x^{-2/3} t^{-1}$. La integral de $1/t$ es $\ln|t|$."""
    },
    {
        "tema": "1.1.1 Integrales Directas",
        "pregunta": r"""Calcule la integral definida: $$ \int_{1}^{2} \frac{x^2-1}{x^2} dx $$""",
        "opciones": [
            r"""A) $0.5$""",
            r"""B) $1.5$""",
            r"""C) $2.0$""",
            r"""D) $\ln(2)$"""
        ],
        "respuesta_correcta": r"""A) $0.5$""",
        "explicacion": r"""Separamos: $1 - x^{-2}$. Integral: $[x + 1/x]_1^2 = (2.5) - (2) = 0.5$."""
    },
    {
        "tema": "1.1.1 Integrales Directas",
        "pregunta": r"""Integral de $(x-2y^2)^2$ respecto a $y$:""",
        "opciones": [
            r"""A) $x^2y - \frac{4}{3}xy^3 + \frac{4}{5}y^5 + C$""",
            r"""B) $\frac{1}{3}(x-2y^2)^3 + C$""",
            r"""C) $- \frac{(x-2y^2)^3}{4y} + C$""",
            r"""D) $2(x-2y^2) + C$"""
        ],
        "respuesta_correcta": r"""A) $x^2y - \frac{4}{3}xy^3 + \frac{4}{5}y^5 + C$""",
        "explicacion": r"""Expandir binomio: $x^2 - 4xy^2 + 4y^4$. Integrar término a término respecto a $y$."""
    },
    # --- SUSTITUCIÓN ---
    {
        "tema": "1.1.2 Cambios de variables (Sustitución)",
        "pregunta": r"""Resuelva: $$ \int \frac{\sqrt{1-4\ln x}}{x} dx $$""",
        "opciones": [
            r"""A) $-\frac{1}{6}(1-4\ln x)^{3/2} + C$""",
            r"""B) $\frac{2}{3}(1-4\ln x)^{3/2} + C$""",
            r"""C) $-\frac{1}{4}\sqrt{1-4\ln x} + C$""",
            r"""D) $\ln|1-4\ln x| + C$"""
        ],
        "respuesta_correcta": r"""A) $-\frac{1}{6}(1-4\ln x)^{3/2} + C$""",
        "explicacion": r"""Sustitución $u = 1-4\ln x \Rightarrow du = -4/x dx$. Integral $-\frac{1}{4}\int u^{1/2} du$."""
    },
    {
        "tema": "1.1.2 Cambios de variables (Sustitución)",
        "pregunta": r"""Teoría: Si $z = f(x)$, la integral $\int g(f(x)) f'(x) dx$ es equivalente a:""",
        "opciones": [
            r"""A) $\int g(z) dz$""",
            r"""B) $\int g(z) f'(z) dz$""",
            r"""C) $\int \frac{g(z)}{f'(x)} dz$""",
            r"""D) Ninguna de las anteriores"""
        ],
        "respuesta_correcta": r"""A) $\int g(z) dz$""",
        "explicacion": r"""Definición directa del diferencial $dz = f'(x)dx$."""
    },
    {
        "tema": "1.1.2 Cambios de variables (Sustitución)",
        "pregunta": r"""Resuelva: $$ \int (1-3x)^{-2} dx $$""",
        "opciones": [
            r"""A) $\frac{1}{3(1-3x)} + C$""",
            r"""B) $-\frac{1}{1-3x} + C$""",
            r"""C) $\frac{3}{1-3x} + C$""",
            r"""D) $\frac{(1-3x)^{-3}}{-3} + C$"""
        ],
        "respuesta_correcta": r"""A) $\frac{1}{3(1-3x)} + C$""",
        "explicacion": r"""$u=1-3x \Rightarrow du=-3dx$. Integral $-\frac{1}{3} \int u^{-2} du = \frac{1}{3}u^{-1}$."""
    },
    {
        "tema": "1.1.2 Cambios de variables (Sustitución)",
        "pregunta": r"""Evalúe: $$ \int \frac{\cos(1-2\ln x)}{x} dx $$""",
        "opciones": [
            r"""A) $-\frac{1}{2}\sin(1-2\ln x) + C$""",
            r"""B) $\sin(1-2\ln x) + C$""",
            r"""C) $-2\sin(1-2\ln x) + C$""",
            r"""D) $\cos(1-2\ln x) + C$"""
        ],
        "respuesta_correcta": r"""A) $-\frac{1}{2}\sin(1-2\ln x) + C$""",
        "explicacion": r"""$u=1-2\ln x \Rightarrow du = -2/x dx$. Integral $-\frac{1}{2}\int \cos u du$."""
    },
    {
        "tema": "1.1.2 Cambios de variables (Sustitución)",
        "pregunta": r"""Resuelva: $$ \int \frac{(1-2\sqrt{x})^3}{\sqrt{x}} dx $$""",
        "opciones": [
            r"""A) $-\frac{1}{4}(1-2\sqrt{x})^4 + C$""",
            r"""B) $\frac{1}{4}(1-2\sqrt{x})^4 + C$""",
            r"""C) $-\frac{1}{2}(1-2\sqrt{x})^4 + C$""",
            r"""D) $4(1-2\sqrt{x})^4 + C$"""
        ],
        "respuesta_correcta": r"""A) $-\frac{1}{4}(1-2\sqrt{x})^4 + C$""",
        "explicacion": r"""$u=1-2\sqrt{x} \Rightarrow du = -1/\sqrt{x} dx$. Integral $-\int u^3 du$."""
    },
    # --- FRACCIONES SIMPLES ---
    {
        "tema": "1.1.4 Fracciones Simples",
        "pregunta": r"""Forma correcta de descomponer $\frac{2x+x^2+2x^3+4}{(x^2+4)(x^2+1)}$:""",
        "opciones": [
            r"""A) $\frac{Ax+B}{x^2+4} + \frac{Cx+D}{x^2+1}$""",
            r"""B) $\frac{A}{x^2+4} + \frac{B}{x^2+1}$""",
            r"""C) $\frac{Ax}{x^2+4} + \frac{Bx}{x^2+1}$""",
            r"""D) $\frac{A}{(x^2+4)^2} + \frac{B}{x^2+1}$"""
        ],
        "respuesta_correcta": r"""A) $\frac{Ax+B}{x^2+4} + \frac{Cx+D}{x^2+1}$""",
        "explicacion": r"""Factores cuadráticos irreducibles requieren numeradores lineales ($Ax+B$)."""
    },
    {
        "tema": "1.1.4 Fracciones Simples",
        "pregunta": r"""Resuelva (división primero): $$ \int \frac{2x+1}{x-4} dx $$""",
        "opciones": [
            r"""A) $2x + 9\ln|x-4| + C$""",
            r"""B) $2x + \ln|x-4| + C$""",
            r"""C) $x^2 + \ln|x-4| + C$""",
            r"""D) $2 + 9(x-4)^{-1} + C$"""
        ],
        "respuesta_correcta": r"""A) $2x + 9\ln|x-4| + C$""",
        "explicacion": r"""División: $2 + 9/(x-4)$. Integral directa."""
    },
    {
        "tema": "1.1.4 Fracciones Simples",
        "pregunta": r"""Calcule: $$ \int \frac{1}{x^2 - 5x + 6} dx $$""",
        "opciones": [
            r"""A) $\ln|x-3| - \ln|x-2| + C$""",
            r"""B) $\ln|x-2| - \ln|x-3| + C$""",
            r"""C) $\ln|(x-3)(x-2)| + C$""",
            r"""D) $\frac{1}{2x-5} + C$"""
        ],
        "respuesta_correcta": r"""A) $\ln|x-3| - \ln|x-2| + C$""",
        "explicacion": r"""Factorización $(x-3)(x-2)$. A/(x-3) + B/(x-2). A=1, B=-1."""
    },
    {
        "tema": "1.1.4 Fracciones Simples",
        "pregunta": r"""Resuelva: $$ \int \left( \frac{2}{x-1} - \frac{4}{x+1} + \frac{2x}{x^2+1} \right) dx $$""",
        "opciones": [
            r"""A) $2\ln|x-1| - 4\ln|x+1| + \ln(x^2+1) + C$""",
            r"""B) $2\ln|x-1| - 4\ln|x+1| + 2\arctan x + C$""",
            r"""C) $\ln \frac{(x-1)^2}{(x+1)^4} + \frac{1}{x^2+1}$""",
            r"""D) $2(x-1)^{-1} + C$"""
        ],
        "respuesta_correcta": r"""A) $2\ln|x-1| - 4\ln|x+1| + \ln(x^2+1) + C$""",
        "explicacion": r"""Integrales logarítmicas directas. El último término tiene la derivada en el numerador."""
    },
    {
        "tema": "1.1.4 Fracciones Simples",
        "pregunta": r"""Descomposición de $\frac{x^2+1}{x(x-1)^2}$:""",
        "opciones": [
            r"""A) $\frac{A}{x} + \frac{B}{x-1} + \frac{C}{(x-1)^2}$""",
            r"""B) $\frac{A}{x} + \frac{Bx+C}{(x-1)^2}$""",
            r"""C) $\frac{A}{x} + \frac{B}{x-1} + \frac{Cx+D}{(x-1)^2}$""",
            r"""D) $\frac{A}{x} + \frac{B}{(x-1)^2}$"""
        ],
        "respuesta_correcta": r"""A) $\frac{A}{x} + \frac{B}{x-1} + \frac{C}{(x-1)^2}$""",
        "explicacion": r"""Factor lineal $x$ y factor lineal repetido $(x-1)^2$."""
    },
    # --- POR PARTES ---
    {
        "tema": "1.1.7 Integral por partes",
        "pregunta": r"""Elección $u, dv$ para $\int x^3 \ln(x^2-4) dx$:""",
        "opciones": [
            r"""A) $u = \ln(x^2-4)$, $dv = x^3 dx$""",
            r"""B) $u = x^3$, $dv = \ln(x^2-4) dx$""",
            r"""C) $u = x^2$, $dv = x \ln(...) dx$""",
            r"""D) $u = 1$, $dv = x^3 \ln(...) dx$"""
        ],
        "respuesta_correcta": r"""A) $u = \ln(x^2-4)$, $dv = x^3 dx$""",
        "explicacion": r"""LIATE: Logarítmica va antes que Algebraica para $u$."""
    },
    {
        "tema": "1.1.7 Integral por partes",
        "pregunta": r"""Resultado de la cíclica $\int e^{-x} \cos x dx$:""",
        "opciones": [
            r"""A) $\frac{e^{-x}}{2}(\sin x - \cos x) + C$""",
            r"""B) $e^{-x}(\sin x + \cos x) + C$""",
            r"""C) $\frac{e^{-x}}{2}(\cos x - \sin x) + C$""",
            r"""D) $-e^{-x}\sin x + C$"""
        ],
        "respuesta_correcta": r"""A) $\frac{e^{-x}}{2}(\sin x - \cos x) + C$""",
        "explicacion": r"""Aplicando partes dos veces y despejando la integral original."""
    },
    {
        "tema": "1.1.7 Integral por partes",
        "pregunta": r"""Resuelva: $$ \int 6x e^{1-2x} dx $$""",
        "opciones": [
            r"""A) $-3xe^{1-2x} - \frac{3}{2}e^{1-2x} + C$""",
            r"""B) $3xe^{1-2x} - 3e^{1-2x} + C$""",
            r"""C) $6xe^{1-2x} - 6e^{1-2x} + C$""",
            r"""D) $3x^2 e^{1-2x} + C$"""
        ],
        "respuesta_correcta": r"""A) $-3xe^{1-2x} - \frac{3}{2}e^{1-2x} + C$""",
        "explicacion": r"""$u=6x, dv=e^{1-2x}dx$. Fórmula $uv - \int v du$."""
    },
    {
        "tema": "1.1.7 Integral por partes",
        "pregunta": r"""Resuelva: $$ \int x \ln x dx $$""",
        "opciones": [
            r"""A) $\frac{x^2}{2}\ln x - \frac{x^2}{4} + C$""",
            r"""B) $\frac{x^2}{2}\ln x - \frac{x^2}{2} + C$""",
            r"""C) $x\ln x - x + C$""",
            r"""D) $\frac{1}{x} + C$"""
        ],
        "respuesta_correcta": r"""A) $\frac{x^2}{2}\ln x - \frac{x^2}{4} + C$""",
        "explicacion": r"""$u=\ln x, dv=x dx \Rightarrow v=x^2/2$. $\int v du = \int x/2 dx = x^2/4$."""
    },
    {
        "tema": "1.1.7 Integral por partes",
        "pregunta": r"""Resuelva: $$ \int \arcsin(x) dx $$""",
        "opciones": [
            r"""A) $x \arcsin x + \sqrt{1-x^2} + C$""",
            r"""B) $x \arcsin x - \sqrt{1-x^2} + C$""",
            r"""C) $\frac{1}{\sqrt{1-x^2}} + C$""",
            r"""D) $\cos(\arcsin x) + C$"""
        ],
        "respuesta_correcta": r"""A) $x \arcsin x + \sqrt{1-x^2} + C$""",
        "explicacion": r"""$u=\arcsin x, dv=dx$. La integral resultante se hace por sustitución $w=1-x^2$."""
    },
    {
        "tema": "1.1.7 Integral por partes",
        "pregunta": r"""Resuelva: $$ \int x^3 e^{-x} dx $$""",
        "opciones": [
            r"""A) $-e^{-x}(x^3 + 3x^2 + 6x + 6) + C$""",
            r"""B) $e^{-x}(x^3 - 3x^2 + 6x - 6) + C$""",
            r"""C) $-x^3 e^{-x} + 3x^2 e^{-x} + C$""",
            r"""D) $-\frac{x^4}{4} e^{-x} + C$"""
        ],
        "respuesta_correcta": r"""A) $-e^{-x}(x^3 + 3x^2 + 6x + 6) + C$""",
        "explicacion": r"""Método tabular. Signos alternados. Derivadas de $x^3$: $3x^2, 6x, 6, 0$."""
    },
    # --- ÁREAS ---
    {
        "tema": "1.2.1 Áreas entre curvas",
        "pregunta": r"""Área entre $y=x^2$ y $y=6-x$:""",
        "opciones": [
            r"""A) $\int_{-3}^{2} (6 - x - x^2) dx$""",
            r"""B) $\int_{-3}^{2} (x^2 - (6-x)) dx$""",
            r"""C) $\int_{0}^{6} (6 - x - x^2) dx$""",
            r"""D) $\int_{-2}^{3} (6 - x - x^2) dx$"""
        ],
        "respuesta_correcta": r"""A) $\int_{-3}^{2} (6 - x - x^2) dx$""",
        "explicacion": r"""Cortes en $x=-3, x=2$. La recta está por encima."""
    },
    {
        "tema": "1.2.1 Áreas entre curvas",
        "pregunta": r"""Integral para área entre $y=4-x^2$ y $y=1+2x$:""",
        "opciones": [
            r"""A) $\int_{-3}^{1} [(4-x^2) - (1+2x)] dx$""",
            r"""B) $\int_{-3}^{1} [(1+2x) - (4-x^2)] dx$""",
            r"""C) $\int_{0}^{4} \dots dx$""",
            r"""D) $\int_{-1}^{3} \dots dx$"""
        ],
        "respuesta_correcta": r"""A) $\int_{-3}^{1} [(4-x^2) - (1+2x)] dx$""",
        "explicacion": r"""Raíces de intersección $x=-3, x=1$. Parábola abre hacia abajo y está arriba."""
    },
    {
        "tema": "1.2.1 Áreas entre curvas",
        "pregunta": r"""Área entre $y=x^2+x$ y $y=15-x^2/3$:""",
        "opciones": [
            r"""A) $\int_{-3.75}^{3} [ (15-x^2/3) - (x^2+x) ] dx$""",
            r"""B) $\int_{-3}^{3} [ (x^2+x) - (15-x^2/3) ] dx$""",
            r"""C) $\int_{0}^{3} \dots dx$""",
            r"""D) $\int_{-4}^{4} \dots dx$"""
        ],
        "respuesta_correcta": r"""A) $\int_{-3.75}^{3} [ (15-x^2/3) - (x^2+x) ] dx$""",
        "explicacion": r"""Igualando funciones se obtienen los límites. La segunda función es una parábola que abre hacia abajo (techo)."""
    },
    {
        "tema": "1.2.1 Áreas entre curvas",
        "pregunta": r"""Área región no acotada entre $y=xe^{-x}$ y $y=e^{-x}$ en $[0, \infty)$:""",
        "opciones": [
            r"""A) $\int_{0}^{1} (e^{-x} - xe^{-x}) dx + \int_{1}^{\infty} (xe^{-x} - e^{-x}) dx$""",
            r"""B) $\int_{0}^{\infty} (xe^{-x} - e^{-x}) dx$""",
            r"""C) $\int_{0}^{\infty} (e^{-x} - xe^{-x}) dx$""",
            r"""D) $\int_{0}^{1} xe^{-x} dx$"""
        ],
        "respuesta_correcta": r"""A) $\int_{0}^{1} (e^{-x} - xe^{-x}) dx + \int_{1}^{\infty} (xe^{-x} - e^{-x}) dx$""",
        "explicacion": r"""Las curvas se cruzan en $x=1$. Hay cambio de posición relativa."""
    },
    {
        "tema": "1.2.1 Áreas entre curvas",
        "pregunta": r"""Calcule área entre $y=e^{-x}$ y $y=-e^{-2x}$ en $[0, \infty)$:""",
        "opciones": [
            r"""A) $1.5$""",
            r"""B) $1.0$""",
            r"""C) $0.5$""",
            r"""D) $2.0$"""
        ],
        "respuesta_correcta": r"""A) $1.5$""",
        "explicacion": r"""No se cruzan. $\int_0^\infty (e^{-x} + e^{-2x}) dx = [ -e^{-x} - 0.5e^{-2x} ]_0^\infty = 0 - (-1.5) = 1.5$."""
    },
    # --- EXCEDENTES ---
    {
        "tema": "1.2.2 Excedentes del consumidor y productor",
        "pregunta": r"""Demanda $D(q) = 14 - q^2/4$, Oferta $O(q) = 2q + 2$. Calcule EC:""",
        "opciones": [
            r"""A) $10.67$""",
            r"""B) $32.00$""",
            r"""C) $50.66$""",
            r"""D) $15.50$"""
        ],
        "respuesta_correcta": r"""A) $10.67$""",
        "explicacion": r"""Equilibrio $q=4, p=10$. $\int_0^4 (14-q^2/4) dq - 40 = 10.67$."""
    },
    {
        "tema": "1.2.2 Excedentes del consumidor y productor",
        "pregunta": r"""Demanda $p = 100 - 2q^2$, Oferta $p = 50 + 3q^2$. Calcule EP:""",
        "opciones": [
            r"""A) $\int_0^{\sqrt{10}} (80 - (50+3q^2)) dq$""",
            r"""B) $\int_0^{10} ((100-2q^2) - 80) dq$""",
            r"""C) $100\sqrt{10}$""",
            r"""D) $\int_0^{\sqrt{10}} (50+3q^2) dq$"""
        ],
        "respuesta_correcta": r"""A) $\int_0^{\sqrt{10}} (80 - (50+3q^2)) dq$""",
        "explicacion": r"""Equilibrio $q=\sqrt{10}, p=80$. EP es el área sobre la oferta y bajo el precio."""
    },
    {
        "tema": "1.2.2 Excedentes del consumidor y productor",
        "pregunta": r"""EC dados Oferta $p = x^2/9 + 4$ y Demanda $p = 11 - 2x$:""",
        "opciones": [
            r"""A) $9$""",
            r"""B) $18$""",
            r"""C) $4.5$""",
            r"""D) $27$"""
        ],
        "respuesta_correcta": r"""A) $9$""",
        "explicacion": r"""Equilibrio $x=3, p=5$. EC = $\int_0^3 (11-2x - 5) dx = 9$."""
    },
    {
        "tema": "1.2.2 Excedentes del consumidor y productor",
        "pregunta": r"""EP dados Oferta $p = x^2/4 + 4$ y Demanda $p = 12 - x$:""",
        "opciones": [
            r"""A) $10.67$""",
            r"""B) $32.00$""",
            r"""C) $8.00$""",
            r"""D) $16.33$"""
        ],
        "respuesta_correcta": r"""A) $10.67$""",
        "explicacion": r"""Equilibrio $x=4, p=8$. EP = $\int_0^4 (8 - (x^2/4+4)) dx = 10.67$."""
    },
    {
        "tema": "1.2.2 Excedentes del consumidor y productor",
        "pregunta": r"""Calcule EP con Oferta $p = 4 + 3x^2$ y Demanda $p = 20 - x^2$:""",
        "opciones": [
            r"""A) $16$""",
            r"""B) $32$""",
            r"""C) $12$""",
            r"""D) $24$"""
        ],
        "respuesta_correcta": r"""A) $16$""",
        "explicacion": r"""Equilibrio $x=2, p=16$. EP = $\int_0^2 (16 - (4+3x^2)) dx = 16$."""
    },
    # --- IMPROPIAS ---
    {
        "tema": "1.2.3 Integrales Impropias",
        "pregunta": r"""Halle $b$ tal que $\int_{b}^{\infty} \frac{dx}{(1+2x)^2} = \frac{1}{4}$""",
        "opciones": [
            r"""A) $b = 1/2$""",
            r"""B) $b = 0$""",
            r"""C) $b = 1$""",
            r"""D) $b = 2$"""
        ],
        "respuesta_correcta": r"""A) $b = 1/2$""",
        "explicacion": r"""Integral da $\frac{1}{2(1+2b)}$. Igualando a 1/4 da $b=1/2$."""
    },
    {
        "tema": "1.2.3 Integrales Impropias",
        "pregunta": r"""Convergencia de $\int_{0}^{\infty} \frac{x^2}{\sqrt{(x^3+4)^3}} dx$:""",
        "opciones": [
            r"""A) Converge a $1/3$""",
            r"""B) Diverge""",
            r"""C) Converge a $2/3$""",
            r"""D) Converge a $0$"""
        ],
        "respuesta_correcta": r"""A) Converge a $1/3$""",
        "explicacion": r"""Sustitución $u=x^3+4$. Límite finito."""
    },
    {
        "tema": "1.2.3 Integrales Impropias",
        "pregunta": r"""Convergencia de $\int_{0}^{\infty} x^2 e^{-x} dx$:""",
        "opciones": [
            r"""A) Converge a 2$""",
            r"""B) Converge a 1$""",
            r"""C) Diverge$""",
            r"""D) Converge a 0$"""
        ],
        "respuesta_correcta": r"""A) Converge a 2$""",
        "explicacion": r"""Es $\Gamma(3) = 2!$."""
    },
    {
        "tema": "1.2.3 Integrales Impropias",
        "pregunta": r"""Halle $k$ para que $f(x) = k x^2(1-x)$ sea PDF en $[0,1]$:""",
        "opciones": [
            r"""A) $k = 12$""",
            r"""B) $k = 6$""",
            r"""C) $k = 1$""",
            r"""D) $k = 1/12$"""
        ],
        "respuesta_correcta": r"""A) $k = 12$""",
        "explicacion": r"""Integral $\int_0^1 k(x^2-x^3)dx = k(1/3-1/4) = k/12 = 1$."""
    },
    {
        "tema": "1.2.3 Integrales Impropias",
        "pregunta": r"""Halle $k$ para que $f(x) = k e^{-x/2}$ sea PDF en $x>0$:""",
        "opciones": [
            r"""A) $k = 0.5$""",
            r"""B) $k = 2$""",
            r"""C) $k = 1$""",
            r"""D) $k = -0.5$"""
        ],
        "respuesta_correcta": r"""A) $k = 0.5$""",
        "explicacion": r"""Integral $\int_0^\infty k e^{-x/2} dx = 2k = 1$."""
    },
    {
        "tema": "1.2.3 Integrales Impropias",
        "pregunta": r"""Evalúe $\int_1^{\infty} x^{-3} dx$:""",
        "opciones": [
            r"""A) $0.5$""",
            r"""B) $1$""",
            r"""C) $0.33$""",
            r"""D) Diverge"""
        ],
        "respuesta_correcta": r"""A) $0.5$""",
        "explicacion": r"""$-1/(2x^2)$ evaluado da $0 - (-0.5) = 0.5$."""
    },
    # --- INTEGRALES DOBLES ---
    {
        "tema": "1.2.4 Integrales Dobles",
        "pregunta": r"""Calcule $\int_{0}^{1}\int_{1}^{2} (3x^2 - 6z) dx dz$ (orden $dx, dz$):""",
        "opciones": [
            r"""A) $-2$""",
            r"""B) $7$""",
            r"""C) $0$""",
            r"""D) $-5$"""
        ],
        "respuesta_correcta": r"""A) $-2$""",
        "explicacion": r"""Integral interna $x^3-6zx|_1^2 = 7-6z$. Integral externa $7z-3z^2|_0^1 = 4$."""
    },
    {
        "tema": "1.2.4 Integrales Dobles",
        "pregunta": r"""Calcule $\int_{0}^{1}\int_{1}^{2} (3x^2 - 6z) dx dz$:""",
        "opciones": [
            r"""A) $4$""",
            r"""B) $7$""",
            r"""C) $0$""",
            r"""D) $-2$"""
        ],
        "respuesta_correcta": r"""A) $4$""",
        "explicacion": r"""Evaluación directa: Interna da $7-6z$. Externa da $4$."""
    },
    {
        "tema": "1.2.4 Integrales Dobles",
        "pregunta": r"""Plantee para región entre parábola $x = y^2 - 4y$ y recta $y = x - 6$:""",
        "opciones": [
            r"""A) $\int_{-1}^{6} \int_{y^2-4y}^{y+6} f(x,y) dx dy$""",
            r"""B) $\int_{-1}^{6} \int_{y+6}^{y^2-4y} f(x,y) dx dy$""",
            r"""C) $\int \dots dy dx$""",
            r"""D) $\int \dots$"""
        ],
        "respuesta_correcta": r"""A) $\int_{-1}^{6} \int_{y^2-4y}^{y+6} f(x,y) dx dy$""",
        "explicacion": r"""Integración tipo II (dx primero). Límites de y $[-1, 6]$."""
    },
    {
        "tema": "1.2.4 Integrales Dobles",
        "pregunta": r"""Cambie orden $\int_0^4 \int_0^x f(x,y) dy dx$:""",
        "opciones": [
            r"""A) $\int_0^4 \int_y^4 f(x,y) dx dy$""",
            r"""B) $\int_0^4 \int_0^y \dots$""",
            r"""C) $\int_0^x \dots$""",
            r"""D) $\int_0^4 \int_4^y \dots$"""
        ],
        "respuesta_correcta": r"""A) $\int_0^4 \int_y^4 f(x,y) dx dy$""",
        "explicacion": r"""Región triangular $0 \le y \le x \le 4$. En orden inverso $y \le x \le 4$."""
    },
    {
        "tema": "1.2.4 Integrales Dobles",
        "pregunta": r"""Calcule $\int_0^1 \int_0^2 (x+y) dy dx$:""",
        "opciones": [
            r"""A) $3$""",
            r"""B) $1$""",
            r"""C) $2$""",
            r"""D) $4$"""
        ],
        "respuesta_correcta": r"""A) $3$""",
        "explicacion": r"""Interna $2x+2$. Externa $1+2=3$."""
    },
    {
        "tema": "1.2.4 Integrales Dobles",
        "pregunta": r"""Volumen bajo $z=1+x-y$ sobre región limitada por $y=x^2$ y $y=8-2x$:""",
        "opciones": [
            r"""A) $\int_{-4}^{2} \int_{x^2}^{8-2x} (1+x-y) dy dx$""",
            r"""B) $\int_{-4}^{2} \int_{8-2x}^{x^2} \dots$""",
            r"""C) $\int \dots dx dy$""",
            r"""D) $\int \dots$"""
        ],
        "respuesta_correcta": r"""A) $\int_{-4}^{2} \int_{x^2}^{8-2x} (1+x-y) dy dx$""",
        "explicacion": r"""Cortes en $x=-4, 2$. Recta por encima de parábola."""
    },
    # --- VOLÚMENES DE REVOLUCIÓN ---
    {
        "tema": "1.2.5 Volúmenes de Revolución",
        "pregunta": r"""Volumen de $f(x)=1+x^2$ entre $x=-1, 5$ girando en $y=-1$:""",
        "opciones": [
            r"""A) $\pi \int_{-1}^{5} (2+x^2)^2 dx$""",
            r"""B) $\pi \int (1+x^2)^2 dx$""",
            r"""C) $2\pi \dots$""",
            r"""D) $\pi \int ((1+x^2)^2-1) dx$"""
        ],
        "respuesta_correcta": r"""A) $\pi \int_{-1}^{5} (2+x^2)^2 dx$""",
        "explicacion": r"""Radio $R = (1+x^2) - (-1) = 2+x^2$. No hay hueco (disco)."""
    },
    {
        "tema": "1.2.5 Volúmenes de Revolución",
        "pregunta": r"""Volumen región $y=x^2-4x$, $y=0$ girando en $y=4$:""",
        "opciones": [
            r"""A) $\pi \int_0^4 [ 4^2 - (4-(x^2-4x))^2 ] dx$""",
            r"""B) $\pi \int [ (x^2-4x)^2 ] dx$""",
            r"""C) $\pi \int [ 4^2 - (4-0)^2 ] dx$""",
            r"""D) $2\pi \dots$"""
        ],
        "respuesta_correcta": r"""A) $\pi \int_0^4 [ 4^2 - (4-(x^2-4x))^2 ] dx$""",
        "explicacion": r"""Arandelas. Radio exterior constante 4 (hasta el eje x). Radio interior hasta la curva."""
    },
    {
        "tema": "1.2.5 Volúmenes de Revolución",
        "pregunta": r"""Volumen región $x=y^2+2, x=1$ girando en $x=-2$:""",
        "opciones": [
            r"""A) $\pi \int_{-2}^{2} [ (y^2+4)^2 - 3^2 ] dy$""",
            r"""B) $\pi \int [ (y^2+2)^2 ] dy$""",
            r"""C) $\pi \int \dots$""",
            r"""D) $\pi \dots$"""
        ],
        "respuesta_correcta": r"""A) $\pi \int_{-2}^{2} [ (y^2+4)^2 - 3^2 ] dy$""",
        "explicacion": r"""Radio mayor $R=(y^2+2)-(-2)$. Radio menor $r=1-(-2)$."""
    },
    {
        "tema": "1.2.5 Volúmenes de Revolución",
        "pregunta": r"""Volumen región $y=2+x^2, y=6$ girando en $y=1$:""",
        "opciones": [
            r"""A) $\pi \int_{-2}^{2} [ (6-1)^2 - (2+x^2-1)^2 ] dx$""",
            r"""B) $\pi \int \dots$""",
            r"""C) $\pi \dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $\pi \int_{-2}^{2} [ (6-1)^2 - (2+x^2-1)^2 ] dx$""",
        "explicacion": r"""Radio mayor constante $5$. Radio menor variable $1+x^2$."""
    },
    {
        "tema": "1.2.5 Volúmenes de Revolución",
        "pregunta": r"""Volumen región $y=4-x^2, y=3$ girando en $y=2$:""",
        "opciones": [
            r"""A) $\pi \int_{0}^{1} [ (4-x^2-2)^2 - (3-2)^2 ] dx$""",
            r"""B) $\pi \int \dots$""",
            r"""C) $\pi \dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $\pi \int_{0}^{1} [ (4-x^2-2)^2 - (3-2)^2 ] dx$""",
        "explicacion": r"""Radio mayor $(4-x^2)-2$. Radio menor $3-2=1$."""
    },
    # --- ECUACIONES DIFERENCIALES: SEPARABLES ---
    {
        "tema": "2.1.1 ED 1er Orden: Separación de Variables",
        "pregunta": r"""Población $dp/dt = 10(100-p)^2$. Integral separada:""",
        "opciones": [
            r"""A) $\int (100-p)^{-2} dp = \int 10 dt$""",
            r"""B) $\int (100-p)^2 dp = \dots$""",
            r"""C) $\int \dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $\int (100-p)^{-2} dp = \int 10 dt$""",
        "explicacion": r"""Pasar término $p$ dividiendo."""
    },
    {
        "tema": "2.1.1 ED 1er Orden: Separación de Variables",
        "pregunta": r"""Separar $\sqrt{xy} y' = \frac{x+2}{2-y}$:""",
        "opciones": [
            r"""A) $\int (2-y)\sqrt{y} dy = \int \frac{x+2}{\sqrt{x}} dx$""",
            r"""B) $\int \frac{\sqrt{y}}{2-y} dy = \dots$""",
            r"""C) $\int \dots$""",
            r"""D) $\int \dots$"""
        ],
        "respuesta_correcta": r"""A) $\int (2-y)\sqrt{y} dy = \int \frac{x+2}{\sqrt{x}} dx$""",
        "explicacion": r"""Agrupar y con dy, x con dx."""
    },
    {
        "tema": "2.1.1 ED 1er Orden: Separación de Variables",
        "pregunta": r"""Solución de $(2-y)\sqrt{xy} dy + (x+2) dx = 0$:""",
        "opciones": [
            r"""A) $\frac{4}{3}y^{3/2} - \frac{2}{5}y^{5/2} = -(\frac{2}{3}x^{3/2} + 4x^{1/2}) + C$""",
            r"""B) $2y^{1/2} \dots$""",
            r"""C) $\ln|2-y| \dots$""",
            r"""D) $y(2-y)^2 \dots$"""
        ],
        "respuesta_correcta": r"""A) $\frac{4}{3}y^{3/2} - \frac{2}{5}y^{5/2} = -(\frac{2}{3}x^{3/2} + 4x^{1/2}) + C$""",
        "explicacion": r"""Integración de potencias fraccionarias tras separar."""
    },
    {
        "tema": "2.1.1 ED 1er Orden: Separación de Variables",
        "pregunta": r"""Resuelva $\frac{dy}{dx} = \frac{(x-1)(y+3)}{(x+4)(y-2)}$:""",
        "opciones": [
            r"""A) $y - 5\ln|y+3| = x - 5\ln|x+4| + C$""",
            r"""B) $y + 5\ln \dots$""",
            r"""C) $(y-2)^2 \dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $y - 5\ln|y+3| = x - 5\ln|x+4| + C$""",
        "explicacion": r"""División de polinomios $(y-2)/(y+3) = 1 - 5/(y+3)$."""
    },
    # --- HOMOGÉNEAS ---
    {
        "tema": "2.1.2 ED 1er Orden: Homogéneas",
        "pregunta": r"""Tipo de ecuación $(x^2 - 2y^2)dx + y dy = 0$:""",
        "opciones": [
            r"""A) Homogénea de grado 2""",
            r"""B) Exacta""",
            r"""C) Lineal""",
            r"""D) Separable"""
        ],
        "respuesta_correcta": r"""A) Homogénea de grado 2""",
        "explicacion": r"""Todos los términos son grado 2."""
    },
    {
        "tema": "2.1.2 ED 1er Orden: Homogéneas",
        "pregunta": r"""Clasificación $(x+y)dx - y dy = 0$:""",
        "opciones": [
            r"""A) Homogénea de grado 1""",
            r"""B) Exacta""",
            r"""C) Separable""",
            r"""D) Lineal"""
        ],
        "respuesta_correcta": r"""A) Homogénea de grado 1""",
        "explicacion": r"""Grado 1 en coeficientes."""
    },
    {
        "tema": "2.1.2 ED 1er Orden: Homogéneas",
        "pregunta": r"""Familia de $(x+y)dx + (x-y)dy = 0$:""",
        "opciones": [
            r"""A) Homogénea""",
            r"""B) Separable""",
            r"""C) Lineal""",
            r"""D) Bernoulli"""
        ],
        "respuesta_correcta": r"""A) Homogénea""",
        "explicacion": r"""Coeficientes del mismo grado."""
    },
    {
        "tema": "2.1.2 ED 1er Orden: Homogéneas",
        "pregunta": r"""Sustitución para $(x-3y)dx + 2y dy = 0$:""",
        "opciones": [
            r"""A) $y = ux$""",
            r"""B) $u = x-3y$""",
            r"""C) $x = y^2$""",
            r"""D) $\mu = e^{2y}$"""
        ],
        "respuesta_correcta": r"""A) $y = ux$""",
        "explicacion": r"""Estándar para homogéneas."""
    },
    {
        "tema": "2.1.2 ED 1er Orden: Homogéneas",
        "pregunta": r"""Factor integrante para $y' + y = e^{3x}$ (Lineal básica):""",
        "opciones": [
            r"""A) $e^x$""",
            r"""B) $e^{-x}$""",
            r"""C) $x$""",
            r"""D) $e^{3x}$"""
        ],
        "respuesta_correcta": r"""A) $e^x$""",
        "explicacion": r"""P(x)=1, integral dx es x."""
    },
    # --- EXACTAS ---
    {
        "tema": "2.1.3 ED 1er Orden: Exactas",
        "pregunta": r"""Clasificación $(x^2-y^2)dx + (y^2-xy)dy = 0$:""",
        "opciones": [
            r"""A) Homogénea de grado 2""",
            r"""B) Exacta""",
            r"""C) Lineal""",
            r"""D) Separable"""
        ],
        "respuesta_correcta": r"""A) Homogénea de grado 2""",
        "explicacion": r"""No cumple condición de exactitud $M_y = N_x$ directametne (-2y vs -y)."""
    },
    {
        "tema": "2.1.3 ED 1er Orden: Exactas",
        "pregunta": r"""Valor de $k$ para que sea exacta $(y^3 + kxy^4 - 2x)dx + (3xy^2 + 20x^2y^3)dy = 0$:""",
        "opciones": [
            r"""A) $k = 10$""",
            r"""B) $k = 5$""",
            r"""C) $k = 20$""",
            r"""D) $k = 4$"""
        ],
        "respuesta_correcta": r"""A) $k = 10$""",
        "explicacion": r"""$M_y = 3y^2 + 4ky^3x$. $N_x = 3y^2 + 40xy^3$. $4k=40 \Rightarrow k=10$."""
    },
    {
        "tema": "2.1.3 ED 1er Orden: Exactas",
        "pregunta": r"""Resuelva exacta: $(\cos y - y\sin x + 1)dx + (\cos x - x\sin y - 2)dy = 0$""",
        "opciones": [
            r"""A) $x\cos y + y\cos x + x - 2y = C$""",
            r"""B) $\sin y \cos x \dots$""",
            r"""C) $\dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $x\cos y + y\cos x + x - 2y = C$""",
        "explicacion": r"""Integración parcial y comparación."""
    },
    {
        "tema": "2.1.3 ED 1er Orden: Exactas",
        "pregunta": r"""Resuelva: $(\frac{1}{y} - 2x + \ln^2 y + \dots)dx + \dots = 0$""",
        "opciones": [
            r"""A) $\frac{x}{y} - x^2 + x \ln^2 y + y \ln^2 x + y^3 = C$""",
            r"""B) $\dots$""",
            r"""C) $\dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $\frac{x}{y} - x^2 + x \ln^2 y + y \ln^2 x + y^3 = C$""",
        "explicacion": r"""Reconstrucción de función potencial."""
    },
    {
        "tema": "2.1.3 ED 1er Orden: Exactas",
        "pregunta": r"""Resuelva: $(2x \cos y + 3x^2 y) dx + (x^3 - x^2 \sin y - y) dy = 0$""",
        "opciones": [
            r"""A) $x^2 \cos y + x^3 y - \frac{y^2}{2} = C$""",
            r"""B) $\dots$""",
            r"""C) $\dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $x^2 \cos y + x^3 y - \frac{y^2}{2} = C$""",
        "explicacion": r"""Término $-y$ en N se integra a $-y^2/2$."""
    },
    # --- LINEALES ---
    {
        "tema": "2.1.4 ED 1er Orden: Lineales",
        "pregunta": r"""Factor integrante para $y' + \frac{3}{x}y = x^2 + 1$:""",
        "opciones": [
            r"""A) $\mu(x) = x^3$""",
            r"""B) $e^{3x}$""",
            r"""C) $3 \ln x$""",
            r"""D) $x^{-3}$"""
        ],
        "respuesta_correcta": r"""A) $\mu(x) = x^3$""",
        "explicacion": r"""$e^{3 \ln x} = x^3$."""
    },
    {
        "tema": "2.1.4 ED 1er Orden: Lineales",
        "pregunta": r"""Clasificación de $(x-3y)dx + 2y dy = 0$ vista como $x(y)$:""",
        "opciones": [
            r"""A) Lineal en $x$""",
            r"""B) Bernoulli""",
            r"""C) Separable""",
            r"""D) Exacta"""
        ],
        "respuesta_correcta": r"""A) Lineal en $x$""",
        "explicacion": r"""Se puede escribir como $dx/dy + P(y)x = Q(y)$."""
    },
    {
        "tema": "2.1.4 ED 1er Orden: Lineales",
        "pregunta": r"""Solución general $x y' + 2y = x^3 - x\ln x$:""",
        "opciones": [
            r"""A) $y = \frac{x^3}{5} - \frac{x}{3}\ln x + \frac{x}{9} + \frac{C}{x^2}$""",
            r"""B) $\dots$""",
            r"""C) $\dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $y = \frac{x^3}{5} - \frac{x}{3}\ln x + \frac{x}{9} + \frac{C}{x^2}$""",
        "explicacion": r"""$\mu = x^2$."""
    },
    {
        "tema": "2.1.4 ED 1er Orden: Lineales",
        "pregunta": r"""Solución $y' - \frac{2}{x}y = x^2 \sin x$:""",
        "opciones": [
            r"""A) $y = -x^2 \cos x + C x^2$""",
            r"""B) $\dots$""",
            r"""C) $\dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $y = -x^2 \cos x + C x^2$""",
        "explicacion": r"""$\mu = x^{-2}$."""
    },
    {
        "tema": "2.1.4 ED 1er Orden: Lineales",
        "pregunta": r"""Resuelva $y' + y \tan x = \sec x$:""",
        "opciones": [
            r"""A) $y = \sin x + C \cos x$""",
            r"""B) $\dots$""",
            r"""C) $\dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $y = \sin x + C \cos x$""",
        "explicacion": r"""$\mu = \sec x$."""
    },
    # --- BERNOULLI ---
    {
        "tema": "2.1.5 ED 1er Orden: Bernoulli",
        "pregunta": r"""Bernoulli $x dy + (x^2 y^3 + xy^3 - 2y) dx = 0$. Solución:""",
        "opciones": [
            r"""A) $y^{-2} = \frac{1}{3}x^2 + \frac{2}{5}x + Cx^{-4}$""",
            r"""B) $\dots$""",
            r"""C) $\dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $y^{-2} = \frac{1}{3}x^2 + \frac{2}{5}x + Cx^{-4}$""",
        "explicacion": r"""$n=3$. Sustitución $u=y^{-2}$."""
    },
    {
        "tema": "2.1.5 ED 1er Orden: Bernoulli",
        "pregunta": r"""Bernoulli $xy dy + (2y^2 - x^3 + x\ln x) dx = 0$. Solución:""",
        "opciones": [
            r"""A) $y^2 = \frac{1}{3}x^2 - \frac{1}{2}\ln x + \frac{1}{8} + Cx^{-4}$""",
            r"""B) $\dots$""",
            r"""C) $\dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $y^2 = \frac{1}{3}x^2 - \frac{1}{2}\ln x + \frac{1}{8} + Cx^{-4}$""",
        "explicacion": r"""$n=-1$ para $y(x)$. Sustitución $u=y^2$."""
    },
    {
        "tema": "2.1.5 ED 1er Orden: Bernoulli",
        "pregunta": r"""Bernoulli $y' + \frac{1}{x}y = x y^2$:""",
        "opciones": [
            r"""A) $\frac{1}{y} = Cx - x^2$""",
            r"""B) $\dots$""",
            r"""C) $\dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $\frac{1}{y} = Cx - x^2$""",
        "explicacion": r"""$n=2$. $u=y^{-1}$."""
    },
    {
        "tema": "2.1.5 ED 1er Orden: Bernoulli",
        "pregunta": r"""Bernoulli $y' + \frac{1}{x}y = y^3$:""",
        "opciones": [
            r"""A) $y^{-2} = 2x + C x^2$""",
            r"""B) $\dots$""",
            r"""C) $\dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $y^{-2} = 2x + C x^2$""",
        "explicacion": r"""$n=3$. $u=y^{-2}$."""
    },
    {
        "tema": "2.1.5 ED 1er Orden: Bernoulli",
        "pregunta": r"""Bernoulli $y' - \frac{4}{x}y = x \sqrt{y}$:""",
        "opciones": [
            r"""A) $\sqrt{y} = \frac{1}{2}x^2 \ln x + C x^2$""",
            r"""B) $\dots$""",
            r"""C) $\dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $\sqrt{y} = \frac{1}{2}x^2 \ln x + C x^2$""",
        "explicacion": r"""$n=1/2$. $u=\sqrt{y}$."""
    },
    # --- ORDEN SUPERIOR ---
    {
        "tema": "2.2.1 ED Orden Superior: Homogéneas",
        "pregunta": r"""Primer paso para $y^{IV} - y^{V} + \dots = 0$:""",
        "opciones": [
            r"""A) Hallar las raíces del polinomio característico.""",
            r"""B) Integrar""",
            r"""C) Variación de parámetros""",
            r"""D) Factor integrante"""
        ],
        "respuesta_correcta": r"""A) Hallar las raíces del polinomio característico.""",
        "explicacion": r"""Método estándar para coeficientes constantes."""
    },
    {
        "tema": "2.2.1 ED Orden Superior: Homogéneas",
        "pregunta": r"""Solución general $y''' + 2y'' - 3y' = 0$:""",
        "opciones": [
            r"""A) $y = C_1 + C_2 e^{-3x} + C_3 e^{x}$""",
            r"""B) $\dots$""",
            r"""C) $\dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $y = C_1 + C_2 e^{-3x} + C_3 e^{x}$""",
        "explicacion": r"""Raíces $0, -3, 1$."""
    },
    {
        "tema": "2.2.1 ED Orden Superior: Homogéneas",
        "pregunta": r"""Solución general $y''' + 6y'' + 12y' + 8y = 0$:""",
        "opciones": [
            r"""A) $y = C_1 e^{-2x} + C_2 x e^{-2x} + C_3 x^2 e^{-2x}$""",
            r"""B) $\dots$""",
            r"""C) $\dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $y = C_1 e^{-2x} + C_2 x e^{-2x} + C_3 x^2 e^{-2x}$""",
        "explicacion": r"""Raíz $-2$ con multiplicidad 3."""
    },
    {
        "tema": "2.2.1 ED Orden Superior: Homogéneas",
        "pregunta": r"""Solución particular $y_p$ de $y'' + 4y' + 3y = 12e^x$:""",
        "opciones": [
            r"""A) $y_p = \frac{3}{2}e^x$""",
            r"""B) $12e^x$""",
            r"""C) $\dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $y_p = \frac{3}{2}e^x$""",
        "explicacion": r"""Coeficientes indeterminados."""
    },
    {
        "tema": "2.2.1 ED Orden Superior: Homogéneas",
        "pregunta": r"""Característica de $y^{(4)} - 16y = 0$:""",
        "opciones": [
            r"""A) $r^4 - 16 = 0$""",
            r"""B) $4r-16=0$""",
            r"""C) $\dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $r^4 - 16 = 0$""",
        "explicacion": r"""Sustitución directa."""
    },
    # --- APLICACIONES ---
    {
        "tema": "2.3 Aplicaciones de Ecuaciones Diferenciales en Economía",
        "pregunta": r"""Modelo $\frac{dp}{dt} = kp(1000-p)$:""",
        "opciones": [
            r"""A) Crecimiento Logístico""",
            r"""B) Malthus""",
            r"""C) Newton""",
            r"""D) Desintegración"""
        ],
        "respuesta_correcta": r"""A) Crecimiento Logístico""",
        "explicacion": r"""Ecuación verhulst."""
    },
    {
        "tema": "2.3 Aplicaciones de Ecuaciones Diferenciales en Economía",
        "pregunta": r"""Límite de $\frac{dp}{dt} = kp(200-p)$:""",
        "opciones": [
            r"""A) 200 unidades""",
            r"""B) 0""",
            r"""C) Infinito""",
            r"""D) 200k"""
        ],
        "respuesta_correcta": r"""A) 200 unidades""",
        "explicacion": r"""Capacidad de carga."""
    },
    {
        "tema": "2.3 Aplicaciones de Ecuaciones Diferenciales en Economía",
        "pregunta": r"""Ley Enfriamiento: $100 \to 80$ en 10 min ($T_a=25$). Temp a los 20 min:""",
        "opciones": [
            r"""A) $65.33^{\circ}C$""",
            r"""B) $60$""",
            r"""C) $70$""",
            r"""D) $55$"""
        ],
        "respuesta_correcta": r"""A) $65.33^{\circ}C$""",
        "explicacion": r"""Cálculo exponencial iterativo."""
    },
    {
        "tema": "2.3 Aplicaciones de Ecuaciones Diferenciales en Economía",
        "pregunta": r"""Límite $\frac{dp}{dt} = kt(1000 - p/2)$:""",
        "opciones": [
            r"""A) $2000$ unidades""",
            r"""B) $1000$""",
            r"""C) $500$""",
            r"""D) $\infty$"""
        ],
        "respuesta_correcta": r"""A) $2000$ unidades""",
        "explicacion": r"""Equilibrio cuando derivada es 0."""
    },
    {
        "tema": "2.3 Aplicaciones de Ecuaciones Diferenciales en Economía",
        "pregunta": r"""Carbono-14, 1/6 remanente. Vida media 5600. Ecuación:""",
        "opciones": [
            r"""A) $\frac{1}{6} = e^{k t}$ con $k = \frac{\ln(0.5)}{5600}$""",
            r"""B) $\dots$""",
            r"""C) $\dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $\frac{1}{6} = e^{k t}$ con $k = \frac{\ln(0.5)}{5600}$""",
        "explicacion": r"""Decaimiento radioactivo."""
    },
    {
        "tema": "2.3 Aplicaciones de Ecuaciones Diferenciales en Economía",
        "pregunta": r"""Solución general enfriamiento $T(t)$:""",
        "opciones": [
            r"""A) $T(t) = T_a + (T_0 - T_a)e^{kt}$""",
            r"""B) $\dots$""",
            r"""C) $\dots$""",
            r"""D) $\dots$"""
        ],
        "respuesta_correcta": r"""A) $T(t) = T_a + (T_0 - T_a)e^{kt}$""",
        "explicacion": r"""Solución analítica estándar."""
    },
    # --------------------------------------------------------------------------
    # AMPLIACIÓN: ED ORDEN SUPERIOR NO HOMOGÉNEAS (Meta: 5 ejercicios)
    # Fuente: Taller 2 - 202525
    # --------------------------------------------------------------------------
    {
        "tema": "2.2.2 ED Orden Superior: No Homogéneas",
        "pregunta": r"""Dada la ecuación $y'' - 2y' - 3y = 4e^{3x}$, ¿cuál es la forma correcta de la solución particular $y_p$ a proponer?""",
        "opciones": [
            r"""A) $y_p = Ax e^{3x}$""",
            r"""B) $y_p = A e^{3x}$""",
            r"""C) $y_p = A x^2 e^{3x}$""",
            r"""D) $y_p = (Ax+B) e^{3x}$"""
        ],
        "respuesta_correcta": r"""A) $y_p = Ax e^{3x}$""",
        "explicacion": r"""La solución homogénea tiene raíces $r=3, r=-1$, por lo que $y_h = c_1 e^{3x} + c_2 e^{-x}$. Como el término $e^{3x}$ ya está en la homogénea (resonancia), multiplicamos la propuesta por $x$."""
    },
    {
        "tema": "2.2.2 ED Orden Superior: No Homogéneas",
        "pregunta": r"""Encuentre la solución particular de $y'' + y = x^2 + 1$ usando coeficientes indeterminados:""",
        "opciones": [
            r"""A) $y_p = x^2 - 1$""",
            r"""B) $y_p = x^2 + 1$""",
            r"""C) $y_p = Ax^2 + Bx + C$""",
            r"""D) $y_p = x^2 - 2$"""
        ],
        "respuesta_correcta": r"""A) $y_p = x^2 - 1$""",
        "explicacion": r"""Proponemos $y_p = Ax^2 + Bx + C$. Derivando: $y_p'' = 2A$. Sustituyendo: $2A + (Ax^2 + Bx + C) = x^2 + 1$. Igualando coeficientes: $A=1, B=0, 2A+C=1 \Rightarrow C=-1$."""
    },
    {
        "tema": "2.2.2 ED Orden Superior: No Homogéneas",
        "pregunta": r"""Resuelva la ecuación $y''' - y'' = 12x$ (Solo la parte particular $y_p$):""",
        "opciones": [
            r"""A) $y_p = -2x^3 - 6x^2$""",
            r"""B) $y_p = Ax + B$""",
            r"""C) $y_p = -6x^2$""",
            r"""D) $y_p = x^3$"""
        ],
        "respuesta_correcta": r"""A) $y_p = -2x^3 - 6x^2$""",
        "explicacion": r"""Raíces homogénea: $r^2(r-1)=0 \Rightarrow 0, 0, 1$. Como 0 es raíz doble, la propuesta para $12x$ (polinomio grado 1) debe multiplicarse por $x^2$. $y_p = x^2(Ax+B) = Ax^3 + Bx^2$."""
    },
    {
        "tema": "2.2.2 ED Orden Superior: No Homogéneas",
        "pregunta": r"""Seleccione la solución general de $y'' + 4y = 8$:""",
        "opciones": [
            r"""A) $y = c_1 \cos 2x + c_2 \sin 2x + 2$""",
            r"""B) $y = c_1 e^{2x} + c_2 e^{-2x} + 2$""",
            r"""C) $y = c_1 \cos 2x + c_2 \sin 2x + 4$""",
            r"""D) $y = \cos 2x + \sin 2x + 8$"""
        ],
        "respuesta_correcta": r"""A) $y = c_1 \cos 2x + c_2 \sin 2x + 2$""",
        "explicacion": r"""Homogénea: $r^2+4=0 \Rightarrow r=\pm 2i$. Particular para constante 8: $y_p=A$. Sustitución $4A=8 \Rightarrow A=2$. Suma: $y_h + y_p$."""
    },
    {
        "tema": "2.2.2 ED Orden Superior: No Homogéneas",
        "pregunta": r"""¿Cuál es la forma de $y_p$ para $y'' + 2y' + 5y = 12e^x - x^2$?""",
        "opciones": [
            r"""A) $y_p = A e^x + (Bx^2 + Cx + D)$""",
            r"""B) $y_p = A e^x - x^2$""",
            r"""C) $y_p = A x e^x + B x^2$""",
            r"""D) $y_p = (Ax+B) e^x + C x^2$"""
        ],
        "respuesta_correcta": r"""A) $y_p = A e^x + (Bx^2 + Cx + D)$""",
        "explicacion": r"""Principio de superposición. Para $12e^x$ proponemos $Ae^x$. Para $-x^2$ proponemos polinomio completo grado 2 ($Bx^2+Cx+D$). No hay conflicto con la homogénea ($r = -1 \pm 2i$)."""
    }
]

def obtener_preguntas_fijas(temas_solicitados, cantidad):
    candidatas = [p for p in BANCO_FIXED if any(t in p["tema"] for t in temas_solicitados)]
    if not candidatas:
        return []
    num_a_seleccionar = min(len(candidatas), cantidad)
    return random.sample(candidatas, num_a_seleccionar)