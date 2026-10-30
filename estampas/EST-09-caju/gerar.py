"""EST-09 Caju: contorno à mão + sombra em pontilhismo. Gera arte.svg e arte-off-white.svg.

Rode da raiz do repositório: python3 estampas/EST-09-caju/gerar.py
O volume é desenhado aqui (luz de cima à esquerda), vira tons de cinza e o textura.py
transforma esses tons em pontos. O contorno é traçado com o tremor de uma caneta.
"""
import math
import os
import random
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(AQUI, "..", "..", ".claude", "skills", "estampa-arte-modestino")
L, A = 64.0, 92.0  # mm
rnd = random.Random(9)


def curva(pontos, n=180):
    """Catmull-Rom fechada pelos pontos de controle."""
    out = []
    m = len(pontos)
    for i in range(m):
        p0, p1, p2, p3 = (pontos[(i + k - 1) % m] for k in range(4))
        for s in range(n // m):
            t = s / (n // m)
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    return out


# fruto (pedúnculo): largo em cima, junto do cabo, afinando até a castanha, um pouco torto
FRUTO = curva([(32, 6), (42, 7), (51, 13), (55, 24), (53, 36), (48, 48), (43, 58), (38, 65), (30, 66),
               (24, 62), (19, 52), (14, 40), (10, 28), (12, 16), (20, 9)])
# castanha: rim pendurado embaixo do fruto, com a barriga para a direita
CASTANHA = curva([(31, 64), (38, 66), (43, 72), (44, 80), (40, 88), (32, 91), (25, 88), (22, 82),
                  (25, 77), (27, 72), (26, 67)])
CABO = [(32, 6), (33.5, 1.5)]


def tremido(pts, amp=0.22):
    fase = rnd.uniform(0, 6)
    return [(x + amp * math.sin(i * 0.37 + fase) + rnd.uniform(-amp, amp) * 0.4,
             y + amp * math.cos(i * 0.29 + fase) + rnd.uniform(-amp, amp) * 0.4) for i, (x, y) in enumerate(pts)]


def d(pts, fechar=True):
    return "M" + "L".join("%.2f %.2f" % p for p in pts) + ("Z" if fechar else "")


def sombra_svg(fundo="#fff"):
    """Tons de cinza: gradiente de luz em cada forma + sombra no pé do fruto."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{L}mm" height="{A}mm" viewBox="0 0 {L} {A}">
  <defs>
    <radialGradient id="f" cx="0.34" cy="0.28" r="0.85"><stop offset="0" stop-color="#fff"/>
      <stop offset="0.35" stop-color="#b4b4b4"/><stop offset="1" stop-color="#000"/></radialGradient>
    <radialGradient id="c" cx="0.62" cy="0.28" r="0.85"><stop offset="0" stop-color="#d0d0d0"/>
      <stop offset="1" stop-color="#202020"/></radialGradient>
  </defs>
  <rect width="100%" height="100%" fill="{fundo}"/>
  <path fill="url(#f)" d="{d(FRUTO)}"/>
  <path fill="url(#c)" d="{d(CASTANHA)}"/>
</svg>'''


def pontilhar(tmp, fundo, inverter):
    """Pontos onde há sombra (tinta escura) ou onde há luz (tinta clara, --inverter)."""
    s_svg, s_png, pont = (os.path.join(tmp, fundo[1:] + n) for n in ("s.svg", "s.png", "p.svg"))
    open(s_svg, "w").write(sombra_svg(fundo))
    subprocess.run(["node", os.path.join(SK, "exportar.mjs"), s_svg, s_png, "--dpi", "254"], check=True,
                   stdout=subprocess.DEVNULL)
    cmd = [sys.executable, os.path.join(SK, "textura.py"), s_png, pont, "--largura-mm", str(L),
           "--ponto-mm", "0.6", "--gama", "1.0", "--semente", "4"] + (["--inverter"] if inverter else [])
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    return open(pont).read().split('d="', 1)[1].split('"', 1)[0]


def main():
    tmp = tempfile.mkdtemp()
    contorno = d(tremido(FRUTO)) + d(tremido(CASTANHA)) + d(tremido(CABO), False)
    # duas passadas curtas de caneta, como num rascunho que ficou
    marcas = d(tremido([(45, 17), (49, 26), (48, 35)], 0.15), False) + d(tremido([(38, 72), (39, 79)], 0.1), False)
    # tinta clara (preta e mapple): pontos na luz, fundo preto não recebe ponto
    # tinta escura (off-white): pontos na sombra, fundo branco não recebe ponto
    for nome, cor, fundo, inv in (("arte.svg", "#ECE7DE", "#000", True),
                                  ("arte-off-white.svg", "#22201D", "#fff", False)):
        pontos = pontilhar(tmp, fundo, inv)
        open(os.path.join(AQUI, nome), "w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{L}mm" height="{A}mm" viewBox="0 0 {L} {A}">
  <title>EST-09 Caju · contorno à mão + pontilhismo · 1 tinta</title>
  <path fill="none" stroke="{cor}" stroke-width="0.55" stroke-linecap="round" stroke-linejoin="round" d="{contorno}{marcas}"/>
  <path fill="{cor}" d="{pontos}"/>
</svg>
''')
    print("ok")


if __name__ == "__main__":
    main()
