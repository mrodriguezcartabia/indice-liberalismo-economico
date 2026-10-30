"""Prueba de humo: ejecuta main() con un streamlit simulado.

No verifica el aspecto visual, pero atrapa NameError, KeyError y errores de
logica antes de levantar el servidor, que es exactamente lo que se nos escapo.
"""
import re, sys, types
from pathlib import Path
sys.path.insert(0, "src")

class Col:
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def __getattr__(self, n): return getattr(sys.modules["streamlit"], n)

class Estado(dict):
    """Imita st.session_state: acceso por punto y por clave."""
    def __getattr__(self, k):
        try: return self[k]
        except KeyError: raise AttributeError(k)
    def __setattr__(self, k, v): self[k] = v
    def setdefault(self, k, v=None): return super().setdefault(k, v)


class ST(types.ModuleType):
    session_state = Estado()
    query_params = {}
    column_config = types.SimpleNamespace(
        TextColumn=lambda *a, **k: None, NumberColumn=lambda *a, **k: None)
    sidebar = Col()
    def cache_data(self, *a, **k):
        if a and callable(a[0]): return a[0]
        return lambda fn: fn
    def dialog(self, *a, **k): return lambda fn: fn
    def columns(self, spec, **k):
        n = len(spec) if isinstance(spec, (list, tuple)) else spec
        return [Col() for _ in range(n)]
    def tabs(self, labels, **k): return [Col() for _ in labels]
    def form(self, *a, **k): return Col()
    def container(self, *a, **k): return Col()
    def expander(self, *a, **k): return Col()
    def number_input(self, label, mn=0, mx=100, val=0, step=1, **k):
        if "key" in k and k["key"] in ST.session_state:   # widget con clave
            return int(ST.session_state[k["key"]])
        return int(k.get("value", val))
    def slider(self, label, mn=0, mx=10, val=5, step=1, **k): return val
    def selectbox(self, label, opciones, index=0, **k):
        if "key" in k and k["key"] in ST.session_state:     # widget con clave
            return ST.session_state[k["key"]]
        return list(opciones)[index] if len(opciones) else None
    def multiselect(self, label, opciones, default=None, **k): return default or []
    def text_input(self, *a, **k): return ""
    def button(self, *a, **k): return False
    def form_submit_button(self, *a, **k): return False
    def download_button(self, *a, **k): return False
    def progress(self, *a, **k): return None
    def __getattr__(self, nombre): return lambda *a, **k: None

st = ST("streamlit"); sys.modules["streamlit"] = st
ruta = Path("app/streamlit_app.py")
src = ruta.read_text().replace("\nmain()\n", "\n")
ns = {"__name__": "app", "__file__": str(ruta.resolve())}
exec(compile(src, str(ruta), "exec"), ns)

BASE = {"lang": "es", "puntos": None, "tutorial": False, "ver": 0,
        "tut_paso": 0, "tut_notas": {}}
f0 = ns["cargar"]()["f"]
Z = f0["presets"]["liberalismo"]["puntos"]

for etiqueta, extra in [("Heritage", {}),
                        ("preset liberalismo", {"puntos": Z, "ver": 1}),
                        ("tutorial abierto", {"tutorial": True}),
                        ("todo en cero salvo uno",
                         {"puntos": {k: (10 if k == "hf_tax_burden" else 0)
                                     for k in f0["componentes"]}}),
                        ("en inglés", {"lang": "en"}),
                        ("en inglés con tutorial", {"lang": "en", "tutorial": True})]:
    ST.session_state = Estado({**BASE, **extra})
    ns["ss"] = ST.session_state
    ns["main"]()
    print(f"  main() OK — {etiqueta}")

# Códigos publicados antes de sumar componentes: tienen que seguir leyéndose
# igual. Si esto falla, un PDF o un link viejo mostraría otra configuración.
import codigo as cod
claves_cod = f0["orden_codigo"]
viejas = claves_cod[2:]                    # las 18 claves anteriores a OCDE y FMI
mezcla = {c: 5 * (i % 4) for i, c in enumerate(viejas)}
# Configuración del índice propio hasta octubre de 2026 (13 componentes).
LIBERALISMO_2026_10 = {c: 10 for c in (
    "hf_property_rights", "hf_judicial_effectiveness", "hf_tax_burden",
    "hf_government_spending", "hf_fiscal_health", "hf_monetary_freedom",
    "hf_trade_freedom", "z_propiedad_estatal", "z_inversion_publica",
    "z_controles_capital", "z_regulacion_credito", "z_consumo_publico",
    "z_entrada_mercados")}
