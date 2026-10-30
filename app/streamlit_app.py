"""Página pública: el índice de Heritage, y qué pasa cuando se lo repondera.

    streamlit run app/streamlit_app.py

Diseño:
  - barra lateral -> texto introductorio y los componentes en puntos, con su
    definición al pasar el mouse. Es lo que define qué es el índice.
  - pantalla principal -> selector de índice, controles de vista en
    horizontal y ranking.
  - columna derecha -> idioma, razones, cómo funciona, tutorial, código de
    configuración y PDF.
  - cualquier cambio de puntos convierte el índice activo en "Índice propio".

Los pesos se asignan en PUNTOS por componente, no en porcentajes. El peso de un
componente es sus puntos sobre el total, y el de un pilar es la suma de los
puntos de sus componentes: no se pondera aparte. Esa es la mecánica del índice
de Heritage, y dejarla a la vista es parte de lo que la página muestra.

La app no descarga ni recalcula desde las fuentes: lee los vintages congelados
que produce src/build.py.
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

import codigo as cod           # noqa: E402
import normalize as nz         # noqa: E402
from countries import nombre   # noqa: E402
from i18n import t, txt        # noqa: E402

st.set_page_config(page_title=t("titulo_pestana", st.session_state.get("lang", "es")),
                   layout="wide", initial_sidebar_state="expanded")

# ---------------------------------------------------------------------------
# IMPORTANTE: sin líneas en blanco ni comentarios CSS. Streamlit divide el
# markdown en cada línea vacía, cierra el <style> por su cuenta y el resto se
# imprime como texto. Por eso además se usa st.html().
# Las ventanas del "?" (stTooltipContent) solo cambian de color: Streamlit
# calcula su tamaño, y cambiarles letra, márgenes o alto desarma el recuadro.
# ---------------------------------------------------------------------------
CSS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;800&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{--fondo:#2E2C36;--panel:#383641;--panel2:#42404C;--tinta:#F0EDF6;
--tenue:#BAB6C6;--gris-pop:#55525F;--acento:#D3C5FF;--sobre-acento:#2A2440;--violeta:#9A8DBF;
--violeta2:#5A566B;--alerta:#E39A8C;--linea:#47444F;--pista:#211F28;}
.stApp{background:var(--fondo);}
html,body,[class*="css"]{font-family:'Archivo',system-ui,sans-serif;
color:var(--tinta);font-size:16px;line-height:1.62;}
h1,h2,h3,h4{font-family:'Archivo',sans-serif;font-weight:800;letter-spacing:-.02em;color:var(--tinta);}
h1{font-size:2.1rem;line-height:1.05;margin:.1rem 0 .3rem;}
h1 em{font-style:normal;color:var(--acento);}
.bajada{color:var(--tinta);font-size:.98rem;line-height:1.65;opacity:.9;}
.bajada .mas{color:var(--acento);font-weight:600;}
.cab{display:grid;grid-template-columns:2.5rem 10.5rem 1fr 4rem 3.6rem 3.6rem;gap:.5rem;
white-space:nowrap;font-family:'IBM Plex Mono',monospace;font-size:.62rem;
color:var(--tenue);
padding-bottom:.35rem;border-bottom:1px solid var(--violeta2);}
.fila{display:grid;grid-template-columns:2.5rem 10.5rem 1fr 4rem 3.6rem 3.6rem;gap:.5rem;
align-items:center;padding:.26rem 0;border-bottom:1px solid var(--linea);}
.pos,.val,.vs{font-family:'IBM Plex Mono',monospace;font-size:.86rem;}
.pos{color:var(--tenue);font-weight:600;}
.val{text-align:right;font-weight:600;color:var(--acento);}
.vs{text-align:right;color:var(--tenue);font-size:.76rem;}
.pais{font-size:.92rem;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.barra{display:flex;height:14px;background:var(--pista);border-radius:2px;}
.seg{height:100%;transition:width .28s cubic-bezier(.4,0,.2,1);min-width:0;position:relative;}
.seg:first-child{border-radius:2px 0 0 2px;}
.seg .segpop{display:none;position:absolute;bottom:calc(100% + 6px);left:50%;transform:translateX(-50%);
white-space:nowrap;z-index:1000;padding:.3rem .55rem;border-radius:4px;background:var(--gris-pop);
border:1px solid var(--linea);color:var(--tinta);font-family:'Archivo',system-ui,sans-serif;
font-size:.76rem;line-height:1.38;box-shadow:0 6px 18px rgba(0,0,0,.35);pointer-events:none;}
.seg:hover .segpop{display:block;}
.sube{color:var(--acento);font-weight:600;}
.baja{color:var(--alerta);font-weight:600;}
.seguido{background:rgba(154,130,201,.15);margin:0 -.4rem;padding:.26rem .4rem;border-radius:3px;}
.seguido .pais{color:var(--acento);}
.corte{font-family:'IBM Plex Mono',monospace;font-size:.7rem;
color:var(--tenue);margin:1rem 0 .3rem;}
.nota{font-size:.86rem;color:var(--tinta);opacity:.85;
border-left:2px solid var(--violeta);padding-left:.75rem;margin:.6rem 0;
line-height:1.6;}
.aviso{font-size:.9rem;color:var(--alerta);border-left:2px solid var(--alerta);
padding-left:.75rem;margin:.6rem 0;line-height:1.5;}
.paso{font-family:'IBM Plex Mono',monospace;font-size:.8rem;padding:.3rem 0;
border-bottom:1px dotted var(--linea);color:var(--tinta);}
.etq{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:.62rem;
padding:.1rem .45rem;border-radius:3px;
border:1px solid var(--linea);color:var(--tenue);}
.etq.ok{border-color:var(--acento);color:var(--acento);}
.etq.no{border-color:var(--alerta);color:var(--alerta);}
.chip{width:9px;height:9px;border-radius:2px;display:inline-block;
margin-right:.4rem;flex:0 0 auto;}
.wrow{font-size:.86rem;cursor:default;border-radius:3px;padding:.15rem .3rem;
margin:0 -.3rem;transition:background .15s;position:relative;}
.wrow:hover{background:rgba(211,197,255,.14);}
.wrow .pop{display:none;position:absolute;left:0;top:100%;z-index:1000;width:100%;
min-width:12rem;margin-top:.25rem;padding:.45rem .6rem;border-radius:4px;
background:var(--gris-pop);border:1px solid var(--linea);color:var(--tinta);
font-size:.76rem;line-height:1.38;box-shadow:0 6px 18px rgba(0,0,0,.35);
pointer-events:none;}
.wrow:hover .pop{display:block;}
.wrow .pop100{display:block;margin-top:.35rem;color:var(--acento);}
[data-testid="stNumberInputStepUp"],[data-testid="stNumberInputStepDown"]{display:none !important;}
@media (min-width:640px){
[data-testid="stColumn"]:has(.marca-der){flex:0 0 max-content !important;width:max-content !important;max-width:none !important;}
[data-testid="stColumn"]:has(.marca-der) [data-testid="stElementContainer"]:not(:has(button)){width:0 !important;min-width:100% !important;}
[data-testid="stColumn"]:has(.marca-der) button p{white-space:nowrap;}
[data-testid="stHorizontalBlock"]:has(.marca-der) > [data-testid="stColumn"]:not(:has(.marca-der)){flex:1 1 0 !important;min-width:0 !important;width:auto !important;}
}
[data-testid="stDialog"] :is([data-testid="stCaptionContainer"],[data-testid="stCaptionContainer"] *,.nota,.sfn,.sfpeso,.refrow,.refnum,.etq,.tabcab,.tabcab *,.tabnum,.pil,.pil *,[data-testid="stMetricLabel"] *,[data-baseweb="tab"] p,[data-testid="stExpander"] summary *,[data-testid="stWidgetLabel"] *,[data-testid="stTable"] *,[data-testid="stProgress"] *,[data-testid="stAlertContentInfo"] *,[data-testid="stAlertContentWarning"] *,small){font-size:1rem !important;}
[data-testid="stTooltipContent"]{background-color:var(--gris-pop) !important;color:var(--tinta) !important;
border:1px solid var(--linea);box-shadow:0 6px 18px rgba(0,0,0,.35) !important;}
[data-testid="stTooltipContent"] *{color:var(--tinta) !important;}
.wrow.arriba .pop{top:auto;bottom:100%;margin-top:0;margin-bottom:.25rem;}
[data-testid="stSidebarUserContent"] [data-testid="stLayoutWrapper"]:has(.wrow:hover),
[data-testid="stSidebarUserContent"] [data-testid="stVerticalBlock"]:has(.wrow:hover),
[data-testid="stSidebarUserContent"] [data-testid="stHorizontalBlock"]:has(.wrow:hover),
[data-testid="stSidebarUserContent"] [data-testid="stColumn"]:has(.wrow:hover),
[data-testid="stSidebarUserContent"] [data-testid="stElementContainer"]:has(.wrow:hover),
[data-testid="stSidebarUserContent"] [data-testid="stMarkdownContainer"]:has(.wrow:hover)
{position:relative;z-index:1000;overflow:visible;}
.wrow .sfn{display:block;margin-left:1.3rem;color:var(--tenue);font-size:.72rem;}
.pil{display:grid;grid-template-columns:1fr 3.6rem;gap:.5rem;font-size:.86rem;
padding:.22rem 0;border-bottom:1px solid var(--linea);}
.pil b{font-family:'IBM Plex Mono',monospace;text-align:right;color:var(--acento);}
.tabcab{display:grid;grid-template-columns:11rem 1fr 12rem 4rem;gap:.8rem;
font-family:'IBM Plex Mono',monospace;font-size:.7rem;
color:var(--tenue);padding-bottom:.3rem;
border-bottom:1px solid var(--violeta2);}
.tabrow{display:grid;grid-template-columns:11rem 1fr 12rem 4rem;gap:.8rem;
padding:.55rem 0;border-bottom:1px solid var(--linea);font-size:.87rem;
line-height:1.45;align-items:start;}
.tabnum{font-family:'IBM Plex Mono',monospace;text-align:right;color:var(--acento);}
.tabpil{font-weight:800;font-size:.8rem;margin:.9rem 0 .1rem;color:var(--violeta);}
.sfrow{display:grid;grid-template-columns:14rem 1fr 7rem;gap:.8rem;align-items:center;
padding:.32rem 0;border-bottom:1px solid var(--linea);font-size:.85rem;}
.sfbar{display:flex;height:19px;gap:2px;}
.sfseg{background:var(--violeta);height:100%;border-radius:2px;}
.sfpeso{font-family:'IBM Plex Mono',monospace;font-size:.76rem;text-align:right;color:var(--acento);}
.sfn{font-size:.72rem;color:var(--tenue);}
.pista-ayuda{font-size:.78rem;color:var(--tenue);margin:-.1rem 0 .6rem;}
a.ref{color:var(--acento);text-decoration:none;font-weight:600;}
.refrow{display:grid;grid-template-columns:2.2rem 1fr;gap:.5rem;
padding:.28rem 0;border-bottom:1px solid var(--linea);font-size:.84rem;}
.refnum{font-family:'IBM Plex Mono',monospace;color:var(--acento);}
.refrow a{color:var(--tinta);text-decoration:none;}
a.mas{color:var(--acento);font-weight:600;text-decoration:none;}
a.mas:hover{text-decoration:underline;}
details.mastxt{display:block;}
details.mastxt summary{display:block;list-style:none;pointer-events:none;}
details.mastxt summary::-webkit-details-marker{display:none;}
details.mastxt summary::marker{content:"";}
details.mastxt .resto{display:none;}
details.mastxt[open] .resto{display:inline;}
details.mastxt .mas,details.mastxt .menos{color:var(--acento);font-weight:600;
cursor:pointer;pointer-events:auto;}
details.mastxt .mas:hover,details.mastxt .menos:hover{text-decoration:underline;}
details.mastxt .menos{display:none;}
details.mastxt[open] .mas{display:none;}
details.mastxt[open] .menos{display:inline;}
details.mastxt a{pointer-events:auto;}
.formula{font-size:1.12em;color:inherit;}
@keyframes destello{0%,100%{box-shadow:0 0 0 0 rgba(211,197,255,0);}
50%{box-shadow:0 0 0 4px rgba(211,197,255,.35);}}
.destello .stButton button{animation:destello 2.6s ease-in-out 0s 15;
border-color:var(--acento) !important;}
[data-testid="stSidebar"]{background:var(--panel);border-right:1px solid var(--linea);}
.txtmas [data-testid="stExpander"]{border:none !important;background:none !important;}
.txtmas [data-testid="stExpander"] summary{font-size:.9rem;color:var(--acento);
font-weight:600;padding:0;}
.txtmas [data-testid="stExpander"] summary:hover{text-decoration:underline;}
.txtmas [data-testid="stExpander"] svg{display:none;}
.txtmas [data-testid="stExpanderDetails"]{padding:.2rem 0 0 !important;}
[data-testid="stExpander"]{border-color:var(--linea);}
[data-testid="stExpander"] summary{font-size:.82rem;color:var(--tenue);}
.stButton button{border-color:var(--violeta2);}
[data-testid="stMultiSelectTagsContainer"] [data-tag],[data-testid="stMultiSelectTagsContainer"] [data-tag] *{color:var(--sobre-acento) !important;}
[data-testid="stMultiSelectTagsContainer"] [data-tag] svg{fill:var(--sobre-acento) !important;}
button[kind="primary"],button[data-testid="stBaseButton-primary"],button[kind="primary"] *,button[data-testid="stBaseButton-primary"] *{color:var(--sobre-acento) !important;}
</style>"""

