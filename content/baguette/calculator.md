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

  .calc-header { margin-bottom: 2em; }
  .calc-header h1 { font-size: 1.1em; font-weight: bold; margin: 0 0 0.2em 0; }
  .calc-header p  { color: #888; font-size: 0.85em; margin: 0; }

  /* Input rows */
  .calc-field { margin-bottom: 1.4em; }
  .calc-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.3em;
  }
  .calc-row .label { color: #888; font-size: 0.85em; }
  .calc-val {
    font-size: 1em; font-weight: bold; color: #000;
    transition: transform 0.12s ease; display: inline-block;
  }
  .calc-val.bump { transform: scale(1.15); }

  input[type=range] { width: 100%; display: block; }

  /* Output table */
  .result-table {
    border: 1px solid #E5DECF;
    width: 100%;
    box-sizing: border-box;
    border-collapse: collapse;
  }
  .result-field {
    padding: 0.5em 1em;
    border-bottom: 1px solid #E5DECF;
  }
  .result-field:last-child { border-bottom: none; }
  .result-field:nth-child(odd)  { background: #fff; }
  .result-field:nth-child(even) { background: #F6EEE3; }
  .result-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }
  .result-row .label { color: #888; font-size: 0.85em; }
  .result-val {
    font-size: 1.6em; font-weight: bold; color: #000; line-height: 1.2;
    transition: transform 0.1s ease; display: inline-block;
  }

  .calc-note { margin-top: 1.2em; font-size: 0.8em; color: #888; }
  .calc-note a { color: #888; }
</style>

<div class="calc-wrap">
  <div class="calc-header">
    <h1>/ Dough Storage</h1>
    <p><a href="/baguette/">recipe v2.1</a></p>
  </div>

  <div class="calc-field">
    <div class="calc-row">
      <span class="label">baguettes per session</span>
      <span class="calc-val" id="bpd-val">2</span>
    </div>
    <input type="range" id="bpd" min="1" max="8" value="2">
  </div>

  <div class="calc-field">
    <div class="calc-row">
      <span class="label">bake sessions</span>
      <span class="calc-val" id="days-val">1</span>
    </div>
    <input type="range" id="days" min="1" max="5" value="1">
    <div style="font-size:0.75em; color:#aaa; margin-top:0.8em; line-height:1.5;" id="calc-note">bulk mix once, divide into <span id="n-pots">1</span> <span id="pots-word">pot</span> and store in the fridge, bake fresh when you have time. once removed from fridge, <a href="/baguette/" style="color:#aaa;">follow from step 4</a></div>
  </div>

  <div class="calc-field" style="margin-top:1.6em;">
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
  </div>

  <div style="font-size:0.75em; color:#aaa; margin-top:1em;">max 5 days</div>

</div>

<script>
  const BASE_FLOUR = 420, BASE_WATER = 580, BASE_SALT = 9, BASE_YEAST = 2;
  const BASE_TOTAL = BASE_FLOUR + BASE_WATER + BASE_SALT + BASE_YEAST;
  const YEAST_K = 0.018;

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
    function step(now) {
      const t = Math.min((now - t0) / duration, 1);
      const val = Math.round(start + (target - start) * t);
      current[key] = val;
      el.textContent = val + suffix;
      if (t < 1) anims[key] = requestAnimationFrame(step);
    }
    anims[key] = requestAnimationFrame(step);
  }

  function pulse(id) {
    const el = document.getElementById(id);
    el.classList.remove('bump');
    void el.offsetWidth;
    el.classList.add('bump');
    setTimeout(() => el.classList.remove('bump'), 150);
  }

  function update(changed) {
    const bpd  = parseInt(document.getElementById('bpd').value);
    const days = parseInt(document.getElementById('days').value);
    document.getElementById('bpd-val').textContent  = bpd;
    document.getElementById('days-val').textContent = days;
    if (changed) pulse(changed + '-val');
    const r = calc(bpd, days);
    animateTo('flour', r.flour, 'g',  180);
    animateTo('water', r.water, 'ml', 180);
    animateTo('salt',  r.salt,  'g',  180);
    animateTo('yeast', r.yeast, 'g',  180);
    document.getElementById('n-pots').textContent   = days;
    document.getElementById('pots-word').textContent = days === 1 ? 'pot' : 'pots';
  }

  document.getElementById('bpd').addEventListener('input', () => update('bpd'));
  document.getElementById('days').addEventListener('input', () => update('days'));
  update();
</script>
