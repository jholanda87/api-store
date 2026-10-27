"""Prévia local do tema Modestino (sem Shopify).

python3 loja/tema/tools/previa.py
Renderiza as seções modestino-* com python-liquid (pip install "python-liquid<2") e dados de exemplo
iguais aos da loja (preços, variantes, fotos provisórias de loja/fotos-provisorias) em loja/tema/previa/.
Serve para conferir layout, estados e textos em 390 e 1440 px; a loja de verdade continua sendo a prévia
do tema na Shopify. Filtros da Shopify (money, image_url, asset_url...) são imitados aqui.
"""
import json, pathlib, re, shutil, html

from liquid import Environment, FileSystemLoader

TEMA = pathlib.Path(__file__).resolve().parents[1]
LOJA = TEMA.parent
SAIDA = TEMA / 'previa'


def sem_blocos_shopify(src):
    src = re.sub(r'{%-?\s*schema\s*-?%}.*?{%-?\s*endschema\s*-?%}', '', src, flags=re.S)
    return re.sub(r'{%-?\s*stylesheet\s*-?%}.*?{%-?\s*endstylesheet\s*-?%}', '', src, flags=re.S)


def schema(src):
    m = re.search(r'{%-?\s*schema\s*-?%}(.*?){%-?\s*endschema\s*-?%}', src, flags=re.S)
    return json.loads(m.group(1)) if m else {}


class Loader(FileSystemLoader):
    def get_source(self, env, name, *a, **k):
        if not name.endswith('.liquid'):
            name += '.liquid'
        s = super().get_source(env, name, *a, **k)
        return s._replace(source=sem_blocos_shopify(s.source))


env = Environment(loader=Loader([str(TEMA / 'snippets'), str(TEMA / 'sections')]))


def money(c):
    c = int(c or 0)
    return 'R$ ' + f"{c // 100:,}".replace(',', '.') + f",{c % 100:02d}"


env.add_filter('money', money)
env.add_filter('money_without_trailing_zeros', lambda c: money(c)[:-3] if int(c or 0) % 100 == 0 else money(c))
env.add_filter('asset_url', lambda n: 'assets/' + n)
env.add_filter('stylesheet_tag', lambda u: f'<link rel="stylesheet" href="{u}">')
env.add_filter('json', lambda v: json.dumps(v, ensure_ascii=False))
env.add_filter('image_url', lambda img, **k: (img or {}).get('src', '') if isinstance(img, dict) else str(img))


def image_tag(src, **k):
    attrs = ' '.join(f'{a}="{html.escape(str(v))}"' for a, v in k.items() if a not in ('widths',))
    return f'<img src="{src}" {attrs} width="1080" height="1350">'


env.add_filter('image_tag', image_tag)


# ---------- dados de exemplo (iguais aos da Shopify em 27/10) ----------
FOTOS = {
    'preta-frente': 'Camiseta básica Modestino preta, lisa, vestida de frente',
    'preta-ombro': 'Ombro e gola da camiseta preta Modestino de perto',
    'marrom-frente': 'Camiseta básica Modestino mapple brown, lisa, vestida de frente',
    'marrom-gola': 'Gola careca da camiseta mapple brown Modestino de perto',
    'marrom-lado': 'Camiseta mapple brown Modestino vestida, vista de lado',
    'off-white-frente': 'Camiseta básica Modestino off white, lisa, vestida de frente',
    'off-white-costas': 'Costas e manga da camiseta off white Modestino',
    'off-white-gola': 'Gola da camiseta off white Modestino de perto',
}
media = [{'alt': alt, 'preview_image': {'src': f'fotos/{n}.jpg'}} for n, alt in FOTOS.items()]
textos = {a['sku']: a for a in json.loads((LOJA / 'catalogo/textos.json').read_text())['anuncios']}


def desc(sku):
    return ''.join(f'<p>{html.escape(p).replace(chr(10), "<br>")}</p>' for p in textos[sku]['descricao'].split('\n\n'))


ESTOQUE = {  # estoque.csv de 27/10
    ('Preto', 'P'): 13, ('Preto', 'M'): 27, ('Preto', 'G'): 24, ('Preto', 'GG'): 9,
    ('Mapple Brown', 'P'): 12, ('Mapple Brown', 'M'): 23, ('Mapple Brown', 'G'): 23, ('Mapple Brown', 'GG'): 11,
    ('Off White', 'P'): 11, ('Off White', 'M'): 24, ('Off White', 'G'): 24, ('Off White', 'GG'): 11,
}


def camiseta(estoque):
    vs = []
    for i, ((c, t), q) in enumerate(estoque.items()):
        vs.append({'id': 50899000000000 + i, 'title': f'{c} / {t}', 'option1': c, 'option2': t, 'price': 8000,
                   'available': q > 0, 'inventory_quantity': q, 'inventory_management': 'shopify', 'sku': f'MOD-CAM-{c}-{t}'})
    return {'title': 'Camiseta Básica Modestino', 'url': 'produto.html', 'price': 8000, 'media': media,
            'featured_media': media[0], 'description': desc('MOD-CAM'), 'variants': vs,
            'options_with_values': [{'values': ['Preto', 'Mapple Brown', 'Off White']}, {'values': ['P', 'M', 'G', 'GG']}],
            'selected_variant': None, 'selected_or_first_available_variant': vs[0]}


def kit(sku, titulo, preco, url):
    v = {'id': 5089900075, 'sku': sku, 'price': preco, 'available': True}
    fr = [m for m in media if 'de frente' in m['alt']]
    return {'title': titulo, 'url': url, 'price': preco, 'media': fr, 'featured_media': fr[0], 'description': desc(sku),
            'variants': [v], 'selected_or_first_available_variant': v}


