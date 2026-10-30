#!/usr/bin/env python3
"""Mockup plano da estampa nas camisetas da Modestino, em escala real (tamanho M).

Uso:
  python3 mockup.py arte.svg saida.svg [--posicao peito|frente|costas|nuca]
                    [--cores preto,mapple,off-white] [--arte-off-white outra.svg] [--png saida.png]

Desenha a camiseta M (54 cm de axila a axila, 72 cm de comprimento) em cada cor e
põe a arte no lugar, no tamanho do arquivo. Serve para o Jorge aprovar proporção e
cor; não é foto de produto e nunca vai para a vitrine. --arte-off-white troca a
versão da arte na camiseta clara (ex.: tinta carvão em vez de areia). --png chama
exportar.mjs (Node + Playwright) para gerar a imagem.
"""

import argparse
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estampa  # noqa: E402

ET.register_namespace("", estampa.SVG_NS)
Q = "{%s}" % estampa.SVG_NS

MEIA = 27.0          # meia largura do peito (cm), tamanho M
COMPRIMENTO = 72.0
GOLA = {"frente": 9.0, "costas": 2.2}  # profundidade do decote
# Onde fica o topo e o centro da arte, em cm a partir do ombro junto da gola.
LUGAR = {
    "peito": ("frente", GOLA["frente"] + 10.0, 7.0),  # medido na peça real; esquerdo de quem veste
    "frente": ("frente", GOLA["frente"] + 8.0, 0.0),
    "costas": ("costas", GOLA["costas"] + 11.0, 0.0),  # aprovado pelo Jorge em 30/10
    "nuca": ("costas", GOLA["costas"] + 2.5, 0.0),
}


def corpo(lado):
    g = GOLA[lado]
    return ("M-8.5 0 L-23 3.5 L-36 19 L-31 23.5 L-27 21 L-27 {c} Q0 {c2} 27 {c} L27 21 "
            "L31 23.5 L36 19 L23 3.5 L8.5 0 C8 {g1} -8 {g1} -8.5 0 Z").format(
                c=COMPRIMENTO, c2=COMPRIMENTO + 0.6, g1=g * 1.33)


def ribana(lado):
    g = GOLA[lado]
    return "M-8.5 0 C-8 {a} 8 {a} 8.5 0 M-10 -0.4 C-9.5 {b} 9.5 {b} 10 -0.4".format(
        a=g * 1.33, b=g * 1.33 + 2.2)


def mockup(arte_texto, posicao="frente", cores=("preto", "mapple", "off-white"), alternativas=None):
    alternativas = alternativas or {}
    lado, topo, centro = LUGAR[posicao]
    celula = 84.0
    sheet = ET.Element(Q + "svg", {
        "width": "%gmm" % (celula * len(cores) * 10), "height": "920mm",
        "viewBox": "0 0 %g 92" % (celula * len(cores))})
    ET.SubElement(sheet, Q + "rect", {"width": "100%", "height": "100%", "fill": "#F5F2EC"})
    for i, nome in enumerate(cores):
        fundo = estampa.CAMISETAS[nome]
        escura = not estampa.clara(fundo)
        linha = "#00000033" if not escura else "#FFFFFF22"
        g = ET.SubElement(sheet, Q + "g", {"transform": "translate(%g 6)" % (celula * i + celula / 2)})
        ET.SubElement(g, Q + "path", {"d": corpo(lado), "fill": fundo, "stroke": "#22201D",
                                      "stroke-opacity": "0.25", "stroke-width": "0.15"})
        ET.SubElement(g, Q + "path", {"d": ribana(lado), "fill": "none", "stroke": linha,
                                      "stroke-width": "0.25"})
        art = ET.fromstring(alternativas.get(nome, arte_texto))
        medida = estampa.tamanho_mm(art)
        if medida is None:
            raise SystemExit("A arte precisa de width/height em mm (rode estampa.py).")
        w, h = medida[0] / 10, medida[1] / 10
        art.set("x", "%g" % (centro - w / 2))
        art.set("y", "%g" % topo)
        art.set("width", "%g" % w)
        art.set("height", "%g" % h)
        g.append(art)
        rot = ET.SubElement(g, Q + "text", {
            "x": "0", "y": "%g" % (COMPRIMENTO + 6.5), "text-anchor": "middle",
            "font-family": "'Geist Mono', ui-monospace, monospace", "font-size": "2.2",
            "fill": "#5F5850", "letter-spacing": "0.3"})
        rot.text = "%s · %s · %.1f × %.1f cm" % (nome.upper(), posicao, w, h)
    return ET.tostring(sheet, encoding="unicode")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("svg")
    ap.add_argument("saida")
    ap.add_argument("--posicao", choices=sorted(LUGAR), default="frente")
    ap.add_argument("--cores", default="preto,mapple,off-white")
    ap.add_argument("--arte-off-white")
    ap.add_argument("--arte-preto")
    ap.add_argument("--arte-mapple")
    ap.add_argument("--png")
    a = ap.parse_args(argv)
    cores = [c.strip() for c in a.cores.split(",") if c.strip()]
    for c in cores:
        if c not in estampa.CAMISETAS:
            raise SystemExit("Cor desconhecida: %s (use %s)" % (c, ", ".join(estampa.CAMISETAS)))
    alt = {}
    for nome, arq in (("off-white", a.arte_off_white), ("preto", a.arte_preto),
                      ("mapple", a.arte_mapple)):
        if arq:
            alt[nome] = open(arq, encoding="utf-8").read()
    texto = mockup(open(a.svg, encoding="utf-8").read(), a.posicao, cores, alt)
    with open(a.saida, "w", encoding="utf-8") as fh:
        fh.write(texto)
    print(a.saida)
    if a.png:
        script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exportar.mjs")
        r = subprocess.run(["node", script, a.saida, a.png, "--dpi", "30"])
        if r.returncode:
            print("PNG não gerado: precisa de Node + Playwright. O SVG abre em qualquer navegador.")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
