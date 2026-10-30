"""Descarga automática de series desde la fuente original.

Cada fuente baja de la API oficial del organismo que produce el dato, no de
sitios que lo recopilan: así cada serie tiene una sola definición y un año
explícito por país. El resultado queda en data/raw/manual/<serie>.csv con el
mismo formato que el resto (`iso3,serie,anio,valor`) y build.py lo levanta.

    python src/descargar.py              # todas las fuentes
    python src/descargar.py ocde_presion_fiscal heritage

Fuentes:
    ocde_presion_fiscal  Recaudación tributaria total del gobierno general,
                         incluidas contribuciones a la seguridad social, % del
                         PBI. OCDE, Global Revenue Statistics Database.
    fmi_gasto_publico    Gasto total del gobierno general, % del PBI. FMI,
                         World Economic Outlook. Solo años con dato observado:
                         las proyecciones se descartan.
    heritage             Los doce componentes y el puntaje total del Index of
                         Economic Freedom, ediciones `meta.ediciones_desde` a
                         `meta.vintage` del config.
                         Si Heritage ya publicó la edición siguiente, avisa:
                         pasar a una edición nueva cambia la fecha de corte y
                         la cita de la fuente, así que no se hace solo.

Fraser no está: su sitio no permite descargas automáticas. Se carga a mano con
cargar.py siguiendo docs/CARGAR_FRASER.md.
"""

from __future__ import annotations

import argparse
import io
import os
import re
import sys
import tempfile
from pathlib import Path

import pandas as pd
import requests
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cargar import convertir  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
DESTINO = RAIZ / "data" / "raw" / "manual"
CONFIG = RAIZ / "config" / "heritage.yaml"
# Se identifica como lo que es. Si una fuente bloquea descargas automáticas
# (como Fraser), se respeta y esa fuente se carga a mano con cargar.py.
CABECERAS = {"User-Agent": "indice-liberalismo-economico/1.0 "
                           "(+https://github.com/mrodriguezcartabia/indice-liberalismo-economico)"}

URL_OCDE = ("https://sdmx.oecd.org/public/rest/data/"
            "OECD.CTP.TPS,DSD_REV_COMP_GLOBAL@DF_RSGLOBAL,/"
            ".TAX_REV.S13._T._T.PT_B1GQ.A")
# El FMI usa códigos propios para dos países; el resto del proyecto usa ISO3.
FMI_A_ISO3 = {"KOS": "XKX", "WBG": "PSE"}

URL_FMI = ("https://api.imf.org/external/sdmx/2.1/data/"
           "IMF.RES,WEO/*.GGX_NGDP.A")

URL_HERITAGE = ("https://static.heritage.org/index/data/{a}/"
                "{a}_indexofeconomicfreedom_data.xlsx")
# Ediciones anteriores a 2024: sus direcciones están en el config
# (meta.fuente.urls_ediciones_viejas), que también las usa para citarlas.
# Columna del Excel de Heritage -> serie. Cada edición escribe algunos nombres
# a su manera (y con erratas: "Judicial Efectiveness", "Monitary Freedom",
# "Judical Effectiveness"); se acepta cualquiera de las grafías conocidas.
# "{a} Score" es el puntaje total en las ediciones viejas.
HERITAGE = {("Property Rights",): "hf_property_rights",
            ("Judicial Effectiveness", "Judicial Efectiveness",
             "Judical Effectiveness"): "hf_judicial_effectiveness",
            ("Government Integrity", "Govt Integrity"): "hf_government_integrity",
            ("Tax Burden",): "hf_tax_burden",
            ("Government Spending", "Gov't Spending"): "hf_government_spending",
            ("Fiscal Health",): "hf_fiscal_health",
            ("Business Freedom",): "hf_business_freedom",
            ("Labor Freedom",): "hf_labor_freedom",
            ("Monetary Freedom", "Monitary Freedom"): "hf_monetary_freedom",
            ("Trade Freedom",): "hf_trade_freedom",
            ("Investment Freedom",): "hf_investment_freedom",
            ("Financial Freedom",): "hf_financial_freedom",
            ("Overall Score", "{a} Score"): "hf_overall",
            ("World Rank",): "hf_puesto"}
# Columnas que no todas las ediciones traen: si faltan, esa edición no la aporta.
HERITAGE_OPCIONALES = {"hf_puesto"}


def _get(url: str, accept: str = "*/*") -> requests.Response:
    r = requests.get(url, headers={**CABECERAS, "Accept": accept}, timeout=300)
    r.raise_for_status()
    return r


def _csv(url: str, accept: str) -> pd.DataFrame:
    return pd.read_csv(io.StringIO(_get(url, accept).text), low_memory=False)


def ocde_presion_fiscal() -> None:
    d = _csv(URL_OCDE, "application/vnd.sdmx.data+csv")
    d = d[d["REF_AREA"].str.fullmatch(r"[A-Z]{3}")]      # fuera agregados (A9, OECD...)
    guardar("ocde_presion_fiscal",
            pd.DataFrame({"iso3": d["REF_AREA"], "anio": d["TIME_PERIOD"],
                          "valor": d["OBS_VALUE"]}))


