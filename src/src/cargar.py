"""Convierte cualquier planilla descargada al formato del indice.

Toda fuente manual termina siendo lo mismo: bajaste un Excel o un CSV con los
paises en una columna y el dato en otra, y hay que dejarlo como
`iso3,serie,anio,valor`. Este script hace esa traduccion y te avisa que nombres
de pais no pudo resolver, en vez de perderlos en silencio.

Se usa en dos pasos.

1) Mirar que tiene el archivo (hojas y columnas):

    python src/cargar.py inspeccionar ~/Descargas/bos_database.xlsx

2) Convertir, nombrando las columnas que viste en el paso 1:

    python src/cargar.py convertir ~/Descargas/bos_database.xlsx \
        --pais "Country Name" \
        --valor "SOE assets (% GDP)" \
        --serie soe_assets_gdp \
        --anio 2023

El resultado se escribe en data/raw/manual/<serie>.csv y ya lo levanta build.py.

Opciones utiles:
    --hoja "Table 2"     si el Excel tiene varias hojas
    --col-anio "year"    si el anio esta en una columna en vez de ser fijo
    --escala 100         multiplica los valores (para pasar 0.37 -> 37.0)
    --saltar 3           ignora las primeras 3 filas (encabezados decorativos)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from countries import is_aggregate, to_iso3  # noqa: E402

MANUAL = Path(__file__).resolve().parents[1] / "data" / "raw" / "manual"


def _leer(path: Path, hoja=None, saltar: int = 0) -> pd.DataFrame:
    if path.suffix.lower() in (".xlsx", ".xls", ".xlsm"):
        return pd.read_excel(path, sheet_name=hoja if hoja is not None else 0,
                             skiprows=saltar)
    sep = "\t" if path.suffix.lower() in (".tsv", ".txt") else ","
    return pd.read_csv(path, sep=sep, skiprows=saltar, low_memory=False)


def detectar_encabezado(path: Path, hoja=None, maximo: int = 12) -> int:
    """Encuentra en que fila esta el encabezado real.

    Muchas planillas oficiales arrancan con filas de titulo y logo. Si pandas
    las toma como encabezado, las columnas quedan como 'Unnamed: 78' y no hay
    forma de nombrarlas. Probamos saltar de 0 a `maximo` filas y nos quedamos
    con la opcion donde mas columnas tienen nombre de verdad.
    """
    mejor, mejor_puntaje = 0, -1.0
    for n in range(maximo + 1):
        try:
            df = _leer(path, hoja, n).head(5)
        except Exception:                            # noqa: BLE001
            continue
        if df.empty or len(df.columns) < 2:
            continue
        con_nombre = sum(1 for c in df.columns
                         if not str(c).startswith("Unnamed:")
                         and not str(c).strip().isdigit())
        puntaje = con_nombre / len(df.columns)
        if puntaje > mejor_puntaje:
            mejor, mejor_puntaje = n, puntaje
        if puntaje == 1.0:
            break
    return mejor


def crudo(path: Path, hoja=None, filas: int = 8, columnas: int = 8) -> None:
    """Imprime las primeras filas sin interpretar ninguna como encabezado."""
    if path.suffix.lower() in (".xlsx", ".xls", ".xlsm"):
        df = pd.read_excel(path, sheet_name=hoja if hoja is not None else 0,
                           header=None, nrows=filas)
    else:
        df = pd.read_csv(path, header=None, nrows=filas, low_memory=False)
    print("Primeras filas sin encabezado (el numero de la izquierda es la fila):\n")
    for i, (_, fila) in enumerate(df.head(filas).iterrows()):
        celdas = [str(v)[:22] for v in fila.head(columnas).tolist()]
        print(f"  fila {i}: {celdas}")
    print("\nSi el encabezado esta en la 'fila 4', usa --saltar 4")


def inspeccionar(path: Path, hoja=None, saltar: int | None = None) -> None:
    """Muestra hojas, columnas y una muestra. Siempre corre esto primero."""
    if saltar is None:
        saltar = detectar_encabezado(path, hoja)
        if saltar:
            print(f">>> Encabezado detectado en la fila {saltar}. "
                  f"AGREGA --saltar {saltar} a TODOS los comandos siguientes.\n")
        saltar = saltar
    if path.suffix.lower() in (".xlsx", ".xls", ".xlsm"):
        hojas = pd.ExcelFile(path).sheet_names
        print(f"Hojas ({len(hojas)}): {hojas}\n")

    df = _leer(path, hoja, saltar)
    print(f"Filas: {len(df)}   Columnas: {len(df.columns)}\n")
    print("Columnas disponibles:")
    for c in df.columns:
        muestra = df[c].dropna().head(3).tolist()
        print(f"  {c!r:<45} ej: {muestra}")

    # Adivina cual es la columna de paises: la que mas nombres resuelve a ISO3.
    mejor, tasa_mejor = None, 0.0
    for c in df.columns:
        if df[c].dtype == object or pd.api.types.is_string_dtype(df[c]):
            tasa = df[c].dropna().head(80).map(
                lambda v: to_iso3(v) is not None).mean()
            if tasa > tasa_mejor:
                mejor, tasa_mejor = c, tasa
    if mejor and tasa_mejor > 0.5:
        print(f"\nColumna de paises probable: {mejor!r} "
              f"({tasa_mejor:.0%} resuelve a ISO3)")


def convertir(path: Path, col_pais: str, col_valor: str, serie: str,
              anio: int | None = None, col_anio: str | None = None,
              hoja=None, saltar: int = 0, escala: float = 1.0,
              salida: Path | None = None) -> pd.DataFrame:
    df = _leer(path, hoja, saltar)

    faltan = [c for c in (col_pais, col_valor) if c not in df.columns]
    if faltan:
        sugerido = detectar_encabezado(path, hoja)
        extra = ""
        if sugerido and sugerido != saltar:
            extra = (f"\n\nProbablemente te falta --saltar {sugerido}: "
                     f"el encabezado no esta en la primera fila.")
        raise SystemExit(
            f"No existe la columna {faltan[0]!r}.{extra}\n\n"
            f"Corre: python src/cargar.py inspeccionar {path}")

    out = pd.DataFrame()
    out["iso3"] = df[col_pais].map(to_iso3)
    out["serie"] = serie
    out["anio"] = df[col_anio] if col_anio else (anio or pd.Timestamp.today().year)
    out["valor"] = pd.to_numeric(df[col_valor], errors="coerce") * escala

    # Reporte de lo que se pierde. Nunca se descarta en silencio.
    sin_iso = df.loc[out["iso3"].isna(), col_pais].dropna().unique()
    reales = [n for n in sin_iso if not is_aggregate(n)]
    if reales:
        print(f"\n{len(reales)} nombres sin ISO3 (NO entraron al indice):")
        for n in reales[:25]:
            print(f"   - {n}")
        if len(reales) > 25:
            print(f"   ... y {len(reales) - 25} mas")
        print("   Si son paises reales, agregalos al diccionario EN o ES "
              "de src/countries.py")
    if len(sin_iso) > len(reales):
        print(f"   ({len(sin_iso) - len(reales)} agregados regionales "
              f"descartados, correcto)")

    sin_valor = int(out["valor"].isna().sum())
    if sin_valor:
        print(f"{sin_valor} filas sin valor numerico -> descartadas "
              f"(faltante nunca es cero)")

    out = out.dropna(subset=["iso3", "valor"])
    # Se conservan TODOS los anios: la serie temporal es parte del producto.
    # Solo se descartan duplicados exactos de pais-serie-anio.
    out = (out.sort_values("anio")
              .drop_duplicates(["iso3", "serie", "anio"], keep="last"))

    destino = salida or (MANUAL / f"{serie}.csv")
    destino.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(destino, index=False)

    anios = sorted(out["anio"].dropna().unique())
    tramo = (f"  anios {int(anios[0])}-{int(anios[-1])}" if len(anios) > 1 else "")
    print(f"\n{out['iso3'].nunique()} paises, {len(out)} observaciones{tramo}"
          f" -> {destino}")
    print(f"   rango: {out['valor'].min():.2f} a {out['valor'].max():.2f}   "
          f"mediana: {out['valor'].median():.2f}")
    print("\nSi el rango te parece raro, revisa --escala "
          "(el indice espera puntos porcentuales: 37.0, no 0.37)")
    print("Ahora corre: python src/build.py")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    i = sub.add_parser("inspeccionar", help="ver hojas y columnas del archivo")
    i.add_argument("archivo")
    i.add_argument("--hoja", default=None)
    i.add_argument("--saltar", type=int, default=None,
                   help="filas a ignorar; si no lo pasas, se detecta solo")
    i.add_argument("--crudo", action="store_true",
                   help="ver las primeras filas sin interpretar encabezado")

    c = sub.add_parser("convertir", help="pasar al formato del indice")
    c.add_argument("archivo")
    c.add_argument("--pais", required=True, help="columna con el nombre del pais")
    c.add_argument("--valor", default=None, help="columna con el dato")
    c.add_argument("--serie", default=None, help="nombre de serie en index.yaml")
    c.add_argument("--anio", type=int, default=None)
    c.add_argument("--col-anio", default=None)
    c.add_argument("--hoja", default=None)
    c.add_argument("--saltar", type=int, default=0)
    c.add_argument("--escala", type=float, default=1.0)
    c.add_argument("--varios", nargs="+", default=None,
                   help='varias columnas de un saque: "Columna=serie" "Otra=serie2". '
                        'Reemplaza a --valor y --serie.')

    a = ap.parse_args()
    hoja = a.hoja
    if hoja is not None and str(hoja).isdigit():
        hoja = int(hoja)

    if a.cmd == "inspeccionar":
        ruta = Path(a.archivo).expanduser()
        if a.crudo:
            crudo(ruta, hoja)
        else:
            inspeccionar(ruta, hoja, a.saltar)
    else:
        ruta = Path(a.archivo).expanduser()
        if a.varios:
            for par in a.varios:
                if "=" not in par:
                    raise SystemExit(f'Formato invalido: {par!r}. Usa "Columna=serie".')
                col, serie = par.rsplit("=", 1)
                print(f"\n=== {serie} ===")
                convertir(ruta, a.pais, col, serie, a.anio, a.col_anio,
                          hoja, a.saltar, a.escala)
        else:
            convertir(ruta, a.pais, a.valor, a.serie,
                      a.anio, a.col_anio, hoja, a.saltar, a.escala)


if __name__ == "__main__":
    main()
