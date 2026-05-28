---
title: "Butter"
toc: false
showreadingtime: false
layout: single
---

<style>
  main > h1:first-of-type { display: none; }
  .time { display: none; }
  h2::before, h3::before { content: none !important; }
  img:hover { transform: none !important; box-shadow: none !important; }
  img { border-radius: 8px !important; border: none !important; padding: 0 !important; }
  details { margin: -1em 0 0 0; padding: 0; }
  details summary {
    color: #888;
    font-size: 0.8em;
    cursor: pointer;
    user-select: none;
    line-height: 1;
  }
  details summary:hover { color: #555; }
  details[open] { margin-bottom: 0.5em; }
  .content pre { color: #000; }
  .step-media { margin: -0.8em 0 0 0; font-size: 0.8em; color: #888; }
  .step-media-row { display: flex; align-items: center; gap: 0.4em; line-height: 1; }
  .step-link { cursor: pointer; user-select: none; color: #888; }
  .step-link:hover { color: #555; }
  .step-link.photo-link::before { content: '▶ '; font-size: 0.7em; }
  .step-link.photo-link.open::before { content: '▼ '; font-size: 0.7em; }
  .media-content { display: none; margin-top: 0.5em; margin-bottom: 0.5em; }
  .media-content.open { display: block; }
  .terminal-nav { display: none; }
</style>

<h1>Butter</h1>
<p style="color: #888; margin-top: -0.5em;">5–10 min whisk</p>

<img src="/images/butter/header.png" alt="Finished butter">

## Ingredients

<pre style="padding: 1em; border-radius: 4px; display: inline-block; margin: 0; color: #000;">double cream    600ml
</pre>

## Recipe

**1.** Take the cream out of the fridge 30-60 minutes before starting. Room temp is key, cold cream takes much longer and won't break as cleanly.

<div class="step-media">
  <div class="step-media-row">
    <span class="step-link photo-link" onclick="toggleMedia('s1-photo',this)">show photo</span>
  </div>
  <div class="media-content" id="s1-photo"><img src="/images/butter/IMG_5131.png" alt="Cream and mixer ready"></div>
</div>

**2.** Pour into a stand mixer and whisk on high for 5-10 minutes. It goes through stages: whipped cream, stiff peaks, then it breaks. You'll see the butter form suddenly. Stop there.

<div class="step-media">
  <div class="step-media-row">
    <span class="step-link photo-link" onclick="toggleMedia('s2-photo',this)">show photo</span>
  </div>
  <div class="media-content" id="s2-photo"><img src="/images/butter/IMG_5135.png" alt="Butter formed on whisk"></div>
</div>

**3.** Sieve the buttermilk off into a jug and set aside.

<div class="step-media">
  <div class="step-media-row">
    <span class="step-link photo-link" onclick="toggleMedia('s3-photo',this)">show photo</span>
  </div>
  <div class="media-content" id="s3-photo"><img src="/images/butter/IMG_5138.png" alt="Buttermilk bottled up"></div>
</div>

<span style="display:block; color:#888; font-size:0.8em; margin-top:0.3em; border-left: 2px solid #E5DECF; padding-left: 0.6em;">600ml of cream gives you roughly 200ml of buttermilk. Worth keeping, good for marinating chicken or making pancakes.</span>

**4.** Put the butter in a bowl of icy water and work it with your hands, pressing out as much buttermilk as you can. Change the water and repeat until it runs clear. Any leftover buttermilk will make the butter go off faster.

<div class="step-media">
  <div class="step-media-row">
    <span class="step-link photo-link" onclick="toggleMedia('s4-photo',this)">show photo</span>
  </div>
  <div class="media-content" id="s4-photo"><img src="/images/butter/IMG_5136.png" alt="Butter ready to wash, ice bowl alongside"></div>
</div>

**5.** Lift it out and pat dry. Add flaky salt, herbs or garlic if you want, or leave it plain. Press into a container and refrigerate.

<div class="step-media">
  <div class="step-media-row">
    <span class="step-link photo-link" onclick="toggleMedia('s5-photo',this)">show photo</span>
  </div>
  <div class="media-content" id="s5-photo"><img src="/images/butter/IMG_5139.png" alt="Butter on cutting board ready to season"></div>
</div>

<script>
function toggleMedia(id, el) {
  const wrap = el.closest('.step-media');
  const target = document.getElementById(id);
  const isOpen = target.classList.contains('open');
  wrap.querySelectorAll('.media-content').forEach(c => c.classList.remove('open'));
  wrap.querySelectorAll('.step-link').forEach(l => l.classList.remove('open'));
  if (!isOpen) { target.classList.add('open'); el.classList.add('open'); }
}
</script>
