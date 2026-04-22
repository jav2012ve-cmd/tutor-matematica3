from __future__ import annotations
from datetime import datetime
import json
import os
import re
import sys
import time
from typing import Any, List, Optional, Union

import streamlit as st
from PIL import Image
from pypdf import PdfReader

# Asegura que la carpeta `modules/` esté en `sys.path` aunque Streamlit Cloud
# ejecute desde una ubicación distinta (o "App location" no sea la raíz del repo).
HERE = os.path.abspath(os.path.dirname(__file__))
modules_parent = None
for candidate in [HERE] + [os.path.abspath(os.path.join(HERE, os.pardir))] + [
    os.path.abspath(os.path.join(HERE, os.pardir, os.pardir))
]:
    if os.path.isdir(os.path.join(candidate, "modules")):
        modules_parent = candidate
        break

if modules_parent and modules_parent not in sys.path:
    sys.path.insert(0, modules_parent)

from modules import (
    ia_core,
    interfaz,
    temario,
    banco_preguntas,
    banco_muestras,
    uso_stats,
    registro_interacciones,
    graficos_entrenamiento,
)

# --- CONFIGURACIÓN CENTRALIZADA ---
NUM_EJERCICIOS_ENTRENAMIENTO = 5
NUM_PREGUNTAS_QUIZ = 5
INTENTOS_MAX_IA = 3
MULTIPLICADOR_ESPERA_429 = 4  # segundos por intento ante error 429
MAX_MENSAJES_HISTORIAL_TUTOR = 10  # últimos N mensajes para contexto IA
AVISO_HISTORIAL_LARGO = 20  # si hay más mensajes, mostrar aviso
ADMIN_EMAIL_PERMITIDO = os.environ.get("ADMIN_EMAIL", "jsalas@ucab.edu.ve").strip().lower()
ADMIN_CLAVE_PERMITIDA = os.environ.get("ADMIN_PASSWORD", "J-2002-MateIII")

# --- 1. CONFIGURACIÓN INICIAL ---
interfaz.configurar_pagina()
interfaz.inyectar_estilo_matematico()

if not ia_core.configurar_gemini():
    st.stop()

model, nombre_modelo = ia_core.iniciar_modelo()

# =======================================================
# FUNCIONES DE SEGURIDAD Y UTILIDADES
# =======================================================

def generar_contenido_seguro(
    prompt_parts: Union[str, list],
    intentos_max: Optional[int] = None,
) -> Optional[Any]:
    """
    Intenta llamar a la IA con texto o imágenes.
    Soporta lista de partes (prompt + imagen) o solo texto.
    """
    if intentos_max is None:
        intentos_max = INTENTOS_MAX_IA
    texto_pregunta = registro_interacciones.serializar_pregunta(prompt_parts)
    modelo_log = nombre_modelo or ""
    errores_recientes = ""
    for i in range(intentos_max):
        try:
            response = model.generate_content(prompt_parts)
            texto_respuesta = registro_interacciones.extraer_texto_respuesta(response)
            registro_interacciones.registrar_interaccion(
                texto_pregunta, texto_respuesta, modelo_log
            )
            return response
        except Exception as e:
            errores_recientes = str(e)
            if "429" in str(e):
                tiempo_espera = MULTIPLICADOR_ESPERA_429 * (i + 1)
                st.toast(f"🚦 Tráfico alto. Reintentando en {tiempo_espera}s...", icon="⏳")
                time.sleep(tiempo_espera)
            else:
                time.sleep(1)

    st.error(f"❌ Error de conexión: {errores_recientes}")
    registro_interacciones.registrar_interaccion(
        texto_pregunta,
        f"(sin respuesta tras reintentos) {errores_recientes}",
        modelo_log,
    )
    return None

def _parece_formula(contenido: str) -> bool:
    """True si el contenido entre backticks parece una fórmula (no texto largo)."""
    c = contenido.strip()
    if not c or len(c) > 80:
        return False
    # Exponente, LaTeX, fracción numérica, variable sola, dx/dt
    if re.search(r"\^|\\\\|\\frac|\\sqrt|\\int|\\cdot", c):
        return True
    if re.match(r"^\d+/\d+$", c):
        return True
    if re.match(r"^[a-zA-Z]$", c) or c in ("dx", "dt"):
        return True
    if re.search(r"[a-zA-Z]\^\d|[a-zA-Z]\^\{", c):
        return True
    return False


def preparar_latex_para_streamlit(texto: Optional[str]) -> str:
    if not texto:
        return ""

    # 1. Normalización de escapes de barra invertida de la IA
    t = str(texto).replace('\\\\', '\\').replace(r'\$', '$')

    # 2. Unificación: Si hay fragmentos pegados tipo "$ \int $ $ x $", los une en "$ \int x $"
    t = re.sub(r'\$\s*\$', ' ', t)

    # 3. PROTECCIÓN: Si el texto ya tiene bloques delimitados, no los tocamos.
    # Pero si detectamos comandos LaTeX fuera de $, envolvemos la frase matemática completa.

    # Expresión regular para detectar una fórmula completa (incluyendo paréntesis y potencias)
    # (reservada para extensiones; el envoltorio de integrales usa el bloque siguiente)
    patron_formula_completa = (
        r'(\\int|\\frac|\\sqrt|\\alpha|\\beta|[\w\d\s\+\-\*\/\^\(\)]+?)(?=\s|$|\.|\,)'
    )

    # Bloque integral completo (grupo), no token a token (DOTALL: \int en línea siguiente al texto)
    if ("\\int" in t or "\\frac" in t) and "$" not in t:
        t = re.sub(
            r'(\\int.*?(?:dx|dy|dt|dz))',
            r' $\1$ ',
            t,
            flags=re.DOTALL,
        )

    # Opciones de quiz / fórmulas cortas con \frac, \ln, etc. sin delimitadores.
    # IMPORTANTE: evitar envolver frases mixtas (texto + fórmula), porque
    # terminan renderizadas como "todo matemático" y se pierde legibilidad.
    if "$" not in t and len(t.strip()) <= 280 and re.search(
        r'\\(?:frac|sqrt|ln|int|sum|cdot|left|right|infty|partial|alpha|beta|gamma|delta|theta|pi)\b',
        t,
    ):
        texto_sin_cmd = re.sub(r"\\[a-zA-Z]+", " ", t)
        texto_sin_cmd = re.sub(r"[{}[\]().,;:!?=+\-*/^_|$0-9]", " ", texto_sin_cmd)
        palabras_normales = re.findall(r"[A-Za-zÁÉÍÓÚáéíóúÑñ]{3,}", texto_sin_cmd)
        es_texto_mixto = len(palabras_normales) >= 3
        if not es_texto_mixto:
            t = f"${t.strip()}$"

    return t


def latex_display_puro(texto: Optional[str]) -> str:
    """
    Para campos que la IA devuelve como LaTeX puro (sin texto natural):
    paso_intermedio, resultado_final, enunciado_latex. Quita cualquier $
    residual y envuelve en $$...$$ para display math (estilo VVappy).
    Evita delimitadores rotos o dobles.
    """
    if not texto:
        return ""
    s = str(texto).replace("$", "").strip()
    if not s:
        return ""
    return f"$${s}$$"

def _limpiar_para_st_latex(texto: Any) -> str:
    """
    Streamlit `st.latex()` espera una expresión LaTeX sin delimitadores ($$ o $).
    Si la IA devolvió $...$ o $$...$$, los removemos.
    """
    s = str(texto).strip()
    if s.startswith("$$") and s.endswith("$$"):
        return s[2:-2].strip()
    if s.startswith("$") and s.endswith("$"):
        return s[1:-1].strip()
    if s.startswith("$"):
        s = s[1:].strip()
    if s.endswith("$"):
        s = s[:-1].strip()
    return s

def _render_texto_con_latex(texto: Optional[str]) -> None:
    """
    Renderiza texto mixto separando por delimitadores $...$ / $$...$$.
    - Texto: `st.markdown`
    - Fórmulas: `st.latex` (sin $ / $$)

    Esto reduce fallos cuando el markdown recibe delimitadores rotos o
    cuando hay un '$' molesto en el texto natural.
    """
    if not texto:
        return

    s = preparar_latex_para_streamlit(texto)
    s = str(s)

    # Si hay un '$' suelto al final, lo quitamos (caso típico del enunciado).
    if s.count("$") % 2 != 0:
        s = re.sub(r'\$\s*$', '', s).strip()

    i = 0
    n = len(s)
    while i < n:
        if s.startswith("$$", i):
            j = s.find("$$", i + 2)
            if j == -1:
                st.markdown(s[i:])
                break
            expr = s[i + 2 : j].strip()
            if expr:
                st.latex(expr)
            i = j + 2
            continue

        if s[i] == "$":
            j = s.find("$", i + 1)
            if j == -1:
                st.markdown(s[i:])
                break
            expr = s[i + 1 : j].strip()
            if expr:
                st.latex(expr)
            i = j + 1
            continue

        # Captura texto hasta el siguiente '$'
        j = s.find("$", i)
        if j == -1:
            j = n
        chunk = s[i:j]
        if chunk.strip():
            st.markdown(chunk)
        i = j


def mostrar_como_formula_si_corresponde(texto: Optional[str]) -> str:
    """
    Para enunciados y fórmulas sueltas (pregunta, paso_intermedio, resultado_final).
    Pasa por preparar_latex; si el resultado es una sola fórmula sin $/$$, la envuelve en $$.
    Misma pauta que en Corrección de Manuscritos: no tocar texto mixto.
    """
    t = preparar_latex_para_streamlit(texto or "")
    s = t.strip()
    if not s:
        return t
    if s.startswith(("$", "$$")):
        return t
    if "\\int" in s or "\\sqrt" in s or "\\frac" in s:
        return "$$" + s + "$$"
    return t


def limpiar_json(texto: Optional[str]) -> Optional[Any]:
    """
    Limpieza quirúrgica para respuestas con LaTeX.
    Devuelve dict o list si parsea correctamente; None en caso contrario.
    """
    if not texto: return None
    texto = texto.replace("```json", "").replace("```", "").strip()
    
    # Intento 1: Directo
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        pass

    # Intento 2: Reparación Regex para LaTeX
    try:
        # Escapa barras invertidas que no sean de control JSON
        texto_reparado = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', texto)
        return json.loads(texto_reparado)
    except Exception:
        # Intento 3: Fuerza bruta si falla regex
        try:
            return json.loads(texto.replace("\\", "\\\\"))
        except Exception:
            return None


def _bloque_lista_temas_oficial() -> str:
    return "\n".join(f"  - {t}" for t in temario.LISTA_TEMAS)


