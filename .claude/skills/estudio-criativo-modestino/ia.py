"""Edição e geração com IA para a Modestino, direto na API da fal.ai (paga por uso, sem assinatura, sem conector).

python3 .claude/skills/estudio-criativo-modestino/ia.py imagem <efeito> <foto> [<foto-ref> ...] [--pro] [--formato 4:5] [--extra "..."] [--saida pasta]
python3 .claude/skills/estudio-criativo-modestino/ia.py video  <efeito> <foto> [--segundos 5|10] [--extra "..."] [--saida pasta]
python3 .claude/skills/estudio-criativo-modestino/ia.py livre imagem|video <foto> "prompt completo"

Efeitos de imagem (Nano Banana edit; --pro usa o Nano Banana Pro, mais fiel em detalhe e texto):
  manequim  peça vestida num corpo invisível (ghost mannequin), frente, fundo da marca
  passar    tira amassado e vinco, mantém tudo o mais
  estudio   peça flutuando sobre linho, luz de estúdio e sombra macia (vitrine da loja)
  cena      peça dobrada sobre linho natural com luz de janela (feed, editorial)
  esticada  peça estendida e lisa, vista de cima, sem cabide (flat lay)
  cor       mesma peça em outra cor (--extra "off white #F2EEE6"): só para prévia; a foto final é da peça real
Efeitos de vídeo (Kling 2.6 Pro image-to-video, sem áudio):
  giro360   peça em manequim invisível girando 360° no lugar, em loop
  flutuar   peça flutuando e ondulando devagar, como ao vento
  esticar   macro do tecido esticando e voltando (elasticidade)
  vestir    corpo invisível veste a peça e ajeita a gola
  cair      peça cai do alto e assenta dobrada sobre o linho

Chave: crie em fal.ai (Dashboard → API Keys) e guarde em FAL_KEY (segredo do ambiente). Custo aproximado
(confira em fal.ai/pricing): imagem US$ 0,04 (Pro US$ 0,15); vídeo de 5 s ~US$ 0,35.
Saída: <nome>-<efeito>.png|mp4 e <nome>-<efeito>.json (prompt, modelo, data) na pasta de saída.
Conferir sempre a etiqueta, a gola e a cor contra a peça real: a IA pode redesenhar letras pequenas.
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
M_VIDEO = 'fal-ai/kling-video/v2.6/pro/image-to-video'

PECA = ('the exact same t-shirt from the photo: keep its exact color, fabric texture, crew-neck collar, '
        'stitching and the printed inner neck label exactly as they are (same letters, same size tag)')
FUNDO = 'seamless warm linen beige background (#ECE7DE)'
IMAGEM = {
    'manequim': f'Ghost mannequin product photo of {PECA}, worn by an invisible body, front view, natural 3D volume, '
                f'no person, no hanger, no mannequin visible, {FUNDO}, soft studio light, soft contact shadow, ultra-realistic, high-end e-commerce.',
    'passar': f'Remove all wrinkles and creases from {PECA}. Change nothing else: same framing, same background, same light.',
    'estudio': f'Professional studio photo of {PECA}, perfectly smooth and floating slightly above the floor, no hanger, '
               f'{FUNDO}, soft diffused key light from the left, gentle shadow below, ultra-realistic premium fashion catalog.',
    'cena': f'Editorial photo of {PECA}, neatly folded on natural linen fabric, morning window light from the side, '
            f'soft shadows, calm minimal mood, ultra-realistic, shot on a full-frame camera.',
    'esticada': f'Top-down flat lay of {PECA}, laid perfectly flat and symmetrical, sleeves extended, no wrinkles, no hanger, '
                f'{FUNDO}, even soft light, ultra-realistic e-commerce.',
    'cor': f'Same photo, same t-shirt and everything identical, only change the fabric color to the color given below. '
           f'Keep texture, light, shadows, collar and label.',
}
VIDEO = {
    'giro360': f'{PECA} on an invisible mannequin slowly rotates 360 degrees in place, smooth turntable motion, '
               f'{FUNDO}, soft studio light, static camera, seamless loop, ultra-realistic.',
    'flutuar': f'{PECA} floats in mid-air and gently ripples as if in a soft breeze, slow elegant motion, {FUNDO}, static camera, ultra-realistic.',
    'esticar': f'Macro close-up: hands-free, the fabric of {PECA} stretches softly and returns to shape, showing elasticity and soft texture, '
               f'shallow depth of field, slow motion, ultra-realistic.',
    'vestir': f'An invisible body puts on {PECA} and adjusts the collar, the shirt takes the shape of a torso, no visible person, '
              f'{FUNDO}, static camera, ultra-realistic.',
    'cair': f'{PECA} falls slowly from above and settles neatly folded on natural linen fabric, soft window light, slow motion, ultra-realistic.',
}
NEGATIVO = 'blur, distortion, extra sleeves, extra collar, changed logo, misspelled label, person, face, hands, text overlay, low quality'


def chave():
    k = os.environ.get('FAL_KEY')
    if not k:
        sys.exit('Falta FAL_KEY (fal.ai → Dashboard → API Keys). Guarde como segredo do ambiente, nunca no repositório.')
    return k


def data_uri(foto, lado=2048):
    im = ImageOps.exif_transpose(Image.open(foto))
    if im.mode == 'RGBA':
        fundo = Image.new('RGB', im.size, (236, 231, 222))
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
    ap.add_argument('tipo', choices=['imagem', 'video', 'livre'])
    ap.add_argument('efeito')
    ap.add_argument('fotos', nargs='+')
    ap.add_argument('--pro', action='store_true')
    ap.add_argument('--formato', default='4:5')
    ap.add_argument('--segundos', default='5', choices=['5', '10'])
    ap.add_argument('--extra', default='')
    ap.add_argument('--saida', default='loja/estudio/vitrine/ia')
    a = ap.parse_args()
    if a.tipo == 'livre':                       # livre imagem|video <foto> "prompt"
        tipo, fotos, prompt, efeito = a.efeito, a.fotos[:-1], a.fotos[-1], 'livre'
    else:
        tabela = IMAGEM if a.tipo == 'imagem' else VIDEO
        if a.efeito not in tabela:
            sys.exit(f'efeitos de {a.tipo}: {", ".join(tabela)}')
        tipo, fotos, prompt, efeito = a.tipo, a.fotos, tabela[a.efeito], a.efeito
    if a.extra:
        prompt += ' ' + a.extra
    saida = pathlib.Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    base = saida / f'{pathlib.Path(fotos[0]).stem}-{efeito}'
    if tipo == 'imagem':
        modelo = M_IMAGEM_PRO if a.pro else M_IMAGEM
        r = rodar(modelo, {'prompt': prompt, 'image_urls': [data_uri(f) for f in fotos], 'num_images': 1,
                           'aspect_ratio': a.formato, 'output_format': 'png'})
        arq = base.with_suffix('.png')
        baixar(r['images'][0]['url'], arq)
    else:
        modelo = M_VIDEO
        r = rodar(modelo, {'prompt': prompt, 'start_image_url': data_uri(fotos[0], 1600), 'duration': a.segundos,
                           'negative_prompt': NEGATIVO, 'generate_audio': False})
        arq = base.with_suffix('.mp4')
        baixar(r['video']['url'], arq)
    base.with_suffix('.json').write_text(json.dumps({
        'modelo': modelo, 'efeito': efeito, 'fotos': [str(f) for f in fotos], 'prompt': prompt,
        'data': datetime.datetime.now().isoformat(timespec='seconds')}, ensure_ascii=False, indent=2))
    print(arq)


if __name__ == '__main__':
    main()
