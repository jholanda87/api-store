# Estúdio criativo — padrões

Fonte única de cor, fonte e logo: `loja/design/tokens.json` e `loja/design/logo/`. As ferramentas (`arte.js`, `reel.py`, `foto.py`) já aplicam estes padrões; aqui estão as regras para quem criar ou conferir à mão (CapCut, Canva, celular).

## 1. Princípios

1. **Menos, porém melhor.** Uma ideia por peça, uma afirmação por lâmina, um botão por tela. O espaço vazio faz parte da marca.
2. **A roupa é a protagonista.** Foto e vídeo mostram tecido, gola, ombro, caimento e cor; o rosto aparece só quando não der para evitar.
3. **Reconhecível em 1 segundo.** Mesmos elementos sempre: linho/carvão/mapple, Instrument Serif nos títulos, o Cavalheiro só na abertura ou no fechamento. Mudar o conteúdo, nunca o sistema.
4. **Pensado para o celular, sem som.** Texto grande, contraste AA, legenda em todo vídeo com fala.
5. **Cada peça com um trabalho:** alcance, envio, salvar, clique ou conversa. Se não dá para dizer qual, a peça não está pronta.

## 2. Formatos

| peça | tamanho | área segura | observação |
| --- | --- | --- | --- |
| carrossel / post | 1080×1350 (4:5) | 88 px nas laterais, 96 px em cima e embaixo | a grade do perfil corta em 3:4: título e foco no centro |
| story / Reel / capa | 1080×1920 (9:16) | topo 250 px e base 380 px livres (interface do app) | texto principal no terço do meio |
| capa de Reel no perfil | 1080×1920, lida em 3:4 | centro 1080×1440 | título no centro, nunca nas pontas |
| texto de vídeo (overlay) | 1080×1920 transparente | terço inferior, acima dos 380 px | caixa carvão, texto linho |
| destaque (capa) | 1080×1920, ícone no centro | círculo central de ~600 px | fundo linho, traço carvão |
| produto (loja) | 2048×2560 (4:5) | foco em peito e gola | mesma luz e enquadramento nas três cores |
| catálogo (Meta/WhatsApp) | 1080×1080 (1:1) | peça inteira visível | fundo limpo |

## 3. Tipografia (em 1080 px de largura)

| uso | fonte | tamanho | observação |
| --- | --- | --- | --- |
| título de capa | Instrument Serif 400 | 110 a 120 px | até 6 palavras; itálico para a ênfase |
| título de lâmina | Instrument Serif 400 | 84 a 96 px | até 10 palavras |
| texto de apoio | Instrument Sans 400 | 38 a 42 px | até 24 caracteres por linha, 2 a 3 linhas |
| texto de vídeo | Instrument Sans 600 | 52 a 60 px | caixa carvão, até 6 palavras |
| dado (preço, medida, numeração) | Geist Mono 400 | 28 a 32 px | números tabulares |
| nome MODESTINO | Instrument Sans 600 | 28 a 32 px | espaçamento 0,32 em, caixa alta |

Destaque de palavra na capa: fundo areia `#CBBFAE` atrás de uma palavra (no JSON: `*palavra*`). No máximo uma por peça.

## 4. Cor por pilar

| fundo | quando | texto |
| --- | --- | --- |
| linho `#ECE7DE` | utilidade, tamanho, fechamento | carvão |
| linho escuro `#E4DDD0` (chave `areia` nas ferramentas) | oferta (kit, entrega), dados | carvão |
| carvão `#22201D` | frase de impacto, pergunta final, texto de vídeo | linho |
| mapple `#5B3F30` | marca e fechamento especial (no máximo 1 por semana) | linho |
| foto | produto e gente | linho sobre o degradê escuro de baixo |

Nada de cor viva, terracota, branco puro ou preto puro de fundo.

## 5. Fotografia (briefing para as fotos oficiais)

**Luz e cenário:** luz natural lateral de janela (manhã ou fim de tarde), sem flash; parede clara lisa ou tecido linho ao fundo; mesma posição de câmera para as três cores. Celular na horizontal da pessoa, a 1,5 m, altura do peito; modo retrato desligado; foto em resolução máxima.

**Por cor (Preto, Mapple Brown, Off White), na mesma pessoa e no mesmo dia:**
1. frente vestida, braços relaxados (peça inteira até o quadril);
2. costas vestida;
3. lado (perfil), para mostrar o caimento;
4. gola de perto (a 30 cm);
5. ombro e manga de perto (costura no osso do ombro);
6. nome MODESTINO na nuca interna (gola virada com a mão);
7. peça dobrada sobre linho, vista de cima;
8. as três cores juntas (dobradas lado a lado e penduradas na arara).

