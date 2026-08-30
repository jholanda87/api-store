// ---------- Data layer ----------
const STORAGE_KEY = 'estudioDesignData';

const SEED_FABRICS = [{
  id: 'seed-starlink-light',
  nome: 'Starlink Light',
  composicao: '95% modal + 5% elastano',
  gramatura: 190,
  largura: 180,
  rendimento: 2.92,
  custoPorKg: 85.00,
  createdAt: Date.now(),
  cores: [
    { id: uidSeed('preto'), nome: 'Preto', hex: '#1a1a1a', estoqueKg: 2836.36 },
    { id: uidSeed('offwhite'), nome: 'Off White', hex: '#efe9dc', estoqueKg: 2824.19 },
    { id: uidSeed('marinho'), nome: 'Marinho', hex: '#262b45', estoqueKg: 1625.16 },
    { id: uidSeed('mapplebrown'), nome: 'Mapple Brown', hex: '#6b4a38', estoqueKg: 497.62 },
    { id: uidSeed('evergreen'), nome: 'Evergreen', hex: '#1f4a41', estoqueKg: 288.25 },
    { id: uidSeed('vinho'), nome: 'Vinho Carmenere', hex: '#5a2430', estoqueKg: 215.77 },
    { id: uidSeed('darkpowder'), nome: 'Dark Powder', hex: '#5c4c46', estoqueKg: 16.99 },
  ],
}];

function uidSeed(tag) { return 'seed-color-' + tag; }

function loadData() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (!parsed.fabrics) parsed.fabrics = JSON.parse(JSON.stringify(SEED_FABRICS));
      if (!parsed.collections) parsed.collections = [];
      if (!parsed.palettes) parsed.palettes = [];
      return parsed;
    }
  } catch (e) { /* ignore corrupted storage */ }
  return { palettes: [], collections: [], fabrics: JSON.parse(JSON.stringify(SEED_FABRICS)) };
}

function saveData() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function uid() {
  return (crypto.randomUUID ? crypto.randomUUID() : 'id-' + Date.now() + '-' + Math.random().toString(16).slice(2));
}

const state = loadData();

// ---------- Color math ----------
function hexToHsl(hex) {
  let r = parseInt(hex.slice(1, 3), 16) / 255;
  let g = parseInt(hex.slice(3, 5), 16) / 255;
  let b = parseInt(hex.slice(5, 7), 16) / 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b);
  let h, s, l = (max + min) / 2;
  if (max === min) { h = s = 0; }
  else {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch (max) {
      case r: h = (g - b) / d + (g < b ? 6 : 0); break;
      case g: h = (b - r) / d + 2; break;
      default: h = (r - g) / d + 4;
    }
    h *= 60;
  }
  return { h, s: s * 100, l: l * 100 };
}

function hslToHex(h, s, l) {
  h = ((h % 360) + 360) % 360;
  s /= 100; l /= 100;
  const c = (1 - Math.abs(2 * l - 1)) * s;
  const x = c * (1 - Math.abs((h / 60) % 2 - 1));
  const m = l - c / 2;
  let r, g, b;
  if (h < 60) [r, g, b] = [c, x, 0];
  else if (h < 120) [r, g, b] = [x, c, 0];
  else if (h < 180) [r, g, b] = [0, c, x];
  else if (h < 240) [r, g, b] = [0, x, c];
  else if (h < 300) [r, g, b] = [x, 0, c];
  else [r, g, b] = [c, 0, x];
  const toHex = (v) => Math.round((v + m) * 255).toString(16).padStart(2, '0');
  return '#' + toHex(r) + toHex(g) + toHex(b);
}

function generatePalette(baseHex, type) {
  const { h, s, l } = hexToHsl(baseHex);
  const clamp = (v, min, max) => Math.min(max, Math.max(min, v));
  switch (type) {
    case 'monocromatica':
      return [20, 38, 55, 72, 88].map(lv => hslToHex(h, clamp(s, 25, 90), lv));
    case 'analoga':
      return [-40, -20, 0, 20, 40].map(dh => hslToHex(h + dh, clamp(s, 30, 85), clamp(l, 35, 65)));
    case 'triadica':
      return [
        hslToHex(h, s, clamp(l, 30, 70)),
        hslToHex(h, clamp(s, 20, 90), clamp(l + 20, 20, 85)),
        hslToHex(h + 120, s, clamp(l, 30, 70)),
        hslToHex(h + 240, s, clamp(l, 30, 70)),
        hslToHex(h + 120, clamp(s, 20, 90), clamp(l + 20, 20, 85)),
      ];
    case 'complementar':
    default:
      return [
        hslToHex(h, s, clamp(l - 15, 15, 85)),
        hslToHex(h, s, clamp(l, 20, 85)),
        hslToHex(h, clamp(s, 15, 60), clamp(l + 25, 30, 92)),
        hslToHex(h + 180, s, clamp(l, 20, 85)),
        hslToHex(h + 180, s, clamp(l - 15, 15, 85)),
      ];
  }
}

