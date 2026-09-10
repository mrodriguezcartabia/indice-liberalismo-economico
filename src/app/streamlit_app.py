"""Página pública: el índice de Heritage, y qué pasa cuando se lo repondera.

    streamlit run app/streamlit_app.py

Diseño:
  - barra lateral -> texto introductorio, los componentes en puntos, y el
    código de configuración abajo. Es lo que define QUÉ ES el índice.
  - pantalla principal -> selector de ponderación, controles de vista en
    horizontal, ranking, árbol de indicadores, dispersión.
  - cualquier cambio de puntos convierte "Heritage" en "Índice propio".

Los pesos se asignan en PUNTOS por componente, no en porcentajes. El peso de un
componente es sus puntos sobre el total, y el de un pilar es la suma de los
puntos de sus componentes: no se pondera aparte. Esa es la mecánica del índice
original, y dejarla a la vista es parte de lo que la página muestra.

La app no descarga ni recalcula desde las fuentes: lee los vintages congelados
que produce src/build.py.
"""

from __future__ import annotations

import json
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

st.set_page_config(page_title="Índice de libertad económica", layout="wide",
                   initial_sidebar_state="expanded")

# ---------------------------------------------------------------------------
# IMPORTANTE: sin líneas en blanco ni comentarios CSS. Streamlit divide el
# markdown en cada línea vacía, cierra el <style> por su cuenta y el resto se
# imprime como texto. Por eso además se usa st.html().
# ---------------------------------------------------------------------------
CSS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;800&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{--papel:#EFF1EC;--tinta:#131A17;--tenue:#6B7A72;--senal:#0F6B5C;
--alerta:#A8412F;--linea:#D5DAD2;--panel:#E7EAE4;}
.stApp{background:var(--papel);}
html,body,[class*="css"]{font-family:'Archivo',system-ui,sans-serif;color:var(--tinta);}
h1,h2,h3,h4{font-family:'Archivo',sans-serif;font-weight:800;letter-spacing:-.02em;}
h1{font-size:2.2rem;line-height:1.05;margin:.1rem 0 .2rem;}
.cintillo{font-family:'IBM Plex Mono',monospace;font-size:.67rem;letter-spacing:.15em;
text-transform:uppercase;color:var(--tenue);margin-bottom:.3rem;}
.bajada{color:var(--tenue);max-width:70ch;font-size:.92rem;line-height:1.5;margin:.2rem 0 0;}
.cab{display:grid;grid-template-columns:2.6rem 11rem 1fr 4rem 4.6rem;gap:.6rem;
white-space:nowrap;
font-family:'IBM Plex Mono',monospace;font-size:.66rem;letter-spacing:.1em;
text-transform:uppercase;color:var(--tenue);padding-bottom:.3rem;
border-bottom:1px solid var(--tinta);}
.fila{display:grid;grid-template-columns:2.6rem 11rem 1fr 4rem 4.6rem;gap:.6rem;
align-items:center;padding:.26rem 0;border-bottom:1px solid var(--linea);}
.barra{display:flex;height:14px;background:#E3E7E0;border-radius:2px;overflow:hidden;}
.seg{height:100%;transition:width .28s cubic-bezier(.4,0,.2,1);min-width:0;}
.chip{width:9px;height:9px;border-radius:2px;display:inline-block;
margin-right:.4rem;flex:0 0 auto;}
.wrow{cursor:default;border-radius:3px;padding:.15rem .3rem;margin:0 -.3rem;
transition:background .15s;}
.wrow:hover{background:rgba(15,107,92,.10);}
.pista-ayuda{font-size:.75rem;color:var(--tenue);margin:-.2rem 0 .6rem;}
.pos,.val,.vs{font-family:'IBM Plex Mono',monospace;font-size:.84rem;}
.pos{color:var(--tenue);font-weight:600;}
.val{text-align:right;font-weight:600;}
.vs{text-align:right;color:var(--tenue);}
.pais{font-size:.9rem;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.sube{color:var(--senal);font-weight:600;}
.baja{color:var(--alerta);font-weight:600;}
.seguido{background:rgba(15,107,92,.08);margin:0 -.5rem;padding:.3rem .5rem;border-radius:3px;}
.seguido .pais{color:var(--senal);}
.corte{font-family:'IBM Plex Mono',monospace;font-size:.67rem;letter-spacing:.12em;
text-transform:uppercase;color:var(--tenue);margin:1.1rem 0 .3rem;}
.nota{font-size:.79rem;color:var(--tenue);border-left:2px solid var(--senal);
padding-left:.75rem;margin:.7rem 0;line-height:1.55;}
.aviso{font-size:.79rem;color:var(--alerta);border-left:2px solid var(--alerta);
padding-left:.75rem;margin:.7rem 0;line-height:1.5;}
.paso{font-family:'IBM Plex Mono',monospace;font-size:.8rem;padding:.3rem 0;
border-bottom:1px dotted var(--linea);}
.etq{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:.62rem;
letter-spacing:.08em;text-transform:uppercase;padding:.1rem .45rem;border-radius:3px;
border:1px solid var(--linea);color:var(--tenue);}
.etq.ok{border-color:var(--senal);color:var(--senal);}
.etq.no{border-color:var(--alerta);color:var(--alerta);}
.pil{display:grid;grid-template-columns:1fr 3.6rem;gap:.5rem;font-size:.82rem;
padding:.22rem 0;border-bottom:1px solid var(--linea);}
.pil b{font-family:'IBM Plex Mono',monospace;text-align:right;font-weight:600;}
.sfrow{display:grid;grid-template-columns:14rem 1fr 7rem;gap:.8rem;align-items:center;
padding:.32rem 0;border-bottom:1px solid var(--linea);font-size:.85rem;}
.sfbar{display:flex;height:19px;gap:2px;}
.sfseg{background:var(--senal);height:100%;border-radius:2px;opacity:.85;}
.sfpeso{font-family:'IBM Plex Mono',monospace;font-size:.76rem;text-align:right;color:var(--tenue);}
.sfn{font-size:.72rem;color:var(--tenue);}
[data-testid="stSidebar"]{background:var(--panel);border-right:1px solid var(--linea);}
.wrow{font-size:.82rem;}
.wrow .sfn{display:block;margin-left:1.3rem;}
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


def reglas_hover(claves: list[str]) -> str:
    """CSS que aísla un componente al pasar el mouse.

    Al apoyar el mouse sobre el nombre de un componente en la barra lateral,
    todos los segmentos del ranking se encogen a cero y el elegido se estira
    hasta el ancho que tendría si ese componente pesara 100.

    Se usa :has() sobre `body`, que es ancestro común de la barra lateral y del
    ranking, así una sola regla por componente alcanza a los 176 países.

    El disparador está en la barra lateral y no en los segmentos porque los
    segmentos se mueven: al encogerse los vecinos, el segmento se desplazaría
    bajo el cursor, perdería el hover y la animación titilaría. El hover sobre
    el segmento queda igual como atajo, pero el camino confiable es la barra.
    """
    css = []
    for c in claves:
        for disp in (f'.wrow[data-c="{c}"]:hover', f'.seg[data-c="{c}"]:hover'):
            css.append(f'body:has({disp}) .seg{{width:0 !important;}}')
            css.append(f'body:has({disp}) .seg[data-c="{c}"]'
                       f'{{width:var(--solo) !important;}}')
    return "<style>" + "".join(css) + "</style>"


def contraste(f, pesos_comp):
    """Componente con el indicador más pesado y con el más liviano.

    Es el dato central de la página: peso igual entre componentes no es peso
    igual entre indicadores, porque cada componente se calcula con una cantidad
    distinta de ellos.
    """
    d = []
    for k, v in f["componentes"].items():
        sf = v.get("subfactores")
        w = pesos_comp.get(k, 0)
        if not sf or w <= 0:
            continue
        n = sf["n"]
        ws = sf.get("pesos") or [1 / n] * n
        d.append((k, n, [x * w * 100 for x in ws]))
    if len(d) < 2:
        return None
    mx = max(d, key=lambda x: max(x[2]))
    mn = min(d, key=lambda x: min(x[2]))
    if mx[0] == mn[0]:
        return None
    return {"cmax": mx[0], "nmax": mx[1], "pmax": max(mx[2]),
            "cmin": mn[0], "nmin": mn[1], "pmin": min(mn[2]),
            "veces": max(mx[2]) / min(mn[2])}
REPO = "github.com/tu-usuario/indice-z"


@st.cache_data(show_spinner=False)
def cargar(carpeta: str = "heritage"):
    d = VINTAGES / carpeta
    if not (d / "indice.csv").exists():
        return None
    return {"ind": pd.read_csv(d / "indice.csv"),
            "scores": pd.read_csv(d / "scores.csv"),
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


# ===========================================================================
def arbol_subfactores(f, L, compacto=False):
    """Bloques del mismo ancho, cortados en tantos pedazos como subfactores
    declara cada componente.

    Hace visible que peso igual entre componentes no es peso igual entre
    indicadores. No son manipulables: Heritage publica su existencia y su
    cantidad, no sus valores por país.
    """
    if not compacto:
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
        etiqueta = (f"{cada[0]:.2f}%" if len({round(c, 4) for c in cada}) == 1
                    else f"{max(cada):.2f}% / {min(cada):.2f}%")
        marca = "" if sf.get("verificado") else " *"
        unidad = t("indicador", L) if n == 1 else t("indicadores", L)
        filas.append(
            f'<div class="sfrow"><div>{txt(ci["titulo"], L)}{marca}'
            f'<div class="sfn">{n} {unidad}</div></div>'
            f'<div class="sfbar">{segs}</div>'
            f'<div class="sfpeso">{etiqueta}</div></div>')
    st.markdown("".join(filas), unsafe_allow_html=True)
    if cadas and not compacto:
        st.markdown(
            f'<div class="nota">'
            f'{t("arbol_conclusion", L).format(v=f"{max(cadas) / min(cadas):.0f}")}'
            f'</div>', unsafe_allow_html=True)
        st.caption(t("arbol_nota", L))


@st.dialog(" ", width="large")
def tutorial(f, L):
    """Un componente por vez, en ventana flotante.

    Los botones usan `on_click` en vez de st.rerun(): dentro de un diálogo,
    st.rerun() lo cierra, mientras que un callback vuelve a dibujar sólo el
    diálogo y el paso avanza sin perder la pantalla de atrás.
    """
    comps = list(f["componentes"])
    paso = min(ss.tut_paso, len(comps))

    st.markdown(f'<div class="cintillo">{t("tut_titulo", L)}</div>',
                unsafe_allow_html=True)

    if paso < len(comps):
        c = comps[paso]
        ci = f["componentes"][c]
        st.progress((paso + 1) / (len(comps) + 1),
                    text=t("tut_paso", L).format(i=paso + 1, n=len(comps)))
        st.markdown(f"### {txt(ci['titulo'], L)}")
        st.caption(txt(f["pilares"][ci["pilar"]]["titulo"], L))
        st.write(txt(ci.get("definicion"), L))

        sf = ci.get("subfactores")
        if sf and sf["n"] > 1:
            st.info(t("tut_ojo", L).format(n=sf["n"]))

        st.markdown(f"**{t('tut_pregunta', L)}**")
        valor = st.slider(f"{t('tut_nada', L)} → {t('tut_mucho', L)}", 0, 10,
                          ss.tut_notas.get(c, 5), 1, key=f"tn_{c}")
        ss.tut_notas[c] = valor

        b1, b2, b3 = st.columns([1, 1, 1])
        b1.button(t("tut_anterior", L), disabled=paso == 0,
                  use_container_width=True,
                  on_click=lambda: ss.__setitem__("tut_paso", paso - 1))
        b2.button(t("tut_cancelar", L), use_container_width=True,
                  on_click=lambda: ss.__setitem__("tutorial", False))
        b3.button(t("tut_siguiente", L), type="primary",
                  use_container_width=True,
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
        f'{sum(notas[c] for c, i in f["componentes"].items() if i["pilar"] == k) / total:.1%}'
        f'</b></div>' for k, v in f["pilares"].items()), unsafe_allow_html=True)

    b1, b2 = st.columns(2)
    b1.button(t("tut_anterior", L), use_container_width=True,
              on_click=lambda: ss.__setitem__("tut_paso", paso - 1))

    def aplicar():
        ss.tutorial = False
        ss.puntos = {c: notas[c] * 5 for c in comps}
        ss.ver += 1

    b2.button(t("tut_aplicar", L), type="primary", use_container_width=True,
              on_click=aplicar)


@st.dialog(" ", width="large")
def ayuda(datos, puntos, pesos, anio, foco, L):
    f, m = datos["f"], datos["f"]["meta"]
    st.markdown(f"## {t('como_funciona', L)}")
    p = st.tabs([t("ayuda_p1", L), t("ayuda_p2", L), t("ayuda_p3", L),
                 t("ayuda_p4", L), t("ayuda_p5", L)])

    with p[0]:
        st.write(t("ayuda_1", L))
        st.markdown(f"##### {t('peso_resultante', L)}")
        st.caption(t("peso_resultante_ayuda", L))
        st.markdown("".join(
            f'<div class="pil"><span>{txt(v["titulo"], L)}</span>'
            f'<b>{pesos["pilar"][k]:.1%}</b></div>'
            for k, v in f["pilares"].items()), unsafe_allow_html=True)

    with p[1]:
        st.write(t("ayuda_2", L))
        fu = m["fuente"]
        st.markdown(f"**{fu['publicador']}** — {fu['dataset']}")
        st.markdown(f"[{fu.get('url_datos', '')}]({fu.get('url_datos', '')})")
        st.caption(f"`{fu.get('archivo', '')}` · {t('m_corte', L)} "
                   f"{m.get('fecha_corte', '')}")
        if fu.get("nota"):
            st.caption(txt(fu["nota"], L))
        for k, r in (f.get("rezagos") or {}).items():
            st.info(t("esc_rezago", L).format(
                comp=txt(f["componentes"][k]["titulo"], L),
                a1=r["anio_dato"], a2=r["anio_asignado"], n=r["paises"]))
        st.download_button(t("esc_descargar", L),
                           datos["ind"].to_csv(index=False).encode("utf-8"),
                           file_name=f"indice_{anio}.csv", mime="text/csv",
                           use_container_width=True)

    with p[2]:
        st.markdown(f"**{nombre(foco)} · {anio}**")
        sc, ind = datos["scores"], datos["ind"]
        fs = sc[(sc.iso3 == foco) & (sc.anio == anio)]
        fi = ind[(ind.iso3 == foco) & (ind.anio == anio)]
        if len(fs) and len(fi):
            fs = fs.iloc[0]
            acum = 0.0
            for cn, ci in f["componentes"].items():
                w = pesos["comp"].get(cn, 0)
                if w <= 0 or cn not in fs or pd.isna(fs[cn]):
                    continue
                aporte = fs[cn] * w
                acum += aporte
                col = (ci.get("fuente") or {}).get("columna", "")
                st.markdown(
                    f'<div class="paso">{txt(ci["titulo"], L)} '
                    f'<span style="color:var(--tenue)">· {col}</span> → '
                    f'<b>{fs[cn]:.1f}</b> × {w:.1%} = <b>{aporte:.2f}</b></div>',
                    unsafe_allow_html=True)
            st.markdown(f'<div class="paso" style="border:0;font-size:1.05rem">'
                        f'<b>= {acum:.1f}</b></div>', unsafe_allow_html=True)

    with p[3]:
        st.write(t("ayuda_4", L))
        val = f.get("validacion", {})
        if val.get("disponible"):
            marca = "ok" if val["cierra"] else "no"
            st.markdown(f'**{t("esc_validacion", L)}** '
                        f'<span class="etq {marca}">máx '
                        f'{val["diferencia_maxima"]}</span> · '
                        f'{val["paises_comparados"]} obs.',
                        unsafe_allow_html=True)
        for cn, ci in f["componentes"].items():
            with st.expander(txt(ci["titulo"], L)):
                st.write(txt(ci.get("definicion"), L))
                fu2 = ci.get("fuente") or {}
                if fu2.get("publicador"):
                    st.caption(f"{fu2['publicador']} — {fu2.get('dataset', '')}")
                if fu2.get("columna"):
                    st.caption(f"{t('esc_columna', L)}: `{fu2['columna']}`")
                if fu2.get("insumos"):
                    st.caption(f"{t('esc_insumos', L)}: {fu2['insumos']}")
                if ci.get("formula"):
                    st.caption(f"{t('esc_formula', L)}: {ci['formula']}")
                if ci.get("reproducible"):
                    st.caption(t(f"repro_{ci['reproducible']}", L))
                if fu2.get("advertencia"):
                    st.warning(txt(fu2["advertencia"], L))

    with p[4]:
        if m.get("ausencias"):
            st.write(txt(m["ausencias"], L))
        nc = m.get("no_calificados", {})
        if nc:
            st.markdown(f"**{t('esc_no_calificados', L)}**")
            st.write(", ".join(nombre(c) for c in nc.get("paises", [])))
            st.caption(txt(nc.get("nota"), L))
        st.caption(f"{t('repo', L)}: {REPO}")


# ===========================================================================
def main():
    datos = cargar()
    if datos is None:
        st.error(t("sin_datos", ss.lang))
        return
    f, m = datos["f"], datos["f"]["meta"]
    L = ss.lang
    claves = list(f["componentes"])
    presets = f.get("presets", {})
    orig = presets["heritage"]["puntos"]

    # Valores por defecto antes de la barra lateral: si algo falla ahí dentro,
    # main() sigue teniendo con qué seguir en lugar de romper con NameError.
    puntos = dict(orig)
    total = sum(puntos.values())
    modificado = False

    # ---------------- barra lateral: texto + componentes + código ----------
    with st.sidebar:
        c1, c2 = st.columns([3, 2])
        c1.markdown(f'<div class="cintillo">{t("pesos", L)}</div>',
                    unsafe_allow_html=True)
        nl = c2.selectbox("l", ["es", "en"], index=0 if L == "es" else 1,
                          format_func=str.upper, label_visibility="collapsed")
        if nl != ss.lang:
            ss.lang = nl
            st.rerun()
        st.markdown(f'<div class="nota">{t("intro_barra", L)}</div>',
                    unsafe_allow_html=True)

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

        # Formulario: Streamlit no recalcula la página en cada tecla, sólo al
        # apretar Aplicar. Con trece campos sueltos, cada pulsación disparaba
        # un recálculo completo de los 176 países y la barra se trababa.
        with st.form("pesos", border=False):
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
                        pct = (f' · <b>{pi[1]:.2f}%</b> {t("cada_uno", L)}'
                               if pi else "")
                        detalle = f'<span class="sfn">{n} {unidad}{pct}</span>'
                    col1, col2 = st.columns([1, 0.42])
                    col1.markdown(
                        f'<div class="wrow" data-c="{c}">'
                        f'<span><i class="chip" style="background:{color[c]}">'
                        f'</i>{txt(ci["titulo"], L)}{detalle}</span></div>',
                        unsafe_allow_html=True)
                    puntos[c] = col2.number_input(
                        txt(ci["titulo"], L), 0, 100,
                        int(base.get(c, orig.get(c, 0))), 5,
                        key=f"pt_{c}_{ss.ver}", label_visibility="collapsed")
            aplicado = st.form_submit_button(t("aplicar_pesos", L),
                                             type="primary",
                                             use_container_width=True)
        if aplicado:
            ss.puntos = dict(puntos)
            st.rerun()

        puntos = dict(base)
        total = sum(puntos.values())
        modificado = any(puntos[k] != orig.get(k, 0) for k in claves)

        pi = [peso_ind(c) for c in f["componentes"]]
        pi = [x for x in pi if x]
        if pi:
            st.caption(t("peso_por_ind_ayuda", L).format(
                v=f"{max(x[2] for x in pi) / min(x[1] for x in pi):.0f}"))

        st.divider()
        st.markdown(f'<div class="cintillo">{t("codigo_config", L)}</div>',
                    unsafe_allow_html=True)
        codigo = cod.codificar(m["sigla"], puntos, claves)
        st.code(codigo, language=None)
        st.caption(t("codigo_ayuda", L))
        e = st.text_input("cod", placeholder=cod.codificar(m["sigla"], orig, claves),
                          label_visibility="collapsed")
        if st.button(t("aplicar_codigo", L), use_container_width=True) and e:
            r = cod.decodificar(e, claves)
            if r:
                cargar_puntos(r)
                st.rerun()
            st.error(t("codigo_invalido", L))

    if total <= 0:
        st.warning(t("sin_datos", L))
        return
    pesos_comp = cod.pesos_desde_puntos(puntos)
    pesos_pilar = {}
    for pil in f["pilares"]:
        pesos_pilar[pil] = sum(pesos_comp[c] for c, i in f["componentes"].items()
                               if i["pilar"] == pil)
    pesos = {"comp": pesos_comp, "pilar": pesos_pilar}

    # ---------------- encabezado ----------------
    izq, der = st.columns([5, 1.15])
    with izq:
        st.markdown(f'<div class="cintillo">{m["fuente"]["publicador"]} · '
                    f'{t("m_corte", L)} {m.get("fecha_corte", "")}</div>',
                    unsafe_allow_html=True)
        st.markdown(f"# {t('titulo_propio', L) if modificado else txt(m['nombre'], L)}")
        st.markdown(
            f'<p class="bajada">'
            f'{t("sub_propio", L) if modificado else txt(m.get("descripcion"), L)}'
            f'</p>', unsafe_allow_html=True)
        ctr = contraste(f, pesos_comp)
        if ctr:
            with st.container(border=True):
                st.markdown(t("titular", L).format(
                    cmax=txt(f["componentes"][ctr["cmax"]]["titulo"], L),
                    nmax=ctr["nmax"],
                    cmin=txt(f["componentes"][ctr["cmin"]]["titulo"], L),
                    nmin=ctr["nmin"], pmin=f'{ctr["pmin"]:.2f}%',
                    pmax=f'{ctr["pmax"]:.2f}%', veces=f'{ctr["veces"]:.0f}'))

    # ---------------- controles en horizontal ----------------
    ind_all = datos["ind"]
    anios_ok = [int(a) for a in sorted(ind_all[ind_all.publicable].anio.unique())]
    g = st.columns([1.5, 1, 0.9, 1.1, 2.4])

    opciones = list(presets) + (["propio"] if modificado else [])
    etiq = {k: txt(v["nombre"], L) for k, v in presets.items()}
    etiq["propio"] = t("titulo_propio", L)
    actual = "propio" if modificado else "heritage"
    sel = g[0].selectbox(t("elegir_indice", L), opciones,
                         index=opciones.index(actual),
                         format_func=lambda k: etiq[k],
                         help=txt(presets.get(actual, {}).get("descripcion"), L))
    if sel != actual and sel in presets:
        cargar_puntos(presets[sel]["puntos"])
        st.rerun()

    anio = g[1].selectbox(t("anio", L), anios_ok, index=len(anios_ok) - 1,
                      key="v_anio")
    cuantos = g[2].number_input(t("mostrar", L), 5, 200, 25, 5, key="v_cuantos")
    min_cob = g[3].slider(t("cobertura_min", L), 0.0, 1.0,
                          float(m["cobertura_minima"]), 0.05, key="v_cob",
                          help=t("cobertura_ayuda", L))
    ind_a = ind_all[ind_all.anio == anio].set_index("iso3")
    seguidos = g[4].multiselect(
        t("seguir", L), sorted(ind_a.index),
        default=[c for c in ("SGP", "NOR", "ARG", "USA") if c in ind_a.index],
        format_func=nombre, key="v_seg", help=t("seguir_ayuda", L))

    with der:
        st.write("")
        if st.button(t("como_funciona", L), use_container_width=True,
                     type="secondary"):
            foco = seguidos[0] if seguidos else "SGP"
            ayuda(datos, puntos, pesos, anio, foco, L)
        if st.button(t("tut_boton", L), use_container_width=True, type="primary"):
            ss.tutorial = True
            ss.tut_paso = 0
            ss.tut_notas = {}
            st.rerun()
        if modificado and st.button(t("volver_heritage", L),
                                    use_container_width=True):
            cargar_puntos(orig)
            st.rerun()

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
    if "cumplimiento" in ind_a.columns:
        vivo["cumplimiento"] = ind_a["cumplimiento"]
    vivo["publicable"] = vivo["cobertura"] >= min_cob
    vivo["ranking"] = vivo.where(vivo.publicable)["indice"].rank(
        ascending=False, method="min")
    vivo["rank_orig"] = ind_a["ranking"]

    huerfanos = [txt(f["pilares"][p]["titulo"], L) for p in f["pilares"]
                 if pesos_pilar[p] > 0 and vivo[p].notna().sum() == 0]
    if huerfanos:
        st.markdown(f'<div class="aviso">'
                    f'{t("aviso_sin_dato", L).format(p=", ".join(huerfanos), a=anio)}'
                    f'</div>', unsafe_allow_html=True)

    # ---------------- pestañas ----------------
    tabs = st.tabs([t("v_arbol", L), t("v_ranking", L), t("v_dispersion", L)])

    with tabs[1]:
        color = paleta(f)
        activos = [c for c in claves if pesos_comp.get(c, 0) > 0]
        n_pub = max(int(vivo.publicable.sum()), 1)

        def fila(iso3, r, marcar=False):
            # Cada tramo mide puntaje_del_componente x peso_del_componente, así
            # que la suma de los tramos es el índice y el largo total es
            # comparable entre países.
            segs = ""
            for c in claves:
                v = sc_a[c].get(iso3) if c in sc_a.columns else None
                if v is None or pd.isna(v):
                    continue
                segs += (f'<div class="seg" data-c="{c}" '
                         f'style="width:{v * pesos_comp[c]:.3f}%;'
                         f'--solo:{v:.2f}%;background:{color[c]}" '
                         f'title="{txt(f["componentes"][c]["titulo"], L)}: '
                         f'{v:.1f} × {pesos_comp[c]:.1%}"></div>')
            if pd.isna(r.get("rank_orig")) or r["rank_orig"] == r["ranking"]:
                vs = (f'{int(r["rank_orig"])}'
                      if pd.notna(r.get("rank_orig")) else "—")
            else:
                d = int(r["rank_orig"] - r["ranking"])
                vs = (f'{int(r["rank_orig"])} '
                      f'<span class="{"sube" if d > 0 else "baja"}">'
                      f'{"▲" if d > 0 else "▼"}{abs(d)}</span>')
            return (f'<div class="fila{" seguido" if marcar else ""}">'
                    f'<div class="pos">{int(r["ranking"])}</div>'
                    f'<div class="pais">{nombre(iso3)}</div>'
                    f'<div class="barra">{segs}</div>'
                    f'<div class="val">{r["indice"]:.1f}</div>'
                    f'<div class="vs">{vs}</div></div>')

        tabla = vivo[vivo.publicable].nlargest(min(int(cuantos), n_pub), "indice")
        bloque = [
            reglas_hover(claves),
            f'<div class="pista-ayuda">{t("barra_ayuda", L)}</div>',
            f'<div class="cab"><div>{t("col_puesto", L)}</div>'
            f'<div>{t("col_pais", L)}</div><div>{t("col_aporte", L)}</div>'
            f'<div style="text-align:right">{t("col_puntaje", L)}</div>'
            f'<div style="text-align:right">{t("col_vs", L)}</div></div>',
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
                       + ", ".join(nombre(c) for c in sin))

        st.write("")
        try:
            from pdf import generar
            filas_pdf = [(int(r["ranking"]), nombre(i), r["indice"],
                          r["rank_orig"] if pd.notna(r.get("rank_orig")) else None)
                         for i, r in tabla.iterrows()]
            blob = generar(
                t("titulo_propio", L) if modificado else txt(m["nombre"], L),
                t("sub_propio", L) if modificado else txt(m.get("descripcion"), L),
                filas_pdf,
                {"codigo": codigo, "repo": REPO,
                 "fuente": m["fuente"]["publicador"],
                 "corte": m.get("fecha_corte", ""), "anio": anio,
                 "procedencia": f"{m['fuente']['dataset']}. "
                                f"{m['fuente'].get('url_datos', '')}"},
                {"codigo": t("codigo_config", L), "corte": t("m_corte", L),
                 "anio": t("anio", L), "ponderacion": t("pdf_ponderacion", L),
                 "puesto": t("col_puesto", L), "pais": t("col_pais", L),
                 "puntaje": t("col_puntaje", L), "comparacion": t("col_vs", L),
                 "procedencia": t("pdf_procedencia", L)},
                [(txt(v["titulo"], L), f"{pesos_pilar[k]:.1%}")
                 for k, v in f["pilares"].items() if pesos_pilar[k] > 0])
            st.download_button(t("imprimir", L), blob,
                               file_name=f"indice_{anio}_{codigo}.pdf",
                               mime="application/pdf")
        except ImportError:
            pass

    with tabs[2]:
        if "cumplimiento" in vivo.columns and vivo["cumplimiento"].notna().any():
            st.markdown(f'<div class="nota">{t("disp_ayuda", L)}</div>',
                        unsafe_allow_html=True)
            base_d = vivo[vivo.publicable].reset_index()
            base_d["pais"] = base_d["iso3"].map(nombre)
            base_d["seguido"] = base_d["iso3"].isin(seguidos)
            try:
                import altair as alt
                st.altair_chart(
                    alt.Chart(base_d).mark_circle(opacity=.8).encode(
                        x=alt.X("indice", title=t("eje_x", L)),
                        y=alt.Y("cumplimiento",
                                title=txt(f["eje_cumplimiento"]["titulo"], L)),
                        color=alt.condition(alt.datum.seguido,
                                            alt.value("#A8412F"),
                                            alt.value("#0F6B5C")),
                        size=alt.condition(alt.datum.seguido,
                                           alt.value(230), alt.value(70)),
                        tooltip=["pais", "indice", "cumplimiento"],
                    ).properties(height=470).interactive(),
                    use_container_width=True)
            except ImportError:
                st.scatter_chart(base_d, x="indice", y="cumplimiento")


main()
