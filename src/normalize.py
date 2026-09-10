"""Normalizacion a escala 0-100 y agregacion en dos niveles.

Regla que atraviesa todo el modulo: **faltante nunca es cero**. Un pais sin
dato de empresas publicas no es un pais sin empresas publicas. Los NaN se
propagan y se reportan; jamas se imputan.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------
# Normalizacion
# --------------------------------------------------------------------------


def cuadratica(x: pd.Series, alpha: float = 0.03) -> pd.Series:
    """Forma funcional de Heritage: score = 100 - alpha * x^2, piso en 0.

    `x` en puntos porcentuales (14.8 para 14,8% del PBI), no en fraccion.
    Con alpha=0.03: 15% -> 93.3 | 30% -> 73.0 | 45% -> 39.3 | 58% -> 0.

    Se replica a proposito para que el pilar de extraccion sea comparable
    uno a uno contra Heritage y la diferencia de ranking se explique solo
    por los pesos y los componentes nuevos, no por la escala.
    """
    return (100.0 - alpha * x.astype(float) ** 2).clip(lower=0.0, upper=100.0)


def minmax(x: pd.Series, p_lo: float = 0.05, p_hi: float = 0.95,
           invertir: bool = True) -> pd.Series:
    """Min-max winsorizado a percentiles.

    La winsorizacion no es cosmetica: sin ella Nauru, con gasto publico de
    135% del PBI, comprime a todos los demas paises contra el techo de la
    escala y el componente deja de discriminar.
    """
    lo, hi = x.quantile(p_lo), x.quantile(p_hi)
    if not np.isfinite(lo) or not np.isfinite(hi) or hi == lo:
        return pd.Series(np.nan, index=x.index)
    z = ((x.clip(lo, hi) - lo) / (hi - lo)).clip(0, 1)
    return (1 - z) * 100 if invertir else z * 100


def lineal_invertida(x: pd.Series) -> pd.Series:
    """Para variables ya expresadas en 0-100 o en fraccion 0-1."""
    v = x.astype(float)
    if v.dropna().max() is not np.nan and v.dropna().max() <= 1.0:
        v = v * 100
    return (100.0 - v).clip(0, 100)


def escala_fija(x: pd.Series, minimo: float = 0.0, maximo: float = 10.0) -> pd.Series:
    """Reescala linealmente desde un rango conocido de la fuente a 0-100.

    Para indicadores que ya vienen acotados (Fraser usa 0-10). Usar minmax aca
    seria un error: estiraria la escala al rango observado y un pais dejaria de
    ser comparable entre vintages segun quien mas y quien menos haya salido ese
    anio.
    """
    return (100.0 * (x.astype(float) - minimo) / (maximo - minimo)).clip(0, 100)


def aplicar(x: pd.Series, spec: dict, direccion: str) -> pd.Series:
    """Despacha segun `normalizacion` del YAML. Devuelve 0-100, 100 = mas libre."""
    tipo = spec.get("tipo", "minmax")
    invertir = direccion == "menos_es_mas_libre"

    if tipo == "cuadratica":
        out = cuadratica(x, spec.get("alpha", 0.03))
        return out if invertir else 100 - out
    if tipo == "escala_fija":
        out = escala_fija(x, spec.get("min", 0.0), spec.get("max", 10.0))
        return 100 - out if invertir else out
    if tipo == "lineal_invertida":
        out = lineal_invertida(x)
        return out if invertir else 100 - out
    return minmax(x, spec.get("p_lo", 0.05), spec.get("p_hi", 0.95), invertir)


# --------------------------------------------------------------------------
# Agregacion
# --------------------------------------------------------------------------


def puntaje_pilar(scores: pd.DataFrame, pesos: dict[str, float]) -> pd.Series:
    """Promedio ponderado dentro del pilar, renormalizando por lo observado.

    Si a un pais le faltan componentes, se reparte el peso entre los que si
    tiene en lugar de imputar. Un pais con un solo componente observado da
    un numero, pero `cobertura()` lo va a marcar y el reporte lo excluye.
    """
    cols = [c for c in pesos if c in scores.columns]
    if not cols:
        return pd.Series(np.nan, index=scores.index)
    w = pd.Series({c: pesos[c] for c in cols}, dtype=float)
    sub = scores[cols].astype(float)
    w_efectivo = sub.notna().mul(w, axis=1)
    denom = w_efectivo.sum(axis=1).replace(0, np.nan)
    num = (sub.fillna(0) * w_efectivo).sum(axis=1)
    return num / denom


def cobertura(scores: pd.DataFrame, componentes: list[str]) -> pd.Series:
    """Fraccion de componentes observados por pais. Se publica junto al score."""
    cols = [c for c in componentes if c in scores.columns]
    if not cols:
        return pd.Series(0.0, index=scores.index)
    return scores[cols].notna().mean(axis=1)


def indice(pilares: pd.DataFrame, pesos_pilar: dict[str, float],
           media: str = "aritmetica") -> pd.Series:
    """Agrega pilares. `media='geometrica'` penaliza la compensacion entre ellos.

    La aritmetica deja que un pais compense propiedad estatal 20 con
    extraccion 95. La geometrica no. Es un parametro, no una decision
    escondida: el reporte publica las dos.
    """
    cols = [c for c in pesos_pilar if c in pilares.columns]
    w = pd.Series({c: pesos_pilar[c] for c in cols}, dtype=float)
    sub = pilares[cols].astype(float)
    w_ef = sub.notna().mul(w, axis=1)
    denom = w_ef.sum(axis=1).replace(0, np.nan)

    if media == "geometrica":
        logs = np.log(sub.clip(lower=1e-6))
        num = (logs.fillna(0) * w_ef).sum(axis=1)
        return np.exp(num / denom)

    num = (sub.fillna(0) * w_ef).sum(axis=1)
    return num / denom
