#!/usr/bin/env python
"""Figures for the two-interface Faraday series (Pototsky & Bestehorn 2016).

Recreates the unforced dispersion relation (PB06 Fig. 2) and the Faraday
stability tongues (PB06 Fig. 4a, 4b) in the blog's unified visual styling.

Source data:
    project_faramix_safekeeping/light_data/linear_stability_PB06_dedalus/
        pb06_dispersion.h5
        pb06_faraday_f10.h5
        pb06_faraday_f50.h5

Run:
    uv run --with matplotlib --with h5py --with numpy \
        python scripts/figures/pb06_figures.py
"""
from pathlib import Path

import h5py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

from blogstyle import (
    CATEGORICAL,
    DEFAULT_FIGSIZE,
    DPI,
    IMAGE_DIR,
    INK,
    INK_MUTED,
    PAPER,
    RULE,
    apply_style,
)

DATA = Path('/home/andres/Projects1/project_faramix_safekeeping/light_data'
            '/linear_stability_PB06_dedalus')

# Palette mapping
SUBHARMONIC = CATEGORICAL[0]  # #0093ad (teal)
HARMONIC = CATEGORICAL[1]     # #d1495b (crimson)

ZIGZAG = CATEGORICAL[1]       # #d1495b (crimson)
VARICOSE = INK                # #3b3f45 (ink)
EQ30_COLOR = CATEGORICAL[0]   # #0093ad (teal)

COMPLEX_TOL = 1e-6


def draw_inset(ax, pos, dh1, dh2, marker_xy, num, color):
    """Schematic of the two interface deformations for one mode."""
    x = np.linspace(0, 4 * np.pi, 128)
    rot = np.exp(-1j * np.angle(dh1))
    scale = 0.85 / max(abs(dh1), abs(dh2))
    axi = ax.inset_axes(pos)
    axi.patch.set_facecolor(PAPER)
    axi.plot(x, scale * (dh1 * rot * np.exp(1j * x)).real, lw=0.7, color=INK_MUTED)
    axi.plot(x, 2.4 + scale * (dh2 * rot * np.exp(1j * x)).real, lw=0.7, color=INK_MUTED)
    axi.set_ylim(-1.3, 3.7)
    axi.set_xticks([])
    axi.set_yticks([])
    for spine in axi.spines.values():
        spine.set_linewidth(0.5)
        spine.set_color(RULE)
        spine.set_linestyle(':')
    axi.text(0.04, 0.04, f'({num})', transform=axi.transAxes, fontsize=6,
             va='bottom', color=INK_MUTED)
    ax.plot(*marker_xy, 's', ms=4, mfc='none', color=color, zorder=4)
    ax.annotate(f'({num})', marker_xy, textcoords='offset points',
                xytext=(3, -7), fontsize=6, color=INK)


