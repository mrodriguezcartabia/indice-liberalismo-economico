"""Normalizacion de nombres de pais a ISO3.

Todo el pipeline usa ISO3 como clave unica. Cualquier fuente nueva entra por
`to_iso3()`. Si un nombre no matchea devuelve None: nunca se adivina, se reporta.
"""

from __future__ import annotations

import unicodedata

# --- Espanol (datosmacro / fuentes en castellano) --------------------------
ES = {
    "afganistan": "AFG", "albania": "ALB", "alemania": "DEU", "andorra": "AND",
    "angola": "AGO", "antigua y barbuda": "ATG", "arabia saudita": "SAU",
    "argelia": "DZA", "argentina": "ARG", "armenia": "ARM", "australia": "AUS",
    "austria": "AUT", "azerbaiyan": "AZE", "bahamas": "BHS", "banglades": "BGD",
    "barbados": "BRB", "barein": "BHR", "belice": "BLZ", "benin": "BEN",
    "bielorrusia": "BLR", "bolivia": "BOL", "bosnia y herzegovina": "BIH",
    "botsuana": "BWA", "brasil": "BRA", "brunei": "BRN", "bulgaria": "BGR",
    "burkina faso": "BFA", "burundi": "BDI", "butan": "BTN", "belgica": "BEL",
    "cabo verde": "CPV", "camboya": "KHM", "camerun": "CMR", "canada": "CAN",
    "catar": "QAT", "chad": "TCD", "chequia": "CZE", "chile": "CHL",
    "china": "CHN", "chipre": "CYP", "colombia": "COL", "comoras": "COM",
    "corea del sur": "KOR", "costa rica": "CRI", "costa de marfil": "CIV",
    "croacia": "HRV", "cuba": "CUB", "dinamarca": "DNK", "dominica": "DMA",
    "ecuador": "ECU", "egipto": "EGY", "el salvador": "SLV",
    "emiratos arabes unidos": "ARE", "eritrea": "ERI", "eslovaquia": "SVK",
    "eslovenia": "SVN", "espana": "ESP", "estado de palestina": "PSE",
    "estados federados de micronesia": "FSM", "estados unidos": "USA",
    "estonia": "EST", "eswatini": "SWZ", "etiopia": "ETH", "filipinas": "PHL",
    "finlandia": "FIN", "fiyi": "FJI", "francia": "FRA", "gabon": "GAB",
    "gambia": "GMB", "georgia": "GEO", "ghana": "GHA", "granada": "GRD",
    "grecia": "GRC", "guatemala": "GTM", "guinea": "GIN",
    "guinea ecuatorial": "GNQ", "guinea-bisau": "GNB", "guyana": "GUY",
    "haiti": "HTI", "honduras": "HND", "hong kong": "HKG", "hungria": "HUN",
    "india": "IND", "indonesia": "IDN", "irak": "IRQ", "irlanda": "IRL",
    "iran": "IRN", "islandia": "ISL", "islas marshall": "MHL",
    "islas salomon": "SLB", "israel": "ISR", "italia": "ITA", "jamaica": "JAM",
    "japon": "JPN", "jordania": "JOR", "kazajistan": "KAZ", "kenia": "KEN",
    "kirguistan": "KGZ", "kiribati": "KIR", "kuwait": "KWT", "laos": "LAO",
    "lesoto": "LSO", "letonia": "LVA", "liberia": "LBR", "libia": "LBY",
    "liechtenstein": "LIE", "lituania": "LTU", "luxemburgo": "LUX",
    "libano": "LBN", "macedonia del norte": "MKD", "madagascar": "MDG",
    "malasia": "MYS", "malaui": "MWI", "maldivas": "MDV", "malta": "MLT",
    "mali": "MLI", "marruecos": "MAR", "mauricio": "MUS", "mauritania": "MRT",
    "moldavia": "MDA", "mongolia": "MNG", "montenegro": "MNE",
    "mozambique": "MOZ", "myanmar": "MMR", "mexico": "MEX", "namibia": "NAM",
    "nauru": "NRU", "nepal": "NPL", "nicaragua": "NIC", "nigeria": "NGA",
    "noruega": "NOR", "nueva zelanda": "NZL", "niger": "NER", "oman": "OMN",
    "pakistan": "PAK", "palaos": "PLW", "panama": "PAN",
    "papua nueva guinea": "PNG", "paraguay": "PRY", "paises bajos": "NLD",
    "peru": "PER", "polonia": "POL", "portugal": "PRT", "reino unido": "GBR",
    "republica centroafricana": "CAF", "republica democratica del congo": "COD",
    "republica dominicana": "DOM", "republica del congo": "COG",
    "ruanda": "RWA", "rumania": "ROU", "rusia": "RUS", "samoa": "WSM",
    "san cristobal y nieves": "KNA", "san marino": "SMR",
    "san vicente y las granadinas": "VCT", "santa lucia": "LCA",
    "santo tome y principe": "STP", "senegal": "SEN", "serbia": "SRB",
    "seychelles": "SYC", "sierra leona": "SLE", "singapur": "SGP",
    "siria": "SYR", "somalia": "SOM", "sri lanka": "LKA", "sudafrica": "ZAF",
    "sudan": "SDN", "sudan del sur": "SSD", "suecia": "SWE", "suiza": "CHE",
    "surinam": "SUR", "tailandia": "THA", "taiwan": "TWN", "tanzania": "TZA",
    "tayikistan": "TJK", "timor oriental": "TLS", "togo": "TGO",
    "tonga": "TON", "trinidad y tobago": "TTO", "turkmenistan": "TKM",
    "tuvalu": "TUV", "tunez": "TUN", "turkiye": "TUR", "turquia": "TUR",
    "ucrania": "UKR", "uganda": "UGA", "uruguay": "URY", "uzbekistan": "UZB",
    "vanuatu": "VUT", "venezuela": "VEN", "viet nam": "VNM", "vietnam": "VNM",
    "yemen": "YEM", "yibuti": "DJI", "zambia": "ZMB", "zimbabue": "ZWE",
}

