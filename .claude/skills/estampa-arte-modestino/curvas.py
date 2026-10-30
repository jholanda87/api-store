#!/usr/bin/env python3
"""Converte uma palavra em curvas (SVG de vetor puro, sem fonte) para a estampa.

Uso:
  python3 curvas.py fonte.woff "texto" --altura-mm 8 [--espaco 0.12] [--cor "#CBBFAE"] > palavra.svg

--altura-mm é a altura da maiúscula (H) na camiseta. --espaco é o espaçamento entre
letras em fração do corpo (o nome MODESTINO usa 0.32). Precisa do fontTools
(pip install fonttools brotli; brotli só para .woff2). Fontes da marca:
npm i @fontsource/instrument-serif @fontsource/instrument-sans @fontsource/geist-mono
e use os .woff de node_modules/@fontsource/<fonte>/files/. Todas são OFL: uso comercial livre.
O kerning da fonte não é aplicado: confira o par de letras no olho e ajuste com --espaco.
"""

import argparse
import sys


def curvas(fonte, texto, altura_mm=8.0, espaco=0.0, cor="#22201D"):
    try:
        from fontTools.pens.boundsPen import BoundsPen
        from fontTools.pens.svgPathPen import SVGPathPen
        from fontTools.pens.transformPen import TransformPen
        from fontTools.ttLib import TTFont
    except ImportError:
        raise SystemExit("Falta o fontTools: pip install fonttools brotli")

    font = TTFont(fonte)
    upm = font["head"].unitsPerEm
    cap = getattr(font["OS/2"], "sCapHeight", 0) or 0
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    if not cap:
        b = BoundsPen(gs)
        gs[cmap[ord("H")]].draw(b)
        cap = b.bounds[3]
    s = altura_mm / cap  # mm por unidade da fonte
    pen = SVGPathPen(gs, ntos=lambda v: ("%.3f" % v).rstrip("0").rstrip("."))
    caixa = BoundsPen(gs)
    x = 0.0
    faltando = []
    for ch in texto:
        nome = cmap.get(ord(ch))
        if nome is None:
            faltando.append(ch)
            continue
        t = (s, 0, 0, -s, x, 0)
        gs[nome].draw(TransformPen(pen, t))
        gs[nome].draw(TransformPen(caixa, t))
        x += gs[nome].width * s + espaco * upm * s
    if faltando:
        raise SystemExit("A fonte não tem: %s" % "".join(faltando))
    if caixa.bounds is None:
        raise SystemExit("Texto sem desenho (só espaços?).")
    x0, y0, x1, y1 = caixa.bounds
    w, h = x1 - x0, y1 - y0
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%.2fmm" height="%.2fmm" '
            'viewBox="%.3f %.3f %.3f %.3f">\n  <path fill="%s" d="%s"/>\n</svg>\n'
            % (w, h, x0, y0, w, h, cor, pen.getCommands()))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("fonte")
    ap.add_argument("texto")
    ap.add_argument("--altura-mm", type=float, default=8.0)
    ap.add_argument("--espaco", type=float, default=0.0)
    ap.add_argument("--cor", default="#22201D")
    a = ap.parse_args(argv)
    sys.stdout.write(curvas(a.fonte, a.texto, a.altura_mm, a.espaco, a.cor))
    return 0


if __name__ == "__main__":
    sys.exit(main())