try:
    st.html(CSS)
except AttributeError:
    st.markdown(CSS, unsafe_allow_html=True)

VINTAGES = RAIZ / "data" / "vintages"

# Trece colores agrupados por pilar: tres tonos por familia, para que la barra
# se lea como estructura y no como arcoíris.
FAMILIAS = {
    "estado_de_derecho":     ["#0F6B5C", "#2C8A78", "#57A896"],
    "tamano_estado":         ["#1F5C8B", "#3E7FAD", "#6BA3C9"],
    "eficiencia_regulatoria": ["#7A6B1F", "#9C8A33", "#BCA858"],
    "mercados_abiertos":     ["#8C3A22", "#AC5638", "#C67A5C"],
    "propiedad_estatal":     ["#5B3A7E", "#7A56A0", "#9B7BBD"],
    "restricciones_externas": ["#7C3B5E", "#A0577E", "#C27FA0"],
}


def paleta(f) -> dict[str, str]:
    """Un color por componente, dentro de la familia de su pilar."""
    usados, out = {}, {}
    for c, ci in f["componentes"].items():
        fam = FAMILIAS.get(ci["pilar"], ["#6B7A72"])
        i = usados.get(ci["pilar"], 0)
        out[c] = fam[i % len(fam)]
        usados[ci["pilar"]] = i + 1
    return out


def fmt_num(x, dec: int, L: str, signo: bool = False) -> str:
    """Número para mostrar: coma decimal en castellano, punto en inglés."""
    s = f"{x:+.{dec}f}" if signo else f"{x:.{dec}f}"
    return s.replace(".", ",") if L == "es" else s


def fmt_pct(x, dec: int, L: str) -> str:
    """Porcentaje desde una fracción. En castellano, con espacio antes de %."""
    s = fmt_num(x * 100, dec, L)
    return f"{s}\u00a0%" if L == "es" else f"{s}%"