// ---------- Pattern generation (SVG) ----------
function patternTileContent(type, colors, s) {
  const c = (i) => colors[i % colors.length];
  switch (type) {
    case 'listras': {
      const n = colors.length;
      const bandH = s / n;
      let bands = '';
      for (let i = 0; i < n; i++) {
        bands += `<rect x="0" y="${i * bandH}" width="${s}" height="${bandH + 0.5}" fill="${c(i)}"/>`;
      }
      return bands;
    }
    case 'poa': {
      return `
        <rect width="${s}" height="${s}" fill="${c(0)}"/>
        <circle cx="${s * 0.25}" cy="${s * 0.25}" r="${s * 0.16}" fill="${c(1)}"/>
        <circle cx="${s * 0.75}" cy="${s * 0.75}" r="${s * 0.16}" fill="${c(1)}"/>
        <circle cx="${s * 0.75}" cy="${s * 0.25}" r="${s * 0.09}" fill="${c(2)}"/>
        <circle cx="${s * 0.25}" cy="${s * 0.75}" r="${s * 0.09}" fill="${c(2)}"/>
      `;
    }
    case 'geometrico': {
      const cx = s / 2, cy = s / 2, r = s * 0.32;
      return `
        <rect width="${s}" height="${s}" fill="${c(0)}"/>
        <polygon points="${cx},${cy - r} ${cx + r},${cy} ${cx},${cy + r} ${cx - r},${cy}" fill="${c(1)}"/>
        <rect x="0" y="0" width="${s * 0.22}" height="${s * 0.22}" fill="${c(2)}"/>
        <rect x="${s * 0.78}" y="0" width="${s * 0.22}" height="${s * 0.22}" fill="${c(2)}"/>
        <rect x="0" y="${s * 0.78}" width="${s * 0.22}" height="${s * 0.22}" fill="${c(2)}"/>
        <rect x="${s * 0.78}" y="${s * 0.78}" width="${s * 0.22}" height="${s * 0.22}" fill="${c(2)}"/>
      `;
    }
    case 'organico':
    default: {
      return `
        <rect width="${s}" height="${s}" fill="${c(0)}"/>
        <ellipse cx="${s * 0.3}" cy="${s * 0.35}" rx="${s * 0.28}" ry="${s * 0.2}" fill="${c(1)}" opacity="0.85" transform="rotate(15 ${s * 0.3} ${s * 0.35})"/>
        <ellipse cx="${s * 0.75}" cy="${s * 0.65}" rx="${s * 0.24}" ry="${s * 0.17}" fill="${c(2)}" opacity="0.85" transform="rotate(-20 ${s * 0.75} ${s * 0.65})"/>
        <ellipse cx="${s * 0.65}" cy="${s * 0.2}" rx="${s * 0.15}" ry="${s * 0.11}" fill="${c(3)}" opacity="0.8" transform="rotate(40 ${s * 0.65} ${s * 0.2})"/>
      `;
    }
  }
}

function buildPatternDefs(patId, type, colors, scale, rotation) {
  const tile = patternTileContent(type, colors, scale);
  return `<pattern id="${patId}" width="${scale}" height="${scale}" patternUnits="userSpaceOnUse" patternTransform="rotate(${rotation} ${scale / 2} ${scale / 2})">${tile}</pattern>`;
}

function fabricSVG(patId, defs, size = 300) {
  return `<svg viewBox="0 0 ${size} ${size}" width="${size}" height="${size}" xmlns="http://www.w3.org/2000/svg">
    <defs>${defs}</defs>
    <rect width="${size}" height="${size}" fill="url(#${patId})" rx="14"/>
  </svg>`;
}

const GARMENT_SHAPES = {
  camiseta: `
    <polygon points="70,80 15,110 35,160 90,130" fill="__FILL__"/>
    <polygon points="230,80 285,110 265,160 210,130" fill="__FILL__"/>
    <rect x="70" y="70" width="160" height="210" rx="18" fill="__FILL__"/>
    <ellipse cx="150" cy="76" rx="26" ry="13" fill="#ffffff"/>
  `,
  vestido: `
    <polygon points="110,65 75,55 65,90 105,105" fill="__FILL__"/>
    <polygon points="190,65 225,55 235,90 195,105" fill="__FILL__"/>
    <rect x="105" y="58" width="90" height="95" rx="10" fill="__FILL__"/>
    <polygon points="100,148 200,148 235,290 65,290" fill="__FILL__"/>
    <ellipse cx="150" cy="60" rx="20" ry="9" fill="#ffffff"/>
  `,
  moletom: `
    <polygon points="65,85 10,120 32,175 88,140" fill="__FILL__"/>
    <polygon points="235,85 290,120 268,175 212,140" fill="__FILL__"/>
    <rect x="65" y="75" width="170" height="215" rx="22" fill="__FILL__"/>
    <path d="M120,80 Q150,120 180,80 L180,95 Q150,135 120,95 Z" fill="__FILL__"/>
    <ellipse cx="150" cy="82" rx="28" ry="14" fill="#ffffff"/>
  `,
  calca: `
    <path d="M95,60 L205,60 L215,150 L235,285 L185,285 L155,165 L145,285 L95,285 L105,150 Z" fill="__FILL__"/>
    <rect x="95" y="55" width="110" height="18" rx="6" fill="__FILL__"/>
  `,
  jaqueta: `
    <polygon points="65,85 10,125 35,180 90,145" fill="__FILL__"/>
    <polygon points="235,85 290,125 265,180 210,145" fill="__FILL__"/>
    <path d="M85,75 L150,90 L215,75 L232,95 L215,290 L150,270 L85,290 L68,95 Z" fill="__FILL__"/>
    <line x1="150" y1="90" x2="150" y2="270" stroke="#ffffff" stroke-width="4"/>
    <ellipse cx="150" cy="80" rx="18" ry="10" fill="#ffffff"/>
  `,
  saia: `
    <rect x="95" y="60" width="110" height="45" rx="8" fill="__FILL__"/>
    <polygon points="95,100 205,100 245,270 55,270" fill="__FILL__"/>
  `,
};

