"""Arte de traço fino para DTF: tudo que fica dentro do contorno recebe a cor do tecido, para o filme
virar uma peça só (não descola). Saída por camiseta: SVG com 2 camadas (preenchimento + traço) e PNG 300 dpi.
Rode: python3 preencher.py"""
import glob, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
sys.path.insert(0, '../../../.claude/skills/estampa-arte-modestino')
import vetorizar  # noqa

TECIDO = {'preta': ('#1E1D1C', '#ECE7DE'), 'mapple': ('#5B3F30', '#ECE7DE'), 'offwhite': ('#ECE7DE', '#22201D')}
ALT, LARG = 350.0, 320.0  # mm, máximo nas costas
for f in sorted(glob.glob('*.jpg')):
    nome = f[:-4]
    g = np.asarray(Image.open(f).convert('L'))
    linha = g < 150
    ys, xs = np.nonzero(linha); linha = linha[ys.min()-10:ys.max()+11, xs.min()-10:xs.max()+11]
    linha = np.array(Image.fromarray(linha.astype('uint8')*255).resize((linha.shape[1]*3, linha.shape[0]*3), Image.LANCZOS)) > 100
    h, w = linha.shape; mmpx = min(ALT/h, LARG/w)
    traco = np.array(vetorizar.garantir(Image.fromarray(np.where(linha, 0, 255).astype('uint8')), mmpx, 0.8)) == 0
    fechado = ndi.binary_dilation(traco, iterations=int(1.2/mmpx))         # fecha vãos pequenos do contorno
    fundo, _ = ndi.label(~fechado); bordas = set(np.unique(np.r_[fundo[0], fundo[-1], fundo[:, 0], fundo[:, -1]]))
    dentro = ~np.isin(fundo, list(bordas)) | fechado
    dentro = ndi.binary_opening(dentro, iterations=2) | traco
    dl, _ = vetorizar.tracar(Image.fromarray(np.where(dentro, 0, 255).astype('uint8')), 128, 20)
    tl, _ = vetorizar.tracar(Image.fromarray(np.where(traco, 0, 255).astype('uint8')), 128, 4)
    for cam, (fundo_c, tinta) in TECIDO.items():
        open(f'{nome}-{cam}.svg', 'w').write(
            '<svg xmlns="http://www.w3.org/2000/svg" width="%.1fmm" height="%.1fmm" viewBox="0 0 %d %d">'
            '<title>%s · camiseta %s · DTF: preenchimento na cor do tecido</title>'
            '<path fill="%s" fill-rule="evenodd" d="%s"/><path fill="%s" fill-rule="evenodd" d="%s"/></svg>'
            % (w*mmpx, h*mmpx, w, h, nome, cam, fundo_c, ''.join(dl), tinta, ''.join(tl)))
        rgba = np.zeros((h, w, 4), np.uint8)
        hx = lambda c: [int(c[i:i+2], 16) for i in (1, 3, 5)]
        rgba[dentro] = hx(fundo_c) + [255]; rgba[traco] = hx(tinta) + [255]
        Image.fromarray(rgba).save(f'{nome}-{cam}.png', dpi=(int(h/(h*mmpx/25.4)),)*2)
    print(nome, round(w*mmpx/10, 1), 'x', round(h*mmpx/10, 1), 'cm')
