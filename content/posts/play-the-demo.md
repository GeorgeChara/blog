---
title: "First Demo"
date: 2026-04-03
draft: false
showreadingtime: false
---

<style>
  main > h1:first-of-type { display: none; }
  main > .time:first-of-type { display: none; }
  .demo-game { display: block; }
  .demo-mobile { display: none; text-align: center; padding: 60px 20px; color: #999; }
  @media (max-width: 768px) {
    .demo-game { display: none !important; }
    .demo-mobile { display: block; }
  }
</style>

<div class="demo-mobile">
  <p style="font-size: 2em; margin-bottom: 8px;">:(</p>
  <p>This demo requires a keyboard and mouse.</p>
  <p>Come back on a PC to play!</p>
</div>

<div class="demo-game" style="position: relative; width: 90vw; max-width: 1280px; aspect-ratio: 16/9; left: 50%; transform: translateX(-50%); overflow: hidden;">
  <iframe src="/demo/index.html"
          frameborder="0" allow="autoplay; fullscreen" scrolling="no"
          style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;">
  </iframe>
  <div style="position: absolute; top: 12px; left: 12px; background: rgba(0,0,0,0.6); border-radius: 8px; padding: 10px 14px; pointer-events: none;">
    <div style="display: grid; grid-template-columns: 34px 8px 34px 34px 34px; grid-template-rows: 32px 32px; gap: 0; align-items: center; justify-items: center;">
      <span class="key-sprite animated" style="background-image: url(/images/keys/Q.png)"></span>
      <div></div>
      <div></div>
      <span class="key-sprite" style="background-image: url(/images/keys/W.png)"></span>
      <div></div>
      <div></div>
      <div></div>
      <span class="key-sprite" style="background-image: url(/images/keys/A.png)"></span>
      <span class="key-sprite" style="background-image: url(/images/keys/S.png)"></span>
      <span class="key-sprite" style="background-image: url(/images/keys/D.png)"></span>
    </div>
    <p style="font-size: 0.7em; color: #ccc; margin: 8px 0 0 0; line-height: 1.4;">
      WASD move · Q cast<br>
      Scroll zoom · Esc pause<br><br>
      Pause to equip abilities<br>
      and adjust their values
    </p>
  </div>
</div>
