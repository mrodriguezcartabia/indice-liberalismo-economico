# Reconstruir el índice desde las fuentes

Objetivo: recalcular cada componente de Heritage desde los datos originales que
ellos declaran, y compararlo contra el puntaje que publican.

Ese contraste es el producto. Si un componente cierra, queda demostrado que el
índice es auditable y quedan publicados sus subfactores por país. Si no cierra,
queda documentado que la metodología publicada no alcanza para reproducirlo.
Las dos cosas son resultados.

---

## Qué es reconstruible y qué no

| Componente | Estado | Qué hace falta |
|---|---|---|
| Gasto público | **completo** | gasto/PBI |
| Salud fiscal | **completo** | déficit y deuda/PBI |
| Carga tributaria | **completo** | alícuota personal, corporativa, recaudación/PBI |
| Libertad monetaria | base sí, castigo no | inflación · el descuento por controles de precios no se publica |
| Libertad comercial | base sí, castigo no | arancel promedio · el descuento por barreras no se publica |
| Libertad laboral | **completo** | 9 subfactores, fórmula publicada |
| Libertad de empresa | probable | 4 subfactores de fuentes públicas |
| Derechos de propiedad | probable | 3 fuentes, ponderación interna no declarada |
| Efectividad judicial | probable | 2 fuentes |
| Integridad del gobierno | probable | 3 fuentes |
| Libertad de inversión | **imposible** | descuentos cualitativos, sin insumo |
| Libertad financiera | **imposible** | escalones asignados a criterio |

**Diez de doce son reconstruibles. Dos nunca.** Ese dato ya es publicable.

Las dos filas de "castigo no publicado" son las más interesantes: con la base
calculada y el puntaje publicado, se despeja por resta **la penalización
discrecional que Heritage aplicó a cada país sin declararla**.

---

## Tanda 1 — La más rentable: dos archivos

Rinde tres componentes completos y el despeje del castigo monetario.

### 1.1 · FMI, World Economic Outlook

`imf.org/en/Publications/WEO/weo-database` → última edición → **By Countries** →
seleccionar todos los países y todos los años → descargar el archivo tabulado.

Trae en una sola descarga las cuatro series que necesitamos:

| Serie WEO | Para qué |
|---|---|
| `GGX_NGDP` | gasto público / PBI → **Gasto público** |
| `GGXCNL_NGDP` | resultado fiscal / PBI → **Salud fiscal** |
| `GGXWDG_NGDP` | deuda bruta / PBI → **Salud fiscal** |
| `PCPIPCH` | inflación anual | → base de **Libertad monetaria** |

### 1.2 · Banco Mundial, recaudación tributaria

Indicador `GC.TAX.TOTL.GD.ZS`. Se baja solo con el adaptador que ya está escrito:

```bash
python -c "import sys; sys.path.insert(0,'src'); import sources; sources.fetch_worldbank('GC.TAX.TOTL.GD.ZS')"
```

### 1.3 · Alícuotas máximas

No hay descarga única. PwC *Worldwide Tax Summaries* las publica país por país.
Para arrancar alcanza con cargar a mano las treinta economías que importan para
la nota, y declarar la cobertura parcial.

**Fórmulas, ya verificadas:**

```
Gasto público   = 100 − 0,03 · G²                       G = gasto/PBI, promedio 3 años
Salud fiscal    = 0,8·(100 − 2·D²) + 0,2·(100 − 0,01·B²)
Carga tributaria = promedio de tres subfactores 100 − 0,03·x²
Libertad monetaria = 100 − 6,333·√(inflación ponderada) − castigo
                     pesos 0,665 / 0,245 / 0,090 para t, t−1, t−2
```

---

## Tanda 2 — Libertad laboral y sus nueve subfactores

El componente con más indicadores adentro y el que ninguna otra publicación
desagrega.

**Banco Mundial, Employing Workers** — `worldbank.org`, sección Employing
Workers. Cubre los subfactores 1 a 6 y los dos binarios.

**ILOSTAT** — `ilostat.ilo.org/data`, dos indicadores: tasa de participación en
la fuerza de trabajo, y productividad laboral (producto por persona ocupada).

