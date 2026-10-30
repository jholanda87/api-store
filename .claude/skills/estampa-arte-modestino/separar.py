#!/usr/bin/env python3
"""Separa uma estampa em fotolitos (um SVG por tinta) para a gráfica de silk.

Uso:
  python3 separar.py arte.svg pasta-saida [--vazado "#1E1D1C"] [--base-branca] [--margem-mm 12]

Cada fotolito: a tinta em preto chapado, o resto em branco (as formas de outra tinta
que ficam por cima vazam a de baixo), fundo branco, marcas de registro dos lados e
o nome da tinta. --base-branca gera mais um com tudo que leva tinta (camiseta escura).
Escreve também separacoes.md com a lista para mandar junto.
"""

import argparse
import copy
import os
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estampa  # noqa: E402

ET.register_namespace("", estampa.SVG_NS)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
Q = "{%s}" % estampa.SVG_NS


def pintar(el, prop, valor):
    el.set(prop, valor)
    resto = [p for p in (el.get("style") or "").split(";")
             if p.strip() and p.split(":")[0].strip() not in ("fill", "stroke")]
    if resto:
        el.set("style", ";".join(resto))
    elif "style" in el.attrib:
        del el.attrib["style"]


def fotolito(root, alvo, rotulo, margem_mm, vazado=None):
    """alvo: cor (#RRGGBB) ou '*' para todas as tintas (base branca). vazado: o tecido."""
    novo = copy.deepcopy(root)
    largura, altura, escala = estampa.tamanho_mm(root)
    for f in estampa.pinturas(novo):
        el = f["el"]
        for prop, c in (("fill", f["fill"]), ("stroke", f["stroke"])):
            if c is None:
                if prop == "fill" and f["tag"] != "line":
                    pintar(el, "fill", "none")
                continue
            imprime = c != vazado and (alvo == "*" or c == alvo)
            pintar(el, prop, "#000000" if imprime else "#FFFFFF")

    vb = [estampa.numero(x) for x in novo.get("viewBox").replace(",", " ").split()]
    m = margem_mm / escala
    nvb = [vb[0] - m, vb[1] - m, vb[2] + 2 * m, vb[3] + 2 * m]
    novo.set("viewBox", " ".join("%.4g" % v for v in nvb))
    novo.set("width", "%.2fmm" % (largura + 2 * margem_mm))
    novo.set("height", "%.2fmm" % (altura + 2 * margem_mm))

    fundo = ET.Element(Q + "rect", {"x": "%.4g" % nvb[0], "y": "%.4g" % nvb[1],
                                    "width": "%.4g" % nvb[2], "height": "%.4g" % nvb[3],
                                    "fill": "#FFFFFF"})
    novo.insert(0, fundo)
    r, t = 2.5 / escala, 0.25 / escala
    cy = vb[1] + vb[3] / 2
    for cx in (vb[0] - m / 2, vb[0] + vb[2] + m / 2):
        g = ET.SubElement(novo, Q + "g", {"fill": "none", "stroke": "#000000",
                                          "stroke-width": "%.4g" % t})
        ET.SubElement(g, Q + "circle", {"cx": "%.4g" % cx, "cy": "%.4g" % cy, "r": "%.4g" % r})
        ET.SubElement(g, Q + "path", {"d": "M%.4g %.4gH%.4gM%.4g %.4gV%.4g" % (
            cx - 1.6 * r, cy, cx + 1.6 * r, cx, cy - 1.6 * r, cy + 1.6 * r)})
    txt = ET.SubElement(novo, Q + "text", {
        "x": "%.4g" % (vb[0]), "y": "%.4g" % (vb[1] - m / 2),
        "font-family": "monospace", "font-size": "%.4g" % (2.6 / escala), "fill": "#000000"})
    txt.text = rotulo
    return novo


def separar(svg_texto, saida, vazado=None, base_branca=False, margem_mm=12, nome="arte"):
    root = ET.fromstring(svg_texto)
    if estampa.tamanho_mm(root) is None:
        raise SystemExit("Sem tamanho real (width/height em mm). Rode estampa.py primeiro.")
    vazado = estampa.cor(vazado) if vazado else None
    formas = estampa.pinturas(root)
    tintas = estampa.tintas(formas, vazado)
    os.makedirs(saida, exist_ok=True)
    arquivos = []
    for i, c in enumerate(tintas, 1):
        rotulo = "%s  TINTA %d/%d  %s %s" % (nome, i, len(tintas), c, estampa.PALETA.get(c, ""))
        arq = os.path.join(saida, "%s-tinta-%d-%s.svg" % (nome, i, c[1:].lower()))
        ET.ElementTree(fotolito(root, c, rotulo, margem_mm, vazado)).write(arq, encoding="utf-8",
                                                                   xml_declaration=True)
        arquivos.append((arq, c))
    if base_branca:
        arq = os.path.join(saida, "%s-tinta-0-base-branca.svg" % nome)
        ET.ElementTree(fotolito(root, "*", "%s  BASE BRANCA (por baixo)" % nome,
                                margem_mm, vazado)).write(arq, encoding="utf-8", xml_declaration=True)
        arquivos.insert(0, (arq, "base"))
    larg, alt, _ = estampa.tamanho_mm(root)
    with open(os.path.join(saida, "separacoes.md"), "w", encoding="utf-8") as fh:
        fh.write("# Fotolitos: %s\n\nArte: %.1f × %.1f cm (tamanho real, sem margem).\n\n"
                 % (nome, larg / 10, alt / 10))
        fh.write("| ordem | arquivo | tinta |\n| --- | --- | --- |\n")
        for i, (arq, c) in enumerate(arquivos):
            desc = "base branca" if c == "base" else "%s %s" % (c, estampa.PALETA.get(c, ""))
            fh.write("| %d | %s | %s |\n" % (i, os.path.basename(arq), desc))
        if vazado:
            fh.write("\nVazado (tecido aparece, sem tinta): %s\n" % vazado)
        fh.write("\nMarcas de registro dos lados de cada fotolito. "
                 "Preto = imprime; branco = não imprime.\n")
    return [a for a, _ in arquivos]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("svg")
    ap.add_argument("saida")
    ap.add_argument("--vazado")
    ap.add_argument("--base-branca", action="store_true")
    ap.add_argument("--margem-mm", type=float, default=12)
    a = ap.parse_args(argv)
    nome = os.path.splitext(os.path.basename(a.svg))[0]
    arqs = separar(open(a.svg, encoding="utf-8").read(), a.saida, a.vazado, a.base_branca,
                   a.margem_mm, nome)
    for arq in arqs:
        print(arq)
    print(os.path.join(a.saida, "separacoes.md"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
