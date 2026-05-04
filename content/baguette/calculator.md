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

  .calc-field { margin-bottom: 1.6em; }
  .calc-label { display: flex; align-items: baseline; gap: 0.4em; margin-bottom: 0.4em; }
  .calc-label span { color: #888; font-size: 0.85em; }
  .calc-val {
    font-size: 2em; font-weight: bold; color: #000; line-height: 1;
    transition: transform 0.12s ease; display: inline-block;
  }
  .calc-val.bump { transform: scale(1.25); }

  input[type=range] { width: 60%; display: block; }

  .storage-ind { font-size: 0.78em; color: #aaa; margin-top: 0.3em; }

  .calc-result {
    margin-top: 2em; padding-top: 1.2em;
    border-top: 1px solid #E5DECF; font-size: 0.9em;
    border-bottom: none;
  }
  .result-row { display: flex; line-height: 1.7; }
  .result-row span:first-child { color: #000; width: 6em; flex-shrink: 0; }
  .result-row span:last-child  { color: #000; }

  .calc-note {
    margin-top: 1em;
    font-size: 0.8em; color: #888;
  }
  .calc-note a { color: #888; }
  .content hr { display: none; }
  .terminal-nav { border-top: none !important; }
</style>

<div class="calc-wrap">
  <div class="calc-header">
    <h1>/ Dough Storage</h1>
    <p><a href="/baguette/">recipe v2.1</a></p>
  </div>

  <div class="calc-field">
    <div class="calc-label">
      <span>baguettes per session</span>
      <span class="calc-val" id="bpd-val">2</span>
    </div>
    <input type="range" id="bpd" min="1" max="8" value="2">
  </div>

  <div class="calc-field">
    <div class="calc-label">
      <span>bake sessions</span>
      <span class="calc-val" id="days-val">3</span>
    </div>
    <input type="range" id="days" min="1" max="5" value="3">
    <div class="storage-ind" id="storage-ind">●●●○○ &nbsp;3 of 5 days</div>
  </div>

  <div class="calc-result">
    <div class="result-row"><span>flour</span><span id="r-flour">1260g</span></div>
    <div class="result-row"><span>water</span><span id="r-water">1740ml</span></div>
    <div class="result-row"><span>salt</span><span id="r-salt">27g</span></div>
    <div class="result-row"><span>yeast</span><span id="r-yeast">6g</span></div>
    <div class="calc-note">
      Mix once and divide into 3 pots. Bake one pot per session from <a href="/baguette/">step 4</a>.
    </div>
  </div>
</div>

<script>
  const BASE_FLOUR = 420, BASE_WATER = 580, BASE_SALT = 9, BASE_YEAST = 2;
  const BASE_TOTAL = BASE_FLOUR + BASE_WATER + BASE_SALT + BASE_YEAST;
  const YEAST_K = 0.018;

  function calc(bpd, days) {
    const flour = Math.round(bpd * days * (BASE_TOTAL / 2) * (BASE_FLOUR / BASE_TOTAL) / 10) * 10;
    const water = Math.round(flour * (BASE_WATER / BASE_FLOUR));
    const salt  = Math.round(flour * (BASE_SALT  / BASE_FLOUR));
    const yeast = Math.max(1, Math.ceil(flour * (BASE_YEAST / BASE_FLOUR) / (1 + YEAST_K * (days - 1))));
    return { flour, water, salt, yeast };
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
    document.getElementById('storage-ind').innerHTML =
      '●'.repeat(days) + '○'.repeat(5 - days) + ' &nbsp;' + days + ' of 5 days';
    const r = calc(bpd, days);
    document.getElementById('r-flour').textContent = r.flour + 'g';
    document.getElementById('r-water').textContent = r.water + 'ml';
    document.getElementById('r-salt').textContent  = r.salt  + 'g';
    document.getElementById('r-yeast').textContent = r.yeast + 'g';
    document.querySelector('.calc-note').innerHTML = days === 1
      ? 'Mix once. Bake from <a href="/baguette/" style="color:#888;">step 4</a>.'
      : `Mix once and divide into ${days} pots. Bake one pot per session from <a href="/baguette/" style="color:#888;">step 4</a>.`;
  }

  document.getElementById('bpd').addEventListener('input', () => update('bpd'));
  document.getElementById('days').addEventListener('input', () => update('days'));
  update();
</script>
