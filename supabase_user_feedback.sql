-- Ejecutar en Supabase → SQL Editor (después de supabase_usage_events.sql).
-- Registra de forma tipada las retroalimentaciones anónimas (opciones a–e del tutor).

CREATE TABLE IF NOT EXISTS public.app_user_feedback_report (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at timestamptz NOT NULL DEFAULT now(),
  funcionalidad text NOT NULL,
  codigo_opcion char(1) NOT NULL CHECK (codigo_opcion IN ('a', 'b', 'c', 'd', 'e')),
  tipo_reporte text NOT NULL CHECK (
    tipo_reporte IN (
      'ok_sin_incidencias',
      'latex_visual_sin_impacto_funcional',
      'latex_afecto_funcionalidad',
      'contenido_respuestas_incorrectas',
      'imagen_manuscrito_no_reconocido'
    )
  ),
  extra jsonb NOT NULL DEFAULT '{}'::jsonb
);

COMMENT ON TABLE public.app_user_feedback_report IS
  'Retroalimentación anónima del usuario: código de opción (a–e) y tipo de informe normalizado para analítica.';

COMMENT ON COLUMN public.app_user_feedback_report.codigo_opcion IS
  'a=sin errores, b=LaTeX sin impacto funcional, c=LaTeX perjudicial, d=respuestas erradas, e=imagen/manuscrito no reconocido.';

COMMENT ON COLUMN public.app_user_feedback_report.tipo_reporte IS
  'Etiqueta estable para GROUP BY / dashboards (mapeada desde codigo_opcion).';

CREATE INDEX IF NOT EXISTS idx_app_user_feedback_created
  ON public.app_user_feedback_report (created_at DESC);

CREATE INDEX IF NOT EXISTS idx_app_user_feedback_tipo
  ON public.app_user_feedback_report (tipo_reporte);

CREATE INDEX IF NOT EXISTS idx_app_user_feedback_funcionalidad
  ON public.app_user_feedback_report (funcionalidad);

-- Inserción desde la app (PostgREST RPC + service_role).
CREATE OR REPLACE FUNCTION public.insert_user_feedback_report(
  p_funcionalidad text,
  p_codigo text
)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_code char(1);
  v_tipo text;
BEGIN
  IF p_funcionalidad IS NULL OR btrim(p_funcionalidad) = '' THEN
    RETURN;
  END IF;
  IF p_codigo IS NULL OR btrim(p_codigo) = '' THEN
    RETURN;
  END IF;

  v_code := lower(left(btrim(p_codigo), 1))::char(1);

  v_tipo := CASE v_code
    WHEN 'a' THEN 'ok_sin_incidencias'
    WHEN 'b' THEN 'latex_visual_sin_impacto_funcional'
    WHEN 'c' THEN 'latex_afecto_funcionalidad'
    WHEN 'd' THEN 'contenido_respuestas_incorrectas'
    WHEN 'e' THEN 'imagen_manuscrito_no_reconocido'
    ELSE NULL
  END;

  IF v_tipo IS NULL THEN
    RETURN;
  END IF;

  INSERT INTO public.app_user_feedback_report (funcionalidad, codigo_opcion, tipo_reporte)
  VALUES (left(btrim(p_funcionalidad), 120), v_code, v_tipo);
END;
$$;

ALTER TABLE public.app_user_feedback_report ENABLE ROW LEVEL SECURITY;

GRANT ALL ON TABLE public.app_user_feedback_report TO service_role;
GRANT EXECUTE ON FUNCTION public.insert_user_feedback_report(text, text) TO service_role;

-- Consultas útiles (SQL Editor o Metabase):
--
-- SELECT tipo_reporte, COUNT(*) AS n
-- FROM public.app_user_feedback_report
-- GROUP BY tipo_reporte
-- ORDER BY n DESC;
--
-- SELECT funcionalidad, tipo_reporte, COUNT(*) AS n
-- FROM public.app_user_feedback_report
-- GROUP BY funcionalidad, tipo_reporte
-- ORDER BY funcionalidad, n DESC;
