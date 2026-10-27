# Construção da loja — registro

## 27/10/2026 — escolha das peças nos kits

- Tema: cópia do Horizon "Modestino (construção)" (`167188168752`, não publicado). O tema no ar não foi alterado.
- `loja/tema/blocks/modestino-kit-pecas.liquid`: para cada peça, cor e tamanho (com a medida de axila a axila). Kit 2 = 2 peças, Kit 3 e Essencial = 3; o Essencial já abre com uma de cada cor, e o cliente troca se quiser. As escolhas vão para o pedido como "Peça 1: Preto · M". Estoque lido da Camiseta Básica: combinação esgotada (ou repetida além do estoque) bloqueia o botão com aviso. Compra expressa escondida na página de kit (pularia a escolha).
- `loja/tema/templates/product.kit.json`: página de kit (título, preço, escolha das peças, comprar, descrição). Os 3 kits usam o modelo "kit"; no tema atual, sem esse modelo, eles caem na página padrão.
- Handle do Kit Essencial: `kit-essencial-modestino` (o antigo redireciona).
- **Não testado no navegador:** a loja tem senha e a prévia do tema só abre logado. Jorge confere pela prévia.
- Baixa de estoque: o kit não baixa sozinho as variantes da camiseta; lançar a baixa de cada peça (Painel → `estoque.py` → Shopify) até haver app de kits.

Próximo: calculadora de tamanho na página da camiseta, cabeçalho/rodapé com a marca (Cavalheiro, CNPJ, políticas), cores e fontes dos tokens.