function garmentSVG(patId, defs, garmentType, size = 300) {
  const shape = (GARMENT_SHAPES[garmentType] || GARMENT_SHAPES.camiseta).replace(/__FILL__/g, `url(#${patId})`);
  return `<svg viewBox="0 0 ${size} ${size}" width="${size}" height="${size}" xmlns="http://www.w3.org/2000/svg">
    <defs>${defs}</defs>
    ${shape}
  </svg>`;
}

// ---------- DOM refs ----------
const $ = (sel) => document.querySelector(sel);

const manualColorInput = $('#manualColor');
const manualColorLabelInput = $('#manualColorLabel');
const manualSwatchesEl = $('#manualSwatches');
const manualEmptyHint = $('#manualEmptyHint');
const paletteNameInput = $('#paletteName');
const savedPalettesEl = $('#savedPalettes');

const patternPaletteSelect = $('#patternPalette');
const patternTypeSelect = $('#patternType');
const patternScaleInput = $('#patternScale');
const scaleOut = $('#scaleOut');
const patternRotationInput = $('#patternRotation');
const rotationOut = $('#rotationOut');
const garmentTypeSelect = $('#garmentType');
const pieceNameInput = $('#pieceName');
const pieceYieldInput = $('#pieceYield');
const pieceCostInput = $('#pieceCost');
const piecePriceInput = $('#piecePrice');
const fabricPreviewWrap = $('#fabricPreviewWrap');
const garmentPreviewWrap = $('#garmentPreviewWrap');

const collectionsListEl = $('#collectionsList');
const modalRoot = $('#modalRoot');

const fabricsListEl = $('#fabricsList');
const fabricsTotalValueEl = $('#fabricsTotalValue');
const yieldFabricPickSelect = $('#yieldFabricPick');
const yieldResultCard = $('#yieldResultCard');

let manualColors = []; // [{hex, label}] working list for the palette being built
let currentPaletteColors = ['#000000', '#ffffff']; // fallback palette used before any is saved

// ---------- Tabs ----------
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    $('#' + btn.dataset.tab).classList.add('active');
    if (btn.dataset.tab === 'estampas') {
      refreshPatternPaletteOptions();
      renderPatternPreviews();
    }
  });
});

// ---------- Paletas (montagem manual com cores/tecidos reais) ----------
function renderManualSwatches() {
  if (!manualColors.length) {
    manualSwatchesEl.innerHTML = '';
    manualEmptyHint.style.display = 'block';
    return;
  }
  manualEmptyHint.style.display = 'none';
  manualSwatchesEl.innerHTML = manualColors.map((c, i) => `
    <div class="manual-swatch">
      <div class="chip" style="background:${c.hex}"></div>
      <div class="label">${escapeHtml(c.label || c.hex)}</div>
      <button class="remove-btn" data-remove-idx="${i}" title="Remover">✕</button>
    </div>
  `).join('');
  manualSwatchesEl.querySelectorAll('[data-remove-idx]').forEach(btn => {
    btn.addEventListener('click', () => {
      manualColors.splice(Number(btn.dataset.removeIdx), 1);
      renderManualSwatches();
    });
  });
}

$('#addManualColorBtn').addEventListener('click', () => {
  const hex = manualColorInput.value;
  const label = manualColorLabelInput.value.trim();
  manualColors.push({ hex, label });
  manualColorLabelInput.value = '';
  renderManualSwatches();
});

$('#useBasicsBtn').addEventListener('click', () => {
  manualColors.push({ hex: '#000000', label: 'Preto' }, { hex: '#ffffff', label: 'Branco' });
  renderManualSwatches();
});

$('#savePaletteBtn').addEventListener('click', () => {
  if (!manualColors.length) { alert('Adicione pelo menos uma cor antes de salvar.'); return; }
  const name = paletteNameInput.value.trim() || 'Paleta sem nome';
  state.palettes.push({
    id: uid(),
    name,
    colors: manualColors.map(c => c.hex),
    colorLabels: manualColors.map(c => c.label),
    createdAt: Date.now(),
  });
  saveData();
  paletteNameInput.value = '';
  manualColors = [];
  renderManualSwatches();
  renderSavedPalettes();
  refreshPatternPaletteOptions();
});

