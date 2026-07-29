# acastillo-castellanos.github.io

Personal academic website of Andrés Castillo-Castellanos — about, publications,
blog (with KaTeX math), and CV. Built with [Astro](https://astro.build) +
Tailwind CSS, deployed as a static site to **GitHub Pages** (primary) and
**GitLab Pages on plmlab** (mirror).

Live site: https://acastillo-castellanos.github.io

## Development

Requires Node.js ≥ 20 (see `.nvmrc`).

```bash
npm install        # once
npm run dev        # dev server with hot reload at http://localhost:4321
npm run build      # static build into dist/
npm run preview    # serve the built dist/ locally
```

## Adding content

### Blog post

Create `src/content/blog/YYYY-MM-slug.md` (or `.mdx`):

```markdown
---
title: 'Post title'
date: 2026-07-29
description: 'One-line summary shown in the blog index and RSS.'
tags: ['cfd', 'waves']   # optional, defaults to []
draft: false             # optional; true hides the post
---

Body in Markdown. Math via KaTeX: inline $\nu = \mu/\rho$ or display blocks
with `$$ ... $$`.
```

### Publication

Create `src/content/publications/YYYY-slug.yaml`:

```yaml
title: 'Paper title'
authors:
  - 'A. Castillo-Castellanos'
  - 'B. Coauthor'
journal: 'J. Fluid Mech.'
year: 2024
doi: '10.1017/xxx'   # optional
pdf: '/papers/x.pdf' # optional
```

### 3D models

- **glTF/GLB models**: use the `src/components/ModelViewer.astro` component
  from an `.mdx` post or a page:

  ```astro
  import ModelViewer from '../../components/ModelViewer.astro';

  <ModelViewer src="/models/example.glb" alt="Description" />
  ```

  Put `.glb` files under `public/models/`. Track large meshes with Git LFS
  (`git lfs track "*.glb"`).

- **PyVista scenes**: export a standalone HTML scene and embed it in an iframe.
  Python tooling is managed with **uv** — no Python environment lives in this
  repo. One-off export:

  ```bash
  uvx --with pyvista python export.py
  ```

  where `export.py` ends with `plotter.export_html('scene.html')`. Put the
  exported file in `public/scenes/` and embed it:

  ```html
  <iframe src="/scenes/scene.html" width="100%" height="400"></iframe>
  ```

  For recurring exports, keep a `uv run` script in the analysis repo that
  produces the scene, and copy only the HTML here. Large scene files also go
  through Git LFS.

## Deployment

`astro.config.mjs` reads two env vars so the same code deploys to both hosts:

- `SITE_URL` — canonical origin (default `https://acastillo-castellanos.github.io`)
- `BASE_PATH` — subpath prefix (default `/`)

Internal links must use the `withBase()` helper from `src/utils/url.ts` so they
work under a subpath.

### GitHub Pages (primary)

`.github/workflows/deploy.yml` builds and deploys on every push to `main`.
Repo setting required once: **Settings → Pages → Source = GitHub Actions**
(already done).

### GitLab Pages on plmlab (mirror)

`.gitlab-ci.yml` builds with `SITE_URL=$CI_PAGES_URL` and
`BASE_PATH=/$CI_PROJECT_NAME/`, publishing `dist/`. Setup (user action,
pending):

1. Create a project on https://plmlab.math.cnrs.fr.
2. In the plmlab project: **Settings → Repository → Mirroring repositories →
   Pull**, URL `https://github.com/acastillo-castellanos/acastillo-castellanos.github.io.git`.
3. Each mirrored push to `main` runs the pipeline and publishes to
   `https://plmlab.math.cnrs.fr/<namespace>/<project>` Pages.

Fallback without mirroring — push to both remotes manually:

```bash
git remote add plmlab git@plmlab.math.cnrs.fr:<user>/<project>.git
git push plmlab main
```

## Pending user actions

- [x] GitHub Pages source set to GitHub Actions (site is live)
- [ ] Create the plmlab project and configure pull mirroring (§ above)
- [ ] Replace placeholder ORCID / Google Scholar IDs in `src/data/site.ts`
- [ ] Add a profile photo
- [ ] Replace the placeholder blog post and publication entry
