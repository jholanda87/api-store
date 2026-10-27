---
name: loja-lancamento-modestino
description: "Use quando Jorge pedir o lançamento da loja virtual da Modestino, texto da página inicial ou de produto, preço e frete da loja, anúncio para Mercado Livre, Shopee, Google ou catálogo do Instagram, ou o plano de Black Friday na loja: escreve, revisa contra limites e regras da marca, e monta o plano."
---

# Lançamento da loja (Replica adaptada)

Versão Modestino do `replica-launch`. Lê `loja/correcoes.md` (o ângulo e a evidência), `loja/voz.md` e `loja/marca.json`. Escreve em `loja/lancamento/`: `pagina-inicial.md`, `precos.md`, `anuncios.json`, `plano.md`.

Ferramenta (a versão Modestino do `listing.py`):

```bash
python3 .claude/skills/loja-lancamento-modestino/vitrine.py loja/lancamento/anuncios.json
```

Confere limite de caracteres de cada canal (loja/SEO, Mercado Livre, Shopee, Google, Meta, Instagram, WhatsApp — limites de out/2026, confira no canal e sobrescreva em `"limites"` se mudou), nome de outra marca, e as regras da casa: modal como "o" tecido, mesma peça em sequência, promessa não testada, streetwear, tom engessado, logo na roupa, urgência falsa, preço fora da tabela da Central. Comece de `vitrine.exemplo.json`. Saída 1 em erro.

## As regras

- **Nenhuma prova falsa.** Sem depoimento inventado, sem "mais de mil clientes", sem estrela inventada. Seção de prova vazia é melhor que falsa. Cliente real, com permissão, pode.
- **Frase de cliente dos outros não vira depoimento nosso.**
- **Nome de outra marca fora** de textos, anúncios, palavras-chave e campanhas.
- **Educar antes de vender.** Primeiro a utilidade (como achar o tamanho, como cuidar da peça); a compra vem como consequência.

## Passo 1: página inicial (`pagina-inicial.md`, depois construir)

1. **Primeira tela:** o ângulo como título (o que fazemos, para quem), uma linha embaixo, um botão. Foto real da peça.
2. **O problema:** os dois temas mais odiados de `feedback.md`, com nossas palavras (paráfrase, nunca citação).
3. **Como funciona:** escolher cor → achar o tamanho pela camiseta que já tem → receber rápido em Fortaleza.
4. **Diferenciais:** cada um preso a uma correção de `correcoes.md`. Paridade é o preço de entrada, não o argumento.
5. **Preço:** avulsa, kit 2, kit 3 (preço por peça).
6. **Perguntas:** as objeções reais (tamanho, tecido no calor, troca, prazo, Pix/cartão).
7. **Fechamento:** busto do Cavalheiro + MODESTINO + ação.

## Passo 2: preços e frete (`precos.md`)

- Tabela das referências e de 2 ou 3 alternativas locais, com link e **data** (preço muda).
- O que as avaliações dizem de preço e frete, com contagem.
- A tabela da Central é a lei: avulsa R$ 80; R$ 75/70 só sem embalagem; kit 2 R$ 160 (R$ 150 sem embalagem); kit 3 R$ 225; empresa R$ 210 (10–29) e R$ 195 (30+). Margem mínima 50% depois de cupom, comissão e taxa do gateway. Promoção usa o kit 3, nunca avulsa mais barata.
- Frete grátis só se a margem aguentar: calcule e mostre antes (ex.: frete grátis em Fortaleza no kit 3).
- Kit 3 a R$ 225 confirmado pelo Jorge em 27/10/2026. R$ 210 e R$ 195 existem só no preço por volume para empresas.

## Passo 3: anúncios (`anuncios.json`)

Página de produto e SEO, catálogo da Meta (Instagram/Facebook), Google Shopping e, quando houver CNPJ, Mercado Livre e Shopee (taxa de 12% a 20%: só com preço que absorva). Rode `vitrine.py` até zero erro.

## Passo 4: plano de lançamento (`plano.md`)

- **Antes:** lista de espera — "Comenta LOJA" no post e nos Stories, os ~20 clientes da Wolf e a lista de contatos quentes (meta 100); embaixadores com cupom pronto; pixel e medição no ar.
- **Dia 1:** post + Reels de lançamento (com `criar-conteudo-modestino` e `roteiro-reels-modestino`), Stories com o link, mensagem 1 a 1 para a lista pelo `atendimento-modestino` (Jorge envia), condição de lançamento já prevista na Central.
- **Semana 1:** responder todo comentário e Direct em até 10 min, falar à mão com os 10 primeiros compradores (o que quase os fez desistir?), impulsionar o post que engajou sozinho (`trafego-pago-modestino`).
- **Datas:** Black Friday 27/11 com o Kit Presente (kit 3) e Natal; empresas com o preço por volume.

## Saída

`loja/lancamento/` completo, página construída, `vitrine.py` sem erro. Próxima: `loja-deploy-modestino`.

## Fora deste repositório

Instalada pelo Claude.ai (arquivo .zip), as ferramentas citadas acima vêm dentro da própria pasta desta habilidade, ao lado deste SKILL.md: troque `.claude/skills/<pasta>/` pelo caminho desta pasta. Sem Python disponível, siga o método à mão; ele funciona igual.
