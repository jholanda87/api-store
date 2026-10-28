"""Links rastreados (UTM) da Modestino para Instagram, WhatsApp e embaixadores.

python3 .claude/skills/estudio-criativo-modestino/utm.py <campanha> [--peca <nome>] [--destino <caminho>]

Imprime um link por canal. A Shopify registra a origem (Relatórios → Sessões por UTM) e o pedido
mostra de onde veio; assim dá para saber qual post, story ou embaixador trouxe venda.
Exemplo: utm.py lote02-tres-cores --peca carrossel --destino /products/kit-3-camisetas-basicas-modestino
"""
import argparse
from urllib.parse import urlencode

LOJA = 'https://modestino-store.myshopify.com'
CANAIS = [
    ('instagram', 'bio'), ('instagram', 'story'), ('instagram', 'reels'), ('instagram', 'post'),
    ('instagram', 'direct'), ('whatsapp', 'atendimento'), ('whatsapp', 'status'),
    ('embaixador', 'keanu'), ('embaixador', 'paulovitor'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('campanha')
    ap.add_argument('--peca', default='')
    ap.add_argument('--destino', default='/')
    a = ap.parse_args()
    for fonte, meio in CANAIS:
        q = {'utm_source': fonte, 'utm_medium': meio, 'utm_campaign': a.campanha}
        if a.peca:
            q['utm_content'] = a.peca
        print(f'{fonte:<11} {meio:<12} {LOJA}{a.destino}?{urlencode(q)}')


if __name__ == '__main__':
    main()