for viejo, esperado in [("HF-I7ZY0", f0["presets"]["heritage"]["puntos"]),
                        ("HF-I6WSZ", LIBERALISMO_2026_10),
                        ("HF-P0001-AQE4-GRPJ-AVGS-WS", mezcla)]:
    leido = cod.decodificar(viejo, claves_cod)
    assert leido and all(leido[k] == esperado.get(k, 0) for k in claves_cod), viejo
print("  códigos publicados OK")

# El aviso de superposición tiene que aparecer cuando los dos están activos.
salida = []
st.markdown = lambda x="", *a, **k: salida.append(str(x))
ST.session_state = Estado({**BASE, "puntos": {k: (10 if k in ("hf_government_spending",
                                                    "fmi_gasto_publico") else 0)
                                              for k in f0["componentes"]}})
ns["ss"] = ST.session_state
ns["main"]()
assert any("miden casi lo mismo" in x for x in salida), "no apareció el aviso de superposición"
print("  aviso de superposición OK")
assert any('class="pop"' in x and "Gasto total del gobierno general" in x for x in salida), \
    "no apareció la definición en la ventana emergente"
print("  ventana con la definición OK")

# Con un preset activo, su propia columna de referencia no puede mostrar
# movimientos: es el mismo ranking.
for nombre in f0["presets"]:
    salida.clear()
    ST.session_state = Estado({**BASE, "puntos": dict(f0["presets"][nombre]["puntos"])})
    ns["ss"] = ST.session_state
    ns["main"]()
    tabla = "".join(salida)
    filas = [x for x in tabla.split('<div class="fila') if 'class="pos"' in x]
    orden = [n for n in ("liberalismo", "heritage") if n in f0["presets"]]
    propia = [re.findall(r'<div class="vs">(.*?)</div>', x)[orden.index(nombre)] for x in filas]
    assert filas and not any("▲" in c or "▼" in c for c in propia), \
        f"la columna {nombre} muestra movimientos contra sí misma"
print("  referencias sin movimientos contra sí mismas OK")

# Con Heritage, los componentes de Estado de derecho que superan el umbral
# de superposición salen en un solo aviso, no en uno por par.
salida.clear()
ST.session_state = Estado({**BASE, "puntos": dict(f0["presets"]["heritage"]["puntos"])})
ns["ss"] = ST.session_state
ns["main"]()
avisos = [x for x in salida if "miden casi" in x]
assert len(avisos) == 1 and " e «Integridad" in avisos[0], avisos
print("  avisos de superposición agrupados OK")

# Con todos los datos, el largo de la barra (suma de los tramos) es el puntaje.
# Con alguno faltante (Haití no tiene presión fiscal, y aparece bajando la
# cobertura a 90), la barra es más corta y el nombre lleva asterisco.
salida.clear()
ST.session_state = Estado({**BASE, "sel_cob": 90,
                           "puntos": dict(f0["presets"]["liberalismo"]["puntos"])})
ns["ss"] = ST.session_state
ns["main"]()
html_ = "".join(salida)
vistos = 0
for x in html_.split('<div class="fila')[1:]:
    largo = sum(float(w) for w in re.findall(r'class="seg"[^>]*style="width:([\d.]+)%', x))
    puntaje = re.search(r'<div class="val">([\d.,]+)</div>', x)
    pais = re.search(r'<div class="pais">([^<]+)</div>', x).group(1)
    if not puntaje:
        continue
    if pais.endswith("*"):
        vistos += 1
        assert largo < float(puntaje.group(1).replace(',', '.')) - 1, (pais, largo, puntaje.group(1))
    else:
        assert abs(largo - float(puntaje.group(1).replace(',', '.'))) < 0.06, (pais, largo, puntaje.group(1))
assert vistos and "Haití*" in html_ and "Sin dato, o con un dato de más de diez años" in html_, vistos
print("  barras y asteriscos de datos faltantes OK")

# Con Heritage activo, los países cuyo puesto difiere del que surge del puntaje
# publicado llevan doble asterisco y una nota que lo explica.
salida.clear()
ST.session_state = Estado({**BASE, "sel_cuantos": 60,
                           "puntos": dict(f0["presets"]["heritage"]["puntos"])})
ns["ss"] = ST.session_state
ns["main"]()
html_ = "".join(salida)
assert re.search(r'class="pais">[^<]+\*\*<', html_) and "** Puesto distinto" in html_
print("  doble asterisco de puestos de Heritage OK")

# Cada barra trae un tramo por componente con dato, también los de peso cero:
# si no, pasar el mouse por uno de ellos deja las barras vacías.
f_ = [x for x in html_.split('<div class="fila')[1:] if 'class="pos"' in x][0]
assert 'data-c="ocde_presion_fiscal"' in f_, "falta el tramo de un componente con peso cero"
print("  tramos de componentes con peso cero OK")
print("prueba de humo superada")
