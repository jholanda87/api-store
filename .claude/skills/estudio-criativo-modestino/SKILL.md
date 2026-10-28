---
name: estudio-criativo-modestino
description: "Use quando Jorge pedir artes, comunicação visual, design gráfico, carrossel, post, story, capa, Reels, edição de foto ou vídeo, tirar fundo, manequim invisível, vídeo 360° ou efeito com IA, fotos da vitrine da loja, plano ou calendário de conteúdo, ou quiser levar mais gente do Instagram e do WhatsApp para a loja virtual da Modestino: dirige a criação de ponta a ponta (estratégia, peça, edição, distribuição e medição) com foco em alcance, curiosidade e venda."
---

# Estúdio criativo da Modestino (direção de criação)

Etapa 13 da máquina de vendas: o estúdio que faz as pessoas chegarem até a loja. Trabalhe como diretor de criação sênior que também entende de distribuição e de conversão: cada peça tem um trabalho no funil, um formato que o Instagram distribui e um caminho medido até a loja ou o WhatsApp.

Esta habilidade **dirige**; as outras executam partes. Não repita o que elas já fazem:

| parte | habilidade | quando chamar |
| --- | --- | --- |
| método de carrossel e regras de texto da marca | `criar-conteudo-modestino` | todo carrossel ou post único |
| roteiro de Reels (4 tipos) e regras de gravação | `roteiro-reels-modestino` | antes de gravar |
| edição de bruto no CapCut, animatic, kit de textos | `reels-capcut-modestino` | quando chegar vídeo bruto |
| subir no Drive e agendar no Metricool | `agendar-post-modestino` | só depois do ok do Jorge |
| impulsionar o que já engajou | `trafego-pago-modestino` | post vencedor da semana |
| textos de loja, anúncio e `vitrine.py` | `loja-lancamento-modestino` | legenda de produto e anúncio |
| mensagens depois da compra | `pos-venda-modestino` | pedido de foto/avaliação do cliente |

## Leia antes de criar

1. `loja/estudio/estrategia.md` — diagnóstico com os números reais, funil, pilares, ritmo, metas.
2. `loja/estudio/padroes.md` — sistema visual das peças (grade, tipografia, cor, foto, vídeo, vitrine) e checklist.
3. `loja/estudio/calendario.md` — o que está planejado e o que já saiu.
4. `loja/design/tokens.json` e `loja/design/logo/` — cores, fontes e o Cavalheiro (fonte única da identidade).
5. `loja/correcoes.md` e `loja/estado.md` — o que a marca promete e o que não promete.

## Diretrizes (revistas em 28/10/2026)

- **Desempenho acima de tudo.** O padrão é o das marcas de roupa que mais engajam: imagem hiper-realista, peça sem fundo, efeito visual (flutuar, girar 360°, vestir um corpo invisível, esticar, cair e dobrar). **IA liberada** para imagem e vídeo. Não há lista de proibições de criação; quem decide é o número da peça.
- **Fidelidade à peça.** A camiseta que aparece é a que o cliente recebe: cor, gola, etiqueta, manga. Diferença vira troca. Conferir sempre (checklist de `padroes.md`).
- **Sem preço na arte.** Preço, frete e kit vão na legenda, no story com link e na loja.
- **Créditos e APIs pagas liberados** (decisão de 28/10). Registrar o gasto do lote em `calendario.md`.
- **Publicar, agendar, impulsionar e mandar a cliente** continuam passando pelo ok do Jorge.
- As fotos do Keanu (out/2026) não são oficiais.

## Fluxo de um lote (semanal)

1. **Ler os números** da semana anterior no Metricool (marca `7230036`): por post, alcance, envios (shares), salvos, seguidores ganhos; por Reel, retenção e taxa de visualização acima de 3 s. Ler na Shopify as sessões por UTM e os pedidos com origem. Escrever em `calendario.md` o vencedor e o perdedor da semana e por quê (uma linha cada).
2. **Planejar o lote** (5 a 7 peças) pela mistura de `estrategia.md`: pelo menos 2 Reels, 1 carrossel, stories diários, 1 peça de conversão. Cada peça tem: pilar, objetivo (alcance, envio, salvar, clique, conversa), gancho, CTA e link UTM.
3. **Briefing de produção** quando faltar material: lista de fotos e tomadas de `padroes.md` (seção de fotografia), com local, luz, peça e duração. O material bruto chega em `loja/estudio/entrada/` (fora do Git).
4. **Produzir** (ferramentas desta pasta; cardápio de formatos em `padroes.md`, seção 3):
   - **recorte:** `python3 .claude/skills/estudio-criativo-modestino/recorte.py <fotos> [--fundo linho|carvao|areia|mapple]`. Tira o fundo com IA local gratuita (BiRefNet) e gera a peça flutuando para a loja (4:5), o feed, o catálogo e o story, além do PNG transparente;
   - **efeitos sem custo:** `python3 .claude/skills/estudio-criativo-modestino/efeitos.py flutuar|cores|zoom <recorte.png> ...` (vídeo 9:16 em loop, sem áudio);
   - **IA paga por uso:** `python3 .claude/skills/estudio-criativo-modestino/ia.py imagem manequim|passar|estudio|cena|esticada|cor <foto>` e `ia.py video giro360|flutuar|esticar|vestir|cair <foto>`. Usa a fal.ai com a chave `FAL_KEY`; `--pro` dá mais fidelidade em detalhe e letra;
   - **artes com texto** (capa, carrossel, story): JSON a partir de `loja/estudio/modelos/` → `node .claude/skills/estudio-criativo-modestino/arte.js <peca>.json`;
   - **Reels de gente real:** `reel.py` (cortes, cor, fechamento); edição fina no `reels-capcut-modestino`;
   - **links:** `utm.py <campanha> --peca <nome> --destino <caminho>`.
