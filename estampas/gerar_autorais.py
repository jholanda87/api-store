"""Gera as estampas autorais EST-04 a EST-08 (vetor, mm) em estampas/EST-NN-nome/."""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO + "/.claude/skills/estampa-arte-modestino")
import curvas  # noqa: E402

FON = os.environ.get("FONTES", "node_modules/@fontsource/")  # npm i @fontsource/instrument-serif @fontsource/geist-mono
SERIF = FON + "instrument-serif/files/instrument-serif-latin-400-normal.woff"
SERIF_I = FON + "instrument-serif/files/instrument-serif-latin-400-italic.woff"
MONO = FON + "geist-mono/files/geist-mono-latin-500-normal.woff"

CLARO = "#ECE7DE"   # linho, para preta e mapple
ESCURO = "#22201D"  # carvão, para off-white
TINTA = "#000001"   # marcador trocado pela tinta de cada versão


def texto(fonte, s, altura, espaco=0.0):
    """(largura, altura, viewBox, path) de uma palavra em curvas."""
    svg = curvas.curvas(fonte, s, altura, espaco, TINTA)
    w, h = [float(x) for x in re.findall(r'(?:width|height)="([\d.]+)mm"', svg)]
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
    corpo = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1).strip()
    return w, h, vb, corpo


def coloca(t, x, y):
    w, h, vb, corpo = t
    return '<svg x="%.2f" y="%.2f" width="%.2f" height="%.2f" viewBox="%s">%s</svg>' % (
        x, y, w, h, vb, corpo)


def salva(pasta, titulo, w, h, corpo):
    os.makedirs(REPO + "/estampas/" + pasta, exist_ok=True)
    base = ('<svg xmlns="http://www.w3.org/2000/svg" width="%.2fmm" height="%.2fmm" '
            'viewBox="0 0 %.2f %.2f">\n  <title>%s</title>\n  %s\n</svg>\n' % (w, h, w, h, titulo, corpo))
    for nome, cor in (("arte.svg", CLARO), ("arte-off-white.svg", ESCURO)):
        with open("%s/estampas/%s/%s" % (REPO, pasta, nome), "w", encoding="utf-8") as fh:
            fh.write(base.replace(TINTA, cor))


# EST-04 Horizonte: o pôr do sol no mar reto de Fortaleza. Peito, 9 cm.
salva("EST-04-horizonte", "EST-04 Horizonte · peito · 1 tinta", 90, 54, f'''
  <path fill="{TINTA}" d="M23 30 A22 22 0 0 1 67 30 Z"/>
  <g fill="none" stroke="{TINTA}" stroke-width="2">
    <path d="M0 35 H90"/><path d="M26 41 H64"/><path d="M34 47 H56"/><path d="M41 53 H49"/>
  </g>''')

# EST-05 Aracati: o vento que chega do mar à noite em Fortaleza. Peito, 9 cm.
nome = texto(MONO, "ARACATI", 2.8, 0.45)
traco = f'fill="none" stroke="{TINTA}" stroke-width="1.6" stroke-linecap="round"'
corpo = f'''
  <g {traco}>
    <path d="M2 12 H62 A5 5 0 1 0 57 7"/>
    <path d="M16 25 H84 A5 5 0 1 0 79 20"/>
    <path d="M2 38 H46 A5 5 0 1 0 41 33"/>
  </g>
  {coloca(nome, 2, 47)}'''
salva("EST-05-aracati", "EST-05 Aracati · peito · 1 tinta", 90, 47 + nome[1] + 0.5, corpo)

# EST-06 Jangada: vela, mastro e casco, sobre a linha do mar. Peito, 8 cm.
salva("EST-06-jangada", "EST-06 Jangada · peito · 1 tinta", 80, 60, f'''
  <path fill="{TINTA}" d="M41 3 C50 16 55 30 57 45 L41 45 Z"/>
  <path fill="none" stroke="{TINTA}" stroke-width="1.6" stroke-linecap="round" d="M39 2 L38 49 M30 45 H58"/>
  <path fill="{TINTA}" d="M14 49 H68 L65 53 H17 Z"/>
  <g fill="none" stroke="{TINTA}" stroke-width="1.4" stroke-linecap="round">
    <path d="M2 58 H26"/><path d="M34 58 H78"/>
  </g>''')

# EST-07 Postura: frase da marca nas costas + cartola pequena no peito.
l1 = texto(SERIF, "Cartola é opcional.", 27)
l2 = texto(SERIF_I, "Postura, não.", 27)
W = max(l1[0], l2[0]) + 2
corpo = coloca(l1, (W - l1[0]) / 2, 1) + "\n  " + coloca(l2, (W - l2[0]) / 2, l1[1] + 14)
salva("EST-07-postura", "EST-07 Postura · costas · 1 tinta · frase da campanha O Cavalheiro",
      W, l1[1] + l2[1] + 15, corpo)

# EST-08 Meio-dia: em Fortaleza (3°43'S) o sol do meio-dia fica quase a pino e a sombra some.
leg = texto(MONO, "12H00  3°43'S", 2.4, 0.3)
corpo = f'''
  <circle cx="25" cy="8" r="7" fill="{TINTA}"/>
  <g fill="none" stroke="{TINTA}" stroke-width="1.2" stroke-linecap="round">
    <path d="M25 19 V22 M25 25 V28 M25 31 V34"/>
  </g>
  <rect x="23" y="37" width="4" height="22" fill="{TINTA}"/>
  <path fill="none" stroke="{TINTA}" stroke-width="1.6" stroke-linecap="round" d="M5 60 H45"/>
  {coloca(leg, (50 - leg[0]) / 2, 66)}'''
salva("EST-08-meio-dia", "EST-08 Meio-dia · peito · 1 tinta", 50, 66 + leg[1] + 0.5, corpo)
print("ok")