# --- Ingles (OMC, Banco Mundial, FMI, V-Dem, Fraser, Heritage) -------------
EN = {
    "the bahamas": "BHS", "burma": "MMR", "democratic republic of congo": "COD",
    "republic of congo": "COG", "north korea": "PRK", "korea, dem. rep.": "PRK",
    "korea, north": "PRK", "kosovo": "XKX", "micronesia": "FSM",
    "cote d'ivoire ": "CIV", "eswatini (swaziland)": "SWZ", "macau": "MAC",
    "afghanistan": "AFG", "albania": "ALB", "algeria": "DZA", "andorra": "AND",
    "angola": "AGO", "antigua and barbuda": "ATG", "argentina": "ARG",
    "armenia": "ARM", "australia": "AUS", "austria": "AUT", "azerbaijan": "AZE",
    "bahamas": "BHS", "bahamas, the": "BHS", "bahrain": "BHR",
    "bahrain, kingdom of": "BHR", "bangladesh": "BGD", "barbados": "BRB",
    "belarus": "BLR", "belgium": "BEL", "belize": "BLZ", "benin": "BEN",
    "bhutan": "BTN", "bolivia": "BOL", "bolivia, plurinational state of": "BOL",
    "bosnia and herzegovina": "BIH", "botswana": "BWA", "brazil": "BRA",
    "brunei": "BRN", "brunei darussalam": "BRN", "bulgaria": "BGR",
    "burkina faso": "BFA", "burundi": "BDI", "cabo verde": "CPV",
    "cape verde": "CPV", "cambodia": "KHM", "cameroon": "CMR", "canada": "CAN",
    "central african republic": "CAF", "chad": "TCD", "chile": "CHL",
    "china": "CHN", "chinese taipei": "TWN", "taiwan": "TWN",
    "taiwan, china": "TWN", "colombia": "COL", "comoros": "COM",
    "congo, dem. rep.": "COD", "congo, rep.": "COG",
    "democratic republic of the congo": "COD", "republic of the congo": "COG",
    "costa rica": "CRI", "cote d'ivoire": "CIV", "cote divoire": "CIV",
    "ivory coast": "CIV", "croatia": "HRV", "cuba": "CUB", "cyprus": "CYP",
    "czech republic": "CZE", "czechia": "CZE", "denmark": "DNK",
    "djibouti": "DJI", "dominica": "DMA", "dominican republic": "DOM",
    "ecuador": "ECU", "egypt": "EGY", "egypt, arab rep.": "EGY",
    "el salvador": "SLV", "equatorial guinea": "GNQ", "eritrea": "ERI",
    "estonia": "EST", "eswatini": "SWZ", "swaziland": "SWZ", "ethiopia": "ETH",
    "fiji": "FJI", "finland": "FIN", "france": "FRA", "gabon": "GAB",
    "gambia": "GMB", "the gambia": "GMB", "gambia, the": "GMB",
    "georgia": "GEO", "germany": "DEU", "ghana": "GHA", "greece": "GRC",
    "grenada": "GRD", "guatemala": "GTM", "guinea": "GIN",
    "guinea-bissau": "GNB", "guyana": "GUY", "haiti": "HTI", "honduras": "HND",
    "hong kong": "HKG", "hong kong, china": "HKG", "hong kong sar, china": "HKG",
    "hungary": "HUN", "iceland": "ISL", "india": "IND", "indonesia": "IDN",
    "iran": "IRN", "iran, islamic rep.": "IRN", "iraq": "IRQ",
    "ireland": "IRL", "israel": "ISR", "italy": "ITA", "jamaica": "JAM",
    "japan": "JPN", "jordan": "JOR", "kazakhstan": "KAZ", "kenya": "KEN",
    "kiribati": "KIR", "korea, republic of": "KOR", "korea, rep.": "KOR",
    "south korea": "KOR", "kuwait": "KWT", "kuwait, the state of": "KWT",
    "kyrgyz republic": "KGZ", "kyrgyzstan": "KGZ", "lao pdr": "LAO",
    "lao people's democratic republic": "LAO", "laos": "LAO", "latvia": "LVA",
    "lebanon": "LBN", "lesotho": "LSO", "liberia": "LBR", "libya": "LBY",
    "liechtenstein": "LIE", "lithuania": "LTU", "luxembourg": "LUX",
    "macao, china": "MAC", "macao sar, china": "MAC", "madagascar": "MDG",
    "malawi": "MWI", "malaysia": "MYS", "maldives": "MDV", "mali": "MLI",
    "malta": "MLT", "marshall islands": "MHL", "mauritania": "MRT",
    "mauritius": "MUS", "mexico": "MEX", "micronesia, fed. sts.": "FSM",
    "moldova": "MDA", "moldova, republic of": "MDA", "mongolia": "MNG",
    "montenegro": "MNE", "morocco": "MAR", "mozambique": "MOZ",
    "myanmar": "MMR", "namibia": "NAM", "nauru": "NRU", "nepal": "NPL",
    "netherlands": "NLD", "new zealand": "NZL", "nicaragua": "NIC",
    "niger": "NER", "nigeria": "NGA", "north macedonia": "MKD",
    "norway": "NOR", "oman": "OMN", "pakistan": "PAK", "palau": "PLW",
    "panama": "PAN", "papua new guinea": "PNG", "paraguay": "PRY",
    "peru": "PER", "philippines": "PHL", "poland": "POL", "portugal": "PRT",
    "qatar": "QAT", "romania": "ROU", "russia": "RUS",
    "russian federation": "RUS", "rwanda": "RWA",
    "saint kitts and nevis": "KNA", "saint lucia": "LCA",
    "saint vincent and the grenadines": "VCT", "samoa": "WSM",
    "san marino": "SMR", "sao tome and principe": "STP",
    "saudi arabia": "SAU", "saudi arabia, kingdom of": "SAU",
    "senegal": "SEN", "serbia": "SRB", "seychelles": "SYC",
    "sierra leone": "SLE", "singapore": "SGP", "slovak republic": "SVK",
    "slovakia": "SVK", "slovenia": "SVN", "solomon islands": "SLB",
    "somalia": "SOM", "south africa": "ZAF", "south sudan": "SSD",
    "spain": "ESP", "sri lanka": "LKA", "sudan": "SDN", "suriname": "SUR",
    "sweden": "SWE", "switzerland": "CHE", "syria": "SYR",
    "syrian arab republic": "SYR", "tajikistan": "TJK", "tanzania": "TZA",
    "thailand": "THA", "timor-leste": "TLS", "togo": "TGO", "tonga": "TON",
    "trinidad and tobago": "TTO", "tunisia": "TUN", "turkey": "TUR",
    "turkiye": "TUR", "turkmenistan": "TKM", "tuvalu": "TUV", "uganda": "UGA",
    "ukraine": "UKR", "united arab emirates": "ARE", "united kingdom": "GBR",
    "united states": "USA", "united states of america": "USA",
    "uruguay": "URY", "uzbekistan": "UZB", "vanuatu": "VUT",
    "venezuela": "VEN", "venezuela, bolivarian republic of": "VEN",
    "venezuela, rb": "VEN", "viet nam": "VNM", "vietnam": "VNM",
    "west bank and gaza": "PSE", "state of palestine": "PSE", "yemen": "YEM",
    "yemen, rep.": "YEM", "zambia": "ZMB", "zimbabwe": "ZWE",
}