def reglas_hover(claves: list[str]) -> str:
    """CSS que aísla un componente al pasar el mouse.

    Al apoyar el mouse sobre el nombre de un componente en la barra lateral,
    todos los segmentos del ranking se encogen a cero y el elegido se estira
    hasta el ancho que tendría si ese componente pesara 100.

    Se usa :has() sobre `body`, que es ancestro común de la barra lateral y del
    ranking, así una sola regla por componente alcanza a todos los países.

    El disparador está SÓLO en la barra lateral. Sobre la barra del ranking no
    hay animación: el segmento muestra el nombre del componente y su aporte en
    un rótulo, y nada se mueve.
    """
    css = []
    for c in claves:
        disp = f'.wrow[data-c="{c}"]:hover'
        css.append(f'body:has({disp}) .seg{{width:0 !important;}}')
        css.append(f'body:has({disp}) .seg[data-c="{c}"]'
                   f'{{width:var(--solo) !important;}}')
    return "<style>" + "".join(css) + "</style>"


REPO = "github.com/mrodriguezcartabia/indice-liberalismo-economico"
ENLACES = {
    "fuente_metodologia":
        "https://static.heritage.org/index/pdf/2026/"
        "2026_indexofeconomicfreedom_methodology.pdf",
    "fuente_datos":
        "https://static.heritage.org/index/data/2026/"
        "2026_indexofeconomicfreedom_data.xlsx",
    "fuente_definicion": "https://economicfreedom.heritage.org/pages/about",
    "fuente_fraser": "https://www.fraserinstitute.org/economic-freedom/dataset",
    "fuente_repo": f"https://{REPO}",
}


def texto_plegable(prefijo: str, resto: str, L: str,
                   clase: str = "bajada", extra: str = "") -> str:
    """Texto al estilo de las descripciones de YouTube, sin recargar la página.

    Usa <details>/<summary> con display inline: el navegador abre y cierra solo,
    sin pedirle nada al servidor. La versión anterior guardaba el estado en la
    barra de direcciones y cada clic disparaba un recálculo completo de todos los
    países para mostrar dos oraciones.

    Devuelve HTML para que quien lo llame lo inserte donde corresponda.
    """
    return (f'<details class="mastxt {clase}"><summary>{prefijo}'
            f'<span class="resto">{resto}{extra}</span>'
            f'<span class="mas"> {t("mas", L)}</span>'
            f'<span class="menos"> {t("menos", L)}</span>'
            f'</summary></details>')


# Registro numerado de fuentes. El orden define el número que se ve en el
# texto, así que agregar una nueva va al final y nunca en el medio.
REFERENCIAS = [
    ("fuente_metodologia", ENLACES["fuente_metodologia"]),
    ("fuente_datos", ENLACES["fuente_datos"]),
    ("fuente_definicion", ENLACES["fuente_definicion"]),
    ("fuente_fraser", ENLACES["fuente_fraser"]),
    ("fuente_repo", ENLACES["fuente_repo"]),
]


def refs(texto: str) -> str:
    """Convierte los marcadores [n] del texto en llamadas numeradas.

    Cada afirmación de la página lleva el número de la fuente que la respalda,
    y el número enlaza a la lista del pie. Es lo que permite contrastar la
    página sin tener que preguntarle a nadie de dónde salió cada dato.
    """
    def llamada(m):
        i = int(m.group(1))
        if not 1 <= i <= len(REFERENCIAS):
            return m.group(0)
        return f' <a class="ref" href="#ref{i}" target="_self">[{i}]</a>'
    # Siempre con un espacio antes: "económica [3]", también entre dos citas.
    return re.sub(r"\s*\[(\d+)\]", llamada, texto)


