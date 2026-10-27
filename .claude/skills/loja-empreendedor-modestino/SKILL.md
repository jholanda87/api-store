---
name: loja-empreendedor-modestino
description: "Use quando Jorge perguntar o que os clientes odeiam nas marcas de camiseta básica, como a Modestino pode vender mais que a concorrência, qual o diferencial ou o posicionamento da loja: lê avaliações públicas reais (Reclame Aqui, Google, Mercado Livre, Instagram) e vira lista de correções e um ângulo de venda."
---

# O Empreendedor da Modestino

Versão Modestino do `replica-entrepreneur`, a habilidade que o vídeo destaca: "lê o que os usuários odeiam e corrige isso na sua". Uma cópia da Insider não tem motivo para existir. Esta habilidade acha o motivo, nas palavras dos próprios clientes das referências.

Ferramenta (da Replica, com temas em português da Modestino):

```bash
python3 .claude/skills/replica-entrepreneur/reviews.py loja/reviews.csv \
  --themes .claude/skills/loja-empreendedor-modestino/temas.json --out loja/feedback.md
```

## As regras, inegociáveis

- **Nunca inventar.** Nenhuma avaliação, frase, nota, contagem ou fonte inventada. Se a fonte não abre, diga e siga. Se há 14 avaliações, diga 14.
- **Toda frase é literal e tem link.** O `reviews.py` descarta linha sem link.
- **Ler, não raspar.** Navegador, como uma pessoa, copiando para a planilha.
- **Nunca avaliação falsa,** nem para a Modestino nem contra os outros. É crime pelo CDC e propaganda enganosa.
- **Cliente dos outros não é depoimento nosso.** As frases são pesquisa e nunca vão para a página da loja.

## Passo 1: coletar (meta: 100+ avaliações, 3+ fontes, recentes primeiro)

| fonte | onde |
| --- | --- |
| Reclame Aqui | página da empresa, reclamações recentes e as respondidas |
| Google | avaliações da loja física e do perfil da empresa |
| Mercado Livre / Shopee | perguntas e opiniões dos anúncios de camiseta básica das referências |
| Instagram | comentários com reclamação nos posts e anúncios das referências |
| Reddit / fóruns BR | "camiseta básica boa", "vale a pena", "desbotou" |
| política de troca e FAQ | o que a marca já resolve, para não "corrigir" o que já está certo |

Cada linha de `loja/reviews.csv`: `source,url,date,rating,text`, texto copiado exato. Leia também as 3 e 4 estrelas: "gostei, mas…" é onde moram as melhores correções.

## Passo 2: ranquear

Rode o comando acima. Ele agrupa por tema (tamanho, tecido, durabilidade, entrega, troca, atendimento, diferente da foto, preço, site, logo grande, embalagem, grade), pesa nota baixa e avaliação recente, marca como fraco o tema com menos de 3 avaliações ou de uma fonte só, e lista as avaliações negativas sem tema. Leia essa última lista à mão: costuma ser a melhor parte. Se aparecer um tema novo com força, acrescente em `temas.json`.

## Passo 3: três listas

1. **O que odeiam** (o que a marca faz mal).
2. **O que falta** (o que pedem pelo nome).
3. **O que ninguém resolve** (um público ou uma situação ignorada, ex.: "camiseta para o calor de Fortaleza", "homem grande que não acha GG que caia bem").

Cada item: o problema em uma linha, quantas avaliações, quantas fontes, 1 ou 2 frases com link. Tema fraco fica marcado como fraco.

## Passo 4: plano de correções

Escolha de 5 a 8 por evidência × custo de corrigir. Para cada: o que fazer na loja ou na operação, tamanho (P, M, G), qual habilidade faz, e a evidência. Acrescente cada uma em `loja/features.csv` com `original = no`. Exemplos do tipo de correção que a Modestino já tem na mão, a confirmar com dados: calculadora de tamanho pela camiseta que o cliente já tem; troca de tamanho em mãos em Fortaleza; atendimento humano em até 10 min no WhatsApp; foto real de perto das 3 cores; camiseta lisa sem logo. **Só vira promessa o que foi testado** (lavagem, cor, calor).

Reclamação de preço e frete vai para `loja-lancamento-modestino`. Reclamação de troca e atendimento vai também para `pos-venda-modestino` e `atendimento-modestino`.

## Passo 5: o ângulo

Três opções, cada uma presa a um tema forte:

```
Para {quem} que {odeia isto nas outras marcas, em palavras simples},
a Modestino {faz isto no lugar}.
Evidência: {tema}, {n} avaliações em {n} fontes.
```

Recomende uma. Ela guia o título da página inicial, os anúncios e a legenda fixa. Nunca use o nome de outra marca nos nossos textos e anúncios; comparação nominal é assunto de advogado.

## Saída

`loja/reviews.csv`, `loja/feedback.md`, `loja/correcoes.md` (3 listas, plano, ângulo), linhas novas em `features.csv` e um resumo que diz o tamanho da amostra. Registre o ângulo escolhido na Central (seção 10) depois do ok do Jorge. Próxima etapa: `loja-arquitetura-modestino`.

## Fora deste repositório

Instalada pelo Claude.ai (arquivo .zip), as ferramentas citadas acima vêm dentro da própria pasta desta habilidade, ao lado deste SKILL.md: troque `.claude/skills/<pasta>/` pelo caminho desta pasta. Sem Python disponível, siga o método à mão; ele funciona igual.