function renderSavedPalettes() {
  if (!state.palettes.length) {
    savedPalettesEl.innerHTML = '<p class="empty-hint">Nenhuma paleta salva ainda. Adicione suas cores acima e clique em "Salvar paleta".</p>';
    return;
  }
  savedPalettesEl.innerHTML = state.palettes.map(p => `
    <div class="palette-card">
      <div class="mini-swatches">${p.colors.map(hex => `<div style="background:${hex}"></div>`).join('')}</div>
      <div class="palette-card-head">
        <strong>${escapeHtml(p.name)}</strong>
        <button class="btn danger" data-delete-palette="${p.id}">Excluir</button>
      </div>
    </div>
  `).join('');
  savedPalettesEl.querySelectorAll('[data-delete-palette]').forEach(btn => {
    btn.addEventListener('click', () => {
      state.palettes = state.palettes.filter(p => p.id !== btn.dataset.deletePalette);
      saveData();
      renderSavedPalettes();
      refreshPatternPaletteOptions();
    });
  });
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// ---------- Estampas ----------
function refreshPatternPaletteOptions() {
  const prev = patternPaletteSelect.value;
  if (!state.palettes.length) {
    patternPaletteSelect.innerHTML = '<option value="">Nenhuma paleta salva</option>';
    return;
  }
  patternPaletteSelect.innerHTML = state.palettes.map(p => `<option value="${p.id}">${escapeHtml(p.name)}</option>`).join('');
  if (state.palettes.some(p => p.id === prev)) patternPaletteSelect.value = prev;
}

function activePatternColors() {
  const p = state.palettes.find(p => p.id === patternPaletteSelect.value);
  return p ? p.colors : currentPaletteColors;
}

function renderPatternPreviews() {
  const colors = activePatternColors();
  const type = patternTypeSelect.value;
  const scale = Number(patternScaleInput.value);
  const rotation = Number(patternRotationInput.value);
  scaleOut.textContent = scale;
  rotationOut.textContent = rotation;

  const patId1 = 'pat_fabric_' + uid().slice(0, 8);
  const defs1 = buildPatternDefs(patId1, type, colors, scale, rotation);
  fabricPreviewWrap.innerHTML = fabricSVG(patId1, defs1);

  const patId2 = 'pat_garment_' + uid().slice(0, 8);
  const defs2 = buildPatternDefs(patId2, type, colors, scale, rotation);
  garmentPreviewWrap.innerHTML = garmentSVG(patId2, defs2, garmentTypeSelect.value);
}

['change', 'input'].forEach(evt => {
  patternPaletteSelect.addEventListener(evt, renderPatternPreviews);
  patternTypeSelect.addEventListener(evt, renderPatternPreviews);
  patternScaleInput.addEventListener(evt, renderPatternPreviews);
  patternRotationInput.addEventListener(evt, renderPatternPreviews);
  garmentTypeSelect.addEventListener(evt, renderPatternPreviews);
});
$('#generatePatternBtn').addEventListener('click', renderPatternPreviews);

function svgToPngDownload(svgEl, filename) {
  const serializer = new XMLSerializer();
  const svgStr = serializer.serializeToString(svgEl);
  const svgBlob = new Blob([svgStr], { type: 'image/svg+xml;charset=utf-8' });
  const url = URL.createObjectURL(svgBlob);
  const img = new Image();
  img.onload = () => {
    const canvas = document.createElement('canvas');
    const size = 600;
    canvas.width = size; canvas.height = size;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, size, size);
    ctx.drawImage(img, 0, 0, size, size);
    URL.revokeObjectURL(url);
    canvas.toBlob((blob) => {
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = filename;
      link.click();
      setTimeout(() => URL.revokeObjectURL(link.href), 2000);
    });
  };
  img.src = url;
}

$('#downloadPatternBtn').addEventListener('click', () => {
  const svgEl = fabricPreviewWrap.querySelector('svg');
  if (svgEl) svgToPngDownload(svgEl, 'estampa.png');
});
$('#downloadGarmentBtn').addEventListener('click', () => {
  const svgEl = garmentPreviewWrap.querySelector('svg');
  if (svgEl) svgToPngDownload(svgEl, 'peca-mockup.png');
});

// ---------- Adicionar peça a coleção ----------
$('#addToCollectionBtn').addEventListener('click', () => {
  if (!state.palettes.length) {
    alert('Salve uma paleta antes de adicionar uma peça a uma coleção.');
    return;
  }
  openCollectionPickerModal();
});

function openCollectionPickerModal() {
  const listHtml = state.collections.length
    ? state.collections.map(c => `<button data-pick-collection="${c.id}">${escapeHtml(c.name)}</button>`).join('')
    : '<p class="empty-hint">Nenhuma coleção ainda.</p>';

  modalRoot.innerHTML = `
    <div class="modal-backdrop" id="modalBackdrop">
      <div class="modal-box">
        <h3>Adicionar peça a qual coleção?</h3>
        <div class="modal-list">${listHtml}</div>
        <button class="btn secondary" id="modalNewCollectionBtn">+ Criar nova coleção</button>
        <button class="btn ghost modal-close" id="modalCloseBtn">Cancelar</button>
      </div>
    </div>
  `;
  $('#modalCloseBtn').addEventListener('click', closeModal);
  $('#modalBackdrop').addEventListener('click', (e) => { if (e.target.id === 'modalBackdrop') closeModal(); });
  modalRoot.querySelectorAll('[data-pick-collection]').forEach(btn => {
    btn.addEventListener('click', () => {
      addPieceToCollection(btn.dataset.pickCollection);
      closeModal();
    });
  });
  $('#modalNewCollectionBtn').addEventListener('click', () => {
    const name = prompt('Nome da nova coleção:');
    if (!name) return;
    const col = { id: uid(), name: name.trim(), season: '', description: '', createdAt: Date.now(), pieces: [] };
    state.collections.push(col);
    saveData();
    addPieceToCollection(col.id);
    closeModal();
  });
}

