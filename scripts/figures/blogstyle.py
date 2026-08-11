"""Shared plotting style for figures embedded in blog posts.

Import this from every figure script so the plots read as one system:

    from blogstyle import PAPER, CATEGORICAL, apply_style, finish

    fig, ax = plt.subplots(figsize=(5.4, 3.7))
    apply_style(fig, ax)
    ...
    finish(fig, ax, xlabel='$k$', ylabel=r'$a\\omega^2/g$', out='name.png')

Colors are the site's light-theme tokens from src/styles/global.css, converted
from oklch. The categorical pair is validated for colorblind separation — see
README.md before changing it.
"""
from pathlib import Path

import matplotlib.pyplot as plt

# Where figure PNGs land: co-located with the posts so Astro optimizes them.
IMAGE_DIR = Path(__file__).resolve().parents[2] / 'src' / 'content' / 'blog' / 'images'

# Site tokens (light theme).
PAPER = '#fcfcfc'       # --bg
INK = '#3b3f45'         # --ink
INK_MUTED = '#767c85'   # --ink-muted
RULE = '#e6e6e6'        # --rule

# Categorical series colors, in fixed order. Never cycle past the end: a fifth
# series means small multiples or a composite encoding, not a new hue.
CATEGORICAL = ['#0093ad', '#d1495b', '#7b6cd9', '#c97a1f']

DEFAULT_FIGSIZE = (5.4, 3.7)
DPI = 220


def apply_style(fig, ax):
    """Paper background, recessive grid, two spines."""
    fig.patch.set_facecolor(PAPER)
    ax.set_facecolor(PAPER)

    ax.grid(True, color=RULE, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)

    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    for side in ('left', 'bottom'):
        ax.spines[side].set_color(RULE)
        ax.spines[side].set_linewidth(0.9)

    ax.tick_params(colors=INK_MUTED, labelsize=9, length=3, width=0.9)


def finish(fig, ax, xlabel, ylabel, out):
    """Axis labels in ink tokens, frameless legend, save into IMAGE_DIR.

    The legend goes in a strip above the axes rather than floating inside
    them: with dense scatter there is rarely a corner that stays empty at
    every parameter set, and an in-axes legend silently lands on the data.
    """
    ax.set_xlabel(xlabel, fontsize=11, color=INK)
    ax.set_ylabel(ylabel, fontsize=11, color=INK)

    for axis in (ax.xaxis, ax.yaxis):
        axis.get_offset_text().set(color=INK_MUTED, fontsize=9)

    handles, labels = ax.get_legend_handles_labels()
    if handles:
        legend = ax.legend(fontsize=9.5, loc='lower left', frameon=False,
                           bbox_to_anchor=(0, 1.0), ncol=len(handles),
                           handletextpad=0.2, borderaxespad=0.4,
                           columnspacing=1.4)
        for text in legend.get_texts():
            text.set_color(INK)

    fig.tight_layout(pad=0.6)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    path = IMAGE_DIR / out
    fig.savefig(path, dpi=DPI, facecolor=PAPER)
    plt.close(fig)
    print(f'wrote {path}')
    return path
