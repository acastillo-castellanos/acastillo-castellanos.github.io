---
title: 'Parametric instability of the interface between two fluids, pt. 1'
date: 2026-08-11
description: 'We revisit the work of Kumar & Tuckerman (1994).'
tags: ['linear-stability', 'faraday', 'floquet']
draft: false
---

A container holding two immiscible fluids, shaken vertically. Above a critical
amplitude, standing waves grow and oscillate at *half* the forcing frequency,
indicating a parametric resonance. [Kumar & Tuckerman (1994)](#reference)
presented the linear stability of this system for two viscous layers, reducing
it to a Floquet problem.

The goal of this series is to reproduce their results and implement the
stability analysis in Python. This first part is the theory: from the
dimensional Navier–Stokes equations down to the Floquet system that has to be
solved. The second describes the matrix eigenvalue problem for the forcing
amplitude solved by Kumar & Tuckerman, while the third presents an alternative
approach using [Dedalus](https://dedalus-project.org/).

## Physical system and dimensional parameters

We consider a two-layer system composed of two immiscible, incompressible
viscous fluids bounded by horizontal rigid boundaries. The interface separating
the two fluids is located at $z = \zeta(x, y, t)$, with a (constant) interfacial
surface tension coefficient $\gamma$. The two layers are:

- **Fluid 1 :** occupies $z \in [-h_1, 0]$, with constant density
  $\rho_1$, dynamic viscosity $\mu_1$, and kinematic viscosity
  $\nu_1 = \mu_1/\rho_1$.
- **Fluid 2 :** occupies $z \in [0, h_2]$, with constant density
  $\rho_2$, dynamic viscosity $\mu_2$, and kinematic viscosity
  $\nu_2 = \mu_2/\rho_2$.

The set of dimensional parameters is completed by the gravitational
acceleration $g$ and an externally applied time-periodic body acceleration. For
each layer $\beta \in \{1,2\}$ the system is governed by the Navier–Stokes and
mass conservation equations,

$$
\begin{aligned}
\rho_\beta \left[ \frac{\partial \boldsymbol{U}_\beta}{\partial t} + (\boldsymbol{U}_\beta \cdot \nabla) \boldsymbol{U}_\beta \right] &= -\nabla P_\beta + \mu_\beta \nabla^2 \boldsymbol{U}_\beta - \rho_\beta \boldsymbol{G}(t), \\
\nabla \cdot \boldsymbol{U}_\beta &= 0,
\end{aligned}
$$

where $\boldsymbol{U}_\beta = (U_\beta, V_\beta, W_\beta)$ is the velocity
vector and $P_\beta$ the pressure field in layer $\beta$, and 

$$
\begin{aligned}
\boldsymbol{G}(t) = \left[ g + a \omega^2 \cos(\omega t) \right] \boldsymbol{e}_z,
\end{aligned}
$$
the effective acceleration.

## Linearized perturbation equations

We decompose the fields into a time-periodic base state and infinitesimal
perturbations,

$$
\begin{aligned}
\boldsymbol{U}_\beta(\boldsymbol{x}, t) &= \boldsymbol{U}^{(0)}_\beta(z, t) + \boldsymbol{u}_\beta(\boldsymbol{x}, t), \\
P_\beta(\boldsymbol{x}, t) &= P^{(0)}_\beta(z, t) + p_\beta(\boldsymbol{x}, t), \\
\zeta(x, y, t) &= \zeta^{(0)}(x, y, t) + \zeta(x, y, t).
\end{aligned}
$$

Substituting and subtracting the base-state equations gives the linearised
momentum and mass conservation equations for the perturbations,

$$
\begin{aligned}
\rho_\beta \left[ \frac{\partial \boldsymbol{u}_\beta}{\partial t} + (\boldsymbol{U}^{(0)}_\beta \cdot \nabla)\boldsymbol{u}_\beta + (\boldsymbol{u}_\beta \cdot \nabla)\boldsymbol{U}^{(0)}_\beta \right] &= -\nabla p_\beta + \mu_\beta \nabla^2 \boldsymbol{u}_\beta, \\
\nabla \cdot \boldsymbol{u}_\beta &= 0,
\end{aligned}
$$

where the nonlinear perturbation advection terms
$(\boldsymbol{u}_\beta \cdot \nabla)\boldsymbol{u}_\beta$ have been neglected.

### Base state

In the classic Faraday problem the fluid remains quiescent in the oscillating
reference frame, so the base velocity vanishes identically,

$$ 
\begin{aligned}
\boldsymbol{U}^{(0)}_\beta = \boldsymbol{0}, \qquad \nabla P^{(0)}_\beta = -\rho_\beta \left[ g + a \omega^2 \cos(\omega t) \right] \boldsymbol{e}_z, \qquad
\zeta^{(0)} = 0
\end{aligned}
$$

and the linearised perturbation equations simplify to

$$
\begin{aligned}
\rho_\beta \frac{\partial \boldsymbol{u}_\beta}{\partial t} &= -\nabla p_\beta + \mu_\beta \nabla^2 \boldsymbol{u}_\beta, \\
\nabla \cdot \boldsymbol{u}_\beta &= 0.
\end{aligned}
$$

Note that the forcing has disappeared from the perturbation equations: it
survives only in the base pressure gradient, and will re-enter through the
normal stress balance at the interface. That is the whole mechanism of the
parametric instability.

### Expansion in normal modes

Two properties of the linearised system let us separate variables in one go.
Horizontally the problem is uniform, so its normal modes are spatial Fourier
modes $\exp{\lbrace i\boldsymbol{k}\cdot\boldsymbol{x} \rbrace}$ (where
$\boldsymbol{k} = k_x \boldsymbol{e}_x + k_y \boldsymbol{e}_y$ is the horizontal
wavenumber). In time the coefficients are $T$-periodic with $\omega = 2\pi/T$,
so its normal modes are temporal Fourier modes $\exp{\lbrace \sigma_n t
\rbrace}$ (where $\sigma_n$ is the complex Floquet exponent). Combining both 

$$
\begin{aligned}
  \begin{bmatrix}
    \boldsymbol{u}_\beta(\boldsymbol{x}, z, t) 
    \\
    p_\beta(\boldsymbol{x}, z, t) 
    \\
    \zeta(\boldsymbol{x}, t)
  \end{bmatrix}
  &= 
  \sum_{n=-\infty}^{\infty}
  \begin{bmatrix}
    \boldsymbol{u}_{\beta n}(z) 
    \\
    p_{\beta n}(z) 
    \\
    \zeta_{n}
  \end{bmatrix}
  \exp{\lbrace i \boldsymbol{k}\cdot\boldsymbol{x} + \sigma_n t \rbrace}, 
\end{aligned}
$$

Since the problem is linear and horizontally homogeneous, distinct
$\boldsymbol{k}$ never mix, so a single wavevector can be treated at a time.
Substituting the ansatz amounts to three replacement rules,

$$ 
\begin{aligned}
\nabla_H \to i\boldsymbol{k}, \qquad \nabla^2 \to \partial_{zz} - k^2, \qquad \frac{\partial}{\partial t} \to \sigma_n \equiv s + i n \omega, 
\end{aligned}
$$

with $k^2 = k_x^2 + k_y^2$, while $n$ represents the temporal harmonics.

### Bulk equation

Under these rules, incompressibility becomes

$$ 
\begin{aligned}
  \partial_z w_{\beta n} = -i \boldsymbol{k} \cdot \boldsymbol{u}_{H,\beta n}, 
\end{aligned}
$$

where $\boldsymbol{u}_{H,\beta n} = (u_{\beta n}, v_{\beta n})$ is the
horizontal velocity amplitude. The horizontal and vertical momentum equations
become

$$
\begin{aligned}
\rho_\beta \left[ \sigma_n - \nu_\beta (\partial_{zz} - k^2) \right] \boldsymbol{u}_{H,\beta n} &= -i \boldsymbol{k}\, p_{\beta n}, \\
\rho_\beta \left[ \sigma_n - \nu_\beta (\partial_{zz} - k^2) \right] w_{\beta n} &= -\partial_z p_{\beta n}.
\end{aligned}
$$

Combining both expressions leaves a single fourth-order ordinary differential
equation for $w_{\beta n}(z)$, 

$$ 
\begin{aligned}
\left[ \sigma_n - \nu_\beta (\partial_{zz} - k^2) \right] (\partial_{zz} - k^2) \, w_{\beta n} = 0. 
\end{aligned}
$$

### Boundary conditions

At the two rigid plates, no-slip and no-penetration give, for every $n$,

$$
\begin{aligned}
w_{1n} &= 0, \quad \partial_z w_{1n} = 0, && \text{at } z = -h_1, \\
w_{2n} &= 0, \quad \partial_z w_{2n} = 0, && \text{at } z = h_2.
\end{aligned}
$$

### Conditions at the interface

The interface conditions need one extra step. Every term transcribes directly
except the forcing, where the product of $\cos(\omega t)$ with the temporal
series shifts harmonics by one,

$$ 
\begin{aligned}
\cos(\omega t) \sum_n \zeta_n \exp{\lbrace i n \omega t \rbrace} 
= \frac{1}{2}\sum_n (\zeta_{n-1} + \zeta_{n+1}) \exp{\lbrace i n \omega t \rbrace}, 
\end{aligned}
$$

so that harmonic $n$ picks up its neighbours $n \pm 1$.

Four of the five conditions are statements that some quantity is continuous
across the interface, so it is worth writing $\Delta[\,\cdot\,]$ for the jump
from the lower to the upper layer, evaluated at $z = 0$. For instance,

$$ 
\begin{aligned}
\Delta[\mu \, \partial_z w_n] = \mu_1 \partial_z w_{1n} - \mu_2 \partial_z w_{2n}, 
\end{aligned}
$$

This way, the conditions at the interface read

$$
\begin{aligned}
\sigma_n \zeta_n - w_{1n} &= 0, 
\\
\Delta [w_{n}] &= 0, 
\\
\Delta [\partial_z w_{n}] &= 0, 
\\
\Delta [\mu (\partial_{zz} + k^2) w_{n}] &= 0, 
\\
\Delta \left[
  \left( \rho\sigma_n - \mu (\partial_{zz} - 3k^2) \right) \partial_z w_{n} 
\right]
&= \Delta[\rho] g k^2 \left[ \left( 1 + \frac{\gamma k^2}{g\Delta[\rho]} \right) \zeta_n 
+ \frac{a \omega^2}{2g} (\zeta_{n-1} + \zeta_{n+1}) \right]
\end{aligned}
$$

These are, in order, the kinematic condition, continuity of normal and
tangential velocity, continuity of tangential stress, and the normal stress
balance. Together with the bulk equation they constitute the **full
hydrodynamic system** (FHS).

## Reference

K. Kumar and L. S. Tuckerman, *Parametric instability of the interface between
two fluids*, Journal of Fluid Mechanics **279**, 49–68 (1994).
[doi:10.1017/S0022112094003812](https://doi.org/10.1017/S0022112094003812)
