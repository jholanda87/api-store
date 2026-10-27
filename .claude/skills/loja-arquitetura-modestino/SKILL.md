---
name: loja-arquitetura-modestino
description: "Use quando Jorge perguntar qual plataforma usar para a loja virtual da Modestino (Shopify, Nuvemshop, site próprio), como organizar produtos, kits, cupons e estoque, ou como ligar pagamento, frete, WhatsApp e o Painel: escreve a arquitetura da loja."
---

# Arquitetura da loja (Replica adaptada)

Versão Modestino do `replica-architect`. Lê `loja/recon.md`, `loja/features.csv` e `loja/correcoes.md`. Escreve `loja/arquitetura.md`. Sem recon, pare e rode `loja-recon-modestino`: planejar loja de memória é como se esquece metade.

## Passo 1: a plataforma (no máximo 3 opções, uma recomendada)

A Modestino tem 2 sócios com 3 a 4 h por dia e um produto. A regra da Replica vale em dobro: **tecnologia chata e gerenciada**. Loja em código próprio só se uma plataforma pronta não fizer o que o recon pede.

| opção | quando | atenção |
| --- | --- | --- |
| **Shopify** (recomendada por padrão) | já existe conector do Claude para produto, estoque, coleção, desconto e pedido; catálogo da Meta e Google nativos | mensalidade em dólar; Pix e frete por app (ex.: Mercado Pago/Pagar.me, Melhor Envio/Frenet) |
| Nuvemshop | plano grátis para começar, Pix e frete brasileiros nativos | sem conector do Claude hoje: lançamentos manuais |
| Site próprio (Next.js + Mercado Pago/Stripe) | só se as duas acima não servirem | mais manutenção do que os sócios têm |

Confira o preço do plano na página oficial no dia e escreva a data. Não assine nada: Jorge cria a conta.

## Passo 2: o catálogo (o "esquema")

- **Produto:** Camiseta Básica Modestino. **Variantes:** cor (Preto, Mapple Brown, Off White) × tamanho (P, M, G, GG). SKU `MOD-CAM-<COR>-<TAM>` (o mesmo que `catalogo-modestino/estoque.py` gera).
- **Kits:** produto próprio (Kit 2 R$ 160, Kit 3 R$ 225, com ecobag; sem embalagem R$ 150 no kit 2) com escolha das cores e tamanhos de cada peça, baixando o estoque das variantes. Kit Essencial: uma de cada cor.
- **Cupons:** um por embaixador, 10% **só na avulsa**, sem acumular com kit (senão a margem cai para 49%). Empresa: preço por volume (R$ 210 de 10 a 29 kits, R$ 195 a partir de 30) por pedido manual ou lista de preço.
- **Pedido:** guarda o cupom e a origem (anúncio, orgânico, embaixador, WhatsApp) para o ranking de vendedor e a comissão do Painel.
- **Dinheiro em centavos,** horário em `America/Fortaleza`.

## Passo 3: as integrações (só APIs oficiais, chaves do Jorge)

| frente | o que liga | por quê |
| --- | --- | --- |
| pagamento | Pix + cartão até 3x (juros repassados) | Central seção 8 |
| frete | cálculo pelo CEP + entrega local em Fortaleza com preço fixo | Uber Flash / entrega própria |
| estoque | Painel → loja (planilha do `estoque.py`) | o Painel é a fonte única dos números |
| vendas | loja → Painel (cada pedido vira `sales[]` pela `financeiro-modestino`) | caixa e metas batem |
| Meta | pixel + API de conversões, catálogo para Instagram Shopping | `trafego-pago-modestino` |
| Google | Analytics + Merchant Center | |
| WhatsApp | botão de atendimento e catálogo | `atendimento-modestino` |
| e-mail | confirmação, rastreio, carrinho abandonado | `pos-venda-modestino` |
| nota fiscal | emissor ligado à plataforma | só depois do CNPJ |

## Passo 4: o que morde

Escreva uma linha para cada: estoque dividido entre a casa do Jorge e a do Lucas (quem despacha cada pedido); venda no Direct e na loja ao mesmo tempo (a mesma peça vendida duas vezes — o Painel é atualizado no mesmo dia); Pix que expira; webhook que chega duas vezes; LGPD (dados do cliente); frete para fora de Fortaleza; troca que volta para o estoque.

## Passo 5: ordem de construção

1. **Fatia vertical:** um produto com as 12 variantes, Pix, frete de Fortaleza, pedido confirmado. Feio pode; funcionando é o ponto.
2. Os `must` de `features.csv` por área.
3. Os `should`, depois os `could`.
4. As correções de `correcoes.md`.

## Saída

`loja/arquitetura.md` com a plataforma (com o porquê em uma linha), catálogo, integrações, riscos e ordem. Resumo: plataforma, número de variantes, integrações, os 3 riscos maiores. Registre a escolha da plataforma na Central depois do ok do Jorge. Próxima: `loja-design-modestino`.
