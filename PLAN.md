# Implementation Plan — Academic Website (Astro)

Goal: replace the abandoned Create React App under `main/` with an Astro + Tailwind
static site (academic sections + blog), deployable to **both** GitHub Pages
(`https://acastillo-castellanos.github.io`) and GitLab Pages on plmlab
(`https://plmlab.math.cnrs.fr`).

Reference for structure (NOT design): https://dspelaez.github.io
Design/styling is explicitly **out of scope** — build with minimal default styling.

## Rules for the executor

- Execute phases in order. Do not skip "Done when" checks; stop and report if one fails.
- Never commit `node_modules/`, `dist/`, or `.astro/`.
- Do not invent content. All real content is in this file (§ Content data). Use
  placeholder lorem text only where this plan says "placeholder".
- All commands run from the repo root unless stated otherwise.
- Commit at the end of each phase with the message given in that phase.

---

## Phase 0 — Repo rename (requires the user's GitHub auth) ✅ COMPLETE (2026-07-29)

The GitHub username is now `acastillo-castellanos`. A user site must live in a repo
named `<username>.github.io`.

1. Rename the repo on GitHub:
   ```bash
   gh repo rename acastillo-castellanos.github.io
   ```
   If `gh` is not authenticated, stop and ask the user to rename via GitHub web UI
   (Settings → General → Repository name), then continue.
2. Update the local remote if the rename didn't do it automatically:
   ```bash
   git remote set-url origin git@github.com:acastillo-castellanos/acastillo-castellanos.github.io.git
   ```

**Done when:** `git remote -v` shows `acastillo-castellanos.github.io` and
`git ls-remote origin HEAD` succeeds.

---

## Phase 1 — Clean the repo ✅ COMPLETE (2026-07-29)

1. The old CRA app is untracked. Its only value (CV text) is already captured in
   § Content data below. Delete it:
   ```bash
   rm -rf main/
   ```
2. Keep `README.md` for now (it will be rewritten in Phase 5).

**Done when:** `git status` shows a clean tree except `PLAN.md`, and `ls` shows only
`README.md` and `PLAN.md`. Commit: `chore: remove abandoned CRA prototype`

---

## Phase 2 — Scaffold Astro + Tailwind ✅ COMPLETE (2026-07-29)

1. Pin Node (any current LTS ≥ 20):
   ```bash
   node --version   # verify >= 20; if not, stop and report
   echo "22" > .nvmrc
   ```
2. Scaffold Astro into the repo root, non-interactively:
   ```bash
   npm create astro@latest . -- --template minimal --install --no-git --yes
   npx astro add tailwind --yes
   npx astro add sitemap --yes
   npm install @astrojs/rss remark-math rehype-katex katex
   ```
3. Create `.gitignore` at repo root (the scaffold may create one — overwrite it):
   ```gitignore
   node_modules/
   dist/
   .astro/
   .env
   .DS_Store
   ```
