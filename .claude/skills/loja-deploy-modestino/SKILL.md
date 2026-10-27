---
name: loja-deploy-modestino
description: "Use quando Jorge pedir para colocar a loja virtual da Modestino no ar, ligar o domínio, sair do modo teste ou publicar a loja: roda a checagem final (testes, paridade, varredura da marca, anúncios, páginas legais), passa o passo a passo de domínio e pagamento real, e só publica com o ok dele."
---

# Loja no ar (Replica adaptada)

Versão Modestino do `replica-deploy`. Lê tudo em `loja/`. Escreve `loja/deploy.md` (o checklist de `.claude/skills/replica-deploy/preflight.md`, preenchido).

## As regras

- **Nada vai ao ar sem o "pode" do Jorge.** Mostre a checagem e pergunte.
- **Jorge compra e entra nas contas.** Claude nunca compra domínio, nunca digita cartão, senha ou chave real. Claude escreve os registros DNS, os nomes das configurações e o caminho de cada tela.
- **Sem CNPJ não abre checkout público** (portão da `maquina-vendas-modestino`).

## Passo 1: checagem final (cada falha para tudo)

```bash
npx playwright test                                                          # loja-teste-modestino
python3 .claude/skills/replica-diff/parity.py loja/features.csv              # todos os must
python3 .claude/skills/replica-brand/sweep.py <pasta da loja> --config loja/marca.json   # saída 0
python3 .claude/skills/loja-lancamento-modestino/vitrine.py loja/lancamento/anuncios.json
python3 .claude/skills/catalogo-modestino/estoque.py state.json              # nada negativo
python3 .claude/skills/replica-design/contrast.py loja/design/tokens.json
```

À mão: nenhum S1/S2 aberto; política de troca, privacidade e termos publicadas (`administrativo-modestino`); CNPJ e razão social no rodapé; favicon, títulos e imagem de compartilhamento da Modestino; estoque da loja = Painel; preço = Central.

## Passo 2: produção

- Pagamento em modo real: Jorge troca as chaves; uma compra real de R$ 1 (ou produto oculto) por Pix e uma por cartão, e estorno das duas.
- Webhooks apontando para a loja de produção.
- E-mail de envio verificado no domínio.
- Admin com 2 fatores para Jorge e Lucas.

## Passo 3: domínio

Depois que Jorge registrar (registro.br para .com.br), na plataforma escolhida:

| registro | nome | valor |
| --- | --- | --- |
| A | @ | o IP que a plataforma mostra (Shopify mostra na tela de domínios) |
| CNAME | www | o destino da plataforma (Shopify: `shops.myshopify.com`) |
| TXT | @ | verificação, se pedir |

E-mail: SPF, DKIM e DMARC começando em `v=DMARC1; p=none; rua=mailto:<email da loja>`, apertando para `quarantine` quando os relatórios vierem limpos. Escolha um endereço principal (com ou sem www) e redirecione o outro. Confirme o HTTPS.

## Passo 4: acompanhar

Alerta de pedido e de erro no celular dos dois; Analytics e pixel conferidos com uma compra de teste; Jorge faz uma compra pelo próprio celular, do post até o pedido. Na primeira semana: pedidos, conversão, carrinhos abandonados, perguntas mais feitas no WhatsApp (viram FAQ).

## Saída

`loja/deploy.md` com cada checagem e o resultado, a URL no ar, os DNS feitos e o que olhar na primeira semana. Atualize a Central (seção 5, fase 8 E-commerce; seção 9, canais) e `loja/estado.md`.

## Fora deste repositório

Instalada pelo Claude.ai (arquivo .zip), as ferramentas citadas acima vêm dentro da própria pasta desta habilidade, ao lado deste SKILL.md: troque `.claude/skills/<pasta>/` pelo caminho desta pasta. Sem Python disponível, siga o método à mão; ele funciona igual.
