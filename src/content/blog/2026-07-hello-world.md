---
title: 'Hello, world'
date: 2026-07-29
description: 'Placeholder first post, mostly here to prove the pipeline works.'
tags: ['meta']
draft: false
---

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. This is a placeholder post used to
verify Markdown rendering, tags, dates, and the RSS feed.

Math should render via KaTeX. Inline: $\nu = \mu / \rho$. Display:

$$ \partial_t \mathbf{u} + (\mathbf{u}\cdot\nabla)\mathbf{u} = -\nabla p + \nu \nabla^2 \mathbf{u} $$

If the equation above shows as typeset math rather than raw `$$`, the
remark-math + rehype-katex pipeline is working.

<!--
3D model embed example (requires converting this post to .mdx and committing
a .glb under public/models/ — large meshes should go through Git LFS):

import ModelViewer from '../../components/ModelViewer.astro';

<ModelViewer src="/models/example.glb" alt="Example 3D model" />
-->