4. Replace `astro.config.mjs` with (keep whatever integration imports
   `astro add` generated — merge, don't drop them):
   ```js
   import { defineConfig } from 'astro/config';
   import sitemap from '@astrojs/sitemap';
   import tailwindcss from '@tailwindcss/vite';
   import remarkMath from 'remark-math';
   import rehypeKatex from 'rehype-katex';

   // Dual deployment: GitHub Pages serves a user site at the domain root;
   // GitLab Pages (plmlab) serves under a subpath. CI overrides these.
   const site = process.env.SITE_URL ?? 'https://acastillo-castellanos.github.io';
   const base = process.env.BASE_PATH ?? '/';

   export default defineConfig({
     site,
     base,
     integrations: [sitemap()],
     vite: { plugins: [tailwindcss()] },
     markdown: {
       remarkPlugins: [remarkMath],
       rehypePlugins: [rehypeKatex],
     },
   });
   ```
   Note: if `astro add tailwind` configured Tailwind differently (e.g. an
   `integrations` entry instead of a Vite plugin), keep the generated mechanism —
   only add `site`, `base`, `sitemap`, and the `markdown` block.
5. Verify locally:
   ```bash
   npm run build
   ```

**Done when:** `npm run build` exits 0 and `dist/index.html` exists.
Commit: `feat: scaffold Astro + Tailwind with dual-host config`

---

## Phase 3 — Content architecture

### 3.1 Site-wide config data

Create `src/data/site.ts`:
```ts
export const SITE = {
  title: 'Andrés Castillo-Castellanos',
  description: 'Research scientist in fluid dynamics.',
  author: 'Andrés Castillo-Castellanos',
  email: 'andres.castillo.castellanos@proton.me',
  location: 'Greater Paris, France',
  links: {
    github: 'https://github.com/acastillo-castellanos',
    // The following are placeholders — user must fill real IDs later:
    orcid: 'https://orcid.org/XXXX-XXXX-XXXX-XXXX',
    scholar: 'https://scholar.google.com/citations?user=XXXX',
  },
};
```

### 3.2 Content collections

Create `src/content.config.ts`:
```ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    description: z.string(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

const publications = defineCollection({
  loader: glob({ pattern: '**/*.yaml', base: './src/content/publications' }),
  schema: z.object({
    title: z.string(),
    authors: z.array(z.string()),
    journal: z.string(),
    year: z.number(),
    doi: z.string().optional(),
    pdf: z.string().optional(),
  }),
});

export const collections = { blog, publications };
```

### 3.3 Seed content

- `src/content/blog/2026-07-hello-world.md` — placeholder post with frontmatter
  matching the schema, including one display equation
  (`$$ \partial_t \mathbf{u} + (\mathbf{u}\cdot\nabla)\mathbf{u} = -\nabla p + \nu \nabla^2 \mathbf{u} $$`)
  to prove KaTeX works.
- `src/content/publications/2024-example.yaml` — one placeholder entry.

### 3.4 Layout and pages

Create a single shared layout `src/layouts/Base.astro`: HTML skeleton, KaTeX CSS
(`import 'katex/dist/katex.min.css';` in frontmatter), and a plain `<nav>` linking
all pages. IMPORTANT: every internal link must be prefixed with
`import.meta.env.BASE_URL` so the site works under a subpath on plmlab. Create a
helper `src/utils/url.ts` exporting `withBase(path: string)` and use it for all
internal hrefs.

Pages (all use `Base.astro`, minimal semantic HTML, no styling effort):

| File | Content |
|---|---|
| `src/pages/index.astro` | Name, one-paragraph bio (use "Profile" text from § Content data), links from `SITE.links` |
| `src/pages/publications.astro` | List the `publications` collection, sorted by year desc |
| `src/pages/blog/index.astro` | List non-draft posts, sorted by date desc |
| `src/pages/blog/[...id].astro` | Render a post (`getStaticPaths` over the `blog` collection) |
| `src/pages/cv.astro` | Full CV from § Content data, as headed sections |
| `src/pages/rss.xml.js` | RSS feed via `@astrojs/rss` over the blog collection |

**Done when:** `npm run build` exits 0; `npm run preview` serves: an index with bio,
a publications list, a blog index, one post where the Navier–Stokes equation renders
as math (not raw `$$`), a CV page, and `/rss.xml` is valid XML.
Also verify subpath mode: `BASE_PATH=/testbase/ npm run build` exits 0 and links in
`dist/` HTML start with `/testbase/`.
Commit: `feat: content collections, core pages, RSS`

---

## Phase 4 — CI/CD for both hosts

### 4.1 GitHub Pages

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: withastro/action@v4
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```
If `withastro/action@v4` does not exist yet, use `@v3`.

Then tell the user (cannot be done from CLI without admin scope): in repo
**Settings → Pages**, set Source to **GitHub Actions**.

### 4.2 GitLab Pages (plmlab)

Create `.gitlab-ci.yml`:
```yaml
pages:
  image: node:22
  stage: deploy
  script:
    - npm ci
    - npm run build
  variables:
    SITE_URL: $CI_PAGES_URL
    BASE_PATH: "/$CI_PROJECT_NAME/"
  publish: dist
  artifacts:
    paths:
      - dist
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```
Note: if the plmlab GitLab version rejects the `publish:` keyword, fall back to
renaming the output: add `- mv dist public` to `script`, set `artifacts.paths` to
`public`, and remove `publish:`.

### 4.3 Mirroring

GitHub is the primary. Two options, in order of preference:
1. Ask the user to create the project on plmlab and configure a **push mirror**
   (GitHub repo → Settings → this is a *pull* on GitLab side: plmlab project →
   Settings → Repository → Mirroring repositories → Pull from the GitHub URL).
2. Fallback: document in README a dual-push remote:
   ```bash
   git remote add plmlab git@plmlab.math.cnrs.fr:<user>/<project>.git
   ```
The executor cannot create the plmlab project (needs the user's CNRS credentials) —
write the instructions into the README (Phase 5) and report this as a user action.

**Done when:** workflow file passes `actionlint` if available (else YAML-parses),
`.gitlab-ci.yml` YAML-parses, and after push the GitHub Actions run is green and the
site is live at `https://acastillo-castellanos.github.io`.
Commit: `ci: GitHub Pages + GitLab Pages (plmlab) pipelines`

---

## Phase 5 — Academic extras + README

1. **3D model embed component** `src/components/ModelViewer.astro`: wraps Google's
   `<model-viewer>` web component. Load the library with
   `<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js"></script>`
   only inside this component; props: `src`, `alt`. Add a demo usage note (commented
   out) in the placeholder blog post. No `.glb` asset is committed now.
2. **PyVista scene pattern**: document in README — exported
   `plotter.export_html()` files go in `public/scenes/` and are embedded with an
   `<iframe>`; large meshes go through Git LFS. Python tooling is managed with
   **uv**: document one-off exports as `uvx --with pyvista python export.py` (or a
   `uv run` script in a separate analysis repo) — do not add pip/conda instructions,
   and no Python environment belongs in this website repo.
3. Rewrite `README.md`: what the site is, `npm run dev|build|preview`, how to add a
   blog post (file + frontmatter example), how to add a publication (YAML example),
   how deployment works on both hosts, the plmlab mirroring instructions from § 4.3,
   and the pending user actions list (Pages source setting, plmlab project creation,
   real ORCID/Scholar links, profile photo).
4. Delete `PLAN.md`? **No** — keep until the user confirms the site is live, then
   the user decides.

**Done when:** `npm run build` exits 0; README covers all items above.
Commit: `feat: model-viewer component, docs`

---

## Content data (extracted from the old CRA prototype — the source of truth)

**Name:** Andrés Castillo · **Title:** Research Engineer | PhD in Fluid Mechanics
**Email:** andres.castillo.castellanos@proton.me · **Location:** Greater Paris, France

**Profile:** Mechanical Engineer with a doctorate in fluid dynamics and over seven
years of research experience. Specializing in modelling and simulation of heat
transfer, vortex, and two-phase flow. Proficient in numerical methods, data
analysis, visualization, scientific computing & HPC.

**Skills — Soft:** Adaptability and Learning Agility; Creative problem-solving;
Oral and Written Communication; Languages: Spanish (Native), English (C2), French (C1).
**Skills — Technical:** Numerical Methods: FEM, FVM, DNS, ROMs; Languages: Python,
C, Fortran, Matlab; CFD: Basilisk, ANSYS CFX, Fluent.

**Research Experience:**
- *Research Fellow, Centre Borelli UMR 9010* — École Normale Supérieure
  Paris-Saclay, Greater Paris, France (2022–2025). Developed phenomenological
  models of the interaction between surface waves and internal stratification using
  experiments, simulations, and PINNs. Devised a novel approach to study two
  non-miscible fluids under intense horizontal vibrations ("frozen wave"
  instability) using experiments and simulations.
- *Research Fellow, IRPHÉ UMR 7342* — CNRS/Aix-Marseille Université, Marseille,
  France (2019–2022). Developed simplified models to study the wake of an
  asymmetric rotor in good agreement with experimental data. Proposed an approach
  to study rotor wakes with twin tip vortices on the Vortex Filament Method (VFM).

**Industry Experience:**
- *Project Engineer* — Tiger-Sepam / SAEG Engineering Group / BG; Cartagena,
  Bogotá & Barrancabermeja, Colombia (2009–2011). Executed phase A and prepared
  phases B/B1 for the Cartagena Refinery Expansion Project. Assisted in bidding,
  tendering, planning, and execution of HVAC, energy recovery, and automation
  projects.

**Education:**
- PhD in Fluid Mechanics — University of Paris VI (UPMC), Paris, France (2017)
- MSc in Energetics & Environment — ENSAM ParisTech, Paris, France (2013)
