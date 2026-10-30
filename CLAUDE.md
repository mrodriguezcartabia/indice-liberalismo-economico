# App: Índice de Liberalismo económico

## Qué es
Página que compara la réplica del Index of Economic Freedom de Heritage con un índice propio, el Índice de Liberalismo económico, que pone arriba a los países con menor presencia del Estado. Un tercer índice lo arma el visitante con sus pesos. App en Streamlit publicada en Streamlit Cloud desde la rama main de GitHub. La app es bilingüe (español/inglés): todo texto visible va en los dos idiomas.

El índice propio mide solo el tamaño y la intervención del Estado: diez componentes con el mismo peso (código HF-I8R9Z), sin los de Estado de derecho. Es una decisión metodológica mía: no la cambies sin preguntarme.

## Idioma
- Conversación conmigo: español rioplatense.
- Todo texto en castellano sigue las normas de la RAE: sin coma antes de "y" salvo los casos que corresponden, "solo" sin tilde, coma decimal ("86,3"), espacio antes de "%" ("8,3 %"), citas con espacio y antes del signo ("…insumo [1]."), sin mayúsculas de énfasis.

## Estructura
- Archivo principal de la app: app/streamlit_app.py
- Módulos que usa la app y el pipeline: src/*.py
- Textos de la interfaz en los dos idiomas: src/i18n.py
- Decisiones metodológicas (componentes, pesos, nombres de los índices, umbrales): config/heritage.yaml
- Datos de entrada: data/raw/manual/
- Datos que lee la app: data/vintages/. Los genera src/build.py; no editarlos a mano.
- Descargas automáticas: src/descargar.py (OCDE, FMI y Heritage 2020 a 2026). Fraser no permite descargas automáticas: se carga a mano siguiendo docs/CARGAR_FRASER.md.
- Fuentes y procedencia de cada dato: docs/FUENTES.md
- Tareas de GitHub: .github/workflows/actualizar-datos.yml (día 5 de cada mes; si hay datos nuevos, abre un pull request para que yo lo revise) y recordatorio-fraser.yml (15 de octubre, abre un aviso con el instructivo).
- Dependencias: requirements.txt en la raíz (es lo que instala Streamlit Cloud)

## Datos y fuentes
- Todo dato de terceros lleva su fuente citada (bloque `fuente` en config/heritage.yaml y docs/FUENTES.md), lo exija o no quien lo publica.
- Si un sitio bloquea las descargas automáticas, no forzarlo (nada de hacerse pasar por un navegador): se carga a mano.
- Para cada año, los componentes que no son de Heritage usan el último dato de cada país hasta ese año, si no tiene más de diez años (meta.antiguedad_maxima). Más viejo cuenta como faltante. Faltante nunca es cero.
- Componente nuevo: agregarlo al principio de `orden_codigo` en el config; si no, los códigos compartibles ya publicados cambian de significado.
- La superposición entre componentes es automática: pares con correlación ≥ 0,9 (umbral_superposicion), con un aviso en la app.

## Entorno
- Usar siempre el entorno de la carpeta: .venv/bin/python y .venv/bin/pip. No hace falta activarlo.
- Toda biblioteca nueva: instalarla con .venv/bin/pip y agregarla a requirements.txt en el mismo cambio. Si falta en requirements.txt, la app publicada se rompe.

## Cómo trabajar
- Antes de editar, crear una rama nueva desde main con un nombre descriptivo (git switch -c nombre). Nunca editar directamente en main.
- No correr "streamlit run": la app ya la tengo corriendo yo en otra terminal y se recarga sola. Ojo: los cambios en src/ no se ven hasta reiniciar la app (Ctrl+C y volver a arrancarla); avisame cuando haga falta.
- Después de cada cambio, correr la prueba desde la raíz: .venv/bin/python src/prueba_humo.py. Si se agregan pruebas con pytest en tests/, correr también .venv/bin/python -m pytest.
- La prueba de humo simula Streamlit. Para comprobar la app real (ventanas, botones, avisos de funciones que se eliminan) se puede usar streamlit.testing.v1.AppTest, que no es "streamlit run".
- Detalles de Streamlit 1.66 que ya dieron problemas:
  - Los controles cuyo valor cambia entre recálculos van con clave fija (`key`) y sin valor inicial; si no, la elección se pierde.
  - Las ventanas del "?" solo pueden cambiar de color: tocarles letra, márgenes o alto desarma el recuadro.
  - Dentro del string CSS de la app no puede haber líneas en blanco.
  - Los números que ve el visitante pasan por fmt_num y fmt_pct (coma en castellano, punto en inglés).
- Al terminar, mostrarme un resumen de qué cambió y en qué archivos.

## Publicar
- No hacer git push salvo que yo lo pida explícitamente.
- Cuando lo pida: commit en la rama, pasar a main (git switch main), git merge de la rama, git push, y borrar la rama local.
- Nunca git push --force, nunca git reset --hard.
- No cambiar la configuración de git (user.name, user.email).

## Prohibido
- Escribir claves, contraseñas o tokens en el código. Si hacen falta, van en .streamlit/secrets.toml, que no se sube nunca.
- Borrar datos de data/ sin preguntarme.
- Agregar comentarios que aludan a posiciones políticas, en el código o en la app.
