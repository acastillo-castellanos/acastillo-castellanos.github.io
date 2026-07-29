# Design Plan — Academic Website styling

Goal: style the already-built Astro site (see `PLAN.md`, all phases complete).
Register: **modern minimal** — sans-serif, generous whitespace, restrained
color. Accent: **teal/sea green**. Dark mode: **automatic only** (follows the
OS via `prefers-color-scheme`; no toggle, no JavaScript). Typography-first:
the site is mostly text and math.

## Rules for the executor

- Execute phases in order; stop and report if a "Done when" check fails.
- No JavaScript for styling/theming. No component libraries. No animations
  beyond CSS `transition` on hover/focus.
- All colors, fonts, and sizes come from the design tokens in
  `src/styles/global.css` — never hard-code a hex value in a component.
- Do not change page content or routes; styling only. Keep `withBase()` for
  all internal links.
- Verify `npm run build` exits 0 at the end of every phase, then commit with
  the message given in that phase.

---

## Phase D0 — Tokens, fonts, dark mode foundation

1. Install:
   ```bash
   npm install @tailwindcss/typography @fontsource-variable/google-sans-flex
   ```
2. Rewrite `src/styles/global.css`:
   ```css
   @import 'tailwindcss';
   @plugin '@tailwindcss/typography';
   @import '@fontsource-variable/google-sans-flex';

   @theme {
     --font-sans: 'Google Sans Flex Variable', ui-sans-serif, system-ui, sans-serif;
     --color-accent-600: oklch(0.52 0.1 195);  /* teal, light-mode links */
     --color-accent-400: oklch(0.72 0.1 195);  /* teal, dark-mode links */
   }

   :root {
     color-scheme: light dark;
     /* paper / ink pairs; light-dark() flips them with the OS preference */
     --bg: light-dark(oklch(0.99 0 0), oklch(0.21 0.01 250));
     --bg-subtle: light-dark(oklch(0.96 0 0), oklch(0.26 0.01 250));
     --ink: light-dark(oklch(0.25 0.01 250), oklch(0.9 0.005 250));
     --ink-muted: light-dark(oklch(0.5 0.01 250), oklch(0.7 0.005 250));
     --accent: light-dark(var(--color-accent-600), var(--color-accent-400));
     --rule: light-dark(oklch(0.9 0 0), oklch(0.32 0.01 250));
   }

   body {
     background: var(--bg);
     color: var(--ink);
     font-family: var(--font-sans);
   }
   ```
3. Wire the variables into Tailwind utilities by extending `@theme` with
   `--color-bg: var(--bg);` etc., so classes like `bg-bg`, `text-ink`,
   `text-ink-muted`, `text-accent`, `border-rule`, `bg-bg-subtle` exist.
   Use those utility names everywhere in later phases.

4. Reduced motion (MDN): disable non-essential transitions globally:
   ```css
   @media (prefers-reduced-motion: reduce) {
     *, *::before, *::after { transition: none !important; }
   }
   ```

**Done when:** build passes; the site renders in Google Sans Flex on an off-white
background, and switching the OS to dark mode flips it to a dark background
with light text (no toggle anywhere). Contrast check (WCAG AA): body text
(`--ink` on `--bg`) ≥ 4.5:1 and accent-colored links ≥ 4.5:1 in **both**
color schemes — verify with the WebAIM contrast checker and adjust the OKLCH
lightness values if a pair fails.
Commit: `style: design tokens, Google Sans Flex, automatic dark mode`

---

## Phase D1 — Base layout (header, footer, page frame)

In `src/layouts/Base.astro` only:

1. Page frame: centered column, `max-w-2xl` for text pages, horizontal
   padding for mobile; `min-h-screen` flex column so the footer sits at the
   bottom.
2. Header: site name (links home) left, nav links right; small text
   (`text-sm`), muted color, accent + underline on the **active** page
   (compare `Astro.url.pathname` against each link, base-aware). Thin bottom
   border (`border-rule`). Wraps gracefully on narrow screens.
3. Footer: one muted line — `© {year} {SITE.author} · RSS` (RSS links to
   `withBase('/rss.xml')`).
