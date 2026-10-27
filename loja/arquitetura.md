# Arquitetura da loja — proposta para aprovação

Feita em 27/10/2026 com `loja-arquitetura-modestino`, a partir de `recon.md` e da Central. `correcoes.md` ainda não existe (aguarda a coleta de avaliações): as correções entram no passo 5.

## 1. Plataforma — recomendação: Shopify

| opção | por quê | atenção |
| --- | --- | --- |
| **Shopify (recomendada)** | Jorge já conectou; o Claude cadastra produto, estoque, desconto e lê pedidos direto; catálogo da Meta e Google nativos | mensalidade em dólar; Pix e boleto só por gateway externo; taxa da Shopify por venda quando o gateway é externo |
| Nuvemshop | Pix e frete brasileiros nativos, plano de entrada barato | sem conector do Claude: tudo manual |
| Site próprio | — | manutenção maior que as 3 a 4 h/dia dos sócios |

Preços em fontes secundárias de 2026 divergem (Basic entre US$ 19 e US$ 39/mês; taxa de 2% por venda no Basic com gateway externo; teste com US$ 1/mês por 3 meses). **Confira em [shopify.com/pt/precos](https://shopify.com/pt/precos) antes de assinar.** Fontes: [Base](https://base.com/pt-BR/blog/shopify-guia-completo/), [Sellfy](https://sellfy.com/pt/blog/precos-do-shopify/), [GoSmarter](https://gosmarter.com.br/shopify-brasil-vale-a-pena/), [EasySell](https://easysellapp.com/blogs/wiki/brazil-ecommerce-shopify-market-entry-2026).

Gateway (Pix + cartão até 3x): **Mercado Pago** (decidido pelo Jorge em 27/10), conta no CNPJ do MEI. Taxas reais de Pix e cartão a confirmar na conta para refazer a tabela de margem abaixo.

## 2. ⚠️ Achado: a taxa online quebra o piso de margem do cupom

Custo R$ 26,70/peça (kit 2 R$ 55,40, kit 3 R$ 82,10 com ecobag). Taxas **estimadas** (a confirmar com o gateway escolhido): Shopify 2% + cartão 4,99% ou Pix ~0,99%.

| venda | cartão | Pix |
| --- | --- | --- |
| avulsa R$ 80 | 59,6% | 63,6% |
| kit 2 R$ 160 | 58,4% | 62,4% |
| kit 3 R$ 225 | 56,5% | 60,5% |
| **avulsa com cupom (R$ 72 − 10% comissão)** | **45,9%** 🔴 | **49,9%** 🔴 |
| **kit 3 com comissão de embaixador** | **46,5%** 🔴 | 50,5% 🟡 |

Fora da loja (Pix direto, sem plataforma) o cupom fica em 53%.

**Atualização (27/10, tarde):** Mercado Pago Checkout Pro ligado, recebimento em 30 dias. Shopify cobra 2% por venda (gateway externo, plano Basic). Taxas do **Checkout** no painel do Mercado Pago (print do Jorge, 27/10): Pix 0,99%; crédito à vista 3,98% (parcelado com juros do comprador até 3,98%); boleto R$ 3,49; Open Finance 0%. Custo R$ 26,70/peça (kits com ecobag).

| venda | Pix (2,99%) | cartão (5,98%) | boleto (2% + R$ 3,49) | Open Finance (2%) |
| --- | --- | --- | --- | --- |
| avulsa R$ 80 | 63,6% | 60,6% | 60,3% | 64,6% |
| kit 2 R$ 160 | 62,4% | 59,4% | 61,2% | 63,4% |
| kit 3 / Essencial R$ 225 | 60,5% | 57,5% | 60,0% | 61,5% |
| **avulsa com cupom (R$ 72 − 10% comissão)** | **49,9%** 🟡 | **46,9%** 🔴 | **46,1%** 🔴 | 50,9% |
| **kit 3 com comissão de embaixador** | 50,5% 🟡 | **47,5%** 🔴 | 50,0% 🟡 | 51,5% |

**Decisão do Jorge (27/10):** manter o cupom de 10% também na loja online. Exceção aceita ao piso de 50%, registrada na Central (seção 10). Rever quando o gateway e a taxa real do Pix forem escolhidos.

## 3. Catálogo

- Produto **Camiseta Básica Modestino**, variantes cor (Preto, Mapple Brown, Off White) × tamanho (P, M, G, GG), SKU `MOD-CAM-<COR>-<TAM>`, estoque pelo `estoque.py` (212 peças em 27/10).
- **Kit 2** R$ 160, **Kit 3** R$ 225 (confirmado em 27/10), **Kit Essencial** (uma de cada cor, R$ 225), todos com ecobag, escolha de cor e tamanho por peça, baixando o estoque das variantes (app de kits/bundles da Shopify ou produto com opções + baixa manual no primeiro mês).
- Cupom de 10% por embaixador (Paulo Vitor, Keanu), só na avulsa; nunca acumula com kit.
- Empresas: kit 3 a R$ 210 (10–29) e R$ 195 (30+) por pedido manual (rascunho de pedido na Shopify).

## 4. Integrações

| frente | escolha | observação |
| --- | --- | --- |
| pagamento | Mercado Pago (app na Shopify): Pix + cartão até 3x | juros repassados (Central seção 8) |
| frete Fortaleza | entrega local, taxa fixa de R$ 10, saindo do Ponto J (Jorge, de carro) | decidido em 28/10; ver `frete.md` |
| frete fora | app de cotação (Melhor Envio ou Frenet) | peso da ecobag com 3 peças a medir |
| estoque | Painel → Shopify (`estoque.py` + conector `set-inventory`) | no mesmo dia de cada venda no Direct |
| vendas | Shopify → Painel (`list-orders` → `financeiro-modestino`) | origem e cupom em cada pedido |
| Meta / Google | pixel + API de conversões, catálogo, Analytics, Merchant Center | `trafego-pago-modestino` |
| WhatsApp | botão + catálogo | |
| nota fiscal | emissor ligado à Shopify | depois do CNPJ |

## 5. Riscos

1. Estoque em duas casas: despacha quem estiver mais perto do cliente e tiver a peça (decidido em 27/10). A loja precisa do estoque por ponto.
2. A mesma peça vendida no Direct e na loja no mesmo dia: lançar no Painel no mesmo dia e rodar o `estoque.py`.
3. Margem com taxas (item 2).

## 6. Ordem

1. Fatia vertical: Camiseta Básica com as 12 variantes, Pix em teste, frete de Fortaleza, pedido confirmado.
2. Os 23 `must` de `features.csv`.
3. Kits e cupons.
4. Correções de `correcoes.md` (após a coleta).

Próxima etapa: `loja-design-modestino` (tokens já prontos) e `catalogo-modestino` (cadastro na Shopify, em rascunho, quando o conector voltar).
