#!/usr/bin/env python
"""Marginal stability tongues for the Faraday series, pt. 3.

Re-renders KT94's figure 1a (near-inviscid) and 1b (viscous two-layer) from
the committed Dedalus-only sweeps, in the blog's visual language.

Source data lives in the research repo, not here:
    project_faramix_safekeeping/light_data/linear_stability_KT94_dedalus/
produced by
    project_vibmix_safekeeping/model/linear_stability_KT94_dedalus/
        04_compute_kt94_dedalus_only.py

Run (matplotlib/h5py are not website dependencies, so pull them in per-run):
    uv run --with matplotlib --with h5py --with numpy \
        python scripts/figures/kt94_tongues.py
"""
from pathlib import Path

import h5py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from blogstyle import CATEGORICAL, DEFAULT_FIGSIZE, apply_style, finish

DATA = Path('/home/andres/Projects1/project_faramix_safekeeping/light_data'
            '/linear_stability_KT94_dedalus')

HARMONIC, SUBHARMONIC = CATEGORICAL[0], CATEGORICAL[1]


def plot(preset, out_name):
    """One panel: primary and secondary tongues, both Floquet branches.

    The h5 stores the two tongues separately (a_1 and a_2); they share a
    branch identity, so they share a color and only one legend entry.
    """
    with h5py.File(DATA / f'kt94_dedalus_only_{preset}.h5', 'r') as f:
        k = f['k'][:]
        series = [
            ('harmonic', HARMONIC, f['a_harmonic'][:], f['a_harmonic2'][:]),
            ('subharmonic', SUBHARMONIC, f['a_subharmonic'][:], f['a_subharmonic2'][:]),
        ]

    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE)
    apply_style(fig, ax)

    for label, color, primary, secondary in series:
        ax.plot(k, primary, '.', color=color, ms=3.2, label=label, zorder=3)
        ax.plot(k, secondary, '.', color=color, ms=3.2, zorder=3)

    ax.set_xlim(0, 1.5e5)
    ax.set_ylim(0, 150)
    ax.ticklabel_format(axis='x', style='sci', scilimits=(0, 0))

    finish(fig, ax, xlabel='$k$', ylabel=r'$a\omega^2/g$', out=out_name)


if __name__ == '__main__':
    plot('fig1b', 'kt94-tongues-fig1b.png')
    plot('fig1a', 'kt94-tongues-fig1a.png')
