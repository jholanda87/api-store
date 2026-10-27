---
name: trafego-pago-modestino
description: "Use quando Jorge pedir anúncio, impulsionamento, campanha na Meta (Instagram/Facebook) ou Google, orçamento de tráfego, público, criativo de anúncio ou resultado dos anúncios da Modestino: planeja, escreve e mede sem passar do teto de gasto."
---

# Vendas e tráfego pago da Modestino

O setor "Vendas e Tráfego" que a Central (seção 15) deixou "a criar". Nada é ligado, pago ou publicado sem o ok do Jorge; Claude não entra no Gerenciador de Anúncios nem digita cartão. Claude entrega o plano, os textos, as artes e a leitura dos números.

## Regras da casa (Central, seções 4, 6 e 7)

- **Teto:** até R$ 300 por lote em anúncio; teste de R$ 20/dia aprovado em 16/10. Marketing = 20% do custo do lote nos 3 primeiros lotes (~R$ 1.260 no lote 1), 10% depois.
- **Impulsionar o que já engajou sozinho,** não criar anúncio do zero. Criativo aprovado (16/10): golas das 3 cores, "Toque de segunda pele" (feed A, A2 e stories).
- **A peça que aparece vendendo é sempre foto ou vídeo real.**
- Regras de texto da marca (as do `vitrine.py` valem para anúncio também); não vender de cara: o anúncio abre com utilidade ou curiosidade.

## Passo a passo

1. **Objetivo e destino.** Sem loja: conversa no Direct/WhatsApp (ig.me/m/lojamodestino). Com loja: vendas no site com pixel + API de conversões (`loja-backend-modestino`) e catálogo ligado.
2. **Escolher o post.** Puxe do Metricool (marca 7230036) os posts do mês com IGPO (alcance, interações, salvamentos, seguidores) e escolha o de melhor taxa de interação por alcance. Explique em uma linha por quê.
3. **Público** (no máximo 3 conjuntos): (a) homens 22–40 em Fortaleza + 15 km, interesse em moda masculina/academia/trabalho; (b) quem interagiu com o perfil em 90 dias; (c) com loja: quem visitou produto ou adicionou ao carrinho em 14 dias (remarketing com o kit 3). Excluir quem comprou nos últimos 30 dias.
4. **Textos:** 3 variações curtas no tom da marca, uma pergunta ou utilidade na primeira linha, chamada para o Direct ou para a loja. Rode `vitrine.py` com `"canal": "meta"`.
5. **Orçamento:** dividir o teto em blocos de 3 a 4 dias; pausar o conjunto que gastar 2× o ticket (R$ 160) sem conversa ou venda.
6. **Medir toda segunda** (junto com `diretoria-semanal-modestino`): gasto, alcance, cliques, conversas iniciadas, vendas atribuídas (pixel, cupom ou "como nos conheceu?"), **CAC = gasto ÷ vendas novas** e retorno (receita ÷ gasto). Registre em `marketing.ads` do Painel (`{date, spend, note}`). Meta Ads não está ligado ao Metricool: pico de alcance sem post forte = provável anúncio; diga isso.
7. **Decidir:** manter, trocar criativo ou parar. No máximo 3 opções, uma recomendada.

## Pendência para ligar tudo

Conectar a conta de anúncios da Meta ao Metricool (Central seção 15) e, com loja, o pixel. Enquanto isso, a atribuição é pelo cupom e pela pergunta "como nos conheceu?" em toda venda.

## Como responder

Curto: o post escolhido e por quê, público, textos, orçamento por dia, e o que medir. Na leitura semanal: CAC, retorno, o melhor conjunto e uma decisão.
