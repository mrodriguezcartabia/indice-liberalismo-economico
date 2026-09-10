"""Código corto para una configuración de pesos.

Cada componente recibe puntos de 0 a 100 en pasos de 5, así que el espacio de
configuraciones es finito y se puede nombrar con una cadena breve.

Sirve para tres cosas:
  - que el visitante guarde su ponderación y vuelva a ella
  - que una configuración sea citable: "la configuración HF-... ubica a Suiza
    primera" es una afirmación que cualquiera puede reproducir
  - que la ponderación oficial tenga su propio código, lo que muestra que es un
    punto más del mismo espacio y no un punto privilegiado

No es criptografía ni un identificador con estado: el código ES el vector de
puntos escrito en base 32. No se guarda nada en ningún servidor.
"""

from __future__ import annotations

# Sin I, L, O ni U: se confunden al leerlas o al dictarlas.
ALFABETO = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
PASO = 5
MAX_PUNTOS = 100
NIVELES = MAX_PUNTOS // PASO + 1          # 0, 5, 10 ... 100 -> 21 niveles


def _a_base32(n: int, largo: int) -> str:
    s = ""
    for _ in range(largo):
        s = ALFABETO[n % 32] + s
        n //= 32
    return s


def _de_base32(s: str) -> int:
    n = 0
    for c in s:
        if c not in ALFABETO:
            raise ValueError(c)
        n = n * 32 + ALFABETO.index(c)
    return n


def _largo(claves) -> int:
    bits = len(claves) * (NIVELES - 1).bit_length()
    return max(2, -(-bits // 5))


def codificar(sigla: str, puntos: dict[str, float], claves: list[str]) -> str:
    n = 0
    for k in claves:
        v = max(0, min(NIVELES - 1, round(puntos.get(k, 0) / PASO)))
        n = n * NIVELES + v
    cuerpo = _a_base32(n, _largo(claves))
    # Se parte al medio: una cadena larga sin cortes es imposible de dictar.
    mitad = len(cuerpo) // 2
    return f"{sigla.upper()}-{cuerpo[:mitad]}-{cuerpo[mitad:]}"


def decodificar(codigo: str, claves: list[str]) -> dict[str, int] | None:
    """Devuelve los puntos por componente, o None si el código no es válido."""
    try:
        partes = codigo.strip().upper().replace(" ", "").split("-")
        if len(partes) < 2:
            return None
        n = _de_base32("".join(partes[1:]))
    except (ValueError, AttributeError):
        return None
    vals = []
    for _ in claves:
        vals.append((n % NIVELES) * PASO)
        n //= NIVELES
    vals.reverse()
    if n != 0 or sum(vals) == 0:
        return None
    return dict(zip(claves, vals))


def pesos_desde_puntos(puntos: dict[str, float]) -> dict[str, float]:
    total = sum(puntos.values())
    if total <= 0:
        return {k: 0.0 for k in puntos}
    return {k: v / total for k, v in puntos.items()}
