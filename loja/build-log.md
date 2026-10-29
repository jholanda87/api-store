# Construção da loja — registro

## 28–29/10/2026 — fotos oficiais no lugar das do Keanu

- Fotos oficiais das três cores no cabide (enviadas pelo Jorge em 28/10): escolhidas as melhores de cada cor (frente, gola com etiqueta, lado, costura do ombro; Mapple também a etiqueta de lavagem), cortadas em 4:5 sem mexer na cor. Descartadas as escuras, tremidas, de luz amarelada/acinzentada e as com etiqueta cortada. Brutos em `loja/estudio/entrada/<cor>/`, prontas em `loja/estudio/vitrine/loja/` (fora do Git).
- Manequim invisível por cor (`ia.py`, Nano Banana Pro na fal.ai, resultado devolvido na própria resposta porque `v3b.fal.media` está bloqueado no ambiente): mesmo enquadramento nas três (a preta saiu da composição da marrom, trocando só a cor), fundo linho `#ECE7DE`. Correções feitas à mão: etiqueta reescrita na Poppins ("MODESTINO / essencial. diário. real.", a IA errava a frase), retângulo da etiqueta interna que aparecia pela off white removido, suporte da arara tirado do fundo, cor conferida contra a foto real (off white neutralizada ~2%; marrom = média das fotos de gola, que variam com a luz). Arquivos em `loja/estudio/vitrine/ia/*-manequim-final.png`.
- Shopify: Camiseta com 16 fotos (por cor: IA "de frente" primeiro, depois as reais "foto real"); o texto alternativo mantém "preta" / "mapple" / "off white" para a galeria trocar com a cor e só a de IA tem "de frente" (vai para a primeira tela). Variantes ligadas à foto de IA da sua cor. Kits 2, 3 e Essencial: as três fotos de IA (preta, mapple, off white). Fotos do Keanu desvinculadas dos 4 produtos, não apagadas (continuam em Arquivos e em `loja/fotos-provisorias/`).
- Vídeo 360°: os primeiros mostravam o nome nas costas. Refeito o da preta pedindo costas lisas (não conferido: o vídeo fica em `v3b.fal.media`); off white e Mapple pendentes, saldo da fal.ai esgotado. Nenhum vídeo na loja até o Jorge conferir.
- **Não conferido no navegador:** o ambiente não abre o site nem o CDN da Shopify.

## 27/10/2026 (23h30) — correção dos cupons na cópia

Jorge duplicou o tema publicado: "Cópia de Modestino (construção)" (`167202390064`, não publicado). Enviados para a cópia, conferidos por checksum: `modestino-carrinho-aviso`, `modestino-kit`, `templates/page.faq.json`, `templates/index.json` (cupom vale em toda a loja). O rodapé da cópia mantém o endereço do CNPJ. Falta o Jorge publicar a cópia. Daqui em diante, mudanças sempre em cópia não publicada.

## 27/10/2026 (23h) — loja aberta e cupons em toda a loja

- Às 23:11 o tema "Modestino (construção)" (`167188168752`) passou a ser o publicado (MAIN) e a senha da loja foi desligada, pelo admin (não por esta sessão). O Horizon antigo (`166315229232`) virou não publicado. A partir daqui o conector **não escreve mais nesse tema** (bloqueio de tema publicado): mudanças vão numa cópia duplicada pelo Jorge e publicada por ele.
- Cupons `KEANU6` e `PAULOVITOR6` (decisão do Jorge): 6% em qualquer compra, avulsa ou kit; sem limite de usos (limite é o estoque); continuam sem acumular com outro desconto. Atualizados e conferidos na Shopify.
- Textos do tema ajustados no repositório (aviso de "cupom não vale no kit" removido do kit e do carrinho; pergunta frequente reescrita), **mas não enviados**: o tema agora está publicado. Ficam para a cópia.
- Políticas de privacidade e reembolso com o endereço do CNPJ, conferidas pela API.

## 27/10/2026 (noite) — entrega local conferida no checkout

