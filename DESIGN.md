# Design Plan — Academic Website styling

Goal: style the already-built Astro site (see `PLAN.md`, all phases complete).
Register: **modern minimal** — sans-serif, generous whitespace, restrained
color. Accent: **teal/sea green**. Dark mode: **automatic only** (follows the
OS via `prefers-color-scheme`; no toggle, no JavaScript). Typography-first:
the site is mostly text and math.

## Rules for the executor

- Execute phases in order; stop and report if a "Done when" check fails.
- No JavaScript for styling/theming. No component libraries. No animations
  beyond CSS `transition` on hover/focus, except the one-time entrance
  animations scoped to Phase D8.
- All colors, fonts, and sizes come from the design tokens in
  `src/styles/global.css` — never hard-code a hex value in a component.
- Do not change page content or routes; styling only. Keep `withBase()` for
  all internal links.
- Verify `npm run build` exits 0 at the end of every phase, then commit with
  the message given in that phase.

---

## Phase D0 — Tokens, fonts, dark mode foundation ✅ done (`333d045`)

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

## Phase D1 — Base layout (header, footer, page frame) ✅ done (`3becab2`)

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
visible focus rings. Mobile check: at a 320px-wide viewport nothing
overflows horizontally, body text is ≥ 16px, and nav links have enough
padding/line-height to give ≥ 24px tap targets (WCAG 2.5.8).
Commit: `style: header, footer, page frame`

---

## Phase D2 — Home page ✅ done

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

## Phase D3 — Blog and publications ✅ done (`cbc5d06`)

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
3. **Open science (CNRS practice)**: add an optional `hal: z.string().optional()`
   field to the publications schema in `src/content.config.ts` (HAL document
   URL, e.g. `https://hal.science/hal-XXXXXXX`). When present, render a
   "HAL" link next to DOI/PDF — open-access first, per CNRS science ouverte
   policy.
4. **Publications** (`src/pages/publications.astro`): reference-list style —
   no bullets, hanging indent, year groups (`<h2>` per year, entries under
   it), author list with "A. Castillo-Castellanos" wrapped in `<strong>`
   (string-match in the template), journal in italics, DOI/PDF as small
   accent links at the end of the entry.

**Done when:** build passes; the seed post body renders in styled prose with
the Navier–Stokes equation horizontally scrollable at narrow viewport widths;
publications page shows a year-grouped reference list with the site author
bolded. Mobile check: post page and publications list at 320px width — no
horizontal page scroll (only `.katex-display` scrolls), DOI/PDF/HAL links
comfortably tappable.
Commit: `style: blog and publications`

---

## Phase D4 — CV, print, polish, privacy fix ✅ done (`b0c5469`)

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

## Phase D5 — Home hero media (optional, after D0–D4 ship) ✅ done (adapted)

> Implemented as an **image-comparison slider** instead of a video loop: the
> available asset was discrete simulation snapshots, not smooth footage. Two
> transparent WebP crops of the same t3 Rayleigh–Taylor frame (case5) — full
> interface (`public/media/hero-full.webp`, ~95 kB) vs. filtered fragments
> (`public/media/hero-filtered.webp`, ~380 kB) — in
> `src/components/CompareSlider.astro`: a range input drives a `clip-path`
> divider (progressive enhancement; static 50/50 split without JS). The tiny
> script is the D5-sanctioned JS exception; `assetsInlineLimit: 0` in
> `astro.config.mjs` keeps it external so the meta CSP (`script-src 'self'`)
> holds. Transparent backgrounds float on both color schemes.

A short fluid-dynamics loop (simulation render or experiment footage) as a
**bounded** hero element on the index page — never a full-page background,
never behind text.

1. Asset: 5–10 s loop, muted, no audio track, 720p, AV1 or H.264, **≤ 3 MB**,
   plus a still `poster` image (first frame or best frame, ~100 kB WebP/AVIF).
   Committed normally — **not** Git LFS (GitHub Pages does not serve LFS
   files). Place under `public/media/`.
2. Markup (no JS):
   ```html
   <video autoplay muted loop playsinline preload="metadata"
          poster={withBase('/media/hero-poster.webp')}
          src={withBase('/media/hero.mp4')}></video>
   ```
3. Reduced motion / reduced data: inside `@media (prefers-reduced-motion: reduce)`
   — and, where supported, `(prefers-reduced-data: reduce)` — hide the video
   and show the poster image instead (render both elements; toggle with CSS
   only).
4. Optional pause button is the only JS allowed (a few lines, progressive
   enhancement — the page must work without it).

