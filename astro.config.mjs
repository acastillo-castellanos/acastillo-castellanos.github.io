// @ts-check
import { defineConfig } from 'astro/config';
import { unified } from '@astrojs/markdown-remark';
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
  vite: {
    plugins: [tailwindcss()],
    // Never inline scripts/assets into the HTML: the meta CSP in Base.astro
    // allows only same-origin external scripts (script-src 'self').
    build: { assetsInlineLimit: 0 },
  },
  markdown: {
    processor: unified({
      remarkPlugins: [remarkMath],
      rehypePlugins: [rehypeKatex],
    }),
  },
});

