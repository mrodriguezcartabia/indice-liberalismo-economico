# Fuentes y procedencia

Este documento y el archivo `config/*.yaml` de cada índice son la trazabilidad
completa del proyecto. Todo número que aparece en la página se puede seguir
desde acá hasta la celda del archivo original.

El panel **"Cómo funciona esta página"** de la app se genera desde esos mismos
archivos de configuración, no desde este documento. Si un coeficiente cambia,
cambia en los dos lados a la vez: la página no puede desincronizarse de su
propia metodología.

---

## Los dos archivos

Todo el proyecto se alimenta de dos descargas públicas y gratuitas.

### 1 · The Heritage Foundation

| | |
|---|---|
| Dataset | Index of Economic Freedom 2026, 32ª edición |
| Descarga | `https://static.heritage.org/index/data/2026/2026_indexofeconomicfreedom_data.xlsx` |
| Página | `https://economicfreedom.heritage.org/pages/all-country-scores` |
| Metodología | `https://static.heritage.org/index/pdf/2026/2026_indexofeconomicfreedom_methodology.pdf` |
| Hoja | `ef2026` · encabezado en la fila 1 |
| Contenido | 184 países, 15 columnas: país, región, puntaje total y 12 componentes |
| Fecha de corte | 30 de junio de 2025 |
| Registro | no requiere |

**No incluye insumos crudos.** Las ediciones anteriores a 2022 traían tasas
impositivas, gasto y aranceles; ésta no. Para recalcular componentes desde cero
hay que ir a las fuentes originales de Heritage (§ Fuentes de tercer nivel).

**Erratas del original que hay que copiar literalmente:**
`Judicial Efectiveness` y `Monitary Freedom`.

**Ocho países sin puntaje total:** Afganistán, Irak, Libia, Liechtenstein,
Somalía, Siria, Ucrania y Yemen. Heritage no publica en su metodología el
criterio por el cual se los excluye.

**Sobre la reponderación.** La metodología de Heritage declara que proveen los
datos crudos de cada componente para que otros los estudien, ponderen e integren
como consideren. Reponderar su índice es un uso previsto por sus autores.

### 2 · Fraser Institute

| | |
|---|---|
| Dataset | Economic Freedom of the World 2025 Annual Report |
| Descarga | `https://www.fraserinstitute.org/economic-freedom/dataset` |
| Hoja | `EFW Index 1970-2023` · encabezado en la fila 3 |
| Contenido | 165 países, series anuales 1970–2023, 87 columnas |
| Registro | no requiere |

Todos los componentes vienen en **escala 0 a 10, donde 10 significa menos
Estado**. Varias columnas llevan espacios dobles, y el componente de propiedad
estatal figura como `IE State ownership` —con i mayúscula en lugar de `1E`—,
errata del original.

---

## Cargar los datos

```bash
# 1 · ver qué columnas tiene el archivo (detecta solo dónde está el encabezado)
python src/cargar.py inspeccionar ~/Descargas/ARCHIVO.xlsx

# 2 · convertir al formato del proyecto
python src/cargar.py convertir ~/Descargas/ARCHIVO.xlsx --saltar N \
    --pais "COLUMNA" --varios "Columna=serie" "Otra=serie2"

# 3 · construir el índice
python src/build.py --config config/heritage.yaml
```

Todo dato entra al proyecto como un CSV de cuatro columnas en
`data/raw/manual/`: `iso3, serie, anio, valor`. No hay ninguna otra vía de
entrada, y el conversor informa qué nombres de país no pudo resolver en lugar de
descartarlos en silencio.

### Comando para Heritage

```bash
python src/cargar.py convertir ~/Descargas/2026_indexofeconomicfreedom_data.xlsx \
  --hoja ef2026 --saltar 1 --pais "Country" --anio 2026 --varios \
  "Property Rights=hf_property_rights" \
  "Judicial Efectiveness=hf_judicial_effectiveness" \
  "Government Integrity=hf_government_integrity" \
  "Tax Burden=hf_tax_burden" \
  "Government Spending=hf_government_spending" \
  "Fiscal Health=hf_fiscal_health" \
  "Business Freedom=hf_business_freedom" \
  "Labor Freedom=hf_labor_freedom" \
  "Monitary Freedom=hf_monetary_freedom" \
  "Trade Freedom=hf_trade_freedom" \
  "Investment Freedom=hf_investment_freedom" \
  "Financial Freedom=hf_financial_freedom" \
  "Overall Score=hf_overall"

python src/build.py --config config/heritage.yaml
```

Resultado esperado: 184 países, validación con diferencia máxima de 0,067.

### Comando para el índice Z

