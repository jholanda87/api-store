# Construção da loja — registro

## 27/10/2026 (noite, 3ª rodada) — título pela identidade, promessa é a troca

Decisão do Jorge: o título fala da identidade (não dos donos) e a loja não promete "sem erro", só a troca.
- Título: "Três cores. Um caimento." (mockup aprovado). Subtítulo: "Camiseta básica masculina feita em Fortaleza. Lisa, sem logo na frente. Não serviu? A gente troca."
- Saíram "Conferida pelos donos" (vira "Costura no osso do ombro", do mockup), "Conferido e entregue pelos donos" na caixa de frete e a pergunta "Quem confere o pedido?".
- 4 arquivos reenviados ao tema de construção, checksums conferidos; tema segue não publicado.

## 27/10/2026 (noite, 2ª rodada) — textos no tom do mockup aprovado

Pedido do Jorge: textos minimalistas, só o necessário, na voz do mockup aprovado ("Modestino — Landing page", 21/10) e do Instagram, calibrados pelas lojas grandes.
- Estudo rápido (estrutura, sem copiar texto): nas grandes, título de produto com 2 palavras, faixa de 3 a 4 benefícios curtos, botões de 2 a 3 palavras, rodapé com links de 1 a 3 palavras e detalhes guardados em blocos.
- Início: título "O básico que os próprios donos conferem e entregam em Fortaleza." (frase A encurtada) + "Sem pedido errado, sem troca presa. Não serviu? A gente troca em mãos."; botão "Escolher a cor"; "Olhe de perto." com 4 linhas curtas; "Kit com 3, na ecobag."; fechamento "Básico com postura." (do mockup).
- Produto e kit: frases de uma linha, preço sem centavos (R$ 80, como no mockup), calculadora "Meça a que você já ama", "Adicionar · R$ 80", frete/troca/pagamento em uma linha cada, "Detalhes".
- Descrições dos 4 produtos encurtadas em `catalogo/textos.json` e gravadas na Shopify (`vitrine.py` 0 erros).
- Perguntas: 10, uma ou duas linhas cada. Rodapé: Loja · Ajuda · Contato, com @lojamodestino. Página de trocas: só o início e o contato encurtados (o resto é texto legal).
- 13 arquivos reenviados ao tema de construção, checksums conferidos; tema segue não publicado.

## 27/10/2026 (noite) — etapa 6: casca, telas e fotos provisórias

Tema "Modestino (construção)" (`167188168752`, **não publicado**), editado pelo conector (`themeFilesUpsert`); os 36 arquivos conferidos por checksum com `loja/tema/`. Tema no ar (Horizon `166315229232`) não foi tocado; loja continua com senha.
Prévia (precisa estar logado no admin da Shopify): https://nnwyy4-vp.myshopify.com/?preview_theme_id=167188168752 · editor: https://admin.shopify.com/store/nnwyy4-vp/themes/167188168752/editor
Prévia local (sem Shopify): `python3 loja/tema/tools/previa.py`, depois `node loja/tema/tools/prints.js` e `node loja/tema/tools/estados.js` (servidor em `loja/tema/previa`, porta 8765). Prints em `loja/clone-screens/`.

| tela | o que tem | situação |
| --- | --- | --- |
| casca | faixa (Entrega em Fortaleza R$ 10 · Troca em mãos · Pix ou cartão), cabeçalho com busto do Cavalheiro + MODESTINO, menu que vira gaveta < 860 px, rodapé com figura em linho, razão social, CNPJ, WhatsApp, Fortaleza/CE (sem endereço), favicon; fontes e tokens no tema | ✅ |
| S01 início | título "O básico que os próprios donos separam, conferem e entregam em Fortaleza." + subtítulo com o resto da frase A; um botão; foto real; "Quem vende é quem confere, entrega e troca"; kits; fechamento em mapple | ✅ |
| S02 coleção | não feita (1 produto + 3 kits; kits na home) | ⚪ |
| S03 produto | cor troca fotos e fundo; P–GG com a medida; esgotado riscado + "Avise-me" pelo WhatsApp; últimas peças (≤ 2); frete, troca e pagamento antes do botão; botão "Escolha o tamanho" até escolher; WhatsApp | ✅ |
| S04 calculadora | dentro de S03: largura da camiseta do cliente → tamanho mais próximo (P 51 · M 54 · G 57 · GG 60), marca sozinho, `aria-live`, erro fora de 45–66 cm, tabela de largura e tórax | ✅ |
| S05 kits | Kit 2 (R$ 160, R$ 80/peça), Kit 3 e Essencial (R$ 225, R$ 75/peça); cor e tamanho de cada peça vão para o pedido ("Peça 1: Preto · M"); estoque da camiseta bloqueia combinação esgotada; aviso do cupom de embaixador | ✅ (sem app) |
| S06 carrinho | carrinho do Horizon com as cores da marca; aviso de carrinho vazio ("Comece pela cor") e de cupom recusado no kit | 🟡 sem prints reais (precisa da prévia logada) |
| S07–S10 checkout, pedido | checkout da Shopify (não é tema) | ⚪ etapa 7 |
| S11 trocas | página `/pages/trocas` (texto de `politicas/trocas.md` com razão social e CNPJ) | ✅ página · ⚠️ política de reembolso da Shopify vazia |
| S12 perguntas | `/pages/perguntas-frequentes`, 12 perguntas a partir de `correcoes.md` e das políticas, sem promessa de lavagem | ✅ |
| S13 privacidade | página `/pages/privacidade` (processadores reais, pedidos pelo WhatsApp) | ✅ página · ⚠️ política automática da Shopify com endereço e e-mail pessoal |
| S14 sobre | não feita | ⚪ |

