---
title: "TITLE"
tags: []
toc: false
showreadingtime: false
layout: single
---

<!-- ============================================================
     SETTINGS  (delete this block once you're done)

     tags:  freezer | make-ahead | no-cook | vegetarian | vegan
            freezer also puts a blue ❄ next to the index link

     grey link -> blue link
            new recipes go in the cookbook GREY (not cooked yet).
            once you've actually made it:   blog-live SLUG
            to put it back grey:            blog-live SLUG --undo

     photos
            drop them in  _inbox/SLUG/  , crop in Preview, then:
            blog-img SLUG
            it prints the markdown, paste it where you want it

     publish
            blog-publish SLUG --cat savoury --subcat Chicken
            blog-publish --cats     lists every section
     ============================================================ -->

<style>
  main > h1:first-of-type { display: none; }
  .time { display: none; }
  h2::before { content: none !important; }
  .content pre { color: #000; }
  .terminal-nav { display: none; }
</style>

<h1>TITLE</h1>
<p style="color: #888; margin-top: -0.5em;">SUBTITLE, commas, no bullets, e.g. Cypriot pork bake, one pot, 1.5 hr, serves 4</p>

## Ingredients

<pre style="padding: 1em; border-radius: 4px; display: inline-block; margin: 0; color: #000;"><span style="color: #888;">Group</span>
ingredient       100g
another          2 tbsp

<span style="color: #888;">Another group</span>
something else   1 tsp
</pre>

<span style="display:block; color:#888; font-size:0.8em; margin-top:0.8em; border-left: 2px solid #E5DECF; padding-left: 0.6em;">Notes go here, functional only.<br>One sentence per line, separated by br tags.</span>

## Recipe

**1.** First step. Short imperative sentence.

**2.** Any step using 3 or more ingredients ends with a colon and lists them:

{{< ingr "flour=420g, water=320ml, salt=9g, yeast=2g" >}}

<span style="display:block; color:#888; font-size:0.8em; margin:0.2em 0 0.9em; border-left: 2px solid #E5DECF; padding-left: 0.6em;">A note under a step, when it earns its place.</span>

**3.** Third step.

<span style="display:block; color:#888; font-size:0.8em; margin-top:0.8em; border-left: 2px solid #E5DECF; padding-left: 0.6em;">Source: <a href="URL">Site Name</a>.</span>
