'use strict';

// ── History ───────────────────────────────────────────────────
const MAX_POINTS = 120;
const hist = {
  temp: [], dew: [], hum: [], pres: [],
  fan: [],   // boolean series for fan-switch counting
  labels: [] // timestamp strings
};

// ── DOM helpers ───────────────────────────────────────────────
const $ = id => document.getElementById(id);

// ── Overview elements ─────────────────────────────────────────
const els = {
  tempC:        $('tempC'),
  tempF:        $('tempF'),
  dewPoint:     $('dewPoint'),
  humidity:     $('humidity'),
  pressure:     $('pressure'),
  fanStatusMini:$('fanStatusMini'),
  fanStatusSub: $('fanStatusSub'),
  fanRing:      $('fanRing'),
  fanPill:      $('fanPill'),
  fanPillText:  $('fanPillText'),
  fanDetailSub: $('fanDetailSub'),
  detailStatus: $('detailStatus'),
  detailUptime: $('detailUptime'),
  detailAvgTemp:$('detailAvgTemp'),
  statusDot:    $('statusDot'),
  statusValue:  $('statusValue'),
  thresholdInput:  $('thresholdInput'),
  thresholdSlider: $('thresholdSlider'),
  saveBtn:         $('saveBtn'),
  saveFeedback:    $('saveFeedback'),
  clockTime:    $('clockTime'),
  clockDate:    $('clockDate'),
  footerUptime: $('footerUptime'),
};

// ── Monitoring elements ───────────────────────────────────────
const mon = {
  pointCount: $('monPointCount'),
  clockTime:  $('monClockTime'),
  clockDate:  $('monClockDate'),
  avgTemp:    $('statAvgTemp'),
  maxTemp:    $('statMaxTemp'),
  minTemp:    $('statMinTemp'),
  avgHum:     $('statAvgHum'),
  avgPres:    $('statAvgPres'),
  fanSwitches:$('statFanSwitches'),
};

// ── SPA navigation ────────────────────────────────────────────
const views = { overview: $('view-overview'), monitoring: $('view-monitoring') };

document.querySelectorAll('.nav-item[data-view]').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    const target = link.dataset.view;
    document.querySelectorAll('.nav-item[data-view]').forEach(l => l.classList.remove('active'));
    link.classList.add('active');
    Object.entries(views).forEach(([k, el]) => {
      el.style.display = k === target ? 'flex' : 'none';
    });
    if (target === 'monitoring') {
      setTimeout(drawAllCharts, 50); // allow layout to settle
    }
  });
});

// ── Clock ─────────────────────────────────────────────────────
function tickClock() {
  const now = new Date();
  const time = now.toLocaleTimeString('de-DE');
  const date = now.toLocaleDateString('de-DE', { day: 'numeric', month: 'long', year: 'numeric' });
  els.clockTime.textContent = time;
  els.clockDate.textContent = date;
  mon.clockTime.textContent = time;
  mon.clockDate.textContent = date;
}
setInterval(tickClock, 1000);
tickClock();

// ── Uptime ────────────────────────────────────────────────────
const startTime = Date.now();
function formatUptime(ms) {
  const s = Math.floor(ms / 1000);
  const d = Math.floor(s / 86400);
  const h = Math.floor((s % 86400) / 3600);
  const m = Math.floor((s % 3600) / 60);
  if (d > 0) return `${d} Tag${d !== 1 ? 'e' : ''}, ${h} Std.`;
  if (h > 0) return `${h} Std., ${m} Min.`;
  return `${m} Min.`;
}

// ── Sparklines (overview cards) ───────────────────────────────
function pushHist(key, value) {
  if (value == null) return;
  hist[key].push(value);
  if (hist[key].length > MAX_POINTS) hist[key].shift();
}

