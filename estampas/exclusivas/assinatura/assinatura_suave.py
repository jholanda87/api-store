"""Assinatura MODESTINO, versão suave: linha central do traço do Jorge vira curvas Bézier alisadas,
com contorno vetorial uniforme (pontas e cantos redondos) e 3 faixas diagonais de cor.
Rode da raiz: python3 estampas/exclusivas/assinatura/assinatura_suave.py
"""
import os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from skimage.morphology import skeletonize

AQUI = os.path.dirname(os.path.abspath(__file__))
LARGURA_MM, TRACO_MM = 250.0, 4.5
PALETAS = {
    'preta': [('linho', '#ECE7DE', 'Pantone 9224 C'), ('ocre', '#C9A25E', 'Pantone 7562 C'), ('salvia', '#8E9B7A', 'Pantone 5625 C')],
    'mapple': [('linho', '#ECE7DE', 'Pantone 9224 C'), ('areia-dourada', '#D8B878', 'Pantone 7508 C'), ('azul-mar', '#9FB4B3', 'Pantone 5503 C')],
    'offwhite': [('carvao', '#22201D', 'Pantone Black 7 C'), ('mapple', '#5B3F30', 'Pantone 7533 C'), ('oliva', '#6B7350', 'Pantone 5753 C')],
}
VIZ = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def esqueleto():
    g = np.asarray(Image.open(os.path.join(AQUI, 'rascunho-jorge.jpg')).convert('L'), float)[540:1680, 200:1180]
    linha = (g / np.maximum(ndi.gaussian_filter(g, 40), 1)) < 0.82
    linha = ndi.binary_opening(linha, iterations=1)
    lab, n = ndi.label(linha)
    tam = ndi.sum(linha, lab, range(1, n + 1))
    linha = np.isin(lab, [i + 1 for i, t in enumerate(tam) if t > 300])
    linha = np.array(Image.fromarray(linha.astype('uint8') * 255).resize((linha.shape[1] * 2, linha.shape[0] * 2), Image.LANCZOS)) > 127
    linha = ndi.binary_closing(linha, iterations=7)     # traços duplos do grafite viram um só
    return skeletonize(linha)


def caminhos(esq):
    """Quebra o esqueleto em linhas (entre pontas e cruzamentos)."""
    pts = set(zip(*np.nonzero(esq)))
    viz = {p: [(p[0] + a, p[1] + b) for a, b in VIZ if (p[0] + a, p[1] + b) in pts] for p in pts}
    nos = {p for p, v in viz.items() if len(v) != 2}
    usados, saida = set(), []
    def andar(a, b):
        c = [a, b]
        while b not in nos:
            prox = [q for q in viz[b] if q != c[-2] and (b, q) not in usados]
            if not prox:
                break
            usados.add((b, prox[0])); usados.add((prox[0], b))
            c.append(prox[0]); b = prox[0]
        return c
    for a in nos:
        for b in viz[a]:
            if (a, b) not in usados:
                usados.add((a, b)); usados.add((b, a)); saida.append(andar(a, b))
    resto = {p for p in pts if p not in nos and not any((p, q) in usados for q in viz[p])}
    while resto:  # laços fechados sem nós
        p = resto.pop(); c = [p]
        while True:
            prox = [q for q in viz[c[-1]] if q in resto]
            if not prox: break
            resto.discard(prox[0]); c.append(prox[0])
        saida.append(c + [c[0]])
    return [c for c in saida if len(c) > 90]          # tira rebarbas curtas


