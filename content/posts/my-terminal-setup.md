---
title: "My terminal setup: zellij, neovim, Claude, and Hacker News in one window"
date: 2026-04-17
draft: true
---

I spent a Friday evening ripping every GUI out of my dev workflow. No VS Code, no browser tabs for Hacker News, no separate terminal windows for git and the app I'm building. Just one Zellij session with four panes that open in the same layout every time.

Here's what's in it and why.

## The layout

Zellij is a terminal multiplexer like tmux, but with sane defaults and a config you don't need to Google every time you edit it. I've set mine up as a **strict DWM-style master-stack tile**: one big pane on the right (the "master"), everything else stacked vertically on the left.

```
┌─────────────┬─────────────────┐
│  neovim     │                 │
│  (nvim-tree)│                 │
├─────────────┤    Claude Code  │
│  zsh        │                 │
├─────────────┤                 │
│  clx (HN)   │                 │
└─────────────┴─────────────────┘
```

Left-top gets my code editor, left-middle is a shell for quick commands, left-bottom is a live Hacker News feed, and the whole right side is Claude Code for pair programming. `Alt+n` adds a new pane at the bottom of the left stack; new panes can never land under the master. No thinking required.

## Neovim, not VS Code

I switched from VS Code because I wanted my editor to live inside the terminal multiplexer, not in its own window that I'd have to Alt-Tab to. Neovim was the obvious choice, but the default file tree plugin — **NERDTree** — has a few problems:

- It forgets which folders you had expanded every time you open a file
- It's effectively unmaintained
- On `nvim .` it fights netrw for control of the directory listing

I replaced it with **nvim-tree.lua**. State persists, directory arguments work natively, and the terminal cursor blinks *inside the tree* less than in NERDTree (hiding it entirely took some DECTCEM escape-sequence trickery — another post).

I also moved the leader key from `\` to `<Space>`. Closing a buffer is now `<Space>x` instead of `\x`. Less reach, more fingers-on-home-row. The `vim-bbye` plugin makes `:Bdelete` safer than vanilla `:bdelete` — it doesn't close the whole window when you kill the last buffer.

## Zellij: DWM rules for the terminal

I like [DWM's](https://dwmx.org/) window management model: one master pane gets most of the real estate, everything else stacks on the side, and keybindings to shuffle things around. Zellij can do this with a `swap_tiled_layout`, but by default new panes split whatever pane you're focused on — so pressing `Alt+n` from the master would cut the master in half.

I fixed that by binding `Alt+n` to a compound action:

```kdl
bind "Alt n" { MoveFocus "Left"; MoveFocus "Down"; MoveFocus "Down";
               MoveFocus "Down"; MoveFocus "Down"; NewPane "Down"; }
```

Focus snaps left (to the stack), then down-down-down-down (no-ops at the edge, so it lands at the very bottom), then splits. New panes now deterministically land at the bottom of the left stack no matter where I was focused.

I also capped the stack at 5 panes by only defining `swap_tiled_layout` templates up to `max_panes=5`. Zellij's "can't split" error naturally triggers past that, which is fine — past 5 panes in a 40% column is unreadable anyway.

## Hacker News in a terminal pane: clx

The left-bottom pane runs **`clx`** — a terminal HN client I aliased as `news`. It fits in a small pane, updates on demand, and — most importantly — isn't a browser tab that'll tempt me into reading comments when I should be shipping. If a post genuinely needs more than a title's worth of attention I can open it, but the friction is the point.

## Claude Code on the right

The 60% master pane always opens Claude Code. It's where I rubber-duck, where I ask for help implementing features, and occasionally where I just vent about a GL bug until I type my way into the fix.

Running Claude in the terminal instead of a web app means I can pass it files by dragging them into the pane, paste `:read`-style context directly from nvim, and most importantly — it never steals keyboard focus from my editor. It's adjacent, not invasive.

## Dotfiles and stow

All of this is configured from one git repo (`~/programming/dotfiles`) managed with **GNU Stow**. Stow doesn't touch git — it just symlinks `dotfiles/nvim/.config/nvim/init.vim` to `~/.config/nvim/init.vim`, so there's exactly one file per config, not a "live copy" and a "repo copy" that drift.

Bootstrap on a new machine:

```bash
git clone git@github.com:me/dotfiles.git ~/programming/dotfiles
cd ~/programming/dotfiles
brew install stow
stow --target=$HOME --ignore='\.old$' nvim zellij zsh
```

Four commands and I've got my full environment.

## What it feels like

Honestly: focused. One window, predictable layout, instantly restored after a reboot, zero open browser tabs. The cost was one evening of config-fiddling and a couple of small engine-adjacent fixes (nvim-tree compat, zellij pane rules). The benefit is that my dev loop now fits in a single glance.

If you're already comfortable in a terminal, the jump from GUI editors to this kind of setup is lower than you'd think.
