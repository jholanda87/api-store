---
name: loja-teste-modestino
description: "Use quando Jorge pedir para testar a loja virtual da Modestino, achar erro, conferir se a compra funciona no celular, ou antes de publicar qualquer mudança na loja: monta o plano de testes dos fluxos de compra, roda o que der automaticamente e registra os erros por gravidade."
---

# Testes da loja (Replica adaptada)

Versão Modestino do `replica-test`. Lê os fluxos de `loja/recon.md`. Escreve `loja/test-plan.md` e `loja/bugs.md` (modelos em `.claude/skills/replica-test/`).

**A regra:** testar a nossa loja, nunca a dos outros. Nada de robô ou carga contra o site de referência.

## Passo 1: o plano

Para cada fluxo (F01 compra avulsa, F02 kit, F03 cupom de embaixador, F04 troca, F05 vindo do Instagram, F06 vindo do WhatsApp):

- **Caminho feliz:** os passos e o que o cliente vê no fim.
- **Bordas:** tamanho esgotado no meio da compra; última peça comprada em duas abas; duplo clique em "pagar"; voltar e atualizar no checkout; CEP inválido e fora de Fortaleza; Pix expirado; nome com acento e emoji; endereço longo; celular 390 px; só teclado; leitor de tela no seletor de tamanho.
- **Negativos:** cartão recusado (cartão de teste do gateway), cupom inválido, cupom de embaixador no kit (deve recusar com explicação), estoque zerado.
- **Regras da casa:** preço igual à tabela da Central; desconto nunca derruba a margem abaixo de 50%; o pedido aparece certo no Painel (`financeiro-modestino`) e o estoque baixa (`estoque.py`).

Numere: F01-H1, F01-E3, F03-N2.

## Passo 2: automatizar

Playwright (Chromium já instalado no ambiente; não rodar `playwright install`), um teste por fluxo, contra a loja em modo teste. Seletores por papel e rótulo (`getByRole('button', { name: 'Comprar' })`), nunca por classe. Em todo teste: falhar com erro no console, com resposta 5xx e com falha de acessibilidade (`@axe-core/playwright`). Exemplo base em `.claude/skills/replica-test/e2e.example.spec.ts`.

## Passo 3: o que não dá para automatizar

Pix real de R$ 1 (Jorge paga e estorna), e-mail chegando, rastreio, catálogo do Instagram, botão do WhatsApp, visual no iPhone do Jorge. Entregue a lista para ele e espere as respostas.

## Passo 4: registrar

| | quer dizer |
| --- | --- |
| S1 | dinheiro errado, pedido perdido, dado de cliente exposto, compra bloqueada |
| S2 | recurso quebrado sem saída |
| S3 | quebrado com saída, ou visivelmente errado |
| S4 | cosmético |

Só entra o que foi reproduzido; "talvez" vai para a lista "conferir".

## Passo 5: corrigir

S1 e S2 primeiro. Para cada: teste que falha → correção → teste passa → teste fica. Rodar tudo de novo a cada lote.

## Saída

Plano, testes, `bugs.md` e resumo: casos rodados, passaram, falharam, erros por gravidade, corrigidos. Nada vai ao ar com S1 aberto. Próxima: `loja-paridade-modestino`.

## Fora deste repositório

Instalada pelo Claude.ai (arquivo .zip), as ferramentas citadas acima vêm dentro da própria pasta desta habilidade, ao lado deste SKILL.md: troque `.claude/skills/<pasta>/` pelo caminho desta pasta. Sem Python disponível, siga o método à mão; ele funciona igual.
