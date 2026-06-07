---
title: "How Bread Works"
toc: false
showreadingtime: false
layout: single
---

<style>
  main > h1:first-of-type { display: none; }
  .time { display: none; }
  .terminal-nav { display: none; }
  h2::before { content: none !important; }
  .diagram { display: flex; gap: 48px; align-items: center; flex-wrap: wrap; margin: 2em 0; }
  .diagram svg { overflow: visible; flex-shrink: 0; }
  .layer { cursor: pointer; transition: opacity 0.15s; }
  .layer:hover { opacity: 0.82; }
  .layer.active { filter: drop-shadow(0 0 5px rgba(0,0,0,0.2)); }
  .info-panel { max-width: 300px; min-height: 100px; font-size: 0.9em; line-height: 1.65; }
  .info-name { font-weight: bold; margin-bottom: 4px; color: #111; }
  .info-pct { color: #aaa; font-size: 0.8em; margin-bottom: 10px; }
  .info-text { color: #444; }
  .hint { color: #bbb; font-size: 0.8em; }
  .legend { display: flex; gap: 20px; margin-top: 12px; flex-wrap: wrap; }
  .legend-item { display: flex; align-items: center; gap: 7px; font-size: 0.78em; color: #666; cursor: pointer; }
  .legend-item:hover { color: #111; }
  .swatch { width: 12px; height: 12px; border-radius: 2px; flex-shrink: 0; }
  .slider-wrap { margin: 2em 0; }
  .slider-row { display: flex; align-items: center; gap: 14px; margin-bottom: 20px; }
  .slider-label { font-size: 0.78em; color: #888; white-space: nowrap; }
  input[type=range] { flex: 1; accent-color: #7a4e2a; cursor: pointer; }
  .milling-layout { display: flex; gap: 48px; align-items: center; flex-wrap: wrap; }
  .milling-info { max-width: 280px; font-size: 0.9em; line-height: 1.7; }
  .extraction-num { font-size: 2.2em; font-weight: bold; color: #111; line-height: 1; margin-bottom: 4px; }
  .extraction-label { font-size: 0.78em; color: #888; margin-bottom: 16px; }
  .flour-swatch-wrap { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
  .flour-swatch { width: 36px; height: 36px; border-radius: 50%; border: 1px solid #e0d4c0; transition: background 0.2s; }
  .flour-name { font-size: 0.85em; color: #555; }
  .milling-row { display: flex; align-items: baseline; gap: 8px; margin-bottom: 6px; font-size: 0.82em; }
  .milling-tag { color: #aaa; min-width: 110px; }
  .milling-val { color: #333; }
</style>

<h1>How Bread Works</h1>
<p style="color:#888; margin-top:-0.5em;">Grain, flour, water, salt, yeast. What they are and what they do.</p>

---

## The grain

Wheat starts as a seed. A single wheat berry contains everything the plant needs to germinate and grow. Crack one open and there are three distinct parts.

<div class="diagram"><div><svg width="200" height="280" viewBox="0 0 200 280"><ellipse class="layer" id="bran" cx="100" cy="138" rx="68" ry="122" fill="#7a4e2a"/><ellipse class="layer" id="endosperm" cx="100" cy="135" rx="57" ry="109" fill="#f0ddb0"/><ellipse class="layer" id="germ" cx="96" cy="232" rx="20" ry="16" fill="#c4993a"/><path d="M100 22 Q91 138 100 254" stroke="#5c3515" stroke-width="2.5" fill="none" opacity="0.35" pointer-events="none"/><line x1="168" y1="72" x2="140" y2="90" stroke="#7a4e2a" stroke-width="1" opacity="0.5"/><text x="170" y="70" font-family="monospace" font-size="10.5" fill="#7a4e2a">bran</text><line x1="168" y1="132" x2="157" y2="132" stroke="#b89050" stroke-width="1" opacity="0.5"/><text x="170" y="136" font-family="monospace" font-size="10.5" fill="#b89050">endosperm</text><line x1="168" y1="232" x2="116" y2="232" stroke="#c4993a" stroke-width="1" opacity="0.5"/><text x="170" y="236" font-family="monospace" font-size="10.5" fill="#c4993a">germ</text></svg><div class="legend"><div class="legend-item" onclick="selectLayer('bran')"><div class="swatch" style="background:#7a4e2a"></div> Bran</div><div class="legend-item" onclick="selectLayer('endosperm')"><div class="swatch" style="background:#f0ddb0; border:1px solid #ddd"></div> Endosperm</div><div class="legend-item" onclick="selectLayer('germ')"><div class="swatch" style="background:#c4993a"></div> Germ</div></div></div><div class="info-panel" id="info-panel"><div class="hint">Click a layer to learn more.</div></div></div>

<script>
const layers = {
  bran: { name: 'Bran', pct: '~14% of the berry', text: 'The outer skin. Hard, fibrous and protective. High in fibre, B vitamins and minerals. It is brown, which is why wholemeal flour is brown. Removed during roller milling to produce white flour. Removing it extends shelf life but strips most of the nutrition.' },
  endosperm: { name: 'Endosperm', pct: '~83% of the berry', text: 'The starch and protein store. Almost entirely carbohydrate and protein. This is where gluten comes from. White flour is almost entirely endosperm. The finer it is ground, the more surface area for water to hydrate the proteins and form gluten.' },
  germ: { name: 'Germ', pct: '~3% of the berry', text: 'The embryo of the plant. Packed with fat, vitamin E and B vitamins. The fat in the germ oxidises quickly, which is why commercial mills remove it. Without the germ, white flour lasts 12 months. With it, freshly milled flour turns in 72 hours.' }
};
function selectLayer(id) {
  document.querySelectorAll('.layer').forEach(el => el.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  const d = layers[id];
  document.getElementById('info-panel').innerHTML = '<div class="info-name">' + d.name + '</div><div class="info-pct">' + d.pct + '</div><div class="info-text">' + d.text + '</div>';
}
document.querySelectorAll('.layer').forEach(el => { el.addEventListener('click', () => selectLayer(el.id)); });
</script>

---

## From grain to flour

Every bag of flour has an extraction rate: the percentage of the whole grain that ends up in the flour. Drag the slider to see what gets kept and what gets removed.

<div class="slider-wrap"><div class="slider-row"><span class="slider-label">white flour</span><input type="range" id="extraction" min="70" max="100" value="100"><span class="slider-label">wholemeal</span></div><div class="milling-layout"><svg width="200" height="280" viewBox="0 0 200 280" style="overflow:visible; flex-shrink:0;"><ellipse id="mill-bran" cx="100" cy="138" rx="68" ry="122" fill="#7a4e2a"/><ellipse id="mill-endosperm" cx="100" cy="135" rx="57" ry="109" fill="#f0ddb0"/><ellipse id="mill-germ" cx="96" cy="232" rx="20" ry="16" fill="#c4993a"/><path d="M100 22 Q91 138 100 254" stroke="#5c3515" stroke-width="2.5" fill="none" opacity="0.35" pointer-events="none"/></svg><div class="milling-info"><div class="extraction-num" id="mill-pct">100%</div><div class="extraction-label">extraction rate</div><div class="flour-swatch-wrap"><div class="flour-swatch" id="mill-swatch" style="background:#7a4e2a"></div><div class="flour-name" id="mill-name">Wholemeal</div></div><div class="milling-row"><span class="milling-tag">shelf life</span><span class="milling-val" id="mill-shelf">72 hours</span></div><div class="milling-row"><span class="milling-tag">bran</span><span class="milling-val" id="mill-bran-st">included</span></div><div class="milling-row"><span class="milling-tag">germ</span><span class="milling-val" id="mill-germ-st">included</span></div><div class="milling-row"><span class="milling-tag">gluten potential</span><span class="milling-val" id="mill-gluten">moderate</span></div></div></div></div>

<script>
(function() {
  function lerp(a, b, t) { return a + (b - a) * t; }
  function lerpCol(c1, c2, t) {
    var h = function(s) { return parseInt(s, 16); };
    var r = Math.round(lerp(h(c1.slice(1,3)), h(c2.slice(1,3)), t));
    var g = Math.round(lerp(h(c1.slice(3,5)), h(c2.slice(3,5)), t));
    var b = Math.round(lerp(h(c1.slice(5,7)), h(c2.slice(5,7)), t));
    return 'rgb('+r+','+g+','+b+')';
  }
  var slider = document.getElementById('extraction');
  function update() {
    var v = parseInt(slider.value);
    var t = (v - 70) / 30;
    var branOp = Math.max(0, Math.min(1, (v - 72) / 20));
    var germOp = Math.max(0, Math.min(1, (v - 72) / 18));
    document.getElementById('mill-bran').style.opacity = branOp;
    document.getElementById('mill-germ').style.opacity = germOp;
    document.getElementById('mill-pct').textContent = v + '%';
    document.getElementById('mill-swatch').style.background = lerpCol('#f5e6c8', '#7a4e2a', t);
    var name, shelf, branSt, germSt, gluten;
    if (v >= 95) { name = 'Wholemeal'; shelf = '72 hours'; branSt = 'included'; germSt = 'included'; gluten = 'moderate'; }
    else if (v >= 85) { name = 'Brown flour'; shelf = '3/4 months'; branSt = 'partial'; germSt = 'partial'; gluten = 'good'; }
    else if (v >= 78) { name = 'Strong white bread flour'; shelf = '9/12 months'; branSt = 'removed'; germSt = 'removed'; gluten = 'high'; }
    else { name = 'Plain white flour'; shelf = '12 months'; branSt = 'removed'; germSt = 'removed'; gluten = 'moderate'; }
    document.getElementById('mill-name').textContent = name;
    document.getElementById('mill-shelf').textContent = shelf;
    document.getElementById('mill-bran-st').textContent = branSt;
    document.getElementById('mill-germ-st').textContent = germSt;
    document.getElementById('mill-gluten').textContent = gluten;
  }
  slider.addEventListener('input', update);
  update();
})();
</script>

---

## Why we grind it

You cannot bake bread with whole wheat berries. The starch is locked inside and yeast cannot reach it. Grinding breaks open the cells and exposes the starch and proteins.

The finer the grind, the more surface area, the faster hydration, the more developed the gluten network can become.

---

## The four ingredients

### Flour

The milling slider above covers most of it. The other key variable is protein content. Strong white bread flour sits at 12/14% protein. That protein is what forms gluten when water is added. Plain flour is 9/11% and gives a softer, more tender result. The higher the protein, the more structure, the better the loaf holds its shape and traps gas.

---

### Water

Water does several things at once. It hydrates the proteins and allows gluten to form. It activates the yeast. It dissolves the salt. During baking it turns to steam inside the loaf, which drives oven spring.

The ratio of water to flour is called hydration, expressed as a percentage. Drag the slider to see how hydration changes the dough.

<div class="slider-wrap"><div class="slider-row"><span class="slider-label">55% stiff</span><input type="range" id="hydration" min="55" max="85" value="70"><span class="slider-label">85% slack</span></div><div class="milling-layout"><svg id="hydration-svg" width="200" height="200" viewBox="0 0 200 200" style="overflow:visible; flex-shrink:0;"><ellipse id="dough-blob" cx="100" cy="130" rx="40" ry="55" fill="#f0ddb0" stroke="#c8a96e" stroke-width="2"/><text id="dough-label" x="100" y="198" text-anchor="middle" font-family="monospace" font-size="11" fill="#888">70% hydration</text></svg><div class="milling-info"><div class="extraction-num" id="hyd-pct">70%</div><div class="extraction-label">hydration</div><div class="milling-row"><span class="milling-tag">feel</span><span class="milling-val" id="hyd-feel">smooth, workable</span></div><div class="milling-row"><span class="milling-tag">crumb</span><span class="milling-val" id="hyd-crumb">open, airy</span></div><div class="milling-row"><span class="milling-tag">handling</span><span class="milling-val" id="hyd-handle">easy</span></div><div class="milling-row"><span class="milling-tag">examples</span><span class="milling-val" id="hyd-eg">baguette, boule</span></div></div></div></div>

<script>
(function() {
  var sl = document.getElementById('hydration');
  function upd() {
    var v = parseInt(sl.value);
    var t = (v - 55) / 30;
    var rx = 30 + t * 50;
    var ry = 65 - t * 35;
    var cy = 200 - ry - 10;
    document.getElementById('dough-blob').setAttribute('rx', rx);
    document.getElementById('dough-blob').setAttribute('ry', ry);
    document.getElementById('dough-blob').setAttribute('cy', cy);
    document.getElementById('dough-label').setAttribute('y', cy + ry + 14);
    document.getElementById('hyd-pct').textContent = v + '%';
    document.getElementById('dough-label').textContent = v + '% hydration';
    var feel, crumb, handle, eg;
    if (v <= 60) { feel = 'stiff, firm'; crumb = 'tight, dense'; handle = 'very easy'; eg = 'bagels, pretzels'; }
    else if (v <= 68) { feel = 'firm, smooth'; crumb = 'even, structured'; handle = 'easy'; eg = 'sandwich loaf, rolls'; }
    else if (v <= 75) { feel = 'smooth, workable'; crumb = 'open, airy'; handle = 'easy'; eg = 'baguette, boule'; }
    else if (v <= 80) { feel = 'soft, tacky'; crumb = 'very open'; handle = 'moderate'; eg = 'sourdough, focaccia'; }
    else { feel = 'wet, slack'; crumb = 'large irregular holes'; handle = 'difficult'; eg = 'ciabatta'; }
    document.getElementById('hyd-feel').textContent = feel;
    document.getElementById('hyd-crumb').textContent = crumb;
    document.getElementById('hyd-handle').textContent = handle;
    document.getElementById('hyd-eg').textContent = eg;
  }
  sl.addEventListener('input', upd);
  upd();
})();
</script>

---

### Salt

Salt does more than season. It tightens the gluten network, making the dough stronger and more elastic. It slows yeast activity, which is not a problem but a feature: slower fermentation means more time for flavour to develop. It also affects crust colour through its role in the Maillard reaction during baking.

Standard amount is 2% of flour weight. Less and the bread tastes flat. More and fermentation slows significantly.

---

### Yeast vs starter

Both do the same job: eat sugars, produce CO2, make the dough rise. The difference is speed, flavour and complexity.

Drag the slider to see how each one behaves over 24 hours.

<div class="slider-wrap"><div class="slider-row"><span class="slider-label">0h</span><input type="range" id="yeast-time" min="0" max="24" value="0"><span class="slider-label">24h</span></div><div style="display:flex; gap:32px; flex-wrap:wrap; margin-top:8px;"><div style="flex:1; min-width:160px;"><div style="font-size:0.78em; color:#888; margin-bottom:8px;">Commercial yeast</div><svg width="100%" height="120" viewBox="0 0 200 120" style="overflow:visible;"><rect x="20" y="10" width="160" height="90" fill="#f9f9f9" rx="4"/><rect id="cy-bar" x="20" y="100" width="160" height="0" fill="#c4993a" rx="2" transform="scale(1,-1) translate(0,-120)"/><text id="cy-label" x="100" y="108" text-anchor="middle" font-family="monospace" font-size="10" fill="#888">flat</text></svg><div style="font-size:0.78em; color:#aaa; margin-top:4px;" id="cy-note">waiting</div></div><div style="flex:1; min-width:160px;"><div style="font-size:0.78em; color:#888; margin-bottom:8px;">Sourdough starter</div><svg width="100%" height="120" viewBox="0 0 200 120" style="overflow:visible;"><rect x="20" y="10" width="160" height="90" fill="#f9f9f9" rx="4"/><rect id="sd-bar" x="20" y="100" width="160" height="0" fill="#7a4e2a" rx="2" transform="scale(1,-1) translate(0,-120)"/><text id="sd-label" x="100" y="108" text-anchor="middle" font-family="monospace" font-size="10" fill="#888">flat</text></svg><div style="font-size:0.78em; color:#aaa; margin-top:4px;" id="sd-note">waiting</div></div></div><div style="margin-top:20px; font-size:0.82em; color:#444;" id="yeast-time-label">0 hours</div></div>

<script>
(function() {
  function cyRise(h) {
    if (h <= 0.5) return h / 0.5 * 0.1;
    if (h <= 2.5) return 0.1 + (h - 0.5) / 2 * 0.85;
    if (h <= 4) return 0.95 - (h - 2.5) / 1.5 * 0.3;
    return Math.max(0.1, 0.65 - (h - 4) / 20 * 0.55);
  }
  function sdRise(h) {
    if (h <= 2) return h / 2 * 0.08;
    if (h <= 10) return 0.08 + (h - 2) / 8 * 0.87;
    if (h <= 14) return 0.95 - (h - 10) / 4 * 0.15;
    return Math.max(0.3, 0.8 - (h - 14) / 10 * 0.5);
  }
  var sl = document.getElementById('yeast-time');
  function upd() {
    var h = parseFloat(sl.value);
    var cy = Math.min(1, cyRise(h));
    var sd = Math.min(1, sdRise(h));
    document.getElementById('cy-bar').setAttribute('height', cy * 80);
    document.getElementById('sd-bar').setAttribute('height', sd * 80);
    document.getElementById('cy-label').textContent = Math.round(cy * 100) + '%';
    document.getElementById('sd-label').textContent = Math.round(sd * 100) + '%';
    var hStr = h === Math.floor(h) ? h + 'h' : h.toFixed(1) + 'h';
    document.getElementById('yeast-time-label').textContent = hStr;
    var cyNote, sdNote;
    if (h < 1) { cyNote = 'yeast activating'; sdNote = 'bacteria and yeast waking up'; }
    else if (h < 2.5) { cyNote = 'rising fast'; sdNote = 'slow build, acids developing'; }
    else if (h < 4) { cyNote = 'peaked, ready to bake'; sdNote = 'still rising'; }
    else if (h < 10) { cyNote = h > 6 ? 'over-proofed, structure collapsing' : 'past its best'; sdNote = 'rising steadily, complex flavour building'; }
    else if (h < 14) { cyNote = 'collapsed'; sdNote = 'peaked, ready to bake'; }
    else { cyNote = 'unusable'; sdNote = h > 20 ? 'past its best, too sour' : 'still viable, more sour'; }
    document.getElementById('cy-note').textContent = cyNote;
    document.getElementById('sd-note').textContent = sdNote;
  }
  sl.addEventListener('input', upd);
  upd();
})();
</script>

---

## Fermentation

When yeast and bacteria start working, they produce CO2 gas. That gas gets trapped in the gluten network, which is why gluten development matters. No gluten, no structure to hold the bubbles, no rise.

Press play to watch fermentation happen inside a cross-section of dough.

<div style="margin:2em 0;"><canvas id="ferment-canvas" width="560" height="180" style="border-radius:6px; display:block; max-width:100%;"></canvas><div style="display:flex; align-items:center; gap:16px; margin-top:12px;"><button id="ferment-btn" style="font-family:monospace; font-size:0.82em; padding:5px 14px; border:1px solid #ccc; background:#fff; border-radius:4px; cursor:pointer;">play</button><span style="font-size:0.78em; color:#aaa;" id="ferment-status">press play to start</span></div></div>

<script>
(function() {
  var canvas=document.getElementById('ferment-canvas'),ctx=canvas.getContext('2d'),W=canvas.width,H=canvas.height,playing=false,raf=null,t=0,yeast=[],bubbles=[];
  for(var i=0;i<28;i++) yeast.push({x:10+Math.random()*(W-20),y:10+Math.random()*(H-20),vx:(Math.random()-0.5)*0.4,vy:(Math.random()-0.5)*0.4});
  function spawnBubble(){bubbles.push({x:20+Math.random()*(W-40),y:H-8-Math.random()*30,r:1.5,maxR:3+Math.random()*7,vy:-0.25-Math.random()*0.25});}
  function draw(){
    ctx.clearRect(0,0,W,H);ctx.fillStyle='#f0ddb0';ctx.fillRect(0,0,W,H);
    yeast.forEach(function(y){ctx.beginPath();ctx.arc(y.x,y.y,2.5,0,Math.PI*2);ctx.fillStyle='#8B5E3C';ctx.fill();});
    bubbles.forEach(function(b){ctx.beginPath();ctx.arc(b.x,b.y,b.r,0,Math.PI*2);ctx.fillStyle='rgba(255,255,255,0.35)';ctx.strokeStyle='rgba(180,140,60,0.4)';ctx.lineWidth=0.8;ctx.fill();ctx.stroke();});
    var pct=Math.min(100,Math.round(t*1.4));ctx.font='11px monospace';ctx.fillStyle='#bbb';ctx.textAlign='right';ctx.fillText(pct+'% fermented',W-10,H-8);
  }
  function step(){
    t+=0.3;if(Math.random()<Math.min(0.08,0.002+t*0.0006)) spawnBubble();
    yeast.forEach(function(y){y.x+=y.vx;y.y+=y.vy;if(y.x<0)y.x=W;if(y.x>W)y.x=0;if(y.y<0)y.y=H;if(y.y>H)y.y=0;});
    for(var i=bubbles.length-1;i>=0;i--){bubbles[i].y+=bubbles[i].vy;bubbles[i].r=Math.min(bubbles[i].r+0.04,bubbles[i].maxR);if(bubbles[i].y+bubbles[i].r<0)bubbles.splice(i,1);}
    draw();
    var pct=Math.min(100,Math.round(t*1.4));
    document.getElementById('ferment-status').textContent=pct<100?'fermenting... '+pct+'%':'bulk fermentation complete';
    if(pct<100) raf=requestAnimationFrame(step);
    else{playing=false;document.getElementById('ferment-btn').textContent='restart';}
  }
  document.getElementById('ferment-btn').addEventListener('click',function(){
    if(playing){playing=false;cancelAnimationFrame(raf);this.textContent='play';document.getElementById('ferment-status').textContent='paused';return;}
    if(this.textContent==='restart'){t=0;bubbles=[];}
    playing=true;this.textContent='pause';raf=requestAnimationFrame(step);
  });
  draw();
})();
</script>

---

## In the oven

Once the shaped dough goes in, several things happen in sequence. Drag the temperature slider to see what is happening inside the loaf at each stage.

<div class="slider-wrap"><div class="slider-row"><span class="slider-label">20°C</span><input type="range" id="oven-temp" min="20" max="240" value="20"><span class="slider-label">240°C</span></div><div class="milling-layout"><svg width="200" height="200" viewBox="0 0 200 200" style="overflow:visible; flex-shrink:0;"><rect id="loaf-body" x="20" y="90" width="160" height="90" rx="6" fill="#f0ddb0"/><path id="loaf-top" d="M20 90 Q60 30 100 25 Q140 30 180 90 Z" fill="#f0ddb0"/><text id="oven-temp-label" x="100" y="195" text-anchor="middle" font-family="monospace" font-size="10" fill="#aaa">20°C</text></svg><div class="milling-info"><div class="extraction-num" id="ov-temp">20°C</div><div class="milling-row"><span class="milling-tag">stage</span><span class="milling-val" id="ov-stage">cold dough, just loaded</span></div><div class="milling-row"><span class="milling-tag">yeast</span><span class="milling-val" id="ov-yeast">active</span></div><div class="milling-row"><span class="milling-tag">crust</span><span class="milling-val" id="ov-crust">soft</span></div><div class="milling-row"><span class="milling-tag">inside</span><span class="milling-val" id="ov-inside">raw dough</span></div></div></div></div>

<script>
(function(){
  function lerp(a,b,t){return a+(b-a)*t;}
  function lerpCol(c1,c2,t){var h=function(s){return parseInt(s,16);};var r=Math.round(lerp(h(c1.slice(1,3)),h(c2.slice(1,3)),t));var g=Math.round(lerp(h(c1.slice(3,5)),h(c2.slice(3,5)),t));var b=Math.round(lerp(h(c1.slice(5,7)),h(c2.slice(5,7)),t));return 'rgb('+r+','+g+','+b+')';}
  var sl=document.getElementById('oven-temp');
  function upd(){
    var v=parseInt(sl.value);
    document.getElementById('ov-temp').textContent=v+'°C';
    document.getElementById('oven-temp-label').textContent=v+'°C';
    var col=v<60?lerpCol('#f0ddb0','#e8c87a',(v-20)/40):v<140?lerpCol('#e8c87a','#c8872a',(v-60)/80):lerpCol('#c8872a','#5a2a08',(v-140)/100);
    document.getElementById('loaf-body').setAttribute('fill',col);
    document.getElementById('loaf-top').setAttribute('fill',col);
    var stage,yeastSt,crust,inside;
    if(v<35){stage='cold dough, just loaded';yeastSt='active';crust='soft';inside='raw dough';}
    else if(v<60){stage='oven spring';yeastSt='final burst of activity';crust='soft, expanding';inside='gas expanding rapidly';}
    else if(v<75){stage='yeast dying';yeastSt='dying';crust='starting to set';inside='proteins beginning to set';}
    else if(v<100){stage='starches gelatinising';yeastSt='dead';crust='firming';inside='starch network forming';}
    else if(v<140){stage='steam inside the loaf';yeastSt='dead';crust='set, pale';inside='steam driving final expansion';}
    else if(v<165){stage='Maillard reaction';yeastSt='dead';crust='browning fast';inside='fully cooked, 93/96°C core';}
    else{stage='caramelisation';yeastSt='dead';crust='deep brown, crisping';inside='done';}
    document.getElementById('ov-stage').textContent=stage;
    document.getElementById('ov-yeast').textContent=yeastSt;
    document.getElementById('ov-crust').textContent=crust;
    document.getElementById('ov-inside').textContent=inside;
  }
  sl.addEventListener('input',upd);upd();
})();
</script>
