-- Ejecutar en Supabase → SQL Editor (una sola vez por proyecto).
-- Los contadores sobreviven al reinicio / "sueño" de Streamlit Cloud.

CREATE TABLE IF NOT EXISTS public.app_module_usage (
  module text PRIMARY KEY,
  count bigint NOT NULL DEFAULT 0 CHECK (count >= 0)
);

COMMENT ON TABLE public.app_module_usage IS 'Contadores anónimos de uso por modo (Streamlit tutor Mate III).';

-- Incremento atómico (evita condiciones de carrera entre instancias).
CREATE OR REPLACE FUNCTION public.increment_module_usage(p_module text)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  IF p_module IS NULL OR btrim(p_module) = '' THEN
    RETURN;
  END IF;
  INSERT INTO public.app_module_usage (module, count)
  VALUES (btrim(p_module), 1)
  ON CONFLICT (module)
  DO UPDATE SET count = public.app_module_usage.count + 1;
END;
$$;

-- La app Streamlit debe usar la clave service_role (solo en servidor / Secrets).
-- Con esa clave, PostgREST ignora RLS para operaciones del backend.
-- Con la clave `anon` y RLS sin políticas SELECT, la API puede devolver [] (vacío)
-- con HTTP 200 — el panel admin se ve vacío sin error evidente.
ALTER TABLE public.app_module_usage ENABLE ROW LEVEL SECURITY;

GRANT USAGE ON SCHEMA public TO service_role;
GRANT ALL ON TABLE public.app_module_usage TO service_role;
GRANT EXECUTE ON FUNCTION public.increment_module_usage(text) TO service_role;
