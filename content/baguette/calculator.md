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
  }

  .calc-header {
    margin-bottom: 2em;
  }
  .calc-header h1 {
    font-size: 1.1em;
    font-weight: bold;
    margin: 0 0 0.2em 0;
  }
  .calc-header p {
    color: #888;
    font-size: 0.85em;
    margin: 0;
  }

  .calc-field {
    margin-bottom: 1.8em;
  }
  .calc-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.85em;
    margin-bottom: 0.5em;
    font-family: ui-monospace, Menlo, Consolas, monospace;
  }
  .calc-label span {
    color: #888;
  }
  .calc-value {
    color: #000 !important;
    font-weight: bold;
  }

  input[type=range] {
    -webkit-appearance: none;
    width: 100%;
    height: 1px;
    background: #E5DECF;
    outline: none;
    cursor: pointer;
  }
  input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 14px;
    height: 14px;
    background: #000;
    cursor: pointer;
  }
  input[type=range]::-moz-range-thumb {
    width: 14px;
    height: 14px;
    background: #000;
    border: none;
    cursor: pointer;
  }

  .calc-result {
    margin-top: 2em;
    padding: 1em;
    border: 1px solid #E5DECF;
    font-family: ui-monospace, Menlo, Consolas, monospace;
    font-size: 0.9em;
    display: block;
  }
  .calc-result .result-meta {
    color: #888;
    font-size: 0.85em;
    margin-bottom: 0.8em;
  }
  .calc-result .result-row {
    display: flex;
    line-height: 1.7;
  }
  .calc-result .result-row span:first-child {
    color: #000;
    width: 6em;
    flex-shrink: 0;
  }
  .calc-result .result-row span:last-child {
    color: #000;
  }
  .calc-warn {
    margin-top: 1em;
    font-size: 0.8em;
    color: #888;
    font-family: ui-monospace, Menlo, Consolas, monospace;
  }
</style>

<div class="calc-wrap">
  <div class="calc-header">
    <h1>/ Dough Storage</h1>
    <p><a href="/baguette/">recipe v2.1</a></p>
  </div>

  <div class="calc-field">
    <div class="calc-label">
      <span>baguettes per day</span>
      <span class="calc-value" id="bpd-val">2</span>
    </div>
    <input type="range" id="bpd" min="1" max="8" value="2">
  </div>

  <div class="calc-field">
    <div class="calc-label">
      <span>bake days</span>
      <span class="calc-value" id="days-val">3</span>
    </div>
    <input type="range" id="days" min="1" max="7" value="3">
  </div>

  <div class="calc-result">
    <div class="result-meta" id="result-meta">3 pots · 6 baguettes total</div>
    <div class="result-row"><span>flour</span><span id="r-flour">1260g</span></div>
    <div class="result-row"><span>water</span><span id="r-water">1740ml</span></div>
    <div class="result-row"><span>salt</span><span id="r-salt">27g</span></div>
    <div class="result-row"><span>yeast</span><span id="r-yeast">5.8g</span></div>
  </div>

  <div class="calc-warn" id="calc-warn"></div>
</div>

<script>
  const BASE_FLOUR = 420, BASE_WATER = 580, BASE_SALT = 9, BASE_YEAST = 2;
  const BASE_TOTAL = BASE_FLOUR + BASE_WATER + BASE_SALT + BASE_YEAST; // 1011
  const DOUGH_PER_BAGUETTE = BASE_TOTAL / 2; // 505.5
  const YEAST_K = 0.018;

  function calc(bpd, days) {
    const totalBaguettes = bpd * days;
    const totalDough = totalBaguettes * DOUGH_PER_BAGUETTE;
    const rawFlour = totalDough * (BASE_FLOUR / BASE_TOTAL);
    const flour = Math.round(rawFlour / 10) * 10;
    const water = Math.round(flour * (BASE_WATER / BASE_FLOUR));
    const salt  = Math.round(flour * (BASE_SALT  / BASE_FLOUR));
    const dayFactor = 1 / (1 + YEAST_K * (days - 1));
    const yeast = Math.max(1.0, Math.round(flour * (BASE_YEAST / BASE_FLOUR) * dayFactor * 2) / 2);
    return { flour, water, salt, yeast, totalBaguettes };
  }

  function update() {
    const bpd  = parseInt(document.getElementById('bpd').value);
    const days = parseInt(document.getElementById('days').value);

    document.getElementById('bpd-val').textContent  = bpd;
    document.getElementById('days-val').textContent = days;

    const r = calc(bpd, days);
    document.getElementById('result-meta').textContent =
      `${days} pot${days > 1 ? 's' : ''} · ${r.totalBaguettes} baguette${r.totalBaguettes > 1 ? 's' : ''} total`;
    document.getElementById('r-flour').textContent = r.flour  + 'g';
    document.getElementById('r-water').textContent = r.water  + 'ml';
    document.getElementById('r-salt').textContent  = r.salt   + 'g';
    document.getElementById('r-yeast').textContent = r.yeast  + 'g';

    document.getElementById('calc-warn').textContent =
      days > 5 ? `⚠ ${days}-day ferment — quality drops past day 5` : '';
  }

  document.getElementById('bpd').addEventListener('input', update);
  document.getElementById('days').addEventListener('input', update);
  update();
</script>