def clasificar_tema_desde_texto(texto_usuario: str) -> Optional[str]:
    """
    Pide a la IA que elija un tema de LISTA_TEMAS alineado a la consulta (estadísticas).
    """
    t = (texto_usuario or "").strip()
    if not t:
        return None
    lista_txt = _bloque_lista_temas_oficial()
    prompt = f"""Eres asistente de catalogación para Matemáticas III (Economía UCAB).
Indica a qué tema del temario oficial corresponde mejor la consulta del estudiante.

LISTA OFICIAL (elige UN solo texto EXACTO como aparece abajo, carácter por carácter, o null si ninguno encaja):
{lista_txt}

Consulta:
\"\"\"{t[:4000]}\"\"\"

Responde ÚNICAMENTE con JSON válido, sin markdown:
{{"tema_catedra": "<texto exacto de la lista>" | null}}
"""
    resp = generar_contenido_seguro(prompt)
    if not resp:
        return None
    data = limpiar_json(resp.text)
    if not isinstance(data, dict):
        return None
    return temario.normalizar_tema_curso(data.get("tema_catedra"))


def generar_tutor_paso_a_paso(pregunta_texto: str, tema: str) -> Optional[dict]:
    """Genera la tutoría para el modo Entrenamiento (Banco/IA)."""
    tema_txt = tema or ""
    regla_tema = ""
    if "1.1.1" in tema_txt or "Integrales Indefinidas" in tema_txt:
        regla_tema = """
    RESTRICCIÓN DE CONTENIDO (CRÍTICO para este tema):
    - El tema "1.1.1 Integrales Indefinidas Directas" es EXCLUSIVO de integrales INDEFINIDAS.
    - NO uses integrales definidas: ni límites de integración (ej. \\int_a^b, \\int_0^1), ni "evalúe la integral definida", ni aplicación del teorema fundamental.
    - PROHIBIDO cambios de variable / sustitución: NUNCA escribas "u =", "cambio de variable", "sustitución", ni resuelvas con $du$.
    - Usa SOLO métodos directos:
      * Regla de la potencia para $x^n$ y polinomios ya expandidos.
      * Regla de exponentiales: integrales de $e^{ax}$.
      * Distribución por división en fracciones racionales simples (reducir por álgebra antes de integrar).
      * Multiplicación por constantes y suma distributiva.
    - Si el ejercicio que te pasan tiene integral definida, reescríbelo como integral INDEFINIDA equivalente (misma función a integrar, sin límites) o genera un ejercicio de integral indefinida acorde al tema.
    """

    estrategia_objetivo = ""
    tecnicas_prohibidas: List[str] = []
    terminos_obligatorios: List[str] = []
    restricciones_edo = {
        "2.1.1": (
            "Variables separables",
            ["lineal", "exacta", "homogénea", "bernoulli", "factor integrante"],
            ["separable", "separ"],
        ),
        "2.1.2": (
            "Homogéneas",
            ["lineal", "exacta", "bernoulli", "factor integrante"],
            ["homog"],
        ),
        "2.1.3": (
            "Exactas",
            ["lineal", "homogénea", "bernoulli", "separable", "factor integrante"],
            ["exact", "potencial", "m(x,y)", "n(x,y)"],
        ),
        "2.1.4": (
            "Lineales",
            ["exacta", "homogénea", "bernoulli", "separable"],
            ["lineal", "factor integrante"],
        ),
        "2.1.5": (
            "Bernoulli",
            ["lineal directa", "exacta", "homogénea", "separable"],
            ["bernoulli", "cambio", "v=", "v(x)"],
        ),
        "2.2.1": (
            "ED de orden superior homogénea",
            ["no homogénea", "coeficientes indeterminados", "variación de parámetros"],
            ["homog", "ecuación característica", "raíz"],
        ),
        "2.2.2": (
            "ED de orden superior no homogénea",
            ["homogénea pura solamente"],
            ["no homog", "solución particular", "complementaria"],
        ),
    }
    for code, (objetivo, prohibidas, obligatorios) in restricciones_edo.items():
        if code in tema_txt:
            estrategia_objetivo = objetivo
            tecnicas_prohibidas = prohibidas
            terminos_obligatorios = obligatorios
            regla_tema += f"""
    RESTRICCIÓN DE TÉCNICA (CRÍTICA para {code}):
    - La estrategia CORRECTA debe ser explícitamente de tipo: "{objetivo}".
    - El desarrollo (paso_intermedio y resultado_final) DEBE seguir ese método, no otro.
    - Prohibido resolver usando técnicas fuera del tema (ej.: {", ".join(prohibidas)}).
    - Si el enunciado no encaja, adáptalo mínimamente para que SÍ encaje con la técnica del tema.
    """
            break
    prompt = f"""
    Actúa como un profesor experto. Para el ejercicio: "{pregunta_texto}"
    {regla_tema}
    Genera un objeto JSON.

    REGLAS DE FORMATO (CRÍTICO):
    1. El campo "feedback_estrategia" es texto natural.
    2. Si incluyes fórmulas dentro del texto, úsalas ASÍ: $f(x) = x^2$.
    3. NUNCA escribas párrafos largos dentro de símbolos $.

    PROHIBICIÓN DE FRAGMENTACIÓN: No cierres y abras dólares para la misma expresión.
    MAL: $\\int$ $x^2$ $dx$
    BIEN: $\\int x^2 dx$
    Escribe cada término matemático como una unidad atómica (una sola expresión debe tener un solo par $...$).

    REGLAS LATEX para paso_intermedio y resultado_final:
    - Escribe la fórmula pura. NO incluyas signos "$$" dentro del JSON.
    - Usa DOBLE BARRA para comandos: \\\\frac, \\\\int.

    Estructura JSON:
    {{
        "estrategias": ["Estrategia Correcta", "Estrategia Incorrecta 1", "Estrategia Incorrecta 2"],
        "indice_correcta": 0,
        "feedback_estrategia": "Explicación breve.",
        "paso_intermedio": "Ecuación LaTeX PURA (sin $$) del hito",
        "resultado_final": "Ecuación LaTeX PURA (sin $$) del resultado"
    }}
    Orden aleatorio en estrategias.
    """
    if estrategia_objetivo:
        prompt += """
    AJUSTE PARA ENTRENAMIENTO EN ED:
    - Como el estudiante ya conoce el tipo de ED por el tema, evita centrarte en "elegir técnica".
    - En "feedback_estrategia" escribe el ARRANQUE DE RESOLUCIÓN: primeros pasos operativos concretos
      para implementar esa técnica en este ejercicio (1-3 acciones claras).
    - "paso_intermedio" debe ser una expresión/ecuación que naturalmente venga después de ese arranque.
    """

    def _cumple_restriccion_edo(data: Any) -> bool:
        if not estrategia_objetivo:
            return True
        if not isinstance(data, dict):
            return False
        estrategias = data.get("estrategias") or []
        idx_ok = data.get("indice_correcta", 0)
        if not isinstance(estrategias, list) or not estrategias:
            return False
        try:
            estrategia_ok = str(estrategias[int(idx_ok)]).lower()
        except (TypeError, ValueError, IndexError):
            return False
        bloque = " ".join(
            [
                estrategia_ok,
                str(data.get("feedback_estrategia", "")).lower(),
                str(data.get("paso_intermedio", "")).lower(),
                str(data.get("resultado_final", "")).lower(),
            ]
        )
        if not any(t in bloque for t in terminos_obligatorios):
            return False
        return not any(t in bloque for t in tecnicas_prohibidas)

    for intento in range(2):
        prompt_actual = prompt
        if intento == 1 and estrategia_objetivo:
            prompt_actual += f"""
    CORRECCIÓN OBLIGATORIA:
    Tu intento previo no respetó completamente la técnica "{estrategia_objetivo}".
    Rehaz el JSON asegurando que:
    1) la opción correcta sea explícitamente "{estrategia_objetivo}";
    2) paso_intermedio y resultado_final sigan ESA técnica y no otra.
    """
        response = generar_contenido_seguro(prompt_actual)
        if not response:
            continue
        data = limpiar_json(response.text)
        if _cumple_restriccion_edo(data):
            return data
    return None

def analizar_problema_usuario(
    texto_usuario: Optional[str],
    imagen_usuario: Any = None,
) -> Optional[dict]:
    """
    Analiza un problema subido por el alumno (texto o imagen).
    Distingue entre Integrales/EDO (rígido) y Aplicaciones (flexible).
    """
    prompt_base = """
    Actúa como un Tutor Experto de Matemáticas III.
    Analiza el problema del estudiante (texto o imagen).

    OBJETIVO: Generar una guía paso a paso JSON.

    REGLAS DE ESTRATEGIAS (CRÍTICO):
    1. Si es INTEGRAL (Cálculo directo): Las opciones DEBEN ser Técnicas (ej. "Por Partes", "Sustitución", "Fracciones Parciales").
    2. Si es EDO (Resolver ecuación): Las opciones DEBEN ser Tipos (ej. "Variables Separables", "Lineal", "Exacta").
    3. Si es CÁLCULO DE ÁREAS, VOLÚMENES, EXCEDENTES O APLICACIONES:
       - Tienes LIBERTAD TOTAL.
       - Las opciones deben ser PLANTEAMIENTOS o ENFOQUES (ej. "Integrar con respecto a Y", "Usar método de arandelas", "Igualar Oferta y Demanda").

    REGLAS LATEX (CRÍTICO):
    1. Escribe la fórmula pura. NO incluyas signos "$$" dentro del JSON.
    2. Usa DOBLE BARRA para comandos: \\\\frac, \\\\int.
    
    Estructura JSON requerida:
    {
        "tema_detectado": "Nombre del tema (ej. Volumen de Revolución)",
        "enunciado_latex": "El problema transcrito a LaTeX (sin $$)",
        "estrategias": ["Planteamiento/Técnica CORRECTA", "Opción INCORRECTA 1", "Opción INCORRECTA 2"],
        "indice_correcta": 0,
        "feedback_estrategia": "Por qué este es el camino correcto.",
        "paso_intermedio": "Un hito clave a mitad del desarrollo (LaTeX puro, sin $$)",
        "resultado_final": "La solución final (LaTeX puro, sin $$)"
    }
    """
    
    contenido = [prompt_base]
    if texto_usuario:
        contenido.append(f"Enunciado del estudiante: {texto_usuario}")
    if imagen_usuario:
        contenido.append(imagen_usuario)
        contenido.append("Transcribe y resuelve.")

    response = generar_contenido_seguro(contenido)
    if response:
        return limpiar_json(response.text)
    return None


