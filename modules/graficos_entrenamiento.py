"""
Figuras Plotly para apoyo visual en modo entrenamiento.
Los datos vienen del banco (clave `grafico`); no se evalúa texto libre del usuario.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

import numpy as np
import plotly.graph_objects as go
import sympy as sp

_x = sp.symbols("x")


def _lambdify_expr(expr_str: str):
    s = expr_str.strip().replace("^", "**")
    local = {
        "exp": sp.exp,
        "E": sp.E,
        "log": sp.log,
        "ln": sp.log,
        "sqrt": sp.sqrt,
        "pi": sp.pi,
        "sin": sp.sin,
        "cos": sp.cos,
        "tan": sp.tan,
    }
    e = sp.sympify(s, locals=local)
    return sp.lambdify(_x, e, modules=["numpy"])


def _eval_on_grid(fn, xs: np.ndarray) -> np.ndarray:
    ys = fn(xs)
    if np.isscalar(ys) or ys.shape == ():
        ys = np.full_like(xs, float(ys), dtype=float)
    return np.asarray(ys, dtype=float)


def figura_area_entre_curvas(
    bandas: List[Dict[str, Any]],
    titulo: str = "",
) -> go.Figure:
    fig = go.Figure()
    y_min_global = None
    y_max_global = None
    x_min_global = None
    x_max_global = None
    for k, b in enumerate(bandas):
        ys = str(b["y_superior"])
        yi = str(b["y_inferior"])
        x0, x1 = float(b["x_min"]), float(b["x_max"])
        if x1 <= x0:
            continue
        x_min_global = x0 if x_min_global is None else min(x_min_global, x0)
        x_max_global = x1 if x_max_global is None else max(x_max_global, x1)
        npts = min(400, max(60, int((x1 - x0) * 50)))
        xs = np.linspace(x0, x1, npts)
        fn_s = _lambdify_expr(ys)
        fn_i = _lambdify_expr(yi)
        sup = _eval_on_grid(fn_s, xs)
        infy = _eval_on_grid(fn_i, xs)
        y_local_min = float(np.nanmin(np.concatenate([sup, infy])))
        y_local_max = float(np.nanmax(np.concatenate([sup, infy])))
        y_min_global = y_local_min if y_min_global is None else min(y_min_global, y_local_min)
        y_max_global = y_local_max if y_max_global is None else max(y_max_global, y_local_max)

        lab_s = f"Arriba ({k + 1})" if len(bandas) > 1 else "Curva superior"
        lab_i = f"Abajo ({k + 1})" if len(bandas) > 1 else "Curva inferior"
        fig.add_trace(
            go.Scatter(
                x=xs,
                y=sup,
                mode="lines",
                name=lab_s,
                line=dict(width=2, color="#1f77b4"),
                legendgroup=f"g{k}s",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=xs,
                y=infy,
                mode="lines",
                name=lab_i,
                line=dict(width=2, color="#d62728"),
                legendgroup=f"g{k}i",
            )
        )
        x_poly = np.concatenate([xs, xs[::-1]])
        y_poly = np.concatenate([sup, infy[::-1]])
        fig.add_trace(
            go.Scatter(
                x=x_poly,
                y=y_poly,
                fill="toself",
                fillcolor="rgba(100, 149, 237, 0.28)",
                line=dict(width=0),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    fig.update_layout(
        title=titulo or "Área entre curvas",
        xaxis_title="x",
        yaxis_title="y",
        height=440,
        margin=dict(l=48, r=24, t=56, b=48),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    if y_min_global is not None and y_max_global is not None:
        fig.update_yaxes(range=[y_min_global - 2.0, y_max_global + 2.0])
    if x_min_global is not None and x_max_global is not None:
        fig.update_xaxes(range=[min(x_min_global, 0.0), max(x_max_global, 0.0)])
    fig.update_xaxes(
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor="#4a4a4a",
        showgrid=True,
        gridcolor="rgba(74, 74, 74, 0.25)",
        gridwidth=1,
    )
    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor="#4a4a4a")
    return fig


def figura_excedentes(
    demanda: str,
    oferta: str,
    q_min: float,
    q_max: float,
    titulo: str = "",
) -> go.Figure:
    if q_max <= q_min:
        q_max = q_min + 1.0

    qs = np.linspace(q_min, q_max, 220)
    f_d = _lambdify_expr(demanda)
    f_o = _lambdify_expr(oferta)
    p_d = _eval_on_grid(f_d, qs)
    p_o = _eval_on_grid(f_o, qs)
    p_eq = float(_eval_on_grid(f_d, np.array([q_max]))[0])
    y_min = float(np.nanmin(np.concatenate([p_d, p_o, np.array([p_eq])])))
    y_max = float(np.nanmax(np.concatenate([p_d, p_o, np.array([p_eq])])))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=qs,
            y=p_d,
            mode="lines",
            name="Demanda",
            line=dict(width=2, color="#1f77b4"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=qs,
            y=p_o,
            mode="lines",
            name="Oferta",
            line=dict(width=2, color="#d62728"),
        )
    )

    # EC: área entre demanda y línea horizontal de precio de equilibrio
    x_ec = np.concatenate([qs, qs[::-1]])
    y_ec = np.concatenate([p_d, np.full_like(qs, p_eq)[::-1]])
    fig.add_trace(
        go.Scatter(
            x=x_ec,
            y=y_ec,
            fill="toself",
            fillcolor="rgba(34, 139, 34, 0.28)",
            line=dict(width=0),
            name="Excedente del consumidor (EC)",
            hoverinfo="skip",
        )
    )

    # EP: área entre precio de equilibrio y oferta
    x_ep = np.concatenate([qs, qs[::-1]])
    y_ep = np.concatenate([np.full_like(qs, p_eq), p_o[::-1]])
    fig.add_trace(
        go.Scatter(
            x=x_ep,
            y=y_ep,
            fill="toself",
            fillcolor="rgba(255, 140, 0, 0.30)",
            line=dict(width=0),
            name="Excedente del productor (EP)",
            hoverinfo="skip",
        )
    )

    fig.add_hline(y=p_eq, line_dash="dash", line_color="gray", opacity=0.9)
    fig.add_vline(x=q_max, line_dash="dot", line_color="gray", opacity=0.6)
    fig.add_trace(
        go.Scatter(
            x=[q_max],
            y=[p_eq],
            mode="markers",
            marker=dict(size=8, color="black"),
            name="Equilibrio",
        )
    )

    fig.update_layout(
        title=titulo or "Excedente del consumidor y del productor",
        xaxis_title="Cantidad",
        yaxis_title="Precio",
        height=440,
        margin=dict(l=48, r=24, t=56, b=48),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_yaxes(range=[y_min - 2.0, y_max + 2.0])
    fig.update_xaxes(range=[min(q_min, 0.0), max(q_max, 0.0)])
    fig.update_xaxes(
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor="#4a4a4a",
        showgrid=True,
        gridcolor="rgba(74, 74, 74, 0.25)",
        gridwidth=1,
    )
    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor="#4a4a4a")
    return fig


def figura_desde_spec(spec: Optional[Dict[str, Any]]) -> Optional[go.Figure]:
    if not spec:
        return None
    tipo = spec.get("tipo")
    if tipo == "excedentes":
        if not all(k in spec for k in ("demanda", "oferta", "q_max")):
            return None
        return figura_excedentes(
            demanda=str(spec["demanda"]),
            oferta=str(spec["oferta"]),
            q_min=float(spec.get("q_min", 0.0)),
            q_max=float(spec["q_max"]),
            titulo=spec.get("titulo") or "",
        )
    if tipo != "area_entre_curvas":
        return None
    titulo = spec.get("titulo") or ""
    if "bandas" in spec:
        bandas = spec["bandas"]
        if not bandas:
            return None
        return figura_area_entre_curvas(bandas, titulo)
    if all(k in spec for k in ("y_superior", "y_inferior", "x_min", "x_max")):
        banda = {
            "y_superior": spec["y_superior"],
            "y_inferior": spec["y_inferior"],
            "x_min": spec["x_min"],
            "x_max": spec["x_max"],
        }
        return figura_area_entre_curvas([banda], titulo)
    return None


def mostrar_figura_apoyo(
    spec: Optional[Dict[str, Any]],
    *,
    titulo: str = "Apoyo gráfico",
    caption: str = "",
) -> bool:
    """
    Render estándar del apoyo gráfico para TODAS las funcionalidades.
    Retorna True si se mostró la figura, False en caso contrario.
    """
    import streamlit as st

    if not spec:
        return False
    try:
        fig = figura_desde_spec(spec)
        if fig is None:
            return False
        st.subheader(titulo)
        if caption:
            st.caption(caption)
        st.plotly_chart(fig, use_container_width=True)
        return True
    except Exception:
        st.caption("_No se pudo generar la figura para este ítem._")
        return False


def mostrar_si_aplica(
    ejercicio: Dict[str, Any],
    *,
    en_paso_intermedio: bool = False,
) -> None:
    """Si el ejercicio trae `grafico` y el tema admite figura, muestra Plotly."""
    import streamlit as st

    from . import temario

    tema = ejercicio.get("tema")
    if not temario.tema_admite_grafico_plotly_entrenamiento(tema):
        return
    spec = ejercicio.get("grafico")
    if not spec:
        return
    if en_paso_intermedio:
        mostrar_figura_apoyo(
            spec,
            titulo="Apoyo gráfico — valida tu planteamiento",
            caption=(
                "Compara la región sombreada con los límites y la función que integraste "
                "tras elegir la estrategia (referencia del banco)."
            ),
        )
    else:
        mostrar_figura_apoyo(
            spec,
            titulo="Apoyo gráfico",
            caption="Misma región que el planteamiento del banco (referencia visual).",
        )
