"""PDF imprimible del ranking en pantalla.

Incluye siempre el código de configuración, la fecha de corte, la fuente y el
enlace al repositorio: un ranking que circula sin esos cuatro datos no se puede
verificar, y la página entera está construida sobre la idea de que sí se pueda.
"""

from __future__ import annotations

from fpdf import FPDF

TINTA = (19, 26, 23)
TENUE = (107, 122, 114)
SENAL = (15, 107, 92)
LINEA = (213, 218, 210)

# Helvetica sólo cubre latin-1: las comillas y rayas tipográficas de los textos
# se pasan a su equivalente simple y cualquier otro carácter se reemplaza por "?".
SIMPLES = str.maketrans({"\u201c": '"', "\u201d": '"', "\u2018": "'",
                         "\u2019": "'", "\u2013": "-", "\u2014": "-",
                         "\u2026": "..."})


class Hoja(FPDF):
    def __init__(self, pie: str):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.pie_texto = pie
        self.set_auto_page_break(True, margin=18)

    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", size=7)
        self.set_text_color(*TENUE)
        self.cell(0, 4, self.pie_texto, align="L")
        self.cell(0, 4, str(self.page_no()), align="R")

    def normalize_text(self, text):
        text = text.translate(SIMPLES).encode("latin-1", "replace").decode("latin-1")
        return super().normalize_text(text)


def generar(titulo: str, subtitulo: str, filas: list[tuple],
            meta: dict, etiquetas: dict, pesos: list[tuple]) -> bytes:
    """`filas` son (puesto, país, puntaje, puesto_original o None)."""
    pie = f"{etiquetas['codigo']}: {meta['codigo']}  ·  {meta['repo']}"
    pdf = Hoja(pie)
    pdf.add_page()

    pdf.set_font("Helvetica", size=7)
    pdf.set_text_color(*TENUE)
    pdf.cell(0, 4, f"{meta['fuente']}  ·  {etiquetas['corte']} {meta['corte']}"
                   f"  ·  {etiquetas['anio']} {meta['anio']}", new_y="NEXT")

    pdf.set_font("Helvetica", "B", 19)
    pdf.set_text_color(*TINTA)
    pdf.cell(0, 10, titulo, new_y="NEXT")

    if subtitulo:
        pdf.set_font("Helvetica", size=8.5)
        pdf.set_text_color(*TENUE)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(pdf.epw, 4.2, subtitulo, new_y="NEXT")
    pdf.ln(2)

    # --- ponderación aplicada ---
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*TINTA)
    pdf.cell(0, 5, etiquetas["ponderacion"], new_y="NEXT")
    pdf.set_font("Helvetica", size=7.5)
    pdf.set_text_color(*TENUE)
    for nombre_p, pct in pesos:
        pdf.cell(90, 4, f"   {nombre_p}", border=0)
        pdf.cell(0, 4, pct, align="L", new_y="NEXT")
    pdf.ln(3)

    # --- encabezado de tabla ---
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_text_color(*TENUE)
    pdf.cell(12, 5, etiquetas["puesto"])
    pdf.cell(88, 5, etiquetas["pais"])
    pdf.cell(28, 5, etiquetas["puntaje"], align="R")
    pdf.cell(0, 5, etiquetas["comparacion"], align="R", new_y="NEXT")
    pdf.set_draw_color(*LINEA)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(1)

    for puesto, pais, puntaje, orig in filas:
        pdf.set_font("Helvetica", size=8.5)
        pdf.set_text_color(*TENUE)
        pdf.cell(12, 5.2, str(puesto))
        pdf.set_text_color(*TINTA)
        pdf.cell(88, 5.2, pais)
        pdf.cell(28, 5.2, f"{puntaje:.1f}", align="R")
        if orig is None or orig == puesto:
            pdf.set_text_color(*TENUE)
            pdf.cell(0, 5.2, "-", align="R", new_y="NEXT")
        else:
            dif = int(orig - puesto)
            pdf.set_text_color(*(SENAL if dif > 0 else (168, 65, 47)))
            flecha = "+" if dif > 0 else "-"
            pdf.cell(0, 5.2, f"{orig:.0f}  {flecha}{abs(dif)}", align="R",
                     new_y="NEXT")

    # --- procedencia ---
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*TINTA)
    pdf.cell(0, 5, etiquetas["procedencia"], new_y="NEXT")
    pdf.set_font("Helvetica", size=7.5)
    pdf.set_text_color(*TENUE)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(pdf.epw, 4, meta["procedencia"])

    return bytes(pdf.output())
