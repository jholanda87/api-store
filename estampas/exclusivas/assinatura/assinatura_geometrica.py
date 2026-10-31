"""Assinatura MODESTINO geométrica: 9 laçadas idênticas (uma por letra) numa linha contínua,
construída por cicloide alongada (curva simétrica), inclinada como o rascunho do Jorge.
Rode da raiz: python3 estampas/exclusivas/assinatura/assinatura_geometrica.py"""
import os
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__))
LARGURA_MM, TRACO_MM, LACOS, INCL = 250.0, 4.5, 9, 0.35
from assinatura_suave import PALETAS  # noqa: E402

def main():
    t = np.linspace(0, LACOS * 2 * np.pi, LACOS * 160)
    r, d, alt = 1.0, 2.6, 9.5                         # passo, largura do laço, altura do laço
    x = r * t - d * np.sin(t)
    y = -alt * d * np.cos(t)
    x = x + INCL * (y.max() - y)                       # inclinação do traço
    pts = np.c_[x, y]
    x0, y0 = pts.min(0); x1, y1 = pts.max(0)
    esc = LARGURA_MM / (x1 - x0); pad = TRACO_MM / esc
    dd = 'M%.3f %.3f' % tuple(pts[0]) + ''.join('L%.3f %.3f' % tuple(p) for p in pts[1:])
    u = x - INCL * (y0 - y)
    q1, q2 = x0 + (x1 - x0) / 3, x0 + 2 * (x1 - x0) / 3
    def faixa(a, b):
        A, B = y0 - 50, y1 + 50
        return 'M%.2f %.2fL%.2f %.2fL%.2f %.2fL%.2f %.2fZ' % (a + INCL*(B-A)/2, A, b + INCL*(B-A)/2, A, b - INCL*(B-A)/2, B, a - INCL*(B-A)/2, B)
    lims = [(x0 - 99, q1), (q1, q2), (q2, x1 + 99)]
    for tec, cores in PALETAS.items():
        defs = ''.join('<clipPath id="f%d"><path d="%s"/></clipPath>' % (i, faixa(*l)) for i, l in enumerate(lims))
        g = ''.join('<g id="tinta-%s" clip-path="url(#f%d)"><title>%s</title><path d="%s" fill="none" stroke="%s" stroke-width="%.3f" stroke-linecap="round" stroke-linejoin="round"/></g>\n'
                    % (n, i, p, dd, c, TRACO_MM / esc, ) for i, (n, c, p) in enumerate(cores))
        H = (y1 - y0 + 2 * pad) * esc
        open(os.path.join(AQUI, 'assinatura-%s.svg' % tec), 'w').write(
            '<svg xmlns="http://www.w3.org/2000/svg" width="%.1fmm" height="%.1fmm" viewBox="%.3f %.3f %.3f %.3f">\n<defs>%s</defs>\n%s</svg>\n'
            % (LARGURA_MM + 2 * TRACO_MM, H, x0 - pad, y0 - pad, x1 - x0 + 2 * pad, y1 - y0 + 2 * pad, defs, g))
    print('ok', round(H / 10, 1), 'cm de altura')

if __name__ == '__main__':
    main()
