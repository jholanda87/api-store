# Loja virtual Modestino — estado do projeto

Pasta de trabalho da máquina de vendas (o equivalente da pasta `replica/` da Replica).
Cada habilidade lê o que a anterior escreveu aqui. Números de venda, estoque e caixa
continuam no Painel da Modestino; estratégia e decisões na Central Modestino.

| etapa | habilidade | arquivo | situação |
| --- | --- | --- | --- |
| 0. Pré-requisitos | administrativo-modestino | loja/administrativo.md, politicas/ | 🟡 MEI aberto em 27/10 (CNPJ 69.828.190/0001-36) · políticas em rascunho · endereço do rodapé e teto proporcional do MEI a ver com o contador |
| 1. Mapa das referências | loja-recon-modestino | loja/recon.md, features.csv | 🟡 recon público feito (27/10); falta página de produto completa e checkout pelo navegador do Jorge |
| 2. O que o cliente odeia | loja-empreendedor-modestino | loja/reviews.csv, feedback.md, correcoes.md | ✅ 114 reclamações de 4 marcas (28/10); correcoes.md com 8 correções; frase A aprovada e 10 lavagens confirmadas (28/10) |
| 3. Arquitetura | loja-arquitetura-modestino | loja/arquitetura.md | ✅ Shopify + Mercado Pago; cupons de 6% (`KEANU6`, `PAULOVITOR6`, criados na Shopify) só na avulsa; frete R$ 10 em Fortaleza saindo do Ponto J; pesos estimados para Correios (28/10) |
| 4. Design | loja-design-modestino | loja/design/ | ✅ tokens, componentes, amostra e logo do Drive aplicado (PNG transparente + favicon); SVG opcional |
| 5. Catálogo e estoque | catalogo-modestino | loja/catalogo.csv, estoque.csv, catalogo/ | 🟡 4 rascunhos na Shopify `nnwyy4-vp` (27/10): camiseta com 12 variantes e 212 peças no Ponto J; SEO gravado; fotos **provisórias** (frames dos vídeos do Keanu, 27/10); faltam fotos de estúdio e seleção por peça nos kits |
| 6. Construção | loja-build-modestino | loja/build-log.md, loja/tema/ | 🟡 tema de construção montado (27/10, não publicado, loja com senha): casca + S01, S03/S04, S05, S11–S13 com todos os estados; fotos **provisórias** dos vídeos do Keanu; falta S02, S14, prints da prévia real e ligar a entrega local |
| 7. Pagamento, frete, integrações | loja-backend-modestino | loja/backend.md | 🟡 Mercado Pago ativado na Shopify (27/10, informado pelo Jorge; a API não mostra o gateway); Mercado Pago em modo teste; frete: internacional desligado, Brasil R$ 22, Fortaleza R$ 10 ainda **não** ligado (a tarifa criada valia para o Brasil todo e foi removida em 27/10; refazer como Entrega local por CEP); pesos de envio gravados (28/10), falta tarifa calculada dos Correios fora de Fortaleza; meios de pagamento: os que o Mercado Pago oferece, boleto incluído (decisão do Jorge, 27/10); margem refeita com Shopify 2% + taxas do Checkout do Mercado Pago (Pix 0,99%, cartão 3,98%) |
| 8. Testes | loja-teste-modestino | loja/test-plan.md, bugs.md | ⚪ |
| 9. Paridade | loja-paridade-modestino | loja/paridade.md | ⚪ 0 de 23 obrigatórios |
| 10. Varredura da marca | loja-marca-modestino | loja/marca.json | 🟡 lista de nomes pronta; paleta neutra confirmada (27/10) |
| 11. Lançamento | loja-lancamento-modestino | loja/lancamento/ | ⚪ |
| 12. No ar | loja-deploy-modestino | loja/deploy.md | ⚪ depende do CNPJ e do ok do Jorge |
| Depois do ar | trafego-pago-modestino, pos-venda-modestino, maquina-vendas-modestino | loja/funil.md | ⚪ |

## Etapa 5 — catálogo (27/10/2026)

Gravado como rascunho e **ativado em 27/10** na Loja virtual (loja ainda com senha; Ponto de venda não) na loja `nnwyy4-vp` (Minha loja 2; BRL, America/Fortaleza, plano trial). Antes de criar: busca por `vendor`/SKU sem nenhum produto existente.

