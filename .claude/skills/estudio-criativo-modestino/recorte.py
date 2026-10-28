"""Tira o fundo da peça com IA local (BiRefNet, código aberto, sem custo) e monta a foto de estúdio.

python3 .claude/skills/estudio-criativo-modestino/recorte.py <foto> [<foto2> ...] [--fundo linho|areia|carvao|mapple] [--saida loja/estudio/vitrine]

Para cada foto:
  <nome>-recorte.png    peça sem fundo, na resolução original (para efeitos.py, arte.js, Canva, ia.py)
  <nome>-produto.jpg    2048×2560 (4:5) peça flutuando sobre o fundo, com sombra suave (loja)
  <nome>-feed.jpg       1080×1350 (4:5) mesma composição para o feed
  <nome>-catalogo.jpg   1080×1080 (1:1) catálogo Meta/WhatsApp
  <nome>-story.jpg      1080×1920 (9:16)
Instalação (uma vez por máquina): pip install "rembg[cpu]"  — o modelo (~1 GB) baixa sozinho no primeiro uso.
Para manequim invisível, passar a peça, trocar cenário ou gerar vídeo: ia.py.
"""
import argparse
import json
import pathlib
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter, ImageOps

RAIZ = pathlib.Path(__file__).resolve().parents[3]
C = json.loads((RAIZ / 'loja/design/tokens.json').read_text())['color']
FUNDOS = {'linho': C['bg'], 'areia': C['surface'], 'carvao': C['surface-dark'], 'mapple': C['accent']}
SAIDAS = {'produto': (2048, 2560), 'feed': (1080, 1350), 'catalogo': (1080, 1080), 'story': (1080, 1920)}


def rgb(hexa):
    hexa = hexa.lstrip('#')
    return tuple(int(hexa[i:i + 2], 16) for i in (0, 2, 4))


def recortar(foto, sessao):
    from rembg import remove
    im = ImageOps.exif_transpose(Image.open(foto)).convert('RGB')
    out = remove(im, session=sessao, post_process_mask=True)
    a = np.array(out)
    # fica só a peça: o maior pedaço da máscara (sobras do fundo nas bordas saem)
    alfa = a[..., 3] > 128
    try:
        import cv2
        n, lbl, st, _ = cv2.connectedComponentsWithStats(alfa.astype(np.uint8))
        if n > 2:
            maior = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
            a[..., 3][lbl != maior] = 0
    except ImportError:
        pass
    # sobra clara do fundo grudada na barra ou na manga (fora da faixa da gola, onde fica a etiqueta) sai
    dentro = a[..., 3] > 128
    ys = np.where(dentro.any(1))[0]
    lum = a[..., :3].mean(2)
    claro = (lum > np.median(lum[dentro]) + 60) & dentro
    claro[:ys[0] + int((ys[-1] - ys[0]) * 0.15)] = False
    a[..., 3][claro] = 0
    # borda 1 px para dentro: sem halo claro da manta quando o fundo novo é escuro
    alfa = Image.fromarray(a[..., 3]).filter(ImageFilter.MinFilter(3))
    a[..., 3] = np.array(alfa)
    return Image.fromarray(a)


def compor(peca, w, h, fundo, ocupa=0.8, dy=0):
    """Peça centrada, levemente acima do meio, com sombra de chão suave (efeito flutuando)."""
    peca = peca.crop(peca.getbbox())
    esc = min(w * ocupa / peca.width, h * ocupa / peca.height)
    pw, ph = round(peca.width * esc), round(peca.height * esc)
    p = peca.resize((pw, ph), Image.LANCZOS)
    x, y = (w - pw) // 2, round((h - ph) * 0.42) + dy
    cor = rgb(fundo)
    tela = Image.new('RGBA', (w, h), cor + (255,))
    escuro = sum(cor) < 300
    if not escuro:
        sombra = Image.new('L', (w, h), 0)
        base = p.split()[3].resize((round(pw * 0.86), max(1, round(ph * 0.08))))
        sombra.paste(255, (x + round(pw * 0.07), y + ph + round(h * 0.035) - dy // 2), base)
        sombra = sombra.filter(ImageFilter.GaussianBlur(w * 0.025)).point(lambda v: int(v * 0.3))
        tela = Image.composite(Image.new('RGBA', (w, h), rgb(C['surface-dark']) + (255,)), tela, sombra)
    tela.alpha_composite(p, (x, y))
    return tela.convert('RGB')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('fotos', nargs='+')
    ap.add_argument('--fundo', default='linho', choices=FUNDOS)
    ap.add_argument('--saida', default='loja/estudio/vitrine')
    a = ap.parse_args()
    if len(a.fotos) > 1:
        # uma foto por processo: o modelo acumula memória entre imagens e estoura a máquina
        for f in a.fotos:
            subprocess.run([sys.executable, __file__, f, '--fundo', a.fundo, '--saida', a.saida], check=True)
        return
    from rembg import new_session
    sessao = new_session('birefnet-general')
    saida = pathlib.Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    for f in map(pathlib.Path, a.fotos):
        peca = recortar(f, sessao)
        peca.save(saida / f'{f.stem}-recorte.png')
        for nome, (w, h) in SAIDAS.items():
            compor(peca, w, h, FUNDOS[a.fundo]).save(saida / f'{f.stem}-{nome}.jpg', quality=93)
        print(saida / f'{f.stem}-recorte.png')


if __name__ == '__main__':
    main()
