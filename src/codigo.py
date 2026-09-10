"""Código corto para una configuración de pesos.

El código ES el vector de puntos, escrito de forma compacta. No hay nada
guardado en ningún servidor: quien lo escribe reproduce exactamente el mismo
ranking.

Dos modos, porque casi todas las configuraciones útiles son del primero:

  Modo I (igual)  — todos los componentes activos pesan lo mismo. Alcanza con
                    decir cuáles están prendidos: un bit por componente. Con 21
                    componentes son 21 bits, o sea cinco caracteres.
  Modo P (pesos)  — pesos distintos entre sí. Hace falta el vector completo.

La ponderación oficial de Heritage entra en el modo I, igual que cualquier otra
propuesta de pesos iguales. Que tenga un código tan corto y tan común como
cualquiera es parte de lo que la página muestra.
"""

from __future__ import annotations

# Sin I, L, O ni U: se confunden al leerlas o al dictarlas.
ALFABETO = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
PASO = 5
MAX_PUNTOS = 100
NIVELES = MAX_PUNTOS // PASO + 1          # 0, 5, 10 ... 100


def _a_base32(n: int, largo: int) -> str:
    s = ""
    for _ in range(largo):
        s, n = ALFABETO[n % 32] + s, n // 32
    return s


def _de_base32(s: str) -> int:
    n = 0
    for c in s:
        if c not in ALFABETO:
            raise ValueError(c)
        n = n * 32 + ALFABETO.index(c)
    return n


def _largo(bits: int) -> int:
    return max(1, -(-bits // 5))


def _partir(cuerpo: str) -> str:
    """Corta en grupos de cuatro: una cadena larga sin cortes no se dicta."""
    if len(cuerpo) <= 5:
        return cuerpo
    return "-".join(cuerpo[i:i + 4] for i in range(0, len(cuerpo), 4))


def codificar(sigla: str, puntos: dict[str, float], claves: list[str]) -> str:
    activos = [k for k in claves if puntos.get(k, 0) > 0]
    valores = {puntos.get(k, 0) for k in activos}

    if len(valores) <= 1:                                   # modo I
        n = 0
        for k in claves:
            n = n * 2 + (1 if puntos.get(k, 0) > 0 else 0)
        cuerpo = _a_base32(n, _largo(len(claves)))
        return f"{sigla.upper()}-I{_partir(cuerpo)}"

    n = 0                                                   # modo P
    for k in claves:
        v = max(0, min(NIVELES - 1, round(puntos.get(k, 0) / PASO)))
        n = n * NIVELES + v
    bits = len(claves) * (NIVELES - 1).bit_length()
    return f"{sigla.upper()}-P{_partir(_a_base32(n, _largo(bits)))}"


def decodificar(codigo: str, claves: list[str]) -> dict[str, int] | None:
    """Devuelve los puntos por componente, o None si el código no es válido."""
    try:
        sigla, resto = codigo.strip().upper().replace(" ", "").split("-", 1)
        cuerpo = resto.replace("-", "")
        modo, cuerpo = cuerpo[0], cuerpo[1:]
        n = _de_base32(cuerpo)
    except (ValueError, AttributeError, IndexError):
        return None

    if modo == "I":
        bits = []
        for _ in claves:
            bits.append(n % 2)
            n //= 2
        bits.reverse()
        if n != 0 or not any(bits):
            return None
        return {k: (10 if b else 0) for k, b in zip(claves, bits)}

    if modo == "P":
        vals = []
        for _ in claves:
            vals.append((n % NIVELES) * PASO)
            n //= NIVELES
        vals.reverse()
        if n != 0 or sum(vals) == 0:
            return None
        return dict(zip(claves, vals))

    return None


def pesos_desde_puntos(puntos: dict[str, float]) -> dict[str, float]:
    total = sum(puntos.values())
    if total <= 0:
        return {k: 0.0 for k in puntos}
    return {k: v / total for k, v in puntos.items()}
