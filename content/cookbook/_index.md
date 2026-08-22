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

  /* z-index:0 traps every recipe inside its own stacking context BELOW the
     search (z-index:30). A whole stacking context composites as one unit, so
     content physically cannot paint above the search — this is what kills the
     iOS Safari bug where recipes smeared above the sticky bar during scroll. */
  .cookbook { display: flex; gap: 3em; align-items: flex-start; position: relative; z-index: 0; }

  /* Desktop: search is a normal sticky element (works fine on desktop).
     display:contents makes the wrapper invisible to layout so the sticky
     element behaves as a direct child of the column. */
  .cb-searchwrap { display: contents; }
  /* Column so the chips sit inside the bar, above its bottom border, and read
     as part of the search rather than a separate strip below the line. */
  .cb-searchbar { position: sticky; top: 0; z-index: 30; background: var(--color-bg-primary); padding: 0.5em 0; margin-bottom: 1.3em; border-bottom: 1px solid var(--color-border); display: flex; flex-direction: column; }
  .cb-searchrow { display: flex; align-items: center; gap: 0.5em; }

  .cb-navwrap { position: sticky; top: 4em; flex: 0 0 120px; align-self: flex-start; padding-left: 0.3em; }
  .cb-nav { display: flex; flex-direction: column; gap: 0.55em; }
  .cb-nav a { color: #4169E1; text-decoration: none; align-self: flex-start; }
  .cb-nav a:hover { color: #2a50c8; border-bottom-color: #2a50c8; }
  .cb-nav a.is-hidden { display: none; }

  .cb-main { flex: 1 1 auto; min-width: 0; padding-left: 0.5em; }

  .cat { margin: 0 0 1.9em 0; scroll-margin-top: 4em; }
  .cat-heading { font-weight: bold; font-size: 1.05em; margin: 0 0 0.6em 0; color: #000; }

  .subcat { margin: 0 0 1.1em 0; }
  .subcat-heading { font-weight: bold; font-size: 0.85em; letter-spacing: 0.02em; color: #666; margin: 0 0 0.35em 0; }
  .subcat.is-hidden { display: none; }

  .recipe-list { list-style: none; padding: 0; margin: 0; }
  .recipe-list li { margin: 0.6em 0; }
  .recipe-list a { color: #4169E1; text-decoration: none; }
  .recipe-list a:hover { color: #2a50c8; border-bottom-color: #2a50c8; }
  .recipe-list li.pending a { color: #aaa; border-bottom-color: #e0d9d0; }
  .recipe-list li.pending a:hover { color: #888; border-bottom-color: #aaa; }
  .frz { color: #3f9fd4; font-size: 1em; margin-left: 0.35em; }

  .cookbook-search { flex: 1 1 0; min-width: 0; box-sizing: border-box; padding: 0.4em 0.7em; margin: 0; font-family: inherit; font-size: 16px; border: 1px solid #e0d9d0; border-radius: 6px; background: #fff; color: #555; }

  /* Tags toggle, sits inside the search bar on the right */
  .cb-tagbtn {
    flex: 0 0 auto; font-family: inherit; font-size: 0.75em; line-height: 1.4;
    padding: 0.4em 0.7em; border: 1px solid #e0d9d0; border-radius: 3px;
    background: #fff; color: #888; cursor: pointer; white-space: nowrap;
    transition: color .15s, border-color .15s;
  }
  .cb-tagbtn:hover { color: #555; border-color: #cfc6ba; }
  .cb-tagbtn.has-active { color: #4169E1; border-color: #4169E1; }
  .cb-chips.is-collapsed { display: none; }
  .cookbook-search::placeholder { color: #b3b3b3; font-size: 13px; }
  .cookbook-search:focus { outline: none; border-color: #4169E1; }
  .cat.is-hidden, .recipe-list li.is-hidden { display: none; }

  /* Tag chips. Click to filter, multiple chips are AND (recipe must have all).
     Deliberately outside .cb-searchbar so the mobile sticky logic is untouched. */
  .cb-chips { display: flex; flex-wrap: wrap; gap: 0.4em; margin: 0.6em 0 0.15em 0; }
  .cb-chip {
    font-family: inherit; font-size: 0.75em; line-height: 1.4;
    padding: 0.25em 0.7em; border: 1px solid #e0d9d0; border-radius: 3px;
    background: #fff; color: #888; cursor: pointer; transition: all .15s;
  }
  /* Each chip carries its own hue: coloured text at rest, filled when active.
     --c is the colour, --fg the text once it's filled. */
  .cb-chip { --c: #4169E1; --fg: #fff; }
  .cb-chip[data-tag="vegetarian"],
  .cb-chip[data-tag="vegan"]       { --c: #6aa84f; color: #6aa84f; }
  .cb-chip[data-tag]:hover { border-color: var(--c); }
  .cb-chip.is-active { background: var(--c); border-color: var(--c); color: var(--fg); }
  .cb-chip.is-empty { opacity: 0.35; cursor: default; }
  /* Forces a wrap so diet/storage and equipment are always separate rows,
     rather than whichever chips happen to fit on line one. */
  .cb-chip-break { flex-basis: 100%; height: 0; }
  .cookbook-noresults { display: none; color: #888; font-size: 0.9em; margin: 0 0 1.3em 0; }

  @media (max-width: 600px) {
    body { overflow-x: visible; }

    /* Mobile: the search sits normally at the top (breadcrumb stays put), then
       JS adds .stuck once you scroll past it. .stuck uses position:fixed (which
       works on iOS, unlike sticky) and the wrapper reserves the height so
       nothing jumps. It slides down as it pins. */
    .cb-searchwrap { display: block; }
    .cb-searchbar { position: static; margin: 0 0 1.2em; padding: 0.55em 0; }
    /* iOS doesn't fire scroll events mid-momentum, so the bar pins when the flick
       settles. A gentle fade + small slide softens that moment (a full-height
       slide read as a snap; no animation read as an abrupt pop). */
    .cb-searchbar.stuck {
      position: fixed; top: 0; left: 0; right: 0; margin: 0;
      padding: 0.55em var(--spacing-lg);
      animation: cb-slide-in 0.28s ease-out;
    }
    @keyframes cb-slide-in {
      from { opacity: 0; transform: translateY(-6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Single column; stretch so the recipe list fills the width */
    .cookbook { flex-direction: column; gap: 1em; align-items: stretch; }
    .cb-main { padding-left: 0; }
    /* Hide the section tabs on mobile — just the search */
    .cb-navwrap { display: none; }
    /* The forced diet/equipment split only reads well when each group fits one
       line. On a phone both groups wrap anyway, so the break just leaves a gap
       mid-row. Drop it and let all the chips flow evenly. */
    .cb-chip-break { display: none; }
    .cat { scroll-margin-top: 4.5em; }
  }
</style>

<div class="cb-searchwrap">
<div class="cb-searchbar">
<div class="cb-searchrow">
<input type="search" id="cookbook-search" class="cookbook-search" placeholder="Search recipes…" autocomplete="off" aria-label="Search recipes">
<button type="button" class="cb-tagbtn" id="cb-tagbtn" aria-expanded="false" aria-controls="cb-chips">tags</button>
</div>
<div class="cb-chips is-collapsed" id="cb-chips">
<button class="cb-chip" data-tag="freezer">❄ freezer</button>
<button class="cb-chip" data-tag="make-ahead">make ahead</button>
<button class="cb-chip" data-tag="vegetarian">vegetarian</button>
<button class="cb-chip" data-tag="vegan">vegan</button>
<button class="cb-chip" data-tag="no-cook">no cook</button>
<span class="cb-chip-break"></span>
<button class="cb-chip" data-tag="dutch-oven">dutch oven</button>
<button class="cb-chip" data-tag="cast-iron">cast iron</button>
<button class="cb-chip" data-tag="stand-mixer">stand mixer</button>
<button class="cb-chip" data-tag="microwave">microwave</button>
</div>
</div>
</div>

<p id="cookbook-noresults" class="cookbook-noresults">No recipes match that search.</p>

<div class="cookbook">

<div class="cb-navwrap">
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
</div>

<div class="cb-main">

<section id="signature" class="cat">
<p class="cat-heading">Signature</p>
<ul class="recipe-list">
<li data-tags="freezer"><a href="/cookbook/baguette/">Baguette</a><span class="frz">❄</span></li>
</ul>
</section>

<section id="bread" class="cat">
<p class="cat-heading">Bread</p>
<ul class="recipe-list">
<li data-tags="stand-mixer"><a href="/cookbook/bagels/">Bagels</a></li>
<li data-tags="dutch-oven"><a href="/cookbook/boule/">Boule</a></li>
<li class="pending" data-tags="freezer stand-mixer"><a href="/cookbook/brioche-buns/">Brioche Buns</a><span class="frz">❄</span></li>
<li class="pending" data-tags="vegetarian"><a href="/cookbook/cheese-potato-bread/">Cheese Potato Bread</a></li>
<li class="pending"><a href="/cookbook/cinnamon-swirls/">Cinnamon Swirls</a></li>
<li class="pending"><a href="/cookbook/crumpets/">Crumpets</a></li>
<li class="pending"><a href="/cookbook/english-muffins/">English Muffins</a></li>
<li class="pending" data-tags="stand-mixer"><a href="/cookbook/farata/">Farata</a></li>
<li data-tags="freezer make-ahead stand-mixer"><a href="/cookbook/flour-tortillas/">Flour Tortillas</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/focaccia/">Focaccia</a></li>
<li class="pending"><a href="/cookbook/hot-cross-buns/">Hot Cross Buns</a></li>
<li class="pending" data-tags="stand-mixer"><a href="/cookbook/iced-fingers/">Iced Fingers</a></li>
<li data-tags="dutch-oven freezer stand-mixer"><a href="/cookbook/lazy-boule/">Lazy Boule</a><span class="frz">❄</span></li>
<li class="pending" data-tags="freezer stand-mixer"><a href="/cookbook/milk-buns/">Milk Buns</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/pita/">Pita</a></li>
<li class="pending" data-tags="freezer"><a href="/cookbook/pupusas/">Pupusas</a><span class="frz">❄</span></li>
<li class="pending" data-tags="freezer"><a href="/cookbook/rye-loaf/">Rye Loaf</a><span class="frz">❄</span></li>
<li class="pending" data-tags="freezer stand-mixer"><a href="/cookbook/seeded-wholemeal-loaf/">Seeded Wholemeal Loaf</a><span class="frz">❄</span></li>
<li class="pending" data-tags="stand-mixer"><a href="/cookbook/shokupan/">Shokupan</a></li>
<li class="pending" data-tags="freezer"><a href="/cookbook/soda-bread/">Soda Bread</a><span class="frz">❄</span></li>
<li class="pending" data-tags="dutch-oven"><a href="/cookbook/sourdough/">Sourdough</a></li>
<li class="pending"><a href="/cookbook/sourdough-starter/">Sourdough Starter</a></li>
</ul>
</section>

<section id="basics" class="cat">
<p class="cat-heading">Basics</p>
<ul class="recipe-list">
<li class="pending" data-tags="freezer microwave"><a href="/cookbook/apple-sauce/">Apple Sauce</a><span class="frz">❄</span></li>
<li data-tags="freezer stand-mixer"><a href="/cookbook/butter/">Butter</a><span class="frz">❄</span></li>
<li data-tags="freezer"><a href="/cookbook/buttercream/">Buttercream</a><span class="frz">❄</span></li>
<li data-tags="freezer"><a href="/cookbook/chicken-marinade/">Chicken Marinade</a><span class="frz">❄</span></li>
<li data-tags="make-ahead vegetarian"><a href="/cookbook/egg-mayo/">Egg Mayo</a></li>
<li class="pending" data-tags="stand-mixer"><a href="/cookbook/fresh-pasta-dough/">Fresh Pasta Dough</a></li>
<li data-tags="freezer"><a href="/cookbook/hash-browns/">Hash Browns</a><span class="frz">❄</span></li>
<li class="pending" data-tags="freezer stand-mixer"><a href="/cookbook/mashed-potato/">Mashed Potato</a><span class="frz">❄</span></li>
<li class="pending" data-tags="freezer make-ahead microwave"><a href="/cookbook/quick-mash/">Quick Mash</a><span class="frz">❄</span></li>
<li data-tags="dutch-oven freezer microwave"><a href="/cookbook/rice/">Rice</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/rough-puff-pastry/">Rough Puff Pastry</a></li>
<li class="pending" data-tags="freezer"><a href="/cookbook/soffritto/">Soffritto</a><span class="frz">❄</span></li>
</ul>
</section>

<section id="sweet" class="cat">
<p class="cat-heading">Sweet</p>
<ul class="recipe-list">
<li class="pending"><a href="/cookbook/bakewell-tart/">Bakewell Tart</a></li>
<li data-tags="freezer vegetarian"><a href="/cookbook/banana-bread/">Banana Bread</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/blondies/">Blondies</a></li>
<li><a href="/cookbook/brownie-blondie/">Brownie Blondie</a></li>
<li data-tags="stand-mixer"><a href="/cookbook/brownies/">Brownies</a></li>
<li data-tags="freezer microwave stand-mixer"><a href="/cookbook/buttermilk-pancakes/">Buttermilk Pancakes</a><span class="frz">❄</span></li>
<li data-tags="freezer stand-mixer vegetarian"><a href="/cookbook/carrot-cake/">Carrot Cake</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/cheesecake/">Cheesecake</a></li>
<li data-tags="freezer stand-mixer"><a href="/cookbook/cookies/">Cookies</a><span class="frz">❄</span></li>
<li class="pending" data-tags="stand-mixer"><a href="/cookbook/croissants/">Croissants</a></li>
<li><a href="/cookbook/flapjacks/">Flapjacks</a></li>
<li class="pending"><a href="/cookbook/french-toast/">French Toast</a></li>
<li class="pending" data-tags="freezer stand-mixer vegetarian"><a href="/cookbook/gingerbread-men/">Gingerbread Men</a><span class="frz">❄</span></li>
<li class="pending" data-tags="stand-mixer vegetarian"><a href="/cookbook/matilda-chocolate-cake/">Matilda Chocolate Cake</a></li>
<li class="pending"><a href="/cookbook/mille-feuille/">Mille-feuille</a></li>
<li class="pending" data-tags="stand-mixer"><a href="/cookbook/pain-au-chocolat/">Pain au Chocolat</a></li>
<li class="pending"><a href="/cookbook/scones/">Scones</a></li>
<li class="pending" data-tags="cast-iron freezer stand-mixer vegetarian"><a href="/cookbook/skillet-cookie/">Skillet Cookie</a><span class="frz">❄</span></li>
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
<li class="pending" data-tags="dutch-oven freezer make-ahead"><a href="/cookbook/beef-shin-stew/">Beef Shin Stew</a><span class="frz">❄</span></li>
<li class="pending" data-tags="dutch-oven"><a href="/cookbook/braised-short-ribs/">Braised Short Ribs</a></li>
<li class="pending" data-tags="cast-iron"><a href="/cookbook/skillet-steak/">Skillet Steak</a></li>
<li data-tags="cast-iron"><a href="/cookbook/smash-burgers/">Smash Burgers</a></li>
<li class="pending" data-tags="freezer"><a href="/cookbook/steak-pie/">Steak Pie</a><span class="frz">❄</span></li>
</ul>
</div>

<div class="subcat">
<p class="subcat-heading">Chicken</p>
<ul class="recipe-list">
<li class="pending" data-tags="freezer microwave"><a href="/cookbook/buttermilk-fried-chicken/">Buttermilk Fried Chicken</a><span class="frz">❄</span></li>
<li class="pending" data-tags="dutch-oven"><a href="/cookbook/chicken-alfredo/">Chicken Alfredo</a></li>
<li class="pending"><a href="/cookbook/chicken-and-leek-pie/">Chicken and Leek Pie</a></li>
<li><a href="/cookbook/chicken-couscous-bowl/">Chicken Couscous Bowl</a></li>
<li class="pending" data-tags="dutch-oven"><a href="/cookbook/chicken-tagine/">Chicken Tagine</a></li>
<li class="pending"><a href="/cookbook/creamy-chicken-and-gnocchi/">Creamy Chicken and Gnocchi</a></li>
<li class="pending"><a href="/cookbook/greek-chicken-and-potatoes/">Greek Chicken and Potatoes</a></li>
<li><a href="/cookbook/lemon-butter-chicken-ravioli/">Lemon Butter Chicken Ravioli</a></li>
<li class="pending" data-tags="dutch-oven"><a href="/cookbook/pot-roast-chicken/">Pot Roast Chicken</a></li>
<li class="pending" data-tags="dutch-oven freezer"><a href="/cookbook/pot-roast-chicken-thighs/">Pot-Roast Chicken Thighs</a><span class="frz">❄</span></li>
</ul>
</div>

<div class="subcat">
<p class="subcat-heading">Curry</p>
<ul class="recipe-list">
<li class="pending" data-tags="dutch-oven freezer make-ahead"><a href="/cookbook/butter-chicken/">Butter Chicken</a><span class="frz">❄</span></li>
<li class="pending" data-tags="dutch-oven"><a href="/cookbook/cari-poulet/">Cari Poulet</a></li>
<li class="pending" data-tags="freezer make-ahead vegan"><a href="/cookbook/chana-saag/">Chana Saag</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/leftover-chicken-curry/">Leftover Chicken Curry</a></li>
<li class="pending" data-tags="freezer"><a href="/cookbook/thai-green-curry/">Thai Green Curry</a><span class="frz">❄</span></li>
</ul>
</div>

<div class="subcat">
<p class="subcat-heading">Fish</p>
<ul class="recipe-list">
<li data-tags="dutch-oven"><a href="/cookbook/baked-cod/">Baked Cod</a></li>
<li><a href="/cookbook/creamy-salmon-salad/">Creamy Salmon Salad</a></li>
<li class="pending" data-tags="cast-iron"><a href="/cookbook/mediterranean-cod/">Mediterranean Cod</a></li>
<li class="pending" data-tags="cast-iron make-ahead"><a href="/cookbook/miso-cod/">Miso Cod</a></li>
<li data-tags="cast-iron"><a href="/cookbook/soy-garlic-salmon/">Soy Garlic Salmon</a></li>
</ul>
</div>

<div class="subcat">
<p class="subcat-heading">Mexican</p>
<ul class="recipe-list">
<li class="pending" data-tags="freezer microwave"><a href="/cookbook/bowsers-big-bean-burrito/">Bowser's Big Bean Burrito</a><span class="frz">❄</span></li>
<li data-tags="freezer microwave"><a href="/cookbook/breakfast-burritos/">Breakfast Burritos</a><span class="frz">❄</span></li>
<li><a href="/cookbook/enchiladas/">Enchiladas</a></li>
<li class="pending" data-tags="cast-iron vegetarian"><a href="/cookbook/quesadilla/">Quesadilla</a></li>
<li class="pending" data-tags="cast-iron"><a href="/cookbook/steak-fajitas/">Steak Fajitas</a></li>
</ul>
</div>

<div class="subcat">
<p class="subcat-heading">Pasta</p>
<ul class="recipe-list">
<li class="pending"><a href="/cookbook/carbonara/">Carbonara</a></li>
<li class="pending" data-tags="dutch-oven"><a href="/cookbook/chicken-and-orzo/">Chicken and Orzo</a></li>
<li class="pending" data-tags="make-ahead"><a href="/cookbook/greek-pasta-salad/">Greek Pasta Salad</a></li>
<li class="pending" data-tags="make-ahead"><a href="/cookbook/green-goddess-pasta-salad/">Green Goddess Pasta Salad</a></li>
<li class="pending" data-tags="make-ahead"><a href="/cookbook/italian-deli-pasta-salad/">Italian Deli Pasta Salad</a></li>
<li class="pending" data-tags="dutch-oven freezer"><a href="/cookbook/pasta-with-tiny-meatballs/">Pasta with Tiny Meatballs</a><span class="frz">❄</span></li>
<li class="pending" data-tags="freezer"><a href="/cookbook/ragu/">Ragù</a><span class="frz">❄</span></li>
<li class="pending" data-tags="dutch-oven freezer make-ahead"><a href="/cookbook/sausage-ragu/">Sausage Ragu</a><span class="frz">❄</span></li>
<li class="pending" data-tags="cast-iron freezer"><a href="/cookbook/skillet-lasagna/">Skillet Lasagna</a><span class="frz">❄</span></li>
</ul>
</div>

<div class="subcat">
<p class="subcat-heading">Pork</p>
<ul class="recipe-list">
<li data-tags="dutch-oven freezer stand-mixer"><a href="/cookbook/carnitas/">Carnitas</a><span class="frz">❄</span></li>
<li class="pending" data-tags="freezer"><a href="/cookbook/roast-pork-loin/">Roast Pork Loin</a><span class="frz">❄</span></li>
<li class="pending" data-tags="dutch-oven freezer make-ahead"><a href="/cookbook/sausage-and-butter-bean-casserole/">Sausage and Butter Bean Casserole</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/sausage-plait/">Sausage Plait</a></li>
<li class="pending" data-tags="freezer"><a href="/cookbook/sausage-rolls/">Sausage Rolls</a><span class="frz">❄</span></li>
<li data-tags="dutch-oven make-ahead"><a href="/cookbook/scotch-eggs/">Scotch Eggs</a></li>
</ul>
</div>

<div class="subcat">
<p class="subcat-heading">Rice</p>
<ul class="recipe-list">
<li data-tags="dutch-oven"><a href="/cookbook/chicken-and-chorizo-rice/">Chicken and Chorizo Rice</a></li>
<li class="pending" data-tags="freezer make-ahead"><a href="/cookbook/chicken-biryani/">Chicken Biryani</a><span class="frz">❄</span></li>
<li class="pending" data-tags="dutch-oven"><a href="/cookbook/jollof-rice/">Jollof Rice</a></li>
<li class="pending" data-tags="freezer make-ahead vegetarian"><a href="/cookbook/mujadara/">Mujadara</a><span class="frz">❄</span></li>
<li class="pending" data-tags="dutch-oven"><a href="/cookbook/oven-pilaf/">Oven Pilaf</a></li>
<li class="pending" data-tags="dutch-oven vegetarian"><a href="/cookbook/tahdig/">Tahdig</a></li>
</ul>
</div>

<div class="subcat">
<p class="subcat-heading">Sandwiches</p>
<ul class="recipe-list">
<li data-tags="make-ahead"><a href="/cookbook/blt-baguettes/">BLT Baguettes</a></li>
<li><a href="/cookbook/cheese-toastie/">Cheese Toastie</a></li>
<li data-tags="cast-iron"><a href="/cookbook/cheesesteak/">Cheesesteak</a></li>
</ul>
</div>

<div class="subcat">
<p class="subcat-heading">Sides &amp; Veg</p>
<ul class="recipe-list">
<li class="pending"><a href="/cookbook/cheese-twists/">Cheese Twists</a></li>
<li data-tags="stand-mixer"><a href="/cookbook/confit-byaldi/">Confit Byaldi</a></li>
<li class="pending" data-tags="cast-iron freezer vegetarian"><a href="/cookbook/gnocchi-bake/">Gnocchi Bake</a><span class="frz">❄</span></li>
<li><a href="/cookbook/lime-cabbage-slaw/">Lime Cabbage Slaw</a></li>
<li class="pending"><a href="/cookbook/plantain-dodo/">Plantain (Dodo)</a></li>
<li class="pending"><a href="/cookbook/quiche-lorraine/">Quiche Lorraine</a></li>
<li class="pending" data-tags="vegetarian"><a href="/cookbook/shakshuka/">Shakshuka</a></li>
</ul>
</div>

<div class="subcat">
<p class="subcat-heading">Soups</p>
<ul class="recipe-list">
<li class="pending" data-tags="freezer make-ahead"><a href="/cookbook/chicken-noodle-soup/">Chicken Noodle Soup</a><span class="frz">❄</span></li>
<li class="pending" data-tags="freezer make-ahead vegan"><a href="/cookbook/fakes/">Fakes</a><span class="frz">❄</span></li>
<li class="pending" data-tags="dutch-oven"><a href="/cookbook/french-onion-soup/">French Onion Soup</a></li>
<li data-tags="dutch-oven freezer vegetarian"><a href="/cookbook/tomato-soup/">Tomato Soup</a><span class="frz">❄</span></li>
</ul>
</div>

<div class="subcat">
<p class="subcat-heading">Vegetarian</p>
<ul class="recipe-list">
<li class="pending" data-tags="dutch-oven freezer make-ahead vegan"><a href="/cookbook/gigantes-plaki/">Gigantes Plaki</a><span class="frz">❄</span></li>
<li class="pending" data-tags="dutch-oven vegetarian"><a href="/cookbook/halloumi-kleftiko/">Halloumi Kleftiko</a></li>
<li class="pending" data-tags="dutch-oven freezer vegan"><a href="/cookbook/mushroom-bourguignon/">Mushroom Bourguignon</a><span class="frz">❄</span></li>
<li class="pending" data-tags="dutch-oven freezer make-ahead vegan"><a href="/cookbook/ribollita/">Ribollita</a><span class="frz">❄</span></li>
<li class="pending" data-tags="vegan"><a href="/cookbook/whole-roasted-cauliflower/">Whole Roasted Cauliflower</a></li>
</ul>
</div>

</section>

<section id="cypriot" class="cat">
<p class="cat-heading">Cypriot</p>
<ul class="recipe-list">
<li class="pending" data-tags="dutch-oven freezer make-ahead"><a href="/cookbook/afelia/">Afelia</a><span class="frz">❄</span></li>
<li data-tags="freezer stand-mixer vegan"><a href="/cookbook/arkatena/">Arkatena</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/avgolemoni/">Avgolemoni</a></li>
<li class="pending" data-tags="stand-mixer"><a href="/cookbook/bourekia/">Bourekia</a></li>
<li class="pending" data-tags="dutch-oven make-ahead"><a href="/cookbook/giouvetsi/">Giouvetsi</a></li>
<li data-tags="dutch-oven"><a href="/cookbook/kleftiko/">Kleftiko</a></li>
<li class="pending"><a href="/cookbook/kolouri/">Kolouri</a></li>
<li><a href="/cookbook/koupepia/">Koupepia</a></li>
<li class="pending" data-tags="stand-mixer"><a href="/cookbook/loukanika/">Loukanika</a></li>
<li><a href="/cookbook/louvi/">Louvi</a></li>
<li data-tags="stand-mixer"><a href="/cookbook/moussaka/">Moussaka</a></li>
<li data-tags="stand-mixer"><a href="/cookbook/pastitsio/">Pastitsio</a></li>
<li><a href="/cookbook/pourgouri-pilafi/">Pourgouri Pilafi</a></li>
<li class="pending" data-tags="cast-iron vegetarian"><a href="/cookbook/saganaki/">Saganaki</a></li>
<li><a href="/cookbook/souvla/">Souvla</a></li>
<li class="pending" data-tags="dutch-oven freezer make-ahead"><a href="/cookbook/stifado/">Stifado</a><span class="frz">❄</span></li>
<li class="pending" data-tags="dutch-oven make-ahead"><a href="/cookbook/tavas/">Tavas</a></li>
</ul>
</section>

<section id="sauces" class="cat">
<p class="cat-heading">Sauces &amp; Preserves</p>
<ul class="recipe-list">
<li data-tags="freezer"><a href="/cookbook/aji-verde/">Aji Verde</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/brown-sauce/">Brown Sauce</a></li>
<li data-tags="freezer vegan"><a href="/cookbook/cosmic-souvla-sauce/">Cosmic Souvla Sauce</a><span class="frz">❄</span></li>
<li class="pending"><a href="/cookbook/fermented-hot-sauce/">Fermented Hot Sauce</a></li>
<li class="pending" data-tags="make-ahead"><a href="/cookbook/honey-chipotle-glaze/">Honey Chipotle Glaze</a></li>
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
<li data-tags="no-cook vegan"><a href="/cookbook/growing-cress/">Cress</a></li>
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
    li._tags = (li.getAttribute('data-tags') || '').split(' ').filter(Boolean);
  });
  var chips = [].slice.call(document.querySelectorAll('.cb-chip[data-tag]'));
  var chipRow = document.getElementById('cb-chips');
  var tagBtn = document.getElementById('cb-tagbtn');
  var active = [];
  // One button, two jobs: it opens the row when nothing is selected, and turns
  // into the clear control once something is. The count matters because the row
  // can be collapsed while filters are on.
  function syncTagBtn() {
    tagBtn.textContent = active.length ? 'clear (' + active.length + ')' : 'tags';
    tagBtn.classList.toggle('has-active', active.length > 0);
  }
  function clearTags() {
    active = [];
    chips.forEach(function (c) { c.classList.remove('is-active'); });
    syncTagBtn();
  }
  // Grey out chips no recipe carries, so the row never lies about what's there.
  chips.forEach(function (c) {
    var tag = c.getAttribute('data-tag');
    if (!items.some(function (li) { return li._tags.indexOf(tag) !== -1; })) {
      c.classList.add('is-empty');
      c.disabled = true;
    }
  });
  var nores = document.getElementById('cookbook-noresults');
  function hasVisible(el) { return !!el.querySelector('.recipe-list li:not(.is-hidden)'); }
  function filter() {
    var q = input.value.trim().toLowerCase();
    var any = false;
    items.forEach(function (li) {
      var show = (!q || li._name.indexOf(q) !== -1) &&
                 active.every(function (t) { return li._tags.indexOf(t) !== -1; });
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
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      var tag = c.getAttribute('data-tag');
      var i = active.indexOf(tag);
      if (i === -1) { active.push(tag); } else { active.splice(i, 1); }
      c.classList.toggle('is-active', i === -1);
      syncTagBtn();
      filter();
    });
  });
  tagBtn.addEventListener('click', function () {
    // Clearing takes priority, and leaves the row open so you can pick again.
    if (active.length) { clearTags(); filter(); return; }
    var open = chipRow.classList.toggle('is-collapsed') === false;
    tagBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  // Reset to a clean, consistent state on every (re)visit, including Back via
  // the bfcache (where the input clears but the filtered DOM is restored stale).
  window.addEventListener('pageshow', function () {
    input.value = '';
    clearTags();
    chipRow.classList.add('is-collapsed');
    tagBtn.setAttribute('aria-expanded', 'false');
    syncTagBtn();
    filter();
  });
})();
</script>

<script>
// Mobile: pin the search (position:fixed) once you scroll past it, release at top.
// The wrapper reserves the search's height while it's detached so nothing jumps.
(function () {
  var wrap = document.querySelector('.cb-searchwrap');
  var bar = document.querySelector('.cb-searchbar');
  if (!wrap || !bar) return;
  var stuck = false;
  function update() {
    if (window.innerWidth > 600) {
      if (stuck) { bar.classList.remove('stuck'); wrap.style.height = ''; stuck = false; }
      return;
    }
    var top = wrap.getBoundingClientRect().top;
    if (!stuck && top <= 0) {
      wrap.style.height = bar.offsetHeight + 'px'; // reserve space before detaching
      bar.classList.add('stuck');
      stuck = true;
    } else if (stuck && top > 0) {
      bar.classList.remove('stuck');
      wrap.style.height = '';
      stuck = false;
    }
  }
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
})();
</script>
