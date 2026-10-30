"""Textos de interfaz. Un solo lugar para los dos idiomas.

Los textos que describen los índices, pilares y componentes NO están acá: viven
en los archivos de configuración y llegan a la app vía `fuentes.json`. Acá sólo
está el andamiaje de la interfaz.
"""

from __future__ import annotations

T = {
    # --- portada ---
    "tagline": {
        "es": "Comparar índices de libertad económica bajo distintas ponderaciones",
        "en": "Comparing economic freedom indices under different weightings"},
    "portada_intro": {
        "es": "Un índice compuesto es un promedio de decisiones. Esta página permite "
              "cambiarlas y ver qué pasa, con datos publicados por terceros.",
        "en": "A composite index is an average of decisions. This page lets you change "
              "them and see what happens, using data published by third parties."},
    "elegir": {"es": "Abrir", "en": "Open"},
    "propio_titulo": {"es": "Armá el tuyo", "en": "Build your own"},
    "propio_desc": {
        "es": "Respondé unas comparaciones concretas y la página deriva tus pesos. "
              "No hay respuestas correctas: el objetivo es que veas qué implica tu "
              "propia definición.",
        "en": "Answer a few concrete comparisons and the page derives your weights. "
              "There are no right answers: the point is to see what your own "
              "definition implies."},

    # --- navegación ---
    "volver": {"es": "Inicio", "en": "Home"},
    "como_funciona": {"es": "Cómo funciona esta página", "en": "How this page works"},
    "indice": {"es": "Índice", "en": "Index"},
    "idioma": {"es": "Idioma", "en": "Language"},

    # --- controles ---
    "pesos": {"es": "Pesos", "en": "Weights"},
    "pesos_ayuda": {
        "es": "Se renormalizan a 100%. Movelos y el ranking se recalcula.",
        "en": "Renormalized to 100%. Move them and the ranking recalculates."},
    "componentes_de": {"es": "Componentes de", "en": "Components of"},
    "agregacion": {"es": "Agregación", "en": "Aggregation"},
    "aritmetica": {"es": "aritmética", "en": "arithmetic"},
    "geometrica": {"es": "geométrica", "en": "geometric"},
    "agregacion_ayuda": {
        "es": "La aritmética permite que un pilar alto compense a uno bajo. "
              "La geométrica no.",
        "en": "Arithmetic lets a high pillar offset a low one. Geometric does not."},
    "cobertura_min": {"es": "Cobertura mínima de datos", "en": "Minimum data coverage"},
    "cobertura_ayuda": {
        "es": "Un dato faltante nunca se completa con cero. Por debajo de este "
              "valor, el país se lista aparte en vez de puntuarse.",
        "en": "A missing value is never filled with zero. Below this threshold a "
              "country is listed separately instead of scored."},
    "seguir": {"es": "Seguir países", "en": "Track countries"},
    "seguir_ayuda": {"es": "Aparecen siempre, aunque queden fuera del top.",
                     "en": "Always shown, even outside the visible top."},
    "anio": {"es": "Año", "en": "Year"},
    "codigo_config": {"es": "Código de configuración", "en": "Configuration code"},
    "codigo_ayuda": {
        "es": "Cada ponderación tiene un código único. Guardalo para volver "
              "exactamente a esta configuración, o citalo en una nota: "
              "cualquiera que lo ingrese acá reproduce el mismo ranking. No se "
              "guarda nada en ningún servidor; el código es la ponderación, "
              "escrita en forma corta.",
        "en": "Every weighting has a unique code. Save it to return to this exact "
              "configuration, or cite it: anyone who enters it here reproduces "
              "the same ranking. Nothing is stored on any server; the code is the "
              "weighting, written in short form."},
    "aplicar_codigo": {"es": "Aplicar", "en": "Apply"},
    "codigo_invalido": {"es": "Código no reconocido", "en": "Code not recognized"},
    "restablecer": {"es": "Volver a los pesos originales", "en": "Reset to original weights"},

    # --- vistas ---
    "v_ranking": {"es": "Ranking", "en": "Ranking"},
    "v_comparacion": {"es": "Comparación", "en": "Comparison"},
    "v_dispersion": {"es": "Dispersión", "en": "Scatter"},
    "v_cobertura": {"es": "Cobertura", "en": "Coverage"},
    "v_fuentes": {"es": "Fuentes", "en": "Sources"},

    "mostrar": {"es": "Mostrar", "en": "Show"},
    "fuera_top": {"es": "Fuera del top visible", "en": "Outside the visible top"},
    "sin_cobertura": {"es": "Sin cobertura suficiente para rankear",
                      "en": "Insufficient coverage to rank"},
    "puesto": {"es": "puesto", "en": "rank"},

    "delta_titulo": {"es": "Quién se mueve más", "en": "Who moves the most"},
    "delta_ayuda": {
        "es": "Diferencia de puesto entre la ponderación original del índice y la "
              "que tenés puesta ahora. El movimiento es el dato, no las tablas.",
        "en": "Rank difference between the index's original weighting and the one "
              "you have set. The movement is the finding, not the tables."},
    "sube": {"es": "sube", "en": "up"},
    "baja": {"es": "baja", "en": "down"},

    "disp_ayuda": {
        "es": "El eje vertical no entra al puntaje. Incorporarlo mezclaría "
              "presencia del Estado con calidad institucional, que es justamente "
              "la distinción que esta página busca mantener.",
        "en": "The vertical axis does not enter the score. Including it would mix "
              "state presence with institutional quality, the very distinction "
              "this page seeks to preserve."},
    "eje_x": {"es": "Puntaje del índice", "en": "Index score"},

    "cob_ayuda": {
        "es": "La cobertura se publica junto al puntaje. Sin esto, un índice que "
              "imputa ceros premia a los países con peor estadística.",
        "en": "Coverage is published alongside the score. Without it, an index that "
              "imputes zeros rewards countries with worse statistics."},
    "observados": {"es": "Países con dato", "en": "Countries with data"},

    # --- métricas ---
    "m_paises": {"es": "Países", "en": "Countries"},
    "m_rankeados": {"es": "Rankeados", "en": "Ranked"},
    "m_componentes": {"es": "Componentes", "en": "Components"},
    "m_corte": {"es": "Fecha de corte", "en": "Data cutoff"},

    # --- escrutinio ---
    "esc_intro": {
        "es": "Todo el contenido de este panel se genera desde el archivo de "
              "configuración del índice, no está escrito aparte. Si cambia un "
              "coeficiente, cambia acá.",
        "en": "Everything in this panel is generated from the index configuration "
              "file, not written separately. If a coefficient changes, it changes "
              "here."},
    "esc_aritmetica": {"es": "La aritmética, paso a paso", "en": "The arithmetic, step by step"},
    "esc_elegir_pais": {"es": "Ver el cálculo para", "en": "Show the calculation for"},
    "esc_fuente": {"es": "Fuente de los datos", "en": "Data source"},
    "esc_pesos": {"es": "Pesos aplicados", "en": "Weights applied"},
    "esc_validacion": {"es": "Validación de la réplica", "en": "Replica validation"},
    "esc_descargar": {"es": "Descargar el dataset de esta pantalla",
                      "en": "Download the dataset behind this screen"},
    "esc_ausencias": {"es": "Qué no incluye este índice", "en": "What this index leaves out"},
    "esc_repro": {"es": "Reproducibilidad", "en": "Reproducibility"},
    "esc_columna": {"es": "Columna en el archivo original", "en": "Column in the source file"},
    "esc_insumos": {"es": "Insumos", "en": "Inputs"},
    "esc_escala": {"es": "Escala original", "en": "Original scale"},
    "esc_formula": {"es": "Fórmula", "en": "Formula"},
    "esc_aporta": {"es": "aporta", "en": "contributes"},
    "esc_de": {"es": "de", "en": "of"},
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
    "sub_propio": {
        "es": "Modificaste la ponderación, así que esto ya no es el índice de "
              "Heritage. Los datos son los mismos; lo que cambió es cuánto pesa "
              "cada componente.",
        "en": "You changed the weighting, so this is no longer the Heritage index. "
              "The data is the same; what changed is how much each component "
              "weighs."},
    "volver_heritage": {"es": "Volver a los pesos de Heritage",
                        "en": "Back to Heritage weights"},
    "ver_componentes": {"es": "Ver los {n} componentes",
                        "en": "Show the {n} components"},
    "cerrar": {"es": "Cerrar", "en": "Close"},
    "aviso_sin_dato": {
        "es": "El pilar {p} tiene peso pero no tiene datos en {a}. Su peso se "
              "reparte entre los demás. Elegí otro año para usarlo.",
        "en": "Pillar {p} has weight but no data for {a}. Its weight is "
              "redistributed. Pick another year to use it."},
    "esc_rezago": {
        "es": "{comp}: la fuente llega hasta {a1}. Se usa el último dato "
              "disponible, asignado a {a2}, para {n} países. No es imputación: "
              "es un dato real con su año declarado.",
        "en": "{comp}: the source ends in {a1}. The latest available value is "
              "used, assigned to {a2}, for {n} countries. This is not "
              "imputation: it is a real value with its year declared."},
    "esc_arbol": {"es": "Peso real por indicador",
                  "en": "Actual weight per indicator"},
    "arbol_intro": {
        "es": "Heritage promedia sus doce componentes con peso igual: 8,33% cada "
              "uno. Pero cada componente contiene una cantidad distinta de "
              "indicadores. Todos los bloques miden lo mismo; lo que cambia es en "
              "cuántos pedazos está cortado cada uno.",
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
    "codigo_oficial": {
        "es": "La ponderación oficial de Heritage es {c}. Que tenga código igual "
              "que cualquier otra muestra que es un punto más del mismo espacio.",
        "en": "Heritage's official weighting is {c}. That it has a code like any "
              "other shows it is one point in the same space."},
    "tut_boton": {"es": "Armá tu propio índice", "en": "Build your own index"},
    "tut_titulo": {"es": "Tutorial", "en": "Tutorial"},
    "tut_encabezado": {
        "es": "¿Cuánto importa cada cosa?",
        "en": "How much does each thing matter?"},
    "tut_intro": {
        "es": "Calificá de 1 a 10 la importancia que le das a cada componente "
              "para medir la libertad económica de un país. No hay respuestas "
              "correctas: el objetivo es que veas qué implica tu propia "
              "definición. Puntuar todo alto no cambia nada, porque lo que "
              "importa es la importancia relativa.",
        "en": "Rate from 1 to 10 how important each component is for measuring a "
              "country's economic freedom. There are no right answers: the point "
              "is to see what your own definition implies. Rating everything high "
              "changes nothing, since only relative importance matters."},
    "tut_aplicar": {"es": "Ver mi ranking", "en": "See my ranking"},
    "tut_cancelar": {"es": "Cancelar", "en": "Cancel"},
    "intro_barra": {
        "es": "Cada componente vale"
              "|"
              "los puntos que le des: su peso es sus puntos sobre el total. "
              "Subir uno baja el peso "
              "relativo de los demás. Los pilares no se ponderan aparte: su "
              "peso es la suma de los puntos de sus componentes — que es "
              "exactamente cómo funciona el índice original.",
        "en": "Each component is worth|the points you give it. Its weight is its "
              "points over the total, so raising one lowers everyone else's "
              "relative weight. Pillars are not weighted separately: their "
              "weight is the sum of their components' points — which is exactly "
              "how the original index works."},
    "puntos": {"es": "puntos", "en": "points"},
    "indicadores": {"es": "indicadores", "en": "indicators"},
    "indicador": {"es": "indicador", "en": "indicator"},
    "peso_resultante": {"es": "Peso resultante por pilar",
                        "en": "Resulting weight per pillar"},
    "peso_resultante_ayuda": {
        "es": "Nadie eligió estos porcentajes: salen de cuántos componentes "
              "tiene cada pilar y cuántos puntos les diste. Con los puntos de "
              "Heritage, las cuatro categorías dan 25% porque cada una agrupa "
              "tres componentes.",
        "en": "Nobody chose these percentages: they follow from how many "
              "components each pillar has and how many points you gave them. "
              "With Heritage's points, all four categories give 25% because "
              "each groups three components."},
    "elegir_indice": {"es": "Ponderación", "en": "Weighting"},
    "v_ranking": {"es": "Ranking", "en": "Ranking"},
    "v_arbol": {"es": "Peso real por indicador", "en": "Actual weight per indicator"},
    "col_vs": {"es": "Heritage", "en": "Heritage"},
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
              "distintas, y alguien tuvo que decidir cuánto pesa cada una. Esta "
              "página parte del índice de The Heritage Foundation, el más citado "
              "en la prensa, y te deja cambiar esas decisiones para ver qué "
              "pasa. Los datos no se tocan nunca: lo único que cambia es el "
              "peso.",
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
              "uso previsto por sus autores. El único dato que no es de "
              "Heritage es el de propiedad estatal, que arranca en cero puntos y "
              "sólo entra si vos se los das.",
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
              "ningún dato de entrada verificable: son el 16,7% del puntaje "
              "total. Cada componente indica en qué categoría cae.",
        "en": "Not all of the index is equally auditable. Three components have "
              "published formula and inputs and can be recalculated exactly. Two "
              "have a published formula but include a discretionary deduction "
              "not published by country. Five can be reconstructed from "
              "third-party sources, with effort. And two — investment and "
              "financial freedom — are assigned by analyst judgment, with no "
              "verifiable input: they are 16.7% of the total score. Each "
              "component states which category it falls into."},
    "titular": {
        "es": "Heritage promedia sus doce componentes con peso igual. Pero "
              "**{cmax}** se calcula con {nmax} indicador y **{cmin}** con "
              "{nmin}. Resultado: cada indicador de {cmin} pesa **{pmin}** y el "
              "de {cmax} pesa **{pmax}**. **{veces} veces más.**",
        "en": "Heritage averages its twelve components with equal weight. But "
              "**{cmax}** is computed from {nmax} indicator and **{cmin}** from "
              "{nmin}. As a result, each {cmin} indicator weighs **{pmin}** and "
              "the {cmax} one weighs **{pmax}**. **{veces} times more.**"},
    "titular_ver": {"es": "Ver el desglose completo", "en": "See the full breakdown"},
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
    "tut_ojo": {
        "es": "Este componente se calcula con {n} indicadores distintos. Si le "
              "das mucho peso, cada uno de esos indicadores pesa poco por "
              "separado.",
        "en": "This component is computed from {n} different indicators. If you "
              "give it a lot of weight, each of those indicators weighs little "
              "on its own."},
    "col_ind_ayuda": {
        "es": "Cantidad de indicadores distintos con que se calcula ese "
              "componente, según la metodología de Heritage. Es la clave: dos "
              "componentes con los mismos puntos pesan igual entre sí, pero sus "
              "indicadores no.",
        "en": "Number of distinct indicators used to compute that component, per "
              "Heritage's methodology. That is the key: two components with the "
              "same points weigh the same as each other, but their indicators do "
              "not."},
    "peso_por_ind": {"es": "Peso de cada indicador", "en": "Weight of each indicator"},
    "peso_por_ind_ayuda": {
        "es": "Con esta ponderación, el indicador más pesado vale {v} veces el "
              "más liviano. Los puntos son iguales entre componentes; el peso "
              "por indicador no.",
        "en": "Under this weighting, the heaviest indicator is worth {v} times "
              "the lightest. Points are equal across components; weight per "
              "indicator is not."},
    "vintage_viejo": {
        "es": "Los datos construidos son de una versión anterior y no traen el "
              "detalle de subfactores. Corré de nuevo: "
              "python src/build.py --config config/heritage.yaml",
        "en": "The built data is from an older version and lacks sub-factor "
              "detail. Re-run: python src/build.py --config config/heritage.yaml"},
    "aplicar_pesos": {"es": "Aplicar pesos", "en": "Apply weights"},
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
        "es": "«{a}» y «{b}» tienen una correlación de {r}: miden casi lo "
              "mismo. Con los dos activos, esa dimensión pesa el doble sin que "
              "el porcentaje lo diga: es el mismo problema de doble conteo que "
              "este proyecto le señala a los índices compuestos.",
        "en": "\u201c{a}\u201d and \u201c{b}\u201d have a correlation of {r}: "
              "they measure almost the same thing. With both active, that "
              "dimension weighs twice without the percentage saying so: the "
              "same double-counting problem this project points out in "
              "composite indices."},
    "critica": {"es": "Razones para un nuevo índice",
                "en": "Reasons for a new index"},
    "crit_p0": {"es": "Por qué otro índice", "en": "Why another index"},
    "crit_porque": {
        "es": "Ningún índice compuesto es neutral. Promediar doce o trece "
              "números distintos obliga a decidir cuáles entran, cuánto pesa "
              "cada uno y qué se hace con lo que no se puede medir. **Este "
              "índice también toma esas decisiones**, y por eso están todas a "
              "la vista: los pesos se editan en pantalla, el código de "
              "configuración permite reproducir cualquier ponderación, y el "
              "cálculo de cada país se muestra paso a paso.\n\n"
              "No pretende ser perfecto. Pretende ser **mejor en cuatro cosas "
              "concretas** que el índice del que parte.\n\n"
              "**1. Sólo entra lo que mide reglas.** Quedan fuera los cinco "
              "componentes de Heritage que miden otra cosa: integridad del "
              "gobierno y las libertades de inversión y financiera, que son "
              "evaluaciones cualitativas sin insumo verificable; libertad de "
              "empresa, donde tres de sus cuatro subfactores son consecuencias "
              "del desarrollo; y libertad laboral, cuya fórmula compara contra "
              "el promedio mundial y produce resultados que no se sostienen.\n\n"
              "**2. Se mide lo que el Estado posee, no sólo lo que gasta.**[4] "
              "Heritage no tiene ningún componente que mida propiedad estatal "
              "de la economía, inversión pública, control del crédito ni "
              "controles de capital. Los cuatro entran acá, con datos "
              "publicados por el Fraser Institute, una organización del mismo "
              "campo ideológico[5].\n\n"
              "**3. Ninguna dimensión se cuenta dos veces.** Se midió la "
              "correlación entre todos los pares de componentes y se "
              "descartaron los que superaban 0,7 con otro ya incluido. En "
              "Heritage, sus tres componentes de Estado de derecho "
              "correlacionan entre 0,91 y 0,93: pesan 25% pero funcionan como "
              "una sola dimensión.\n\n"
              "**4. Todo se puede rehacer.**[6] Los datos son públicos y sin "
              "modificar, el código está abierto, y la réplica del índice "
              "original se valida en cada compilación contra el puntaje que "
              "Heritage publica.\n\n"
              "Lo que **no** resuelve: sigue dependiendo de componentes cuyos "
              "subfactores nadie publica, sigue siendo un promedio que permite "
              "compensar una dimensión mala con otra buena, y sigue sin medir "
              "la coerción que no ejerce el Estado.",
        "en": "No composite index is neutral. Averaging twelve or thirteen "
              "different numbers forces decisions about what enters, how much "
              "each weighs and what to do with what cannot be measured. **This "
              "index makes those decisions too**, which is why they are all "
              "visible.\n\n"
              "It does not claim to be perfect. It claims to be **better in "
              "four concrete ways** than the index it starts from: only "
              "rule-measuring components enter; what the state owns is measured, "
              "not only what it spends; no dimension is counted twice; and "
              "everything can be redone from public data and open code.\n\n"
              "What it does **not** solve: it still depends on components whose "
              "sub-factors nobody publishes, it is still an average that lets "
              "one dimension offset another, and it still does not measure "
              "coercion not exercised by the state."},
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
              "que en una sociedad libre los gobiernos se abstienen de coaccionar "
              "más allá de lo necesario para proteger y mantener la libertad "
              "misma.\n\n"
              "**Pero la fórmula del componente de gasto público[1] toma el gasto "
              "cero como óptimo.** Si el criterio es no coaccionar más allá de "
              "lo necesario para proteger la libertad, entonces el gasto que "
              "sostiene tribunales y policía no es una pérdida de libertad. La "
              "fórmula lo trata como tal: `100 − 0,03 × G²` sólo llega a 100 "
              "cuando el gasto es cero. Hay una distancia medible entre la "
              "definición declarada y el cálculo.\n\n"
              "La propia metodología[1] admite el problema: reconoce que tomar el "
              "gasto cero como referencia puede dar puntajes artificialmente "
              "altos a países con poca capacidad estatal, y confía en que los "
              "demás componentes los penalicen.\n\n"
              "**Segunda distancia: la definición habla de controlar la propia "
              "propiedad, pero ningún componente mide quién es dueño de qué.** "
              "El componente de derechos de propiedad mide seguridad y "
              "cumplimiento, no titularidad. Por eso Singapur puntúa 89,2 con "
              "el Estado dueño de más del 90% del suelo, que vende en "
              "concesiones de 99 años.",
        "en": "Heritage defines economic freedom as every person's right to "
              "control their own labor and property, and adds that in a free "
              "society governments refrain from coercion beyond what is needed "
              "to protect and maintain liberty itself.\n\n"
              "**Yet the government spending formula[1] takes zero spending as the "
              "optimum.** If the criterion is not coercing beyond what is needed "
              "to protect liberty, then the spending that sustains courts and "
              "police is not a loss of freedom. The formula treats it as one: "
              "`100 − 0.03 × G²` only reaches 100 when spending is zero.\n\n"
              "Their own methodology concedes the issue: it acknowledges that "
              "using zero spending as the benchmark may give artificially high "
              "scores to countries with little state capacity.\n\n"
              "**A second gap: the definition speaks of controlling one's own "
              "property, but no component measures who owns what.** The property "
              "rights component measures security and enforcement, not "
              "ownership. Hence Singapore scores 89.2 while the state owns over "
              "90% of the land."},
    "crit_casos": {
        "es": "**Austria primera en libertad laboral, Paraguay 163º.**[2] Austria "
              "tiene negociación colectiva sectorial que cubre a casi toda su "
              "fuerza de trabajo, y encabeza igual con 81,6. Paraguay saca "
              "44,1. Dos razones se combinan: el componente incluye "
              "productividad y participación laboral, que son resultados "
              "económicos y no reglas; y la fórmula de los primeros siete "
              "subfactores compara cada valor contra el promedio mundial, así "
              "que un salario mínimo alto pesa poco si el valor agregado por "
              "trabajador también lo es. Un país rico con regulación fuerte "
              "puede superar a uno pobre con regulación débil.\n\n"
              "**Singapur primero en el índice, 67º en efectividad judicial.**[2] "
              "Su peor componente es 58,3, por debajo de Argentina (58,2), y "
              "aun así queda primero en el total: el promedio aritmético "
              "permite que once componentes compensen a uno.\n\n"
              "**Estados Unidos comparte el primer puesto en libertad "
              "financiera con 80.**[2] El valor 90 no lo alcanza nadie; hay 16 "
              "países en 80. El componente mide el estado actual del sector, "
              "no la disposición del Estado a intervenir: un país que rescató "
              "a su banca y volvió a soltarla puntúa igual que uno que nunca "
              "intervino.\n\n"
              "**Peso igual entre componentes no es peso igual entre "
              "indicadores.**[1] Heritage promedia sus doce componentes con peso "
              "igual, 8,33% cada uno. Pero gasto público se calcula con un "
              "indicador y libertad laboral con nueve: cada indicador laboral "
              "pesa 0,93% y el de gasto público 8,33%. Nueve veces más. Y "
              "salud fiscal reparte 80/20 internamente entre déficit y deuda, "
              "una ponderación desigual declarada dentro de un índice que se "
              "presenta como de peso igual.\n\n"
              "**Libertad de empresa mide desarrollo, no reglas.**[1] Sus cuatro "
              "subfactores pesan igual: acceso a electricidad, riesgo del "
              "entorno de negocios, calidad regulatoria e inclusión económica "
              "de la mujer. Sólo el tercero mide una regla. El acceso a "
              "electricidad es infraestructura: un país sin red eléctrica no "
              "es menos libre, es más pobre. El riesgo del entorno es una "
              "evaluación de agencias de seguro de crédito, o sea el juicio de "
              "quien vende cobertura sobre qué tan riesgoso es cobrar ahí. La "
              "inclusión económica de la mujer mide un resultado social. Tres "
              "de los cuatro son consecuencias del desarrollo, no causas de "
              "libertad.\n\n"
              "Eso produce circularidad: el índice incorpora indicadores de "
              "desarrollo y después se lo usa para mostrar que la libertad "
              "económica produce desarrollo. Y castiga a los países pobres dos "
              "veces, porque ser pobre baja el puntaje de un componente que "
              "dice medir libertad.",
        "en": "**Austria first in labor freedom, Paraguay 163rd.** Austria has "
              "sectoral collective bargaining covering nearly its whole "
              "workforce and still leads with 81.6. Two reasons combine: the "
              "component includes productivity and participation, which are "
              "outcomes rather than rules; and the formula compares each value "
              "against the world average.\n\n"
              "**Singapore first overall, 67th in judicial effectiveness.** Its "
              "worst component is 58.3, below Argentina's 58.2, and it still "
              "ranks first: the arithmetic mean lets eleven components offset "
              "one.\n\n"
              "**The United States shares first place in financial freedom with "
              "80.** No country reaches 90. The component measures the sector's "
              "current state, not the state's willingness to intervene.\n\n"
              "**Development indicators inside freedom components.** Business "
              "freedom includes access to electricity among its four "
              "sub-factors."},
    "crit_opacidad": {
        "es": "**Heritage publica los promedios, no los sumandos.**[2] El archivo "
              "trae doce columnas, una por componente. Libertad laboral llega "
              "como un solo número —77,0 para Singapur— y los nueve subfactores "
              "que lo componen ya vinieron promediados adentro. La metodología "
              "dice cuáles son y cómo se combinan, pero **los valores por país "
              "no existen en ningún archivo público**. Se puede verificar que "
              "Singapur saca 77,0; no se puede verificar cómo se llegó a ese "
              "77,0.\n\n"
              "Eso se repite en nueve de los doce componentes. Sólo gasto "
              "público, carga tributaria y salud fiscal son auditables de punta "
              "a punta: tienen fórmula e insumos publicados y se recalculan al "
              "decimal.\n\n"
              "**Y dos componentes no tienen ningún insumo.**[1] Libertad de "
              "inversión arranca en 100 y descuenta 5, 10, 15, 20 o 25 puntos "
              "según evaluación cualitativa. Libertad financiera se asigna en "
              "escalones de diez a criterio del analista. Son 16,7% del puntaje "
              "total sin nada que auditar.\n\n"
              "**Dos componentes más esconden un descuento.** Libertad "
              "monetaria y comercial publican su fórmula, pero después restan "
              "una penalización discrecional —por controles de precios y por "
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
    "fuente_vdem": {"es": "V-Dem, base de datos país-año",
                    "en": "V-Dem, country-year dataset"},
    "fuente_repo": {"es": "Código y datos de esta página",
                    "en": "Code and data of this page"},
    "ayuda_p0": {"es": "Qué mide cada componente",
                 "en": "What each component measures"},
    "ayuda_p0_txt": {
        "es": "Todos los componentes van de 0 a 100 y más alto siempre "
              "significa más libre según la definición de Heritage. El puntaje "
              "total es el promedio ponderado por los puntos que asignes. Cada fila "
              "enlaza a la fuente de la que sale el dato.[1][4]",
        "en": "All components run from 0 to 100 and higher always means freer "
              "under Heritage's definition. The total score is the average "
              "weighted by the points you assign."},
    "col_mide": {"es": "Qué mide", "en": "What it measures"},
    "col_cien": {"es": "100 significa", "en": "100 means"},
    "col_comp": {"es": "Componente", "en": "Component"},
    "col_origen": {"es": "Origen", "en": "Source"},
    "calc_elegir": {"es": "Elegí un país", "en": "Pick a country"},
    "calc_intro": {
        "es": "Cada línea muestra el puntaje publicado por la fuente, el peso "
              "que le diste, y el aporte al total. La suma de la última columna "
              "es el puntaje del país. Con la ponderación original de Heritage "
              "el resultado tiene que coincidir con el puntaje que ellos "
              "publican[2], y la diferencia se muestra al final.",
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
        "es": "La palabra «libertad» está en disputa y los índices que dicen "
              "medirla toman decisiones que casi nunca se ven"
              "|"
              ". Esta página pretende resolver este problema. "
              "Primero reconstruye el Index of Economic Freedom de The "
              "Heritage Foundation con sus propios datos y muestra dónde su "
              "cálculo se aparta de su propia definición: qué mide, qué no "
              "mide, y qué pasa con el ranking cuando se cambian los pesos. "
              "Esto nos permite armar un nuevo índice que presentamos como "
              "«Índice de Liberalismo económico» y que puede ser "
              "escrutado en detalle.",
        "en": "The word \u201cfreedom\u201d is contested, and the indices that "
              "claim to measure it make decisions that are rarely visible"
              "|"
              ". This page sets out to address that. "
              "It first reconstructs The Heritage Foundation's Index of "
              "Economic Freedom from its own data and shows where its "
              "computation departs from its own definition: what it measures, "
              "what it does not, and what happens to the ranking when the "
              "weights change. That allows us to build a new index, presented "
              "here as the \u201cEconomic Liberalism Index\u201d, which "
              "can be scrutinized in detail.",
    },
    "volver_defecto": {"es": "Volver al índice por defecto",
                       "en": "Back to the default index"},
    "ver_razones": {
        "es": "El detalle de estas decisiones está en «{b}», arriba a la derecha.",
        "en": "The detail of these decisions is in \u201c{b}\u201d, top right."},
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