| produto | variantes | preço | estoque | admin |
| --- | --- | --- | --- | --- |
| Camiseta Básica Modestino | 12 (Cor × Tamanho), SKU `MOD-CAM-<PRETA\|MARROM\|OFF>-<P\|M\|G\|GG>`, estoque controlado | R$ 80,00 | 212 (por variante em `estoque.csv`) | [10343489273904](https://admin.shopify.com/store/nnwyy4-vp/products/10343489273904) |
| Kit 2 Camisetas Básicas Modestino | 1 (`MOD-KIT2`), com ecobag | R$ 160,00 | não controlado: baixa nas variantes da camiseta | [10343489568816](https://admin.shopify.com/store/nnwyy4-vp/products/10343489568816) |
| Kit 3 Camisetas Básicas Modestino | 1 (`MOD-KIT3`), com ecobag | R$ 225,00 | idem | [10343489732656](https://admin.shopify.com/store/nnwyy4-vp/products/10343489732656) |
| Kit Essencial Modestino (sugestão: uma de cada cor; cores livres) | 1 (`MOD-KIT-ESS`), com ecobag | R$ 225,00 | idem | [10343489896496](https://admin.shopify.com/store/nnwyy4-vp/products/10343489896496) |

Arquivos: `catalogo/textos.json` (títulos, descrições e SEO, revisados com `vitrine.py`), `catalogo.csv`, `estoque.csv` e `catalogo/shopify-import.csv` (cópia de segurança para importação manual; não importar de novo, duplicaria).

Atualizado em 27/10 (tarde), por decisão do Jorge:
- **Só um ponto de despacho por enquanto:** o local padrão virou "Ponto J" (endereço só no cadastro da Shopify, nunca aqui) e guarda as 212 peças. O Ponto L fica para depois.
- **SEO** (título e descrição de `textos.json`) gravado nos 4 produtos.
- **Foto provisória:** um quadro do vídeo `IMG_3268.mov` do Drive (camiseta preta vestida, recorte 4:5, 1080×1350) nos 4 produtos e nas variantes Preto. Não há foto real de Mapple Brown nem de Off White que preste no Drive (só folhas de quadros de vídeo em baixa resolução; os MP4 do Keanu passam de 10 MB e o conector do Drive não baixa). Trocar tudo quando o estúdio ficar pronto.
- **Kits:** qualquer cor que o cliente quiser, nos três. O Kit Essencial fica como sugestão pronta (uma de cada cor), mas o cliente pode trocar as cores. A escolha por peça entra na construção, por campos no carrinho ou app de kits.

Falta: fotos de estúdio; seleção de cor e tamanho por peça nos kits e baixa no estoque da camiseta (app de kits ou campos do carrinho, na construção); gateway de pagamento. Plano Basic da Shopify assinado (27/10); nome da loja já é MODESTINO; loja com senha.


## Peso de envio (28/10/2026)

Gravado na Shopify `nnwyy4-vp` (busca por SKU `MOD-*`, sem chutar id), com "requer frete" ligado em todas as variantes; conferido lendo de volta. Preço, estoque (212), textos e status não mudaram. Base: seção "Peso para Correios" de `frete.md`.

| produto | SKU | variantes | peso |
| --- | --- | --- | --- |
| Camiseta Básica Modestino | `MOD-CAM-*` | 12 | 250 g |
| Kit 2 Camisetas Básicas Modestino | `MOD-KIT2` | 1 | 500 g |
| Kit 3 Camisetas Básicas Modestino | `MOD-KIT3` | 1 | 750 g |
| Kit Essencial Modestino | `MOD-KIT-ESS` | 1 | 750 g |

Frete visto em 28/10: perfil geral (Ponto J) só com a tarifa fixa "Padrão" R$ 22 para o Brasil inteiro; **nenhuma tarifa calculada pelos Correios** e nenhum app de frete (carrier service) ligado. A entrega local de Fortaleza (R$ 10) não aparece pela API e não foi mexida. Falta o Jorge escolher: app Melhor Envio ou Frenet (cotação real dos Correios pelo peso), ou tarifas manuais por faixa de peso. Nada instalado nem criado.

## Atendimento (28/10/2026)

WhatsApp Business da loja: (85) 98155-9590, todos os dias, sem robô. Link testado pelo Jorge em 28/10. Link do botão da loja e do rodapé: https://wa.me/5585981559590?text=Oi%21%20Vim%20pela%20loja%20da%20MODESTINO%20e%20tenho%20uma%20d%C3%BAvida.

## Cupons de embaixador (decisão do Jorge, 28/10/2026)

Criados na Shopify `nnwyy4-vp` e conferidos lendo de volta. Antes de criar: nenhum desconto existia na loja.

| código | embaixador | desconto | vale para | combina | fim / limite | admin |
| --- | --- | --- | --- | --- | --- | --- |
| `KEANU6` | Keanu | 6% | só Camiseta Básica Modestino avulsa (produto 10343489273904); não vale para Kit 2, Kit 3 nem Kit Essencial | não combina com nenhum outro desconto (produto, pedido nem frete) | sem fim, sem limite de usos | [1492022722608](https://admin.shopify.com/store/nnwyy4-vp/discounts/1492022722608) |
| `PAULOVITOR6` | Paulo Vitor | 6% | idem | idem | idem | [1492022755376](https://admin.shopify.com/store/nnwyy4-vp/discounts/1492022755376) |

Ativos desde 27/10 00:00 (Fortaleza), para todos os clientes. Comissão do embaixador: 10% sobre o valor pago. Margem da avulsa com cupom e comissão: 51,5% no Pix e 48,5% no cartão (Shopify 2% + Mercado Pago 0,99% Pix / 3,98% cartão). Regras 14 a 16 de `politicas/antifraude.md` valem (embaixador não usa o próprio cupom; venda lançada no Painel com o embaixador em `seller`).

## Fotos provisórias (27/10/2026)

**As fotos da loja são provisórias:** 8 quadros dos vídeos do Keanu (preta: frente e ombro; mapple brown: frente, gola e lado; off white: frente, costas e gola), em `loja/fotos-provisorias/`. Estão na Camiseta Básica (cada cor ligada às suas variantes) e nos 3 kits (as 3 frentes). **O Jorge vai mandar fotos novas**; quando chegarem, trocar todas, incluindo costas da preta e da mapple brown, que não existem nos vídeos.
