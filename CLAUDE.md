# Blog – Claude Rules

## Site
- Hugo static site, theme: shibui, hosted on GitHub Pages
- Content: `/content/`, static images: `/static/images/`
- Run locally: `hugo server --port 1313`

## Images
- All images must be WebP, max 1200px wide, quality 82 (`cwebp -q 82`)
- Convert: HEIF → `sips -s format png` → Pillow P3→sRGB ICC conversion → `cwebp`
- Animated clips: `ffmpeg` palette GIF → `gif2webp -lossy -q 80`
- The pre-commit hook in `.git/hooks/pre-commit` auto-converts staged PNG/JPG to WebP

## Writing style
- No em dashes (—) anywhere. Use a comma, colon, or split into two sentences instead.

## Recipe pages
- Layout: `layout: single`, hide h1/time/terminal-nav via inline `<style>`
- Subtitle format: `45 min bake, 180°C, 23cm square tin` — commas, no bullets
  - Keep `recipe vX.Y` prefix only for versioned/adjusted recipes (e.g. baguette)
- Step dropdowns: use `<details><summary>show photo</summary>` or `show video`

## Ingredient blocks — standard format
Use a `<pre>` block (inline-block, same padding/border as other recipes).
Two columns only: ingredient name | amount. Left-align both.
- Clean short names — no parenthetical specs in the name column
- All amounts start at the same column (pad with spaces)
- If a note is needed (e.g. "Use strong white bread flour", "reserve 25g for step 5"),
  put it as a grey callout below the pre block:
  `<span style="display:block; color:#888; font-size:0.8em; margin-top:0.8em; border-left: 2px solid #E5DECF; padding-left: 0.6em;">...</span>`
- Multiple notes: separate with `<br>`, one sentence per line
- No third column, no inline notes inside the pre block

Example:
```
flour     500g
water     320ml
salt      9g
yeast     2g
```

## Baking index (`/content/baking/_index.md`)
- Main list (published recipes): alphabetical order, with `— time` meta
- "to make" list (pending): alphabetical order, greyed out links, no meta
- Both lists must stay alphabetical when adding new recipes
