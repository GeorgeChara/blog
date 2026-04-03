---
title: "From desktop to browser"
date: 2026-04-03
draft: false
---

Quite a few changes since the last post. It actually plays like a game and I have also configured a pipeline so that I can provide demos to play in a web browser.

## Running in the browser

The entire engine compiles to WebAssembly via Emscripten using the same source code, same OpenGL calls. Emscripten translates them to WebGL 2.0 automatically. The total download is under 1MB, for comparison the google homepage is about 1.5MB total size.

![Web & os pipelines](/images/devlog-002/web-pipeline.svg)

You can **[play the demo here](/posts/play-the-demo/)**. The rest of this post covers a few more changes I have made since the last.

## Abilities and damage numbers

Added some passive abilities, **QWER** keys are hotkeys for abilities in game and we currently have two equipped: 'Slam' and some kind of 'aura' which auto attacks (this is the blue square around the player).

![Abilities](/images/devlog-002/1.png)

Enemies show floating damage numbers on hit and kills chain into a combo counter shown in the centre of the screen.

![Damage numbers and combo counter](/images/devlog-002/2.png)

## Chain effects

Here I am just messing around with the idea that enemies can have a 'chain' like effect when they are killed.

![Abilities in action](/images/devlog-002/3.gif)

## Pinball

A lot is happening in this clip, but firstly we have added a bit of variety to how the 'mobs' spawn so they're not too uniform like before in their ring like configuration. I also added a new passive ability which is a pinball which bounces off the mobs speeding up until it eventually goes off screen. There are also some rough broken flippers at the bottom but I didn't bother to fix these as of yet. It might also be hard to tell from the low frame gif but I have added a subtle screen shake on larger group kills too giving it a satisfying feeling for multikills.

![Combat gameplay](/images/devlog-002/4.gif)

## Enemy variety

I added a few different enemies, smaller ones are more common with less health and the larger ones are rare with more health. As you survive longer, more large enemies will spawn adjusting to the players creep up in damage output.

![Enemy variety](/images/devlog-002/5.png)

## Chain lightning

Each ability is defined as a single struct in a catalog with a cooldown, damage, radius and effect type which allows me to add more 'basic' abilities easily.

```c
catalog_add((AbilityDef){
    .name = "Chain Lightning",
    .effect = EFFECT_CHAIN,
    .damage = 3.0f,
    .radius = 8.0f,
    .cooldown = 3.0f,
    .extra = { 4.0f }, // chain count
});
```

The default for lightning chain is set to 4 enemies but here it is in play with over 50. I set this to 50 in the demo so you can test it out but feel free to adjust and play with any of the abilities using the pause menu.

![Chain lightning and enemy hordes](/images/devlog-002/6.gif)
