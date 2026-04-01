---
title: "Building a game and engine from scratch"
date: 2026-03-31
draft: false
---

Building a game from scratch. No Unity, no Unreal, no Godot. Just C, C++, and OpenGL. The project is codenamed **Coopla**, and the custom engine powering it is called **Terra**.

## Game, engine & libraries

The engine is written in C17 with OpenGL 3.3. No massive framework, no bloated dependency tree. Just enough to get pixels on screen and a player moving through 3D space.

![Engine architecture](/images/devlog-001/engine-diagram.svg)

Game specific code on top, the engine in the middle handling rendering, input, camera, lighting and audio, and platform libraries at the bottom.

## First signs of life

The first milestone was getting the renderer working and hooked up to the game. Just a chequered floor and some coloured cubes. Each face is a different colour using vertex colours, which is the simplest way to get colour on screen without textures. Terra + Coopla were working: shaders compiling, camera moving, game loop ticking.

![First render — coloured cubes on a chequered floor](/images/devlog-001/first-vertexes.png)

![Different angle — each face of the cube has a different vertex colour](/images/devlog-001/first-vertexes-2.png)

## Building the tools

After adding a lightbox and some other basics, I integrated [ImGui](https://github.com/ocornut/imgui): an open source C++ GUI library for building in-engine tools. I built a level editor with brush placement, an asset pipeline for importing 3D models (glTF format), and prop placement for dropping objects into the scene.

Here I'm stacking tower props at different scales to test the prop system.

![Small tower](/images/devlog-001/tower-edit.png)

![Large tower](/images/devlog-001/tower-edit-2.png)

## Physics & movement

The best way to tune movement is to feel it while playing. I'm using the ImGui sliders I set up earlier to adjust physics variables in real time without ever leaving the game.

![Physics tuning panel with live CVars and performance bar](/images/devlog-001/physics.png)

The movement system is based on Quake's air acceleration model, which means it supports strafe jumping. It's a bit rough at this point but you can see it working as the bar at the bottom tracks speed.

![Strafe jumping movement demo](/images/devlog-001/movement.gif)

## Developer console & debug tools

I built a Quake/Source-style developer console that drops down with the tilde key. It's useful for things like teleport, noclip, god mode, and direct CVar editing, all with tab autocomplete and command history.

![In-game developer console with command list](/images/devlog-001/command-mode.png)

Here's everything open at once: performance graphs, CVar sliders, brush editor, game state, log viewer, and level save/load.

![All GUI panels open at once](/images/devlog-001/gui-menus.png)

## Nextbot detour

I messed around with [nextbots](https://developer.valvesoftware.com/wiki/NextBot) (the AI system from Garry's Mod). Slowed the movement down, added fog, a torch, some pillars to hide behind, and had a nextbot chasing the player through a dark room.

![Dark room with fog, torch, and a nextbot](/images/devlog-001/6.png)

## Zooming out

I started experimenting with procedurally generated rooms and started building a system that pieces together simple room templates and arranges them into a dungeon layout.

![Row of procedurally generated rooms from above](/images/devlog-001/7.png)

![Closer look at the generated rooms](/images/devlog-001/8.png)

Looking at the game from here made me think about controlling the character like an ARPG. That led to an isometric camera, click-to-move controls, and eventually a completely different game direction.

## Current state: ARPG prototype

The game has pivoted to an isometric ARPG, enemies swarm in and abilities fire on cooldowns.

![ARPG prototype with isometric camera](/images/devlog-001/9.png)
