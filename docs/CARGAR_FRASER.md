# Cargar la edición nueva de Fraser

El Fraser Institute publica el *Economic Freedom of the World* una vez por año,
en general entre septiembre y octubre. Su sitio no permite descargas
automáticas, así que esta carga se hace a mano. Este instructivo es el que
llega en el recordatorio anual del repositorio.

**Si la edición del año todavía no salió**, dejá el aviso abierto y volvé a
mirar en unas semanas.

---

## 1 · Bajar el archivo

1. Entrá con el navegador a https://www.fraserinstitute.org/economic-freedom/dataset
2. Bajá el Excel para investigadores con códigos ISO. El de 2026 se llamaba
   `efotw-2026-master-index-data-for-researchers-iso.xlsx`; el nombre del año
   nuevo debería ser parecido.
3. Guardalo en la carpeta del proyecto (`~/proyectos/app-indice`). No se sube
   a GitHub: el `.gitignore` excluye los `.xlsx`.

## 2 · Cargarlo

**Opción A — con Claude Code (recomendada).** Abrí `claude` en la carpeta del
proyecto y escribí:

> Cargá la edición nueva de Fraser siguiendo docs/CARGAR_FRASER.md. El archivo
> es NOMBRE_DEL_ARCHIVO.xlsx

**Opción B — a mano**, desde la carpeta del proyecto y en una rama nueva
(`git switch -c fraser-AÑO`):

```bash
# 1 · Ver hojas y columnas. Fraser a veces cambia nombres o la fila del
#     encabezado entre ediciones: compará con el bloque del paso 2.
.venv/bin/python src/cargar.py inspeccionar ARCHIVO.xlsx

# 2 · Convertir. Ajustar --hoja y --saltar si el paso 1 muestra otra hoja u
#     otra fila de encabezado (en 2026 la hoja era "EFW Ratings").
#     Los espacios dobles y el "IE" con i mayúscula son literales del original.
.venv/bin/python src/cargar.py convertir ARCHIVO.xlsx \
  --hoja "EFW Ratings" --saltar 3 --pais "Countries" --col-anio "Year" --varios \
  "1A Government consumption=z_consumo_publico" \
  "1B  Transfers and subsidies=z_transferencias" \
  "1D  Top marginal tax rate=z_alicuotas" \
  "IE State ownership=z_propiedad_estatal" \
  "1C  Government investment=z_inversion_publica" \
  "4Dii  Capital controls=z_controles_capital" \
  "5D Freedom to enter markets and compete=z_entrada_mercados" \
  "5A  Credit market regulation=z_regulacion_credito" \
  "Area 2 Legal System & Property Rights -- With Gender Adjustment=z_area2"

# 3 · Regenerar el índice y correr la prueba
.venv/bin/python src/build.py --config config/heritage.yaml
.venv/bin/python src/prueba_humo.py
```

## 3 · Actualizar la cita de la fuente

Todo dato va con su fuente. Con la edición nueva hay que cambiar:

- `config/heritage.yaml`: en cada componente `z_*`, `dataset:` pasa a
  `"Economic Freedom of the World AÑO"`; actualizar también `cobertura:` donde
  figure (países y último año con dato).
- `docs/FUENTES.md`, sección Fraser Institute: dataset, hoja, contenido y el
  nombre del archivo en el comando.

Después, volver a correr `build.py` y la prueba de humo.

## 4 · Revisar y publicar

1. Mirar la app en la compu (menú ⋮ → *Clear cache* y recargar).
2. Si está todo bien, publicar: commit en la rama, merge a `main` y push.
3. Cerrar el aviso de GitHub.