def plot_dispersion(out_name='pb06-dispersion.png'):
    """Dispersion relation (PB06 Fig. 2): frequency Im(lambda) and damping -Re(lambda)."""
    with h5py.File(DATA / 'pb06_dispersion.h5', 'r') as h5f:
        k = h5f['k'][:]
        sigma = h5f['sigma'][:]
        dh1 = h5f['delta_h1'][:]
        dh2 = h5f['delta_h2'][:]
        eq30 = h5f['eq30'][:]
        d2 = float(h5f.attrs['d2_dim'])

    k_mm = k / 1e3  # mm^-1

    is_complex = np.isfinite(sigma) & (np.abs(sigma.imag) > COMPLEX_TOL * np.abs(sigma))
    is_real = np.isfinite(sigma) & ~is_complex
    keep_real = is_real & (
        np.cumsum(is_real, axis=1) <= np.maximum(0, 4 - 2 * is_complex.sum(axis=1))[:, None]
    )

    with np.errstate(invalid='ignore'):
        is_zigzag = np.abs(np.angle(dh2 / dh1)) < np.pi / 2

    kk = np.broadcast_to(k_mm[:, None], sigma.shape)

    fig, (ax_a, ax_b) = plt.subplots(2, 1, sharex=True, figsize=(5.4, 6.2))
    apply_style(fig, ax_a)
    apply_style(fig, ax_b)

    # Panel (a): Oscillation frequencies Im(lambda)
    for zz, color in [(True, ZIGZAG), (False, VARICOSE)]:
        sel = is_complex & (is_zigzag == zz)
        ax_a.plot(kk[sel], sigma.imag[sel], '.', color=color, ms=3.5, zorder=3)
        sel_b = keep_real & (is_zigzag == zz)
        ax_b.plot(kk[sel], -sigma.real[sel], '.', color=color, ms=3.5, zorder=3)
        ax_b.plot(kk[sel_b], -sigma.real[sel_b], 'o', ms=3, mfc='none', color=color, zorder=3)

    ax_a.plot(k_mm, eq30, '-.', color=EQ30_COLOR, lw=1.1, label='one-layer Eq. (30), $h=d_2$')

    ax_a.set_ylabel(r'$\mathrm{Im}(\lambda)$ [s$^{-1}$]', fontsize=10.5, color=INK)
    ax_a.set_yscale('log')
    ax_a.text(0.03, 0.06, '(a)', transform=ax_a.transAxes, fontsize=10, fontweight='bold', color=INK)
    ax_a.legend(loc='lower right', fontsize=8.5, frameon=False)

    # Secondary top axis in k*d2
    sec = ax_a.secondary_xaxis('top', functions=(lambda x: x * 1e3 * d2, lambda x: x / (1e3 * d2)))
    sec.set_xlabel('$k d_2$', fontsize=10, color=INK)
    sec.tick_params(colors=INK_MUTED, labelsize=8.5, length=3, width=0.9)
    for side in ('top', 'right', 'left', 'bottom'):
        if side in sec.spines:
            sec.spines[side].set_color(RULE)

    # Panel (b): Damping rates -Re(lambda)
    ax_b.set_ylabel(r'$-\mathrm{Re}(\lambda)$ [s$^{-1}$]', fontsize=10.5, color=INK)
    ax_b.set_yscale('log')
    ax_b.set_xlabel('$k$ [mm$^{-1}$]', fontsize=10.5, color=INK)
    ax_b.set_xscale('log')
    ax_b.text(0.13, 0.06, '(b)', transform=ax_b.transAxes, fontsize=10, fontweight='bold', color=INK)

    legend_elements = [
        Line2D([], [], marker='.', ls='', color=ZIGZAG, ms=5, label='zigzag (in-phase)'),
        Line2D([], [], marker='.', ls='', color=VARICOSE, ms=5, label='varicose (antiphase)'),
        Line2D([], [], marker='.', ls='', color=INK_MUTED, ms=5, label='dispersive'),
        Line2D([], [], marker='o', ls='', color=INK_MUTED, ms=4, mfc='none', label='monotonic'),
    ]
    ax_b.legend(handles=legend_elements, fontsize=8, loc='lower right', ncols=2, frameon=False)

    # Insets
    insets_a = [(0.03, 0), (0.03, 1), (1.0, 0), (1.0, 1)]
    insets_b = [(1.2e-3, 0), (1.2e-3, 1), (5e-3, 1), (5e-3, 2)]
    inset_w, inset_h = 0.16, 0.20

    for num, (ax, (k_target, rank)) in enumerate(
        [(ax_a, s) for s in insets_a] + [(ax_b, s) for s in insets_b], start=1
    ):
        i = int(np.argmin(np.abs(k_mm - k_target)))
        value = sigma.imag[i, rank] if ax is ax_a else -sigma.real[i, rank]
        pos = [0.035 + ((num - 1) % 4) * 0.175, 0.74, inset_w, inset_h]
        phase = np.angle(dh2[i, rank] / dh1[i, rank])
        color = ZIGZAG if abs(phase) < np.pi / 2 else VARICOSE
        draw_inset(ax, pos, dh1[i, rank], dh2[i, rank], (k_mm[i], value), num, color)

    fig.tight_layout(pad=0.8)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    out_path = IMAGE_DIR / out_name
    fig.savefig(out_path, dpi=DPI, facecolor=PAPER)
    plt.close(fig)
    print(f'wrote {out_path}')


def plot_faraday_single(preset, out_name, xlim, ylim, logy=False):
    """Single-panel Faraday instability tongues matching blog's DEFAULT_FIGSIZE."""
    with h5py.File(DATA / f'pb06_faraday_{preset}.h5', 'r') as h5f:
        k = h5f['k'][:]
        a_h = h5f['a_harmonic'][:]
        a_s = h5f['a_subharmonic'][:]
        d2 = float(h5f.attrs['d2_dim'])
        f_hz = float(h5f.attrs['f_dim'])

    k_mm = k / 1e3
    kk_h = np.broadcast_to(k_mm[:, None], a_h.shape)
    kk_s = np.broadcast_to(k_mm[:, None], a_s.shape)

    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    apply_style(fig, ax)

    ax.plot(
        kk_s[np.isfinite(a_s)], a_s[np.isfinite(a_s)], '.',
        color=SUBHARMONIC, ms=3.0, zorder=3, label='subharmonic'
    )
    ax.plot(
        kk_h[np.isfinite(a_h)], a_h[np.isfinite(a_h)], '.',
        color=HARMONIC, ms=4.0, zorder=3, label='harmonic'
    )

    if logy:
        ax.set_yscale('log')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel('$k$ [mm$^{-1}$]', fontsize=11, color=INK)
    ax.set_ylabel('$a$', fontsize=11, color=INK)

    sec = ax.secondary_xaxis(
        'top', functions=(lambda x, d2=d2: x * 1e3 * d2, lambda x, d2=d2: x / (1e3 * d2))
    )
    sec.set_xlabel('$k d_2$', fontsize=10, color=INK)
    sec.tick_params(colors=INK_MUTED, labelsize=9, length=3, width=0.9)
    for side in ('top', 'right', 'left', 'bottom'):
        if side in sec.spines:
            sec.spines[side].set_color(RULE)

    legend = ax.legend(
        fontsize=9.5, loc='lower left', frameon=False,
        bbox_to_anchor=(0, 1.08), ncol=2, handletextpad=0.2, borderaxespad=0.4,
        columnspacing=1.4
    )
    for text in legend.get_texts():
        text.set_color(INK)

    fig.tight_layout(pad=0.6)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    out_path = IMAGE_DIR / out_name
    fig.savefig(out_path, dpi=DPI, facecolor=PAPER)
    plt.close(fig)
    print(f'wrote {out_path}')


if __name__ == '__main__':
    plot_dispersion('pb06-dispersion.png')
    plot_faraday_single('f10', 'pb06-tongues-f10.png', xlim=(0, 0.9), ylim=(0, 2.5), logy=False)
    plot_faraday_single('f50', 'pb06-tongues-f50.png', xlim=(0, 5.5), ylim=(0.1, 80), logy=True)