def evaluar_manuscrito(imagen_manuscrito: Any) -> Optional[dict]:
    """
    Analiza un manuscrito (foto de resolución del estudiante).
    Identifica el enunciado, valora la resolución y emite juicio con sugerencias.
    """
    lista_txt = _bloque_lista_temas_oficial()
    prompt = f"""
    Eres un corrector experto de Matemáticas III (Cálculo Integral y Ecuaciones Diferenciales) para Economía.

    En la imagen verás un manuscrito del estudiante: suele incluir el enunciado del ejercicio y su resolución escrita.

    Realiza en orden:

    0) TEMARIO: Según el enunciado y la resolución visibles, indica a cuál de estos temas oficiales corresponde mejor el ejercicio.
       Copia UN texto EXACTO de la lista (mismo texto, carácter por carácter) o usa null si no encaja ninguno:
{lista_txt}

    1) ENUNCIADO: Identifica y transcribe con claridad el enunciado del ejercicio (qué pide el problema). Si hay fórmulas, escríbelas en LaTeX puro (usa \\\\frac, \\\\int, etc., sin $$ dentro del JSON).

    2) VALORACIÓN: Evalúa la resolución del estudiante (cálculos, método usado, resultado final). Considera si el método es correcto, si hay errores de desarrollo y si el resultado final es correcto.

    3) JUICIO: Emite exactamente uno de estos tres valores: "correcto", "parcialmente_correcto" o "incorrecto".
       - correcto: método adecuado, desarrollo sin errores relevantes y resultado final correcto.
       - parcialmente_correcto: idea o método correcto pero hay errores de cálculo o un paso mal ejecutado; o resultado final incorrecto por un desliz.
       - incorrecto: método equivocado, desarrollo mayormente erróneo o resultado final incorrecto sin rescate.

    4) ERRORES Y OMISIONES: Lista errores detectados (cálculos erróneos, signos, aplicaciones incorrectas de reglas). Lista pasos importantes que el estudiante omitió (por ejemplo, no justificar un cambio de variable, no verificar condiciones, saltarse un paso algebraico clave).

    5) SUGERENCIAS: Da sugerencias concretas de ajuste para corregir errores o completar pasos omitidos. Sé breve y didáctico.

    REGLAS DE FORMATO OBLIGATORIAS:
    1. CADA VEZ que menciones una variable (x, t, y), una función o una integral, 
       DEBES envolverla en símbolos de dólar. Ejemplo: "la variable $x$ se convierte en $t^2$".
    2. PARA EXPRESIONES LARGAS: Usa doble dólar para centrarlas. 
       Ejemplo: "La integral resultante es: $$ \\int (t^2-2) 2t dt $$"
    3. ESPACIOS: Nunca pegues texto a un símbolo $. Deja un espacio: "en $t$," en lugar de "en$t$,".
    4. JSON ESCAPE: Recuerda que en el JSON debes usar DOBLE barra invertida (\\\\int) 
       para que el sistema la reciba correctamente.

    INSTRUCCIONES DE TIPOGRAFÍA SUPERIOR (CRÍTICO):
    1. TODA expresión matemática, por mínima que sea ($x$, $t$, $dx$, $dt$), DEBE ir entre símbolos de dólar.
    2. TRANSFORMACIONES COMPLETAS: Cuando escribas una integral completa resultante de un cambio de variable
       o una simplificación mayor, DEBES usar doble dólar ($$ ... $$) en una línea independiente.
    3. No fragmentes: No escribas $\\int$ $x^2$ $dx$. Escribe $\\int x^2 dx$.
    ...

    Responde ÚNICAMENTE con un objeto JSON válido (sin markdown ni texto alrededor) con esta estructura exacta:
    {{
        "tema_catedra": "<texto exacto de la lista oficial>" | null,
        "enunciado": "Texto o LaTeX del ejercicio identificado",
        "juicio": "correcto" | "parcialmente_correcto" | "incorrecto",
        "resumen_valoracion": "Breve explicación del juicio en 1-3 oraciones.",
        "errores_detectados": ["error 1", "error 2"],
        "pasos_omitidos": ["paso omitido 1", "paso omitido 2"],
        "sugerencias": ["sugerencia 1", "sugerencia 2"]
    }}
    Si no hay errores o pasos omitidos, usa listas vacías [].
    """
    contenido = [prompt, imagen_manuscrito]
    response = generar_contenido_seguro(contenido)
    if response:
        return limpiar_json(response.text)
    return None


def generar_respuesta_tutor_abierto(
    pregunta_usuario: str,
    historial_previo: str,
) -> str:
    """
    Tutor de Preguntas Abiertas.
    Usa el contexto de banco_muestras y banco_preguntas para personalizar la respuesta.
    """
    # 1. Construimos el contexto (tomamos una muestra para no saturar)
    contexto_ejercicios = str(banco_preguntas.BANCO_FIXED[:10]) 
    estilos_examen = banco_muestras.EJEMPLOS_ESTILO

    # 2. Prompt del Sistema (La personalidad del profesor)
    prompt_tutor = f"""
    Eres el tutor virtual de Matemáticas III para Economía en la UCAB.
    Tu objetivo es ayudar al estudiante a entender la teoría, pero SIEMPRE aterrizándola a la práctica de la clase.

    CONTEXTO DE LA CÁTEDRA (Tu base de conocimiento):
    --- Estilos de Examen ---
    {estilos_examen}
    --- Ejercicios del Banco Oficial (Muestra) ---
    {contexto_ejercicios}
    
    INSTRUCCIONES CLAVE:
    1. Responde de forma clara y pedagógica.
    
    2. GESTIÓN DEL CONOCIMIENTO (CRÍTICO):
       - Usa los ejercicios del contexto para mantener el estilo y la dificultad de la cátedra.
       - SI EL CONTEXTO NO TIENE EJEMPLOS DE UN TEMA (ej. Integrales Dobles o Impropias): 
         NO digas "el banco es pequeño" ni "no tengo ejemplos". 
         Genera tú mismo un ejemplo matemático riguroso (nivel Leithold/Larson) y preséntalo con naturalidad, diciendo: "Un caso típico que estudiamos en este tema es..." o "Para ilustrar esto, analicemos...".
    
    3. FORMATO MATEMÁTICO (CRÍTICO): 
       - Usa SIEMPRE signos de dólar para encerrar el LaTeX.
       - Para fórmulas dentro del texto usa uno solo: $ f(x) = x^2 $
       - Para ecuaciones grandes o centradas usa doble signo: $$ \\int_{{a}}^{{b}} f(x) dx $$
       
    4. VINCULACIÓN: Siempre que sea posible, menciona: "Esto sigue la lógica de nuestros ejercicios de parcial..." o "Es análogo a los problemas de oferta y demanda...".

    Historial de chat reciente:
    {historial_previo}

    Pregunta del estudiante:
    {pregunta_usuario}
    """
    
    response = generar_contenido_seguro(prompt_tutor)
    if response:
        return response.text
    return "Lo siento, tuve un problema pensando la respuesta."

def _sanitizar_para_pdf(texto: Optional[str]) -> str:
    """
    Convierte LaTeX a texto legible en el PDF: fracciones como (num/den),
    raíces como sqrt(...), integrales, exponentes, etc., sin código LaTeX crudo.
    """
    if not texto:
        return ""

    t = texto.replace("$$", "").replace("$", "").strip()

    # \frac con contenido posiblemente anidado (ej. \frac{x^3}{3})
    def _reemplazar_frac(s: str) -> str:
        out = []
        i = 0
        while i < len(s):
            if s[i : i + 6] == "\\frac{" and i + 6 < len(s):
                depth = 1
                j = i + 6
                start = j
                while j < len(s) and depth > 0:
                    if s[j] == "{":
                        depth += 1
                    elif s[j] == "}":
                        depth -= 1
                    j += 1
                num = s[start : j - 1]
                if j < len(s) and s[j] == "{":
                    depth = 1
                    j += 1
                    start_den = j
                    while j < len(s) and depth > 0:
                        if s[j] == "{":
                            depth += 1
                        elif s[j] == "}":
                            depth -= 1
                        j += 1
                    den = s[start_den : j - 1]
                    out.append(f" ({_sanitizar_para_pdf(num)}/{_sanitizar_para_pdf(den)}) ")
                    i = j
                else:
                    out.append(s[i:j])
                    i = j
            else:
                out.append(s[i])
                i += 1
        return "".join(out)

    t = _reemplazar_frac(t)

    # Raíz: \sqrt{...} -> sqrt(...) (contenido puede tener llaves anidadas)
    def _reemplazar_sqrt(s: str) -> str:
        idx = s.find("\\sqrt{")
        if idx == -1:
            return s
        depth = 1
        j = idx + 6
        while j < len(s) and depth > 0:
            if s[j] == "{":
                depth += 1
            elif s[j] == "}":
                depth -= 1
            j += 1
        contenido = s[idx + 6 : j - 1]
        return s[:idx] + " sqrt(" + _sanitizar_para_pdf(contenido) + ") " + _reemplazar_sqrt(s[j:])
    t = _reemplazar_sqrt(t)

    # Exponentes: e^{...} -> e^(...), x^{...} -> x^(...)
    t = re.sub(r"e\^\{([^{}]*)\}", r"e^(\1)", t)
    t = re.sub(r"(\w)\^\{([^{}]*)\}", r"\1^(\2)", t)
    # \left( \right) \left[ \right] -> ( ) [ ]
    t = re.sub(r"\\left\s*\(\s*", " ( ", t)
    t = re.sub(r"\s*\\right\s*\)\s*", " ) ", t)
    t = re.sub(r"\\left\s*\[\s*", " [ ", t)
    t = re.sub(r"\s*\\right\s*\]\s*", " ] ", t)
    # Comandos LaTeX -> texto
    t = t.replace("\\int", " integral ")
    t = t.replace("\\ln", " ln ")
    t = t.replace("\\cdot", " ")
    t = t.replace("\\left", " ")
    t = t.replace("\\right", " ")
    # Raíz simple por si quedó algo
    t = re.sub(r"\\sqrt\{([^{}]+)\}", r" sqrt(\1) ", t)
    # Espacios múltiples y recorte
    t = re.sub(r"\s+", " ", t).strip()
    return t[:500] if len(t) > 500 else t

