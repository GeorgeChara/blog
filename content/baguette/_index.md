---
title: "Baguette"
toc: false
showreadingtime: false
layout: single
---

<style>
  main > h1:first-of-type { display: none; }
  .time { display: none; }
  h2::before, h3::before { content: none !important; }
  img:hover { transform: none !important; box-shadow: none !important; }
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

  /* Inline row: "▶ show photo  |  ↳ watch: xxx" */
  .step-media { margin: -0.8em 0 0 0; font-size: 0.8em; color: #888; }
  .step-media-row { display: flex; align-items: center; gap: 0.4em; line-height: 1; }
  .step-link { cursor: pointer; user-select: none; color: #888; }
  .step-link:hover { color: #555; }
  .step-link.photo-link::before { content: '▶ '; font-size: 0.7em; }
  .step-link.photo-link.open::before { content: '▼ '; font-size: 0.7em; }
  .step-link.watch-link::before { content: '↳ '; }
  .step-media-sep { color: #ccc; }
  .media-content { display: none; margin-top: 0.5em; margin-bottom: 0.5em; }
  .media-content.open { display: block; }
  .media-content iframe { width: 100%; aspect-ratio: 16/9; display: block; }

  /* Solo video (no photo on same step) */
  details.video-embed { margin-top: 0; }
  details.video-embed > summary { list-style: none; }
  details.video-embed > summary::-webkit-details-marker { display: none; }
  details.video-embed > summary::before { content: '↳ '; }
  details.video-embed iframe { margin-top: 0.5em; display: block; }

</style>

<h1>Baguette</h1>
<p style="color: #888; margin-top: -0.5em;">recipe v2.1 · 25 min prep · 17 min bake</p>

![](/images/baguette/result-alt-angle-2.png)

## Ingredients

<pre style="padding: 1em; border-radius: 4px; display: inline-block; margin-top: 0; color: #000;"><span style="color: #888;">Makes 2 baguettes</span>

flour    420g
water    580ml
salt     9g
yeast    2g
</pre>

## Recipe

**1.** Mix all ingredients until no dry patches of flour are visible. It should look shaggy at this point, close to porridge consistency. Cover and let rest for 30 mins.

**2.** One set of stretch and fold. Cover and let rest for 30 mins.

<div class="step-media">
  <div class="step-media-row">
    <span class="step-link photo-link" onclick="toggleMedia('s2-photo',this)">show photo</span>
    <span class="step-media-sep">|</span>
    <span class="step-link watch-link" onclick="toggleMedia('s2-video',this)">watch: stretch and fold</span>
  </div>
  <div class="media-content" id="s2-photo"><img src="/images/baguette/foldandcoil.png" alt="Fold and coil"></div>
  <div class="media-content" id="s2-video"><iframe src="https://www.youtube.com/embed/mwtTZK7_t08?mute=1" frameborder="0" allowfullscreen></iframe></div>
</div>

**3.** Two sets of coil fold 30 mins apart. Cover and leave in fridge overnight.
<span style="display:block; color:#888; font-size:0.8em; margin-top:0.2em;">Baking across multiple days? Use the <a href="/baguette/calculator/" style="color:#888;">dough storage calculator</a>.</span>

<details class="video-embed">
<summary>watch: coil fold</summary>
<iframe width="100%" style="aspect-ratio:16/9;" src="https://www.youtube.com/embed/RcJWjGeoZbc?mute=1" frameborder="0" allowfullscreen></iframe>
</details>

**4.** Flour the work surface, turn out the dough and dust the top. Divide into two, shape into rough baguettes, cover and rest for 15 mins.

<details>
<summary>show photo</summary>

![Shaped dough](/images/baguette/shaped-dough.png)

</details>

**5. Final shape:** Flatten, fold and pinch into baguettes to ensure they are tight. This will allow them to spring in the oven. Place on tray, cover with tea towel and prove until 1.5x in size.

<div class="step-media">
  <div class="step-media-row">
    <span class="step-link photo-link" onclick="toggleMedia('s5-photo',this)">show photo</span>
    <span class="step-media-sep">|</span>
    <span class="step-link watch-link" onclick="toggleMedia('s5-video',this)">watch: shaping baguettes</span>
  </div>
  <div class="media-content" id="s5-photo"><img src="/images/baguette/baguettes-in-tray.png" alt="Baguettes in tray"></div>
  <div class="media-content" id="s5-video"><iframe src="https://www.youtube.com/embed/IRDL3lPQSkc?start=57&mute=1" frameborder="0" allowfullscreen></iframe></div>
</div>

**6.** Place a metal tray at the bottom of your oven to pour boiling water into. This is to create steam to crisp the baguettes up as much as possible. Pre-heat the oven to 230°C.

**7.** Score baguettes with 3/4 lines down the middle using a sharp blade.

<details>
<summary>show photo</summary>

![Scored baguettes](/images/baguette/scored-baguettes.png)

</details>

**8.** Load baguettes into the oven. Pour boiling water in tray to create steam. **Bake at 230°C for 10 mins then 210°C for 7 mins**.

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