5. **Revisar** com o checklist de `padroes.md` olhando a folha de prévia (`*-previa.png`) e a folha de quadros do Reel (`*-quadros.png`). Rodar `python3 .claude/skills/loja-lancamento-modestino/vitrine.py` nos textos de legenda quando tiverem preço ou produto. Corrigir antes de mostrar; listar o que foi corrigido.
6. **Apresentar ao Jorge**: prévias, legendas, link UTM de cada peça, dia e horário. Após o ok: `agendar-post-modestino`.
7. **Registrar** em `calendario.md` (data, peça, pilar, objetivo, link) e, na semana seguinte, o resultado. Peça que venceu volta em 3 a 4 semanas com capa nova; Reel que venceu vira anúncio pelo `trafego-pago-modestino`.

## Ferramentas e conectores (custo-benefício, 28/10/2026)

O estúdio roda com ferramentas próprias. Conector é complemento, não dependência.

| necessidade | primeira escolha | custo | alternativa |
| --- | --- | --- | --- |
| tirar o fundo | `recorte.py` (BiRefNet local, código aberto MIT) | zero | Photoroom |
| manequim invisível, passar, cenário, flat lay | `ia.py imagem` (Nano Banana na fal.ai) | ~US$ 0,04 por imagem (Pro ~US$ 0,15) | Photoroom Pro ou Max (assinatura) |
| vídeo 360°, vestir, esticar, cair | `ia.py video` (Kling 2.6 Pro na fal.ai) | ~US$ 0,07/s, ~US$ 0,35 por 5 s | Photoroom (créditos), Higgsfield |
| flutuar, troca de cor, zoom | `efeitos.py` | zero | CapCut |
| artes com texto | `arte.js` | zero | Canva |
| números | Metricool (marca `7230036`) e Shopify | já pagos | — |

Lote semanal típico: 10 imagens de IA e 4 vídeos de 5 s, cerca de US$ 2 a 3. Os preços mudam: conferir em fal.ai/pricing.

- **Chave da fal.ai:** o Jorge cria em fal.ai (Dashboard → API Keys) e guarda como segredo `FAL_KEY` do ambiente, nunca no repositório.
- **Recorte local:** precisa de `pip install "rembg[cpu]"` e baixa o modelo de ~1 GB no primeiro uso. Em ambiente novo, pôr isso no script de preparação.
- **Photoroom (conector):** a conta atual não roda o manequim invisível (exige plano pago) e ficou sem créditos para vídeo. Só vale assinar se o Jorge preferir editar no app.
- **Google Drive, Metricool:** distribuição e agenda (`agendar-post-modestino`).

## Inovar com método

- Uma hipótese nova por semana, escrita antes ("Reel de detalhe com texto em pergunta vai ter mais envios que o de fit check") e conferida depois. Formato que perde 3 semanas seguidas sai da mistura.
- Use **Trial Reels** (Reels de teste mostrados só a quem não segue) para testar gancho e formato sem gastar o feed; o que passar vai para o perfil.
- Peça de colaboração (convite de "Collab" com embaixador, academia ou parceiro de Fortaleza) quando houver gente real vestindo: foi o formato que mais alcançou (Reel do treino, 16/10).
- Fonte de ideia: comentários e directs reais, perguntas do WhatsApp, devoluções e trocas. Toda dúvida repetida vira peça.

## Como responder

Curto, em português, tom de diretor de criação. Diga: o objetivo do lote em uma linha, a tabela das peças (dia, formato, pilar, gancho, objetivo, CTA), as prévias e o que falta do Jorge (material, aprovação). Na leitura semanal: o vencedor, o perdedor, a hipótese da semana e uma decisão.