**Done when:** build passes; index shows the loop in a bounded element; with
OS reduced-motion enabled the poster shows instead; the video file is ≤ 3 MB.
Commit: `feat: home hero media loop`

---

## Phase D6 — Security hardening (independent of styling; can run anytime) ✅ done

The site is static — no forms, no auth, no user input — so the realistic
threats are **supply chain** (npm packages, GitHub Actions) and **account
takeover**, not XSS on the pages. Harden accordingly:

1. **Pin GitHub Actions to commit SHAs** in `.github/workflows/deploy.yml`:
   replace each `uses: owner/action@vN` with `@<full-40-char-sha> # vN.N.N`
   (look up the SHA of the current release tag for `actions/checkout`,
   `withastro/action`, `actions/deploy-pages`). Tags are mutable; SHAs are
   the exact audited code.
2. **Scope workflow permissions per job**: top-level `permissions: {}`
   (or `contents: read`); move `pages: write` + `id-token: write` down onto
   the `deploy` job only, and give `build` just `contents: read`.
3. **Add `.github/dependabot.yml`** with two update ecosystems, weekly:
   `npm` (keeps Astro/Tailwind/KaTeX deps patched) and `github-actions`
   (keeps the SHA pins moving — Dependabot updates pinned SHAs and the
   version comment together).
