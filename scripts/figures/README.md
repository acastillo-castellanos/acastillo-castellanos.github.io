# Figure scripts

Plots embedded in blog posts are generated here rather than copied in from
elsewhere, so that every figure shares one visual language and can be
regenerated when the underlying data changes.

## Running

matplotlib and h5py are not website dependencies — pull them in per run:

```bash
uv run --with matplotlib --with h5py --with numpy \
    python scripts/figures/kt94_tongues.py
```

Output goes to `src/content/blog/images/`. Those PNGs are referenced
relatively from the posts (`![alt](./images/name.png)`), which is what lets
Astro optimize them to WebP and stamp width/height at build time. Reference
them relatively, never as `/images/...` — the GitLab mirror deploys under a
base path and absolute URLs break there.

## Style

`blogstyle.py` holds the shared tokens and two helpers, `apply_style()` and
`finish()`. Use them for every new figure. The colors are the site's
light-theme tokens from `src/styles/global.css`, converted from oklch.

Figures render on the light `PAPER` background in both themes; the dark theme
frames them with a border (see the `.prose-custom img` rule in `global.css`)
so they read as deliberate figure cards rather than glare. If a figure ever
needs to be genuinely theme-aware, the way to do it is two files plus a
`<picture>` with `prefers-color-scheme`, not a transparent background — a
single ink color cannot stay legible on both surfaces.

## Palette

`CATEGORICAL` is a fixed order — assign from the front, never cycle. It was
checked with the dataviz validator against both the light surface (`#fcfcfc`)
and the dark one (`#2b2f36`):

| check | result |
|---|---|
| lightness band | pass |
| chroma floor | pass |
| CVD separation | pass — worst adjacent ΔE 13.4 (deutan) |
| normal-vision floor | pass — ΔE 27.6 |
| contrast vs surface | pass — both ≥ 3:1 |

Re-run that validation before changing any color; a pair that looks fine can
still collapse under deuteranopia. Past four series, use small multiples or a
composite encoding instead of inventing a fifth hue.