Fotos provisórias: 8 quadros dos 4 vídeos do Keanu (pasta "Vídeo Keanu" do Drive), escolhidos pelo quadro mais nítido em cada trecho, recorte 4:5 (1080×1350) cortando o rosto: preta frente e ombro; mapple frente, gola e lado; off white frente, costas e gola. Nenhum trecho sem camisa ou trocando de peça, nenhum escuro ou tremido, nenhuma selfie, nada de `2_preta_vestida` nem `4_espelho_preta`. Subidas pela API (upload temporário da Shopify) na Camiseta (cada cor ligada às suas variantes) e as 3 frentes nos 3 kits; a foto antiga (`IMG_3268`) saiu dos produtos. Cópias em `loja/fotos-provisorias/`.

Conferências: `vitrine.py` 0 erros; `sweep.py` limpo (troquei `preco_reserva` por `preco_padrao`, que batia com "Reserva"); contraste 13/13 AA; 390 e 1440 px sem rolagem lateral e sem erro no console (prévia local); estados testados: calculadora certa e com erro, esgotado, últimas peças, troca de cor, kit sem escolha, kit com combinação esgotada, carrinho vazio, cupom recusado no kit, menu do celular. Paridade 51,6 (11 de 23 obrigatórios).

Maior do que parecia / pendências:
- **Política de privacidade automática da Shopify mostra a rua e o e-mail pessoal do Jorge.** O conector não tem permissão (`write_legal_policies`): Jorge troca em Configurações → Políticas, colando `loja/tema/paginas/privacidade.html`, e preenche a de reembolso com `trocas.html`. Conferir também Configurações → Informações da loja (endereço aparece em e-mails e no checkout).
- Entrega local de R$ 10 em Fortaleza ainda não ligada na Shopify (a loja já anuncia).
- Prints da loja real: não deu para abrir a prévia (loja com senha; prévia de tema só logado). Os prints são da prévia local com os mesmos arquivos.
- O kit não baixa sozinho o estoque das variantes: lançar a baixa por peça até haver app de kits.
- Bloco antigo `blocks/modestino-kit-pecas.liquid` continua no tema, sem uso (a página de kit agora é a seção `modestino-kit`).

## 27/10/2026 — escolha das peças nos kits

- Tema: cópia do Horizon "Modestino (construção)" (`167188168752`, não publicado). O tema no ar não foi alterado.
- `loja/tema/blocks/modestino-kit-pecas.liquid`: para cada peça, cor e tamanho (com a medida de axila a axila). Kit 2 = 2 peças, Kit 3 e Essencial = 3; o Essencial já abre com uma de cada cor, e o cliente troca se quiser. As escolhas vão para o pedido como "Peça 1: Preto · M". Estoque lido da Camiseta Básica: combinação esgotada (ou repetida além do estoque) bloqueia o botão com aviso. Compra expressa escondida na página de kit (pularia a escolha).
- `loja/tema/templates/product.kit.json`: página de kit (título, preço, escolha das peças, comprar, descrição). Os 3 kits usam o modelo "kit"; no tema atual, sem esse modelo, eles caem na página padrão.
- Handle do Kit Essencial: `kit-essencial-modestino` (o antigo redireciona).
- **Não testado no navegador:** a loja tem senha e a prévia do tema só abre logado. Jorge confere pela prévia.
- Baixa de estoque: o kit não baixa sozinho as variantes da camiseta; lançar a baixa de cada peça (Painel → `estoque.py` → Shopify) até haver app de kits.

Próximo: calculadora de tamanho na página da camiseta, cabeçalho/rodapé com a marca (Cavalheiro, CNPJ, políticas), cores e fontes dos tokens.