4. **Meta CSP** (defense in depth — GitHub Pages cannot set response
   headers, so a `<meta http-equiv="Content-Security-Policy">` in
   `Base.astro`'s `<head>` is the only option). Start from:
   ```
   default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';
   img-src 'self' data:; font-src 'self'; base-uri 'self'; form-action 'none';
   object-src 'none'
   ```
   `style-src 'unsafe-inline'` is required: KaTeX emits inline `style=`
   attributes and Astro may inline small stylesheets. Known meta-tag
   limits: `frame-ancestors` and report-only mode don't work via meta —
   accept that. **Done when:** all six routes (5 pages + 404) render with
   zero CSP violations in the browser console, including a blog post with
   math and (if enabled) the model-viewer component.

**User actions (outside the repo):** enable 2FA/passkey on the GitHub
account (an attacker with the account owns the site); check that Dependabot
alerts + secret scanning are enabled in repo Settings → Security (default
for public repos); optionally protect the `main` branch.

Commit: `chore: pin actions, dependabot, scoped permissions, meta CSP`

---

## Phase D7 — Bilingual EN/FR (separate track; exempt from the "styling only, no route changes" rule)

Decision: English stays at the **root** (every existing URL keeps working),
French lives under **`/fr/`**. Translate only the low-churn pages — home and
CV. The blog stays single-language per post; publications YAML is
language-neutral (only page chrome gets translated later if ever needed).
No automatic redirect from browser language or IP — readers choose via a
visible switcher. Labels are text (`FR` / `EN`), never flags.

1. **Config** — in `astro.config.mjs`:
   ```js
   i18n: {
     locales: ['en', 'fr'],
     defaultLocale: 'en',
     routing: { prefixDefaultLocale: false, fallbackType: 'redirect' },
     fallback: { fr: 'en' },
   }
   ```
   With `fallback`, untranslated `/fr/…` routes pre-generate as redirects to
   the English page — so `/fr/blog/` etc. never 404 while untranslated.
   Also pass the i18n option to `sitemap()` (`i18n: { defaultLocale: 'en',
   locales: { en: 'en', fr: 'fr' } }`).
2. **UI strings** — `src/i18n/ui.ts`: a `ui = { en: {…}, fr: {…} }` dictionary
   for nav labels (About / À propos, Publications, Blog, CV), footer text,
   and the skip-link label, plus a tiny `t(lang, key)` helper. No i18n
   library.
3. **Base.astro** — accept a `lang` prop (default `'en'`): set
   `<html lang={lang}>` (RGAA 8.3), render nav/footer through the
   dictionary, and add the language switcher to the header — a text link
   `FR` / `EN` pointing at the **equivalent page** (each translated page
   passes its counterpart's path; use `getRelativeLocaleUrl()` from
   `astro:i18n`, which respects `base`, or keep `withBase()` —
   consistently one of the two). Pages that exist in both languages emit
   `<link rel="alternate" hreflang>` pairs plus `x-default` → English.
4. **French pages** — `src/pages/fr/index.astro` and `src/pages/fr/cv.astro`.
   Draft the French text by translating the existing English content, and
   mark both files with a `<!-- TODO: French wording to be reviewed by
   Andrés -->` comment — the bio and CV are the author's own words, so the
   user validates the phrasing.
5. **Blog language metadata** — add `lang: z.enum(['en', 'fr']).default('en')`
   to the blog schema in `src/content.config.ts`; the post page passes it to
   `Base` so each post's `<html lang>` is correct. Inline foreign phrases in
   a page get `<span lang="…">` (RGAA 8.7) — editorial habit, note it in the
   README's blog how-to.
6. **README** — short "Adding a translated page" section (drop a file under
   `src/pages/fr/`, pass `lang="fr"` and the counterpart path to `Base`).

**Done when:** build passes; `/` and `/fr/` both render with the correct
`lang` attribute and translated nav; the switcher on home and CV links
between language equivalents (not to the other homepage); `/fr/blog/`
redirects to `/blog/`; hreflang pairs present on translated pages; a
`BASE_PATH=/testbase/` build keeps every locale URL under the prefix.
Commit: `feat: bilingual EN/FR — i18n config, French home and CV, language switcher`

---

## Phase D8 — Entrance animations (optional, visual polish) ✅ done

The site currently reads as static/flat once loaded. Add a light, one-time
entrance animation on first paint — no scroll-triggered JS, no libraries.

1. In `global.css`, define `@keyframes fade-in-up` (opacity 0→1, translateY
   ~8px→0, ~400ms ease-out) alongside the existing reduced-motion block.
2. Apply via a small set of utility classes (e.g. `.animate-in`,
   `.animate-in-delay-1/2/3`) using CSS `animation`, staggered with
   `animation-delay` in ~80ms steps — applied directly in markup to page-level
   elements (heading, bio, links row on the home page; header block on other
   pages). No JS, no IntersectionObserver — everything animates on load since
   pages are short enough that nothing is off-screen.
3. Respect `prefers-reduced-motion: reduce` — the existing global rule
   (`* { transition: none !important; }`) must be extended to also zero out
   `animation` for these classes, so reduced-motion users see the final state
   immediately with no motion.
4. Keep it subtle: opacity + small translate only, no bounce/scale, no color
   animation, ~400ms total per element. This is meant to soften the "boring"
   flat-load feel, not add visual noise.

**Done when:** build passes; loading `/` shows a brief, staggered fade/rise-in
of the name, bio, and links row; other pages get a lighter single fade on
their header block; with OS reduced-motion enabled every page renders in its
final state immediately, no animation.
Commit: `style: entrance animations on page load`

---

## Out of scope

Design toggles/JS theming, blog pagination, search, comments, analytics,
OG-image generation, and any restyling of PyVista/model-viewer embeds
(they arrive styled by their own libraries).

## French institutional notes (context, not tasks)

- **RGAA 4.1.2** (French accessibility referential, based on WCAG 2.1/EN 301 549)
  legally binds public bodies' sites, not personal pages — but since this site
  mirrors to CNRS infrastructure (plmlab), we align with its core criteria
  anyway: AA contrast, keyboard navigation + visible focus, skip link,
  `lang` attribute, reduced-motion support (all already in D0–D5).
  Decorative hero video (D5) carries no information, is muted, and has a
  poster fallback — RGAA-compatible as decorative media.
- **CNIL / RGPD**: the site sets **no cookies and no trackers** and makes no
  third-party requests (fonts and model-viewer self-hosted) — so no consent
  banner is required. If analytics are ever wanted, use a CNIL
  consent-exemption-configured self-hosted Matomo, never Google Analytics.
- **DSFR** (Système de Design de l'État): its license restricts use to French
  state sites — do **not** adopt it here.
- **RGESN** (DINUM eco-design referential, 2024, 78 criteria): a static,
  no-tracker, self-hosted-assets site already satisfies the bulk of it. The
  criteria that remain actionable here: serve images as WebP/AVIF at display
  size (home portrait, D2; hero poster, D5), keep the hero video ≤ 3 MB and
  honor `prefers-reduced-data` (D5), WOFF2-only subset fonts (Fontsource
  default, D0), and no client-side JS beyond progressive enhancement —
  already a plan rule.
- **Security posture (context for D6)**: `*.github.io` is HSTS-preloaded and
  HTTPS-only, so transport security is handled by the host. GitHub Pages
  offers no custom response headers at all — header-based controls (HSTS
  tuning, `frame-ancestors`, report-only CSP) are simply unavailable; the
  meta CSP in D6 is the ceiling. The site already avoids the classic
  static-site pitfalls: no third-party scripts after D4 (no SRI needed
  because nothing is remote), no analytics, no forms. `package-lock.json`
  is committed and CI uses `npm ci`, so builds are reproducible.
- **Science ouverte**: ORCID is the pivot researcher ID (already in
  `site.ts`); the `hal` publication field (D3) links open-access HAL
  versions. Consider creating an idHAL and linking it to ORCID (user action,
  outside this repo).
