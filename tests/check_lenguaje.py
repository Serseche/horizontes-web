#!/usr/bin/env python3
"""Chequeo de lenguaje del frontend (index.html). Solo librería estándar.

Protege que la interfaz DESCRIBA el puntaje y no sugiera acciones de compra o venta:
  (a) están las cuatro bandas de puntaje entre comillas;
  (b) no aparece ninguna etiqueta de acción prohibida;
  (c) el descargo legal está literal;
  (d) existe el elemento con id="descargo-radar".

Los textos de referencia de abajo salen de horizontes-core (radar_template.html, bloque
<div class="disc">, y test_textos_sin_recomendacion.py). Si cambian allá, HAY QUE
ACTUALIZARLOS ACÁ: este script no los lee de ningún otro repo.

Uso: python tests/check_lenguaje.py [ruta/a/index.html]   (por defecto: ../index.html)
Sale con código 1 si falla algún chequeo.
"""
import sys
from pathlib import Path

BANDAS = ("Puntaje alto", "Puntaje medio-alto", "Puntaje medio-bajo", "Puntaje bajo")

ETIQUETAS_PROHIBIDAS = ("Comprar fuerte", "Acumular", "Mantener", "Evitar")

# Texto interno del descargo del Radar (radar_template.html de horizontes-core).
DESCARGO = (
    '<b>Importante.</b> Ranking cuantitativo informativo, calculado con datos públicos y reglas fijas. No es una recomendación personalizada ni una oferta de compra o venta. No considera tu situación, tus objetivos ni tu tolerancia al riesgo. Los datos pueden tener demoras o errores. Rendimientos pasados no garantizan resultados futuros. Las bandas de puntaje describen la salida del modelo y no constituyen una instrucción de compra, venta o mantenimiento.'
)

ID_DESCARGO = 'id="descargo-radar"'


def verificar(html: str) -> list[str]:
    errores = []
    for banda in BANDAS:
        if f'"{banda}"' not in html:
            errores.append(f'[bandas] falta la banda entre comillas: "{banda}"')
    for etiqueta in ETIQUETAS_PROHIBIDAS:
        if etiqueta in html:
            errores.append(f'[prohibidas] aparece la etiqueta de accion prohibida: "{etiqueta}"')
    if DESCARGO not in html:
        errores.append("[descargo] el descargo exacto del Radar NO esta literal en index.html "
                       "(texto de referencia en tests/check_lenguaje.py)")
    if ID_DESCARGO not in html:
        errores.append(f"[descargo] falta el elemento con {ID_DESCARGO}")
    return errores


def main() -> int:
    ruta = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "index.html"
    if not ruta.is_file():
        print(f"ERROR: no existe {ruta}")
        return 1
    errores = verificar(ruta.read_text(encoding="utf-8"))
    if errores:
        print(f"FALLO: {len(errores)} chequeo(s) de lenguaje en {ruta.name}")
        for e in errores:
            print("  -", e)
        return 1
    print(f"OK: {ruta.name} cumple los 4 chequeos de lenguaje (bandas, etiquetas, descargo, id).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
