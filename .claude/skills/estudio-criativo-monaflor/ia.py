"""Imagens de IA das joias da Mona Flor, direto na API da fal.ai (paga por uso, sem assinatura, sem conector).

python3 .claude/skills/estudio-criativo-monaflor/ia.py imagem <efeito> <foto> [<foto-ref> ...] [--pro] [--formato 1:1] [--extra "..."] [--saida pasta]
python3 .claude/skills/estudio-criativo-monaflor/ia.py livre imagem <foto> "prompt completo"

Efeitos de imagem (Nano Banana edit; para joia use --pro sempre que houver pedra, conta pequena ou pingente com desenho):
  estudio  joia sobre creme, luz macia e sombra delicada (vitrine)
  pescoco  colar no pescoço de uma modelo, recorte da boca à clavícula (sem olhos)
  orelha   brinco na orelha, recorte de orelha e maxilar
  flores   flat lay em linho com flores secas (feed, editorial)
  pedra    sobre pedra natural e cerâmica
  maos     segurada por duas mãos (feito à mão)
  macro    detalhe extremo do acabamento
  caixa    na caixa de presente aberta
Chave: FAL_KEY (segredo do ambiente). Custo aproximado (confira em fal.ai/pricing): imagem US$ 0,04 (Pro US$ 0,15).
Saída: <nome>-<efeito>.png e .json (prompt, modelo, data).
Conferir sempre contra a peça real: número de contas, pingente, cor das pedras, tamanho no corpo. A IA pode
inventar ou tirar contas; se errar, refaça com --pro ou passe mais fotos da mesma peça como referência.
"""
import argparse
import base64
import datetime
import io
import json
import os
import pathlib
import sys
import time
import urllib.request

from PIL import Image, ImageOps

FILA = 'https://queue.fal.run/'
M_IMAGEM, M_IMAGEM_PRO = 'fal-ai/nano-banana/edit', 'fal-ai/nano-banana-pro/edit'

PECA = ('the exact same handmade jewelry piece from the photo: keep every bead, stone, pendant, charm, chain, '
        'clasp, color, finish and proportion exactly as they are; do not add, remove or redesign any element')
FUNDO = 'seamless warm cream background (#F4EEE6)'
IMAGEM = {
    'estudio': f'Luxury product photo of {PECA}, laid elegantly, {FUNDO}, soft diffused light, delicate natural shadow, '
               f'crisp macro detail, ultra-realistic high-end jewelry e-commerce.',
    'pescoco': f'{PECA} worn on a woman, cropped from lips down to the collarbone (no eyes), natural skin texture, '
               f'neutral linen top, soft window light, editorial, ultra-realistic. The necklace sits naturally on the neck.',
    'orelha': f'{PECA} worn on a woman\'s ear, close crop of ear and jawline, hair tucked back, soft natural light, '
              f'ultra-realistic editorial beauty shot. Show the earring at true scale.',
    'flores': f'Editorial flat lay of {PECA} on natural linen with a few dried flowers and petals around it, '
              f'morning window light, soft shadows, romantic artisanal mood, ultra-realistic.',
    'pedra': f'{PECA} displayed on a smooth natural stone and ceramic dish, warm side light, soft shadows, '
             f'minimal premium mood, ultra-realistic.',
    'maos': f'Two hands with natural nails gently holding {PECA}, cream linen background, soft light, '
            f'artisanal and delicate, ultra-realistic.',
    'macro': f'Extreme macro close-up of {PECA}, showing texture and handmade detail, shallow depth of field, '
             f'soft light, ultra-realistic.',
    'caixa': f'{PECA} presented in an open kraft gift box with tissue paper, {FUNDO}, soft light, ready to gift, ultra-realistic.',
}


def chave():
    k = os.environ.get('FAL_KEY')
    if not k:
        sys.exit('Falta FAL_KEY (fal.ai → Dashboard → API Keys). Guarde como segredo do ambiente, nunca no repositório.')
    return k


def data_uri(foto, lado=2048):
    im = ImageOps.exif_transpose(Image.open(foto))
    if im.mode == 'RGBA':
        fundo = Image.new('RGB', im.size, (244, 238, 230))
        fundo.paste(im, mask=im.split()[3])
        im = fundo
    im = im.convert('RGB')
    im.thumbnail((lado, lado), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=92)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def pedir(url, k, corpo=None):
    req = urllib.request.Request(url, data=json.dumps(corpo).encode() if corpo is not None else None,
                                 headers={'Authorization': f'Key {k}', 'Content-Type': 'application/json'},
                                 method='POST' if corpo is not None else 'GET')
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def rodar(modelo, entrada):
    k = chave()
    fila = pedir(FILA + modelo, k, entrada)
    inicio = time.time()
    while True:
        st = pedir(fila['status_url'], k)
        if st.get('status') == 'COMPLETED':
            return pedir(fila['response_url'], k)
        if time.time() - inicio > 900:
            sys.exit(f'tempo esgotado; pedido {fila.get("request_id")} continua na fila da fal.ai')
        time.sleep(4)


def baixar(url, destino):
    with urllib.request.urlopen(url, timeout=300) as r:
        destino.write_bytes(r.read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tipo', choices=['imagem', 'livre'])
    ap.add_argument('efeito')
    ap.add_argument('fotos', nargs='+')
    ap.add_argument('--pro', action='store_true')
    ap.add_argument('--formato', default='1:1')
    ap.add_argument('--extra', default='')
    ap.add_argument('--saida', default='imagens')
    a = ap.parse_args()
    if a.tipo == 'livre':                       # livre imagem <foto> "prompt"
        fotos, prompt, efeito = a.fotos[:-1], a.fotos[-1], 'livre'
    else:
        if a.efeito not in IMAGEM:
            sys.exit(f'efeitos: {", ".join(IMAGEM)}')
        fotos, prompt, efeito = a.fotos, IMAGEM[a.efeito], a.efeito
    if a.extra:
        prompt += ' ' + a.extra
    saida = pathlib.Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    base = saida / f'{pathlib.Path(fotos[0]).stem}-{efeito}'
    modelo = M_IMAGEM_PRO if a.pro else M_IMAGEM
    r = rodar(modelo, {'prompt': prompt, 'image_urls': [data_uri(f) for f in fotos], 'num_images': 1,
                       'aspect_ratio': a.formato, 'output_format': 'png'})
    arq = base.with_suffix('.png')
    baixar(r['images'][0]['url'], arq)
    base.with_suffix('.json').write_text(json.dumps({
        'modelo': modelo, 'efeito': efeito, 'fotos': [str(f) for f in fotos], 'prompt': prompt,
        'data': datetime.datetime.now().isoformat(timespec='seconds')}, ensure_ascii=False, indent=2))
    print(arq)


if __name__ == '__main__':
    main()
