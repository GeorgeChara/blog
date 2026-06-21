---
title: "Cookbook"
toc: false
showreadingtime: false
layout: single
---

<style>
  main > h1:first-of-type { display: none; }
  .time { display: none; }
  .terminal-nav { display: none; }

  .cookbook-cols { column-count: 2; column-gap: 3em; }
  .cat { break-inside: avoid; margin-bottom: 1.6em; }

  .cat-heading { font-weight: bold; font-size: 1em; margin: 0 0 0.5em 0; color: #000; }

  .recipe-list { list-style: none; padding: 0; margin: 0; }
  .recipe-list li { margin: 0.6em 0; }
  .recipe-list a { color: #4169E1; text-decoration: none; border-bottom: 1px solid #c5ccee; }
  .recipe-list a:hover { color: #2a50c8; border-bottom-color: #2a50c8; }
  .recipe-meta { color: #888; font-size: 0.85em; margin-left: 0.4em; }
  .recipe-list li.pending a { color: #aaa; border-bottom-color: #e0d9d0; }
  .recipe-list li.pending a:hover { color: #888; border-bottom-color: #aaa; }
  .frz { color: #3f9fd4; font-size: 1em; margin-left: 0.35em; }

  @media (max-width: 600px) { .cookbook-cols { column-count: 1; } }

  .featured { margin: 0 0 1.6em 0; padding-bottom: 1.2em; border-bottom: 1px solid #eee; }
  .featured a { color: #4169E1; text-decoration: none; font-weight: bold; border-bottom: 1px solid #c5ccee; }
  .featured a:hover { color: #2a50c8; border-bottom-color: #2a50c8; }
  .featured span { color: #888; font-size: 0.85em; margin-left: 0.4em; }

  .cookbook-search { width: 100%; box-sizing: border-box; padding: 0.4em 0.7em; margin: 0 0 1.3em 0; font-family: inherit; font-size: 16px; border: 1px solid #e0d9d0; border-radius: 6px; background: #fff; color: #555; }
  .cookbook-search::placeholder { color: #b3b3b3; font-size: 13px; }
  .cookbook-search:focus { outline: none; border-color: #4169E1; }
  .cat.is-hidden, .recipe-list li.is-hidden { display: none; }
  .cookbook-noresults { display: none; color: #888; font-size: 0.9em; margin: 0; }
</style>

<input type="search" id="cookbook-search" class="cookbook-search" placeholder="Search recipes…" autocomplete="off" aria-label="Search recipes">
<p id="cookbook-noresults" class="cookbook-noresults">No recipes match that search.</p>

<div class="cookbook-cols">
<div class="cat">
<p class="cat-heading">Signature</p>
<ul class="recipe-list">
<li><a href="/cookbook/baguette/">Baguette</a></li>
</ul>
</div>
<div class="cat">
<p class="cat-heading">Basics</p>
<ul class="recipe-list">
<li class="pending"><a href="/cookbook/apple-sauce/">Apple Sauce</a><span class="frz">❄</span></li>
<li><a href="/cookbook/butter/">Butter</a><span class="frz">❄</span></li>
<li><a href="/cookbook/buttercream/">Buttercream</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/chicken-marinade/">Chicken Marinade</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/fresh-pasta-dough/">Fresh Pasta Dough</a></li>
<li><a href="/cookbook/hash-browns/">Hash Browns</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/mashed-potato/">Mashed Potato</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/rice/">Rice</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/rough-puff-pastry/">Rough Puff Pastry</a></li>
<li class="pending"><a href="/cookbook/soffritto/">Soffritto</a><span class="frz">❄</span></li>
</ul>
</div>
<div class="cat">
<p class="cat-heading">Bread</p>
<ul class="recipe-list">
<li><a href="/cookbook/bagels/">Bagels</a></li>
<li><a href="/cookbook/boule/">Boule</a></li>
<li class="pending"><a href="/cookbook/cinnamon-swirls/">Cinnamon Swirls</a></li>
<li class="pending"><a href="/cookbook/crumpets/">Crumpets</a></li>
<li class="pending"><a href="/cookbook/english-muffins/">English Muffins</a></li>
<li class="pending"><a href="/cookbook/farata/">Farata</a></li>
<li><a href="/cookbook/flour-tortillas/">Flour Tortillas</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/focaccia/">Focaccia</a></li>
<li class="pending"><a href="/cookbook/hot-cross-buns/">Hot Cross Buns</a></li>
<li class="pending"><a href="/cookbook/iced-fingers/">Iced Fingers</a></li>
<li><a href="/cookbook/lazy-boule/">Lazy Boule</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/pita/">Pita</a></li>
<li class="pending"><a href="/cookbook/pupusas/">Pupusas</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/rye-loaf/">Rye Loaf</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/seeded-wholemeal-loaf/">Seeded Wholemeal Loaf</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/shokupan/">Shokupan</a></li>
<li class="pending"><a href="/cookbook/soda-bread/">Soda Bread</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/sourdough/">Sourdough</a></li>
<li class="pending"><a href="/cookbook/sourdough-starter/">Sourdough Starter</a></li>
</ul>
</div>
<div class="cat">
<p class="cat-heading">Sweet</p>
<ul class="recipe-list">
<li class="pending"><a href="/cookbook/bakewell-tart/">Bakewell Tart</a></li>
<li class="pending"><a href="/cookbook/blondies/">Blondies</a></li>
<li><a href="/cookbook/brownie-blondie/">Brownie Blondie</a></li>
<li><a href="/cookbook/brownies/">Brownies</a></li>
<li><a href="/cookbook/buttermilk-pancakes/">Buttermilk Pancakes</a><span class="frz">❄</span></li>
<li><a href="/cookbook/carrot-cake/">Carrot Cake</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/cheesecake/">Cheesecake</a></li>
<li><a href="/cookbook/cookies/">Cookies</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/croissants/">Croissants</a></li>
<li><a href="/cookbook/flapjacks/">Flapjacks</a></li>
<li class="pending"><a href="/cookbook/french-toast/">French Toast</a></li>
<li class="pending"><a href="/cookbook/gingerbread-men/">Gingerbread Men</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/mille-feuille/">Mille-feuille</a></li>
<li class="pending"><a href="/cookbook/pain-au-chocolat/">Pain au Chocolat</a></li>
<li class="pending"><a href="/cookbook/scones/">Scones</a></li>
<li class="pending"><a href="/cookbook/sticky-toffee-pudding/">Sticky Toffee Pudding</a></li>
<li><a href="/cookbook/tottenham-cake/">Tottenham Cake</a></li>
<li><a href="/cookbook/victoria-sponge/">Victoria Sponge</a></li>
</ul>
</div>
<div class="cat">
<p class="cat-heading">Savoury</p>
<ul class="recipe-list">
<li class="pending"><a href="/cookbook/bowsers-big-bean-burrito/">Bowser's Big Bean Burrito</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/braised-short-ribs/">Braised Short Ribs</a></li>
<li><a href="/cookbook/breakfast-burritos/">Breakfast Burritos</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/buttermilk-fried-chicken/">Buttermilk Fried Chicken</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/cari-poulet/">Cari Poulet</a></li>
<li><a href="/cookbook/carnitas/">Carnitas</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/cheese-toastie/">Cheese Toastie</a></li>
<li class="pending"><a href="/cookbook/cheese-twists/">Cheese Twists</a></li>
<li class="pending"><a href="/cookbook/chicken-alfredo/">Chicken Alfredo</a></li>
<li class="pending"><a href="/cookbook/chicken-and-leek-pie/">Chicken and Leek Pie</a></li>
<li><a href="/cookbook/chicken-couscous-bowl/">Chicken Couscous Bowl</a></li>
<li class="pending"><a href="/cookbook/chicken-tagine/">Chicken Tagine</a></li>
<li><a href="/cookbook/confit-byaldi/">Confit Byaldi</a></li>
<li><a href="/cookbook/creamy-salmon-salad/">Creamy Salmon Salad</a></li>
<li><a href="/cookbook/enchiladas/">Enchiladas</a></li>
<li class="pending"><a href="/cookbook/french-onion-soup/">French Onion Soup</a></li>
<li class="pending"><a href="/cookbook/greek-pasta-salad/">Greek Pasta Salad</a></li>
<li><a href="/cookbook/green-goddess-pasta-salad/">Green Goddess Pasta Salad</a></li>
<li class="pending"><a href="/cookbook/italian-deli-pasta-salad/">Italian Deli Pasta Salad</a></li>
<li class="pending"><a href="/cookbook/jollof-rice/">Jollof Rice</a></li>
<li><a href="/cookbook/lime-cabbage-slaw/">Lime Cabbage Slaw</a></li>
<li class="pending"><a href="/cookbook/plantain-dodo/">Plantain (Dodo)</a></li>
<li class="pending"><a href="/cookbook/pot-roast-chicken-thighs/">Pot-Roast Chicken Thighs</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/quiche-lorraine/">Quiche Lorraine</a></li>
<li class="pending"><a href="/cookbook/ragu/">Ragù</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/roast-pork-loin/">Roast Pork Loin</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/sausage-plait/">Sausage Plait</a></li>
<li class="pending"><a href="/cookbook/sausage-rolls/">Sausage Rolls</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/steak-pie/">Steak Pie</a><span class="frz">❄</span></li>
<li><a href="/cookbook/tomato-soup/">Tomato Soup</a><span class="frz">❄</span></li>
</ul>
</div>
<div class="cat">
<p class="cat-heading">Cypriot</p>
<ul class="recipe-list">
<li class="pending"><a href="/cookbook/arkatena/">Arkatena</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/bourekia/">Bourekia</a></li>
<li class="pending"><a href="/cookbook/kleftiko/">Kleftiko</a></li>
<li class="pending"><a href="/cookbook/kolouri/">Kolouri</a></li>
<li class="pending"><a href="/cookbook/koupepia/">Koupepia</a></li>
<li class="pending"><a href="/cookbook/loukanika/">Loukanika</a></li>
<li class="pending"><a href="/cookbook/louvi/">Louvi</a></li>
<li class="pending"><a href="/cookbook/moussaka/">Moussaka</a></li>
<li class="pending"><a href="/cookbook/pastitsio/">Pastitsio</a></li>
<li class="pending"><a href="/cookbook/pourgouri-pilafi/">Pourgouri Pilafi</a></li>
<li><a href="/cookbook/souvla/">Souvla</a></li>
</ul>
</div>
<div class="cat">
<p class="cat-heading">Sauces &amp; Preserves</p>
<ul class="recipe-list">
<li class="pending"><a href="/cookbook/aji-verde/">Aji Verde</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/brown-sauce/">Brown Sauce</a></li>
<li><a href="/cookbook/cosmic-souvla-sauce/">Cosmic Souvla Sauce</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/fermented-hot-sauce/">Fermented Hot Sauce</a></li>
<li class="pending"><a href="/cookbook/hot-honey/">Hot Honey</a></li>
<li class="pending"><a href="/cookbook/jalapeno-relish/">Jalapeño Relish</a></li>
<li><a href="/cookbook/parsley-yoghurt/">Parsley Yoghurt</a></li>
<li class="pending"><a href="/cookbook/piccalilli/">Piccalilli</a></li>
<li><a href="/cookbook/pickled-red-onions/">Pickled Red Onions</a></li>
<li><a href="/cookbook/pickles/">Pickles</a></li>
<li class="pending"><a href="/cookbook/pikla/">Pikla</a></li>
<li class="pending"><a href="/cookbook/pink-turnip-pickle/">Pink Turnip Pickle</a></li>
<li class="pending"><a href="/cookbook/preserved-lemons/">Preserved Lemons</a></li>
<li class="pending"><a href="/cookbook/tomato-ketchup/">Tomato Ketchup</a></li>
<li class="pending"><a href="/cookbook/tsoursi/">Tsoursi</a></li>
</ul>
</div>
<div class="cat">
<p class="cat-heading">Drinks</p>
<ul class="recipe-list">
<li><a href="/cookbook/smoothies/">Smoothies</a></li>
</ul>
</div>
</div>

<script>
(function () {
  var input = document.getElementById('cookbook-search');
  if (!input) return;
  var cats = [].slice.call(document.querySelectorAll('.cat'));
  var items = [].slice.call(document.querySelectorAll('.recipe-list li'));
  items.forEach(function (li) {
    var a = li.querySelector('a');
    li._name = (a ? a.textContent : li.textContent).toLowerCase();
  });
  var nores = document.getElementById('cookbook-noresults');
  function filter() {
    var q = input.value.trim().toLowerCase();
    var any = false;
    items.forEach(function (li) {
      var show = !q || li._name.indexOf(q) !== -1;
      li.classList.toggle('is-hidden', !show);
      if (show) any = true;
    });
    cats.forEach(function (cat) {
      cat.classList.toggle('is-hidden', !cat.querySelector('.recipe-list li:not(.is-hidden)'));
    });
    if (nores) nores.style.display = any ? 'none' : 'block';
  }
  input.addEventListener('input', filter);
  // Reset to a clean, consistent state on every (re)visit, including Back via
  // the bfcache (where the input clears but the filtered DOM is restored stale).
  window.addEventListener('pageshow', function () { input.value = ''; filter(); });
})();
</script>
