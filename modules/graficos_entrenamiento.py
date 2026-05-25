"""
Figuras Plotly para apoyo visual en modo entrenamiento.
Los datos vienen del banco (clave `grafico`); no se evalúa texto libre del usuario.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

import numpy as np
import plotly.graph_objects as go
import sympy as sp

_x = sp.symbols("x")
_y = sp.symbols("y")


def _lambdify_expr(expr_str: str, variable=None):
    var = variable or _x
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
    return sp.lambdify(var, e, modules=["numpy"])


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


def figura_pdf_densidad(
    f_expr: str,
    x_min: float,
    x_max: float,
    *,
    x_shade_min: Optional[float] = None,
    x_shade_max: Optional[float] = None,
    titulo: str = "",
) -> go.Figure:
    """
    Densidad f(x) ≥ 0 y sombreado opcional de P(a ≤ X ≤ b) como área bajo la curva.
    """
    if x_max <= x_min:
        x_max = x_min + 1.0
    npts = min(400, max(80, int((x_max - x_min) * 60)))
    xs = np.linspace(x_min, x_max, npts)
    fn = _lambdify_expr(f_expr)
    ys = _eval_on_grid(fn, xs)
    y_max = float(np.nanmax(ys))
    y_min = min(0.0, float(np.nanmin(ys)))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="lines",
            name="f(x) — densidad",
            line=dict(width=2.5, color="#1f77b4"),
        )
    )

    a = x_shade_min if x_shade_min is not None else x_min
    b = x_shade_max if x_shade_max is not None else x_max
    if b > a:
        mask = (xs >= a) & (xs <= b)
        xs_s = xs[mask]
        ys_s = ys[mask]
        if len(xs_s) >= 2:
            x_poly = np.concatenate([xs_s, xs_s[::-1]])
            y_poly = np.concatenate([ys_s, np.zeros_like(ys_s)[::-1]])
            fig.add_trace(
                go.Scatter(
                    x=x_poly,
                    y=y_poly,
                    fill="toself",
                    fillcolor="rgba(34, 139, 34, 0.32)",
                    line=dict(width=0),
                    name="Probabilidad (área)",
                    hoverinfo="skip",
                )
            )

    fig.update_layout(
        title=titulo or "Función de densidad de probabilidad",
        xaxis_title="x",
        yaxis_title="f(x)",
        height=440,
        margin=dict(l=48, r=24, t=56, b=48),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_yaxes(range=[y_min - 0.05 * max(y_max, 0.1), y_max * 1.15])
    fig.update_xaxes(range=[min(x_min, 0.0), x_max + 0.05 * (x_max - x_min)])
    fig.update_xaxes(
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor="#4a4a4a",
        showgrid=True,
        gridcolor="rgba(74, 74, 74, 0.25)",
    )
    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor="#4a4a4a")
    return fig


def figura_region_xy_tipo2(
    x_inferior: str,
    x_superior: str,
    y_min: float,
    y_max: float,
    titulo: str = "",
) -> go.Figure:
    """
    Región en el plano xy para integración tipo II: x_inferior(y) ≤ x ≤ x_superior(y).
    """
    if y_max <= y_min:
        y_max = y_min + 1.0
    npts = min(400, max(60, int((y_max - y_min) * 50)))
    ys = np.linspace(y_min, y_max, npts)
    fn_i = _lambdify_expr(x_inferior, _y)
    fn_s = _lambdify_expr(x_superior, _y)
    x_inf = _eval_on_grid(fn_i, ys)
    x_sup = _eval_on_grid(fn_s, ys)
    x_min_g = float(np.nanmin(np.concatenate([x_inf, x_sup])))
    x_max_g = float(np.nanmax(np.concatenate([x_inf, x_sup])))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x_sup,
            y=ys,
            mode="lines",
            name="Curva derecha (x superior)",
            line=dict(width=2, color="#1f77b4"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_inf,
            y=ys,
            mode="lines",
            name="Curva izquierda (x inferior)",
            line=dict(width=2, color="#d62728"),
        )
    )
    x_poly = np.concatenate([x_sup, x_inf[::-1]])
    y_poly = np.concatenate([ys, ys[::-1]])
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
        title=titulo or "Región de integración (tipo II)",
        xaxis_title="x",
        yaxis_title="y",
        height=440,
        margin=dict(l=48, r=24, t=56, b=48),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(range=[x_min_g - 1.0, x_max_g + 1.0])
    fig.update_yaxes(range=[min(y_min, 0.0), max(y_max, 0.0)])
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


def _lambdify_xy(expr_str: str):
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
    return sp.lambdify([_x, _y], e, modules=["numpy"])


def _eval_on_grid_xy(fn, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
    out = fn(xs, ys)
    return np.asarray(out, dtype=float)


def _mascara_region_rect(
    x: np.ndarray,
    y: np.ndarray,
    *,
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
) -> np.ndarray:
    return (x >= x_min) & (x <= x_max) & (y >= y_min) & (y <= y_max)


def _mascara_region_tipo1(
    x: np.ndarray,
    y: np.ndarray,
    *,
    y_superior_fn,
    y_inferior_fn,
    x_min: float,
    x_max: float,
) -> np.ndarray:
    y_sup = _eval_on_grid(y_superior_fn, x)
    y_inf = _eval_on_grid(y_inferior_fn, x)
    return (x >= x_min) & (x <= x_max) & (y >= y_inf) & (y <= y_sup)


def _mascara_region_tipo2(
    x: np.ndarray,
    y: np.ndarray,
    *,
    x_inferior_fn,
    x_superior_fn,
    y_min: float,
    y_max: float,
) -> np.ndarray:
    x_inf = _eval_on_grid(x_inferior_fn, y)
    x_sup = _eval_on_grid(x_superior_fn, y)
    return (y >= y_min) & (y <= y_max) & (x >= x_inf) & (x <= x_sup)


def _contorno_region_xy(spec: Dict[str, Any]) -> tuple[np.ndarray, np.ndarray]:
    """Polígono cerrado (x, y) que delimita la región en el plano xy."""
    tipo = spec.get("tipo")
    if tipo == "rectangulo" or all(k in spec for k in ("x_min", "x_max", "y_min", "y_max")):
        x0, x1 = float(spec["x_min"]), float(spec["x_max"])
        y0, y1 = float(spec["y_min"]), float(spec["y_max"])
        xs = np.array([x0, x1, x1, x0, x0])
        ys = np.array([y0, y0, y1, y1, y0])
        return xs, ys
    if tipo == "region_xy_tipo2" or all(k in spec for k in ("x_inferior", "x_superior", "y_min", "y_max")):
        y0, y1 = float(spec["y_min"]), float(spec["y_max"])
        n = min(120, max(40, int((y1 - y0) * 30)))
        ys = np.linspace(y0, y1, n)
        fn_i = _lambdify_expr(str(spec["x_inferior"]), _y)
        fn_s = _lambdify_expr(str(spec["x_superior"]), _y)
        x_inf = _eval_on_grid(fn_i, ys)
        x_sup = _eval_on_grid(fn_s, ys)
        xs = np.concatenate([x_sup, x_inf[::-1], [x_sup[0]]])
        ys_out = np.concatenate([ys, ys[::-1], [ys[0]]])
        return xs, ys_out
    if tipo == "area_entre_curvas" or all(k in spec for k in ("y_superior", "y_inferior", "x_min", "x_max")):
        x0, x1 = float(spec["x_min"]), float(spec["x_max"])
        n = min(120, max(40, int((x1 - x0) * 30)))
        xs = np.linspace(x0, x1, n)
        fn_s = _lambdify_expr(str(spec["y_superior"]))
        fn_i = _lambdify_expr(str(spec["y_inferior"]))
        y_sup = _eval_on_grid(fn_s, xs)
        y_inf = _eval_on_grid(fn_i, xs)
        xs_out = np.concatenate([xs, xs[::-1], [xs[0]]])
        ys_out = np.concatenate([y_sup, y_inf[::-1], [y_sup[0]]])
        return xs_out, ys_out
    raise ValueError("Especificación de región no reconocida para contorno 3D")


def _mascara_region_desde_spec(spec: Dict[str, Any], x: np.ndarray, y: np.ndarray) -> np.ndarray:
    tipo = spec.get("tipo")
    if tipo == "rectangulo" or all(k in spec for k in ("x_min", "x_max", "y_min", "y_max")):
        return _mascara_region_rect(
            x,
            y,
            x_min=float(spec["x_min"]),
            x_max=float(spec["x_max"]),
            y_min=float(spec["y_min"]),
            y_max=float(spec["y_max"]),
        )
    if tipo == "region_xy_tipo2" or all(k in spec for k in ("x_inferior", "x_superior", "y_min", "y_max")):
        fn_i = _lambdify_expr(str(spec["x_inferior"]), _y)
        fn_s = _lambdify_expr(str(spec["x_superior"]), _y)
        return _mascara_region_tipo2(
            x,
            y,
            x_inferior_fn=fn_i,
            x_superior_fn=fn_s,
            y_min=float(spec["y_min"]),
            y_max=float(spec["y_max"]),
        )
    if tipo == "area_entre_curvas" or all(k in spec for k in ("y_superior", "y_inferior", "x_min", "x_max")):
        fn_s = _lambdify_expr(str(spec["y_superior"]))
        fn_i = _lambdify_expr(str(spec["y_inferior"]))
        return _mascara_region_tipo1(
            x,
            y,
            y_superior_fn=fn_s,
            y_inferior_fn=fn_i,
            x_min=float(spec["x_min"]),
            x_max=float(spec["x_max"]),
        )
    raise ValueError("Especificación de región no reconocida para máscara 3D")


def _limites_region_real(spec: Dict[str, Any]) -> tuple[float, float, float, float]:
    """Caja delimitadora ajustada a la región R (sin margen visual)."""
    xs, ys = _contorno_region_xy(spec)
    return float(np.min(xs)), float(np.max(xs)), float(np.min(ys)), float(np.max(ys))


def _margen_plano_3d(x_min: float, x_max: float, y_min: float, y_max: float) -> float:
    """Unidades extra por lado para el plano base visible en la vista 3D."""
    span = max(x_max - x_min, y_max - y_min, 1e-6)
    return max(1.0, 0.15 * span)


def _limites_plano_base(
    spec: Dict[str, Any],
    *,
    margen: Optional[float] = None,
) -> tuple[float, float, float, float]:
    """Extensión del plano xy: región R más margen simétrico en x e y."""
    rx0, rx1, ry0, ry1 = _limites_region_real(spec)
    m = margen if margen is not None else _margen_plano_3d(rx0, rx1, ry0, ry1)
    return rx0 - m, rx1 + m, ry0 - m, ry1 + m


def _limites_bbox_region(spec: Dict[str, Any]) -> tuple[float, float, float, float]:
    return _limites_plano_base(spec)


def _mesh_rectangulo_xy(
    x0: float,
    x1: float,
    y0: float,
    y1: float,
    z0: float,
    *,
    color: str,
    name: str,
) -> go.Mesh3d:
    return go.Mesh3d(
        x=[x0, x1, x1, x0],
        y=[y0, y0, y1, y1],
        z=[z0, z0, z0, z0],
        i=[0, 0],
        j=[1, 2],
        k=[2, 3],
        color=color,
        name=name,
        hoverinfo="skip",
        showscale=False,
    )


def _es_figura_3d(fig: go.Figure) -> bool:
    return any(isinstance(t, (go.Surface, go.Scatter3d, go.Mesh3d)) for t in fig.data)


def _plotly_config_figura(fig: go.Figure) -> Dict[str, Any]:
    if _es_figura_3d(fig):
        return {"scrollZoom": True, "displayModeBar": True}
    return {}


def figura_integral_doble_3d(
    z_expr: str,
    region_spec: Dict[str, Any],
    *,
    titulo: str = "",
    resolucion: int = 36,
) -> go.Figure:
    """
    Superficie z = f(x,y) sobre un plano base ampliado.
    Muestra la función en un dominio mayor y destaca la porción sobre la región R.
    """
    fn_z = _lambdify_xy(z_expr)
    px0, px1, py0, py1 = _limites_plano_base(region_spec)
    nx = ny = max(32, min(resolucion, 56))
    xs = np.linspace(px0, px1, nx)
    ys = np.linspace(py0, py1, ny)
    X, Y = np.meshgrid(xs, ys)
    Z_full = _eval_on_grid_xy(fn_z, X, Y)
    mascara = _mascara_region_desde_spec(region_spec, X, Y)
    Z_sobre_r = np.where(mascara, Z_full, np.nan)

    z_min = float(np.nanmin(Z_full))
    z_max = float(np.nanmax(Z_full))
    if z_max <= z_min:
        z_max = z_min + 1.0
    z_floor = min(0.0, z_min)

    bx, by = _contorno_region_xy(region_spec)
    bz = np.full_like(bx, z_floor)

    fig = go.Figure()
    fig.add_trace(
        _mesh_rectangulo_xy(
            px0,
            px1,
            py0,
            py1,
            z_floor,
            color="rgba(200, 210, 220, 0.35)",
            name="Plano xy (referencia)",
        )
    )
    fig.add_trace(
        go.Surface(
            x=X,
            y=Y,
            z=Z_full,
            colorscale="Blues",
            showscale=False,
            opacity=0.3,
            name=f"z = {z_expr} (contexto)",
            hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<br>z=%{z:.2f}<extra></extra>",
            legendgroup="surf_ctx",
        )
    )
    fig.add_trace(
        go.Surface(
            x=X,
            y=Y,
            z=Z_sobre_r,
            colorscale="Blues",
            showscale=True,
            colorbar=dict(title="z sobre R", len=0.55, y=0.78),
            opacity=0.92,
            name="Proyección sobre R",
            hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<br>z=%{z:.2f}<extra></extra>",
            legendgroup="surf_r",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=bx,
            y=by,
            z=bz,
            mode="lines",
            line=dict(color="#d62728", width=5),
            name="Contorno de R",
            hoverinfo="skip",
        )
    )
    bx_u = bx[:-1] if len(bx) > 1 and bx[0] == bx[-1] else bx
    by_u = by[:-1] if len(by) > 1 and by[0] == by[-1] else by
    nv = len(bx_u)
    if nv >= 3:
        fig.add_trace(
            go.Mesh3d(
                x=bx_u,
                y=by_u,
                z=np.full(nv, z_floor),
                i=[0] * max(0, nv - 2),
                j=list(range(1, max(1, nv - 1))),
                k=list(range(2, max(2, nv))),
                color="rgba(255, 140, 0, 0.35)",
                name="Región R (plano xy)",
                hoverinfo="skip",
                showscale=False,
            )
        )

    fig.update_layout(
        title=titulo or f"Volumen bajo z = {z_expr}",
        height=520,
        margin=dict(l=0, r=0, t=56, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        scene=dict(
            xaxis_title="x",
            yaxis_title="y",
            zaxis_title="z",
            aspectmode="manual",
            aspectratio=dict(x=1, y=1, z=0.55),
            xaxis=dict(range=[px0, px1]),
            yaxis=dict(range=[py0, py1]),
            zaxis=dict(range=[z_floor - 0.5, z_max + 0.5]),
        ),
    )
    return fig


def _superficie_revolucion_eje_y(
    xs: np.ndarray,
    y_expr: str,
    y0: float,
    thetas: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Genera malla (X, Y, Z) al girar y = f(x) alrededor de la recta horizontal y = y0."""
    fn = _lambdify_expr(y_expr)
    y_curve = _eval_on_grid(fn, xs)
    r = y_curve[np.newaxis, :] - y0
    th = thetas[:, np.newaxis]
    x3 = np.broadcast_to(xs, r.shape)
    y3 = y0 + r * np.cos(th)
    z3 = r * np.sin(th)
    return x3, y3, z3