function renderSparkline(polylineId, data) {
  const el = document.getElementById(polylineId);
  if (!el || data.length < 2) return;
  const w = 120, h = 32, pad = 1;
  const min = Math.min(...data) - pad;
  const max = Math.max(...data) + pad;
  const range = max - min || 1;
  const pts = data.map((v, i) => {
    const x = (i / (data.length - 1)) * w;
    const y = h - ((v - min) / range) * h;
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(' ');
  el.setAttribute('points', pts);
}

// ── Canvas chart engine ───────────────────────────────────────
const CHART_PAD = { top: 14, right: 16, bottom: 36, left: 52 };
const COLORS = {
  temp: '#3E6AE1',
  dew:  '#16A34A',
  hum:  '#F59E0B',
  pres: '#8B5CF6',
};

function drawChart(canvasId, datasets, opts = {}) {
  const canvas = $(canvasId);
  if (!canvas) return;
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.parentElement.getBoundingClientRect();
  canvas.width  = rect.width  * dpr;
  canvas.height = rect.height * dpr;
  canvas.style.width  = rect.width  + 'px';
  canvas.style.height = rect.height + 'px';

  const ctx = canvas.getContext('2d');
  ctx.scale(dpr, dpr);
  const W = rect.width, H = rect.height;
  const { top: pt, right: pr, bottom: pb, left: pl } = CHART_PAD;
  const cw = W - pl - pr;
  const ch = H - pt - pb;

  ctx.clearRect(0, 0, W, H);

  // collect all values across datasets for shared y-axis
  const allVals = datasets.flatMap(d => d.data).filter(v => v != null);
  if (allVals.length < 2) {
    ctx.fillStyle = '#8E8E8E';
    ctx.font = '13px -apple-system, Arial, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Noch keine Daten', W / 2, H / 2);
    return;
  }

  const rawMin = Math.min(...allVals);
  const rawMax = Math.max(...allVals);
  const pad = (rawMax - rawMin) * 0.12 || 1;
  const yMin = opts.yMin ?? (rawMin - pad);
  const yMax = opts.yMax ?? (rawMax + pad);
  const yRange = yMax - yMin || 1;

  const toX = i => pl + (i / Math.max(datasets[0].data.length - 1, 1)) * cw;
  const toY = v => pt + ch - ((v - yMin) / yRange) * ch;

  // Grid lines
  const GRID_LINES = 5;
  ctx.strokeStyle = '#E5E7EB';
  ctx.lineWidth = 1;
  for (let i = 0; i <= GRID_LINES; i++) {
    const y = pt + (i / GRID_LINES) * ch;
    ctx.beginPath();
    ctx.moveTo(pl, y);
    ctx.lineTo(pl + cw, y);
    ctx.stroke();

    // Y labels
    const val = yMax - (i / GRID_LINES) * yRange;
    ctx.fillStyle = '#8E8E8E';
    ctx.font = `11px -apple-system, Arial, sans-serif`;
    ctx.textAlign = 'right';
    ctx.fillText(val.toFixed(opts.decimals ?? 1), pl - 6, y + 4);
  }

  // X labels (time)
  const labels = hist.labels;
  const labelStep = Math.max(1, Math.floor(labels.length / 6));
  ctx.fillStyle = '#8E8E8E';
  ctx.font = '11px -apple-system, Arial, sans-serif';
  ctx.textAlign = 'center';
  const n = datasets[0].data.length;
  for (let i = 0; i < n; i += labelStep) {
    const lbl = labels[labels.length - n + i];
    if (lbl) ctx.fillText(lbl, toX(i), H - 8);
  }

  // Area fill + line per dataset
  datasets.forEach(ds => {
    const data = ds.data.filter((_, i) => ds.data[i] != null);
    if (data.length < 2) return;
    const indices = ds.data.map((v, i) => v != null ? i : null).filter(i => i !== null);

    // Filled area
    ctx.beginPath();
    ctx.moveTo(toX(indices[0]), toY(ds.data[indices[0]]));
    indices.forEach(i => ctx.lineTo(toX(i), toY(ds.data[i])));
    ctx.lineTo(toX(indices[indices.length - 1]), pt + ch);
    ctx.lineTo(toX(indices[0]), pt + ch);
    ctx.closePath();
    ctx.fillStyle = ds.color + '18'; // very transparent fill
    ctx.fill();

    // Line
    ctx.beginPath();
    ctx.strokeStyle = ds.color;
    ctx.lineWidth = 2;
    ctx.lineJoin = 'round';
    ctx.lineCap  = 'round';
    let first = true;
    indices.forEach(i => {
      const x = toX(i), y = toY(ds.data[i]);
      first ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      first = false;
    });
    ctx.stroke();

    // Threshold line
    if (opts.threshold != null) {
      const ty = toY(opts.threshold);
      ctx.beginPath();
      ctx.strokeStyle = '#DC2626';
      ctx.lineWidth = 1;
      ctx.setLineDash([4, 4]);
      ctx.moveTo(pl, ty);
      ctx.lineTo(pl + cw, ty);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = '#DC2626';
      ctx.font = '11px -apple-system, Arial, sans-serif';
      ctx.textAlign = 'right';
      ctx.fillText(`Schwelle ${opts.threshold}°C`, pl + cw, ty - 4);
    }

    // Last value dot
    const last = indices[indices.length - 1];
    const lx = toX(last), ly = toY(ds.data[last]);
    ctx.beginPath();
    ctx.arc(lx, ly, 4, 0, Math.PI * 2);
    ctx.fillStyle = ds.color;
    ctx.fill();
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 1.5;
    ctx.stroke();
  });

  // Axes border
  ctx.strokeStyle = '#E5E7EB';
  ctx.lineWidth = 1;
  ctx.strokeRect(pl, pt, cw, ch);
}

function drawAllCharts() {
  const threshold = parseFloat(els.thresholdInput.value) || null;

  drawChart('chartMain', [
    { data: [...hist.temp], color: COLORS.temp },
    { data: [...hist.dew],  color: COLORS.dew  },
  ], { threshold, decimals: 1 });

  drawChart('chartHum',  [{ data: [...hist.hum],  color: COLORS.hum  }], { decimals: 0, yMin: 0, yMax: 100 });
  drawChart('chartPres', [{ data: [...hist.pres], color: COLORS.pres }], { decimals: 0 });
}

// ── Stats ─────────────────────────────────────────────────────
function updateStats() {
  const temps = hist.temp.filter(v => v != null);
  const hums  = hist.hum.filter(v => v != null);
  const press = hist.pres.filter(v => v != null);

  const avg = arr => arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : null;
  const fmt = (v, d, u) => v != null ? `${v.toFixed(d)} ${u}` : '—';

  mon.avgTemp.textContent  = fmt(avg(temps), 1, '°C');
  mon.maxTemp.textContent  = temps.length ? fmt(Math.max(...temps), 1, '°C') : '—';
  mon.minTemp.textContent  = temps.length ? fmt(Math.min(...temps), 1, '°C') : '—';
  mon.avgHum.textContent   = fmt(avg(hums), 0, '%');
  mon.avgPres.textContent  = fmt(avg(press), 0, 'hPa');

  // Count fan on→off transitions
  let switches = 0;
  for (let i = 1; i < hist.fan.length; i++) {
    if (!hist.fan[i - 1] && hist.fan[i]) switches++;
  }
  mon.fanSwitches.textContent = switches;
  mon.pointCount.textContent  = hist.temp.length;
}

// ── Apply API data to overview ────────────────────────────────
function applyStatus(d) {
  els.tempC.textContent     = d.temperature != null ? `${d.temperature.toFixed(1)} °C` : '—';
  els.tempF.textContent     = d.temperature_f != null ? `${d.temperature_f.toFixed(1)} °F` : '—';
  els.dewPoint.textContent  = d.dew_point != null ? `${d.dew_point.toFixed(1)} °C` : '—';
  els.humidity.textContent  = d.humidity != null ? `${Math.round(d.humidity)} %` : '—';
  els.pressure.textContent  = d.pressure != null ? `${Math.round(d.pressure)} hPa` : '—';

  const fanOn = d.fan_on;
  els.fanStatusMini.textContent = fanOn ? 'AN' : 'AUS';
  els.fanStatusMini.className   = 'metric-value fan-status ' + (fanOn ? 'on' : 'off');
  els.fanStatusSub.textContent  = fanOn ? 'Lüfter laufen normal' : 'Lüfter aus';
  els.fanStatusSub.className    = 'fan-status-sub' + (fanOn ? '' : ' off');

  fanOn ? els.fanRing.classList.add('is-spinning') : els.fanRing.classList.remove('is-spinning');

  els.fanPill.className        = 'fan-status-pill' + (fanOn ? '' : ' off');
  els.fanPillText.textContent  = fanOn ? 'AN' : 'AUS';
  els.fanDetailSub.textContent = fanOn ? 'Lüfter laufen normal' : 'Lüfter sind aus';
  els.detailStatus.textContent = fanOn ? 'Normal' : 'Aus';
  els.detailUptime.textContent = formatUptime(Date.now() - startTime);
  els.detailAvgTemp.textContent = d.temperature != null ? `${d.temperature.toFixed(1)} °C` : '—';

  els.statusDot.className     = 'status-dot' + (fanOn ? '' : ' off');
  els.statusValue.textContent = 'Normal';
  els.footerUptime.textContent = formatUptime(Date.now() - startTime);

  if (document.activeElement !== els.thresholdInput &&
      document.activeElement !== els.thresholdSlider) {
    const t = d.switch_on_temperature;
    els.thresholdInput.value  = t != null ? t.toFixed(1) : '';
    els.thresholdSlider.value = t != null ? t : 25;
    updateSliderFill(t ?? 25);
    committedValue = t ?? committedValue;
    updateSaveBtn();
  }

  // Sparklines
  pushHist('temp', d.temperature);
  pushHist('dew',  d.dew_point);
  pushHist('hum',  d.humidity);
  pushHist('pres', d.pressure);
  pushHist('fan',  d.fan_on ? 1 : 0);

  // Timestamp label (HH:MM:SS)
  const t = new Date();
  hist.labels.push(t.toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
  if (hist.labels.length > MAX_POINTS) hist.labels.shift();

  renderSparkline('sparkTemp', hist.temp);
  renderSparkline('sparkDew',  hist.dew);
  renderSparkline('sparkHum',  hist.hum);
  renderSparkline('sparkPres', hist.pres);

  // Redraw monitoring charts if visible
  if ($('view-monitoring').style.display !== 'none') {
    drawAllCharts();
  }
  updateStats();
}

// ── Slider fill ───────────────────────────────────────────────
function updateSliderFill(val) {
  const pct = ((val - 10) / 30) * 100;
  els.thresholdSlider.style.background =
    `linear-gradient(to right, #3E6AE1 ${pct}%, #E5E7EB ${pct}%)`;
}

let committedValue = parseFloat(els.thresholdSlider.value) || 25;

function updateSaveBtn() {
  const v = parseFloat(els.thresholdInput.value);
  els.saveBtn.disabled = isNaN(v) || v === committedValue;
}

els.thresholdSlider.addEventListener('input', () => {
  const v = parseFloat(els.thresholdSlider.value);
  els.thresholdInput.value = v.toFixed(1);
  updateSliderFill(v);
  updateSaveBtn();
});

els.thresholdInput.addEventListener('input', () => {
  const v = parseFloat(els.thresholdInput.value);
  if (!isNaN(v) && v >= 10 && v <= 40) {
    els.thresholdSlider.value = v;
    updateSliderFill(v);
  }
  updateSaveBtn();
});

// ── Save ──────────────────────────────────────────────────────
els.saveBtn.addEventListener('click', async () => {
  const val = parseFloat(els.thresholdInput.value);
  if (isNaN(val)) return;
  els.saveBtn.disabled = true;
  try {
    const res = await fetch('/api/settings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ switch_on_temperature: val }),
    });
    if (res.ok) {
      committedValue = val;
      applyStatus(await res.json());
      showFeedback('Übernommen ✓');
    }
  } catch { showFeedback('Fehler beim Speichern'); }
  finally { updateSaveBtn(); }
});

function showFeedback(msg) {
  els.saveFeedback.textContent = msg;
  els.saveFeedback.style.opacity = '1';
  setTimeout(() => { els.saveFeedback.style.opacity = '0'; }, 2500);
}

// ── Polling ───────────────────────────────────────────────────
async function fetchStatus() {
  try {
    const res = await fetch('/api/status?t=' + Date.now());
    if (res.ok) applyStatus(await res.json());
  } catch (_) {}
}

fetchStatus();
setInterval(fetchStatus, 1500);

// ── Resize → redraw charts ────────────────────────────────────
window.addEventListener('resize', () => {
  if ($('view-monitoring').style.display !== 'none') drawAllCharts();
});

// ── Init ──────────────────────────────────────────────────────
updateSliderFill(parseFloat(els.thresholdSlider.value) || 25);
