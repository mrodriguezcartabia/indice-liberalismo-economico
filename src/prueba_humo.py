"""Prueba de humo: ejecuta main() con un streamlit simulado.

No verifica el aspecto visual, pero atrapa NameError, KeyError y errores de
logica antes de levantar el servidor, que es exactamente lo que se nos escapo.
"""
import sys, types
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
    def number_input(self, label, mn=0, mx=100, val=0, step=1, **k): return int(val)
    def slider(self, label, mn=0, mx=10, val=5, step=1, **k): return val
    def selectbox(self, label, opciones, index=0, **k):
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
        "tut_paso": 0, "tut_notas": {}, "esc": False}
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
print("prueba de humo superada")
