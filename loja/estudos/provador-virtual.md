# Provador virtual Modestino — estudo (16/11/2026)

## Caminhos
1. Foto + IA (recomendado). Cliente manda/tira foto de frente; uma IA de "virtual try-on" veste a camiseta escolhida.
   - APIs: Google Vertex AI Virtual Try-On (~US$0,06/imagem), FASHN (~US$0,075/imagem; versão Max mais cara), opções no fal.ai (US$0,04–0,10).
   - Apps Shopify prontos: TryOn Virtual (grátis até 50/mês), Try It On (US$0,10 por prova), Wearbly, TryItOn etc. (US$19–49/mês). Funcionam na página do produto, não no Monte a sua.
2. Câmera ao vivo (AR). Overlay 2D com MediaPipe parece adesivo, não roupa. IA em tempo real (Decart/Anywear) cobra por segundo e ainda é nova. Não recomendado agora.
3. Híbrido (proposta): câmera com silhueta, checagem de luz e foto automática → manda para o caminho 1.

## Limites
- Foto de frente só mostra a arte do peito; arte das costas exige foto de costas.
- Selos pequenos (7 cm) podem sair deformados pela IA — testar antes.
- Chave da API não pode ficar no tema: precisa de um servidor pequeno (Cloudflare Worker/Vercel) ou app.
- LGPD: consentimento antes, não guardar a foto, apagar após gerar, citar na Privacidade.

## Custo estimado
500 provas/mês × ~R$0,40 ≈ R$200/mês (+ limite de 3 provas por pessoa/dia).

## Plano
1. Teste de 1 semana com um app Shopify grátis em 3 produtos (inclui um selo) — avaliar fidelidade da arte.
2. Se aprovar: construir o provador dentro do Monte a sua (câmera guiada + foto), com API própria.
