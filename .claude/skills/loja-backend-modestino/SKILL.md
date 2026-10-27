---
name: loja-backend-modestino
description: "Use quando Jorge pedir para ligar pagamento (Pix, cartão), frete, nota fiscal, e-mails, pixel da Meta, Google, WhatsApp ou a ligação loja ↔ Painel na loja virtual da Modestino: configura as integrações com as contas e chaves dele, com checklist de segurança."
---

# Pagamento, frete e integrações (Replica adaptada)

Versão Modestino do `replica-backend`. Lê `loja/arquitetura.md` e mantém `loja/backend.md` com o checklist abaixo.

## As regras

- **Só APIs oficiais, com as chaves do Jorge.** Nada de API escondida de outra loja.
- **Jorge cria as contas e as chaves.** Claude nunca se cadastra, nunca digita senha, cartão nem chave de produção. Claude escreve a lista do que criar e onde colar (`.env.example` sem valores, ou o passo a passo na tela da plataforma).
- **Modo teste primeiro.** Pagamento em sandbox até `loja-deploy-modestino`.

## Pagamento

- Pix (com QR e copia-e-cola, prazo de expiração definido) e cartão em até 3x com os juros repassados (Central seção 8). Gateway: o da plataforma escolhida (Shopify Payments se disponível; senão Mercado Pago ou Pagar.me). Não construir formulário de cartão.
- Webhook: assinatura verificada, id do evento guardado, cada tratamento idempotente (chega duas vezes). Pedido só vira "pago" pelo webhook, nunca pelo navegador.
- Taxa do gateway vira custo separado no Painel (categoria `taxas`), a venda fica com o valor bruto — regra da `financeiro-modestino`.
- Cancelamento e estorno simples e no prazo: desistência em 7 dias com reembolso total, inclusive do frete (CDC art. 49).

## Frete

- Fortaleza: entrega própria/Uber Flash com tabela por bairro ou preço fixo; opção "retirar/trocar em mãos" como diferencial.
- Fora: Correios/transportadora por app de cotação (Melhor Envio, Frenet ou o da plataforma), com etiqueta e rastreio automáticos.
- Peso e medidas por produto e por kit (pese a ecobag com 3 peças).

## Ligação com o Painel (a regra "tudo num lugar só")

- **Loja → Painel:** cada pedido pago vira uma venda em `sales[]` (cliente, linhas cor/tamanho/lote, preço, recebido, método, cupom → `seller`) pela habilidade `financeiro-modestino`, no mesmo dia. Se houver conector (Shopify `list-orders`), puxe dele; senão, Jorge manda o resumo.
- **Painel → Loja:** estoque com `catalogo-modestino/estoque.py`.
- O caixa do Painel deve bater com o repasse do gateway; diferença vira pergunta.

## Medição

Pixel da Meta + API de conversões (eventos ViewContent, AddToCart, InitiateCheckout, Purchase com valor), Google Analytics 4 + Merchant Center, UTMs padrão (`utm_source=instagram&utm_medium=bio|post|stories|ads&utm_campaign=<tema>`) e cupom por embaixador para atribuir venda.

## E-mail e WhatsApp

Confirmação de pedido, Pix pendente, pago, enviado (com rastreio), entregue. Do domínio da marca quando houver. Texto novo, no tom da marca (`pos-venda-modestino` escreve).

## Nota fiscal

Só depois do CNPJ (`administrativo-modestino`). Emissor ligado à plataforma, emitindo na confirmação do pagamento.

## Checklist de segurança

- [ ] chaves só em variáveis de ambiente/configuração da plataforma; nada em código ou print
- [ ] webhooks com assinatura verificada
- [ ] dado de cliente fora de URL e de log; só o necessário (LGPD)
- [ ] política de privacidade lista cada processador (plataforma, gateway, frete, e-mail, Meta, Google)
- [ ] acesso de admin da loja com 2 fatores para Jorge e Lucas
- [ ] backup/exportação de pedidos e clientes mensal

## Saída

Pagamento em teste, frete, e-mails, medição e ligação com o Painel funcionando, `loja/backend.md` com o checklist marcado e `features.csv` atualizado. Próxima: `loja-teste-modestino`.