def fmi_gasto_publico() -> None:
    d = _csv(URL_FMI, "application/vnd.sdmx.data+csv;version=1.0.0")
    d = d[d["COUNTRY"].str.fullmatch(r"[A-Z]{3}")]       # fuera agregados (G001...)
    anio = d["TIME_PERIOD"].astype(str).str[:4].astype(int)
    # "2025" o "FY2024/25": el primer año es el último cerrado con dato observado.
    ultimo = d["LATEST_ACTUAL_ANNUAL_DATA"].astype(str).map(
        lambda s: int(m.group()) if (m := re.search(r"\d{4}", s)) else -1)
    d = d[anio <= ultimo]
    guardar("fmi_gasto_publico",
            pd.DataFrame({"iso3": d["COUNTRY"].replace(FMI_A_ISO3),
                          "anio": anio[d.index], "valor": d["OBS_VALUE"]}))


def heritage() -> None:
    """Todas las ediciones desde `ediciones_desde` hasta `meta.vintage`.

    Cada edición se guarda con su año. Las que Heritage ya no deja bajar
    automáticamente se avisan y se cargan a mano.
    """
    meta = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))["meta"]
    vintage = int(meta["vintage"])
    partes = {serie: [] for serie in HERITAGE.values()}
    fuentes_usadas = {}
    with tempfile.TemporaryDirectory() as tmp:
        for anio in range(int(meta.get("ediciones_desde", vintage)), vintage + 1):
            viejas = meta["fuente"].get("urls_ediciones_viejas") or {}
            urls = [URL_HERITAGE.format(a=anio)] + ([viejas[anio]] if anio in viejas else [])
            for url in urls:
                r = requests.get(url, headers=CABECERAS, timeout=300)
                if r.status_code == 200 and not r.headers.get("content-type", "").startswith("text/html"):
                    break
            else:
                print(f"  ! heritage {anio}: no se pudo bajar de ninguna dirección")
                continue
            xlsx = Path(tmp) / f"heritage_{anio}{Path(url).suffix}"
            xlsx.write_bytes(r.content)
            hoja = pd.ExcelFile(xlsx).sheet_names[0]
            # Las ediciones nuevas traen un rótulo arriba del encabezado; las viejas, no.
            saltar = next(n for n in (0, 1, 2) if {"Country", "Country Name"} &
                          set(pd.read_excel(xlsx, sheet_name=hoja, skiprows=n, nrows=0).columns))
            cols = list(pd.read_excel(xlsx, sheet_name=hoja, skiprows=saltar, nrows=0).columns)
            limpias = {str(c).strip(): c for c in cols}
            col_pais = limpias.get("Country") or limpias["Country Name"]
            for nombres, serie in HERITAGE.items():
                col = next((limpias[n.format(a=anio)] for n in nombres
                            if n.format(a=anio) in limpias), None)
                if col is None and serie in HERITAGE_OPCIONALES:
                    continue
                if col is None:
                    raise ValueError(f"heritage {anio}: falta la columna {nombres[0]}")
                csv = Path(tmp) / f"{serie}_{anio}.csv"
                convertir(xlsx, col_pais, col, serie, anio=anio, hoja=hoja,
                          saltar=saltar, salida=csv)
                partes[serie].append(pd.read_csv(csv))
            fuentes_usadas[anio] = url
            print(f"  · heritage: edición {anio} <- {url}")
    for serie, dfs in partes.items():
        if dfs:
            guardar(serie, pd.concat(dfs)[["iso3", "anio", "valor"]])

    siguiente = vintage + 1
    r = requests.head(URL_HERITAGE.format(a=siguiente), headers=CABECERAS,
                      timeout=60, allow_redirects=True)
    if r.status_code == 200:
        print(f"  ! Heritage publicó la edición {siguiente}: cargarla a mano "
              f"(cambia meta.vintage, la fecha de corte y la cita).")
        if salida := os.environ.get("GITHUB_OUTPUT"):
            with open(salida, "a", encoding="utf-8") as fh:
                fh.write(f"heritage_nueva={siguiente}\n")


FUENTES = {"ocde_presion_fiscal": ocde_presion_fiscal,
           "fmi_gasto_publico": fmi_gasto_publico,
           "heritage": heritage}


def guardar(serie: str, df: pd.DataFrame) -> Path:
    df = df.dropna(subset=["valor"]).assign(serie=serie)
    df["anio"] = df["anio"].astype(int)
    df = df[["iso3", "serie", "anio", "valor"]].sort_values(["anio", "iso3"])
    destino = DESTINO / f"{serie}.csv"
    df.to_csv(destino, index=False)
    ult = df.sort_values("anio").groupby("iso3").anio.last()
    print(f"  · {serie}: {df.iso3.nunique()} países, {df.anio.min()}–{df.anio.max()}, "
          f"último dato más común {ult.mode().iat[0]} -> {destino.relative_to(RAIZ)}")
    return destino


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fuentes", nargs="*",
                    help=f"fuentes a bajar (por defecto, todas): {', '.join(FUENTES)}")
    args = ap.parse_args()
    if desconocidas := set(args.fuentes) - set(FUENTES):
        ap.error(f"fuentes desconocidas: {', '.join(sorted(desconocidas))}")
    # Una fuente caída no frena a las demás, pero el error no se esconde: el
    # script termina con código 1 y GitHub lo reporta.
    fallidas = []
    for nombre in args.fuentes or FUENTES:
        try:
            FUENTES[nombre]()
        except Exception as e:
            fallidas.append(nombre)
            print(f"  ✗ {nombre}: {type(e).__name__}: {e}", file=sys.stderr)
    if fallidas:
        sys.exit(f"Fallaron: {', '.join(fallidas)}")


if __name__ == "__main__":
    main()