function closeModal() { modalRoot.innerHTML = ''; }

function addPieceToCollection(collectionId) {
  const col = state.collections.find(c => c.id === collectionId);
  if (!col) return;
  const piece = {
    id: uid(),
    name: pieceNameInput.value.trim() || 'Peça sem nome',
    garment: garmentTypeSelect.value,
    patternType: patternTypeSelect.value,
    scale: Number(patternScaleInput.value),
    rotation: Number(patternRotationInput.value),
    colors: activePatternColors(),
    yieldInfo: pieceYieldInput.value.trim(),
    cost: pieceCostInput.value ? Number(pieceCostInput.value) : null,
    price: piecePriceInput.value ? Number(piecePriceInput.value) : null,
    createdAt: Date.now(),
  };
  col.pieces.push(piece);
  saveData();
  pieceNameInput.value = '';
  pieceYieldInput.value = '';
  pieceCostInput.value = '';
  piecePriceInput.value = '';
  renderCollections();
  alert(`"${piece.name}" adicionada à coleção "${col.name}".`);
}

// ---------- Coleções ----------
$('#createCollectionBtn').addEventListener('click', () => {
  const name = $('#collectionName').value.trim();
  if (!name) { alert('Dê um nome para a coleção.'); return; }
  const col = {
    id: uid(),
    name,
    season: $('#collectionSeason').value.trim(),
    description: $('#collectionDesc').value.trim(),
    createdAt: Date.now(),
    pieces: [],
  };
  state.collections.push(col);
  saveData();
  $('#collectionName').value = '';
  $('#collectionSeason').value = '';
  $('#collectionDesc').value = '';
  renderCollections();
});

function renderCollections() {
  if (!state.collections.length) {
    collectionsListEl.innerHTML = '<p class="empty-hint">Nenhuma coleção criada ainda.</p>';
    return;
  }
  collectionsListEl.innerHTML = state.collections.map(col => `
    <div class="collection-card">
      <div class="collection-card-head">
        <div>
          <h3>${escapeHtml(col.name)}</h3>
          <div class="collection-meta">${escapeHtml(col.season || '')}${col.season ? ' · ' : ''}${col.pieces.length} peça(s)</div>
        </div>
        <button class="btn danger" data-delete-collection="${col.id}">Excluir coleção</button>
      </div>
      ${col.description ? `<p class="collection-desc">${escapeHtml(col.description)}</p>` : ''}
      <div class="pieces-row">
        ${col.pieces.map(pc => pieceChipHtml(pc)).join('') || '<span class="empty-hint">Nenhuma peça ainda — vá até a aba Estampas para adicionar.</span>'}
      </div>
    </div>
  `).join('');

  collectionsListEl.querySelectorAll('[data-delete-collection]').forEach(btn => {
    btn.addEventListener('click', () => {
      if (!confirm('Excluir esta coleção e todas as peças dela?')) return;
      state.collections = state.collections.filter(c => c.id !== btn.dataset.deleteCollection);
      saveData();
      renderCollections();
    });
  });
}

function pieceChipHtml(piece) {
  const patId = 'pat_chip_' + piece.id.slice(0, 8);
  const defs = buildPatternDefs(patId, piece.patternType, piece.colors, Math.max(piece.scale / 2.5, 10), piece.rotation);
  const svg = `<svg viewBox="0 0 34 34" xmlns="http://www.w3.org/2000/svg"><defs>${defs}</defs><rect width="34" height="34" rx="6" fill="url(#${patId})"/></svg>`;
  let moneyHtml = '';
  if (piece.cost != null || piece.price != null) {
    const cost = piece.cost != null ? piece.cost : null;
    const price = piece.price != null ? piece.price : null;
    let marginHtml = '';
    if (cost != null && price != null) {
      const margin = price - cost;
      const marginPct = price > 0 ? (margin / price * 100) : 0;
      marginHtml = `<br><span class="${margin >= 0 ? 'margin-pos' : 'margin-neg'}">margem R$ ${margin.toFixed(2)} (${marginPct.toFixed(0)}%)</span>`;
    }
    moneyHtml = `<div class="piece-money">${cost != null ? 'custo R$ ' + cost.toFixed(2) : ''}${cost != null && price != null ? ' · ' : ''}${price != null ? 'venda R$ ' + price.toFixed(2) : ''}${marginHtml}</div>`;
  }
  const yieldHtml = piece.yieldInfo ? `<div class="piece-money">rendimento: ${escapeHtml(piece.yieldInfo)}</div>` : '';
  return `
    <div class="piece-chip">
      ${svg}
      <div class="piece-info">
        <b>${escapeHtml(piece.name)}</b>
        ${piece.garment} · ${piece.patternType}
        ${moneyHtml}
        ${yieldHtml}
      </div>
    </div>
  `;
}