```bash
python src/cargar.py convertir ~/Descargas/efotw-2025-master-index-data-for-researchers-iso.xlsx \
  --saltar 3 --pais "Countries" --col-anio "Year" --varios \
  "1A Government consumption=z_consumo_publico" \
  "1B  Transfers and subsidies=z_transferencias" \
  "1D  Top marginal tax rate=z_alicuotas" \
  "IE State ownership=z_propiedad_estatal" \
  "1C  Government investment=z_inversion_publica" \
  "4Dii  Capital controls=z_controles_capital" \
  "5D Freedom to enter markets and compete=z_entrada_mercados" \
  "5A  Credit market regulation=z_regulacion_credito" \
  "Area 2 Legal System & Property Rights -- With Gender Adjustment=z_area2"

python src/build.py --config config/z.yaml
```

Los espacios dobles y el `IE` con i mayúscula son literales: copiar el bloque,
no tipearlo.

---

## Reproducibilidad de los componentes de Heritage

Clasificación tomada de su metodología publicada. La app la muestra al visitante
junto a cada componente.

| Componente | Estado | Detalle |
|---|---|---|
| Carga tributaria | **total** | `100 − 0,03·x²` sobre tres subfactores |
| Gasto público | **total** | `100 − 0,03·G²`, G = gasto/PBI promedio 3 años |
| Salud fiscal | **total** | `0,8·(100 − 2·D²) + 0,2·(100 − 0,01·B²)` |
| Libertad monetaria | **parcial** | `100 − 6,333·√inflación − penalización` · pesos 0,665 / 0,245 / 0,090 · el descuento por controles de precios, de hasta 20 puntos, no se publica por país |
| Libertad comercial | **parcial** | `100·(50 − arancel)/50 − penalización` · el descuento por barreras no arancelarias no se publica por país |
| Derechos de propiedad | fuentes | Credendo · US Chamber IP Index · World Bank WGI |
| Efectividad judicial | fuentes | Freedom House · World Bank WGI |
| Integridad del gobierno | fuentes | Transparency International · TRACE · WGI |
| Libertad de empresa | fuentes | WGI · WDI · Credendo · Women, Business and the Law |
| Libertad laboral | fuentes | WGI · WDI · Freedom House · OIT · Employing Workers |
| Libertad de inversión | **ninguna** | arranca en 100, descuentos cualitativos de 5 a 25 puntos |
| Libertad financiera | **ninguna** | escalones de 10 asignados por criterio |

Dos de doce componentes —16,7% del índice— no tienen insumo auditable.

**Verificación realizada.** Con los insumos publicados de Singapur del año
anterior: gasto 19,1% → `100 − 0,03·19,1²` = 89,06 contra 89,0 publicado;
alícuotas 22% y 17% y recaudación 12,8% → promedio 90,63 contra 90,6 publicado.

---

## Fuentes de tercer nivel

Las que Heritage usa para construir sus componentes. Todas de acceso libre; la
única de cobertura acotada es el IP Index, con unas cincuenta economías.

Credendo Country Risk · US Chamber of Commerce International IP Index ·
World Bank Worldwide Governance Indicators · World Bank World Development
Indicators · World Bank Women, Business and the Law · World Bank Employing
Workers · Freedom House Freedom in the World · Transparency International CPI ·
TRACE Bribery Risk Matrix · KPMG · Deloitte Tax Guides · PwC Worldwide Tax
Summaries · FMI World Economic Outlook · FMI International Financial Statistics ·
FMI Government Finance Statistics · FMI Artículo IV · OCDE · Eurostat · Banco
Africano de Desarrollo · Banco Asiático de Desarrollo · CEPAL · OIT · OMC World
Tariff Profiles · USTR National Trade Estimate · US Department of State
Investment Climate Statements.

El componente de propiedad estatal de Fraser se deriva de la variable
`v2clstown` del proyecto V-Dem.

---

## Ampliaciones posibles

**Serie histórica.** La página de descargas de Heritage permite seleccionar
varios años; Fraser cubre 1970–2023 en el mismo archivo. El pipeline ya conserva
todos los años, así que basta con cargar más datos.

**Penalizaciones despejadas.** Con inflación del FMI World Economic Outlook y
arancel promedio de OMC World Tariff Profiles se puede calcular la base de
libertad monetaria y comercial y restarla del puntaje publicado. La diferencia
es la penalización discrecional aplicada a cada país, que Heritage no publica.

**Dimensiones ausentes del índice Z.** Ninguna de las dos fuentes publica
señoreaje, aportes obligatorios a la seguridad social, suelo en manos del Estado
ni la fracción del gasto financiada con ingresos no tributarios. Incorporarlas
exigiría recolectar datos propios, lo que saldría de la regla de construcción
actual. Están declaradas como ausencias en `config/z.yaml`.

---

## Cuando un país no matchea

`src/countries.py` traduce nombres a códigos ISO3. Lo que no resuelve devuelve
`None` y se reporta; nunca se adivina. Para agregar un nombre, se suma al
diccionario `EN` o `ES` de ese archivo.

Los agregados regionales —"European Union", "Sub-Saharan Africa"— se descartan
automáticamente y el conversor lo informa.