4. Global link style: accent color, underline on hover/focus;
   `focus-visible` outline using the accent. Add a skip-to-content link
   (visually hidden until focused).

**Done when:** build passes; every page shows the framed layout, the current
page is highlighted in the nav on all five pages, and keyboard Tab shows
visible focus rings.
Commit: `style: header, footer, page frame`

---

## Phase D2 — Home page

`src/pages/index.astro`:

1. Name as a large but quiet heading (`text-3xl font-semibold tracking-tight`),
   role line below in `text-ink-muted`.
2. Bio paragraph at comfortable measure.
3. Links row: GitHub / ORCID / Scholar / email as a horizontal list with
   inline SVG icons (16px, `currentColor`, sourced from Simple Icons paths
   pasted inline — no icon font, no package). Email shown as icon + address.
4. Optional photo slot: if `src/assets/portrait.jpg` exists, show it
   (rounded, ~112px) beside the name using Astro `<Image>`; if absent, skip
   without failing the build (guard with `import.meta.glob`).

**Done when:** build passes; index reads as: photo?/name/role, bio, links row
with icons, in both color schemes.
Commit: `style: home page`

---

## Phase D3 — Blog and publications

1. **Blog index** (`src/pages/blog/index.astro`): remove list bullets; each
   post is a block — title (medium weight, accent on hover), date + tags in
   one muted small line, description below. Tags as plain text
   (`#tag` style), not chips — quieter.
2. **Post page** (`src/pages/blog/[...id].astro`): wrap `<Content />` in
   `prose` (typography plugin), extended so prose colors track the tokens
   (`prose-headings:text-ink`, links accent, etc. — or define a small
   `.prose` override block in `global.css` using the CSS variables).
   Title + date header above, outside the prose block.
   KaTeX: display equations get `overflow-x: auto` on `.katex-display` and
   vertical margin, so long equations scroll instead of breaking the layout
   on mobile.
3. **Publications** (`src/pages/publications.astro`): reference-list style —
   no bullets, hanging indent, year groups (`<h2>` per year, entries under
   it), author list with "A. Castillo-Castellanos" wrapped in `<strong>`
   (string-match in the template), journal in italics, DOI/PDF as small
   accent links at the end of the entry.

**Done when:** build passes; the seed post body renders in styled prose with
the Navier–Stokes equation horizontally scrollable at narrow viewport widths;
publications page shows a year-grouped reference list with the site author
bolded.
Commit: `style: blog and publications`

---

## Phase D4 — CV, print, polish, privacy fix

1. **CV** (`src/pages/cv.astro`): section headings with a thin rule
   (`border-b border-rule`); each experience entry as a grid — dates/place in
   a muted left column, content right — collapsing to stacked on mobile.
2. **Print stylesheet** for the CV page (media query in `global.css` or a
   scoped `<style>` in `cv.astro`): hide header/nav/footer, black on white,
   sensible margins — so "Print to PDF" from the browser yields a usable CV.
3. **404 page** (`src/pages/404.astro`): minimal — "Page not found", link
   home via `withBase()`, uses `Base.astro`.
4. **Privacy fix** — self-host model-viewer: `npm install @google/model-viewer`,
   then in `src/components/ModelViewer.astro` replace the
   `ajax.googleapis.com` CDN `<script>` with a bundled import
   (`<script> import '@google/model-viewer'; </script>`), so visitors' IPs
   are never sent to Google (same GDPR reasoning as self-hosted fonts).
   Also update the README's 3D section if it mentions the CDN.
5. Sweep: consistent vertical rhythm on all pages (same top margin under the
   header, same `h1` scale), `text-wrap: balance` on headings, favicon still
   correct in dark mode (the default Astro SVG adapts; replace only if it
   does not).

**Done when:** build passes; printing `/cv/` shows only CV content in black
on white; `/404` styled; all five pages + 404 look consistent in light and
dark.
Commit: `style: CV layout, print stylesheet, 404`

---

## Out of scope

Design toggles/JS theming, blog pagination, search, comments, analytics,
OG-image generation, and any restyling of PyVista/model-viewer embeds
(they arrive styled by their own libraries).
