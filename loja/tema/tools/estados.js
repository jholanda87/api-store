// Prints dos estados (calculadora, esgotado, últimas peças, erro do kit, menu do celular) na prévia local.
const { chromium } = require('playwright');
const path = require('path');
const out = path.resolve(__dirname, '../../clone-screens');
const U = 'http://localhost:8765/';
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 390, height: 844 } });
  const erros = []; p.on('pageerror', (e) => erros.push(String(e)));
  // Produto: Preto GG esgotado, Preto G com 2 peças; calculadora com 57 cm (G) e com 80 cm (erro)
  await p.goto(U + 'produto-esgotado.html');
  await p.click('summary:has-text("Não sabe o tamanho")');
  await p.fill('[data-calc]', '80'); await p.click('[data-calc-ok]');
  await p.locator('.m-calc').screenshot({ path: path.join(out, 'S04-calculadora-erro-390.png') });
  await p.fill('[data-calc]', '57'); await p.click('[data-calc-ok]');
  await p.locator('.m-info').screenshot({ path: path.join(out, 'S03-esgotado-ultimas-calculadora-390.png') });
  console.log('calc:', await p.textContent('[data-calc-res]'));
  console.log('aviso:', await p.textContent('[data-aviso]'));
  console.log('botao:', await p.textContent('[data-comprar]'));
  await p.click('label[data-cor="Mapple Brown"]');
  console.log('galeria cor:', await p.getAttribute('[data-galeria]', 'data-cor'), 'fotos visiveis:', await p.locator('[data-cor-foto]:not([hidden])').count());
  await p.screenshot({ path: path.join(out, 'S03-troca-cor-390.png') });
  // Kit: enviar sem escolher, depois repetir combinação além do estoque
  await p.goto(U + 'kit-3.html');
  await p.click('[data-comprar]');
  console.log('kit vazio:', await p.textContent('[data-erro]'));
  for (const i of [1, 2, 3]) { await p.selectOption(`#kc-main-${i}`, 'Preto'); await p.selectOption(`#kt-main-${i}`, 'GG'); }
  console.log('kit ok (GG preto x3, estoque 9):', await p.isHidden('[data-erro]'));
  await p.locator('.m-pecas').screenshot({ path: path.join(out, 'S05-kit-pecas-390.png') });
  await p.goto(U + 'kit-3-esgotado.html');
  await p.selectOption('#kc-main-1', 'Preto'); await p.selectOption('#kt-main-1', 'GG');
  console.log('kit esgotado:', await p.textContent('[data-erro]'), '| botão:', await p.textContent('[data-comprar]'));
  await p.locator('.m-info').screenshot({ path: path.join(out, 'S05-kit-esgotado-390.png') });
  // Menu do celular
  await p.goto(U + 'inicio.html');
  await p.click('.m-gaveta summary');
  await p.screenshot({ path: path.join(out, 'menu-celular-390.png') });
  const W = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  console.log('menu aberto, rolagem lateral:', W, 'erros:', erros);
  await b.close();
})();