def lista_referencias(L) -> None:
    st.markdown(f"**{t('ver_fuentes', L)}**")
    st.markdown("".join(
        f'<div class="refrow" id="ref{i}"><span class="refnum">[{i}]</span>'
        f'<a href="{u}" target="_blank">{t(k, L)}</a></div>'
        for i, (k, u) in enumerate(REFERENCIAS, 1)), unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def cargar(carpeta: str = "heritage"):
    d = VINTAGES / carpeta
    if not (d / "indice.csv").exists():
        return None
    return {"ind": pd.read_csv(d / "indice.csv"),
            "scores": pd.read_csv(d / "scores.csv"),
            "panel": pd.read_csv(d / "panel.csv"),
            "f": json.loads((d / "fuentes.json").read_text(encoding="utf-8"))}


ss = st.session_state
ss.setdefault("lang", "es")
ss.setdefault("puntos", None)
ss.setdefault("tutorial", False)
ss.setdefault("ver", 0)
ss.setdefault("tut_paso", 0)
ss.setdefault("tut_notas", {})


def cargar_puntos(nuevos: dict):
    """Cambia la ponderación activa.

    En lugar de borrar las claves de los widgets —que Streamlit puede volver a
    poblar con el valor anterior— se incrementa una versión que forma parte de
    la clave. Con clave nueva, cada widget se inicializa desde `value` y no
    queda ningún resto de la configuración previa.
    """
    ss.puntos = dict(nuevos)
    ss.ver += 1


def fijar_peso(c: str, orig: dict):
    """Toma el peso que se acaba de escribir, antes de que se recalcule todo.

    Se lleva al múltiplo de 5 más cercano: el código compartible guarda los
    puntos de a 5, y un 7 se habría guardado como 5 y reproducido otro ranking.
    """
    escrito = int(ss[f"pt_{c}_{ss.ver}"] or 0)
    v = 5 * round(escrito / 5)
    ss.puntos = {**(ss.puntos or orig), c: v}
    if v != escrito:
        ss.ver += 1          # campos nuevos, que arrancan del valor redondeado


# ===========================================================================
def arbol_subfactores(f, L):
    """Bloques del mismo ancho, cortados en tantos pedazos como subfactores
    declara cada componente.

    Hace visible que peso igual entre componentes no es peso igual entre
    indicadores. No son manipulables: Heritage publica su existencia y su
    cantidad, no sus valores por país.
    """
    st.markdown(f'<div class="nota">{t("arbol_intro", L)}</div>',
                unsafe_allow_html=True)
    if not any(ci.get("subfactores") for ci in f["componentes"].values()):
        st.warning(t("vintage_viejo", L))
        return
    filas, cadas = [], []
    for ci in f["componentes"].values():
        sf = ci.get("subfactores")
        if not sf or ci["peso_total"] <= 0:
            continue
        n = sf["n"]
        pesos = sf.get("pesos") or [1 / n] * n
        base = ci["peso_total"] * 100
        cada = [base * w for w in pesos]
        cadas += cada
        segs = "".join(f'<div class="sfseg" style="flex:{w}"></div>' for w in pesos)
        etiqueta = (fmt_pct(cada[0] / 100, 2, L) if len({round(c, 4) for c in cada}) == 1
                    else f"{fmt_pct(max(cada) / 100, 2, L)} / {fmt_pct(min(cada) / 100, 2, L)}")
        marca = "" if sf.get("verificado") else " *"
        unidad = t("indicador", L) if n == 1 else t("indicadores", L)
        filas.append(
            f'<div class="sfrow"><div>{txt(ci["titulo"], L)}{marca}'
            f'<div class="sfn">{n} {unidad}</div></div>'
            f'<div class="sfbar">{segs}</div>'
            f'<div class="sfpeso">{etiqueta}</div></div>')
    st.markdown("".join(filas), unsafe_allow_html=True)
    if cadas:
        st.markdown(
            f'<div class="nota">'
            f'{t("arbol_conclusion", L).format(v=f"{max(cadas) / min(cadas):.0f}")}'
            f'</div>', unsafe_allow_html=True)
        st.caption(t("arbol_nota", L))


def cerrar_tutorial():
    ss.tutorial = False


def cerrar_tutorial_ya():
    """Cierra la ventana y relanza toda la app.

    Un clic dentro de una ventana vuelve a dibujar solo la ventana: para que se
    cierre y el ranking de atrás se actualice hace falta st.rerun(), que desde
    un callback relanza la app entera.
    """
    ss.tutorial = False
    st.rerun()


# Cerrar con la X también marca el tutorial como cerrado: si no, se volvía a
# abrir en la ejecución siguiente y chocaba con otra ventana.
@st.dialog(" ", width="large", on_dismiss=cerrar_tutorial)
def tutorial(f, L):
    """Un componente por vez, en ventana flotante.

    Los botones de paso usan `on_click`: un callback vuelve a dibujar solo la
    ventana y el paso avanza sin tocar la pantalla de atrás. Cancelar y aplicar
    cierran la ventana con `cerrar_tutorial_ya`.
    """
    comps = list(f["componentes"])
    paso = min(ss.tut_paso, len(comps))

    st.caption(t("tut_titulo", L))

    if paso < len(comps):
        c = comps[paso]
        ci = f["componentes"][c]
        st.progress((paso + 1) / (len(comps) + 1),
                    text=t("tut_paso", L).format(i=paso + 1, n=len(comps)))
        st.markdown(f"### {txt(ci['titulo'], L)}")
        st.caption(txt(f["pilares"][ci["pilar"]]["titulo"], L))
        st.write(txt(ci.get("definicion"), L))

        st.markdown(f"**{t('tut_pregunta', L)}**")
        valor = st.slider(f"{t('tut_nada', L)} → {t('tut_mucho', L)}", 0, 10,
                          ss.tut_notas.get(c, 5), 1, key=f"tn_{c}")
        ss.tut_notas[c] = valor

        b1, b2, b3 = st.columns([1, 1, 1])
        b1.button(t("tut_anterior", L), disabled=paso == 0,
                  width="stretch",
                  on_click=lambda: ss.__setitem__("tut_paso", paso - 1))
        b2.button(t("tut_cancelar", L), width="stretch",
                  on_click=cerrar_tutorial_ya)
        b3.button(t("tut_siguiente", L), type="primary",
                  width="stretch",
                  on_click=lambda: ss.__setitem__("tut_paso", paso + 1))
        return

    # --- resumen ---
    st.progress(1.0)
    st.markdown(f"### {t('tut_resumen', L)}")
    st.write(t("tut_resumen_txt", L))
    notas = {c: ss.tut_notas.get(c, 5) for c in comps}
    total = sum(notas.values()) or 1
    st.markdown("".join(
        f'<div class="pil"><span>{txt(v["titulo"], L)}</span><b>'
        f'{fmt_pct(sum(notas[c] for c, i in f["componentes"].items() if i["pilar"] == k) / total, 1, L)}'
        f'</b></div>' for k, v in f["pilares"].items()), unsafe_allow_html=True)

    b1, b2 = st.columns(2)
    b1.button(t("tut_anterior", L), width="stretch",
              on_click=lambda: ss.__setitem__("tut_paso", paso - 1))

    def aplicar():
        ss.puntos = {c: notas[c] * 5 for c in comps}
        ss.ver += 1
        cerrar_tutorial_ya()

    b2.button(t("tut_aplicar", L), type="primary", width="stretch",
              on_click=aplicar)


@st.dialog(" ", width="large")
def critica(f, L):
    """Los hallazgos, todos verificables con el archivo y la metodología de la
    propia fuente. Ninguno cuestiona sus datos: cuestionan su cálculo."""
    st.markdown(f"## {t('critica', L)}")
    st.markdown(f'<div class="nota">{t("crit_intro", L)}</div>',
                unsafe_allow_html=True)
    # Orden: lo que declaran y lo que calculan (con lo que no se puede
    # verificar), los casos que no cierran y, al final, por qué otro índice.
    # La pestaña "El peso real de cada indicador" (crit_p4, arbol_subfactores)
    # está comentada a pedido: queda acá por si se vuelve a usar.
    p = st.tabs([t("crit_p1", L), t("crit_p2", L), t("crit_p0", L)])
    # , t("crit_p4", L)])
    with p[0]:
        st.markdown(refs(t("crit_definicion", L)), unsafe_allow_html=True)
        st.markdown(f"#### {t('crit_p3', L)}")
        st.markdown(refs(t("crit_opacidad", L)), unsafe_allow_html=True)
    with p[1]:
        st.markdown(refs(t("crit_casos", L)), unsafe_allow_html=True)
    with p[2]:
        st.markdown(refs(t("crit_porque", L)), unsafe_allow_html=True)
    # with p[3]:
    #     arbol_subfactores(f, L)
    st.divider()
    lista_referencias(L)


@st.dialog(" ", width="large")
def ayuda(datos, puntos, pesos, anio, foco, L):
    f, m = datos["f"], datos["f"]["meta"]
    st.markdown(f"## {t('como_funciona', L)}")
    p = st.tabs([t("ayuda_p0", L), t("ayuda_p3", L), t("ayuda_p1", L),
                 t("ayuda_p2", L), t("ayuda_p4", L), t("ayuda_p5", L)])

    # --- qué mide cada componente: la pestaña de apertura ---
    with p[0]:
        st.markdown(refs(t("ayuda_p0_txt", L)), unsafe_allow_html=True)
        filas = [f'<div class="tabcab"><div>{t("col_comp", L)}</div>'
                 f'<div>{t("col_mide", L)}</div><div>{t("col_cien", L)}</div>'
                 f'<div>{t("calc_peso", L)}</div></div>']
        for pil, pinfo in f["pilares"].items():
            dentro = [c for c, i in f["componentes"].items() if i["pilar"] == pil]
            if not dentro:
                continue
            filas.append(f'<div class="tabpil">{txt(pinfo["titulo"], L)}</div>')
            for c in dentro:
                ci = f["componentes"][c]
                fu = ci.get("fuente") or {}
                orig_txt = fu.get("publicador", "The Heritage Foundation")
                filas.append(
                    f'<div class="tabrow"><div><b>{txt(ci["titulo"], L)}</b>'
                    f'<div class="sfn">{orig_txt}</div></div>'
                    f'<div>{txt(ci.get("definicion"), L)}</div>'
                    f'<div>{txt(ci.get("significa_100"), L)}</div>'
                    f'<div class="tabnum">{fmt_pct(pesos["comp"].get(c, 0), 1, L)}</div>'
                    f'</div>')
        st.markdown("".join(filas), unsafe_allow_html=True)

    # --- el cálculo, país por país, comparable contra lo publicado ---
    with p[1]:
        st.markdown(refs(t("calc_intro", L)), unsafe_allow_html=True)
        sc, ind = datos["scores"], datos["ind"]
        disp = sorted(ind[ind.anio == anio].iso3.unique())
        elegido = st.selectbox(t("calc_elegir", L), disp,
                               index=disp.index(foco) if foco in disp else 0,
                               format_func=lambda c: nombre(c, L), key="calc_pais")
        fs = sc[(sc.iso3 == elegido) & (sc.anio == anio)]
        if len(fs):
            fs = fs.iloc[0]
            # Mismo cálculo que el ranking: el peso de un componente sin dato
            # se reparte entre los que el país sí tiene.
            activos_p = [c for c in f["componentes"] if pesos["comp"].get(c, 0) > 0]
            con_dato = [c for c in activos_p if c in fs and pd.notna(fs[c])]
            sin_dato = [c for c in activos_p if c not in con_dato]
            obs = sum(pesos["comp"][c] for c in con_dato) or 1
            filas, total = [], 0.0
            for c, ci in f["componentes"].items():
                if c not in con_dato:
                    continue
                w = pesos["comp"][c] / obs
                aporte = fs[c] * w
                total += aporte
                filas.append({
                    t("col_comp", L): txt(ci["titulo"], L),
                    t("calc_puntaje", L): fmt_num(float(fs[c]), 1, L),
                    t("calc_peso", L): fmt_pct(w, 4, L),
                    t("calc_aporte", L): fmt_num(float(aporte), 4, L),
                })
            st.table(pd.DataFrame(filas).style.hide(axis="index"))
            pub = datos["panel"]
            pub = pub[(pub.iso3 == elegido) & (pub.anio == anio)]
            oficial = (float(pub["hf_overall"].iloc[0])
                       if len(pub) and "hf_overall" in pub
                       and pd.notna(pub["hf_overall"].iloc[0]) else None)
            if sin_dato:
                st.caption(t("calc_falta", L).format(lista=", ".join(
                    txt(f["componentes"][c]["titulo"], L) for c in sin_dato)))
            # El puntaje publicado por Heritage solo es comparable cuando la
            # ponderación activa es la de Heritage.
            w_her = cod.pesos_desde_puntos(f["presets"]["heritage"]["puntos"])
            es_heritage = all(abs(pesos["comp"].get(c, 0) - w_her.get(c, 0)) < 1e-9
                              for c in f["componentes"])
            c1, c2, c3 = st.columns(3)
            c2.metric(t("calc_recalculado", L), fmt_num(total, 4, L))
            if oficial is not None and es_heritage:
                c1.metric(t("calc_publicado", L), fmt_num(oficial, 1, L))
                c3.metric(t("calc_diferencia", L), fmt_num(total - oficial, 4, L, signo=True))
        st.download_button(t("esc_descargar", L),
                           datos["ind"].to_csv(index=False).encode("utf-8"),
                           file_name=f"indice_{anio}.csv", mime="text/csv",
                           width="stretch")

    # --- qué estás mirando ---
    with p[2]:
        st.markdown(refs(t("ayuda_1", L)), unsafe_allow_html=True)
        st.markdown(f"##### {t('peso_resultante', L)}")
        st.caption(t("peso_resultante_ayuda", L))
        st.markdown("".join(
            f'<div class="pil"><span>{txt(v["titulo"], L)}</span>'
            f'<b>{fmt_pct(pesos["pilar"][k], 1, L)}</b></div>'
            for k, v in f["pilares"].items()), unsafe_allow_html=True)

    # --- de dónde salen los números ---
    with p[3]:
        st.markdown(refs(t("ayuda_2", L)), unsafe_allow_html=True)
        for k, r in (f.get("rezagos") or {}).items():
            viejos = r.get("descartados") or []
            st.info(t("esc_rezago", L).format(
                comp=txt(f["componentes"][k]["titulo"], L),
                a1=r["anio_dato"], a2=r["anio_asignado"], n=r["paises"],
                desde=r.get("desde", ""))
                + (" " + t("esc_rezago_viejos", L).format(
                    lista=", ".join(nombre(c, L) for c in viejos)) if viejos else ""))
        for cn, ci in f["componentes"].items():
            with st.expander(txt(ci["titulo"], L)):
                st.write(txt(ci.get("definicion"), L))
                fu2 = ci.get("fuente") or {}
                if fu2.get("columna"):
                    st.caption(f"{t('esc_columna', L)}: `{fu2['columna']}`")
                if fu2.get("insumos"):
                    st.caption(f"{t('esc_insumos', L)}: {txt(fu2['insumos'], L)}")
                if ci.get("formula"):
                    st.caption(f"{t('esc_formula', L)}: {txt(ci['formula'], L)}")
                if ci.get("reproducible"):
                    st.caption(t(f"repro_{ci['reproducible']}", L))
                if fu2.get("url"):
                    st.markdown(f"[{txt(fu2.get('dataset', ''), L)}]({fu2['url']})")
                if fu2.get("advertencia"):
                    st.warning(txt(fu2["advertencia"], L))
        st.divider()
        lista_referencias(L)

    # --- qué se puede verificar ---
    with p[4]:
        st.markdown(refs(t("ayuda_4", L)), unsafe_allow_html=True)
        val = f.get("validacion", {})
        if val.get("disponible"):
            marca = "ok" if val["cierra"] else "no"
            st.markdown(f'**{t("esc_validacion", L)}** '
                        f'<span class="etq {marca}">{t("val_max", L)} '
                        f'{fmt_num(val["diferencia_maxima"], 4, L)}</span> · '
                        f'{val["paises_comparados"]} {t("val_paises", L)}',
                        unsafe_allow_html=True)

    # --- qué falta ---
    with p[5]:
        if m.get("ausencias"):
            st.write(txt(m["ausencias"], L))
        nc = m.get("no_calificados", {})
        if nc:
            st.markdown(f"**{t('esc_no_calificados', L)}**")
            st.write(", ".join(nombre(c, L) for c in nc.get("paises", [])))
            st.caption(txt(nc.get("nota"), L))


# ===========================================================================
def main():
    datos = cargar()
    if datos is None:
        st.error(t("sin_datos", ss.lang))
        return
    f, m = datos["f"], datos["f"]["meta"]
    L = ss.lang
    claves = list(f["componentes"])
    claves_codigo = f["orden_codigo"]      # orden fijo del código compartible
    presets = f.get("presets", {})
    POR_DEFECTO = "liberalismo"
    orig = presets[POR_DEFECTO]["puntos"]
    # El porcentaje mínimo de datos es parte de la definición de cada índice:
    # con otro valor, el ranking ya no es el del índice publicado.
    COB_OFICIAL = int(round(m["cobertura_minima"] * 100))
    ss.setdefault("sel_cob", COB_OFICIAL)

    def preset_activo(pts) -> str | None:
        """Qué preset corresponde a estos puntos, si alguno."""
        for k, v in presets.items():
            if all(int(pts.get(c, 0)) == int(v["puntos"].get(c, 0))
                   for c in f["componentes"]):
                return k
        return None

    # Valores por defecto antes de la barra lateral: si algo falla ahí dentro,
    # main() sigue teniendo con qué seguir en lugar de romper con NameError.
    puntos = dict(orig)
    total = sum(puntos.values())

    # ---------------- barra lateral: texto + componentes + código ----------
    with st.sidebar:
        cabeza, cola = t("intro_barra", L).split("|", 1)
        st.markdown(texto_plegable(cabeza.strip(), f" {cola.strip()}", L,
                                   clase="nota"), unsafe_allow_html=True)

        base = dict(ss.puntos or orig)
        color = paleta(f)

        # El peso por indicador se calcula con los puntos YA aplicados, para
        # que el porcentaje que se lee al lado del campo corresponda al ranking
        # que está en pantalla y no a lo que todavía se está tipeando.
        _tot = sum(base.values()) or 1

        def peso_ind(c):
            """(cantidad de indicadores, peso mínimo, peso máximo) o None."""
            ci = f["componentes"][c]
            sf = ci.get("subfactores")
            if not sf or base.get(c, 0) <= 0:
                return None
            n = sf["n"]
            ws = sf.get("pesos") or [1 / n] * n
            w = base[c] / _tot * 100
            return n, min(x * w for x in ws), max(x * w for x in ws)

        # Sin formulario ni botón: Streamlit no recalcula con cada tecla, solo
        # al apretar Enter o salir del campo, y ahí `fijar_peso` actualiza la
        # ponderación antes del recálculo. Los botones +/- de todos los campos
        # numéricos están ocultos (CSS): cada clic disparaba un recálculo.
        with st.container():
            puntos = {}
            for pil, pinfo in f["pilares"].items():
                dentro = [c for c, i in f["componentes"].items()
                          if i["pilar"] == pil]
                if not dentro:
                    continue
                st.markdown(f"**{txt(pinfo['titulo'], L)}**")
                for c in dentro:
                    ci = f["componentes"][c]
                    sf = ci.get("subfactores")
                    n = sf["n"] if sf else 0
                    detalle = ""
                    if n:
                        unidad = t("indicador" if n == 1 else "indicadores", L)
                        pi = peso_ind(c)
                        # Con pesos internos desiguales (salud fiscal: 80/20)
                        # no hay un "cada uno": se muestran los dos extremos.
                        if not pi:
                            pct = ""
                        elif abs(pi[2] - pi[1]) < 1e-9:
                            pct = f' · <b>{fmt_pct(pi[1] / 100, 2, L)}</b> {t("cada_uno", L)}'
                        else:
                            pct = f' · <b>{fmt_pct(pi[2] / 100, 2, L)} / {fmt_pct(pi[1] / 100, 2, L)}</b>'
                        detalle = f'<span class="sfn">{n} {unidad}{pct}</span>'
                    # Definición en una ventana que solo aparece al pasar el
                    # mouse. Vive dentro de la barra lateral, así que no puede
                    # tapar el ranking.
                    defin = html.escape(txt(ci.get("definicion"), L).strip())
                    s100 = txt(ci.get("significa_100"), L)
                    sentido = (f'<span class="pop100">{t("pop_100", L).format(x=html.escape(s100))}</span>'
                               if s100 else "")
                    pop = f'<span class="pop">{defin}{sentido}</span>' if defin else ""
                    col1, col2 = st.columns([1, 0.42])
                    col1.markdown(
                        f'<div class="wrow" data-c="{c}">'
                        f'<span><i class="chip" style="background:{color[c]}">'
                        f'</i>{txt(ci["titulo"], L)}{detalle}</span>{pop}</div>',
                        unsafe_allow_html=True)
                    puntos[c] = col2.number_input(
                        txt(ci["titulo"], L), 0, 100,
                        int(base.get(c, orig.get(c, 0))), 5,
                        key=f"pt_{c}_{ss.ver}", label_visibility="collapsed",
                        on_change=fijar_peso, args=(c, orig))

        puntos = dict(base)
        total = sum(puntos.values())


    # Con todos los puntos en cero no hay índice que calcular: se avisa y se
    # muestra el índice por defecto, sin cortar la página (los botones de la
    # derecha tienen que seguir estando).
    if total <= 0:
        st.warning(t("todo_cero", L).format(
            indice=txt(presets[POR_DEFECTO]["nombre"], L)))
        puntos = dict(orig)
        total = sum(puntos.values())
    pesos_comp = cod.pesos_desde_puntos(puntos)
    pesos_pilar = {}
    for pil in f["pilares"]:
        pesos_pilar[pil] = sum(pesos_comp[c] for c, i in f["componentes"].items()
                               if i["pilar"] == pil)
    pesos = {"comp": pesos_comp, "pilar": pesos_pilar}

    codigo = cod.codificar(m["sigla"], puntos, claves_codigo)
    act = preset_activo(puntos) if ss.sel_cob == COB_OFICIAL else None

    # ---------------- encabezado ----------------
    izq, der = st.columns([4, 1.35])
    with izq:
        titulo = (txt(presets[act]["nombre"], L) if act
                  else t("titulo_propio", L))
        st.markdown(f"# {titulo}")
        cabeza, cola = t("intro_pagina", L).split("|", 1)
        # "|" separa lo visible de lo que se abre con "…más", dentro del
        # mismo párrafo. La descripción de cada índice no va acá: está en
        # la ayuda del selector de índice.
        st.markdown(texto_plegable(
            cabeza.strip(), " " + cola.strip(), L,
            extra=f'<br><br>{t("ver_razones", L).format(b=t("critica", L))}'),
            unsafe_allow_html=True)
    # ---------------- controles en horizontal ----------------
    ind_all = datos["ind"]
    anios_ok = [int(a) for a in sorted(ind_all[ind_all.publicable].anio.unique())]
    g = izq.columns([1.6, 0.9, 0.9, 1.1])

    # El selector muestra siempre `actual`, que sale de los puntos vigentes.
    # Streamlit recuerda la última elección de un widget, así que la clave
    # cambia con `actual` y cada vez que se abre el tutorial desde acá: con
    # clave nueva, el selector arranca de `actual` y una elección vieja no
    # vuelve a dispararse.
    ss.setdefault("ver_sel", 0)
    opciones = list(presets) + ["propio"]
    etiq = {k: txt(v["nombre"], L) for k, v in presets.items()}
    etiq["propio"] = t("titulo_propio", L)
    actual = act or "propio"
    sel = g[0].selectbox(t("elegir_indice", L), opciones,
                         index=opciones.index(actual),
                         format_func=lambda k: etiq[k],
                         help=txt(presets.get(actual, {}).get("descripcion"), L),
                         key=f"sel_indice_{actual}_{ss.ver_sel}")
    if sel in presets and sel != actual:
        cargar_puntos(presets[sel]["puntos"])
        ss.sel_cob = COB_OFICIAL          # el índice elegido, con su porcentaje
        st.rerun()
    elif sel == "propio" and actual != "propio":
        # Elegido a mano: se abre "Armá tu propio índice". Si se cancela, el
        # selector vuelve solo al índice que estaba, porque `actual` no cambió.
        ss.tutorial = True
        ss.tut_paso = 0
        ss.tut_notas = {}
        ss.ver_sel += 1

    # Los controles de vista guardan su valor en session_state (sel_*): cada
    # control tiene esa clave, así conserva lo elegido entre recálculos.
    ss.setdefault("sel_anio", anios_ok[-1])
    ss.setdefault("sel_cuantos", 15)
    if ss.sel_anio not in anios_ok:
        ss.sel_anio = anios_ok[-1]
    # Con clave fija y sin valor inicial: si el valor inicial cambia entre un
    # recálculo y el siguiente, Streamlit crea un control nuevo y la elección
    # se pierde (un cambio de año sí y otro no).
    anio = g[1].selectbox(t("anio", L), anios_ok, key="sel_anio")
    cuantos = g[2].number_input(t("mostrar", L), min_value=5, max_value=200,
                                step=5, key="sel_cuantos")
    # Con clave propia: el valor nuevo ya está en ss.sel_cob al empezar el
    # recálculo, así el selector de índice pasa a "Índice propio" en el mismo
    # paso en que se cambia el porcentaje.
    min_cob = g[3].number_input(t("cobertura_min", L), min_value=0,
                                max_value=100, step=5, key="sel_cob",
                                help=t("cobertura_ayuda", L))
    min_cob = min_cob / 100
    ind_a = ind_all[ind_all.anio == anio].set_index("iso3")
    ss.setdefault("sel_seg", [c for c in ("ARG",) if c in ind_a.index])
    seguidos = izq.multiselect(
        t("seguir", L), sorted(ind_a.index),
        default=[c for c in ss.sel_seg if c in ind_a.index],
        format_func=lambda c: nombre(c, L), help=t("seguir_ayuda", L))
    ss.sel_seg = list(seguidos)

    # Streamlit admite una sola ventana por ejecución: si se pidió otra, el
    # tutorial cede el lugar.
    if ss.get("btn_critica") or ss.get("btn_ayuda"):
        ss.tutorial = False
    if ss.tutorial:
        tutorial(f, L)

    # ---------------- recálculo ----------------
    sc_a = datos["scores"]
    sc_a = sc_a[sc_a.anio == anio].set_index("iso3")
    vivo = pd.DataFrame(index=sc_a.index)
    vivo["indice"] = nz.puntaje_pilar(sc_a, pesos_comp)
    for pil in f["pilares"]:
        dentro = {c: pesos_comp[c] for c, i in f["componentes"].items()
                  if i["pilar"] == pil and pesos_comp[c] > 0}
        vivo[pil] = (nz.puntaje_pilar(sc_a, dentro) if dentro
                     else pd.Series(float("nan"), index=sc_a.index))
    con_peso = [c for c in claves if pesos_comp.get(c, 0) > 0
                and c in sc_a.columns]
    vivo["cobertura"] = (sc_a[con_peso].notna().mean(axis=1) if con_peso
                         else ind_a["cobertura"])
    # Sin puntaje no hay puesto, aunque la cobertura mínima sea 0. El
    # redondeo a 9 decimales evita que el ruido de punto flotante desempate
    # dos países que suman exactamente lo mismo.
    vivo["publicable"] = (vivo["cobertura"] >= min_cob) & vivo["indice"].notna()
    vivo["ranking"] = vivo.where(vivo.publicable)["indice"].round(9).rank(
        ascending=False, method="min")
    # Rankings de referencia: los dos presets, calculados con los mismos datos,
    # para que se pueda comparar contra cualquiera de los dos sin cambiar de vista.
    referencias = {}
    for nom, pre in presets.items():
        w_ref = cod.pesos_desde_puntos(pre["puntos"])
        act_ref = {c: v for c, v in w_ref.items() if v > 0 and c in sc_a.columns}
        if act_ref:
            # Mismo criterio que el ranking principal: solo compiten los países
            # con cobertura suficiente en los componentes de ese índice. Sin
            # esto, un país sin datos suficientes ocupaba un puesto en la
            # referencia y corría a todos los de abajo.
            cob_ref = sc_a[list(act_ref)].notna().mean(axis=1)
            referencias[nom] = (nz.puntaje_pilar(sc_a, act_ref)
                                .where(cob_ref >= min_cob).round(9)
                                .rank(ascending=False, method="min"))
    for nom, r_ in referencias.items():
        vivo[f"ref_{nom}"] = r_

    huerfanos = [txt(f["pilares"][p]["titulo"], L) for p in f["pilares"]
                 if pesos_pilar[p] > 0 and vivo[p].notna().sum() == 0]
    if huerfanos:
        izq.markdown(f'<div class="aviso">'
                    f'{t("aviso_sin_dato", L).format(p=", ".join(huerfanos), a=anio)}'
                    f'</div>', unsafe_allow_html=True)
    # Pares con correlación >= umbral_superposicion (los calcula build.py).
    # Los pares que comparten componentes se juntan en un solo aviso: tres
    # componentes que miden lo mismo son un grupo, no tres problemas.
    pares = [sp for sp in f.get("superposiciones", [])
             if pesos_comp.get(sp["a"], 0) > 0 and pesos_comp.get(sp["b"], 0) > 0]
    grupos = []
    for sp in pares:
        tocados = [g for g in grupos if {sp["a"], sp["b"]} & g["comps"]]
        nuevo = {"comps": {sp["a"], sp["b"]}, "r": [sp["r"]]}
        for g in tocados:
            nuevo["comps"] |= g["comps"]; nuevo["r"] += g["r"]; grupos.remove(g)
        grupos.append(nuevo)

    def num(x):
        return fmt_num(x, 2, L)

    def y_e(siguiente):
        """«y» pasa a «e» antes de i- o hi- (salvo hie-, hia-...: «y hielo»)."""
        if L != "es":
            return "and"
        w = siguiente.lstrip("«").lower()
        return "e" if re.match(r"h?[ií](?![aeiouáéó])", w) else "y"

    for g in grupos:
        comps = [c for c in claves if c in g["comps"]]
        titulos = [("«{}»" if L == "es" else "\u201c{}\u201d").format(
            txt(f["componentes"][c]["titulo"], L)) for c in comps]
        if len(comps) == 2:
            b_tit = txt(f["componentes"][comps[1]]["titulo"], L)
            aviso = t("aviso_superposicion", L).format(
                a=txt(f["componentes"][comps[0]]["titulo"], L),
                b=b_tit, y=y_e(b_tit), r=num(g["r"][0]))
        else:
            veces = {3: t("veces_3", L), 4: t("veces_4", L)}.get(
                len(comps), t("veces_n", L).format(n=len(comps)))
            aviso = t("aviso_superposicion_grupo", L).format(
                lista=f'{", ".join(titulos[:-1])} {y_e(titulos[-1])} {titulos[-1]}',
                n={3: t("numero_3", L), 4: t("numero_4", L)}.get(len(comps), len(comps)),
                rmin=num(min(g["r"])), rmax=num(max(g["r"])), veces=veces)
        izq.markdown(f'<div class="aviso">{aviso}</div>', unsafe_allow_html=True)

    # Países a la vista a los que les falta algún componente activo: llevan
    # asterisco y acá se aclara cuál falta.
    tope = min(int(cuantos), max(int(vivo.publicable.sum()), 1))
    vista = list(vivo[vivo.publicable].nlargest(tope, "indice").index) + [
        c for c in seguidos if c in vivo.index and vivo.loc[c, "publicable"]]
    activos_c = [c for c in claves if pesos_comp.get(c, 0) > 0 and c in sc_a.columns]
    incompletos = {}
    for iso3 in dict.fromkeys(vista):
        falta = [c for c in activos_c if pd.isna(sc_a[c].get(iso3))]
        if falta:
            incompletos[iso3] = falta
    if incompletos:
        lista = "; ".join(
            f'{nombre(i, L)} ({", ".join(txt(f["componentes"][c]["titulo"], L).lower() for c in fl)})'
            for i, fl in incompletos.items())
        izq.markdown(f'<div class="aviso">{t("aviso_incompleto", L).format(lista=html.escape(lista))}</div>',
                     unsafe_allow_html=True)

    # Con Heritage activo, los países cuyo puesto difiere del que se deduce del
    # puntaje publicado por Heritage llevan doble asterisco: es la misma
    # réplica, pero desempata con los decimales que Heritage no publica.
    distintos = {}
    if act == "heritage":
        pub = datos["panel"]
        pub = pub[(pub.anio == anio) & pub["hf_overall"].notna()].set_index("iso3")
        # El puesto publicado por Heritage cuando la edición lo trae (2020 a
        # 2023). Si no, el que surge de su puntaje: dos países empatados ocupan
        # un rango de puestos (Heritage los desempata con decimales que no
        # publica), y solo se marca un puesto que cae fuera de ese rango.
        if "hf_puesto" in pub and pub["hf_puesto"].notna().any():
            desde_ = hasta_ = pub["hf_puesto"].dropna()
        else:
            desde_ = pub["hf_overall"].rank(ascending=False, method="min")
            hasta_ = pub["hf_overall"].rank(ascending=False, method="max")
        for iso3 in dict.fromkeys(vista):
            if iso3 in desde_.index:
                d_, h_ = int(desde_[iso3]), int(hasta_[iso3])
                if not d_ <= int(vivo.loc[iso3, "ranking"]) <= h_:
                    distintos[iso3] = str(d_) if d_ == h_ else f"{d_}–{h_}"
    if distintos:
        lista = "; ".join(f"{nombre(i, L)} ({t('puesto_heritage', L)} {n})"
                          for i, n in distintos.items())
        izq.markdown(f'<div class="aviso">{t("aviso_puesto_heritage", L).format(lista=html.escape(lista))}</div>',
                     unsafe_allow_html=True)

    # ---------------- pestañas ----------------
    color = paleta(f)
    activos = [c for c in claves if pesos_comp.get(c, 0) > 0]
    n_pub = max(int(vivo.publicable.sum()), 1)
    orden_ref = [n for n in (POR_DEFECTO, "heritage") if n in referencias]
    tabla = vivo[vivo.publicable].nlargest(min(int(cuantos), n_pub), "indice")

    # ---------------- columna de acciones ----------------
    with der:
        # Marca para el CSS: esta columna mide lo que su botón más largo en una
        # línea, y la izquierda ocupa el resto.
        st.markdown('<span class="marca-der"></span>', unsafe_allow_html=True)
        i1, i2 = st.columns(2)
        for col, cod_l in ((i1, "es"), (i2, "en")):
            if col.button(cod_l.upper(), width="stretch",
                          type="primary" if L == cod_l else "secondary",
                          key=f"lang_{cod_l}"):
                ss.lang = cod_l
                st.rerun()
        if st.button(t("critica", L), width="stretch",
                     key="btn_critica"):
            critica(f, L)
        # Destello los primeros 40 segundos: quince ciclos de 2,6 s. Es el
        # botón que hace auditable la página, así que conviene que se note.
        st.markdown('<div class="destello">', unsafe_allow_html=True)
        if st.button(t("como_funciona", L), width="stretch",
                     key="btn_ayuda"):
            ayuda(datos, puntos, pesos, anio,
                  seguidos[0] if seguidos else "SGP", L)
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button(t("tut_boton", L), width="stretch"):
            ss.tutorial = True
            ss.tut_paso = 0
            ss.tut_notas = {}
            st.rerun()
        st.write("")
        st.caption(t("codigo_config", L))
        st.code(codigo, language=None)
        e = st.text_input("cod", placeholder=t("aplicar_codigo", L),
                          label_visibility="collapsed")
        if st.button(t("aplicar_codigo", L), width="stretch") and e:
            r = cod.decodificar(e, claves_codigo)
            if r:
                cargar_puntos(r)
                st.rerun()
            st.error(t("codigo_invalido", L))
        try:
            from pdf import generar
            filas_pdf = [(int(r["ranking"]), nombre(i, L), r["indice"],
                          r.get("ref_heritage")
                          if pd.notna(r.get("ref_heritage")) else None)
                         for i, r in tabla.iterrows()]
            blob = generar(
                titulo, t("intro_pagina", L).replace("|", " "), filas_pdf,
                {"codigo": codigo, "repo": REPO,
                 "fuente": m["fuente"]["publicador"],
                 # La fecha de corte publicada es la de la edición vigente;
                 # para otro año se cita esa edición y no se inventa la fecha.
                 "corte": m.get("fecha_corte", "") if anio == int(m["vintage"]) else "",
                 "anio": anio,
                 "procedencia": (
                     f"{txt(m['fuente']['dataset'], L)}. {m['fuente'].get('url_datos', '')}"
                     if anio == int(m["vintage"]) else
                     f"{txt(m['fuente']['dataset_anio'], L).format(a=anio)}. "
                     f"{(m['fuente'].get('urls_ediciones_viejas') or {}).get(anio) or m['fuente']['url_datos_anio'].format(a=anio)}")},
                {"codigo": t("codigo_config", L), "corte": t("m_corte", L),
                 "anio": t("anio", L), "ponderacion": t("pdf_ponderacion", L),
                 "puesto": t("col_puesto", L), "pais": t("col_pais", L),
                 "puntaje": t("col_puntaje", L), "comparacion": "Heritage",
                 "procedencia": t("pdf_procedencia", L),
                 "sep_decimal": "," if L == "es" else "."},
                [(txt(f["componentes"][c]["titulo"], L),
                  fmt_pct(pesos_comp[c], 1, L)) for c in activos])
            st.download_button(t("imprimir", L), blob,
                               file_name=f"indice_{anio}_{codigo}.pdf",
                               mime="application/pdf",
                               width="stretch")
        except ImportError:
            pass


    with izq:

        def fila(iso3, r, marcar=False):
            # Cada tramo mide puntaje_del_componente x peso_del_componente, así
            # que la suma de los tramos es el índice y el largo total es
            # comparable entre países. Si al país le falta un componente, ese
            # tramo no está y la barra queda más corta que el puntaje: el
            # puntaje reparte el peso entre lo observado, y el asterisco del
            # nombre lo avisa.
            # También van los componentes con peso cero, con ancho cero: al
            # pasar el mouse por uno en la barra lateral, su tramo se estira.
            vals = {c: sc_a[c].get(iso3) for c in claves if c in sc_a.columns}
            vals = {c: v for c, v in vals.items() if v is not None and pd.notna(v)}
            segs = ""
            for c, v in vals.items():
                w = pesos_comp[c]
                segs += (f'<div class="seg" data-c="{c}" '
                         f'style="width:{v * w:.3f}%;'
                         f'--solo:{v:.2f}%;background:{color[c]}">'
                         f'<span class="segpop">'
                         f'{html.escape(txt(f["componentes"][c]["titulo"], L))}: '
                         f'{fmt_num(v, 1, L)} × {fmt_pct(w, 1, L)}</span></div>')
            celdas = ""
            for nom in orden_ref:
                v_ = r.get(f"ref_{nom}")
                if pd.isna(v_):
                    celdas += '<div class="vs">—</div>'
                    continue
                d = int(v_ - r["ranking"])
                marca = ("" if d == 0 else
                         f' <span class="{"sube" if d > 0 else "baja"}">'
                         f'{"▲" if d > 0 else "▼"}{abs(d)}</span>')
                celdas += f'<div class="vs">{int(v_)}{marca}</div>'
            return (f'<div class="fila{" seguido" if marcar else ""}">'
                    f'<div class="pos">{int(r["ranking"])}</div>'
                    f'<div class="pais">{html.escape(nombre(iso3, L))}'
                    f'{"*" if iso3 in incompletos else ""}{"**" if iso3 in distintos else ""}</div>'
                    f'<div class="barra">{segs}</div>'
                    f'<div class="val">{fmt_num(r["indice"], 1, L)}</div>'
                    f'{celdas}</div>')

        bloque = [
            reglas_hover(claves),
            f'<div class="pista-ayuda">{t("barra_ayuda", L)}</div>',
            f'<div class="cab"><div>{t("col_puesto", L)}</div>'
            f'<div>{t("col_pais", L)}</div><div>{t("col_aporte", L)}</div>'
            f'<div style="text-align:right">{t("col_puntaje", L)}</div>'
            + "".join(f'<div style="text-align:right">'
                      f'{txt(presets[n]["corto"], L)}</div>'
                      for n in orden_ref) + '</div>',
        ]
        bloque += [fila(i, r, i in seguidos) for i, r in tabla.iterrows()]

        afuera = [c for c in seguidos if c not in tabla.index
                  and c in vivo.index and vivo.loc[c, "publicable"]]
        if afuera:
            bloque.append(f'<div class="corte">{t("fuera_top", L)}</div>')
            bloque += [fila(c, vivo.loc[c], True)
                       for c in sorted(afuera, key=lambda c: vivo.loc[c, "ranking"])]
        # Una sola llamada: Streamlit encierra cada markdown en su propio
        # contenedor, y dos llamadas romperían la continuidad del bloque.
        st.markdown("".join(bloque), unsafe_allow_html=True)

        sin = [c for c in seguidos if c in vivo.index
               and not vivo.loc[c, "publicable"]]
        if sin:
            st.caption(f"{t('sin_cobertura', L)}: "
                       + ", ".join(nombre(c, L) for c in sin))


main()


def ubicar_ventanas():
    """Abre la ventana de definición hacia arriba cuando abajo no entra.

    CSS no sabe dónde quedó cada componente en la pantalla, así que esto lo
    decide un script chico: al pasar el mouse mide la ventana y, si se sale
    por abajo y arriba hay más lugar, la da vuelta. Se registra una sola vez,
    aunque la app se recalcule.
    """
    st.html("""<script>
    if (!window.ubicarVentanas) {
      window.ubicarVentanas = true;
      document.addEventListener("mouseover", function (e) {
        var fila = e.target.closest && e.target.closest(".wrow");
        if (!fila || !fila.querySelector(".pop")) return;
        fila.classList.remove("arriba");
        requestAnimationFrame(function () {
          var pop = fila.querySelector(".pop").getBoundingClientRect();
          var r = fila.getBoundingClientRect();
          var barra = document.querySelector('[data-testid="stSidebar"]');
          var lim = barra ? barra.getBoundingClientRect()
                          : {top: 0, bottom: window.innerHeight};
          var techo = Math.max(lim.top, 0);
          var piso = Math.min(lim.bottom, window.innerHeight);
          if (pop.bottom > piso && r.top - techo > piso - r.bottom) {
            fila.classList.add("arriba");
          }
        });
      });
    }
    </script>""", unsafe_allow_javascript=True)

ubicar_ventanas()