// ---------- Tecidos (catálogo com estoque por cor) ----------
function renderFabrics() {
  const grandTotalKg = state.fabrics.reduce((sum, f) => sum + sumStock(f), 0);
  const grandTotalValue = state.fabrics.reduce((sum, f) => sum + sumStock(f) * Number(f.custoPorKg || 0), 0);
  fabricsTotalValueEl.innerHTML = state.fabrics.length
    ? `Estoque total: <b>${grandTotalKg.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} kg</b> em ${state.fabrics.length} tecido(s) — valor estimado se comprássemos tudo hoje: <b>R$ ${grandTotalValue.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</b>${grandTotalValue === 0 ? ' (preencha "Custo por kg" nos tecidos para calcular)' : ''}`
    : '';

  if (!state.fabrics.length) {
    fabricsListEl.innerHTML = '<p class="empty-hint">Nenhum tecido cadastrado ainda.</p>';
  } else {
    fabricsListEl.innerHTML = state.fabrics.map(f => {
      const totalKg = sumStock(f);
      const custoPorKg = Number(f.custoPorKg || 0);
      const totalValue = totalKg * custoPorKg;
      return `
      <div class="collection-card">
        <div class="collection-card-head">
          <div>
            <h3>${escapeHtml(f.nome)}</h3>
            <div class="fabric-meta-row">
              ${f.composicao ? `<span>${escapeHtml(f.composicao)}</span>` : ''}
              ${f.gramatura ? `<span><b>${f.gramatura}</b> g/m²</span>` : ''}
              ${f.largura ? `<span>largura <b>${f.largura}cm</b></span>` : ''}
              ${f.rendimento ? `<span>rendimento <b>${f.rendimento}</b> m/kg</span>` : ''}
              ${custoPorKg ? `<span>custo <b>R$ ${custoPorKg.toFixed(2)}</b>/kg</span>` : ''}
              <span>estoque total <b>${totalKg.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} kg</b></span>
              <span>≈ <b>${estimateRolls(totalKg)}</b> rolo(s) <span style="opacity:.7;">(16–22kg/rolo)</span></span>
              ${custoPorKg ? `<span>valor do estoque <b>R$ ${totalValue.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</b></span>` : ''}
            </div>
          </div>
          <button class="btn danger" data-delete-fabric="${f.id}">Excluir tecido</button>
        </div>
        ${f.cores.length ? `
          <table class="fabric-colors-table">
            <thead><tr><th></th><th>Cor</th><th>Estoque (kg)</th><th>Rolos (est.)</th>${custoPorKg ? '<th>Valor (R$)</th>' : ''}<th></th></tr></thead>
            <tbody>
              ${f.cores.map(c => `
                <tr>
                  <td><span class="swatch-dot" style="background:${c.hex}"></span></td>
                  <td>${escapeHtml(c.nome)}</td>
                  <td>${Number(c.estoqueKg || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                  <td>${estimateRolls(Number(c.estoqueKg || 0))}</td>
                  ${custoPorKg ? `<td>${(Number(c.estoqueKg || 0) * custoPorKg).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>` : ''}
                  <td><button class="btn danger" data-delete-color="${f.id}::${c.id}">✕</button></td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        ` : '<p class="empty-hint">Nenhuma cor cadastrada para este tecido.</p>'}
        <div class="fabric-add-color-row" data-fabric-id="${f.id}">
          <input type="color" class="fc-color" value="#000000">
          <input type="text" class="fc-name" placeholder="Nome da cor">
          <input type="number" class="fc-stock" min="0" step="0.01" placeholder="Estoque (kg)">
          <button class="btn secondary fc-add">+ Adicionar cor</button>
        </div>
        <div class="fabric-add-color-row" data-fabric-cost-id="${f.id}">
          <span style="font-size:12.5px; color:var(--ink-soft);">Custo por kg (R$)</span>
          <input type="number" class="fc-cost" min="0" step="0.01" value="${custoPorKg || ''}" placeholder="Ex: 85.00">
          <button class="btn ghost fc-save-cost">Salvar custo</button>
        </div>
      </div>
    `;
    }).join('');

    fabricsListEl.querySelectorAll('[data-delete-fabric]').forEach(btn => {
      btn.addEventListener('click', () => {
        if (!confirm('Excluir este tecido e todas as cores dele?')) return;
        state.fabrics = state.fabrics.filter(f => f.id !== btn.dataset.deleteFabric);
        saveData();
        renderFabrics();
        refreshYieldFabricOptions();
      });
    });
    fabricsListEl.querySelectorAll('[data-delete-color]').forEach(btn => {
      btn.addEventListener('click', () => {
        const [fid, cid] = btn.dataset.deleteColor.split('::');
        const f = state.fabrics.find(f => f.id === fid);
        if (!f) return;
        f.cores = f.cores.filter(c => c.id !== cid);
        saveData();
        renderFabrics();
        refreshYieldFabricOptions();
      });
    });
    fabricsListEl.querySelectorAll('[data-fabric-cost-id]').forEach(row => {
      row.querySelector('.fc-save-cost').addEventListener('click', () => {
        const fid = row.dataset.fabricCostId;
        const f = state.fabrics.find(f => f.id === fid);
        if (!f) return;
        f.custoPorKg = Number(row.querySelector('.fc-cost').value || 0);
        saveData();
        renderFabrics();
      });
    });
    fabricsListEl.querySelectorAll('.fabric-add-color-row[data-fabric-id]').forEach(row => {
      row.querySelector('.fc-add').addEventListener('click', () => {
        const fid = row.dataset.fabricId;
        const f = state.fabrics.find(f => f.id === fid);
        if (!f) return;
        const nome = row.querySelector('.fc-name').value.trim();
        if (!nome) { alert('Dê um nome para a cor.'); return; }
        const hex = row.querySelector('.fc-color').value;
        const estoqueKg = Number(row.querySelector('.fc-stock').value || 0);
        f.cores.push({ id: uid(), nome, hex, estoqueKg });
        saveData();
        renderFabrics();
        refreshYieldFabricOptions();
      });
    });
  }
}

function sumStock(fabric) {
  return fabric.cores.reduce((sum, c) => sum + Number(c.estoqueKg || 0), 0);
}

const ROLL_MIN_KG = 16;
const ROLL_MAX_KG = 22;
function estimateRolls(kg) {
  if (!kg) return '0';
  const min = Math.round(kg / ROLL_MAX_KG);
  const max = Math.round(kg / ROLL_MIN_KG);
  return min === max ? `${min}` : `${min}–${max}`;
}

$('#createFabricBtn').addEventListener('click', () => {
  const nome = $('#fabricName').value.trim();
  if (!nome) { alert('Dê um nome para o tecido.'); return; }
  state.fabrics.push({
    id: uid(),
    nome,
    composicao: $('#fabricComposition').value.trim(),
    gramatura: Number($('#fabricWeight').value || 0),
    largura: Number($('#fabricWidth').value || 0),
    rendimento: Number($('#fabricYield').value || 0),
    custoPorKg: Number($('#fabricCostPerKg').value || 0),
    cores: [],
    createdAt: Date.now(),
  });
  saveData();
  $('#fabricName').value = '';
  $('#fabricComposition').value = '';
  $('#fabricWeight').value = '';
  $('#fabricWidth').value = '';
  $('#fabricYield').value = '';
  $('#fabricCostPerKg').value = '';
  renderFabrics();
  refreshYieldFabricOptions();
});

// ---------- Rendimento / aproveitamento de corte ----------
function refreshYieldFabricOptions() {
  const prev = yieldFabricPickSelect.value;
  const opts = ['<option value="">— preencher manualmente —</option>'];
  state.fabrics.forEach(f => {
    f.cores.forEach(c => {
      opts.push(`<option value="${f.id}::${c.id}">${escapeHtml(f.nome)} — ${escapeHtml(c.nome)} (${Number(c.estoqueKg || 0).toLocaleString('pt-BR')} kg)</option>`);
    });
  });
  yieldFabricPickSelect.innerHTML = opts.join('');
  if ([...yieldFabricPickSelect.options].some(o => o.value === prev)) yieldFabricPickSelect.value = prev;
}

yieldFabricPickSelect.addEventListener('change', () => {
  if (!yieldFabricPickSelect.value) return;
  const [fid, cid] = yieldFabricPickSelect.value.split('::');
  const f = state.fabrics.find(f => f.id === fid);
  if (!f) return;
  const c = f.cores.find(c => c.id === cid);
  if (!c) return;
  $('#yieldMPerKg').value = f.rendimento || '';
  $('#yieldFabricWidth').value = f.largura || '';
  $('#yieldWeightKg').value = c.estoqueKg || '';
  $('#yieldLengthM').value = '';
  $('#yieldFabricCost').value = f.custoPorKg ? (f.custoPorKg * (c.estoqueKg || 0)).toFixed(2) : '';
});

function computeYield({ mPerKg, weightKg, lengthM, widthCm, moldeW, moldeH, marginCm, fabricCost, piecesPerMeter }) {
  let totalLengthM = lengthM;
  if (!totalLengthM && mPerKg && weightKg) totalLengthM = mPerKg * weightKg;
  if (!totalLengthM) return null;

  const costPerPiece = (count) => (fabricCost && count > 0) ? (fabricCost / count) : null;

  if (piecesPerMeter) {
    const bestCount = Math.floor(totalLengthM * piecesPerMeter);
    return {
      totalLengthM, bestCount,
      cols: null, rows: null,
      orientation: `${piecesPerMeter.toFixed(3)} peça(s)/m (informado)`,
      utilizationPct: null,
      costPerPiece: costPerPiece(bestCount),
      usedFormula: 'piecesPerMeter',
    };
  }

  if (!widthCm || !moldeW || !moldeH) return null;

  const widthCmTotal = widthCm;
  const lengthCmTotal = totalLengthM * 100;
  const m = marginCm || 0;

  const colsA = Math.floor((widthCmTotal + m) / (moldeW + m));
  const rowsA = Math.floor((lengthCmTotal + m) / (moldeH + m));
  const countA = Math.max(colsA, 0) * Math.max(rowsA, 0);

  const colsB = Math.floor((widthCmTotal + m) / (moldeH + m));
  const rowsB = Math.floor((lengthCmTotal + m) / (moldeW + m));
  const countB = Math.max(colsB, 0) * Math.max(rowsB, 0);

  const useB = countB > countA;
  const bestCount = useB ? countB : countA;
  const cols = useB ? colsB : colsA;
  const rows = useB ? rowsB : rowsA;

  const usedAreaCm2 = bestCount * moldeW * moldeH;
  const totalAreaCm2 = widthCmTotal * lengthCmTotal;
  const utilizationPct = totalAreaCm2 > 0 ? (usedAreaCm2 / totalAreaCm2 * 100) : 0;

  return { totalLengthM, bestCount, cols, rows, orientation: useB ? 'molde girado 90°' : 'molde na posição informada', utilizationPct, costPerPiece: costPerPiece(bestCount), usedFormula: 'grid' };
}

function readYieldInputs() {
  const piecesCount = Number($('#yieldPiecesCount').value || 0);
  const piecesMeters = Number($('#yieldPiecesMeters').value || 0);
  return {
    mPerKg: Number($('#yieldMPerKg').value || 0),
    weightKg: Number($('#yieldWeightKg').value || 0),
    lengthM: Number($('#yieldLengthM').value || 0),
    widthCm: Number($('#yieldFabricWidth').value || 0),
    moldeW: Number($('#yieldMoldeW').value || 0),
    moldeH: Number($('#yieldMoldeH').value || 0),
    marginCm: Number($('#yieldMargin').value || 0),
    fabricCost: Number($('#yieldFabricCost').value || 0) || null,
    piecesPerMeter: (piecesCount && piecesMeters) ? (piecesCount / piecesMeters) : 0,
  };
}

$('#calcYieldBtn').addEventListener('click', () => {
  const inputs = readYieldInputs();
  const result = computeYield(inputs);
  if (!result) {
    yieldResultCard.innerHTML = '<h2>Resultado</h2><p class="empty-hint">Preencha rendimento/peso (ou comprimento) e, para calcular os moldes, informe "peças a cada X metros" OU a largura do rolo + tamanho do molde.</p>';
    return;
  }
  yieldResultCard.innerHTML = `
    <h2>Resultado</h2>
    <div class="result-stat"><span>Comprimento total de tecido</span><b>${result.totalLengthM.toFixed(2)} m</b></div>
    <div class="result-stat"><span>Moldes possíveis</span><b>${result.bestCount} peça(s)</b></div>
    ${result.cols != null ? `<div class="result-stat"><span>Disposição</span><b>${result.cols} × ${result.rows} (${result.orientation})</b></div>` : `<div class="result-stat"><span>Fórmula usada</span><b>${result.orientation}</b></div>`}
    ${result.utilizationPct != null ? `<div class="result-stat"><span>Aproveitamento do tecido</span><b>${result.utilizationPct.toFixed(1)}%</b></div>` : ''}
    ${result.costPerPiece != null ? `<div class="result-stat"><span>Custo de tecido por peça</span><b>R$ ${result.costPerPiece.toFixed(2)}</b></div>` : ''}
    ${result.costPerPiece != null ? '<button id="useCostInPieceBtn" class="btn ghost small" style="width:100%;">Usar este custo no campo "Custo de produção" da peça</button>' : ''}
  `;
  if (result.costPerPiece != null) {
    $('#useCostInPieceBtn').addEventListener('click', () => {
      pieceCostInput.value = result.costPerPiece.toFixed(2);
      alert('Custo de tecido copiado para a aba Estampas > Custo de produção.');
    });
  }
});

$('#calcYieldAllColorsBtn').addEventListener('click', () => {
  if (!yieldFabricPickSelect.value) {
    alert('Selecione um tecido do catálogo primeiro (campo "Usar do catálogo").');
    return;
  }
  const [fid] = yieldFabricPickSelect.value.split('::');
  const f = state.fabrics.find(f => f.id === fid);
  if (!f) return;
  const base = readYieldInputs();
  const rows = f.cores.map(c => {
    const r = computeYield({ ...base, mPerKg: f.rendimento, weightKg: c.estoqueKg, lengthM: 0, widthCm: f.largura || base.widthCm, fabricCost: f.custoPorKg ? f.custoPorKg * c.estoqueKg : null });
    return { cor: c.nome, hex: c.hex, estoqueKg: c.estoqueKg, result: r };
  });
  yieldResultCard.innerHTML = `
    <h2>Aproveitamento — ${escapeHtml(f.nome)}</h2>
    <table class="yield-table">
      <thead><tr><th></th><th>Cor</th><th>Estoque</th><th>Moldes</th><th>${base.piecesPerMeter ? 'Custo/peça' : 'Aproveit.'}</th></tr></thead>
      <tbody>
        ${rows.map(r => `
          <tr>
            <td><span class="swatch-dot" style="background:${r.hex}"></span></td>
            <td>${escapeHtml(r.cor)}</td>
            <td>${r.estoqueKg.toLocaleString('pt-BR')} kg</td>
            <td>${r.result ? r.result.bestCount : '—'}</td>
            <td>${r.result ? (base.piecesPerMeter ? (r.result.costPerPiece != null ? 'R$ ' + r.result.costPerPiece.toFixed(2) : '—') : r.result.utilizationPct.toFixed(0) + '%') : '—'}</td>
          </tr>
        `).join('')}
      </tbody>
    </table>
    <p class="hint">${base.piecesPerMeter ? `Baseado em ${base.piecesPerMeter.toFixed(3)} peça(s)/metro informado ao lado.` : `Baseado no molde ${base.moldeW || '—'}cm × ${base.moldeH || '—'}cm informado ao lado.`}</p>
  `;
});

// ---------- Init ----------
renderManualSwatches();
renderSavedPalettes();
refreshPatternPaletteOptions();
renderPatternPreviews();
renderCollections();
renderFabrics();
refreshYieldFabricOptions();