# Agregados, no paises. Se excluyen del panel y se reportan aparte.
AGGREGATES = {
    "european union", "world", "grand total", "africa", "asia", "europe",
    "middle east", "north america", "cis",
    "south and central america and the caribbean", "euro area", "oecd members",
}


def _key(name: str) -> str:
    """Minusculas, sin acentos, sin sufijos de scraping ('[+]')."""
    s = str(name).replace("[+]", "").strip().lower()
    # Apostrofes tipograficos: 'Cote d’Ivoire' no matchea con "cote d'ivoire"
    for raro in ("’", "‘", "ʼ", "`", "´"):
        s = s.replace(raro, "'")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.split())


def to_iso3(name: str) -> str | None:
    """Devuelve ISO3, o None si el nombre no esta en ninguna tabla.

    None NO significa cero ni dato faltante del pais: significa que no
    resolvimos el nombre. `build.py` lo reporta como fila sin matchear.
    """
    if name is None:
        return None
    k = _key(name)
    if not k or k in AGGREGATES:
        return None
    return ES.get(k) or EN.get(k)


def is_aggregate(name: str) -> bool:
    return _key(name) in AGGREGATES


# --- ISO3 -> nombre para mostrar -------------------------------------------
# Los diccionarios de arriba estan sin acentos porque son para MATCHEAR texto
# de entrada. Para MOSTRAR hacen falta los nombres bien escritos.
_ACENTOS = {
    "AFG": "Afganistán", "DEU": "Alemania", "SAU": "Arabia Saudita",
    "DZA": "Argelia", "AZE": "Azerbaiyán", "BGD": "Bangladés",
    "BHR": "Baréin", "BEL": "Bélgica", "BWA": "Botsuana", "BTN": "Bután",
    "KHM": "Camboya", "CMR": "Camerún", "CAN": "Canadá", "CZE": "Chequia",
    "KOR": "Corea del Sur", "CIV": "Costa de Marfil", "SVK": "Eslovaquia",
    "ESP": "España", "USA": "Estados Unidos", "ETH": "Etiopía",
    "PHL": "Filipinas", "GAB": "Gabón", "GNQ": "Guinea Ecuatorial",
    "GNB": "Guinea-Bisáu", "HTI": "Haití", "HUN": "Hungría", "IRQ": "Irak",
    "IRN": "Irán", "ISL": "Islandia", "JPN": "Japón", "KAZ": "Kazajistán",
    "KEN": "Kenia", "KGZ": "Kirguistán", "LAO": "Laos", "LSO": "Lesoto",
    "LBN": "Líbano", "LBY": "Libia", "LTU": "Lituania", "MKD": "Macedonia del Norte",
    "MYS": "Malasia", "MWI": "Malaui", "MLI": "Malí", "MUS": "Mauricio",
    "MDA": "Moldavia", "MEX": "México", "NER": "Níger", "NLD": "Países Bajos",
    "PAK": "Pakistán", "PLW": "Palaos", "PAN": "Panamá", "PER": "Perú",
    "GBR": "Reino Unido", "CAF": "República Centroafricana",
    "COD": "R. D. del Congo", "COG": "República del Congo",
    "DOM": "República Dominicana", "RWA": "Ruanda", "ROU": "Rumania",
    "RUS": "Rusia", "KNA": "San Cristóbal y Nieves", "LCA": "Santa Lucía",
    "VCT": "San Vicente y las Granadinas", "STP": "Santo Tomé y Príncipe",
    "SLE": "Sierra Leona", "SGP": "Singapur", "ZAF": "Sudáfrica",
    "SDN": "Sudán", "SSD": "Sudán del Sur", "CHE": "Suiza", "SUR": "Surinam",
    "TWN": "Taiwán", "TJK": "Tayikistán", "TLS": "Timor Oriental",
    "TUN": "Túnez", "TUR": "Turquía", "TKM": "Turkmenistán",
    "UZB": "Uzbekistán", "VNM": "Vietnam", "YEM": "Yemen", "DJI": "Yibuti",
    "ZWE": "Zimbabue", "PSE": "Palestina", "FSM": "Micronesia",
    "PRK": "Corea del Norte", "XKX": "Kosovo",
    "MHL": "Islas Marshall", "SLB": "Islas Salomón", "ATG": "Antigua y Barbuda",
    "BIH": "Bosnia y Herzegovina", "TTO": "Trinidad y Tobago",
    "PNG": "Papúa Nueva Guinea", "NZL": "Nueva Zelanda", "HKG": "Hong Kong",
    "MAC": "Macao", "ARE": "Emiratos Árabes Unidos", "QAT": "Catar",
    "PRT": "Portugal", "GRC": "Grecia", "IND": "India", "CHN": "China",
}
_MINUSCULAS = {"de", "del", "la", "las", "los", "y"}


def _titulo(texto: str) -> str:
    palabras = texto.split()
    return " ".join(p if i and p in _MINUSCULAS else p.capitalize()
                    for i, p in enumerate(palabras))


_NOMBRES = {}
for _k, _v in ES.items():                     # primer nombre en espanol gana
    _NOMBRES.setdefault(_v, _titulo(_k))
for _k, _v in EN.items():                     # completa lo que falte
    _NOMBRES.setdefault(_v, _titulo(_k))
_NOMBRES.update(_ACENTOS)                     # y los bien escritos mandan


def nombre(iso3: str) -> str:
    """Nombre para mostrar. Si no lo conoce, devuelve el propio ISO3."""
    return _NOMBRES.get(iso3, iso3)
