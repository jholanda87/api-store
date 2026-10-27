# Loja virtual Modestino — estado do projeto

Pasta de trabalho da máquina de vendas (o equivalente da pasta `replica/` da Replica).
Cada habilidade lê o que a anterior escreveu aqui. Números de venda, estoque e caixa
continuam no Painel da Modestino; estratégia e decisões na Central Modestino.

| etapa | habilidade | arquivo | situação |
| --- | --- | --- | --- |
| 0. Pré-requisitos | administrativo-modestino | loja/administrativo.md, politicas/ | 🟡 MEI aberto em 27/10 (CNPJ 69.828.190/0001-36) · políticas em rascunho · endereço do rodapé e teto proporcional do MEI a ver com o contador |
| 1. Mapa das referências | loja-recon-modestino | loja/recon.md, features.csv | 🟡 recon público feito (27/10); falta página de produto completa e checkout pelo navegador do Jorge |
| 2. O que o cliente odeia | loja-empreendedor-modestino | loja/reviews.csv, feedback.md, correcoes.md | 🟡 Insider: 24 reclamações (28/10); faltam Reserva, Hering e Básico |
| 3. Arquitetura | loja-arquitetura-modestino | loja/arquitetura.md | 🟡 Shopify; cupom 10% mantido; frete por distância do ponto mais perto (frete.md); falta bairro do Ponto L |
| 4. Design | loja-design-modestino | loja/design/ | ✅ tokens, componentes, amostra e logo do Drive aplicado (PNG transparente + favicon); SVG opcional |
| 5. Catálogo e estoque | catalogo-modestino | loja/catalogo.csv, estoque.csv, catalogo/ | 🟡 4 rascunhos na Shopify `nnwyy4-vp` (27/10): camiseta com 12 variantes e 212 peças no Ponto J; SEO gravado; foto provisória (preta vestida); faltam fotos de estúdio e seleção por peça nos kits |
| 6. Construção | loja-build-modestino | loja/build-log.md | ⚪ |
| 7. Pagamento, frete, integrações | loja-backend-modestino | loja/backend.md | ⚪ |
| 8. Testes | loja-teste-modestino | loja/test-plan.md, bugs.md | ⚪ |
| 9. Paridade | loja-paridade-modestino | loja/paridade.md | ⚪ 0 de 23 obrigatórios |
| 10. Varredura da marca | loja-marca-modestino | loja/marca.json | 🟡 lista de nomes pronta; paleta neutra confirmada (27/10) |
| 11. Lançamento | loja-lancamento-modestino | loja/lancamento/ | ⚪ |
| 12. No ar | loja-deploy-modestino | loja/deploy.md | ⚪ depende do CNPJ e do ok do Jorge |
| Depois do ar | trafego-pago-modestino, pos-venda-modestino, maquina-vendas-modestino | loja/funil.md | ⚪ |

## Etapa 5 — catálogo (27/10/2026)

Gravado como **rascunho** (nada publicado) na loja `nnwyy4-vp` (Minha loja 2; BRL, America/Fortaleza, plano trial). Antes de criar: busca por `vendor`/SKU sem nenhum produto existente.

| produto | variantes | preço | estoque | admin |
| --- | --- | --- | --- | --- |
| Camiseta Básica Modestino | 12 (Cor × Tamanho), SKU `MOD-CAM-<PRETA\|MARROM\|OFF>-<P\|M\|G\|GG>`, estoque controlado | R$ 80,00 | 212 (por variante em `estoque.csv`) | [10343489273904](https://admin.shopify.com/store/nnwyy4-vp/products/10343489273904) |
| Kit 2 Camisetas Básicas Modestino | 1 (`MOD-KIT2`), com ecobag | R$ 160,00 | não controlado: baixa nas variantes da camiseta | [10343489568816](https://admin.shopify.com/store/nnwyy4-vp/products/10343489568816) |
| Kit 3 Camisetas Básicas Modestino | 1 (`MOD-KIT3`), com ecobag | R$ 225,00 | idem | [10343489732656](https://admin.shopify.com/store/nnwyy4-vp/products/10343489732656) |
| Kit Essencial Modestino: uma de cada cor | 1 (`MOD-KIT-ESS`), com ecobag | R$ 225,00 | idem | [10343489896496](https://admin.shopify.com/store/nnwyy4-vp/products/10343489896496) |

Arquivos: `catalogo/textos.json` (títulos, descrições e SEO, revisados com `vitrine.py`), `catalogo.csv`, `estoque.csv` e `catalogo/shopify-import.csv` (cópia de segurança para importação manual; não importar de novo, duplicaria).

Atualizado em 27/10 (tarde), por decisão do Jorge:
- **Só um ponto de despacho por enquanto:** o local padrão virou "Ponto J" (endereço só no cadastro da Shopify, nunca aqui) e guarda as 212 peças. O Ponto L fica para depois.
- **SEO** (título e descrição de `textos.json`) gravado nos 4 produtos.
- **Foto provisória:** um quadro do vídeo `IMG_3268.mov` do Drive (camiseta preta vestida, recorte 4:5, 1080×1350) nos 4 produtos e nas variantes Preto. Não há foto real de Mapple Brown nem de Off White que preste no Drive (só folhas de quadros de vídeo em baixa resolução; os MP4 do Keanu passam de 10 MB e o conector do Drive não baixa). Trocar tudo quando o estúdio ficar pronto.
- **Kits:** qualquer cor que o cliente quiser (Kit 2 e Kit 3). A escolha por peça entra na construção, por campos no carrinho ou app de kits.

Falta: fotos de estúdio; seleção de cor e tamanho por peça nos kits e baixa no estoque da camiseta (app de kits ou campos do carrinho, na construção); gateway de pagamento; plano pago da Shopify antes de vender.
