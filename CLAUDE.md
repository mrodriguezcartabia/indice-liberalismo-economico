# App: Índice de Liberalismo Económico

## Qué es
Página que compara la réplica del Index of Economic Freedom de Heritage con un índice propio, el Índice de Liberalismo Económico, que pone arriba a los países con menor presencia del Estado. Un tercer índice lo arma el visitante con sus pesos. App en Streamlit publicada en Streamlit Cloud desde la rama main de GitHub. La app es bilingüe (español/inglés): todo texto visible va en los dos idiomas.

## Idioma
- Conversación conmigo: español rioplatense.

## Estructura
- Archivo principal de la app: app/streamlit_app.py
- Módulos que usa la app y el pipeline: src/*.py
- Textos de la interfaz en los dos idiomas: src/i18n.py
- Decisiones metodológicas (componentes, pesos, nombres de los índices): config/heritage.yaml
- Datos de entrada: data/raw/manual/
- Datos que lee la app: data/vintages/. Los genera src/build.py; no editarlos a mano.
- Dependencias: requirements.txt en la raíz (es lo que instala Streamlit Cloud)

## Entorno
- Usar siempre el entorno de la carpeta: .venv/bin/python y .venv/bin/pip. No hace falta activarlo.
- Toda biblioteca nueva: instalarla con .venv/bin/pip y agregarla a requirements.txt en el mismo cambio. Si falta en requirements.txt, la app publicada se rompe.

## Cómo trabajar
- Antes de editar, crear una rama nueva desde main con un nombre descriptivo (git switch -c nombre). Nunca editar directamente en main.
- No correr "streamlit run": la app ya la tengo corriendo yo en otra terminal y se recarga sola.
- Después de cada cambio, correr la prueba desde la raíz: .venv/bin/python src/prueba_humo.py. Si se agregan pruebas con pytest en tests/, correr también .venv/bin/python -m pytest.
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
