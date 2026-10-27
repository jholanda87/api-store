---
name: loja-marca-modestino
description: "Use antes de publicar a loja virtual da Modestino ou qualquer mudança grande nela, ou quando Jorge pedir para conferir se sobrou algo de outra marca ou da identidade antiga: varre o código e os textos da loja, confere logo, favicon, voz e os textos mais vistos."
---

# Marca da loja (Replica adaptada)

Na Replica, o `replica-brand` dá nome e marca nova ao clone. A Modestino já tem nome (decidido, INPI classes 25 e 35 sem conflito em set/2026) e identidade (O Cavalheiro, 14/10/2026). Então esta etapa é **a linha entre "inspirado nas referências" e "loja da Modestino"**: nada de outra marca e nada da identidade antiga pode sobrar.

Ferramenta da Replica, com a lista da Modestino:

```bash
python3 .claude/skills/replica-brand/sweep.py <pasta do código da loja> --config loja/marca.json
```

`loja/marca.json` lista as referências (Insider, Reserva, Hering, Básico.com, Shein, Ricardo Almeida, Mirante), a Wolf (loja antiga do Jorge), a fonte antiga (Poppins) e os domínios. A paleta aprovada é a do mockup, dos posts e do logo atual: neutra e minimalista, puxada para o bege, nude e algodão cru (linho, areia, mapple, carvão, grafite). Qualquer cor viva ou fora dos tokens é sobra: além do sweep, liste os hex do código da loja (`grep -rhoiE '#[0-9a-f]{6}\b' <pasta>`) e compare com `loja/design/tokens.json`; o que não estiver lá sai. Rode só na pasta do código/tema da loja, nunca na raiz do repositório (as habilidades citam as referências de propósito). Saída 1 = sobrou algo; corrija até dar limpo.

## Passo 1: nome e registro (conferir, não presumir)

| checagem | onde | situação |
| --- | --- | --- |
| INPI classes 25 e 35 | busca.inpi.gov.br | sem conflito (set/2026); **pedido de registro depende do CNPJ** |
| domínio | registro.br (modestino.com.br) e .com | a rodar |
| @ | Instagram @lojamodestino ativo; TikTok, Mercado Livre, Shopee | a rodar |

Nunca escreva "disponível" para checagem que ninguém rodou. Isto é triagem, não parecer jurídico.

## Passo 2: paleta e contraste

Tokens em `loja/design/tokens.json`. A cada mudança: `python3 .claude/skills/replica-design/contrast.py loja/design/tokens.json`, zero falha AA.

## Passo 3: logo e ícones

- Cabeçalho: O Cavalheiro + MODESTINO (Instrument Sans 600 espaçado). Pequeno: busto ou cartola + nome.
- Favicon 16/32 px (busto ou cartola), ícone 512 px, imagem de compartilhamento 1200×630 (linho ou carvão, Cavalheiro + frase do ângulo).
- Arquivo SVG do desenho do Jorge; se só existir PNG, vetorizar (conector Adobe `image_vectorize`) e mostrar para ele aprovar antes de usar.

## Passo 4: voz

Três palavras: **humano** (não informal demais), **direto** (não seco), **educador** (não professor). Reescreva os 10 textos mais vistos da loja nessa voz: botão de compra, carrinho vazio, frete, erro de CEP, cupom recusado no kit, Pix pendente, pedido confirmado, esgotado/avise-me, troca, rodapé. Nenhum ecoando frase de referência. Sem emoji em excesso, sem "prezado", sem tom de coach.

## Passo 5: varredura e olho

Rode o `sweep.py` até dar limpo. Depois confira a olho: favicon, títulos das páginas, e-mails, imagem de compartilhamento, catálogo do Instagram, nota fiscal (razão social certa).

## Saída

Varredura limpa, `loja/marca.json` atualizado, os 10 textos reescritos em `loja/voz.md`. Próxima: `loja-lancamento-modestino`.

## Fora deste repositório

Instalada pelo Claude.ai (arquivo .zip), as ferramentas citadas acima vêm dentro da própria pasta desta habilidade, ao lado deste SKILL.md: troque `.claude/skills/<pasta>/` pelo caminho desta pasta. Sem Python disponível, siga o método à mão; ele funciona igual.
