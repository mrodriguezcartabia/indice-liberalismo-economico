"""Pipeline: panel tidy -> normalización -> pilares -> vintage.

    python src/build.py --config config/heritage.yaml
    python src/build.py --config config/z.yaml

Diferencias con la versión anterior:
  - conserva TODOS los años en lugar de quedarse con el último
  - los títulos y notas del config son bilingües {es, en}
  - vuelca `fuentes.json`, que es lo que lee el panel de escrutinio de la app

Salidas en data/vintages/<carpeta>/:
    panel.csv       valores crudos por país, serie y año
    scores.csv      componentes normalizados 0-100, por país y año
    indice.csv      pilares + índice + cobertura + ranking, por país y año
    fuentes.json    procedencia completa, para el panel de escrutinio
    validacion.json resultado del test de réplica
    config.yaml     copia congelada de la configuración usada
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import normalize as nz  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"
VINTAGES = RAIZ / "data" / "vintages"


def txt(valor, idioma: str = "es") -> str:
    """Devuelve la variante de idioma de un campo bilingüe {es, en}."""
    if isinstance(valor, dict):
        return str(valor.get(idioma) or valor.get("es") or next(iter(valor.values()), ""))
    return "" if valor is None else str(valor)


def cargar_config(path: Path) -> dict:
    """Los componentes se ponderan por PUNTOS, no por porcentaje.

    El peso de un componente es sus puntos sobre el total. El peso de un pilar
    no se declara: es la suma de los puntos de sus componentes. Esa es
    exactamente la mecánica del índice original, y dejarla a la vista es parte
    de lo que la página muestra.
    """
    cfg = yaml.safe_load(path.read_text(encoding="utf-8"))
    total = sum(c.get("puntos", 0) for c in cfg["componentes"].values())
    if total <= 0:
        raise SystemExit("Ningún componente tiene puntos asignados.")
    cfg["_puntos_totales"] = total
    return cfg


def series_del_config(cfg: dict) -> set[str]:
    """Todas las series que este índice usa, incluidas las sólo reportadas."""
    s = {v.get("serie", k) for k, v in cfg["componentes"].items()}
    s |= set((cfg.get("solo_reportadas") or {}).keys())
    for c in (cfg.get("eje_cumplimiento") or {}).get("componentes", []):
        s.add(c["serie"])
    return s


def cargar_panel(series: set[str] | None = None) -> pd.DataFrame:
    """Une los CSV crudos en un panel tidy. Conserva todos los años.

    `data/raw/manual/` es un pozo común: pueden convivir series de varias
    fuentes. Si no se filtra por las que el config declara, un índice hereda
    los años de otro y aparecen años enteros sin ningún dato propio.
    """
    partes = []
    for csv in sorted(RAW.rglob("*.csv")):
        try:
            df = pd.read_csv(csv)
        except Exception as e:                                   # noqa: BLE001
            print(f"  ! {csv.name}: {e}")
            continue
        if {"iso3", "serie", "anio", "valor"}.issubset(df.columns):
            df = df[["iso3", "serie", "anio", "valor"]]
            if series is not None:
                df = df[df["serie"].isin(series)]
            if len(df):
                partes.append(df)
        else:
            print(f"  ! {csv.name}: faltan columnas, se omite")
    if not partes:
        raise SystemExit(
            "No hay datos en data/raw/.\n"
            "Cargá las fuentes con src/cargar.py (ver docs/FUENTES.md).")
    panel = pd.concat(partes, ignore_index=True).dropna(subset=["iso3", "valor"])
    return panel.drop_duplicates(["iso3", "serie", "anio"], keep="last")


def construir(cfg: dict, panel: pd.DataFrame) -> dict:
    comps = cfg["componentes"]
    idx = ["iso3", "anio"]
    # --- alinear series rezagadas al año del vintage ------------------------
    # Una fuente puede terminar antes que el índice (Fraser llega a 2023 y
    # Heritage a 2026). En ese caso se usa la última observación disponible y
    # se declara de qué año es. No es imputación: es un dato real con su fecha
    # a la vista. El propio Heritage trabaja con datos rezagados respecto de su
    # edición.
    rezagos = {}
    vintage = int(cfg["meta"]["vintage"])
    for nombre, spec in comps.items():
        if not spec.get("alinear_al_vintage"):
            continue
        serie = spec.get("serie", nombre)
        sub = panel[panel["serie"] == serie]
        if sub.empty or vintage in sub["anio"].values:
            continue
        ult = sub.sort_values("anio").groupby("iso3", as_index=False).last()
        rezagos[nombre] = {
            "anio_dato": int(ult["anio"].max()),
            "anio_asignado": vintage,
            "paises": int(len(ult)),
        }
        ult["anio"] = vintage
        panel = pd.concat([panel, ult[["iso3", "serie", "anio", "valor"]]],
                          ignore_index=True)
        print(f"  · {nombre}: último dato {rezagos[nombre]['anio_dato']} "
              f"alineado a {vintage} ({len(ult)} países)")

    ancho = panel.pivot_table(index=idx, columns="serie", values="valor",
                              aggfunc="last")

    # --- normalizar cada componente ---------------------------------------
    scores = pd.DataFrame(index=ancho.index)
    cobertura_comp = []
    for nombre, spec in comps.items():
        serie = spec.get("serie", nombre)
        if serie not in ancho.columns:
            scores[nombre] = float("nan")
            print(f"  - {nombre}: sin datos ({serie}) -> NaN, nunca cero")
        else:
            scores[nombre] = nz.aplicar(ancho[serie], spec["normalizacion"],
                                        spec["direccion"])
        cobertura_comp.append({
            "componente": nombre,
            "titulo_es": txt(spec.get("titulo"), "es"),
            "observados": int(scores[nombre].notna().sum()),
        })

    # --- doble conteo ------------------------------------------------------
    correlaciones = []
    for pil in cfg["pilares"]:
        cols = [n for n, s in comps.items()
                if s["pilar"] == pil and scores[n].notna().sum() > 10]
        if len(cols) > 1:
            m = scores[cols].astype(float).corr()
            for i, a in enumerate(cols):
                for b in cols[i + 1:]:
                    correlaciones.append({"pilar": pil, "a": a, "b": b,
                                          "r": round(float(m.loc[a, b]), 3)})
    for c in correlaciones:
        if abs(c["r"]) > 0.7:
            print(f"  ! doble conteo: {c['a']} y {c['b']} r={c['r']} en {c['pilar']}")

    # --- índice: promedio ponderado por puntos sobre los componentes -------
    total_pts = cfg["_puntos_totales"]
    pesos_comp = {n: s.get("puntos", 0) / total_pts for n, s in comps.items()}

    pilares = pd.DataFrame(index=scores.index)
    for pil in cfg["pilares"]:
        dentro = {n: s.get("puntos", 0) for n, s in comps.items()
                  if s["pilar"] == pil}
        suma = sum(dentro.values())
        pilares[pil] = (nz.puntaje_pilar(scores,
                                         {n: v / suma for n, v in dentro.items()})
                        if suma else pd.Series(float("nan"), index=scores.index))

    ind = pd.DataFrame(index=scores.index)
    ind["indice"] = nz.puntaje_pilar(scores, pesos_comp)
    # La cobertura se mide sólo sobre los componentes que pesan: un país no
    # debe quedar fuera del ranking por no tener un dato que el índice no usa.
    con_peso = [n for n, sp in comps.items() if sp.get("puntos", 0) > 0]
    ind["cobertura"] = nz.cobertura(scores, con_peso or list(comps))
    ind = ind.join(pilares)

    # --- eje del gráfico de dispersión, fuera del puntaje ------------------
    eje = cfg.get("eje_cumplimiento")
    if eje:
        partes, pesos = [], []
        for c in eje["componentes"]:
            if c["serie"] in ancho.columns:
                partes.append(nz.aplicar(ancho[c["serie"]], c["normalizacion"],
                                         c["direccion"]))
                pesos.append(c.get("peso", 1.0))
        if partes:
            m = pd.concat(partes, axis=1)
            m.columns = range(len(partes))
            w = pd.Series(pesos, index=m.columns, dtype=float)
            wef = m.notna().mul(w, axis=1)
            ind["cumplimiento"] = ((m.fillna(0) * wef).sum(axis=1)
                                   / wef.sum(axis=1).replace(0, float("nan")))

    # --- publicable y ranking, calculados POR AÑO --------------------------
    ind["publicable"] = ind["cobertura"] >= cfg["meta"]["cobertura_minima"]
    ind = ind.reset_index()
    ind["ranking"] = (ind.where(ind["publicable"])
                        .groupby("anio")["indice"]
                        .rank(ascending=False, method="min"))

    # --- validación contra el puntaje publicado, si existe -----------------
    validacion = {"disponible": False}
    ref = next((s.get("columna") or s.get("serie")
                for s in (cfg.get("solo_reportadas") or {}).values()), None)
    ref_serie = next(iter((cfg.get("solo_reportadas") or {}).keys()), None)
    if ref_serie and ref_serie in ancho.columns:
        cmp_ = ind.set_index(idx).join(ancho[[ref_serie]]).dropna(
            subset=["indice", ref_serie])
        if len(cmp_):
            dif = (cmp_["indice"] - cmp_[ref_serie]).abs()
            validacion = {
                "disponible": True, "serie_referencia": ref_serie,
                "paises_comparados": int(len(cmp_)),
                "diferencia_media": round(float(dif.mean()), 4),
                "diferencia_maxima": round(float(dif.max()), 4),
                "cierra": bool(dif.max() < 0.5),
            }
            estado = "OK" if validacion["cierra"] else "NO CIERRA"
            print(f"  validación: dif. máx {validacion['diferencia_maxima']} "
                  f"en {validacion['paises_comparados']} obs. -> {estado}")

    return {"rezagos": rezagos,
            "panel": ancho.reset_index(), "scores": scores.reset_index(),
            "indice": ind, "cobertura": pd.DataFrame(cobertura_comp),
            "correlaciones": pd.DataFrame(correlaciones),
            "validacion": validacion}


def volcar_fuentes(cfg: dict, validacion: dict, rezagos: dict | None = None) -> dict:
    """Arma el JSON de procedencia que consume el panel de escrutinio.

    Se genera DESDE el config, nunca se escribe al lado. Si mañana cambia un
    coeficiente y la explicación no se regenera, la página mentiría sobre sí
    misma; generándola así, eso no puede pasar.
    """
    return {
        "meta": cfg["meta"],
        "validacion": validacion,
        "rezagos": rezagos or {},
        "presets": cfg.get("presets", {}),
        "puntos_totales": cfg["_puntos_totales"],
        "pilares": {k: {"titulo": v.get("titulo"),
                        "descripcion": v.get("descripcion")}
                    for k, v in cfg["pilares"].items()},
        "componentes": {
            k: {"pilar": v["pilar"], "puntos": v.get("puntos", 0),
                "peso_total": round(v.get("puntos", 0) / cfg["_puntos_totales"], 6),
                "titulo": v.get("titulo"), "definicion": v.get("definicion"),
                "subfactores": v.get("subfactores"),
                "superpone_con": v.get("superpone_con"),
                "significa_100": v.get("significa_100"),
                "externo": bool(v.get("externo")),
                "formula": v.get("formula"), "fuente": v.get("fuente"),
                "reproducible": v.get("reproducible"),
                "normalizacion": v.get("normalizacion"),
                "direccion": v.get("direccion")}
            for k, v in cfg["componentes"].items()},
        "eje_cumplimiento": cfg.get("eje_cumplimiento"),
        "externo_puntos_cero": [k for k, v in cfg["componentes"].items()
                                if v.get("externo")],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()

    ruta = Path(args.config)
    cfg = cargar_config(ruta)
    print(f"\n{cfg['meta']['sigla']} — {txt(cfg['meta']['nombre'])}")

    salidas = construir(cfg, cargar_panel(series_del_config(cfg)))

    destino = VINTAGES / cfg["meta"]["carpeta"]
    destino.mkdir(parents=True, exist_ok=True)
    for nombre in ("panel", "scores", "indice", "cobertura", "correlaciones"):  # noqa
        salidas[nombre].to_csv(destino / f"{nombre}.csv", index=False)
    (destino / "fuentes.json").write_text(
        json.dumps(volcar_fuentes(cfg, salidas["validacion"], salidas["rezagos"]),
                   indent=2, ensure_ascii=False), encoding="utf-8")
    (destino / "validacion.json").write_text(
        json.dumps(salidas["validacion"], indent=2, ensure_ascii=False),
        encoding="utf-8")
    shutil.copy(ruta, destino / "config.yaml")

    ind = salidas["indice"]
    anios = sorted(ind["anio"].dropna().unique())
    print(f"  observaciones: {len(ind)}   países: {ind.iso3.nunique()}")
    if anios:
        print(f"  años: {int(min(anios))}–{int(max(anios))}")
    print(f"  publicables: {int(ind['publicable'].sum())}")
    print(f"  -> {destino}\n")


if __name__ == "__main__":
    main()
