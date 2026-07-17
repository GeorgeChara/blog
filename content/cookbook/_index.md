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

  .cookbook { display: flex; gap: 3em; align-items: flex-start; }

  .cb-nav { position: sticky; top: 1.5em; flex: 0 0 120px; display: flex; flex-direction: column; gap: 0.55em; }
  .cb-nav a { color: #4169E1; text-decoration: none; border-bottom: 1px solid #c5ccee; align-self: flex-start; }
  .cb-nav a:hover { color: #2a50c8; border-bottom-color: #2a50c8; }
  .cb-nav a.is-hidden { display: none; }

  .cb-main { flex: 1 1 auto; min-width: 0; }

  .cat { margin: 0 0 1.9em 0; scroll-margin-top: 1em; }
  .cat-heading { font-weight: bold; font-size: 1.05em; margin: 0 0 0.6em 0; color: #000; }

  .subcat { margin: 0 0 1.1em 0; }
  .subcat-heading { font-weight: bold; font-size: 0.85em; letter-spacing: 0.02em; color: #666; margin: 0 0 0.35em 0; }
  .subcat.is-hidden { display: none; }

  .recipe-list { list-style: none; padding: 0; margin: 0; }
  .recipe-list li { margin: 0.6em 0; }
  .recipe-list a { color: #4169E1; text-decoration: none; border-bottom: 1px solid #c5ccee; }
  .recipe-list a:hover { color: #2a50c8; border-bottom-color: #2a50c8; }
  .recipe-list li.pending a { color: #aaa; border-bottom-color: #e0d9d0; }
  .recipe-list li.pending a:hover { color: #888; border-bottom-color: #aaa; }
  .frz { color: #3f9fd4; font-size: 1em; margin-left: 0.35em; }

  .cookbook-search { width: 100%; box-sizing: border-box; padding: 0.4em 0.7em; margin: 0 0 1.3em 0; font-family: inherit; font-size: 16px; border: 1px solid #e0d9d0; border-radius: 6px; background: #fff; color: #555; }
  .cookbook-search::placeholder { color: #b3b3b3; font-size: 13px; }
  .cookbook-search:focus { outline: none; border-color: #4169E1; }
  .cat.is-hidden, .recipe-list li.is-hidden { display: none; }
  .cookbook-noresults { display: none; color: #888; font-size: 0.9em; margin: 0 0 1.3em 0; }

  @media (max-width: 600px) {
    .cookbook { flex-direction: column; gap: 1.2em; }
    .cb-nav { position: static; flex-direction: row; flex-wrap: wrap; gap: 0.5em 1.1em; flex-basis: auto; }
  }
</style>

<input type="search" id="cookbook-search" class="cookbook-search" placeholder="Search recipes…" autocomplete="off" aria-label="Search recipes">
<p id="cookbook-noresults" class="cookbook-noresults">No recipes match that search.</p>

<div class="cookbook">

<nav class="cb-nav">
<a href="#signature">Signature</a>
<a href="#bread">Bread</a>
<a href="#basics">Basics</a>
<a href="#sweet">Sweet</a>
<a href="#savoury">Savoury</a>
<a href="#cypriot">Cypriot</a>
<a href="#sauces">Sauces</a>
<a href="#drinks">Drinks</a>
<a href="#growing">Growing</a>
</nav>

<div class="cb-main">

<section id="signature" class="cat">
<p class="cat-heading">Signature</p>
<ul class="recipe-list">
<li><a href="/cookbook/baguette/">Baguette</a><span class="frz">❄</span></li>
</ul>
</section>

<section id="bread" class="cat">
<p class="cat-heading">Bread</p>
<ul class="recipe-list">
<li><a href="/cookbook/bagels/">Bagels</a></li>
<li><a href="/cookbook/boule/">Boule</a></li>
<li class="pending"><a href="/cookbook/brioche-buns/">Brioche Buns</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/cheese-potato-bread/">Cheese Potato Bread</a></li>
<li class="pending"><a href="/cookbook/cinnamon-swirls/">Cinnamon Swirls</a></li>
<li class="pending"><a href="/cookbook/crumpets/">Crumpets</a></li>
<li class="pending"><a href="/cookbook/english-muffins/">English Muffins</a></li>
<li class="pending"><a href="/cookbook/farata/">Farata</a></li>
<li><a href="/cookbook/flour-tortillas/">Flour Tortillas</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/focaccia/">Focaccia</a></li>
<li class="pending"><a href="/cookbook/hot-cross-buns/">Hot Cross Buns</a></li>
<li class="pending"><a href="/cookbook/iced-fingers/">Iced Fingers</a></li>
<li><a href="/cookbook/lazy-boule/">Lazy Boule</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/milk-buns/">Milk Buns</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/pita/">Pita</a></li>
<li class="pending"><a href="/cookbook/pupusas/">Pupusas</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/rye-loaf/">Rye Loaf</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/seeded-wholemeal-loaf/">Seeded Wholemeal Loaf</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/shokupan/">Shokupan</a></li>
<li class="pending"><a href="/cookbook/soda-bread/">Soda Bread</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/sourdough/">Sourdough</a></li>
<li class="pending"><a href="/cookbook/sourdough-starter/">Sourdough Starter</a></li>
</ul>
</section>

<section id="basics" class="cat">
<p class="cat-heading">Basics</p>
<ul class="recipe-list">
<li class="pending"><a href="/cookbook/apple-sauce/">Apple Sauce</a><span class="frz">❄</span></li>
<li><a href="/cookbook/butter/">Butter</a><span class="frz">❄</span></li>
<li><a href="/cookbook/buttercream/">Buttercream</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/chicken-marinade/">Chicken Marinade</a><span class="frz">❄</span></li>
<li><a href="/cookbook/egg-mayo/">Egg Mayo</a></li>
<li class="pending"><a href="/cookbook/fresh-pasta-dough/">Fresh Pasta Dough</a></li>
<li><a href="/cookbook/hash-browns/">Hash Browns</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/mashed-potato/">Mashed Potato</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/rice/">Rice</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/rough-puff-pastry/">Rough Puff Pastry</a></li>
<li class="pending"><a href="/cookbook/soffritto/">Soffritto</a><span class="frz">❄</span></li>
</ul>
</section>

<section id="sweet" class="cat">
<p class="cat-heading">Sweet</p>
<ul class="recipe-list">
<li class="pending"><a href="/cookbook/bakewell-tart/">Bakewell Tart</a></li>
<li><a href="/cookbook/banana-bread/">Banana Bread</a><span class="frz">❄</span></li>
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
<li class="pending"><a href="/cookbook/skillet-cookie/">Skillet Cookie</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/sticky-toffee-pudding/">Sticky Toffee Pudding</a></li>
<li><a href="/cookbook/tottenham-cake/">Tottenham Cake</a></li>
<li><a href="/cookbook/victoria-sponge/">Victoria Sponge</a></li>
</ul>
</section>

<section id="savoury" class="cat">
<p class="cat-heading">Savoury</p>

<div class="subcat">
<p class="subcat-heading">Beef</p>
<ul class="recipe-list">
<li class="pending"><a href="/cookbook/braised-short-ribs/">Braised Short Ribs</a></li>
<li class="pending"><a href="/cookbook/skillet-steak/">Skillet Steak</a></li>
<li class="pending"><a href="/cookbook/smash-burgers/">Smash Burgers</a></li>
<li class="pending"><a href="/cookbook/steak-pie/">Steak Pie</a><span class="frz">❄</span></li>
</ul>
</div>

<div class="subcat">
<p class="subcat-heading">Chicken</p>
<ul class="recipe-list">
<li class="pending"><a href="/cookbook/buttermilk-fried-chicken/">Buttermilk Fried Chicken</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/cari-poulet/">Cari Poulet</a></li>
<li class="pending"><a href="/cookbook/chicken-alfredo/">Chicken Alfredo</a></li>
<li class="pending"><a href="/cookbook/chicken-and-leek-pie/">Chicken and Leek Pie</a></li>
<li><a href="/cookbook/chicken-couscous-bowl/">Chicken Couscous Bowl</a></li>
<li class="pending"><a href="/cookbook/chicken-tagine/">Chicken Tagine</a></li>
<li><a href="/cookbook/lemon-butter-chicken-ravioli/">Lemon Butter Chicken Ravioli</a></li>
<li class="pending"><a href="/cookbook/pot-roast-chicken-thighs/">Pot-Roast Chicken Thighs</a><span class="frz">❄</span></li>
</ul>
</div>

<div class="subcat">
<p class="subcat-heading">Fish</p>
<ul class="recipe-list">
<li class="pending"><a href="/cookbook/baked-cod/">Baked Cod</a></li>
<li><a href="/cookbook/creamy-salmon-salad/">Creamy Salmon Salad</a></li>
<li class="pending"><a href="/cookbook/mediterranean-cod/">Mediterranean Cod</a></li>
<li class="pending"><a href="/cookbook/miso-cod/">Miso Cod</a></li>
<li class="pending"><a href="/cookbook/soy-garlic-salmon/">Soy Garlic Salmon</a></li>
</ul>
</div>

<div class="subcat">
<p class="subcat-heading">Mexican</p>
<ul class="recipe-list">
<li class="pending"><a href="/cookbook/bowsers-big-bean-burrito/">Bowser's Big Bean Burrito</a><span class="frz">❄</span></li>
<li><a href="/cookbook/breakfast-burritos/">Breakfast Burritos</a><span class="frz">❄</span></li>
<li><a href="/cookbook/enchiladas/">Enchiladas</a></li>
<li class="pending"><a href="/cookbook/quesadilla/">Quesadilla</a></li>
</ul>
</div>

<div class="subcat">
<p class="subcat-heading">Pasta</p>
<ul class="recipe-list">
<li class="pending"><a href="/cookbook/carbonara/">Carbonara</a></li>
<li class="pending"><a href="/cookbook/greek-pasta-salad/">Greek Pasta Salad</a></li>
<li class="pending"><a href="/cookbook/green-goddess-pasta-salad/">Green Goddess Pasta Salad</a></li>
<li class="pending"><a href="/cookbook/italian-deli-pasta-salad/">Italian Deli Pasta Salad</a></li>
<li class="pending"><a href="/cookbook/ragu/">Ragù</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/skillet-lasagna/">Skillet Lasagna</a><span class="frz">❄</span></li>
</ul>
</div>

<div class="subcat">
<p class="subcat-heading">Pork</p>
<ul class="recipe-list">
<li><a href="/cookbook/carnitas/">Carnitas</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/roast-pork-loin/">Roast Pork Loin</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/sausage-plait/">Sausage Plait</a></li>
<li class="pending"><a href="/cookbook/sausage-rolls/">Sausage Rolls</a><span class="frz">❄</span></li>
<li><a href="/cookbook/scotch-eggs/">Scotch Eggs</a></li>
</ul>
</div>

<div class="subcat">
<p class="subcat-heading">Sandwiches</p>
<ul class="recipe-list">
<li><a href="/cookbook/blt-baguettes/">BLT Baguettes</a></li>
<li class="pending"><a href="/cookbook/cheese-toastie/">Cheese Toastie</a></li>
<li><a href="/cookbook/cheesesteak/">Cheesesteak</a></li>
</ul>
</div>

<div class="subcat">
<p class="subcat-heading">Sides &amp; Veg</p>
<ul class="recipe-list">
<li class="pending"><a href="/cookbook/cheese-twists/">Cheese Twists</a></li>
<li><a href="/cookbook/confit-byaldi/">Confit Byaldi</a></li>
<li class="pending"><a href="/cookbook/gnocchi-bake/">Gnocchi Bake</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/jollof-rice/">Jollof Rice</a></li>
<li><a href="/cookbook/lime-cabbage-slaw/">Lime Cabbage Slaw</a></li>
<li class="pending"><a href="/cookbook/plantain-dodo/">Plantain (Dodo)</a></li>
<li class="pending"><a href="/cookbook/quiche-lorraine/">Quiche Lorraine</a></li>
</ul>
</div>

<div class="subcat">
<p class="subcat-heading">Soups</p>
<ul class="recipe-list">
<li class="pending"><a href="/cookbook/french-onion-soup/">French Onion Soup</a></li>
<li><a href="/cookbook/tomato-soup/">Tomato Soup</a><span class="frz">❄</span></li>
</ul>
</div>

</section>

<section id="cypriot" class="cat">
<p class="cat-heading">Cypriot</p>
<ul class="recipe-list">
<li><a href="/cookbook/arkatena/">Arkatena</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/avgolemoni/">Avgolemoni</a></li>
<li class="pending"><a href="/cookbook/bourekia/">Bourekia</a></li>
<li class="pending"><a href="/cookbook/kleftiko/">Kleftiko</a></li>
<li class="pending"><a href="/cookbook/kolouri/">Kolouri</a></li>
<li class="pending"><a href="/cookbook/koupepia/">Koupepia</a></li>
<li class="pending"><a href="/cookbook/loukanika/">Loukanika</a></li>
<li class="pending"><a href="/cookbook/louvi/">Louvi</a></li>
<li class="pending"><a href="/cookbook/moussaka/">Moussaka</a></li>
<li class="pending"><a href="/cookbook/pastitsio/">Pastitsio</a></li>
<li class="pending"><a href="/cookbook/pourgouri-pilafi/">Pourgouri Pilafi</a></li>
<li class="pending"><a href="/cookbook/saganaki/">Saganaki</a></li>
<li><a href="/cookbook/souvla/">Souvla</a></li>
</ul>
</section>

<section id="sauces" class="cat">
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
</section>

<section id="drinks" class="cat">
<p class="cat-heading">Drinks</p>
<ul class="recipe-list">
<li><a href="/cookbook/smoothies/">Smoothies</a></li>
</ul>
</section>

<section id="growing" class="cat">
<p class="cat-heading">Growing</p>
<ul class="recipe-list">
<li><a href="/cookbook/growing-cress/">Cress</a></li>
</ul>
</section>

</div>
</div>

<script>
(function () {
  var input = document.getElementById('cookbook-search');
  if (!input) return;
  var cats = [].slice.call(document.querySelectorAll('.cat'));
  var subcats = [].slice.call(document.querySelectorAll('.subcat'));
  var navlinks = [].slice.call(document.querySelectorAll('.cb-nav a'));
  var items = [].slice.call(document.querySelectorAll('.recipe-list li'));
  items.forEach(function (li) {
    var a = li.querySelector('a');
    li._name = (a ? a.textContent : li.textContent).toLowerCase();
  });
  var nores = document.getElementById('cookbook-noresults');
  function hasVisible(el) { return !!el.querySelector('.recipe-list li:not(.is-hidden)'); }
  function filter() {
    var q = input.value.trim().toLowerCase();
    var any = false;
    items.forEach(function (li) {
      var show = !q || li._name.indexOf(q) !== -1;
      li.classList.toggle('is-hidden', !show);
      if (show) any = true;
    });
    subcats.forEach(function (sc) { sc.classList.toggle('is-hidden', !hasVisible(sc)); });
    cats.forEach(function (cat) { cat.classList.toggle('is-hidden', !hasVisible(cat)); });
    navlinks.forEach(function (a) {
      var target = document.querySelector(a.getAttribute('href'));
      a.classList.toggle('is-hidden', !target || target.classList.contains('is-hidden'));
    });
    if (nores) nores.style.display = any ? 'none' : 'block';
  }
  input.addEventListener('input', filter);
  // Reset to a clean, consistent state on every (re)visit, including Back via
  // the bfcache (where the input clears but the filtered DOM is restored stale).
  window.addEventListener('pageshow', function () { input.value = ''; filter(); });
})();
</script>