def _superficie_revolucion_eje_x(
    ys: np.ndarray,
    x_expr: str,
    x0: float,
    thetas: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Genera malla al girar x = g(y) alrededor de la recta vertical x = x0."""
    fn = _lambdify_expr(x_expr, _y)
    x_curve = _eval_on_grid(fn, ys)
    r = x_curve[np.newaxis, :] - x0
    th = thetas[:, np.newaxis]
    y3 = np.broadcast_to(ys, r.shape)
    x3 = x0 + r * np.cos(th)
    z3 = r * np.sin(th)
    return x3, y3, z3


def figura_solido_revolucion_2d(spec: Dict[str, Any]) -> go.Figure:
    """Región generadora en el plano xy y recta de giro."""
    eje_tipo = str(spec.get("eje_tipo", "y"))
    eje_val = float(spec["eje_val"])
    titulo = spec.get("titulo_2d") or spec.get("titulo") or "Región generadora y eje de giro"

    if eje_tipo == "x":
        fig = figura_region_xy_tipo2(
            x_inferior=str(spec["x_inferior"]),
            x_superior=str(spec["x_superior"]),
            y_min=float(spec["y_min"]),
            y_max=float(spec["y_max"]),
            titulo=titulo,
        )
        fig.add_vline(
            x=eje_val,
            line_dash="dash",
            line_color="#d62728",
            line_width=2,
            annotation_text=f"Eje x = {eje_val}",
            annotation_position="top",
        )
        return fig

    banda = {
        "y_superior": str(spec["y_superior"]),
        "y_inferior": str(spec["y_inferior"]),
        "x_min": float(spec["x_min"]),
        "x_max": float(spec["x_max"]),
    }
    fig = figura_area_entre_curvas([banda], titulo)
    fig.add_hline(
        y=eje_val,
        line_dash="dash",
        line_color="#d62728",
        line_width=2,
        annotation_text=f"Eje y = {eje_val}",
        annotation_position="right",
    )
    return fig


def figura_solido_revolucion_3d(
    spec: Dict[str, Any],
    *,
    titulo: str = "",
    resolucion: int = 40,
) -> go.Figure:
    """Sólido de revolución 3D (arandelas/discos) a partir de la región en el plano xy."""
    eje_tipo = str(spec.get("eje_tipo", "y"))
    eje_val = float(spec["eje_val"])
    n_x = max(28, min(resolucion, 50))
    n_th = max(36, min(resolucion + 8, 60))
    thetas = np.linspace(0.0, 2.0 * np.pi, n_th)

    fig = go.Figure()

    if eje_tipo == "x":
        y0, y1 = float(spec["y_min"]), float(spec["y_max"])
        ys = np.linspace(y0, y1, n_x)
        x_sup = str(spec["x_superior"])
        x_inf = str(spec["x_inferior"])
        xs_u, ys_u, zs_u = _superficie_revolucion_eje_x(ys, x_sup, eje_val, thetas)
        xs_i, ys_i, zs_i = _superficie_revolucion_eje_x(ys, x_inf, eje_val, thetas)
        x_line = [eje_val, eje_val]
        y_line = [y0, y1]
        z_line = [0.0, 0.0]
        x_rng = (
            float(np.nanmin(np.concatenate([xs_u.ravel(), xs_i.ravel()]))),
            float(np.nanmax(np.concatenate([xs_u.ravel(), xs_i.ravel()]))),
        )
        y_rng = (y0 - 0.5, y1 + 0.5)
        inf_expr = x_inf
    else:
        x0, x1 = float(spec["x_min"]), float(spec["x_max"])
        xs = np.linspace(x0, x1, n_x)
        y_sup = str(spec["y_superior"])
        y_inf = str(spec["y_inferior"])
        xs_u, ys_u, zs_u = _superficie_revolucion_eje_y(xs, y_sup, eje_val, thetas)
        xs_i, ys_i, zs_i = _superficie_revolucion_eje_y(xs, y_inf, eje_val, thetas)
        x_line = [x0, x1]
        y_line = [eje_val, eje_val]
        z_line = [0.0, 0.0]
        x_rng = (x0 - 0.5, x1 + 0.5)
        radii = np.concatenate([ys_u - eje_val, ys_i - eje_val, zs_u, zs_i])
        r_max = float(np.nanmax(np.abs(radii))) if radii.size else 1.0
        y_rng = (eje_val - r_max - 0.5, eje_val + r_max + 0.5)
        inf_expr = y_inf

    mostrar_interior = _expr_normalizada_cmp(inf_expr) != _expr_normalizada_cmp(str(eje_val))

    fig.add_trace(
        go.Surface(
            x=xs_u,
            y=ys_u,
            z=zs_u,
            colorscale="Blues",
            showscale=False,
            opacity=0.88,
            name="Superficie exterior",
            hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<br>z=%{z:.2f}<extra></extra>",
        )
    )
    if mostrar_interior:
        fig.add_trace(
            go.Surface(
                x=xs_i,
                y=ys_i,
                z=zs_i,
                colorscale="Oranges",
                showscale=False,
                opacity=0.55,
                name="Superficie interior",
                hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<br>z=%{z:.2f}<extra></extra>",
            )
        )

    fig.add_trace(
        go.Scatter3d(
            x=x_line,
            y=y_line,
            z=z_line,
            mode="lines",
            line=dict(color="#d62728", width=6),
            name="Eje de giro",
            hoverinfo="skip",
        )
    )

    z_max = float(np.nanmax(np.abs(np.concatenate([zs_u.ravel(), zs_i.ravel()]))))
    z_max = max(z_max, 0.5)

    fig.update_layout(
        title=titulo or spec.get("titulo_3d") or "Sólido de revolución",
        height=540,
        margin=dict(l=0, r=0, t=56, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        scene=dict(
            xaxis_title="x",
            yaxis_title="y",
            zaxis_title="z",
            aspectmode="cube",
            xaxis=dict(range=list(x_rng)),
            yaxis=dict(range=list(y_rng)),
            zaxis=dict(range=[-z_max - 0.3, z_max + 0.3]),
        ),
    )
    return fig


def figura_desde_spec(spec: Optional[Dict[str, Any]]) -> Optional[go.Figure]:
    if not spec:
        return None
    tipo = spec.get("tipo")
    if tipo == "solido_revolucion":
        try:
            return figura_solido_revolucion_2d(spec)
        except Exception:
            return None
    if tipo == "integral_doble_3d":
        z_expr = spec.get("z")
        region = spec.get("region") or spec
        if not z_expr:
            return None
        return figura_integral_doble_3d(
            str(z_expr),
            region,
            titulo=spec.get("titulo") or "",
            resolucion=int(spec.get("resolucion", 36)),
        )
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
    if tipo == "pdf_densidad":
        if not all(k in spec for k in ("f", "x_min", "x_max")):
            return None
        return figura_pdf_densidad(
            f_expr=str(spec["f"]),
            x_min=float(spec["x_min"]),
            x_max=float(spec["x_max"]),
            x_shade_min=spec.get("x_shade_min"),
            x_shade_max=spec.get("x_shade_max"),
            titulo=spec.get("titulo") or "",
        )
    if tipo == "region_xy_tipo2":
        if not all(k in spec for k in ("x_inferior", "x_superior")):
            return None
        return figura_region_xy_tipo2(
            x_inferior=str(spec["x_inferior"]),
            x_superior=str(spec["x_superior"]),
            y_min=float(spec.get("y_min", 0.0)),
            y_max=float(spec.get("y_max", 1.0)),
            titulo=spec.get("titulo") or "",
        )
    if tipo == "rectangulo":
        if not all(k in spec for k in ("x_min", "x_max", "y_min", "y_max")):
            return None
        banda = {
            "y_superior": str(float(spec["y_max"])),
            "y_inferior": str(float(spec["y_min"])),
            "x_min": spec["x_min"],
            "x_max": spec["x_max"],
        }
        return figura_area_entre_curvas([banda], spec.get("titulo") or "")
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


def figuras_desde_spec(spec: Optional[Dict[str, Any]]) -> List[go.Figure]:
    """
    Devuelve una o más figuras: plano 2D (si aplica) y/o vista 3D cuando hay `z`.
    """
    if not spec:
        return []
    figuras: List[go.Figure] = []
    z_expr = spec.get("z")
    tipo = spec.get("tipo")

    if tipo == "solido_revolucion":
        try:
            fig_2d = figura_solido_revolucion_2d(spec)
            fig_3d = figura_solido_revolucion_3d(
                spec,
                titulo=spec.get("titulo_3d") or "Sólido de revolución",
                resolucion=int(spec.get("resolucion", 40)),
            )
            return [fig_2d, fig_3d]
        except Exception:
            return []

    if tipo == "integral_doble_3d":
        fig = figura_desde_spec(spec)
        if fig is not None:
            figuras.append(fig)
        return figuras

    fig_2d = figura_desde_spec(spec)
    if fig_2d is not None:
        figuras.append(fig_2d)

    if z_expr and tipo in ("area_entre_curvas", "region_xy_tipo2", "rectangulo", None):
        try:
            fig_3d = figura_integral_doble_3d(
                str(z_expr),
                spec,
                titulo=spec.get("titulo_3d") or f"Volumen bajo z = {z_expr}",
                resolucion=int(spec.get("resolucion", 36)),
            )
            figuras.append(fig_3d)
        except Exception:
            pass
    return figuras


def _caption_figura_extra(spec: Dict[str, Any], indice: int, total: int) -> Optional[str]:
    if total <= 1:
        return None
    tipo = spec.get("tipo", "")
    if tipo == "solido_revolucion":
        if indice == 0:
            return "_Plano **xy**: región generadora y **eje de giro** (recta roja)._"
        if indice == 1:
            return (
                "_Sólido **3D**: superficie exterior (azul) e interior (naranja) si hay hueco. "
                "Gire con el **mouse** o acerque con la **rueda**._"
            )
    if tipo != "solido_revolucion" and indice == 1:
        return (
            "_Vista 3D: función en contexto (tenue) y porción sobre **R** resaltada. "
            "Plano base ampliado; acerque con la **rueda del mouse**._"
        )
    return None


def mostrar_figura_apoyo(
    spec: Optional[Dict[str, Any]],
    *,
    titulo: str = "Apoyo gráfico",
    caption: str = "",
) -> bool:
    """
    Render estándar del apoyo gráfico para TODAS las funcionalidades.
    Retorna True si se mostró al menos una figura, False en caso contrario.
    """
    import streamlit as st

    if not spec:
        return False
    try:
        figuras = figuras_desde_spec(spec)
        if not figuras:
            return False
        st.subheader(titulo)
        if caption:
            st.caption(caption)
        for i, fig in enumerate(figuras):
            extra = _caption_figura_extra(spec, i, len(figuras))
            if extra:
                st.caption(extra)
            st.plotly_chart(
                fig,
                width="stretch",
                key=f"plotly_apoyo_{id(spec)}_{i}",
                config=_plotly_config_figura(fig),
            )
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
        cap = (
            "Compara la región sombreada con los límites y la función que integraste "
            "tras elegir la estrategia (referencia del banco)."
        )
        if spec.get("z"):
            cap += " La vista 3D muestra la superficie z = f(x,y) sobre R."
        mostrar_figura_apoyo(
            spec,
            titulo="Apoyo gráfico — valida tu planteamiento",
            caption=cap,
        )
    else:
        mostrar_figura_apoyo(
            spec,
            titulo="Apoyo gráfico",
            caption="Misma región que el planteamiento del banco (referencia visual).",
        )


def _limpiar_expr_raw(raw: str) -> str:
    s = raw.strip().strip("$")
    s = re.sub(r"[?!.]+$", "", s).strip()
    s = re.sub(r"\s+(?:es|sea|para|en|sobre)\b.*$", "", s, flags=re.I).strip()
    return s


def _expr_generica_a_sympy(raw: str) -> str:
    """Convierte expresión legible (x^2+1, 6-x) a formato sympy."""
    s = _limpiar_expr_raw(raw).replace("^", "**")
    s = re.sub(r"\s+", "", s)
    s = re.sub(r"(\d)([xy])", r"\1*\2", s)
    s = re.sub(r"([xy])([xy])", r"\1*\2", s)
    s = re.sub(r"\*\*\*", "**", s)
    return s


def _expr_z_a_sympy(z_raw: str) -> str:
    return _expr_generica_a_sympy(z_raw)


def _texto_es_integrales_dobles(texto: Optional[str]) -> bool:
    if not texto:
        return False
    t = str(texto).lower()
    sc = re.sub(r"\s+", "", t)
    claves = (
        "integraldoble",
        "integralesdobles",
        "iint",
        "∬",
        "volumenbajo",
        "dxdy",
        "dydx",
        "dx dy",
        "dy dx",
        "regiondeintegracion",
        "limitesdeintegracion",
    )
    if any(k in sc for k in claves):
        return True
    if re.search(r"\bz\s*=", t) and any(w in t for w in ("volumen", "superficie", "plano xy", "región", "region")):
        return True
    return bool(re.search(r"\\iint|\\int_\{[^}]+\}\s*\\int", t))


def _extraer_z_desde_texto(texto: str) -> Optional[str]:
    patrones = [
        r"z\s*=\s*([^.;,\n]+?)(?=\s*(?:\.|,|;|\n|sobre|en\b|en el|en la|limitada|limitada por|$))",
        r"superficie\s+([^.;,\n]+?)(?=\s*(?:\.|,|;|\n|sobre|$))",
        r"bajo\s+(?:la\s+)?(?:superficie|función|funcion)\s+([^.;,\n]+)",
    ]
    for pat in patrones:
        m = re.search(pat, texto, re.I | re.DOTALL)
        if m:
            raw = m.group(1).strip()
            raw = re.sub(r"^\$+|\$+$", "", raw)
            if len(raw) >= 3 and re.search(r"[xy\d]", raw, re.I):
                return _expr_z_a_sympy(raw)
    return None


def _extraer_intervalo_variable(texto: str, var: str) -> Optional[tuple[float, float]]:
    """Extrae a < var < b, incluyendo el typo frecuente 3-<x<2 → -3 < x < 2."""
    v = re.escape(var)

    m = re.search(rf"(\d+)\s*-\s*<\s*{v}\s*<\s*([-\d.]+)", texto, re.I)
    if m:
        return -float(m.group(1)), float(m.group(2))

    m = re.search(rf"([-\d.]+)\s*<\s*{v}\s*<\s*([-\d.]+)", texto, re.I)
    if m:
        a, b = float(m.group(1)), float(m.group(2))
        return min(a, b), max(a, b)

    m = re.search(
        rf"{v}\s*(?:\\in|∈)\s*\[\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\]",
        texto,
        re.I,
    )
    if m:
        a, b = float(m.group(1)), float(m.group(2))
        return min(a, b), max(a, b)

    return None


def _extraer_rectangulo_desde_texto(texto: str) -> Optional[Dict[str, float]]:
    m = re.search(
        r"\[\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\]\s*[×xX\*]\s*\[\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\]",
        texto,
    )
    if not m:
        m = re.search(
            r"\[\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\]\s*por\s*\[\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\]",
            texto,
            re.I,
        )
    if m:
        return {
            "x_min": float(m.group(1)),
            "x_max": float(m.group(2)),
            "y_min": float(m.group(3)),
            "y_max": float(m.group(4)),
        }

    x_iv = _extraer_intervalo_variable(texto, "x")
    y_iv = _extraer_intervalo_variable(texto, "y")
    if x_iv and y_iv:
        return {
            "x_min": x_iv[0],
            "x_max": x_iv[1],
            "y_min": y_iv[0],
            "y_max": y_iv[1],
        }
    return None


def _expr_normalizada_cmp(expr: str) -> str:
    s = str(expr or "").lower().replace("^", "**")
    s = re.sub(r"\s+", "", s)
    s = s.replace("**", "").replace("*", "")
    return s


def _score_grafico_banco(
    item: Dict[str, Any],
    texto: Optional[str],
    tokens_match_fn,
) -> int:
    if not texto or not tokens_match_fn:
        return 0
    ref = " ".join([str(item.get("pregunta", "")), str(item.get("explicacion", ""))])
    q_tokens = tokens_match_fn(texto)
    score = len(q_tokens.intersection(tokens_match_fn(ref))) if q_tokens else 0

    g = item.get("grafico") or {}
    z_txt = _extraer_z_desde_texto(texto)
    z_bank = g.get("z")
    if z_txt and z_bank:
        if _expr_normalizada_cmp(z_txt) == _expr_normalizada_cmp(z_bank):
            score += 25
        else:
            score -= 30

    rect = _extraer_rectangulo_desde_texto(texto)
    if rect and g.get("tipo") == "rectangulo":
        tol = 0.05
        if (
            abs(float(g.get("x_min", 0)) - rect["x_min"]) <= tol
            and abs(float(g.get("x_max", 0)) - rect["x_max"]) <= tol
            and abs(float(g.get("y_min", 0)) - rect["y_min"]) <= tol
            and abs(float(g.get("y_max", 0)) - rect["y_max"]) <= tol
        ):
            score += 25

    par = _extraer_dos_curvas_y(texto)
    if par and g.get("tipo") == "area_entre_curvas":
        c1n = _expr_normalizada_cmp(par[0])
        c2n = _expr_normalizada_cmp(par[1])
        gsup = _expr_normalizada_cmp(str(g.get("y_superior", "")))
        ginf = _expr_normalizada_cmp(str(g.get("y_inferior", "")))
        if {c1n, c2n} == {gsup, ginf}:
            score += 30

    return score


def _inferido_integrales_dobles_especifico(
    spec: Optional[Dict[str, Any]],
    texto: Optional[str],
) -> bool:
    """True si el texto aportó z y región concreta (rectángulo o dos curvas)."""
    if not spec or not texto:
        return False
    if not _extraer_z_desde_texto(texto):
        return False
    if _extraer_rectangulo_desde_texto(texto):
        return True
    return _extraer_dos_curvas_y(texto) is not None


def inferir_grafico_integrales_dobles(texto: Optional[str]) -> Optional[Dict[str, Any]]:
    """
    Construye spec Plotly (2D y/o 3D) a partir del texto de una pregunta abierta
    sobre integrales dobles.
    """
    if not texto or not _texto_es_integrales_dobles(texto):
        return None

    z_expr = _extraer_z_desde_texto(texto)
    rect = _extraer_rectangulo_desde_texto(texto)
    par = _extraer_dos_curvas_y(texto)
    intervalo = _extraer_intervalo_x(texto)

    if par and z_expr:
        spec_curvas = _spec_area_entre_curvas(
            par[0],
            par[1],
            intervalo=intervalo,
            z_expr=z_expr,
            titulo="Región base entre curvas (referencia)",
        )
        if spec_curvas:
            return spec_curvas

    if not z_expr and not rect and not par:
        if _texto_es_integrales_dobles(texto):
            return {
                "tipo": "rectangulo",
                "x_min": 0.0,
                "x_max": 1.0,
                "y_min": 0.0,
                "y_max": 1.0,
                "z": "x**2 + y**2 + 1",
                "titulo": "Ejemplo: R = [0,1] × [0,1]",
                "titulo_3d": "Ejemplo: z = x² + y² + 1 sobre R",
            }
        return None

    if not rect:
        return None

    spec: Dict[str, Any] = {
        "tipo": "rectangulo",
        "x_min": rect["x_min"],
        "x_max": rect["x_max"],
        "y_min": rect["y_min"],
        "y_max": rect["y_max"],
        "titulo": (
            f"Región R = [{rect['x_min']},{rect['x_max']}] × "
            f"[{rect['y_min']},{rect['y_max']}]"
        ),
    }

    if z_expr:
        spec["z"] = z_expr
        spec["titulo_3d"] = f"Superficie z = {z_expr.replace('**', '²').replace('*', '')} sobre R"
    return spec


def _texto_es_areas(texto: Optional[str]) -> bool:
    if not texto:
        return False
    if _texto_es_integrales_dobles(texto) and _extraer_z_desde_texto(texto):
        return False
    t = str(texto).lower()
    sc = re.sub(r"\s+", "", t)
    claves = (
        "areaentre",
        "areasentre",
        "areabajo",
        "areabajodela",
        "areadefinida",
        "integradefinida",
        "areacomprendida",
        "arealimitada",
        "areade",
        "bajolacurva",
        "entrecurvas",
    )
    if any(k in sc for k in claves):
        return True
    if ("área" in t or "area" in t) and any(w in t for w in ("curva", "curvas", "encerrada", "bajo")):
        return True
    return bool(re.search(r"y\s*=\s*[^=]+y\s*=", t))


def _texto_es_probabilidad(texto: Optional[str]) -> bool:
    if not texto:
        return False
    t = str(texto).lower()
    sc = re.sub(r"\s+", "", t)
    claves = (
        "probabilidad",
        "distribucion",
        "distribución",
        "densidad",
        "pdf",
        "cdf",
        "funciondedensidad",
        "variablealeatoria",
        "suceso",
        "p(x",
        "p\\(",
    )
    if any(k in sc for k in claves):
        return True
    if re.search(r"\bf\s*\(\s*x\s*\)\s*=", t) and any(
        w in t for w in ("pdf", "densidad", "probabilidad", "distribución", "distribucion")
    ):
        return True
    return False


def _extraer_dos_curvas_y(texto: str) -> Optional[tuple[str, str]]:
    m = re.search(
        r"\by\s*=\s*(.+?)\s*,\s*y\s*=\s*(.+?)(?=\s*(?:girando|gira|en\b|[.;]|$))",
        texto,
        re.I,
    )
    if m:
        e1, e2 = _limpiar_expr_raw(m.group(1)), _limpiar_expr_raw(m.group(2))
        if e1 and e2:
            return _expr_generica_a_sympy(e1), _expr_generica_a_sympy(e2)

    matches = list(re.finditer(r"\by\s*=\s*", texto, re.I))
    exprs: List[str] = []
    for i, m in enumerate(matches):
        start = m.end()
        if i + 1 < len(matches):
            rest = texto[start: matches[i + 1].start()]
            m_delim = re.search(r"\s+y\s*$", rest, re.I)
            chunk = rest[: m_delim.start()] if m_delim else rest
        else:
            chunk = texto[start:]
        raw = _limpiar_expr_raw(chunk)
        if raw:
            exprs.append(raw)

    if len(exprs) < 2:
        m = re.search(
            r"\by\s*=\s*(.+?)\s*,\s*y\s*=\s*(.+?)(?=\s*(?:girando|gira|[.;]|$))",
            texto,
            re.I,
        )
        if m:
            e1 = _limpiar_expr_raw(m.group(1))
            e2 = _limpiar_expr_raw(m.group(2))
            if e1 and e2:
                exprs = [e1, e2]

    if len(exprs) < 2:
        m = re.search(
            r"\by\s*=\s*(.+?)\s+y\s*(?:=\s*)?([^=,\n;?.]+)",
            texto,
            re.I,
        )
        if m:
            e1 = _limpiar_expr_raw(m.group(1))
            e2 = _limpiar_expr_raw(m.group(2))
            if e1 and e2:
                exprs = [e1, e2]

    if len(exprs) < 2:
        fx_matches = list(re.finditer(r"f\s*\(\s*x\s*\)\s*=\s*", texto, re.I))
        exprs = []
        for i, m in enumerate(fx_matches):
            start = m.end()
            end = fx_matches[i + 1].start() if i + 1 < len(fx_matches) else len(texto)
            raw = _limpiar_expr_raw(texto[start:end])
            if raw:
                exprs.append(raw)

    if len(exprs) >= 2:
        return _expr_generica_a_sympy(exprs[0]), _expr_generica_a_sympy(exprs[1])
    return None


def _extraer_intervalo_x(texto: str) -> Optional[tuple[float, float]]:
    m = re.search(
        r"\[\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\]",
        texto,
    )
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(
        r"(?:entre|en|sobre)\s*\(?\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)?",
        texto,
        re.I,
    )
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(
        r"(?:entre|de)\s+([-\d.]+)\s+y\s+([-\d.]+)",
        texto,
        re.I,
    )
    if m:
        return float(m.group(1)), float(m.group(2))
    return None


def _interseccion_x_curvas(y_a: str, y_b: str) -> Optional[tuple[float, float]]:
    try:
        local = {"exp": sp.exp, "sqrt": sp.sqrt, "pi": sp.pi, "E": sp.E}
        e1 = sp.sympify(y_a.replace("^", "**"), locals=local)
        e2 = sp.sympify(y_b.replace("^", "**"), locals=local)
        sols = sp.solve(sp.Eq(e1, e2), _x)
        if not sols:
            sols = sp.solve(e1 - e2, _x)
        reales = sorted(float(s.evalf()) for s in sols if getattr(s, "is_real", True))
        if len(reales) >= 2:
            return reales[0], reales[-1]
        if len(reales) == 1:
            x0 = reales[0]
            return x0 - 1.0, x0 + 1.0
    except Exception:
        pass
    return None


def _extraer_f_pdf(texto: str) -> Optional[str]:
    patrones = [
        r"f\s*\(\s*x\s*\)\s*=\s*(.+?)(?=\s*(?:en|sobre|para|sea|es\b|\.|,|;|\n|$))",
        r"pdf\s*[:\s]+(.+?)(?=\s*(?:en|sobre|\.|,|;|\n|$))",
        r"densidad\s*[:\s]+(.+?)(?=\s*(?:en|sobre|\.|,|;|\n|$))",
    ]
    for pat in patrones:
        m = re.search(pat, texto, re.I)
        if m:
            raw = re.sub(r"^\$+|\$+$", "", m.group(1).strip())
            if len(raw) >= 2:
                expr = _expr_generica_a_sympy(raw)
                # Sustituir k simbólico por valores típicos del curso si aparece solo
                if re.search(r"\bk\b", expr, re.I):
                    if "e**(-x/2)" in expr or "exp(-x/2)" in expr:
                        expr = re.sub(r"\bk\s*\*?", "0.5*", expr, flags=re.I)
                    elif "x**2" in expr and "(1-x)" in expr:
                        expr = re.sub(r"\bk\s*\*?", "12*", expr, flags=re.I)
                    else:
                        expr = re.sub(r"\bk\s*\*?", "", expr, flags=re.I)
                return expr
    return None


def _extraer_intervalo_prob(texto: str) -> Optional[tuple[float, float]]:
    m = re.search(
        r"P\s*\(\s*([-\d.]+)\s*<\s*[xX]\s*<\s*([-\d.]+)\s*\)",
        texto,
    )
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(
        r"P\s*\(\s*[xX]\s*(?:>=|≥|<=|≤|>|<)\s*([-\d.]+)",
        texto,
    )
    if m:
        val = float(m.group(1))
        if ">=" in texto or "≥" in texto or ">" in texto:
            return val, val + 3.0
        return max(0.0, val - 3.0), val
    m = re.search(
        r"(?:probabilidad|prob(?:\.|\b)?)\s+(?:de|hay|en)?\s*(?:entre|de)\s+([-\d.]+)\s+y\s+([-\d.]+)",
        texto,
        re.I,
    )
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(
        r"(?:entre|de)\s+([-\d.]+)\s+y\s+([-\d.]+)(?!\s*\])",
        texto,
        re.I,
    )
    if m:
        return float(m.group(1)), float(m.group(2))
    return None


def _spec_area_entre_curvas(
    c1: str,
    c2: str,
    *,
    intervalo: Optional[tuple[float, float]] = None,
    z_expr: Optional[str] = None,
    titulo: str = "Área entre curvas (referencia)",
) -> Optional[Dict[str, Any]]:
    x_r = _interseccion_x_curvas(c1, c2) or intervalo
    if not x_r:
        return None
    x0, x1 = x_r
    xm = (x0 + x1) / 2.0
    try:
        f1 = _lambdify_expr(c1)
        f2 = _lambdify_expr(c2)
        if float(f1(xm)) >= float(f2(xm)):
            sup, inf = c1, c2
        else:
            sup, inf = c2, c1
    except Exception:
        sup, inf = c1, c2
    spec: Dict[str, Any] = {
        "tipo": "area_entre_curvas",
        "y_superior": sup,
        "y_inferior": inf,
        "x_min": float(x0),
        "x_max": float(x1),
        "titulo": titulo,
    }
    if z_expr:
        spec["z"] = z_expr
        spec["titulo_3d"] = (
            f"Volumen bajo z = {z_expr.replace('**', '²').replace('*', '')} sobre R"
        )
    return spec


def inferir_grafico_areas(texto: Optional[str]) -> Optional[Dict[str, Any]]:
    if not texto or not _texto_es_areas(texto):
        return None

    par = _extraer_dos_curvas_y(texto)
    intervalo = _extraer_intervalo_x(texto)

    if par:
        return _spec_area_entre_curvas(
            par[0],
            par[1],
            intervalo=intervalo,
            titulo="Área entre curvas (referencia)",
        )

    # Área bajo una curva f(x) en [a,b]
    f_pdf = _extraer_f_pdf(texto) or _extraer_z_desde_texto(texto)
    if f_pdf and intervalo:
        a, b = intervalo
        return {
            "tipo": "area_entre_curvas",
            "y_superior": f_pdf,
            "y_inferior": "0",
            "x_min": float(a),
            "x_max": float(b),
            "titulo": f"Área bajo f(x) en [{a}, {b}]",
        }

    # Ejemplo didáctico del curso
    return {
        "tipo": "area_entre_curvas",
        "y_superior": "6 - x",
        "y_inferior": "x**2",
        "x_min": -3.0,
        "x_max": 2.0,
        "titulo": "Ejemplo: área entre y = x² y y = 6 − x",
    }


def inferir_grafico_probabilidad(texto: Optional[str]) -> Optional[Dict[str, Any]]:
    if not texto or not _texto_es_probabilidad(texto):
        return None

    f_expr = _extraer_f_pdf(texto)
    intervalo = _extraer_intervalo_x(texto)
    prob = _extraer_intervalo_prob(texto)

    if f_expr:
        x_min, x_max = intervalo if intervalo else (0.0, 1.0)
        if x_min < 0 and "e**(-" in f_expr:
            x_min, x_max = 0.0, 6.0
        spec: Dict[str, Any] = {
            "tipo": "pdf_densidad",
            "f": f_expr,
            "x_min": float(x_min),
            "x_max": float(x_max),
            "titulo": "Densidad de probabilidad f(x)",
        }
        if prob:
            spec["x_shade_min"] = float(prob[0])
            spec["x_shade_max"] = float(prob[1])
        return spec

    # Ejemplos típicos del curso
    if intervalo:
        a, b = intervalo
    else:
        a, b = 0.0, 1.0
    return {
        "tipo": "pdf_densidad",
        "f": "12*x**2*(1-x)",
        "x_min": a,
        "x_max": b,
        "x_shade_min": a + 0.2 * (b - a),
        "x_shade_max": b - 0.2 * (b - a),
        "titulo": "Ejemplo: PDF f(x) = 12x²(1−x) en [0,1]",
    }


def _texto_es_volumen_revolucion(texto: Optional[str]) -> bool:
    if not texto:
        return False
    t = str(texto).lower()
    sc = re.sub(r"\s+", "", t)
    if re.search(r"\bz\s*=", t) and not any(
        k in sc for k in ("girando", "gira", "revoluc", "rotacion", "rotación", "eje")
    ):
        return False
    claves = (
        "solidoderevolucion",
        "volumenderevolucion",
        "ejedegiro",
        "ejedegiro",
    )
    if any(k in sc for k in claves):
        return True
    if any(k in t for k in ("girando", "gira", "revoluc", "rotación", "rotacion")):
        return "volumen" in t or "sólido" in t or "solido" in t or "región" in t or "region" in t
    if "volumen" in t and any(k in t for k in ("eje", "recta", "torno")):
        return True
    return False


def _extraer_eje_revolucion(texto: str) -> Optional[tuple[str, float]]:
    patrones_y = [
        r"(?:girando|gira|rot(?:a|ar)?(?:\s+torno)?(?:\s+a)?|eje(?:\s+de\s+giro)?)\s*(?:en|sobre|la\s+recta)?\s*\$?\s*y\s*=\s*([-\d.]+)",
        r"recta\s+(?:horizontal\s+)?y\s*=\s*([-\d.]+)",
    ]
    for pat in patrones_y:
        m = re.search(pat, texto, re.I)
        if m:
            return "y", float(m.group(1))
    patrones_x = [
        r"(?:girando|gira|rot(?:a|ar)?(?:\s+torno)?(?:\s+a)?|eje(?:\s+de\s+giro)?)\s*(?:en|sobre|la\s+recta)?\s*\$?\s*x\s*=\s*([-\d.]+)",
        r"recta\s+(?:vertical\s+)?x\s*=\s*([-\d.]+)",
    ]
    for pat in patrones_x:
        m = re.search(pat, texto, re.I)
        if m:
            return "x", float(m.group(1))
    return None


def _extraer_limites_x_texto(texto: str) -> Optional[tuple[float, float]]:
    patrones = [
        r"entre\s*\$?\s*x\s*=\s*([-\d.]+)\s*(?:,\s*|y\s+)\$?\s*([-\d.]+)",
        r"entre\s*\$?\s*x\s*=\s*([-\d.]+)\s*,\s*([-\d.]+)",
        r"x\s*=\s*([-\d.]+)\s*,\s*([-\d.]+)",
        r"x\s*=\s*([-\d.]+)\s+y\s+([-\d.]+)",
    ]
    for pat in patrones:
        m = re.search(pat, texto, re.I)
        if m:
            a, b = float(m.group(1)), float(m.group(2))
            return min(a, b), max(a, b)
    return None


def _extraer_limites_y_texto(texto: str) -> Optional[tuple[float, float]]:
    m = re.search(
        r"(?:entre|de)\s*\$?\s*y\s*=\s*([-\d.]+)\s*(?:,\s*|y\s+)\$?\s*([-\d.]+)",
        texto,
        re.I,
    )
    if m:
        a, b = float(m.group(1)), float(m.group(2))
        return min(a, b), max(a, b)
    return None


def _extraer_fx_desde_texto(texto: str) -> Optional[str]:
    patrones = [
        r"f\s*\(\s*x\s*\)\s*=\s*(.+?)(?=\s*(?:entre|girando|gira|en\b|\.|,|;|$))",
        r"(?:volumen|region|región)\s+(?:de|del|de la)\s*\$?\s*([^$=]+?=\s*)?(.+?)(?=\s*(?:entre|girando|gira|\.|,|$))",
    ]
    m = re.search(r"f\s*\(\s*x\s*\)\s*=\s*(.+?)(?=\s*(?:entre|girando|gira|en\b|\.|,|;|$))", texto, re.I)
    if m:
        raw = _limpiar_expr_raw(m.group(1))
        if raw:
            return _expr_generica_a_sympy(raw)
    m = re.search(r"(?:^|[,\s])y\s*=\s*(.+?)(?=\s*(?:entre|girando|gira|,|$))", texto, re.I)
    if m and "y=" not in m.group(1).lower()[:3]:
        raw = _limpiar_expr_raw(m.group(1))
        if raw and re.search(r"[x\d]", raw, re.I):
            return _expr_generica_a_sympy(raw)
    return None


def _extraer_dos_curvas_x(texto: str) -> Optional[tuple[str, str]]:
    matches = list(re.finditer(r"\bx\s*=\s*", texto, re.I))
    exprs: List[str] = []
    for i, m in enumerate(matches):
        start = m.end()
        if i + 1 < len(matches):
            rest = texto[start: matches[i + 1].start()]
            m_delim = re.search(r"\s+x\s*$", rest, re.I)
            chunk = rest[: m_delim.start()] if m_delim else rest
        else:
            chunk = texto[start:]
        raw = _limpiar_expr_raw(chunk)
        if raw:
            exprs.append(raw)
    if len(exprs) < 2:
        m = re.search(
            r"\bx\s*=\s*(.+?)\s+x\s*(?:=\s*)?([^=,\n;?.]+)",
            texto,
            re.I,
        )
        if m:
            e1, e2 = _limpiar_expr_raw(m.group(1)), _limpiar_expr_raw(m.group(2))
            if e1 and e2:
                exprs = [e1, e2]
    if len(exprs) >= 2:
        return _expr_generica_a_sympy(exprs[0]), _expr_generica_a_sympy(exprs[1])
    return None


def inferir_grafico_solido_revolucion(texto: Optional[str]) -> Optional[Dict[str, Any]]:
    if not texto or not _texto_es_volumen_revolucion(texto):
        return None

    eje = _extraer_eje_revolucion(texto)
    if not eje:
        return None
    eje_tipo, eje_val = eje

    if eje_tipo == "x":
        par = _extraer_dos_curvas_x(texto)
        intervalo = _extraer_limites_y_texto(texto) or (-2.0, 2.0)
        if not par:
            return None
        c1, c2 = par
        y0, y1 = intervalo
        ym = (y0 + y1) / 2.0
        try:
            f1 = _lambdify_expr(c1, _y)
            f2 = _lambdify_expr(c2, _y)
            if float(f1(ym)) >= float(f2(ym)):
                sup, inf = c1, c2
            else:
                sup, inf = c2, c1
        except Exception:
            sup, inf = c1, c2
        return {
            "tipo": "solido_revolucion",
            "eje_tipo": "x",
            "eje_val": float(eje_val),
            "x_superior": sup,
            "x_inferior": inf,
            "y_min": float(y0),
            "y_max": float(y1),
            "titulo_2d": f"Región generadora (giro en x = {eje_val})",
            "titulo_3d": f"Sólido al girar R en torno a x = {eje_val}",
        }

    par = _extraer_dos_curvas_y(texto)
    intervalo = _extraer_limites_x_texto(texto)
    fx = _extraer_fx_desde_texto(texto)

    if par:
        c1, c2 = par
        x_r = _interseccion_x_curvas(c1, c2) or intervalo
        if not x_r:
            return None
        x0, x1 = x_r
        xm = (x0 + x1) / 2.0
        try:
            f1 = _lambdify_expr(c1)
            f2 = _lambdify_expr(c2)
            if float(f1(xm)) >= float(f2(xm)):
                sup, inf = c1, c2
            else:
                sup, inf = c2, c1
        except Exception:
            sup, inf = c1, c2
        return {
            "tipo": "solido_revolucion",
            "eje_tipo": "y",
            "eje_val": float(eje_val),
            "y_superior": sup,
            "y_inferior": inf,
            "x_min": float(x0),
            "x_max": float(x1),
            "titulo_2d": f"Región generadora (giro en y = {eje_val})",
            "titulo_3d": f"Sólido al girar R en torno a y = {eje_val}",
        }

    if fx and intervalo:
        x0, x1 = intervalo
        y_sup, y_inf = fx, str(eje_val)
        if float(_lambdify_expr(fx)( (x0 + x1) / 2)) < eje_val:
            y_sup, y_inf = str(eje_val), fx
        return {
            "tipo": "solido_revolucion",
            "eje_tipo": "y",
            "eje_val": float(eje_val),
            "y_superior": y_sup,
            "y_inferior": y_inf,
            "x_min": float(x0),
            "x_max": float(x1),
            "titulo_2d": f"Región bajo y = f(x) (giro en y = {eje_val})",
            "titulo_3d": f"Sólido al girar f(x) en torno a y = {eje_val}",
        }

    return None


def _inferido_revolucion_especifico(spec: Optional[Dict[str, Any]], texto: Optional[str]) -> bool:
    if not spec or not texto:
        return False
    return _extraer_eje_revolucion(texto) is not None and spec.get("tipo") == "solido_revolucion"


def _buscar_grafico_en_banco(
    banco: Optional[List[Dict[str, Any]]],
    temas_prefijos: tuple[str, ...],
    texto: Optional[str],
    tokens_match_fn=None,
) -> Optional[Dict[str, Any]]:
    if not banco:
        return None
    candidatos = [
        e for e in banco
        if any(str(e.get("tema", "")).startswith(p) or p in str(e.get("tema", "")) for p in temas_prefijos)
        and isinstance(e.get("grafico"), dict)
    ]
    if not candidatos:
        return None
    if not texto or not tokens_match_fn:
        spec = dict(candidatos[0]["grafico"])
        spec.setdefault("titulo", "Referencia del banco")
        return spec
    q_tokens = tokens_match_fn(texto)
    mejor = None
    mejor_score = -1
    for c in candidatos:
        score = _score_grafico_banco(c, texto, tokens_match_fn)
        if score > mejor_score:
            mejor_score = score
            mejor = c
    if mejor is None or mejor_score <= 0:
        return None
    spec = dict(mejor["grafico"])
    spec.setdefault("titulo", "Referencia del banco")
    return spec


def resolver_grafico_tutor_abierto(
    texto: Optional[str],
    *,
    tema: Optional[str] = None,
    banco: Optional[List[Dict[str, Any]]] = None,
    tokens_match_fn=None,
) -> Optional[Dict[str, Any]]:
    """
    Elige spec Plotly para Tutor Preguntas Abiertas:
    integrales dobles, áreas, probabilidad/PDF o banco por tema.
    """
    tema_id = str(tema or "")

    inferido_rev = (
        inferir_grafico_solido_revolucion(texto)
        if _texto_es_volumen_revolucion(texto)
        else None
    )
    if inferido_rev and _inferido_revolucion_especifico(inferido_rev, texto):
        return inferido_rev

    inferido_id = (
        inferir_grafico_integrales_dobles(texto)
        if _texto_es_integrales_dobles(texto)
        else None
    )
    if inferido_id and _inferido_integrales_dobles_especifico(inferido_id, texto):
        return inferido_id

    if "1.2.5" in tema_id or _texto_es_volumen_revolucion(texto):
        spec = _buscar_grafico_en_banco(banco, ("1.2.5",), texto, tokens_match_fn)
        return spec or inferido_rev

    if "1.2.6" in tema_id or _texto_es_integrales_dobles(texto):
        spec = _buscar_grafico_en_banco(banco, ("1.2.6",), texto, tokens_match_fn)
        return spec or inferido_id

    if "1.2.7" in tema_id or _texto_es_probabilidad(texto):
        spec = _buscar_grafico_en_banco(banco, ("1.2.7", "1.2.4"), texto, tokens_match_fn)
        return spec or inferir_grafico_probabilidad(texto)

    if any(t in tema_id for t in ("1.2.2", "1.2.1")) or _texto_es_areas(texto):
        spec = _buscar_grafico_en_banco(banco, ("1.2.2", "1.2.1"), texto, tokens_match_fn)
        return spec or inferir_grafico_areas(texto)

    if "1.2.3" in tema_id:
        return _buscar_grafico_en_banco(banco, ("1.2.3",), texto, tokens_match_fn)

    if tema_id and tokens_match_fn is not None:
        from . import temario as _temario

        if _temario.tema_admite_grafico_plotly_entrenamiento(tema_id):
            return _buscar_grafico_en_banco(banco, (tema_id[:5],), texto, tokens_match_fn)

    if _texto_es_probabilidad(texto):
        return inferir_grafico_probabilidad(texto)
    if _texto_es_areas(texto):
        return inferir_grafico_areas(texto)
    if _texto_es_integrales_dobles(texto):
        return inferir_grafico_integrales_dobles(texto)
    if _texto_es_volumen_revolucion(texto):
        return inferir_grafico_solido_revolucion(texto)
    return None


def _caption_tutor_abierto(spec: Dict[str, Any]) -> str:
    tipo = spec.get("tipo", "")
    if tipo == "solido_revolucion":
        return (
            "Región generadora en el plano **xy** (con el **eje de giro**) y sólido **3D** "
            "formado al rotar la región. Gire la vista con el mouse."
        )
    if spec.get("z"):
        return (
            "Región R en el plano **xy** y superficie **z = f(x,y)** sobre R "
            "(referencia visual para tu consulta)."
        )
    if tipo == "pdf_densidad":
        if spec.get("x_shade_min") is not None:
            return (
                "Densidad **f(x)** y área sombreada = probabilidad del intervalo indicado "
                "(referencia visual)."
            )
        return "Función de densidad de probabilidad **f(x)** (referencia visual)."
    if tipo in ("area_entre_curvas", "rectangulo", "region_xy_tipo2"):
        return "Región sombreada = área / región de integración (referencia visual)."
    if tipo == "excedentes":
        return "Demanda, oferta y excedentes (referencia visual)."
    return "Figura de referencia para reforzar la explicación."


def _titulo_tutor_abierto(spec: Dict[str, Any]) -> str:
    tipo = spec.get("tipo", "")
    if tipo == "solido_revolucion":
        return "📊 Apoyo gráfico — sólidos de revolución"
    if spec.get("z") or tipo == "integral_doble_3d":
        return "📊 Apoyo gráfico — integrales dobles"
    if tipo == "pdf_densidad":
        return "📊 Apoyo gráfico — probabilidad y densidad"
    if tipo in ("area_entre_curvas", "rectangulo", "region_xy_tipo2"):
        return "📊 Apoyo gráfico — áreas y regiones"
    if tipo == "excedentes":
        return "📊 Apoyo gráfico — excedentes"
    return "📊 Apoyo gráfico del tema consultado"


def mostrar_apoyo_tutor_abierto(
    texto: Optional[str],
    *,
    tema: Optional[str] = None,
    banco: Optional[List[Dict[str, Any]]] = None,
    tokens_match_fn=None,
    chart_key: str = "",
) -> bool:
    """Muestra figuras Plotly en Preguntas Abiertas (áreas, probabilidad, integrales dobles, etc.)."""
    import streamlit as st

    spec = resolver_grafico_tutor_abierto(
        texto,
        tema=tema,
        banco=banco,
        tokens_match_fn=tokens_match_fn,
    )
    if not spec:
        return False

    try:
        figuras = figuras_desde_spec(spec)
        if not figuras:
            return False
        st.markdown(f"#### {_titulo_tutor_abierto(spec)}")
        st.caption(_caption_tutor_abierto(spec))
        base_key = chart_key or str(abs(hash(str(spec))) % 10**8)
        for i, fig in enumerate(figuras):
            extra = _caption_figura_extra(spec, i, len(figuras))
            if extra:
                st.caption(extra)
            st.plotly_chart(
                fig,
                width="stretch",
                key=f"plotly_tutor_{base_key}_{i}",
                config=_plotly_config_figura(fig),
            )
        return True
    except Exception:
        st.caption("_No se pudo generar la figura para esta consulta._")
        return False


def mostrar_apoyo_tutor_abierto_integrales_dobles(
    texto: Optional[str],
    *,
    tema: Optional[str] = None,
    banco: Optional[List[Dict[str, Any]]] = None,
    tokens_match_fn=None,
    chart_key: str = "",
) -> bool:
    """Compatibilidad: delega al motor unificado de Preguntas Abiertas."""
    return mostrar_apoyo_tutor_abierto(
        texto,
        tema=tema,
        banco=banco,
        tokens_match_fn=tokens_match_fn,
        chart_key=chart_key,
    )