def secao(tipo, sid, settings=None, blocks=None, order=None):
    src = (TEMA / 'sections' / f'{tipo}.liquid').read_text()
    sc = schema(src)
    s = {x['id']: x.get('default', '') for x in sc.get('settings', []) if 'id' in x}
    s.update(settings or {})
    bl = []
    for bid in (order or []):
        b = blocks[bid]
        bs = {}
        for bt in sc.get('blocks', []):
            if bt['type'] == b['type']:
                bs = {x['id']: x.get('default') for x in bt.get('settings', []) if 'id' in x}
        bs.update(b.get('settings', {}))
        bl.append({'id': bid, 'type': b['type'], 'settings': bs, 'shopify_attributes': ''})
    return {'id': sid, 'settings': s, 'blocks': bl}, sem_blocos_shopify(src)


def render_json(path, ctx):
    d = json.loads((TEMA / path).read_text())
    out = ''
    for sid in d['order']:
        x = d['sections'][sid]
        section, src = secao(x['type'], sid, x.get('settings'), x.get('blocks'), x.get('block_order'))
        out += env.from_string(src).render(**ctx, section=section)
    return out


def pagina(nome, titulo, corpo_ctx, template=None, corpo=None):
    ctx = dict(BASE)
    ctx.update(corpo_ctx)
    head = env.from_string(sem_blocos_shopify((TEMA / 'snippets/modestino-head.liquid').read_text())).render(**ctx)
    cab = render_json('sections/header-group.json', ctx)
    meio = corpo if corpo is not None else render_json(template, ctx)
    rod = render_json('sections/footer-group.json', ctx)
    doc = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} · MODESTINO (prévia)</title>{head}<style>body{{margin:0}}</style></head>
<body class="modestino">{cab}<main id="MainContent">{meio}</main>{rod}</body></html>"""
    (SAIDA / f'{nome}.html').write_text(doc)


cam = camiseta(ESTOQUE)
kits = {
    'kit-2-camisetas-basicas-modestino': kit('MOD-KIT2', 'Kit 2 Camisetas Básicas Modestino', 16000, 'kit-2.html'),
    'kit-3-camisetas-basicas-modestino': kit('MOD-KIT3', 'Kit 3 Camisetas Básicas Modestino', 22500, 'kit-3.html'),
    'kit-essencial-modestino': kit('MOD-KIT-ESS', 'Kit Essencial Modestino', 22500, 'kit-essencial.html'),
}
BASE = {
    'routes': {'root_url': 'inicio.html', 'cart_url': 'carrinho.html', 'cart_add_url': '#adicionado'},
    'cart': {'item_count': 0, 'items': [], 'discount_codes': []},
    'all_products': {'camiseta-basica-modestino': cam, **kits},
}

if __name__ == '__main__':
    SAIDA.mkdir(exist_ok=True)
    shutil.copytree(TEMA / 'assets', SAIDA / 'assets', dirs_exist_ok=True)
    shutil.copytree(LOJA / 'fotos-provisorias', SAIDA / 'fotos', dirs_exist_ok=True)

    pagina('inicio', 'Início', {}, 'templates/index.json')
    pagina('produto', 'Camiseta Básica', {'product': cam}, 'templates/product.json')
    esgot = dict(ESTOQUE); esgot[('Preto', 'GG')] = 0; esgot[('Preto', 'G')] = 2
    pagina('produto-esgotado', 'Camiseta Básica (Preto GG esgotado)', {'product': camiseta(esgot)}, 'templates/product.json')
    for h, k in kits.items():
        pagina(k['url'][:-5], k['title'], {'product': k}, 'templates/product.kit.json')
    pagina('kit-3-esgotado', 'Kit 3 (Preto GG esgotado)', {'product': kits['kit-3-camisetas-basicas-modestino'],
           'all_products': {**BASE['all_products'], 'camiseta-basica-modestino': camiseta(esgot)}}, 'templates/product.kit.json')
    pg = lambda t, f: {'page': {'title': t, 'content': (TEMA / 'paginas' / f).read_text()}}
    pagina('trocas', 'Trocas', pg('Trocas e devoluções', 'trocas.html'), 'templates/page.json')
    pagina('privacidade', 'Privacidade', pg('Privacidade', 'privacidade.html'), 'templates/page.json')
    pagina('perguntas-frequentes', 'Perguntas frequentes', {'page': {'title': 'Perguntas frequentes', 'content': ''}}, 'templates/page.faq.json')

    aviso = (TEMA / 'sections/modestino-carrinho-aviso.liquid').read_text()
    aviso_src = sem_blocos_shopify(aviso)
    vazio = env.from_string(aviso_src).render(**BASE)
    pagina('carrinho-vazio', 'Carrinho vazio', {}, corpo=vazio)
    carr = {'item_count': 1, 'items': [{'sku': 'MOD-KIT3', 'title': 'Kit 3', 'properties': {}}],
            'discount_codes': [{'code': 'KEANU6', 'applicable': False}]}
    linhas = ('<div class="m-wrap" style="padding-block: var(--space-5) var(--space-8)"><h1 style="font-size: var(--text-xl-size)">Seu carrinho</h1>'
              '<p class="m-muted">Kit 3 Camisetas Básicas Modestino · Peça 1: Preto · M · Peça 2: Mapple Brown · G · Peça 3: Off White · M · <span class="m-mono">R$ 225,00</span></p>'
              '<p class="m-muted">(Linhas, cupom e total vêm do carrinho do Horizon na Shopify; aqui só o aviso da Modestino.)</p></div>')
    cupom = env.from_string(aviso_src).render(**{**BASE, 'cart': carr})
    pagina('carrinho-cupom-kit', 'Carrinho com cupom no kit', {'cart': carr}, corpo=cupom + linhas)
    print('prévia em', SAIDA)