Print do Jorge no checkout (CEP de Fortaleza, depois de refazer a configuração): "Entrega local R$ 10,00 — Entrega própria em Fortaleza. Combinamos o horário pelo WhatsApp." com campo de celular obrigatório, e "Padrão R$ 22,00 — 3 a 5 dias úteis" como segunda opção. Falta só conferir um CEP de fora (61600-000, Caucaia: deve aparecer só o Padrão).

## 27/10/2026 (noite) — endereço do CNPJ na loja

Decisão do Jorge: usar o endereço do CNPJ (o residencial dele) como endereço físico da loja, para cumprir o Decreto 7.962, mesmo sem loja física; ele foi avisado de que fica público. Aplicado só na Shopify: rodapé (novo campo `endereco` do `modestino-rodape`, preenchido em `sections/footer-group.json` do tema) e fim das páginas Trocas e Privacidade. **O endereço não entra no repositório**: aqui o campo fica vazio e o `footer-group.json` local difere do tema de propósito; ao reenviar esse arquivo, preencher o campo pelo editor de tema ou pela conversa. Políticas de privacidade e reembolso da Shopify: Jorge acrescenta o endereço no admin.

## 27/10/2026 (noite) — entrega local

Jorge configurou no admin a Entrega local de R$ 10 por CEP de Fortaleza (decisão: valor acessível para gerar fluxo, mesmo abaixo do custo nas entregas longas). A Admin API não expõe a entrega local e a simulação de pedido (`draftOrderCalculate`) só lista as tarifas de frete ("Padrão" R$ 22 em 60150-160, 60871-000 e 61600-000): a conferência final é um teste no checkout. **Testado pelo Jorge: a Entrega local de R$ 10 aparece no checkout com CEP de Fortaleza.**

## 27/10/2026 (noite) — políticas da Shopify

Jorge trocou no admin a política de privacidade automática (que mostrava rua e e-mail pessoal) pelo texto de `tema/paginas/privacidade.html` e preencheu a política de reembolso com `trocas.html`. Conferido pela API e na página pública da política: sem endereço nem e-mail pessoal.

## 27/10/2026 (noite, 5ª rodada) — linha visual da Parla e da Fusion

Referências indicadas pelo Jorge: [Parla](https://parlabr.com/) (@parlabr) e [Fusion](https://usefusion.com.br/) (@usefusion_). Estudo só de estrutura (nenhum texto, foto ou código copiado): foto em tela cheia com pouco texto por cima, grade de produtos logo depois (foto, nome, preço, cores), botões arredondados, fundo claro, dúvidas em lista abrir/fechar com o atendimento ao lado, rodapé com central de atendimento.
- Início: primeira tela agora é foto em tela cheia (as três cores lado a lado no computador, uma no celular), com título, uma linha e "Conhecer". Nova seção "Essenciais" (Camiseta + 3 kits, com cores, preço por peça e segunda foto ao passar o mouse). "Olhe de perto" em fundo claro. Nova seção "Dúvidas" com 4 perguntas e WhatsApp. Botões arredondados em toda a loja.
- Tokens: `overlay.hero` e `size.hero` novos em `tokens.json` (contraste 13/13 AA). Novas seções `modestino-vitrine` e `modestino-duvidas`; `modestino-kits` fica sem uso.
- Sem avaliações de cliente ainda (as referências usam; só entram quando houver avaliações reais).
- 6 arquivos enviados ao tema de construção e conferidos por checksum; tema segue não publicado.
- Título trocado pelo Jorge para "Três cores, várias combinações." (o caimento é o mesmo nas três; o que muda é a cor).

## 27/10/2026 (noite, 4ª rodada) — tom profissional

Pedido do Jorge: nada de linguagem informal nem menção aos donos. Reescritos: subtítulo da primeira tela ("Camiseta básica masculina, produzida em Fortaleza. Lisa, sem logo aparente. Troca de tamanho em até 30 dias."), botões ("Atendimento via WhatsApp", "Selecione o tamanho", "Guia de medidas", "Calcular"), mensagens de estoque e de cupom, cards dos kits, perguntas frequentes (9), rodapé ("Atendimento todos os dias"), páginas de trocas e privacidade (linguagem formal, mesmas regras) e descrições dos 4 produtos (`vitrine.py` 0 erros). 9 arquivos do tema reenviados e conferidos; páginas e produtos atualizados na Shopify.

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
