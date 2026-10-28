---
name: maquina-vendas-modestino
description: "Use quando Jorge pedir a loja virtual, o e-commerce, a máquina de vendas da Modestino ou \"em que pé está a loja\": mostra a etapa atual, chama a próxima habilidade na ordem certa e mede o funil de vendas online."
---

# Máquina de vendas da Modestino (o maestro)

A loja virtual da Modestino é montada com o método da Replica (github.com/Jakeschincariol/replica-skill, MIT): mapear o que as lojas de referência fazem, ler o que os clientes delas odeiam, corrigir isso na nossa, aplicar a nossa marca, lançar e pôr no ar. A Replica clona aplicativos; aqui o "aplicativo" é a experiência de compra de uma loja de básicos masculinos. **Copiamos o que a loja faz, nunca o que ela tem:** nada de texto, foto, logo, código ou cor das referências.

Esta habilidade não constrói nada sozinha. Ela sabe a ordem, lê o estado e chama a habilidade certa.

## Onde fica cada coisa

- `loja/estado.md` — a tabela de etapas, atualizada ao fim de cada uma.
- `loja/` — tudo que as etapas escrevem (como a pasta `replica/` da Replica).
- Ferramentas Python da Replica em `.claude/skills/replica-*/` e as da Modestino em `.claude/skills/*-modestino/`.
- Números (vendas, estoque, caixa, metas): Painel da Modestino, `data/state.json` (https://claude.ai/code/artifact/a01898d2-619b-47f4-a7fe-3d585a03f95a). Estratégia e decisões: Central Modestino (https://claude.ai/code/artifact/aae517c7-5468-4a01-b254-7d6acdd14dce).

## A ordem

```
administrativo → recon → empreendedor → arquitetura → design → catálogo → build
→ backend → teste → paridade → marca → lançamento → deploy
→ (no ar) estúdio criativo + tráfego pago + pós-venda + funil semanal
```

| etapa | habilidade | entra | sai |
| --- | --- | --- | --- |
| 0 | administrativo-modestino | situação do CNPJ | checklist legal, políticas |
| 1 | loja-recon-modestino | lojas de referência | `recon.md`, `features.csv` |
| 2 | loja-empreendedor-modestino | avaliações públicas reais | `feedback.md`, `correcoes.md`, ângulo |
| 3 | loja-arquitetura-modestino | recon + correções | plataforma, catálogo, integrações |
| 4 | loja-design-modestino | identidade oficial | `design/tokens.json`, componentes |
| 5 | catalogo-modestino | Painel + fotos | produtos, variantes, estoque |
| 6 | loja-build-modestino | tudo acima | páginas prontas |
| 7 | loja-backend-modestino | arquitetura | Pix, cartão, frete, e-mails, pixel |
| 8 | loja-teste-modestino | fluxos do recon | `test-plan.md`, `bugs.md` |
| 9 | loja-paridade-modestino | `features.csv` | nota e o que falta |
| 10 | loja-marca-modestino | `marca.json` | varredura limpa |
| 11 | loja-lancamento-modestino | ângulo + marca | textos, anúncios revisados, plano |
| 12 | loja-deploy-modestino | tudo | loja no ar com o ok do Jorge |
| 13 | estudio-criativo-modestino | fotos e vídeos reais, Metricool, UTM da loja | estratégia, padrões, lotes de conteúdo, vitrine, leitura semanal |

Pode rodar uma etapa sozinha. `loja-empreendedor-modestino` antes de tudo é a melhor forma de descobrir o que a loja precisa ter para vender mais que as referências.

## Os portões (não pular)

- **Sem CNPJ, sem checkout público.** A Central diz que o e-commerce depende do CNPJ. Antes disso dá para construir, testar e vender por link de pagamento/Direct, mas não abrir loja com nota, marketplace nem registro.
- **Sinal de escala da Central:** loja própria é a etapa 2, quando a 1ª leva girar (150+ peças). Se Jorge quiser antecipar, registre a decisão na Central (seção 10).
- **Nada é contratado, publicado ou enviado sem o ok do Jorge.** Claude não cria conta, não digita senha, cartão nem chave.
- **No máximo 3 opções por decisão,** com uma recomendada, e cobrar a escolha na mesma semana.

## O funil (depois que a loja estiver no ar)

Toda segunda, junto com `diretoria-semanal-modestino`, escreva `loja/funil.md` com: visitas, adição ao carrinho, checkout iniciado, pedidos, taxa de conversão, ticket médio, carrinhos recuperados, CAC (gasto em anúncio ÷ pedidos novos), origem dos pedidos (orgânico, anúncio, embaixador, WhatsApp). Puxe da plataforma (conector Shopify se for Shopify) e do Metricool. Número que não veio fica "sem dado", nunca estimado. Aponte o maior vazamento do funil e uma ação para ele.

## Como responder

Curto, em português, tom de consultor. Diga: em que etapa a loja está, o que a próxima etapa entrega, e o que falta do Jorge para andar (no máximo 3 itens). Atualize `loja/estado.md`.