**Fórmula publicada**, para los primeros siete subfactores:

```
Subfactor_i = 50 × (promedio_mundial / valor_i)
```

Los dos últimos son binarios: 100 si la restricción no existe, 0 si existe.

**La ambigüedad a resolver:** Heritage no dice sobre qué conjunto de países
calcula el promedio mundial. Hay que probar con los 176 que califica y con
todos los que tienen dato, y quedarse con el que reproduzca sus puntajes.

---

## Tanda 3 — Estado de derecho y libertad de empresa

Cuatro componentes, cinco fuentes, todas gratuitas.

| Fuente | Dónde | Alimenta |
|---|---|---|
| Worldwide Governance Indicators | Banco Mundial, API | propiedad, judicial, integridad, empresa |
| Transparency International CPI | `transparency.org/cpi` | integridad |
| TRACE Bribery Risk Matrix | `traceinternational.org` | integridad |
| Freedom House, Freedom in the World | `freedomhouse.org` | judicial |
| WDI acceso a electricidad | `EG.ELC.ACCS.ZS`, API | empresa |
| Women, Business and the Law | Banco Mundial | empresa |

Acá el obstáculo no son los datos sino la **ponderación interna**: Heritage dice
qué fuentes usa pero no con qué peso las combina. Habrá que estimarla por ajuste
y declarar que es una estimación.

Credendo y el IP Index de la Cámara de Comercio de EE.UU. quedan como pendientes:
el segundo cubre unas cincuenta economías, así que limita la cobertura.

---

## Tanda 4 — Libertad comercial

**OMC, World Tariff Profiles** — `wto.org`, arancel promedio ponderado.

```
Libertad comercial = 100 · (50 − arancel) / 50 − castigo
```

Con el puntaje publicado se despeja el castigo por barreras no arancelarias.

---

## Cómo entra cada archivo

Siempre igual, sin excepciones:

```bash
python src/cargar.py inspeccionar ~/Descargas/ARCHIVO.xlsx
python src/cargar.py convertir ~/Descargas/ARCHIVO.xlsx --saltar N \
    --pais "COLUMNA" --col-anio "AÑO" --varios "Columna=serie"
python src/build.py --config config/heritage.yaml
```

**Lo que necesito de vos por cada fuente:** el archivo bajado y la salida del
comando `inspeccionar`. Con eso escribo el comando de conversión con los nombres
de columna exactos y el cálculo del componente.

No puedo bajarlos yo: mi entorno de código no tiene salida a internet.

---

## El test que decide todo

Cada componente reconstruido se compara contra el que Heritage publica:

```
diferencia = |componente_recalculado − componente_publicado|
```

Es el mismo test que ya valida la réplica del índice completo, que cierra con
una diferencia máxima de 0,067 puntos en 176 países.

Un componente que cierre por debajo de 1 punto está reproducido. Uno que no
cierre marca un hueco entre lo que la metodología declara y lo que el número
publicado contiene — y hay que decirlo con cuidado, porque no se puede distinguir
un error de ellos de un error nuestro.

---

## Lo que cambia en el argumento

Reponderar el índice de Heritage es usar sus datos y discutir su método.
Reconstruirlo es usar **las fuentes originales** y discutir su implementación.

Es más ambicioso y también más discutible: pasás a tener que defender tus
propias decisiones de cálculo. Conviene hacerlo como una segunda etapa
declarada, con la reponderación ya publicada y funcionando.

---

## Orden sugerido

1. **Tanda 1.** Dos archivos, tres componentes completos, y el primer despeje de
   un castigo no publicado. Es la que más rinde por hora invertida.
2. **Tanda 2.** Libertad laboral con sus nueve subfactores, que además vuelve
   manipulables esos pesos en la app.
3. **Tanda 4.** Libertad comercial, para tener los dos castigos despejados.
4. **Tanda 3.** La más trabajosa y la de resultado más incierto, por la
   ponderación interna no declarada.

Inversión y financiera quedan fuera para siempre, y publicar eso —16,7% del
índice sin insumo auditable— es en sí mismo un resultado.