**Kits:** flat lay das 3 peças + ecobag sobre linho; ecobag fechada com o cordão; mão segurando a ecobag.

**Gente e ocasião (para Reels e Collab):** treino, trabalho e social, cada um com a sua peça (nunca a mesma em sequência), em lugares reais de Fortaleza; pessoa em movimento (andar, ajustar a manga, virar).

**Nunca:** sem camisa ou trocando de peça, espelho de banheiro, tremida, escura, fora de foco, filtro pesado.

## 6. Vídeo

- **Gravação:** vertical 9:16, 1080p ou 4K a 30 fps, luz de frente ou lateral, tomadas de 3 a 5 s com a câmera parada; cada tomada começa e termina em movimento (facilita o corte).
- **Lista de tomadas por cor:** caminhando até a câmera; virando 360°; ajustando a manga; mão passando na gola; close do tecido esticando e voltando; peça sendo dobrada; ecobag sendo fechada.
- **Edição:**
  - gancho em até 2 s, com texto na tela e ação ao mesmo tempo;
  - cortes de 1,5 a 2,5 s nos Reels de ritmo;
  - de 7 a 15 s nos de ritmo e de 30 a 45 s nos de fala;
  - cor "Modestino": contraste +8, saturação −8, levemente quente, nitidez leve;
  - legenda em toda fala;
  - fechamento de 1,5 s com o Cavalheiro e MODESTINO.
- **Áudio:** exporte sem música; escolha o áudio em alta no próprio Instagram.
- **Tipos** (ver `roteiro-reels-modestino`): série, frase, resposta e tecido. Os de ritmo vêm de `reels-capcut-modestino`: fit check, macro → revelação, GRWM e transição.

## 7. Vitrine da loja

- Cada cor com a mesma sequência de fotos (seção 5, itens 1 a 7), na mesma ordem em todas: frente, costas, lado, gola, ombro, nome, dobrada.
- `foto.py` aplica a cor e corta em 4:5 (produto), 1:1 (catálogo) e 9:16 (story). Recorte de fundo e sombra (Photoroom) só com ok, porque gasta créditos.
- `alt` de cada foto: cor + vista ("Camiseta básica Modestino off white, costas").
- Trocar as fotos provisórias em todos os produtos e variantes no mesmo dia, para a loja não misturar padrões.

## 8. Texto e legenda

- **Gancho na primeira linha** (até 8 palavras), com uma das formas que funcionam: número concreto, pergunta real de cliente, situação específica, contrário ao senso comum ou instrução para amanhã.
- **Corpo** de 1 a 3 frases curtas e **uma chamada só:** comentar uma palavra, enviar para alguém, salvar, tocar no link ou chamar no WhatsApp.
- **Tom profissional e direto,** sem emoji em excesso e sem "a gente" demais. Nada de prometer lavagem, durabilidade ou "pedido sem erro". Modal é só um dos tecidos.
- Até 3 hashtags específicas e a localização "Fortaleza" quando houver gente ou lugar real.

## 9. Arquivos

- Material bruto em `loja/estudio/entrada/` (fora do Git), com o nome original.
- Lote em `loja/estudio/lotes/AAAA-MM-DD/`: um JSON por peça + saída gerada (`modestino-<peça>-01.png`…, `<reel>.mp4`, folhas de prévia).
- Vitrine em `loja/estudio/vitrine/` (`<foto>-produto.jpg`, `-catalogo.jpg`, `-story.jpg`).
- Publicado vai para a pasta "postagens" do Drive com o número da ordem (`agendar-post-modestino`).

## 10. Checklist antes de mostrar ao Jorge

- [ ] a peça tem um trabalho (alcance, envio, salvar, clique, conversa) e uma chamada só
- [ ] gancho nos 2 primeiros segundos ou na capa, específico
- [ ] só fotos e vídeos reais da Modestino; nenhum trecho proibido (seção 5)
- [ ] cores e fontes de `tokens.json`; Cavalheiro só na abertura ou no fechamento
- [ ] texto dentro da área segura; legível no celular (tamanho mínimo da seção 3)
- [ ] nenhuma promessa fora do que a loja diz (troca, entrega R$ 10, preços, medidas)
- [ ] link com UTM conferido abrindo no celular
- [ ] folha de prévia e folha de quadros olhadas inteiras
