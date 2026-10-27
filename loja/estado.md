# Loja virtual Modestino — estado do projeto

Pasta de trabalho da máquina de vendas (o equivalente da pasta `replica/` da Replica).
Cada habilidade lê o que a anterior escreveu aqui. Números de venda, estoque e caixa
continuam no Painel da Modestino; estratégia e decisões na Central Modestino.

| etapa | habilidade | arquivo | situação |
| --- | --- | --- | --- |
| 0. Pré-requisitos | administrativo-modestino | loja/administrativo.md, politicas/ | 🔴 CNPJ não aberto · políticas em rascunho (27/10) |
| 1. Mapa das referências | loja-recon-modestino | loja/recon.md, features.csv | 🟡 recon público feito (27/10); falta página de produto completa e checkout pelo navegador do Jorge |
| 2. O que o cliente odeia | loja-empreendedor-modestino | loja/reviews.csv, feedback.md, correcoes.md | 🟡 aguardando coleta pelo Jorge (coleta-avaliacoes.md) |
| 3. Arquitetura | loja-arquitetura-modestino | loja/arquitetura.md | 🟡 Shopify; cupom 10% mantido; frete por distância do ponto mais perto (frete.md); falta bairro do Ponto L |
| 4. Design | loja-design-modestino | loja/design/ | ✅ tokens, componentes, amostra e logo do Drive aplicado (PNG transparente + favicon); SVG opcional |
| 5. Catálogo e estoque | catalogo-modestino | loja/catalogo.csv, estoque.csv, catalogo/ | 🟡 pronto para gravar (27/10): 4 produtos, 12 variantes, 212 peças, textos com `vitrine.py` 0 erro; **não gravado na Shopify** (conector pediu login de novo); sem fotos |
| 6. Construção | loja-build-modestino | loja/build-log.md | ⚪ |
| 7. Pagamento, frete, integrações | loja-backend-modestino | loja/backend.md | ⚪ |
| 8. Testes | loja-teste-modestino | loja/test-plan.md, bugs.md | ⚪ |
| 9. Paridade | loja-paridade-modestino | loja/paridade.md | ⚪ 0 de 23 obrigatórios |
| 10. Varredura da marca | loja-marca-modestino | loja/marca.json | 🟡 lista de nomes pronta; paleta neutra confirmada (27/10) |
| 11. Lançamento | loja-lancamento-modestino | loja/lancamento/ | ⚪ |
| 12. No ar | loja-deploy-modestino | loja/deploy.md | ⚪ depende do CNPJ e do ok do Jorge |
| Depois do ar | trafego-pago-modestino, pos-venda-modestino, maquina-vendas-modestino | loja/funil.md | ⚪ |

## Etapa 5 — catálogo (27/10/2026)

Preparado para a loja `nnwyy4-vp`, tudo como **rascunho**. Não chegou a ser gravado: o conector da Shopify pediu login de novo antes do `get-shop-info`, então a loja (moeda BRL, fuso America/Fortaleza) e a busca por duplicados ainda não foram conferidas.

| produto | variantes | preço | estoque |
| --- | --- | --- | --- |
| Camiseta Básica Modestino | 12 (Cor × Tamanho), SKU `MOD-CAM-<PRETA\|MARROM\|OFF>-<P\|M\|G\|GG>`, estoque controlado | R$ 80,00 | 212 (por variante em `estoque.csv`) |
| Kit 2 Camisetas Básicas | 1 (`MOD-KIT2`), com ecobag | R$ 160,00 | baixa nas variantes da camiseta |
| Kit 3 Camisetas Básicas | 1 (`MOD-KIT3`), com ecobag | R$ 225,00 | baixa nas variantes da camiseta |
| Kit Essencial (uma de cada cor) | 1 (`MOD-KIT-ESS`), com ecobag | R$ 225,00 | baixa nas variantes da camiseta |

Arquivos: `catalogo/textos.json` (títulos, descrições e SEO, revisados com `vitrine.py`), `catalogo.csv`, `estoque.csv` e `catalogo/shopify-import.csv` (importação da Shopify, status draft, estoque no local padrão).

Para gravar, depois de reconectar: `get-shop-info` → `search_products` por `sku:MOD-*` → `create-product` (status DRAFT, `inventoryItem.tracked` na camiseta) → `get-inventory-levels` → `set-inventory` com `estoque.csv`. Ou Jorge importa o `shopify-import.csv` em Produtos → Importar.

Estoque vai no local padrão até existirem os locais Ponto J e Ponto L (endereços só no cadastro da Shopify, nunca aqui). Seleção de cor e tamanho por peça nos kits fica para a construção (app de kits ou campos do carrinho).
