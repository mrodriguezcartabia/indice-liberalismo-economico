# Índice Z

Página pública para comparar índices de libertad económica bajo distintas
ponderaciones, usando datos publicados por terceros.

La tesis que la página vuelve verificable: **el ranking de un índice compuesto
depende tanto de cómo se ponderan sus componentes como de los datos que usa.**

## Arrancar

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# cargar datos y construir (comandos exactos en docs/FUENTES.md)
python src/build.py --config config/heritage.yaml
python src/build.py --config config/z.yaml

streamlit run app/streamlit_app.py
```

## Estructura

```
config/heritage.yaml   réplica del índice de Heritage, con procedencia completa
config/z.yaml          índice Z, sobre componentes publicados por Fraser
src/build.py           pipeline: panel tidy -> normalización -> pilares -> vintage
src/cargar.py          conversor de planillas descargadas al formato del proyecto
src/normalize.py       escalas 0-100 y agregación en dos niveles
src/countries.py       nombres de país -> ISO3, y nombres para mostrar
src/codigo.py          código corto de configuración de pesos
src/i18n.py            textos de interfaz, castellano e inglés
app/streamlit_app.py   portada, tablero y panel de escrutinio
docs/FUENTES.md        procedencia, comandos y reproducibilidad
```

**El código no contiene ninguna decisión metodológica.** Pesos, direcciones,
normalizaciones y fuentes viven en los `config/*.yaml`. Cualquiera puede abrir
uno de esos archivos, cambiar un peso y volver a correr.

## Reglas del pipeline

**Ponderación en dos niveles.** Primero el peso del pilar, después el reparto
interno. Agregar componentes a un pilar no cambia el peso del pilar.

**Un dato faltante nunca es cero.** Los NaN se propagan y la cobertura se
publica junto al puntaje. Por debajo del umbral, el país se lista aparte en
lugar de puntuarse. Sin esta regla, el índice premiaría a los países con peor
estadística.

**Chequeo de doble conteo.** El build calcula la correlación entre componentes
del mismo pilar y avisa cuando supera 0,7. Dos componentes muy correlacionados
funcionan como uno con peso duplicado.

**Validación de la réplica.** El promedio recalculado se compara contra el
puntaje publicado por la fuente. Diferencia máxima verificada: 0,067 puntos en
176 países.

**Vintages congelados.** Cada corrida guarda su configuración junto a los
resultados. Un ranking publicado es reproducible indefinidamente.

**La app no descarga ni recalcula desde las fuentes.** Lee vintages congelados.
Si calculara en vivo, el número publicado cambiaría según cuándo se entró.

## Pendiente

Los Estados con baja capacidad obtienen puntajes altos en cualquier índice que
mida presencia estatal, porque la coerción que sufren sus habitantes no es
estatal y por lo tanto queda fuera de la medición. Heritage enfrenta lo mismo y
lo resuelve incorporando el estado de derecho como 25% de su puntaje. El índice Z
separa esas dimensiones a propósito, así que necesita declarar su dominio de
validez. Las opciones evaluadas son umbral, media geométrica o dos ejes sin
ranking. Sin decidir.
