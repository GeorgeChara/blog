---
title: "Building a game and engine from scratch"
date: 2026-03-31
draft: false
---

Building a game from scratch. No Unity, no Unreal, no Godot. Just C, C++, and OpenGL. The project is codenamed **Coopla**, and the custom engine powering it is called **Terra**.

## Game, engine & libraries

The engine is written in C17 with OpenGL 3.3. No massive framework with a load of stuff we will never need. Just enough to get pixels on screen and a player moving through 3D space.

![Engine architecture](/images/devlog-001/engine-diagram.svg)

Game specific code on top, the engine in the middle handling rendering, input, camera, lighting and audio, and platform libraries at the bottom.

## First signs of life

The first milestone was getting the renderer working. A chequered floor and some cubes, each face tinted differently using vertex data (the simplest way to shade geometry without textures).

![First render](/images/devlog-001/first-vertexes.webp)

![Different angle](/images/devlog-001/first-vertexes-2.webp)

## Building the tools

After adding a lightbox and some other basics, I integrated [ImGui](https://github.com/ocornut/imgui): an open source C++ GUI library for building in-engine tools. I built a level editor with brush placement, an asset pipeline for importing 3D models (glTF format), and prop placement for dropping objects into the scene.

Here I'm stacking tower props at different scales to test the prop system.

![Small tower](/images/devlog-001/tower-edit.webp)

![Large tower](/images/devlog-001/tower-edit-2.webp)

## Physics & movement

The best way to tune in game movement is to just feel it while playing. Using the ImGui sliders I can easily adjust physics whilst I play until things feel right.

![Physics tuning panel with live CVars and performance bar](/images/devlog-001/physics.webp)

The movement system is based on Quake's air acceleration model, which means it supports strafe jumping. It's a bit rough at this point but you can see it working as the bar at the bottom tracks speed.

![Strafe jumping movement demo](/images/devlog-001/movement.webp)

## Developer console & debug tools

I built a Quake/Source-style developer console that drops down with the tilde key. It's useful for things like teleport, noclip, god mode, and direct CVar editing, all with tab autocomplete and command history.

![Developer console with command list](/images/devlog-001/command-mode.webp)

Here's everything open at once (performance graphs, game state, log viewer, etc.)

![All GUI panels open at once](/images/devlog-001/gui-menus.webp)

## Nextbot detour

I messed around with [nextbots](https://developer.valvesoftware.com/wiki/NextBot) (the AI system from Garry's Mod). Slowed the movement down, added fog, a torch, some pillars to hide behind, and had a nextbot chasing the player through a dark room.

![Dark room with fog, torch, and a nextbot](/images/devlog-001/6.webp)

## Zooming out

I started experimenting with procedurally generated rooms and started building a system that pieces together simple room templates and arranges them into a dungeon layout.

![Row of procedurally generated rooms from above](/images/devlog-001/7.webp)

![Closer look at the generated rooms](/images/devlog-001/8.webp)

Looking at the game from here made me think about controlling the character like an ARPG. This led to an isometric camera, click to move controls, and eventually a completely different game direction.

## Current state: ARPG prototype

The game has pivoted to an isometric ARPG, enemies swarm in and abilities fire on cooldowns but most of all at this stage, it's showcasing the engine's ability to adapt.

![ARPG prototype with isometric camera](/images/devlog-001/9.webp)
