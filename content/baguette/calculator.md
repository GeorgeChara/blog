---
title: "Dough Storage Calculator"
toc: false
showreadingtime: false
---

<style>
  main > h1:first-of-type { display: none; }
  .time { display: none; }
  h2::before { content: none !important; }

  .calc-wrap {
    max-width: 480px;
    font-family: ui-monospace, Menlo, Consolas, monospace;
  }

  .calc-header { margin-bottom: 2em; }
  .calc-header h1 { font-size: 1.1em; font-weight: bold; margin: 0 0 0.2em 0; }
  .calc-header p  { color: #888; font-size: 0.85em; margin: 0; }

  .calc-field { margin-bottom: 1.8em; }
  .calc-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.85em;
    margin-bottom: 0.5em;
  }
  .calc-label span     { color: #888; }
  .calc-label strong   { color: #000; }

  input[type=range] { width: 100%; display: block; }

  .calc-result {
    margin-top: 2em;
    padding-top: 1.5em;
    border-top: 1px solid #E5DECF;
    font-size: 0.9em;
  }
  .calc-result .result-meta { color: #888; font-size: 0.85em; margin-bottom: 0.8em; }
  .calc-result .result-row  { display: flex; line-height: 1.7; }
  .calc-result .result-row span:first-child { color: #000; width: 6em; flex-shrink: 0; }
  .calc-result .result-row span:last-child  { color: #000; }

  .calc-warn { margin-top: 1em; font-size: 0.8em; color: #888; }
</style>

<div class="calc-wrap">
  <div class="calc-header">
    <h1>/ Dough Storage</h1>
    <p><a href="/baguette/">recipe v2.1</a></p>
  </div>

  <div class="calc-field">
    <div class="calc-label">
      <span>baguettes per day</span>
      <strong id="bpd-val">2</strong>
    </div>
    <input type="range" id="bpd" min="1" max="8" value="2">
  </div>

  <div class="calc-field">
    <div class="calc-label">
      <span>bake days</span>
      <strong id="days-val">3</strong>
    </div>
    <input type="range" id="days" min="1" max="7" value="3">
  </div>

  <div class="calc-result">
    <div class="result-meta" id="result-meta">3 pots · 6 baguettes total</div>
    <div class="result-row"><span>flour</span><span id="r-flour">1260g</span></div>
    <div class="result-row"><span>water</span><span id="r-water">1740ml</span></div>
    <div class="result-row"><span>salt</span><span id="r-salt">27g</span></div>
    <div class="result-row"><span>yeast</span><span id="r-yeast">6g</span></div>
  </div>

  <div class="calc-warn" id="calc-warn"></div>
  <p style="margin-top: 1.5em; font-size: 0.8em; color: #888;">when ready to bake, remove from fridge and follow from <a href="/baguette/" style="color: #888;">step 4</a></p>
</div>

<script>
  const BASE_FLOUR = 420, BASE_WATER = 580, BASE_SALT = 9, BASE_YEAST = 2;
  const BASE_TOTAL = BASE_FLOUR + BASE_WATER + BASE_SALT + BASE_YEAST;
  const YEAST_K = 0.018;

  function calc(bpd, days) {
    const flour = Math.round(bpd * days * (BASE_TOTAL / 2) * (BASE_FLOUR / BASE_TOTAL) / 10) * 10;
    const water = Math.round(flour * (BASE_WATER / BASE_FLOUR));
    const salt  = Math.round(flour * (BASE_SALT  / BASE_FLOUR));
    const yeast = Math.max(1.0, Math.round(flour * (BASE_YEAST / BASE_FLOUR) / (1 + YEAST_K * (days - 1)) * 2) / 2);
    return { flour, water, salt, yeast, total: bpd * days };
  }

  function update() {
    const bpd  = parseInt(document.getElementById('bpd').value);
    const days = parseInt(document.getElementById('days').value);
    document.getElementById('bpd-val').textContent  = bpd;
    document.getElementById('days-val').textContent = days;
    const r = calc(bpd, days);
    document.getElementById('result-meta').textContent =
      `${days} pot${days > 1 ? 's' : ''} · ${r.total} baguette${r.total > 1 ? 's' : ''} total`;
    document.getElementById('r-flour').textContent = r.flour + 'g';
    document.getElementById('r-water').textContent = r.water + 'ml';
    document.getElementById('r-salt').textContent  = r.salt  + 'g';
    document.getElementById('r-yeast').textContent = r.yeast + 'g';
    document.getElementById('calc-warn').textContent =
      days > 5 ? `⚠ ${days}-day ferment — quality drops past day 5` : '';
  }

  document.getElementById('bpd').addEventListener('input', update);
  document.getElementById('days').addEventListener('input', update);
  update();
</script>
