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
  - Bread/dough recipes lead with hydration %, e.g. `70% hydration, 2.5 hr, 2lb tin, makes 1`
    (hydration = (water + milk + buttermilk) ÷ flour; eggs, butter, oil, honey, seeds don't count)
    Skip it where it isn't meaningful: sweet enriched doughs, batters (crumpets), masa (pupusas)
- Step dropdowns: use `<details><summary>show photo</summary>` or `show video`

## Recipe tags (frontmatter)
Every recipe carries a `tags:` array in frontmatter. This is the source of truth for
sorting/filtering the cookbook later, so set it accurately when adding a recipe.

Controlled vocabulary (extend only when there's a real need):
- `quick` — 15 minutes or less, start to finish
- `freezer` — freezes well
- `make-ahead` — keeps well in the fridge for batch / meal prep
- `no-cook` — no hob or oven
- `vegetarian`, `vegan` — dietary

```yaml
tags: [quick, freezer, vegetarian]
```

When a recipe is `quick` or `freezer`, also add the matching icon in the cookbook index
(see below). The frontmatter tag is the source of truth; the icons will eventually be
generated from it.

Tag links are hidden on the page via `.terms-list { display: none }` in
`themes/shibui/assets/css/custom.css`. Tags still power the `/tags/` pages and the index
icons, they just don't render on the recipe itself.

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

## Cookbook index (`/content/cookbook/_index.md`)
- Hand-maintained, grouped by category (Bread, Sweet, Savoury, Cypriot, Sauces & Preserves)
- Each recipe is an `<li>`: published = normal link, pending/unwritten = `<li class="pending">` (greyed out)
- Keep each category alphabetical when adding a recipe
- Icons after the link mirror the recipe's frontmatter tags:
  - `freezer` → `<span class="frz">❄</span>`
  - `quick` → `<span class="clk">🕐</span>`