def suavizar(c, sigma=9):
    """Curva longa e lisa: spline com suavização forte (sem ondulação), pontas no lugar."""
    from scipy.interpolate import splprep, splev
    a = np.array(c, float)[:, ::-1]
    if len(a) < 30:
        return a
    a = a[::3]
    try:
        tck, _ = splprep([a[:, 0], a[:, 1]], s=len(a) * 9.0, k=3)
        x, y = splev(np.linspace(0, 1, max(12, len(a) // 2)), tck)
        out = np.c_[x, y]; out[0], out[-1] = a[0], a[-1]
        return out
    except Exception:
        return a


def suavizar_antigo(c, sigma=9):
    a = np.array(c, float)[:, ::-1]                    # (x, y)
    orig = a.copy()
    if len(a) > 3 * sigma:
        a = np.c_[ndi.gaussian_filter1d(a[:, 0], sigma, mode='nearest'), ndi.gaussian_filter1d(a[:, 1], sigma, mode='nearest')]
        # as pontas voltam ao lugar original (encontro das laçadas sem corte), com transição suave
        k = min(len(a) // 2, 3 * sigma)
        peso = np.linspace(1, 0, k)[:, None]
        a[:k] = peso * orig[:k] + (1 - peso) * a[:k]
        a[-k:] = peso[::-1] * orig[-k:] + (1 - peso[::-1]) * a[-k:]
    a = a[::6] if len(a) > 12 else a
    if len(a) and not np.allclose(a[-1], orig[-1]):
        a = np.vstack([a, orig[-1]])
    return a


def bezier(p):
    """Catmull-Rom -> cúbicas: curva lisa passando pelos pontos."""
    d = 'M%.1f %.1f' % tuple(p[0])
    for i in range(len(p) - 1):
        p0, p1, p2 = p[max(i - 1, 0)], p[i], p[i + 1]
        p3 = p[min(i + 2, len(p) - 1)]
        c1, c2 = p1 + (p2 - p0) / 6, p2 - (p3 - p1) / 6
        d += 'C%.1f %.1f %.1f %.1f %.1f %.1f' % (*c1, *c2, *p2)
    return d


def main():
    esq = esqueleto()
    h, w = esq.shape
    linhas = [suavizar(c) for c in caminhos(esq)]
    allp = np.vstack(linhas)
    x0, y0 = allp.min(0) - 20; x1, y1 = allp.max(0) + 20
    escala = LARGURA_MM / (x1 - x0)                   # mm por unidade
    sw = TRACO_MM / escala
    d = ''.join(bezier(l) for l in linhas)
    # faixas diagonais pela inclinação dos traços (0,35 em x por 1 em y), terços do desenho
    u = allp[:, 0] - 0.35 * allp[:, 1]
    q1, q2 = np.quantile(u, [1 / 3, 2 / 3])
    def faixa(a, b):
        yA, yB = y0 - 500, y1 + 500
        return 'M%.1f %.1fL%.1f %.1fL%.1f %.1fL%.1f %.1fZ' % (a + 0.35 * yA, yA, b + 0.35 * yA, yA, b + 0.35 * yB, yB, a + 0.35 * yB, yB)
    lims = [(-1e5, q1), (q1, q2), (q2, 1e5)]
    for tecido, cores in PALETAS.items():
        defs = ''.join('<clipPath id="f%d"><path d="%s"/></clipPath>' % (i, faixa(*l)) for i, l in enumerate(lims))
        g = ''.join('<g id="tinta-%s" clip-path="url(#f%d)"><title>%s</title><path d="%s" fill="none" stroke="%s" '
                    'stroke-width="%.2f" stroke-linecap="round" stroke-linejoin="round"/></g>\n' % (n, i, p, d, c, sw)
                    for i, (n, c, p) in enumerate(cores))
        open(os.path.join(AQUI, 'assinatura-%s.svg' % tecido), 'w').write(
            '<svg xmlns="http://www.w3.org/2000/svg" width="%.1fmm" height="%.1fmm" viewBox="%.1f %.1f %.1f %.1f">\n'
            '<title>Exclusivas · Assinatura MODESTINO · camiseta %s · 3 tintas · traço %.1f mm</title>\n<defs>%s</defs>\n%s</svg>\n'
            % (LARGURA_MM, (y1 - y0) * escala, x0, y0, x1 - x0, y1 - y0, tecido, TRACO_MM, defs, g))
    print('ok', len(linhas), 'curvas ·', LARGURA_MM / 10, 'x', round((y1 - y0) * escala / 10, 1), 'cm')


if __name__ == '__main__':
    main()
