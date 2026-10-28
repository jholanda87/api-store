# Estúdio criativo — padrões

Revisto em 28/10/2026 a pedido do Jorge. O critério agora é **desempenho**: o padrão é o das marcas de roupa que mais engajam no Instagram, com imagem hiper-realista, efeito visual e IA liberada. Não há lista de proibições de criação. O que decide se uma peça fica é o número dela (`estrategia.md`, seção 8) e se a camiseta da imagem é a mesma que o cliente vai receber, porque diferença vira troca.

Cor, fonte e logo da marca ficam em `loja/design/tokens.json` e `loja/design/logo/`, que são o ponto de partida e não um limite.

## 1. Princípios

1. **A peça é o espetáculo.** Ela flutua, gira, veste um corpo invisível, cai e se dobra, estica e volta. Um efeito que prenda o olho no primeiro segundo vale mais que qualquer texto.
2. **Acabamento de estúdio caro:** sem fundo, sem amassado, luz macia, sombra real, cor igual nas três cores. Foto crua do celular serve de matéria-prima, nunca de peça final.
3. **Pouco texto na arte e nenhum preço.** Preço, frete e condição vão na legenda, no story com link e na loja. A arte leva no máximo uma frase.
4. **Feito para o celular e sem som,** com movimento em loop: o Reel que se repete conta mais tempo assistido.
5. **Uma ideia e uma chamada por peça.** A chamada (comentar, enviar, salvar, tocar no link) fica na legenda ou no último segundo.

## 2. Formatos

| peça | tamanho | onde fica o essencial |
| --- | --- | --- |
| carrossel / post | 1080×1350 (4:5) | centro: a grade do perfil corta em 3:4 |
| Reel / story | 1080×1920 (9:16) | terço do meio; topo 250 px e base 380 px ficam sob a interface |
| capa de Reel | 1080×1920, lida em 3:4 | centro 1080×1440 |
| produto (loja) | 2048×2560 (4:5) | peça inteira, mesma escala nas três cores |
| catálogo (Meta/WhatsApp) | 1080×1080 (1:1) | peça inteira |

## 3. Formatos que mais engajam (o cardápio)

| formato | como fazemos | ferramenta | trabalho no funil |
| --- | --- | --- | --- |
| **Peça flutuando** (loop de 6 s) | recorte + flutuação com sombra que respira | `recorte.py` → `efeitos.py flutuar` | capa, story, anúncio |
| **Giro 360°** em manequim invisível | foto → vídeo de IA | `ia.py video giro360` | alcance, vitrine |
| **Corpo invisível vestindo** | foto → vídeo de IA | `ia.py video vestir` | alcance (efeito "como fez isso?") |
| **Tecido esticando e voltando** (macro) | foto ou vídeo → IA | `ia.py video esticar` | salvar, confiança no tecido |
| **Peça caindo e se dobrando** | foto → IA | `ia.py video cair` | transição, abertura de Reel |
| **Troca de cor no ritmo** | uma peça recortada por cor | `efeitos.py cores` | "Três cores, várias combinações." |
| **Olhe de perto** (zoom até a gola/etiqueta) | recorte + aproximação suave | `efeitos.py zoom` | curiosidade, salvar |
| **Manequim invisível (ghost mannequin)** | foto real → IA | `ia.py imagem manequim` | vitrine, carrossel |
| **Flat lay perfeito / editorial em linho** | foto real → IA | `ia.py imagem esticada` / `cena` | feed, catálogo |
| **Gente real** (fit check, Collab, ocasião) | gravação + `reel.py` | `reel.py`, CapCut | confiança e alcance de quem não segue |

Em cada lote, pelo menos metade das peças são de efeito, e uma é de gente real.

## 4. Tipografia (quando houver texto)

| uso | fonte | tamanho em 1080 px |
| --- | --- | --- |
| frase de capa | Instrument Serif | 110 a 120 px, até 6 palavras |
| texto de vídeo | Instrument Sans 600 | 52 a 60 px, até 6 palavras |
| nome MODESTINO | Instrument Sans 600, espaçado | 28 a 32 px |

Fonte, cor e destaque podem variar quando o teste mostrar que funciona melhor; registre o teste em `calendario.md`.

## 5. Fundo e cor

- **Linho `#ECE7DE`:** vitrine e peça clara.
- **Carvão `#22201D`:** drama e contraste, ótimo para o Off White.
- **Mapple `#5B3F30`:** peça da marca.
- **Cenário gerado** (`ia.py imagem cena`): linho natural, madeira clara, luz de janela.
- A **mesma peça** precisa ter **a mesma cor** em todas as imagens. Confira lado a lado antes de publicar.

## 6. Fotografia (matéria-prima)

A IA trabalha melhor quanto melhor for a foto. O que mais ajuda:

- **Fundo liso** e de cor diferente da peça: lençol branco, parede, papel. Nada de manta estampada.
- **Luz de janela, sem flash,** e a peça inteira no quadro, com folga nas bordas (manga cortada não se recupera).
- **Celular na resolução máxima,** de cima, paralelo à peça.
- **A mesma posição nas três cores:** frente, costas, gola de perto, etiqueta de perto, ombro e manga, dobrada.
- **Para o 360° e o vestir,** a melhor matéria-prima é a peça num manequim, mesmo simples. Sem manequim, a IA parte da foto estendida.

## 7. Vídeo

- **Gancho visual em até 1 s:** o efeito começa já no primeiro quadro.
- **Duração:** loops de 5 a 8 s; ritmo de 7 a 15 s; fala de 30 a 45 s.
- **Sem música na exportação:** o áudio em alta entra no próprio Instagram.
- **Cor "Modestino"** nos vídeos gravados: contraste +8, saturação −8, levemente quente (`reel.py`).

## 8. Texto e legenda

- **Primeira linha de até 8 palavras,** que é o gancho.
- **Corpo:** 1 a 3 frases e uma chamada.
- **Preço, frete e kit vão aqui,** na legenda, e não na arte.
- **Até 3 hashtags específicas** e "Fortaleza" quando houver lugar real.

## 9. Arquivos

- **Bruto** em `loja/estudio/entrada/`; **recortes, efeitos e IA** em `loja/estudio/vitrine/`. As duas pastas ficam fora do Git, porque as imagens são grandes.
- **Lote** em `loja/estudio/lotes/AAAA-MM-DD/`: os JSONs e as prévias.
- **Toda imagem ou vídeo de IA** sai com um `.json` ao lado (prompt, modelo, data), para refazer ou ajustar.

## 10. Checklist antes de mostrar ao Jorge

- [ ] O primeiro segundo (ou a capa) prende o olho.
- [ ] A peça da imagem é a peça real: cor, gola, etiqueta (letras certas), manga e barra. A IA costuma redesenhar letras pequenas; se errar, refaça com `--pro` ou devolva a etiqueta real.
- [ ] Nenhum preço na arte.
- [ ] Uma chamada só, na legenda ou no fim.
- [ ] Link com UTM conferido no celular.
