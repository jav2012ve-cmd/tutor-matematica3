"""
Límites y preparación de imágenes antes de enviarlas al modelo (Gemini).

Mantener alineado con `.streamlit/config.toml` → `maxUploadSize` (en MB).
"""

from __future__ import annotations

import io
from typing import Any, BinaryIO, Optional, Union

from PIL import Image, ImageOps

# Coincide con [server] maxUploadSize en .streamlit/config.toml
MAX_UPLOAD_BYTES = 12 * 1024 * 1024

# Lado largo máximo (px) para no saturar memoria ni la petición
MAX_LONG_EDGE = 2048

# Objetivo de peso tras re-codificar (JPEG)
MAX_PAYLOAD_BYTES = 4 * 1024 * 1024

JPEG_QUALITY_INICIAL = 88
JPEG_QUALITY_MIN = 50


def texto_limite_subida() -> str:
    mb = MAX_UPLOAD_BYTES // (1024 * 1024)
    return (
        f"PNG o JPG. Máximo {mb} MB por archivo. "
        "La imagen se redimensiona y comprime antes de enviarla a la IA."
    )


def _tamaño_archivo_subida(uploaded_file: Any) -> Optional[int]:
    n = getattr(uploaded_file, "size", None)
    if isinstance(n, int) and n >= 0:
        return n
    return None


def mensaje_si_archivo_muy_grande(uploaded_file: Any) -> Optional[str]:
    """Si supera MAX_UPLOAD_BYTES, mensaje de error para el usuario; si no, None."""
    if uploaded_file is None:
        return None
    size = _tamaño_archivo_subida(uploaded_file)
    if size is None:
        return None
    if size > MAX_UPLOAD_BYTES:
        max_mb = MAX_UPLOAD_BYTES / (1024 * 1024)
        return (
            f"El archivo pesa aproximadamente {size / (1024 * 1024):.1f} MB; "
            f"el máximo permitido es {max_mb:.0f} MB. Comprime la foto o elige otra imagen."
        )
    return None


def _abrir_imagen(src: Union[BinaryIO, Any]) -> Image.Image:
    if hasattr(src, "seek"):
        src.seek(0)
    img = Image.open(src)
    img.load()
    return ImageOps.exif_transpose(img)


def _a_rgb(img: Image.Image) -> Image.Image:
    if img.mode in ("RGBA", "LA"):
        fondo = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "RGBA":
            fondo.paste(img, mask=img.split()[3])
        else:
            fondo.paste(img, mask=img.split()[-1] if len(img.split()) > 1 else None)
        return fondo
    if img.mode == "P":
        return img.convert("RGBA").convert("RGB")
    if img.mode != "RGB":
        return img.convert("RGB")
    return img


def _redimensionar(img: Image.Image) -> Image.Image:
    w, h = img.size
    m = max(w, h)
    if m <= MAX_LONG_EDGE:
        return img
    scale = MAX_LONG_EDGE / m
    nw = max(1, int(w * scale))
    nh = max(1, int(h * scale))
    return img.resize((nw, nh), Image.Resampling.LANCZOS)


def _comprimir_jpeg_objetivo(img: Image.Image) -> Image.Image:
    img_work = img
    for _ in range(6):
        q = JPEG_QUALITY_INICIAL
        while q >= JPEG_QUALITY_MIN:
            buf = io.BytesIO()
            img_work.save(buf, format="JPEG", quality=q, optimize=True)
            if buf.tell() <= MAX_PAYLOAD_BYTES:
                buf.seek(0)
                out = Image.open(buf)
                out.load()
                return out.convert("RGB")
            q -= 8
        w, h = img_work.size
        if min(w, h) <= 560:
            buf = io.BytesIO()
            img_work.save(buf, format="JPEG", quality=JPEG_QUALITY_MIN, optimize=True)
            buf.seek(0)
            out = Image.open(buf)
            out.load()
            return out.convert("RGB")
        nw = max(400, int(w * 0.78))
        nh = max(400, int(h * 0.78))
        img_work = img_work.resize((nw, nh), Image.Resampling.LANCZOS)

    buf = io.BytesIO()
    img_work.save(buf, format="JPEG", quality=JPEG_QUALITY_MIN, optimize=True)
    buf.seek(0)
    out = Image.open(buf)
    out.load()
    return out.convert("RGB")


def preparar_imagen_para_ia(uploaded_file_o_pil: Union[Any, Image.Image]) -> Image.Image:
    """
    Imagen lista para `generate_content`: RGB, orientación EXIF corregida,
    lado largo acotado y JPEG re-codificado a un tamaño manejable.
    """
    if isinstance(uploaded_file_o_pil, Image.Image): 
        img = uploaded_file_o_pil.copy()
        img.load()
        img = ImageOps.exif_transpose(img)
    else:
        img = _abrir_imagen(uploaded_file_o_pil)
    img = _a_rgb(img)
    img = _redimensionar(img)
    return _comprimir_jpeg_objetivo(img)
