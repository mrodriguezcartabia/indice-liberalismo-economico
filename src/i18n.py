"""Textos de interfaz. Un solo lugar para los dos idiomas.

Los textos que describen los índices, pilares y componentes NO están acá: viven
en los archivos de configuración y llegan a la app vía `fuentes.json`. Acá solo
está el andamiaje de la interfaz.
"""

from __future__ import annotations

T = {
    # --- navegación ---
    "como_funciona": {"es": "Cómo funciona esta página", "en": "How this page works"},
    "indice": {"es": "Índice", "en": "Index"},

    # --- controles ---
    "pesos": {"es": "Pesos", "en": "Weights"},
    "cobertura_min": {"es": "Porcentaje mínimo de datos", "en": "Minimum data percentage"},
    "cobertura_ayuda": {
        "es": "Un dato faltante nunca se completa con cero. Por debajo de este "
              "valor, el país se lista aparte en vez de puntuarse.",
        "en": "A missing value is never filled with zero. Below this threshold a "
              "country is listed separately instead of scored."},
    "seguir": {"es": "Seguir países", "en": "Track countries"},
    "seguir_ayuda": {"es": "Aparecen siempre, aunque queden fuera de los puestos que se "
                           "muestran.",
                     "en": "Always shown, even outside the visible top."},
    "anio": {"es": "Año", "en": "Year"},
    "codigo_config": {"es": "Código de configuración", "en": "Configuration code"},
    "aplicar_codigo": {"es": "Aplicar", "en": "Apply"},
    "codigo_invalido": {"es": "Código no reconocido", "en": "Code not recognized"},

    # --- vistas ---
    "mostrar": {"es": "Cantidad que se muestra", "en": "Number shown"},
    "fuera_top": {"es": "Fuera de los puestos que se muestran", "en": "Outside the visible top"},
    "sin_cobertura": {"es": "Sin datos suficientes para entrar en el ranking",
                      "en": "Insufficient coverage to rank"},
    "puesto": {"es": "puesto", "en": "rank"},

    "sube": {"es": "sube", "en": "up"},
    "baja": {"es": "baja", "en": "down"},

    "observados": {"es": "Países con dato", "en": "Countries with data"},

    # --- métricas ---
    "m_corte": {"es": "Fecha de corte", "en": "Data cutoff"},

    # --- escrutinio ---
    "esc_validacion": {"es": "Validación de la réplica", "en": "Replica validation"},
    "esc_descargar": {"es": "Descargar los datos de esta pantalla",
                      "en": "Download the dataset behind this screen"},
    "esc_columna": {"es": "Columna en el archivo original", "en": "Column in the source file"},
    "esc_insumos": {"es": "Insumos", "en": "Inputs"},
    "esc_formula": {"es": "Fórmula", "en": "Formula"},
    "esc_no_calificados": {"es": "Países sin calificar", "en": "Ungraded countries"},

    "repro_total": {
        "es": "Reproducible: fórmula e insumos publicados.",
        "en": "Reproducible: formula and inputs published."},
    "repro_parcial": {
        "es": "Parcialmente reproducible: la fórmula está publicada, pero incluye "
              "un descuento discrecional que no se publica por país.",
        "en": "Partially reproducible: the formula is published, but includes a "
              "discretionary deduction not published by country."},
    "repro_fuentes": {
        "es": "Reconstruible desde fuentes de terceros, con trabajo.",
        "en": "Reconstructible from third-party sources, with effort."},
    "repro_ninguna": {
        "es": "No reproducible: asignado por criterio del analista, sin insumo "
              "auditable.",
        "en": "Not reproducible: assigned by analyst judgment, with no auditable "
              "input."},

    "titulo_propio": {"es": "Índice propio", "en": "Your own index"},
    "aviso_sin_dato": {
        "es": "El pilar {p} tiene peso pero no tiene datos en {a}. Su peso se "
              "reparte entre los demás. Elegí otro año para usarlo.",
        "en": "Pillar {p} has weight but no data for {a}. Its weight is "
              "redistributed. Pick another year to use it."},
    "esc_rezago": {
        "es": "{comp}: la fuente llega hasta {a1}. Para cada país se usa su "
              "último dato, siempre que no tenga más de diez años (desde "
              "{desde}), asignado a {a2}: {n} países. No es imputación: es un "
              "dato real con su año declarado.",
        "en": "{comp}: the source ends in {a1}. Each country's latest value is "
              "used, as long as it is no more than ten years old (from "
              "{desde}), assigned to {a2}: {n} countries. This is not "
              "imputation: it is a real value with its year declared."},
    "esc_rezago_viejos": {
        "es": "Quedan sin dato, por tener solo datos más viejos: {lista}.",
        "en": "Left without data, since they only have older values: {lista}."},
    "arbol_intro": {
        "es": "Heritage promedia sus doce componentes con peso igual: 8,33 % "
              "cada uno. Pero cada componente contiene una cantidad distinta de "
              "indicadores. Todos los bloques miden lo mismo; lo que cambia es "
              "en cuántos pedazos está cortado cada uno.",
        "en": "Heritage averages its twelve components with equal weight: 8.33% "
              "each. But each component contains a different number of "
              "indicators. Every block is the same width; what changes is how "
              "many pieces it is cut into."},
    "arbol_conclusion": {
        "es": "El indicador que más pesa vale {v} veces lo que vale el que menos "
              "pesa, dentro de un índice que se presenta como de peso igual. "
              "Salud fiscal, además, reparte 80/20 internamente entre déficit y "
              "deuda: una ponderación desigual declarada en su propia "
              "metodología.",
        "en": "The heaviest indicator is worth {v} times the lightest, inside an "
              "index presented as equally weighted. Fiscal Health also splits "
              "80/20 internally between deficit and debt: an unequal weighting "
              "declared in their own methodology."},
    "arbol_nota": {
        "es": "Los subfactores no son manipulables: Heritage publica su "
              "existencia y su cantidad, pero no sus valores por país. "
              "Los marcados con * están declarados en la metodología y conviene "
              "verificarlos antes de citarlos.",
        "en": "Sub-factors are not adjustable: Heritage publishes their existence "
              "and number, but not their country-level values. Those marked with "
              "* are declared in the methodology and should be verified before "
              "being cited."},
    "tut_boton": {"es": "Armá tu propio índice", "en": "Build your own index"},
    "tut_titulo": {"es": "Tutorial", "en": "Tutorial"},
    "tut_aplicar": {"es": "Ver mi ranking", "en": "See my ranking"},
    "tut_cancelar": {"es": "Cancelar", "en": "Cancel"},
    "intro_barra": {
        "es": "Cada componente vale|los puntos que le des: su peso es sus puntos "
              "sobre el total. Subir uno baja el peso relativo de los demás. Los "
              "pilares no se ponderan aparte: su peso es la suma de los puntos "
              "de sus componentes —que es exactamente cómo funciona el índice de "
              "Heritage.",
        "en": "Each component is worth|the points you give it. Its weight is its "
              "points over the total, so raising one lowers everyone else's "
              "relative weight. Pillars are not weighted separately: their "
              "weight is the sum of their components' points — which is exactly "
              "how the Heritage index works."},
    "puntos": {"es": "puntos", "en": "points"},
    "indicadores": {"es": "indicadores", "en": "indicators"},
    "indicador": {"es": "indicador", "en": "indicator"},
    "peso_resultante": {"es": "Peso resultante por pilar",
                        "en": "Resulting weight per pillar"},
    "peso_resultante_ayuda": {
        "es": "Nadie eligió estos porcentajes: salen de cuántos componentes "
              "tiene cada pilar y cuántos puntos les diste. Con los puntos de "
              "Heritage, las cuatro categorías dan 25 % porque cada una agrupa "
              "tres componentes.",
        "en": "Nobody chose these percentages: they follow from how many "
              "components each pillar has and how many points you gave them. "
              "With Heritage's points, all four categories give 25% because "
              "each groups three components."},
    "elegir_indice": {"es": "Ponderación", "en": "Weighting"},
    "col_puesto": {"es": "Puesto", "en": "Rank"},
    "col_pais": {"es": "País", "en": "Country"},
    "col_puntaje": {"es": "Puntaje", "en": "Score"},
    "imprimir": {"es": "Descargar PDF", "en": "Download PDF"},
    "pdf_procedencia": {"es": "Procedencia", "en": "Provenance"},
    "pdf_ponderacion": {"es": "Ponderación aplicada", "en": "Weighting applied"},
    "repo": {"es": "Código y datos", "en": "Code and data"},
    "ayuda_p1": {"es": "Qué estás mirando", "en": "What you are looking at"},
    "ayuda_p2": {"es": "De dónde salen los números", "en": "Where the numbers come from"},
    "ayuda_p3": {"es": "El cálculo, paso a paso", "en": "The calculation, step by step"},
    "ayuda_p4": {"es": "Qué se puede verificar", "en": "What can be verified"},
    "ayuda_p5": {"es": "Qué falta", "en": "What is missing"},
    "ayuda_1": {
        "es": "Un índice de libertad económica no mide algo que exista en la "
              "naturaleza, como la temperatura. Es un promedio de varias cosas "
              "distintas y alguien tuvo que decidir cuánto pesa cada una. Esta "
              "página parte del índice de The Heritage Foundation, el más citado "
              "en la prensa, y te deja cambiar esas decisiones para ver qué "
              "pasa. Los datos no se tocan nunca: lo único que cambia es el peso.",
        "en": "An economic freedom index does not measure something that exists "
              "in nature, like temperature. It is an average of several "
              "different things, and someone had to decide how much each one "
              "weighs. This page starts from The Heritage Foundation's index, "
              "the most cited in the press, and lets you change those decisions "
              "to see what happens. The data is never touched: only the weight "
              "changes."},
    "ayuda_2": {
        "es": "Todos los puntajes vienen del archivo que Heritage publica en su "
              "sitio, sin ninguna modificación. Su metodología declara que "
              "proveen los datos de cada componente para que otros los estudien "
              "y ponderen como consideren, así que reponderar su índice es un "
              "uso previsto por sus autores. Los demás componentes vienen del "
              "Fraser Institute, la OCDE y el FMI, y cada uno cita su fuente en "
              "«Qué mide cada componente».",
        "en": "All scores come from the file Heritage publishes on its site, "
              "unmodified. Their methodology states that they provide each "
              "component's data so others may study and weight it as they see "
              "fit, so reweighting their index is a use foreseen by its authors. "
              "The only datum not from Heritage is state ownership, which starts "
              "at zero points and only enters if you give it some."},
    "ayuda_4": {
        "es": "No todo el índice es igual de auditable. Tres componentes tienen "
              "fórmula e insumos publicados y se pueden recalcular al decimal. "
              "Dos tienen fórmula publicada pero incluyen un descuento "
              "discrecional que no se publica por país. Cinco se reconstruyen "
              "desde fuentes de terceros, con trabajo. Y dos —libertad de "
              "inversión y financiera— se asignan por criterio del analista, sin "
              "ningún dato de entrada verificable: son el 16,7 % del puntaje "
              "total. Cada componente indica en qué categoría cae.",
        "en": "Not all of the index is equally auditable. Three components have "
              "published formula and inputs and can be recalculated exactly. Two "
              "have a published formula but include a discretionary deduction "
              "not published by country. Five can be reconstructed from "
              "third-party sources, with effort. And two — investment and "
              "financial freedom — are assigned by analyst judgment, with no "
              "verifiable input: they are 16.7% of the total score. Each "
              "component states which category it falls into."},
    "cada_uno": {"es": "c/u", "en": "each"},
    "tut_paso": {"es": "Componente {i} de {n}", "en": "Component {i} of {n}"},
    "tut_siguiente": {"es": "Siguiente", "en": "Next"},
    "tut_anterior": {"es": "Anterior", "en": "Back"},
    "tut_resumen": {"es": "Tu ponderación", "en": "Your weighting"},
    "tut_resumen_txt": {
        "es": "Así queda el peso de cada pilar según lo que respondiste. Fijate "
              "que vos ponderaste componentes, pero el peso de cada pilar salió "
              "solo: depende de cuántos componentes tiene. Eso es exactamente lo "
              "que pasa con el índice de Heritage.",
        "en": "Here is each pillar's weight based on your answers. Note that you "
              "weighted components, but each pillar's weight came out on its "
              "own: it depends on how many components it has. That is exactly "
              "what happens with the Heritage index."},
    "tut_pregunta": {
        "es": "¿Cuánto importa esto para medir la libertad económica de un país?",
        "en": "How much does this matter for measuring a country's economic "
              "freedom?"},
    "tut_nada": {"es": "Nada", "en": "Not at all"},
    "tut_mucho": {"es": "Muchísimo", "en": "Enormously"},
    "vintage_viejo": {
        "es": "Los datos construidos son de una versión anterior y no traen el "
              "detalle de subfactores. Corré de nuevo: "
              "python src/build.py --config config/heritage.yaml",
        "en": "The built data is from an older version and lacks sub-factor "
              "detail. Re-run: python src/build.py --config config/heritage.yaml"},
    "col_aporte": {"es": "Aporte por componente", "en": "Contribution by component"},
    "barra_ayuda": {
        "es": "Cada tramo mide el puntaje del país en ese componente por el peso "
              "que le diste, así que la barra entera es el índice. Pasá el mouse "
              "por el nombre de un componente en el panel izquierdo para ver el "
              "ranking como si ese componente pesara 100 y el resto cero.",
        "en": "Each segment is the country's score in that component times the "
              "weight you gave it, so the whole bar is the index. Hover a "
              "component name in the left panel to see the ranking as if that "
              "component weighed 100 and the rest zero."},
    "aviso_superposicion": {
        "es": "«{a}» {y} «{b}» tienen una correlación de {r}: miden casi lo "
              "mismo. Con los dos activos, esa dimensión pesa el doble sin que "
              "el porcentaje lo diga: es el mismo problema de doble conteo que "
              "este proyecto le señala a los índices compuestos.",
        "en": "\u201c{a}\u201d and \u201c{b}\u201d have a correlation of {r}: "
              "they measure almost the same thing. With both active, that "
              "dimension weighs twice without the percentage saying so: the "
              "same double-counting problem this project points out in "
              "composite indices."},
    "aviso_superposicion_grupo": {
        "es": "{lista} tienen correlaciones entre {rmin} y {rmax}: miden casi "
              "lo mismo. Con los {n} activos, esa dimensión pesa {veces} sin "
              "que el porcentaje lo diga: es el mismo problema de doble conteo "
              "que este proyecto le señala a los índices compuestos.",
        "en": "{lista} have correlations between {rmin} and {rmax}: they "
              "measure almost the same thing. With all {n} active, that "
              "dimension weighs {veces} without the percentage saying so: the "
              "same double-counting problem this project points out in "
              "composite indices."},
    "numero_3": {"es": "tres", "en": "three"},
    "numero_4": {"es": "cuatro", "en": "four"},
    "veces_3": {"es": "el triple", "en": "three times as much"},
    "veces_4": {"es": "el cuádruple", "en": "four times as much"},
    "veces_n": {"es": "{n} veces más", "en": "{n} times as much"},
    "aviso_incompleto": {
        "es": "* Sin dato, o con un dato de más de diez años, en algún "
              "componente: {lista}. Su puntaje reparte ese peso entre los "
              "componentes que sí tiene y por eso su barra es más corta.",
        "en": "* No data, or data more than ten years old, for some "
              "component: {lista}. Its score spreads that weight across the "
              "components it does have, which is why its bar is shorter."},
    "titulo_pestana": {"es": "Índice de Liberalismo económico",
                       "en": "Economic Liberalism Index"},
    "todo_cero": {
        "es": "Todos los componentes están en cero, así que no hay índice que "
              "calcular: asigná puntos a al menos uno. Mientras tanto se "
              "muestra el {indice}.",
        "en": "All components are at zero, so there is no index to compute: "
              "give points to at least one. Meanwhile the {indice} is shown."},
    "calc_falta": {
        "es": "Sin dato de: {lista}. Su peso se reparte entre los componentes "
              "que el país sí tiene, igual que en el ranking.",
        "en": "No data for: {lista}. Its weight is spread across the "
              "components the country does have, as in the ranking."},
    "val_max": {"es": "diferencia máxima", "en": "maximum difference"},
    "val_paises": {"es": "países comparados", "en": "countries compared"},
    "puesto_heritage": {"es": "Heritage:", "en": "Heritage:"},
    "aviso_puesto_heritage": {
        "es": "** Puesto distinto del publicado por Heritage, o del que surge de "
              "su puntaje: {lista}. Heritage publica cada componente redondeado a "
              "un decimal, pero calcula el total con decimales que no publica. "
              "Con los datos publicados, el total puede diferir hasta 0,07 "
              "puntos y países casi empatados pueden quedar ordenados de otra "
              "manera, a pocos puestos de distancia.",
        "en": "** Rank different from the one Heritage publishes, or implied by its "
              "published score: {lista}. Heritage publishes each component rounded to "
              "one decimal, but computes the total with decimals it does not "
              "publish. With the published data, the total can differ by up to "
              "0.07 points, and nearly tied countries can end up ordered "
              "differently, a few places apart."},
    "pop_100": {"es": "Puntaje más alto = más cerca de: {x}.",
                "en": "Higher score = closer to: {x}."},
    "critica": {"es": "Razones para un nuevo índice",
                "en": "Reasons for a new index"},
    "crit_p0": {"es": "Por qué otro índice", "en": "Why another index"},
    "crit_porque": {
        "es": "Ningún índice compuesto es neutral: promediar varios números "
              "distintos obliga a decidir cuáles entran, cuánto pesa cada uno y "
              "qué se hace con lo que no se puede medir. Este índice también "
              "toma esas decisiones y por eso están todas a la vista: los pesos "
              "se editan en pantalla, el código de configuración permite "
              "reproducir cualquier ponderación y el cálculo de cada país se "
              "muestra paso a paso.\n\nSolo entra lo que mide el tamaño y la "
              "intervención del Estado. Cuánto recauda, cuánto gasta y consume, "
              "cuánto posee e invierte, y cuánto restringe el comercio, el "
              "crédito, los capitales y la entrada a los mercados. Quedan fuera "
              "los componentes de Heritage que miden otra cosa: la calidad de "
              "las instituciones (derechos de propiedad, efectividad judicial, "
              "integridad del gobierno), resultados macroeconómicos (salud "
              "fiscal, libertad monetaria) y evaluaciones cualitativas o "
              "consecuencias del desarrollo (libertades de inversión, "
              "financiera, de empresa y laboral) ya que estos componentes no son "
              "valores particulares del Liberalismo económico.\n\nAdemás, se mide "
              "lo que el Estado posee, no solo lo que gasta[4]. Heritage no "
              "tiene ningún componente que mida propiedad estatal de la "
              "economía, inversión pública, control del crédito ni controles de "
              "capital. Los cuatro entran acá, con datos del Fraser Institute.",
        "en": "No composite index is neutral: averaging several different "
              "numbers forces decisions about what enters, how much each weighs "
              "and what to do with what cannot be measured. This index makes "
              "those decisions too, which is why they are all visible: weights "
              "are edited on screen, the configuration code reproduces any "
              "weighting, and each country's calculation is shown step by step.\n\n"
              "Only what measures the size and intervention of the state enters. "
              "How much it collects, how much it spends and consumes, how much "
              "it owns and invests, and how much it restricts trade, credit, "
              "capital and market entry. Heritage components that measure "
              "something else are left out: the quality of institutions "
              "(property rights, judicial effectiveness, government integrity), "
              "macroeconomic outcomes (fiscal health, monetary freedom), and "
              "qualitative assessments or consequences of development "
              "(investment, financial, business and labor freedom), since these "
              "components are not values specific to economic liberalism.\n\nIn "
              "addition, what the state owns is measured, not only what it "
              "spends[4]. Heritage has no component measuring state ownership of "
              "the economy, government investment, credit control or capital "
              "controls. All four enter here, with data from the Fraser "
              "Institute."},
    "crit_p1": {"es": "Lo que declaran y lo que calculan",
                "en": "What they declare and what they compute"},
    "crit_p2": {"es": "Casos que no cierran", "en": "Cases that do not add up"},
    "crit_p3": {"es": "Lo que no se puede verificar",
                "en": "What cannot be verified"},
    "crit_p4": {"es": "El peso real de cada indicador",
                "en": "The actual weight of each indicator"},
    "crit_intro": {
        "es": "Ninguna de estas observaciones cuestiona los datos de Heritage: "
              "todas se verifican con su propio archivo y su propia "
              "metodología, enlazados abajo.",
        "en": "None of these observations question Heritage's data: all can be "
              "verified with their own file and their own methodology, linked "
              "below."},
    "crit_definicion": {
        "es": "Heritage define la libertad económica[3] como el derecho de cada "
              "persona a controlar su propio trabajo y su propiedad, y agrega "
              "que en una sociedad económicamente libre los gobiernos se "
              "abstienen de coaccionar más allá de lo necesario para proteger y "
              "mantener la libertad misma.\n\n**Pero la fórmula del componente de "
              "gasto público[1] toma el gasto cero como óptimo.** Si el criterio "
              "es no coaccionar más allá de lo necesario para proteger la "
              "libertad, entonces el gasto que sostiene tribunales y policía no "
              "es una pérdida de libertad. La fórmula lo trata como tal: <span "
              "class=\"formula\">100 − 0,03 × G²</span> solo llega a 100 cuando el "
              "gasto es cero. Hay una distancia medible entre la definición "
              "declarada y el cálculo.\n\nLa propia metodología[1] admite el "
              "problema: «La metodología del índice toma el gasto público cero "
              "como referencia. En consecuencia, los países subdesarrollados —en "
              "especial los que tienen poca capacidad estatal— pueden recibir "
              "puntajes artificialmente altos. Sin embargo, esos gobiernos "
              "pueden proveer pocos bienes públicos, o ninguno, y probablemente "
              "reciban puntajes bajos en algunos de los otros componentes de la "
              "libertad económica (como derechos de propiedad, libertad "
              "financiera y libertad de inversión) que miden aspectos de la "
              "efectividad del gobierno» (“The Index methodology treats zero "
              "government spending as the benchmark. As a result, underdeveloped "
              "countries—especially those with little government capacity—may "
              "receive artificially high scores. However, such governments can "
              "provide few if any public goods and will probably receive low "
              "scores on some of the other components of economic freedom (such "
              "as property rights, financial freedom, and investment freedom) "
              "that measure aspects of government effectiveness.”).\n\n**Segunda "
              "distancia: la definición habla de controlar la propia propiedad, "
              "pero ningún componente mide quién es dueño de qué.** El "
              "componente de derechos de propiedad mide seguridad y "
              "cumplimiento, no titularidad. Por eso Singapur puntúa 89,2 con el "
              "Estado dueño de más del 90 % del suelo, que vende en concesiones "
              "de 99 años.",
        "en": "Heritage defines economic freedom as every person's right to "
              "control their own labor and property, and adds that in an "
              "economically free society governments refrain from coercion "
              "beyond what is needed to protect and maintain liberty itself.\n\n"
              "**Yet the government spending formula[1] takes zero spending as "
              "the optimum.** If the criterion is not coercing beyond what is "
              "needed to protect liberty, then the spending that sustains courts "
              "and police is not a loss of freedom. The formula treats it as "
              "one: <span class=\"formula\">100 − 0.03 × G²</span> only reaches "
              "100 when spending is zero.\n\nTheir own methodology[1] concedes the "
              "issue: “The Index methodology treats zero government spending as "
              "the benchmark. As a result, underdeveloped countries—especially "
              "those with little government capacity—may receive artificially "
              "high scores. However, such governments can provide few if any "
              "public goods and will probably receive low scores on some of the "
              "other components of economic freedom (such as property rights, "
              "financial freedom, and investment freedom) that measure aspects "
              "of government effectiveness.”\n\n**A second gap: the definition "
              "speaks of controlling one's own property, but no component "
              "measures who owns what.** The property rights component measures "
              "security and enforcement, not ownership. Hence Singapore scores "
              "89.2 while the state owns over 90% of the land."},
    "crit_casos": {
        "es": "**Austria primera en libertad laboral, Paraguay 163.º**[2]. "
              "Austria tiene negociación colectiva sectorial que cubre a casi "
              "toda su fuerza de trabajo, y encabeza igual con 81,6. Paraguay "
              "saca 44,1. Dos razones se combinan: el componente incluye "
              "productividad y participación laboral, que son resultados "
              "económicos y no reglas; y la fórmula de los primeros siete "
              "subfactores compara cada valor contra el promedio mundial, así "
              "que un salario mínimo alto pesa poco si el valor agregado por "
              "trabajador también lo es. Un país rico con regulación fuerte "
              "puede superar a uno pobre con regulación débil.\n\n**Singapur "
              "primero en el índice, 67.º en efectividad judicial**[2]. Su peor "
              "componente es 58,3, apenas por encima de Argentina (58,2), y aun "
              "así queda primero en el total: el promedio aritmético permite que "
              "once componentes compensen a uno.\n\n**Estados Unidos comparte el "
              "primer puesto en libertad financiera con 80**[2]. El valor 90 no "
              "lo alcanza nadie; hay 16 países en 80. El componente mide el "
              "estado actual del sector, no la disposición del Estado a "
              "intervenir: un país que rescató a su banca y volvió a soltarla "
              "puntúa igual que uno que nunca intervino.\n\n**Peso igual entre "
              "componentes no es peso igual entre indicadores**[1]. Heritage "
              "promedia sus doce componentes con peso igual, 8,33 % cada uno. "
              "Pero gasto público se calcula con un indicador y libertad laboral "
              "con nueve: cada indicador laboral pesa 0,93 % y el de gasto "
              "público 8,33 %. Nueve veces más. Y salud fiscal reparte 80/20 "
              "internamente entre déficit y deuda, una ponderación desigual "
              "declarada dentro de un índice que se presenta como de peso igual.\n"
              "\n**Libertad de empresa mide desarrollo, no reglas**[1]. Sus "
              "cuatro subfactores pesan igual: acceso a electricidad, riesgo del "
              "entorno de negocios, calidad regulatoria e inclusión económica de "
              "la mujer. Solo el tercero mide una regla. El acceso a "
              "electricidad es infraestructura: un país sin red eléctrica no es "
              "menos libre, es más pobre. El riesgo del entorno es una "
              "evaluación de agencias de seguro de crédito, o sea el juicio de "
              "quien vende cobertura sobre qué tan riesgoso es cobrar ahí. La "
              "inclusión económica de la mujer mide un resultado social. Tres de "
              "los cuatro son consecuencias del desarrollo, no causas de "
              "libertad.\n\nEso produce circularidad: el índice incorpora "
              "indicadores de desarrollo y después se lo usa para mostrar que la "
              "libertad económica produce desarrollo. Y castiga a los países "
              "pobres dos veces, porque ser pobre baja el puntaje de un "
              "componente que dice medir libertad.",
        "en": "**Austria first in labor freedom, Paraguay 163rd.** Austria has "
              "sectoral collective bargaining covering nearly its whole "
              "workforce and still leads with 81.6. Two reasons combine: the "
              "component includes productivity and participation, which are "
              "outcomes rather than rules; and the formula compares each value "
              "against the world average.\n\n"
              "**Singapore first overall, 67th in judicial effectiveness.** Its "
              "worst component is 58.3, barely above Argentina's 58.2, and it still "
              "ranks first: the arithmetic mean lets eleven components offset "
              "one.\n\n"
              "**The United States shares first place in financial freedom with "
              "80.** No country reaches 90. The component measures the sector's "
              "current state, not the state's willingness to intervene.\n\n"
              "**Development indicators inside freedom components.** Business "
              "freedom includes access to electricity among its four "
              "sub-factors."},
    "crit_opacidad": {
        "es": "**Heritage publica los promedios, no los sumandos**[2]. El "
              "archivo trae doce columnas, una por componente. Libertad laboral "
              "llega como un solo número —77,0 para Singapur— y los nueve "
              "subfactores que lo componen ya vinieron promediados adentro. La "
              "metodología dice cuáles son y cómo se combinan, pero **los "
              "valores por país no existen en ningún archivo público**. Se puede "
              "verificar que Singapur saca 77,0; no se puede verificar cómo se "
              "llegó a ese 77,0.\n\nEso se repite en nueve de los doce "
              "componentes. Solo gasto público, carga tributaria y salud fiscal "
              "son auditables de punta a punta: tienen fórmula e insumos "
              "publicados y se recalculan al decimal.\n\n**Y dos componentes no "
              "tienen ningún insumo**[1]. Libertad de inversión arranca en 100 y "
              "descuenta 5, 10, 15, 20 o 25 puntos según evaluación cualitativa. "
              "Libertad financiera se asigna en escalones de diez a criterio del "
              "analista. Son 16,7 % del puntaje total sin nada que auditar.\n\n"
              "**Dos componentes más esconden un descuento.** Libertad monetaria "
              "y comercial publican su fórmula, pero después restan una "
              "penalización discrecional —por controles de precios y por "
              "barreras no arancelarias— que no se publica por país.",
        "en": "**Heritage publishes averages, not the terms being averaged.** "
              "Labor freedom arrives as a single number and its nine "
              "sub-factors come pre-averaged. The methodology says what they "
              "are, but **their country-level values exist in no public file**. "
              "You can verify that Singapore scores 77.0; you cannot verify how "
              "that 77.0 was reached.\n\n"
              "Only government spending, tax burden and fiscal health are "
              "auditable end to end.\n\n"
              "**And two components have no input at all.** Investment freedom "
              "starts at 100 with qualitative deductions; financial freedom is "
              "assigned in steps of ten. Together they are 16.7% of the score "
              "with nothing to audit."},
    "ver_fuentes": {"es": "Fuentes", "en": "Sources"},
    "fuente_metodologia": {"es": "Metodología oficial 2026",
                           "en": "Official 2026 methodology"},
    "fuente_datos": {"es": "Archivo de datos", "en": "Data file"},
    "fuente_definicion": {"es": "Definición de libertad económica",
                          "en": "Definition of economic freedom"},
    "fuente_fraser": {"es": "Fraser Institute, Economic Freedom of the World",
                      "en": "Fraser Institute, Economic Freedom of the World"},
    "fuente_repo": {"es": "Código y datos de esta página",
                    "en": "Code and data of this page"},
    "ayuda_p0": {"es": "Qué mide cada componente",
                 "en": "What each component measures"},
    "ayuda_p0_txt": {
        "es": "Todos los componentes van de 0 a 100 y más alto siempre significa "
              "más libre según la definición de Heritage. El puntaje total es el "
              "promedio ponderado por los puntos que asignes. Cada fila enlaza a "
              "la fuente de la que sale el dato[1][4].",
        "en": "All components run from 0 to 100 and higher always means freer "
              "under Heritage's definition. The total score is the average "
              "weighted by the points you assign."},
    "col_mide": {"es": "Qué mide", "en": "What it measures"},
    "col_cien": {"es": "100 significa", "en": "100 means"},
    "col_comp": {"es": "Componente", "en": "Component"},
    "calc_elegir": {"es": "Elegí un país", "en": "Pick a country"},
    "calc_intro": {
        "es": "Cada línea muestra el puntaje publicado por la fuente, el peso "
              "que le diste y el aporte al total. La suma de la última columna "
              "es el puntaje del país. Con la ponderación original de Heritage "
              "el resultado tiene que coincidir con el puntaje que ellos "
              "publican[2] y la diferencia se muestra al final.",
        "en": "Each line shows the score published by the source, the weight you "
              "gave it, and its contribution to the total. The last column sums "
              "to the country's score. Under Heritage's original weighting the "
              "result must match their published score, and the difference is "
              "shown at the end."},
    "calc_publicado": {"es": "Publicado por Heritage", "en": "Published by Heritage"},
    "calc_recalculado": {"es": "Recalculado acá", "en": "Recomputed here"},
    "calc_diferencia": {"es": "Diferencia", "en": "Difference"},
    "calc_aporte": {"es": "Aporte", "en": "Contribution"},
    "calc_peso": {"es": "Peso", "en": "Weight"},
    "calc_puntaje": {"es": "Puntaje", "en": "Score"},
    "intro_pagina": {
        "es": "Esta página busca contribuir a diferenciar dos términos: "
              "«libertad económica» y «Liberalismo económico». El primero es "
              "disputado por ideologías políticas diversas; el segundo designa "
              "una ideología concreta, la que defiende un Estado mínimo.|Para "
              "esto, primero reconstruimos el Index of Economic Freedom de The "
              "Heritage Foundation con sus propios datos y mostramos dónde su "
              "cálculo se aparta de su propia definición: qué mide, qué no mide "
              "y qué pasa con el ranking cuando se cambian los pesos. Esto nos "
              "permite armar un nuevo índice que presentamos como «Índice de "
              "Liberalismo económico» que puede ser escrutado en detalle.",
        "en": "This page seeks to help distinguish two terms: “economic freedom” "
              "and “economic liberalism”. The first is contested by diverse "
              "political ideologies; the second names a specific ideology, the "
              "one that advocates a minimal state.|To that end, we first "
              "reconstruct The Heritage Foundation's Index of Economic Freedom "
              "from its own data and show where its computation departs from its "
              "own definition: what it measures, what it does not, and what "
              "happens to the ranking when the weights change. This allows us to "
              "build a new index, presented as the “Economic Liberalism Index”, "
              "which can be scrutinized in detail.",
    },
    "ver_razones": {
        "es": "El detalle de estas decisiones está en «{b}», arriba a la derecha.",
        "en": "The detail of these decisions is in “{b}”, top right."},
    "mas": {"es": "…más", "en": "…more"},
    "menos": {"es": "…menos", "en": "…less"},
    "sin_datos": {
        "es": "Falta cargar los datos de este índice. Ver docs/FUENTES.md.",
        "en": "This index has no data loaded yet. See docs/FUENTES.md."},
}

def t(clave: str, idioma: str = "es") -> str:
    v = T.get(clave)
    if not v:
        return clave
    return v.get(idioma) or v.get("es") or clave

def txt(valor, idioma: str = "es") -> str:
    """Extrae la variante de idioma de un campo bilingüe {es, en} del config."""
    if isinstance(valor, dict):
        return str(valor.get(idioma) or valor.get("es") or
                   next(iter(valor.values()), ""))
    return "" if valor is None else str(valor)
