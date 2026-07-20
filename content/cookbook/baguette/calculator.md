---
title: "Dough Storage Calculator"
toc: false
showreadingtime: false
---

<style>
  main > h1:first-of-type { display: none; }
  .time { display: none; }
  h2::before { content: none !important; }
  .terminal-nav { display: none; }

  header, main, footer { min-width: 0; }

  .calc-wrap {
    max-width: 360px;
    width: 100%;
    box-sizing: border-box;
    font-family: ui-monospace, Menlo, Consolas, monospace;
  }

  .calc-header { margin-bottom: 1.8em; }
  .calc-header h1 { font-size: 1.1em; font-weight: bold; margin: 0 0 0.2em 0; }
  .calc-header p  { color: #888; font-size: 0.85em; margin: 0; }

  /* One container for everything */
  .calc-card {
    border: 1px solid #E5DECF;
    width: 100%;
    box-sizing: border-box;
    margin-bottom: 1.8em;
  }

  /* Stepper rows at top */
  .stepper-card {
    border: 1px solid #E5DECF;
    width: 100%;
    box-sizing: border-box;
    margin-top: 0.6em;
    margin-bottom: 1.8em;
  }
  .stepper-field {
    padding: 0.6em 1em;
    border-bottom: 1px solid #E5DECF;
    background: #fff;
  }
  .stepper-field:last-child { border-bottom: none; }
  .slider-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.3em;
  }
  .slider-row .label { color: #888; font-size: 0.85em; }
  .slider-row .val { font-size: 1em; font-weight: bold; color: #000; }
  input[type=range] { width: 100%; display: block; }

  /* Ingredient rows below */
  .result-field { padding: 0.5em 1em; border-bottom: 1px solid #E5DECF; }
  .result-field:last-child { border-bottom: none; }
  .result-field:nth-child(odd)  { background: #fff; }
  .result-field:nth-child(even) { background: #F6EEE3; }
  .result-row { display: flex; justify-content: space-between; align-items: baseline; }
  .result-row .label { color: #888; font-size: 0.85em; }
  .result-val {
    font-size: 1.6em; font-weight: bold; color: #000; line-height: 1.2;
    display: inline-block;
  }

  .calc-hint { font-size: 0.75em; color: #aaa; margin-top: 1.4em; line-height: 1.5; }
  .calc-hint a { color: #aaa; }
  .calc-max { font-size: 0.75em; color: #aaa; margin-top: 0.6em; }
</style>

<div class="calc-wrap">
  <div class="calc-header">
    <h1>/ Dough Storage</h1>
    <p><a href="/cookbook/baguette/">recipe v2.1</a></p>
  </div>

  <div class="calc-card">
    <div class="result-field">
      <div class="result-row"><span class="label">flour</span><span class="result-val" id="r-flour">420g</span></div>
    </div>
    <div class="result-field">
      <div class="result-row"><span class="label">water</span><span class="result-val" id="r-water">320ml</span></div>
    </div>
    <div class="result-field">
      <div class="result-row"><span class="label">salt</span><span class="result-val" id="r-salt">9g</span></div>
    </div>
    <div class="result-field">
      <div class="result-row"><span class="label">yeast</span><span class="result-val" id="r-yeast">2g</span></div>
    </div>
  </div>

  <div class="stepper-card">
    <div class="stepper-field">
      <div class="slider-row">
        <span class="label">baguettes per session</span>
        <span class="val" id="bpd-val">2</span>
      </div>
      <input type="range" id="bpd" min="1" max="8" value="2">
    </div>
    <div class="stepper-field">
      <div class="slider-row">
        <span class="label">bake sessions</span>
        <span class="val" id="days-val">1</span>
      </div>
      <input type="range" id="days" min="1" max="5" value="1">
    </div>
  </div>

  <div style="margin-top:1.4em; font-size:0.75em; color:#aaa; line-height:1.6; border-left:2px solid #E5DECF; padding-left:0.6em;">
    <span style="color:#888; font-weight:bold;">extra step (storage only)</span><br>
    before refrigerating, divide into <span id="n-pots" style="color:#888; font-weight:bold;">1</span> equal <span id="pots-word">portion</span>, give each a quick coil fold, then place into its container.
  </div>

  <div class="calc-hint" style="margin-top:1.4em;"><a href="/cookbook/baguette/" style="color:#aaa;">follow from step 4</a></div>
  <div class="calc-max">keep in fridge for 5 days max</div>
</div>

<script>
  const BASE_FLOUR = 420, BASE_WATER = 320, BASE_SALT = 9, BASE_YEAST = 2;
  const BASE_TOTAL = BASE_FLOUR + BASE_WATER + BASE_SALT + BASE_YEAST;
  const YEAST_K = 0.018;
  const limits = { bpd: [1, 8], days: [1, 5] };
  const state  = { bpd: 2, days: 1 };
  const current = { flour: 420, water: 320, salt: 9, yeast: 2 };
  const anims = {};

  function calc(bpd, days) {
    const flour = Math.round(bpd * days * (BASE_TOTAL / 2) * (BASE_FLOUR / BASE_TOTAL) / 10) * 10;
    const water = Math.round(flour * (BASE_WATER / BASE_FLOUR));
    const salt  = Math.round(flour * (BASE_SALT  / BASE_FLOUR));
    const yeast = Math.max(1, Math.ceil(flour * (BASE_YEAST / BASE_FLOUR) / (1 + YEAST_K * (days - 1))));
    return { flour, water, salt, yeast };
  }

  function animateTo(key, target, suffix, duration) {
    if (anims[key]) cancelAnimationFrame(anims[key]);
    const start = current[key];
    const el = document.getElementById('r-' + key);
    const t0 = performance.now();
    function tick(now) {
      const t = Math.min((now - t0) / duration, 1);
      const val = Math.round(start + (target - start) * t);
      current[key] = val;
      el.textContent = val + suffix;
      if (t < 1) anims[key] = requestAnimationFrame(tick);
    }
    anims[key] = requestAnimationFrame(tick);
  }

  function update() {
    const bpd  = parseInt(document.getElementById('bpd').value);
    const days = parseInt(document.getElementById('days').value);
    document.getElementById('bpd-val').textContent  = bpd;
    document.getElementById('days-val').textContent = days;
    const r = calc(bpd, days);
    animateTo('flour', r.flour, 'g',  180);
    animateTo('water', r.water, 'ml', 180);
    animateTo('salt',  r.salt,  'g',  180);
    animateTo('yeast', r.yeast, 'g',  180);
    document.getElementById('n-pots').textContent    = days;
    document.getElementById('pots-word').textContent = days === 1 ? 'portion' : 'portions';
  }

  document.getElementById('bpd').addEventListener('input', update);
  document.getElementById('days').addEventListener('input', update);
  update();
</script>
