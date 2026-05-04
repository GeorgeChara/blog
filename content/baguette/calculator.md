---
title: "Dough Storage Calculator"
toc: false
showreadingtime: false
---

<style>
  main > h1:first-of-type { display: none; }
  .time { display: none; }
  h2::before { content: none !important; }
  .terminal-nav { border-top: none !important; }

  .calc-wrap {
    max-width: 320px;
    font-family: ui-monospace, Menlo, Consolas, monospace;
  }

  .calc-header { margin-bottom: 1.8em; }
  .calc-header h1 { font-size: 1.1em; font-weight: bold; margin: 0 0 0.2em 0; }
  .calc-header p  { color: #888; font-size: 0.85em; margin: 0; }

  /* Ingredient table */
  .result-table {
    border: 1px solid #E5DECF;
    width: 100%;
    box-sizing: border-box;
    margin-bottom: 1.8em;
  }
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

  /* Stepper inputs */
  .calc-field { margin-bottom: 1em; }
  .calc-row { display: flex; justify-content: space-between; align-items: center; }
  .calc-row .label { color: #888; font-size: 0.85em; }
  .stepper { display: flex; align-items: center; border: 1px solid #E5DECF; }
  .stepper button {
    background: none; border: none; width: 36px; height: 36px;
    font-family: ui-monospace, Menlo, Consolas, monospace;
    font-size: 1.1em; cursor: pointer; color: #000;
    display: flex; align-items: center; justify-content: center;
    -webkit-tap-highlight-color: transparent; user-select: none;
  }
  .stepper button:active { background: #F6EEE3; }
  .stepper button:disabled { color: #ccc; cursor: default; }
  .stepper .val {
    width: 2.2em; text-align: center; font-size: 0.9em; font-weight: bold;
    border-left: 1px solid #E5DECF; border-right: 1px solid #E5DECF;
    height: 36px; line-height: 36px;
  }

  .calc-hint { font-size: 0.75em; color: #aaa; margin-top: 1.4em; line-height: 1.5; }
  .calc-hint a { color: #aaa; }
  .calc-max { font-size: 0.75em; color: #aaa; margin-top: 0.6em; }
</style>

<div class="calc-wrap">
  <div class="calc-header">
    <h1>/ Dough Storage</h1>
    <p><a href="/baguette/">recipe v2.1</a></p>
  </div>

  <div class="result-table">
    <div class="result-field">
      <div class="result-row"><span class="label">flour</span><span class="result-val" id="r-flour">420g</span></div>
    </div>
    <div class="result-field">
      <div class="result-row"><span class="label">water</span><span class="result-val" id="r-water">580ml</span></div>
    </div>
    <div class="result-field">
      <div class="result-row"><span class="label">salt</span><span class="result-val" id="r-salt">9g</span></div>
    </div>
    <div class="result-field">
      <div class="result-row"><span class="label">yeast</span><span class="result-val" id="r-yeast">2g</span></div>
    </div>
  </div>

  <div class="calc-field">
    <div class="calc-row">
      <span class="label">baguettes per session</span>
      <div class="stepper">
        <button id="bpd-dec" onclick="step('bpd',-1)">−</button>
        <span class="val" id="bpd-val">2</span>
        <button id="bpd-inc" onclick="step('bpd',1)">+</button>
      </div>
    </div>
  </div>

  <div class="calc-field">
    <div class="calc-row">
      <span class="label">bake sessions</span>
      <div class="stepper">
        <button id="days-dec" onclick="step('days',-1)">−</button>
        <span class="val" id="days-val">1</span>
        <button id="days-inc" onclick="step('days',1)">+</button>
      </div>
    </div>
  </div>

  <div class="calc-hint" id="calc-hint">bulk mix once, divide into <span id="n-pots">1</span> <span id="pots-word">pot</span> and store in the fridge, bake fresh when you have time. once removed from fridge, <a href="/baguette/">follow from step 4</a></div>
  <div class="calc-max">keep in fridge for 5 days max</div>
</div>

<script>
  const BASE_FLOUR = 420, BASE_WATER = 580, BASE_SALT = 9, BASE_YEAST = 2;
  const BASE_TOTAL = BASE_FLOUR + BASE_WATER + BASE_SALT + BASE_YEAST;
  const YEAST_K = 0.018;
  const limits = { bpd: [1, 8], days: [1, 5] };
  const state  = { bpd: 2, days: 1 };
  const current = { flour: 420, water: 580, salt: 9, yeast: 2 };
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

  function step(field, dir) {
    const [min, max] = limits[field];
    state[field] = Math.min(max, Math.max(min, state[field] + dir));
    update();
  }

  function update() {
    const { bpd, days } = state;
    document.getElementById('bpd-val').textContent  = bpd;
    document.getElementById('days-val').textContent = days;
    document.getElementById('bpd-dec').disabled  = bpd  === limits.bpd[0];
    document.getElementById('bpd-inc').disabled  = bpd  === limits.bpd[1];
    document.getElementById('days-dec').disabled = days === limits.days[0];
    document.getElementById('days-inc').disabled = days === limits.days[1];
    const r = calc(bpd, days);
    animateTo('flour', r.flour, 'g',  180);
    animateTo('water', r.water, 'ml', 180);
    animateTo('salt',  r.salt,  'g',  180);
    animateTo('yeast', r.yeast, 'g',  180);
    document.getElementById('n-pots').textContent   = days;
    document.getElementById('pots-word').textContent = days === 1 ? 'pot' : 'pots';
  }

  update();
</script>
