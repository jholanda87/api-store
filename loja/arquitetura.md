# Arquitetura da loja — proposta para aprovação

Feita em 27/10/2026 com `loja-arquitetura-modestino`, a partir de `recon.md` e da Central. `correcoes.md` ainda não existe (aguarda a coleta de avaliações): as correções entram no passo 5.

## 1. Plataforma — recomendação: Shopify

| opção | por quê | atenção |
| --- | --- | --- |
| **Shopify (recomendada)** | Jorge já conectou; o Claude cadastra produto, estoque, desconto e lê pedidos direto; catálogo da Meta e Google nativos | mensalidade em dólar; Pix e boleto só por gateway externo; taxa da Shopify por venda quando o gateway é externo |
| Nuvemshop | Pix e frete brasileiros nativos, plano de entrada barato | sem conector do Claude: tudo manual |
| Site próprio | — | manutenção maior que as 3 a 4 h/dia dos sócios |

Preços em fontes secundárias de 2026 divergem (Basic entre US$ 19 e US$ 39/mês; taxa de 2% por venda no Basic com gateway externo; teste com US$ 1/mês por 3 meses). **Confira em [shopify.com/pt/precos](https://shopify.com/pt/precos) antes de assinar.** Fontes: [Base](https://base.com/pt-BR/blog/shopify-guia-completo/), [Sellfy](https://sellfy.com/pt/blog/precos-do-shopify/), [GoSmarter](https://gosmarter.com.br/shopify-brasil-vale-a-pena/), [EasySell](https://easysellapp.com/blogs/wiki/brazil-ecommerce-shopify-market-entry-2026).

Gateway (Pix + cartão até 3x): Mercado Pago, Pagar.me ou PagBank. Escolher pela menor taxa de Pix e pela antecipação; Jorge cria a conta no CNPJ.

## 2. ⚠️ Achado: a taxa online quebra o piso de margem do cupom

Custo R$ 26,70/peça (kit 2 R$ 55,40, kit 3 R$ 82,10 com ecobag). Taxas **estimadas** (a confirmar com o gateway escolhido): Shopify 2% + cartão 4,99% ou Pix ~0,99%.

| venda | cartão | Pix |
| --- | --- | --- |
| avulsa R$ 80 | 59,6% | 63,6% |
| kit 2 R$ 160 | 58,4% | 62,4% |
| kit 3 R$ 225 | 56,5% | 60,5% |
| **avulsa com cupom (R$ 72 − 10% comissão)** | **45,9%** 🔴 | **49,9%** 🔴 |
| **kit 3 com comissão de embaixador** | **46,5%** 🔴 | 50,5% 🟡 |

Fora da loja (Pix direto, sem plataforma) o cupom fica em 53%. **Na loja online, o cupom de embaixador passa do piso de 50%.** Três saídas (decisão do Jorge na reunião de segunda):

1. **(recomendada)** Na loja online, o cupom dá **frete grátis em Fortaleza** em vez de 10% (a Central já prevê isso no kit); comissão de 10% mantida.
2. Cupom de 5% na loja online; 10% continua só no Direct/WhatsApp com Pix.
3. Manter 10% e aceitar margem de ~46% a 50% nessas vendas (contraria a regra da Central).

## 3. Catálogo

- Produto **Camiseta Básica Modestino**, variantes cor (Preto, Mapple Brown, Off White) × tamanho (P, M, G, GG), SKU `MOD-CAM-<COR>-<TAM>`, estoque pelo `estoque.py` (212 peças em 27/10).
- **Kit 2** R$ 160, **Kit 3** R$ 225 (confirmado em 27/10), **Kit Essencial** (uma de cada cor, R$ 225), todos com ecobag, escolha de cor e tamanho por peça, baixando o estoque das variantes (app de kits/bundles da Shopify ou produto com opções + baixa manual no primeiro mês).
- Cupom por embaixador (Paulo Vitor, Keanu) conforme a decisão do item 2; nunca acumula com kit.
- Empresas: kit 3 a R$ 210 (10–29) e R$ 195 (30+) por pedido manual (rascunho de pedido na Shopify).

## 4. Integrações

| frente | escolha | observação |
| --- | --- | --- |
| pagamento | gateway externo com Pix + cartão até 3x | juros repassados (Central seção 8) |
| frete Fortaleza | taxa fixa local + "trocar em mãos" | entrega própria ou Uber Flash |
| frete fora | app de cotação (Melhor Envio ou Frenet) | peso da ecobag com 3 peças a medir |
| estoque | Painel → Shopify (`estoque.py` + conector `set-inventory`) | no mesmo dia de cada venda no Direct |
| vendas | Shopify → Painel (`list-orders` → `financeiro-modestino`) | origem e cupom em cada pedido |
| Meta / Google | pixel + API de conversões, catálogo, Analytics, Merchant Center | `trafego-pago-modestino` |
| WhatsApp | botão + catálogo | |
| nota fiscal | emissor ligado à Shopify | depois do CNPJ |

## 5. Riscos

1. Estoque em duas casas: cada pedido online precisa dizer quem despacha. Decidir a regra (por bairro, por cor ou por quem tem a peça).
2. A mesma peça vendida no Direct e na loja no mesmo dia: lançar no Painel no mesmo dia e rodar o `estoque.py`.
3. Margem com taxas (item 2).

## 6. Ordem

1. Fatia vertical: Camiseta Básica com as 12 variantes, Pix em teste, frete de Fortaleza, pedido confirmado.
2. Os 23 `must` de `features.csv`.
3. Kits e cupons.
4. Correções de `correcoes.md` (após a coleta).

Próxima etapa: `loja-design-modestino` (tokens já prontos) e `catalogo-modestino` (cadastro na Shopify, em rascunho, quando o conector voltar).