def generar_pdf_informe_quiz(
    respuestas_usuario: List[dict],
    nota_final: float,
) -> Union[bytes, bytearray]:
    """Genera bytes del PDF con calificación y detalle del examen."""
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=14)
    pdf.cell(0, 10, "Informe de evaluacion - Matematicas III - Economias UCAB V5.0", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.cell(0, 8, f"Calificacion final: {nota_final} / 20 pts", ln=True)
    pdf.cell(0, 8, "Aprobado." if nota_final >= 10 else "No aprobado.", ln=True)
    pdf.ln(4)
    for i, r in enumerate(respuestas_usuario, 1):
        pdf.set_font("Helvetica", "B", size=10)
        pts = r.get("puntos", 0)
        pdf.cell(0, 6, f"Pregunta {i} ({pts} pts)", ln=True)
        pdf.set_font("Helvetica", size=9)
        pdf.multi_cell(0, 5, _sanitizar_para_pdf(r.get("pregunta", "")))
        pdf.cell(0, 4, "Tu respuesta: " + _sanitizar_para_pdf(r.get("elegida", "")), ln=True)
        if not r.get("es_correcta", True):
            pdf.cell(0, 4, "Correcta: " + _sanitizar_para_pdf(r.get("correcta", "")), ln=True)
        pdf.cell(0, 4, "Comentario: " + _sanitizar_para_pdf(r.get("explicacion", "")), ln=True)
        pdf.ln(2)
    out = pdf.output()
    return bytes(out) if not isinstance(out, bytes) else out


def extraer_texto_pdf(archivo_pdf: Any, max_chars: int = 30000) -> str:
    """
    Extrae texto de un PDF usando pypdf.
    Limita tamaño para evitar prompts excesivos.
    """
    try:
        reader = PdfReader(archivo_pdf)
        partes: list[str] = []
        for i, pagina in enumerate(reader.pages, start=1):
            texto = (pagina.extract_text() or "").strip()
            if texto:
                partes.append(f"[Página {i}]\n{texto}")
        unido = "\n\n".join(partes).strip()
        if len(unido) > max_chars:
            return unido[:max_chars]
        return unido
    except Exception:
        return ""


def _ruta_admin_docs() -> str:
    base = os.path.dirname(os.path.abspath(__file__))
    carpeta = os.path.join(base, "data")
    os.makedirs(carpeta, exist_ok=True)
    return os.path.join(carpeta, "admin_docs.json")


def cargar_admin_docs() -> list[dict]:
    ruta = _ruta_admin_docs()
    if not os.path.isfile(ruta):
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def guardar_admin_docs(docs: list[dict]) -> None:
    try:
        with open(_ruta_admin_docs(), "w", encoding="utf-8") as f:
            json.dump(docs, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def obtener_evaluaciones_publicadas() -> list[dict]:
    out: list[dict] = []
    for doc in cargar_admin_docs():
        if not doc.get("evaluacion_publicada"):
            continue
        temas_doc = [t for t in (doc.get("temas") or []) if t in temario.LISTA_TEMAS]
        if not temas_doc:
            continue
        out.append(
            {
                "id": str(doc.get("id") or ""),
                "nombre": str(doc.get("evaluacion_nombre") or doc.get("nombre") or "Evaluación"),
                "tipo": str(doc.get("evaluacion_tipo") or "Evaluación"),
                "cantidad": max(1, int(doc.get("evaluacion_cantidad") or NUM_PREGUNTAS_QUIZ)),
                "temas": temas_doc,
            }
        )
    return out


def detectar_temas_desde_pdf(texto_pdf: str) -> list[str]:
    if not texto_pdf.strip():
        return []
    lista_txt = _bloque_lista_temas_oficial()
    prompt = f"""
    Eres un clasificador académico de Matemáticas III para Economía (UCAB).
    Analiza el texto de un documento (examen o guía) y detecta cuáles temas oficiales de la cátedra aparecen.

    Lista oficial de temas:
{lista_txt}

    Responde ÚNICAMENTE con un JSON tipo lista de strings con textos EXACTOS de la lista oficial.
    Si no detectas temas, responde [].

    Texto del PDF:
    {texto_pdf}
    """
    response = generar_contenido_seguro(prompt)
    if not response:
        return []
    data = limpiar_json(response.text)
    if not isinstance(data, list):
        return []

    temas_validos = set(temario.LISTA_TEMAS)
    out: list[str] = []
    for item in data:
        t = temario.normalizar_tema_curso(item)
        if t and t in temas_validos and t not in out:
            out.append(t)
    return out


def generar_preguntas_quiz_desde_documento(
    texto_pdf: str,
    temas_detectados: list[str],
    cantidad: int = 4,
) -> list[dict]:
    """
    Genera preguntas tipo quiz (A-D) a partir de un documento PDF.
    """
    if not texto_pdf.strip() or not temas_detectados:
        return []
    n = max(1, min(int(cantidad or 4), 8))
    prompt = f"""
    Actúa como profesor de Matemáticas III para Economía (UCAB).
    Usa el texto del documento como referencia para proponer preguntas de quiz de selección simple.

    REGLAS:
    - Devuelve ÚNICAMENTE un array JSON válido.
    - Genera {n} preguntas.
    - Cada pregunta debe tener exactamente 4 opciones: A), B), C), D).
    - "respuesta_correcta" debe coincidir literalmente con una opción.
    - Usa LaTeX en formato $...$ cuando aplique.
    - Evita acrónimos o reglas nemotécnicas no utilizadas en la cátedra.
    - El campo "tema" debe ser uno exacto de esta lista:
      {", ".join(temas_detectados)}

    FORMATO:
    [
      {{
        "tema": "Tema exacto",
        "pregunta": "Enunciado",
        "opciones": ["A) ...", "B) ...", "C) ...", "D) ..."],
        "respuesta_correcta": "A) ...",
        "explicacion": "Explicación breve"
      }}
    ]

    Texto del documento:
    {texto_pdf}
    """
    response = generar_contenido_seguro(prompt)
    if not response:
        return []
    data = limpiar_json(response.text)
    if not isinstance(data, list):
        return []

    out: list[dict] = []
    temas_validos = set(temario.LISTA_TEMAS)
    for q in data:
        if not isinstance(q, dict):
            continue
        tema_q = temario.normalizar_tema_curso(q.get("tema"))
        opciones = q.get("opciones")
        correcta = str(q.get("respuesta_correcta") or "").strip()
        if (
            not tema_q
            or tema_q not in temas_validos
            or not isinstance(opciones, list)
            or len(opciones) != 4
            or not correcta
        ):
            continue
        opciones_txt = [str(x).strip() for x in opciones]
        if not any(correcta == op for op in opciones_txt):
            continue
        out.append(
            {
                "tema": tema_q,
                "pregunta": str(q.get("pregunta") or "").strip(),
                "opciones": opciones_txt,
                "respuesta_correcta": correcta,
                "explicacion": str(q.get("explicacion") or "").strip(),
            }
        )
    return out

# --- 2. GESTIÓN DE ESTADO ---
if "quiz_activo" not in st.session_state: st.session_state.quiz_activo = False
if "preguntas_quiz" not in st.session_state: st.session_state.preguntas_quiz = []
if "indice_pregunta" not in st.session_state: st.session_state.indice_pregunta = 0
if "respuestas_usuario" not in st.session_state: st.session_state.respuestas_usuario = [] 

# Estados para Respuesta Guiada (Modo B)
if "consulta_step" not in st.session_state: st.session_state.consulta_step = 0
if "consulta_data" not in st.session_state: st.session_state.consulta_data = None
if "consulta_validada" not in st.session_state: st.session_state.consulta_validada = False

# Estado D: Tutor Preguntas Abiertas
if "historial_tutor_abierto" not in st.session_state: st.session_state.historial_tutor_abierto = []

# Estado E: Corrección de Manuscritos
if "manuscrito_correccion" not in st.session_state: st.session_state.manuscrito_correccion = None
if "admin_auth_ok" not in st.session_state: st.session_state.admin_auth_ok = False
if "quiz_temas_custom_widget" not in st.session_state: st.session_state.quiz_temas_custom_widget = []

# --- 3. INTERFAZ PRINCIPAL ---
ruta, tema_actual = interfaz.mostrar_sidebar()

# Mostrar presentación solo si no hay modo seleccionado; con modo activo, centrar vista en el modo
if not ruta:
    interfaz.mostrar_bienvenida()

# =======================================================
# LÓGICA A: MODO ENTRENAMIENTO (Dojo Matemático)
# =======================================================
elif ruta == "a) Entrenamiento (Temario)":
    st.markdown("### 🥋 Dojo de Matemáticas (Entrenamiento Guiado)")
    st.info("Resolución paso a paso: **1. Elegir Estrategia** -> **2. Hito Intermedio** -> **3. Resultado Final**.")

    if "entrenamiento_activo" not in st.session_state:
        st.session_state.entrenamiento_activo = False

    # --- PANTALLA 0: CONFIGURACIÓN ---
    if not st.session_state.entrenamiento_activo:
        temas_entrenamiento = st.multiselect(
            "🎯 Selecciona los temas a practicar:",
            options=temario.LISTA_TEMAS,
            placeholder="Ej. Ecuaciones Diferenciales Lineales..."
        )

        if st.button(f"⚡ Iniciar Sesión ({NUM_EJERCICIOS_ENTRENAMIENTO} Ejercicios)", type="primary", use_container_width=True):
            if not temas_entrenamiento:
                st.error("⚠️ Selecciona al menos un tema.")
            else:
                cargar_exito = False
                with st.spinner("Preparando tu serie de ejercicios..."):
                    try:
                        import random
                        lista_entrenamiento = []
                        
                        # 1. Banco de Preguntas (Protegido)
                        try:
                            # Hasta completar la sesión con banco si hay ítems (incl. los que traen `grafico`)
                            preguntas_banco = banco_preguntas.obtener_preguntas_fijas(
                                temas_entrenamiento, NUM_EJERCICIOS_ENTRENAMIENTO
                            )
                            if preguntas_banco:
                                lista_entrenamiento.extend(preguntas_banco)
                        except Exception as e:
                            print(f"Aviso: Banco no disponible {e}")

                        # 2. Generación IA (Protegida)
                        faltantes = NUM_EJERCICIOS_ENTRENAMIENTO - len(lista_entrenamiento)
                        if faltantes > 0:
                            prompt_train = temario.generar_prompt_quiz(temas_entrenamiento, faltantes)
                            respuesta_ia = generar_contenido_seguro(prompt_train)
                            
                            if respuesta_ia:
                                preguntas_ia = limpiar_json(respuesta_ia.text)
                                if preguntas_ia: 
                                    lista_entrenamiento.extend(preguntas_ia)
                        
                        if not lista_entrenamiento:
                            st.error("No se encontraron preguntas. No se pudo interpretar la respuesta de la IA; intenta con otro tema o de nuevo.")
                        else:
                            random.shuffle(lista_entrenamiento)
                            st.session_state.entrenamiento_lista = lista_entrenamiento[:NUM_EJERCICIOS_ENTRENAMIENTO]
                            st.session_state.entrenamiento_idx = 0
                            st.session_state.entrenamiento_step = 1
                            st.session_state.entrenamiento_data_ia = None
                            st.session_state.entrenamiento_validado = False 
                            st.session_state.entrenamiento_activo = True
                            cargar_exito = True
                            uso_stats.registrar_uso(
                                "Entrenamiento",
                                detalle={"temas": list(temas_entrenamiento)},
                            )

                    except Exception as e:
                        st.error(f"Error técnico al iniciar: {e}")
                
                if cargar_exito:
                    st.rerun()

    # --- PANTALLA DE EJERCICIOS (El Dojo) ---
    else:
        idx = st.session_state.entrenamiento_idx
        lista = st.session_state.entrenamiento_lista
        
        if idx < len(lista):
            ejercicio = lista[idx]
            tema_ejercicio = str(ejercicio.get("tema", ""))
            es_tema_edo_entrenamiento = tema_ejercicio.startswith("2.")
            
            st.progress((idx + 1) / NUM_EJERCICIOS_ENTRENAMIENTO, text=f"Ejercicio {idx + 1} de {NUM_EJERCICIOS_ENTRENAMIENTO}")
            st.markdown(f"**Tema:** `{ejercicio.get('tema', 'General')}`")
            # Mismo pipeline que la explicación final: texto mixto vía $/$$ → markdown + st.latex
            st.markdown("### Enunciado")
            _render_texto_con_latex(ejercicio.get("pregunta"))
            st.divider()

            # --- LLAMADA A LA IA TUTOR ---
            if st.session_state.entrenamiento_data_ia is None:
                with st.spinner("🧠 El profesor está analizando el mejor camino de resolución..."):
                    datos_tutor = generar_tutor_paso_a_paso(ejercicio['pregunta'], ejercicio.get('tema', 'Cálculo'))
                    if datos_tutor:
                        st.session_state.entrenamiento_data_ia = datos_tutor
                        st.rerun()
                    else:
                        st.error("No se pudo interpretar la respuesta del tutor. Saltando ejercicio; puedes continuar con el siguiente.")
                        st.session_state.entrenamiento_idx += 1
                        time.sleep(2)
                        st.rerun()
            
            tutor = st.session_state.entrenamiento_data_ia
            step = st.session_state.entrenamiento_step

            # PASO 1
            if step == 1:
                if es_tema_edo_entrenamiento:
                    st.markdown("#### 1️⃣ Paso 1: Inicio de la Resolución")
                    st.write(
                        "Ya conoces el tipo de ED por el tema. Empieza aplicando la técnica desde el primer paso."
                    )
                    tecnica_tema = tema_ejercicio.split(":", 1)[-1].strip() if ":" in tema_ejercicio else tema_ejercicio
                    st.success(f"🎯 Técnica del tema: **{tecnica_tema}**")
                    st.info("👨‍🏫 **Arranque sugerido:** " + preparar_latex_para_streamlit(tutor['feedback_estrategia']))
                    if st.button("Ir al Paso Intermedio ➡️", type="primary", key=f"btn_go_step2_{idx}"):
                        st.session_state.entrenamiento_step = 2
                        st.rerun()
                else:
                    st.markdown("#### 1️⃣ Paso 1: Selección de Estrategia")
                    st.write("Antes de calcular, ¿cuál crees que es el camino correcto?")
                    
                    opcion_estrategia = st.radio("Selecciona el método:", tutor['estrategias'], index=None, key=f"radio_estrat_{idx}")
                    
                    if st.button("Validar Estrategia", key=f"btn_val_{idx}"):
                        if opcion_estrategia:
                            idx_seleccionado = tutor['estrategias'].index(opcion_estrategia)
                            if idx_seleccionado == tutor['indice_correcta']:
                                st.session_state.entrenamiento_validado = True 
                            else:
                                st.error("❌ Mmm, no es el mejor camino.")
                                st.warning("Pista: " + preparar_latex_para_streamlit(tutor['feedback_estrategia']))
                        else:
                            st.warning("Debes seleccionar una opción.")

                    if st.session_state.get("entrenamiento_validado", False):
                        st.success("✅ ¡Exacto! Esa es la ruta.")
                        st.info("👨‍🏫 **Feedback:** " + preparar_latex_para_streamlit(tutor['feedback_estrategia']))
                        
                        if st.button("Ir al Paso Intermedio ➡️", type="primary", key=f"btn_go_step2_{idx}"):
                            st.session_state.entrenamiento_step = 2
                            st.session_state.entrenamiento_validado = False
                            st.rerun()

            # PASO 2: HITO INTERMEDIO
            if step == 2:
                if es_tema_edo_entrenamiento:
                    st.success("✅ Inicio de implementación completado")
                else:
                    st.success(f"✅ Estrategia: {tutor['estrategias'][tutor['indice_correcta']]}")
                st.markdown("#### 2️⃣ Paso 2: Ejecución Intermedia")
                st.write("Aplica la estrategia seleccionada. Deberías llegar a una expresión similar a esta:")
                
                st.latex(_limpiar_para_st_latex(tutor["paso_intermedio"]))

                graficos_entrenamiento.mostrar_si_aplica(ejercicio, en_paso_intermedio=True)
                
                st.write("¿Lograste llegar a este punto o algo equivalente?")
                
                col_si, col_no = st.columns(2)
                with col_si:
                    if st.button("👍 Sí, lo tengo", key=f"btn_si_{idx}"):
                        st.session_state.entrenamiento_step = 3
                        st.rerun()
                with col_no:
                    if st.button("👎 No, necesito ayuda", key=f"btn_no_{idx}"):
                        st.error("Revisa tus derivadas/integrales básicas o el álgebra.")

            # PASO 3: FINAL
            if step == 3:
                st.success(f"✅ Estrategia Correcta | ✅ Hito Intermedio Alcanzado")
                st.markdown("#### 3️⃣ Paso 3: Resolución Final")
                st.write("El resultado definitivo es:")
                
                st.success("✅ Resultado final:")
                st.latex(_limpiar_para_st_latex(tutor["resultado_final"]))
                
                with st.expander("Ver explicación completa"):
                    _render_texto_con_latex(ejercicio.get("explicacion", "Procedimiento estándar aplicado correctamente."))

                if st.button("Siguiente Ejercicio ➡️", type="primary", key=f"btn_next_{idx}"):
                    st.session_state.entrenamiento_idx += 1
                    st.session_state.entrenamiento_step = 1
                    st.session_state.entrenamiento_data_ia = None 
                    st.session_state.entrenamiento_validado = False
                    st.rerun()

        else:
            st.success("🎉 ¡Entrenamiento completado!")
            if st.button("🔄 Volver al Inicio", key="btn_reset_entrenamiento"):
                st.session_state.entrenamiento_activo = False
                st.session_state.entrenamiento_idx = 0
                st.rerun()

# =======================================================
# LÓGICA B: RESPUESTA GUIADA (Consultas) - TUTOR PERSONALIZADO
# =======================================================
elif ruta == "b) Respuesta Guiada (Consultas)":
    st.markdown("### 🎓 Tutor Personalizado")
    st.info("Sube tu ejercicio (foto o texto) y te guiaré paso a paso.")

    # 1. INPUT (Foto o Texto)
    if st.session_state.consulta_step == 0:
        col_img, col_txt = st.columns([1, 2])
        with col_img:
            imagen_subida = st.file_uploader("📸 Foto del ejercicio", type=["png", "jpg", "jpeg"])
        with col_txt:
            texto_subido = st.text_area("✍️ O escribe el enunciado aquí:", height=100)

        if st.button("🚀 Resolver Paso a Paso", type="primary", use_container_width=True):
            if not imagen_subida and not texto_subido:
                st.warning("⚠️ Sube una imagen o escribe el texto para comenzar.")
            else:
                exito_analisis = False
                with st.spinner("🤖 Analizando el tipo de problema..."):
                    try:
                        # Solo abrir imagen si el usuario subió un archivo (flujo texto-only no usa imagen)
                        img_pil = None
                        if imagen_subida:
                            img_pil = Image.open(imagen_subida)
                        datos_problema = analizar_problema_usuario(texto_subido or None, img_pil)
                        if datos_problema:
                            st.session_state.consulta_data = datos_problema
                            st.session_state.consulta_step = 1
                            st.session_state.consulta_validada = False
                            exito_analisis = True
                            uso_stats.registrar_uso(
                                "Respuesta Guiada",
                                detalle={
                                    "tema_detectado": (
                                        (datos_problema.get("tema_detectado") or "")
                                        .strip()
                                        or None
                                    ),
                                },
                            )
                        else:
                            st.error("No se pudo interpretar la respuesta del tutor. Intenta de nuevo con otra redacción o imagen más clara.")
                    except Exception as e:
                        st.error(f"Error técnico: {e}")
                
                if exito_analisis:
                    st.rerun()

    # 2. INTERACCIÓN (Similar al Dojo pero para el problema del usuario)
    else:
        datos = st.session_state.consulta_data
        step = st.session_state.consulta_step

        # Botón para cancelar/reiniciar arriba
        if st.button("🔄 Nueva Consulta", key="btn_new_query_top"):
            st.session_state.consulta_step = 0
            st.session_state.consulta_data = None
            st.rerun()

        st.divider()
        st.markdown(f"**Tema Detectado:** `{datos.get('tema_detectado', 'Matemáticas')}`")
        if datos.get('enunciado_latex'):
            st.markdown("**Problema Identificado:**")
            st.markdown(latex_display_puro(datos['enunciado_latex']))
        
        # PASO 1: Identificar Técnica/Tipo o Planteamiento
        if step == 1:
            st.subheader("1️⃣ Paso 1: Planteamiento")
            
            # Lógica dinámica para el mensaje
            tema_lower = datos.get('tema_detectado', '').lower()
            if "integral" in tema_lower and "área" not in tema_lower and "volumen" not in tema_lower:
                st.write("¿Qué **técnica de integración** usarías?")
            elif "ecuación diferencial" in tema_lower and "aplicación" not in tema_lower:
                st.write("¿Qué **tipo de EDO** es esta?")
            else:
                # Caso Áreas, Volúmenes, Excedentes, etc.
                st.write("¿Cuál es el **planteamiento o enfoque** correcto?")

            opcion = st.radio("Selecciona:", datos['estrategias'], index=None, key="rad_cons")
            
            if st.button("Validar Estrategia", type="primary"):
                if opcion and datos['estrategias'].index(opcion) == datos['indice_correcta']:
                    st.session_state.consulta_validada = True
                    st.rerun()
                else:
                    st.error("❌ No es lo más eficiente.")
                    st.warning(preparar_latex_para_streamlit(datos['feedback_estrategia']))
            
            if st.session_state.consulta_validada:
                st.success("✅ ¡Correcto! Vamos a desarrollarlo.")
                if st.button("Ver Paso Intermedio ➡️"):
                    st.session_state.consulta_step = 2
                    st.session_state.consulta_validada = False
                    st.rerun()

        # PASO 2: Hito Intermedio
        if step == 2:
            st.success(f"✅ Estrategia: {datos['estrategias'][datos['indice_correcta']]}")
            st.subheader("2️⃣ Paso 2: Desarrollo")
            st.write("Aplicando la técnica, deberías llegar a esta expresión intermedia:")
            
            st.latex(_limpiar_para_st_latex(datos["paso_intermedio"]))
            
            c1, c2 = st.columns(2)
            if c1.button("👍 Llegué a eso"):
                st.session_state.consulta_step = 3
                st.rerun()
            if c2.button("👎 Me perdí, explícame"):
                st.info("💡 Pista: " + preparar_latex_para_streamlit(datos.get('feedback_estrategia', 'Revisa las operaciones algebraicas.')))

        # PASO 3: Solución Final
        if step == 3:
            st.success("✅ Desarrollo intermedio correcto")
            st.subheader("3️⃣ Solución Final")
            
            st.success("✅ Resultado final:")
            st.latex(_limpiar_para_st_latex(datos["resultado_final"]))
            
            st.balloons()
            if st.button("🏁 Terminar ejercicio"):
                st.session_state.consulta_step = 0
                st.session_state.consulta_data = None
                st.rerun()

# =======================================================
# LÓGICA C: AUTOEVALUACIÓN (Quiz)
# =======================================================
elif ruta == "c) Autoevaluación (Quiz)":
    st.markdown("### 📝 Centro de Evaluación")

    # --- PANTALLA 1: CONFIGURACIÓN ---
    if not st.session_state.quiz_activo:
        st.info("Configura tu prueba (El sistema combinará ejercicios oficiales y generados por IA):")
        temas_sugeridos = st.session_state.pop("quiz_temas_sugeridos", None)
        if isinstance(temas_sugeridos, list):
            st.session_state.quiz_temas_custom_widget = [
                t for t in temas_sugeridos if t in temario.LISTA_TEMAS
            ]
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏆 Generar Primer Parcial (Simulacro)", use_container_width=True):
                st.session_state.quiz_modalidad = "primer_parcial"
                st.session_state.config_temas = temario.TEMAS_PARCIAL_1
                st.session_state.config_cant = NUM_PREGUNTAS_QUIZ 
                st.session_state.quiz_doc_eval_id = None
                st.session_state.trigger_quiz = True
                st.rerun()
        with col2:
            if st.button("🏆 Generar Segundo Parcial (Simulacro)", use_container_width=True):
                st.session_state.quiz_modalidad = "segundo_parcial"
                st.session_state.config_temas = temario.TEMAS_PARCIAL_2
                st.session_state.config_cant = NUM_PREGUNTAS_QUIZ
                st.session_state.quiz_doc_eval_id = None
                st.session_state.trigger_quiz = True
                st.rerun()

        evaluaciones_publicadas = obtener_evaluaciones_publicadas()
        if evaluaciones_publicadas:
            st.markdown("#### 📄 Evaluaciones publicadas por Administración")
            cols_eval = st.columns(2)
            for idx, ev in enumerate(evaluaciones_publicadas):
                with cols_eval[idx % 2]:
                    etiqueta = f"🧾 Generar {ev['tipo']}: {ev['nombre']}"
                    if st.button(etiqueta, key=f"btn_eval_pub_{ev['id']}", use_container_width=True):
                        st.session_state.quiz_modalidad = f"evaluacion_publicada_{ev['id']}"
                        st.session_state.config_temas = ev["temas"]
                        st.session_state.config_cant = ev["cantidad"]
                        st.session_state.quiz_doc_eval_id = ev["id"]
                        st.session_state.trigger_quiz = True
                        st.rerun()

        with st.expander("⚙️ Personalizado"):
            docs_admin = [d for d in cargar_admin_docs() if d.get("activo_quiz")]
            if docs_admin:
                opciones_docs = {
                    f"{d.get('nombre', 'Documento')} ({len(d.get('temas', []))} temas)": d
                    for d in docs_admin
                }
                doc_sel = st.selectbox(
                    "📌 Sugerencia desde documentos cargados por Administración:",
                    list(opciones_docs.keys()),
                    key="quiz_doc_admin_sugerido",
                )
                doc_data = opciones_docs.get(doc_sel) or {}
                temas_doc = [
                    t for t in (doc_data.get("temas") or []) if t in temario.LISTA_TEMAS
                ]
                if temas_doc:
                    st.caption("Temas sugeridos: " + ", ".join(temas_doc))
                    if st.button("Usar estos temas sugeridos", key="btn_quiz_usar_sugerencia"):
                        st.session_state.quiz_temas_custom_widget = temas_doc
                        st.rerun()

            temas_custom = st.multiselect(
                "Temas:",
                temario.LISTA_TEMAS,
                key="quiz_temas_custom_widget",
            )
            if st.button("▶️ Iniciar Quiz Custom"):
                if not temas_custom:
                    st.error("Selecciona tema.")
                else:
                    st.session_state.quiz_modalidad = "personalizado"
                    st.session_state.config_temas = temas_custom
                    st.session_state.config_cant = NUM_PREGUNTAS_QUIZ
                    st.session_state.quiz_doc_eval_id = None
                    st.session_state.trigger_quiz = True
                    st.rerun()

        # --- LÓGICA DE GENERACIÓN ---
        if st.session_state.get("trigger_quiz"):
            quiz_generado = False
            with st.spinner("Compilando examen (Balanceando 50% Banco Oficial / 50% IA)..."):
                try:
                    import random
                    lista_final_preguntas = []
                    cantidad_total = st.session_state.config_cant
                    temas = st.session_state.config_temas
                    doc_eval_id = st.session_state.get("quiz_doc_eval_id")
                    doc_eval = None
                    if doc_eval_id:
                        for d in cargar_admin_docs():
                            if str(d.get("id")) == str(doc_eval_id):
                                doc_eval = d
                                break

                    # 0. Banco auxiliar desde PDFs curados por administración
                    preguntas_docs: list[dict] = []
                    if doc_eval:
                        for q in (doc_eval.get("preguntas_quiz") or []):
                            if isinstance(q, dict):
                                tq = temario.normalizar_tema_curso(q.get("tema"))
                                if tq and tq in temas:
                                    preguntas_docs.append(q)
                    else:
                        for doc in cargar_admin_docs():
                            if not doc.get("activo_quiz"):
                                continue
                            temas_doc = [t for t in (doc.get("temas") or []) if t in temas]
                            if not temas_doc:
                                continue
                            for q in (doc.get("preguntas_quiz") or []):
                                if isinstance(q, dict):
                                    tq = temario.normalizar_tema_curso(q.get("tema"))
                                    if tq and tq in temas:
                                        preguntas_docs.append(q)
                    random.shuffle(preguntas_docs)
                    if doc_eval:
                        cuota_docs = min(cantidad_total, len(preguntas_docs))
                    else:
                        cuota_docs = min(max(1, cantidad_total // 3), len(preguntas_docs)) if preguntas_docs else 0
                    if cuota_docs > 0:
                        lista_final_preguntas.extend(preguntas_docs[:cuota_docs])

                    restantes = cantidad_total - len(lista_final_preguntas)
                    cuota_banco = max(0, restantes // 2)

                    # 1. Banco
                    try:
                        preguntas_banco = banco_preguntas.obtener_preguntas_fijas(temas, cuota_banco)
                        if preguntas_banco:
                            lista_final_preguntas.extend(preguntas_banco)
                    except: pass
                    
                    # 2. IA
                    falta = cantidad_total - len(lista_final_preguntas)
                    if falta > 0:
                        prompt_quiz = temario.generar_prompt_quiz(temas, falta)
                        respuesta = generar_contenido_seguro(prompt_quiz)
                        if respuesta:
                            preguntas_ia = limpiar_json(respuesta.text)
                            if preguntas_ia:
                                lista_final_preguntas.extend(preguntas_ia)
                    
                    random.shuffle(lista_final_preguntas)
                    lista_final_preguntas = lista_final_preguntas[:cantidad_total]

                    if not lista_final_preguntas:
                         st.error("No se pudieron generar preguntas. No se pudo interpretar la respuesta de la IA; intenta de nuevo.")
                         st.session_state.trigger_quiz = False
                    else:
                        st.session_state.preguntas_quiz = lista_final_preguntas
                        st.session_state.indice_pregunta = 0
                        st.session_state.respuestas_usuario = []
                        st.session_state.quiz_activo = True
                        st.session_state.trigger_quiz = False
                        st.session_state.quiz_doc_eval_id = None
                        quiz_generado = True
                        uso_stats.registrar_uso(
                            "Quiz",
                            detalle={
                                "modalidad": st.session_state.get(
                                    "quiz_modalidad", "desconocido"
                                ),
                                "temas": list(temas),
                            },
                        )
                    
                except Exception as e:
                    st.error(f"Error generando examen: {e}")
                    st.session_state.trigger_quiz = False
            
            if quiz_generado:
                st.rerun()

    # --- PANTALLA 2 (RESPONDER) y 3 (RESULTADOS) ---
    else:
        total = len(st.session_state.preguntas_quiz)
        actual = st.session_state.indice_pregunta
        
        if actual < total:
            pregunta_data = st.session_state.preguntas_quiz[actual]
            
            st.progress((actual) / total, text=f"Pregunta {actual + 1} de {total}")
            
            # 1. RENDERIZADO DE LA PREGUNTA (misma ruta que entrenamiento: markdown + st.latex)
            st.markdown("#### Pregunta")
            _render_texto_con_latex(pregunta_data["pregunta"])
            st.divider()
            
            # 2. RENDERIZADO DE LAS OPCIONES — letra en markdown, fórmula vía _render_texto_con_latex
            st.write("Opciones:")
            col_ops = st.columns(2)
            opciones_completas = pregunta_data["opciones"]

            for i, opcion_texto in enumerate(opciones_completas):
                with col_ops[i % 2]:
                    if ")" in opcion_texto:
                        letra, resto = opcion_texto.split(")", 1)
                        st.markdown(f"**{letra.strip()})**")
                        _render_texto_con_latex(resto.strip())
                    else:
                        _render_texto_con_latex(opcion_texto)
            
            st.divider()

            # 3. SELECTOR DE RESPUESTA (LÓGICA)
            ya_respondido = len(st.session_state.respuestas_usuario) > actual
            
            if not ya_respondido:
                # Creamos opciones simplificadas (Solo A, B, C, D) para el selector
                # Así evitamos que Streamlit intente renderizar LaTeX crudo en el widget
                opciones_radio = [op.split(")")[0] + ")" for op in opciones_completas]
                
                seleccion_letra = st.radio(
                    "Selecciona tu respuesta:", 
                    opciones_radio, 
                    key=f"radio_{actual}", 
                    index=None,
                    horizontal=True
                )

                if st.button("Responder", type="primary"):
                    if seleccion_letra:
                        # Recuperamos la opción completa original basada en la letra seleccionada
                        letra_elegida = seleccion_letra.split(")")[0] # Ej: "A"
                        # Buscamos la opción original que empieza con esa letra
                        opcion_elegida_completa = next(op for op in opciones_completas if op.startswith(letra_elegida))
                        
                        letra_correcta = pregunta_data['respuesta_correcta'].strip()[0].upper()
                        es_correcta = (letra_elegida == letra_correcta)
                        pts = round(20 / total, 2) if es_correcta else 0
                        
                        st.session_state.respuestas_usuario.append({
                            "pregunta": pregunta_data['pregunta'],
                            "elegida": opcion_elegida_completa, # Guardamos la completa para el reporte final
                            "correcta": pregunta_data['respuesta_correcta'],
                            "explicacion": pregunta_data['explicacion'],
                            "puntos": pts,
                            "es_correcta": es_correcta
                        })
                        st.rerun()
                    else:
                        st.warning("⚠️ Selecciona una opción.")
            
            else:
                # FEEDBACK INMEDIATO (Si ya respondió pero no ha pasado a la siguiente)
                ultimo_dato = st.session_state.respuestas_usuario[actual]
                
                st.info("**Tu respuesta:**")
                _render_texto_con_latex(ultimo_dato["elegida"])
                
                if ultimo_dato['es_correcta']:
                    st.success("✅ ¡Correcto!")
                else:
                    st.error("❌ Incorrecto. **La correcta era:**")
                    _render_texto_con_latex(ultimo_dato["correcta"])
                
                with st.expander("💡 Ver Explicación", expanded=True):
                    _render_texto_con_latex(ultimo_dato["explicacion"])
                
                if st.button("Siguiente Pregunta ➡️", type="primary"):
                    st.session_state.indice_pregunta += 1
                    st.rerun()

        else:
            # PANTALLA 3: RESULTADOS
            suma_puntos = sum(r['puntos'] for r in st.session_state.respuestas_usuario)
            nota_final = round(suma_puntos, 2)

            if nota_final >= 10:
                st.success(f"✅ Examen Finalizado - Aprobado con {nota_final}")
            else:
                st.warning(f"⚠️ Examen Finalizado - Nota: {nota_final}")
            
            col_nota_top, col_info_top = st.columns([1, 2])
            with col_nota_top:
                st.metric("Calificación Final", f"{nota_final} / 20 pts")
            with col_info_top:
                st.info("💡 Puedes **descargar el informe en PDF** con tu calificación y comentarios al final de esta página.")

            st.divider()
            st.subheader("📄 Detalle del Examen")

            for i, r in enumerate(st.session_state.respuestas_usuario):
                st.markdown(f"#### 🔹 Pregunta {i+1} ({r['puntos']} pts)")
                _render_texto_con_latex(r["pregunta"])
                
                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    if r['es_correcta']:
                        st.success("✅ **Tu respuesta:**")
                    else:
                        st.error("❌ **Tu respuesta:**")
                    _render_texto_con_latex(r["elegida"])
                
                with col_res2:
                    if not r['es_correcta']:
                        st.warning("✔ **Correcta:**")
                        _render_texto_con_latex(r["correcta"])

                st.markdown("**📝 Explicación:**")
                _render_texto_con_latex(r["explicacion"])
                st.markdown("---")

            st.markdown("### 🏁 Resumen Final")
            col_nota_bot, col_info_bot = st.columns([1, 2])
            with col_nota_bot:
                st.metric("Calificación Final ", f"{nota_final} / 20 pts")
            
            st.divider()

            col_pdf, col_nuevo = st.columns(2)
            with col_pdf:
                pdf_bytes = generar_pdf_informe_quiz(st.session_state.respuestas_usuario, nota_final)
                pdf_bytes = bytes(pdf_bytes) if isinstance(pdf_bytes, bytearray) else pdf_bytes
                st.download_button(
                    "📥 Descargar informe (PDF)",
                    data=pdf_bytes,
                    file_name=f"informe_Mate3_UCAB_V5_{str(nota_final).replace('.', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            with col_nuevo:
                if st.button("🔄 Comenzar Nuevo Examen", type="primary", use_container_width=True):
                    st.session_state.quiz_activo = False
                    st.session_state.indice_pregunta = 0
                    st.session_state.respuestas_usuario = []
                    st.rerun()
# =======================================================
# LÓGICA D: TUTOR PREGUNTAS ABIERTAS (NUEVO)
# =======================================================
elif ruta == "d) Tutor: Preguntas Abiertas":
    st.markdown("### 💬 Preguntas Abiertas al Tutor")
    with st.form("form_pregunta_abierta", clear_on_submit=True):
        prompt = st.text_input(
            "Escribe tu pregunta",
            placeholder="Ej. Puedes pedir un resumen o una explicación corta de cualquier tema a partir de ejercicios del profesor.",
        )
        enviar_pregunta = st.form_submit_button("Enviar pregunta", use_container_width=True)

    st.markdown("""
    Haz cualquier pregunta teórica. El tutor te responderá **vinculando la teoría con
    los ejercicios y estilos de examen** de nuestra cátedra.
    """)

    if len(st.session_state.historial_tutor_abierto) > AVISO_HISTORIAL_LARGO:
        st.info("💬 **Conversación larga.** Para respuestas más precisas, considera usar **Reiniciar** en el menú y empezar una nueva.")

    for mensaje in st.session_state.historial_tutor_abierto:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    if enviar_pregunta and prompt.strip():
        prompt = prompt.strip()
        with st.spinner("Clasificando tema para estadísticas…"):
            _tema_stats = clasificar_tema_desde_texto(prompt)
        uso_stats.registrar_uso(
            "Tutor Preguntas Abiertas",
            detalle={
                "tema_catedra": _tema_stats,
                "pregunta_resumen": (prompt or "")[:500],
            },
        )
        st.session_state.historial_tutor_abierto.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Consultando guías de la cátedra..."):
                ultimos = st.session_state.historial_tutor_abierto[-MAX_MENSAJES_HISTORIAL_TUTOR:]
                historial_texto = "\n".join([f"{m['role']}: {m['content']}" for m in ultimos])
                respuesta_tutor = generar_respuesta_tutor_abierto(prompt, historial_texto)
                st.markdown(respuesta_tutor)

        st.session_state.historial_tutor_abierto.append({"role": "assistant", "content": respuesta_tutor})

# =======================================================
# LÓGICA E: CORRECCIÓN DE MANUSCRITOS
# =======================================================
elif ruta == "e) Corrección de Manuscritos":
    st.markdown("### 📄 Corrección de Manuscritos")
    st.info("Sube una foto de tu resolución escrita. La app identificará el enunciado, valorará tu solución y te dará un juicio (correcto / parcialmente correcto / incorrecto) con sugerencias de ajuste.")

    imagen_manuscrito = st.file_uploader(
        "📸 Sube la foto de tu manuscrito (enunciado + resolución)",
        type=["png", "jpg", "jpeg"],
        key="upload_manuscrito"
    )

    if imagen_manuscrito:
        st.image(imagen_manuscrito, caption="Tu manuscrito", use_container_width=True)

        if st.button("🔍 Evaluar manuscrito", type="primary", use_container_width=True):
            with st.spinner("Analizando enunciado y valorando tu resolución..."):
                try:
                    img_pil = Image.open(imagen_manuscrito)
                    resultado = evaluar_manuscrito(img_pil)
                    if resultado:
                        _tm = temario.normalizar_tema_curso(resultado.get("tema_catedra"))
                        uso_stats.registrar_uso(
                            "Corrección de Manuscritos",
                            detalle={"tema_catedra": _tm},
                        )
                        st.session_state.manuscrito_correccion = resultado
                        st.rerun()
                    else:
                        st.error("No se pudo interpretar la corrección. Intenta con una imagen más clara o con otro manuscrito.")
                except Exception as e:
                    st.error(f"Error al procesar la imagen: {e}")

    if st.session_state.manuscrito_correccion:
        datos = st.session_state.manuscrito_correccion
        st.divider()
        _tc_show = temario.normalizar_tema_curso(datos.get("tema_catedra"))
        if _tc_show:
            st.caption(f"📌 **Tema identificado (cátedra):** `{_tc_show}`")

        st.subheader("📋 Enunciado identificado")
        enunciado = datos.get("enunciado", "")
        if enunciado:
            s = enunciado.strip().replace("\\\\", "\n")
            # Si es solo una fórmula (sin texto tipo "Calcular..."): un solo bloque $$ sin $ internos
            es_solo_formula = ("\\int" in s or "\\sqrt" in s or "\\frac" in s) and not any(
                w in s.lower() for w in ["calcular", "evalúe", "resuelva", "siguiente", "definida", "indefinida", "con respecto", "variable x", "la integral"]
            )
            if es_solo_formula:
                t = "$$" + s.replace("$", "").strip() + "$$"
            else:
                t = preparar_latex_para_streamlit(enunciado)
            st.markdown(t)
        else:
            st.caption("(No se pudo extraer enunciado)")

        juicio = (datos.get("juicio") or "").strip().lower()
        st.subheader("⚖️ Juicio")
        if juicio == "correcto":
            st.success("✅ **Correcto** — Tu resolución es correcta.")
        elif juicio == "parcialmente_correcto":
            st.warning("⚠️ **Parcialmente correcto** — Hay aspectos a mejorar.")
        elif juicio == "incorrecto":
            st.error("❌ **Incorrecto** — La resolución presenta errores importantes.")
        else:
            st.info(f"**Juicio:** {juicio or 'No especificado'}")

        resumen = datos.get("resumen_valoracion", "")
        if resumen:
            st.markdown("**Valoración:**")
            st.markdown(preparar_latex_para_streamlit(resumen))

        errores = datos.get("errores_detectados") or []
        if errores:
            st.subheader("🔴 Errores detectados")
            for e in errores:
                st.markdown("- " + preparar_latex_para_streamlit(e))

        pasos_omitidos = datos.get("pasos_omitidos") or []
        if pasos_omitidos:
            st.subheader("📌 Pasos omitidos o importantes")
            for p in pasos_omitidos:
                st.markdown("- " + preparar_latex_para_streamlit(p))

        sugerencias = datos.get("sugerencias") or []
        if sugerencias:
            st.subheader("💡 Sugerencias de ajuste")
            for s in sugerencias:
                st.markdown("- " + preparar_latex_para_streamlit(s))

        st.divider()
        if st.button("🔄 Evaluar otro manuscrito", key="btn_nuevo_manuscrito"):
            st.session_state.manuscrito_correccion = None
            st.rerun()

# =======================================================
# LÓGICA F: ADMINISTRADOR (MÉTRICAS + ACTUALIZACIÓN DE CORE)
# =======================================================
elif ruta == "f) Administrador (Métricas)":
    st.markdown("### 🛠️ Panel de Administrador")
    if not st.session_state.get("admin_auth_ok", False):
        st.warning("🔐 Acceso restringido: inicia sesión como administrador.")
        with st.form("admin_login_form", clear_on_submit=False):
            correo_admin = st.text_input("Correo de administrador")
            clave_admin = st.text_input("Clave", type="password")
            enviar = st.form_submit_button("Ingresar")
        if enviar:
            ok = (
                (correo_admin or "").strip().lower() == ADMIN_EMAIL_PERMITIDO
                and (clave_admin or "") == ADMIN_CLAVE_PERMITIDA
            )
            if ok:
                st.session_state.admin_auth_ok = True
                st.success("✅ Autenticación correcta.")
                st.rerun()
            else:
                st.error("❌ Credenciales inválidas.")
        st.stop()

    c_auth1, c_auth2 = st.columns([3, 1])
    with c_auth1:
        st.info(
            "Métricas globales de uso por módulo y tema. "
            "Si Supabase está configurado, verás agregados globales; si no, datos locales."
        )
    with c_auth2:
        if st.button("Cerrar sesión admin"):
            st.session_state.admin_auth_ok = False
            st.rerun()

    st.subheader("📚 Actualización del core con documentos PDF")
    st.caption(
        "Sube exámenes o guías para detectar temas del temario y habilitar sugerencias de quiz específico en Autoevaluación."
    )

    tipo_doc = st.selectbox(
        "Tipo de documento",
        ["Examen", "Guía", "Otro"],
        key="admin_tipo_doc",
    )
    publicar_en_autoeval = st.checkbox(
        "Publicar estos documentos como evaluación en Autoevaluación",
        value=True,
        key="admin_publicar_autoeval",
    )
    tipo_evaluacion = st.selectbox(
        "Tipo de evaluación a publicar",
        ["Prueba Corta", "Quiz Temático", "Evaluación Especial"],
        key="admin_tipo_eval_pub",
    )
    cantidad_eval = st.slider(
        "Cantidad de preguntas para la evaluación publicada",
        min_value=3,
        max_value=20,
        value=NUM_PREGUNTAS_QUIZ,
        step=1,
        key="admin_cantidad_eval_pub",
    )
    docs_pdf = st.file_uploader(
        "Cargar documentos PDF",
        type=["pdf"],
        accept_multiple_files=True,
        key="admin_upload_pdf_docs",
    )
    if st.button("Procesar documentos", type="primary", use_container_width=True, key="admin_procesar_docs"):
        if not docs_pdf:
            st.warning("Selecciona al menos un PDF.")
        else:
            almacenados = cargar_admin_docs()
            nuevos = 0
            for archivo in docs_pdf:
                texto_pdf = extraer_texto_pdf(archivo, max_chars=45000)
                if not texto_pdf:
                    continue
                temas_detectados = detectar_temas_desde_pdf(texto_pdf[:12000])
                registro = {
                    "id": f"{int(time.time())}_{len(almacenados)+1}",
                    "nombre": archivo.name,
                    "tipo": tipo_doc,
                    "fecha_carga": datetime.now().isoformat(timespec="seconds"),
                    "temas": temas_detectados,
                    "activo_quiz": True,
                    "extracto": texto_pdf[:1500],
                    "preguntas_quiz": generar_preguntas_quiz_desde_documento(
                        texto_pdf=texto_pdf[:12000],
                        temas_detectados=temas_detectados,
                        cantidad=max(4, int(cantidad_eval)),
                    ),
                    "evaluacion_publicada": bool(publicar_en_autoeval),
                    "evaluacion_tipo": tipo_evaluacion,
                    "evaluacion_nombre": os.path.splitext(archivo.name)[0],
                    "evaluacion_cantidad": int(cantidad_eval),
                }
                almacenados.insert(0, registro)
                nuevos += 1
            guardar_admin_docs(almacenados)
            if nuevos:
                st.success(f"Documentos procesados y guardados: {nuevos}")
                st.rerun()
            else:
                st.error("No se pudo extraer texto utilizable de los PDF cargados.")

    docs_guardados = cargar_admin_docs()
    if docs_guardados:
        st.markdown("**Documentos registrados**")
        for doc in docs_guardados[:40]:
            doc_id = str(doc.get("id") or "")
            nombre = doc.get("nombre") or "Documento"
            temas = [t for t in (doc.get("temas") or []) if t in temario.LISTA_TEMAS]
            estado = "Activo para sugerencias de quiz" if doc.get("activo_quiz") else "Inactivo"
            ev_txt = ""
            if doc.get("evaluacion_publicada"):
                ev_txt = f" · Publicado: {doc.get('evaluacion_tipo', 'Evaluación')} ({int(doc.get('evaluacion_cantidad') or NUM_PREGUNTAS_QUIZ)} preg.)"
            with st.expander(f"{nombre} · {doc.get('tipo', 'N/D')} · {estado}{ev_txt}", expanded=False):
                st.caption(f"Cargado: {doc.get('fecha_carga', '-')}")
                st.caption("Temas detectados: " + (", ".join(temas) if temas else "Ninguno"))
                st.caption(f"Preguntas candidatas para quiz: {len(doc.get('preguntas_quiz') or [])}")
                st.caption((doc.get("extracto") or "").strip()[:500] or "_Sin extracto_")

                c_d1, c_d2, c_d3, c_d4 = st.columns(4)
                with c_d1:
                    if st.button("Usar para quiz", key=f"admin_set_quiz_{doc_id}"):
                        if temas:
                            st.session_state.quiz_temas_sugeridos = temas
                            st.session_state.modo_actual = "c) Autoevaluación (Quiz)"
                            st.success("Sugerencia enviada a Autoevaluación.")
                            st.rerun()
                        else:
                            st.warning("Este documento no tiene temas detectados del temario.")
                with c_d2:
                    btn_label = "Desactivar" if doc.get("activo_quiz") else "Activar"
                    if st.button(btn_label, key=f"admin_toggle_doc_{doc_id}"):
                        nuevos_docs = cargar_admin_docs()
                        for x in nuevos_docs:
                            if str(x.get("id")) == doc_id:
                                x["activo_quiz"] = not bool(x.get("activo_quiz"))
                                break
                        guardar_admin_docs(nuevos_docs)
                        st.rerun()
                with c_d3:
                    pub_label = "Quitar de Autoeval" if doc.get("evaluacion_publicada") else "Publicar en Autoeval"
                    if st.button(pub_label, key=f"admin_toggle_pub_{doc_id}"):
                        nuevos_docs = cargar_admin_docs()
                        for x in nuevos_docs:
                            if str(x.get("id")) == doc_id:
                                x["evaluacion_publicada"] = not bool(x.get("evaluacion_publicada"))
                                if not x.get("evaluacion_tipo"):
                                    x["evaluacion_tipo"] = "Evaluación Especial"
                                if not x.get("evaluacion_nombre"):
                                    x["evaluacion_nombre"] = os.path.splitext(str(x.get("nombre") or "Evaluación"))[0]
                                if not x.get("evaluacion_cantidad"):
                                    x["evaluacion_cantidad"] = NUM_PREGUNTAS_QUIZ
                                break
                        guardar_admin_docs(nuevos_docs)
                        st.rerun()
                with c_d4:
                    if st.button("Eliminar", key=f"admin_delete_doc_{doc_id}"):
                        nuevos_docs = [
                            x for x in cargar_admin_docs() if str(x.get("id")) != doc_id
                        ]
                        guardar_admin_docs(nuevos_docs)
                        st.rerun()

    st.divider()
    warn = st.session_state.get("_uso_stats_supabase_warn")
    if warn:
        st.warning(warn)

    stats = uso_stats.obtener_estadisticas()
    total_uso = sum(int(stats.get(m, 0) or 0) for m in uso_stats.MODULOS)
    mod_con_uso = sum(1 for m in uso_stats.MODULOS if int(stats.get(m, 0) or 0) > 0)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Interacciones totales", total_uso)
    with c2:
        st.metric("Módulos con uso", f"{mod_con_uso} / {len(uso_stats.MODULOS)}")
    with c3:
        st.metric("Módulo más usado", max(uso_stats.MODULOS, key=lambda m: int(stats.get(m, 0) or 0)))

    st.subheader("Cantidad de accesos por cada funcionalidad")
    st.bar_chart({m: int(stats.get(m, 0) or 0) for m in uso_stats.MODULOS})

    st.subheader("Cantidad de ejercicios resueltos por cada tema del pensum")
    por_tema = uso_stats.obtener_estadisticas_temas()
    top_n = st.slider("Top de temas", min_value=5, max_value=25, value=10, step=1)
    filas_temas = sorted(
        [{"tema": t, "consultas": int(por_tema.get(t, 0) or 0)} for t in temario.LISTA_TEMAS],
        key=lambda r: (-r["consultas"], r["tema"]),
    )
    st.dataframe(filas_temas[:top_n], use_container_width=True, hide_index=True)

    st.subheader("Histograma de uso por fechas")
    eventos_hist = uso_stats.obtener_eventos_recientes(limit=2000)
    fechas_evento = []
    for e in eventos_hist:
        ts = e.get("timestamp")
        if not ts:
            continue
        try:
            dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
            fechas_evento.append(dt.date())
        except ValueError:
            continue

    if fechas_evento:
        min_f = min(fechas_evento)
        max_f = max(fechas_evento)

        cf1, cf2, cf3 = st.columns([1, 1, 1.2])
        with cf1:
            fecha_desde = st.date_input("Desde", value=min_f, min_value=min_f, max_value=max_f, key="admin_f_desde")
        with cf2:
            fecha_hasta = st.date_input("Hasta", value=max_f, min_value=min_f, max_value=max_f, key="admin_f_hasta")
        with cf3:
            granularidad = st.selectbox(
                "Agrupar por",
                ["Día", "Semana", "Mes"],
                index=0,
                key="admin_hist_granularidad",
            )

        if fecha_desde > fecha_hasta:
            st.warning("La fecha 'Desde' no puede ser mayor que 'Hasta'.")
        else:
            hist: dict[str, int] = {}
            for e in eventos_hist:
                ts = e.get("timestamp")
                if not ts:
                    continue
                try:
                    dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
                    d = dt.date()
                except ValueError:
                    continue
                if d < fecha_desde or d > fecha_hasta:
                    continue

                if granularidad == "Día":
                    bucket = d.isoformat()
                elif granularidad == "Semana":
                    y, w, _ = d.isocalendar()
                    bucket = f"{y}-W{w:02d}"
                else:  # Mes
                    bucket = d.strftime("%Y-%m")
                hist[bucket] = hist.get(bucket, 0) + 1

            if hist:
                hist_rows = [
                    {"periodo": p, "uso": n}
                    for p, n in sorted(hist.items(), key=lambda x: x[0])
                ]
                st.bar_chart(hist_rows, x="periodo", y="uso")
                st.caption(f"Periodos con actividad en el rango: {len(hist_rows)}")
            else:
                st.caption("No hay actividad en el rango seleccionado.")
    else:
        st.caption("No hay suficientes eventos con fecha para construir el histograma.")

    st.subheader("Eventos recientes")
    eventos = uso_stats.obtener_eventos_recientes(limit=250)
    if not eventos:
        st.caption("No hay eventos recientes disponibles.")
    else:
        opciones_modo = ["(Todos)"] + sorted({str(e.get("modo") or "") for e in eventos if e.get("modo")})
        filtro_modo = st.selectbox("Filtrar por módulo", opciones_modo, index=0)
        texto = st.text_input("Buscar en payload (texto)", value="").strip().lower()

        rows = []
        for e in eventos:
            modo = str(e.get("modo") or "")
            payload = e.get("payload") or {}
            payload_txt = json.dumps(payload, ensure_ascii=False)
            if filtro_modo != "(Todos)" and modo != filtro_modo:
                continue
            if texto and texto not in payload_txt.lower():
                continue
            rows.append(
                {
                    "timestamp": e.get("timestamp"),
                    "modo": modo,
                    "payload": payload_txt[:500],
                }
            )
        st.caption(f"Mostrando {len(rows)} eventos")
        st.dataframe(rows[:200], use_container_width=True, hide_index=True)

# Cintillo institucional al cierre de la página.
interfaz.mostrar_cintillo_cierre()
