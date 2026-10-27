---
name: pos-venda-modestino
description: "Use quando Jorge pedir as mensagens automáticas da loja virtual da Modestino (pedido confirmado, Pix pendente, enviado, entregue, carrinho abandonado, avaliação, recompra, avise-me) ou a régua de relacionamento do cliente depois da compra: escreve e organiza a régua no tom da marca."
---

# Pós-venda e régua automática da loja

O setor "Pós-venda" que a Central (seção 15) deixou "a criar". `atendimento-modestino` escreve as mensagens 1 a 1 que Jorge envia; esta habilidade monta **o que a loja manda sozinha** e a régua inteira. Toda régua nova passa pelo ok do Jorge antes de ser ligada.

## A régua (e-mail e, quando houver ferramenta, WhatsApp)

| quando | mensagem | objetivo |
| --- | --- | --- |
| na hora | pedido recebido / Pix pendente com o copia-e-cola e o prazo | pagar |
| Pix vence em 30 min | lembrete único, gentil | pagar |
| pago | confirmado, quem separa e quando sai | confiança |
| enviado | rastreio ou "chega hoje em Fortaleza" com a janela | ansiedade zero |
| entregue + 2 a 3 dias | como foi o primeiro uso; nenhuma oferta | relação |
| entregue + 7 dias | pedido de avaliação com foto (ajuda a marca pequena) | prova real |
| entregue + 30 a 45 dias | outra cor ou o kit, sem pressão | recompra (meta ≥ 25% em 60 dias) |
| carrinho abandonado + 1 h | "ficou alguma dúvida?" + guia de tamanho + WhatsApp | recuperar |
| carrinho abandonado + 24 h | lembrete com a troca fácil; **sem desconto** | recuperar sem treinar o cliente a esperar cupom |
| tamanho esgotado | avise-me quando voltar | não perder a venda |

## Regras

- Tom: humano, direto, frases curtas, sem "prezado", sem emoji em excesso. Educar antes de vender.
- Preço e kit da tabela da Central; cupom de embaixador nunca no kit.
- **Avaliação é real ou não existe.** Nunca escrever, editar o sentido ou filtrar só as boas para parecer nota maior. Com permissão do cliente, a foto pode ir para o Instagram.
- Opt-out em todo e-mail de relacionamento; WhatsApp só para quem deu o número para isso (LGPD).
- Troca: 7 dias arrependimento com reembolso total inclusive frete; 30 dias tamanho e defeito; em Fortaleza, troca em mãos. Peça que volta entra no estoque pelo Painel (`moves`/ajuste com o Jorge).

## Passo a passo

1. Confira na plataforma quais gatilhos ela tem nativos (Shopify: e-mails de pedido e carrinho abandonado; régua extra por app). Escreva só o que ela permite ligar; o resto vira tarefa do `atendimento-modestino`.
2. Escreva cada mensagem (assunto + corpo curto + uma ação), no padrão visual da marca (linho/carvão, Instrument Serif no título, Cavalheiro no rodapé).
3. Revise o texto com `loja-lancamento-modestino/vitrine.py` (canal `whatsapp` para mensagens curtas).
4. Mostre a régua inteira ao Jorge numa tabela; ligue só depois do ok.
5. Todo mês: taxa de abertura, carrinhos recuperados (quantos e R$), avaliações recebidas, recompra em 60 dias. Números do placar entram no `bsc` do Painel pela `diretoria-semanal-modestino`.

## Como responder

A régua em tabela (quando, canal, assunto, texto) e o que precisa ser ligado na plataforma. Depois dos dados: o número de recuperação e uma melhoria.
