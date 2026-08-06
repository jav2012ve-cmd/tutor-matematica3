# Matemáticas III - Economías UCAB Versión 5.0

Tutor virtual para la cátedra de **Matemáticas III** (Cálculo Integral y Ecuaciones Diferenciales), Escuela de Economía, UCAB. Incluye entrenamiento guiado (**apoyo gráfico interactivo con Plotly** en el paso intermedio para temas del banco que lo incorporen), consultas con foto o texto, quiz de autoevaluación (con **informe descargable en PDF** al finalizar) y tutor de preguntas abiertas, usando **Streamlit** y **Google Gemini**.

## Requisitos

- Python 3.8+
- API Key de Google (Gemini)

## Instalación

```bash
pip install -r requirements.txt
```

## Configurar la API Key (obligatorio)

La aplicación necesita `GOOGLE_API_KEY` para conectar con Gemini.

1. Obtén una clave en [Google AI Studio](https://aistudio.google.com/apikey).
2. **Ejecución local:** crea la carpeta `.streamlit` y dentro el archivo `secrets.toml` con:
   ```toml
   GOOGLE_API_KEY = "tu-clave-aqui"
   ```
3. **Streamlit Cloud:** en tu app → Settings → Secrets, añade la variable `GOOGLE_API_KEY`.

Opcional: `GEMINI_MODEL = "gemini-3.5-flash"` para fijar el modelo. **No uses** ids retirados (`gemini-2.0-flash`, `gemini-1.5-*`); la app los ignora y cae a un fallback.

Sin esta clave, la app se detendrá y mostrará en pantalla las mismas instrucciones.

## Estadísticas de uso con Supabase (recomendado en Streamlit Cloud)

En la nube el disco del contenedor es **efímero**: los contadores en `data/uso_stats.json` se pierden al reiniciar o cuando la app “duerme”. Para conservar los totales de uso por modo, configura **Supabase**:

1. Crea un proyecto en [Supabase](https://supabase.com/).
2. En **SQL Editor**, ejecuta en este orden (o solo los que falten): `supabase_schema.sql`, `supabase_usage_events.sql`, `supabase_topic_usage.sql`, luego **`supabase_topic_usage_seed.sql`** (crea una fila por cada tema con `count = 0` para ver cobertura). Si hace falta, ejecuta `supabase_grants.sql`.
3. **Comprueba la base** (opcional): en SQL Editor ejecuta `SELECT public.increment_module_usage('Entrenamiento');` y luego `SELECT * FROM public.app_module_usage;` — debe aparecer una fila. Si aquí funciona pero la app no escribe, faltan **Secrets** en Streamlit o la app desplegada está desactualizada.
4. En **Project Settings → API** copia **Project URL** y la clave **service_role** (solo para backend; no la expongas en el navegador).
5. Añade en `.streamlit/secrets.toml` (local) o en **Streamlit Cloud → Secrets**:

   ```toml
   SUPABASE_URL = "https://xxxx.supabase.co"
   SUPABASE_SERVICE_ROLE_KEY = "eyJhbG..."
   ```

   También puedes usar la variable de entorno `SUPABASE_SERVICE_ROLE_KEY` o, por compatibilidad, `SUPABASE_KEY` con el mismo valor de service role.

Si no configuras Supabase, la app sigue funcionando y guardará contadores solo en archivo local (`data/uso_stats.json`). Los detalles de interacción, si no llegan a Supabase, se pueden volcar en `data/usage_events.jsonl` (local). Los conteos por tema van a `data/topic_usage.json` si falla la nube.

**Tabla `app_topic_usage`:** una **fila por tema** del temario (`topic_key`, `count`). Así se ve qué temas acumulan estudio y cuáles siguen en 0, sin crear decenas de columnas fijas en SQL (si cambia `LISTA_TEMAS`, actualiza `supabase_topic_usage_seed.sql` y vuelve a ejecutar solo los `INSERT` nuevos). La app incrementa vía RPC `increment_topic_usage_batch` cuando hay `detalle` con temas (entrenamiento, quiz, respuesta guiada, tutor, manuscritos).

**Tabla `app_usage_event`:** columnas `id`, `created_at`, **`modo`**, **`payload` (jsonb)**. En el Table Editor de Supabase, desplázate horizontalmente o abre **Edit table** si no ves `payload`. Si la tabla se creó sin esa columna, ejecuta `supabase_usage_events_add_payload.sql` en el SQL Editor.

Ejemplos de `payload`: entrenamiento `{"temas": [...]}`, quiz `{"modalidad": "primer_parcial"|"segundo_parcial"|"personalizado", "temas": [...]}`, respuesta guiada `{"tema_detectado": "..."}`, tutor `{"tema_catedra": "..."|null, "pregunta_resumen": "..."}` (tema clasificado por IA según el temario), manuscritos `{"tema_catedra": "..."|null}` (mismo criterio, en la misma respuesta JSON del corrector).

La app habla con Supabase por la **API REST** de PostgREST (con la librería `requests`); no hace falta instalar el paquete pesado `supabase-py`.

## Ejecutar

```bash
streamlit run app.py
```

## Modos de la aplicación

- **Entrenamiento (Temario):** serie de 5 ejercicios paso a paso por temas.
- **Respuesta guiada:** subes foto o texto de un ejercicio y el tutor te guía.
- **Autoevaluación (Quiz):** simulacro de parcial (Primer, Segundo o temas personalizados).
- **Tutor preguntas abiertas:** chat sobre teoría y ejercicios de la cátedra.

## Tests (opcional)

```bash
pip install pytest
python -m pytest tests/ -v
```
