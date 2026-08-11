---
title: 'Parametric instability of the interface between two fluids, pt. 2'
date: 2026-08-12
description: 'Solving the viscous Faraday problem the way Kumar & Tuckerman (1994) did: analytic solutions per layer, matched at the interface, reduced to an eigenvalue problem for the forcing amplitude.'
tags: ['linear-stability', 'faraday-waves', 'floquet-analysis']
draft: false
---

[Part 1](../2026-08-faraday-linear-stability/) ended with the full hydrodynamic
system (FHS): a fourth-order ODE in each layer, coupled at the interface, for
each temporal harmonic $n$. Harmonics are not independent since the forcing ties
$n$ to $n \pm 1$.

The approach used by [Kumar & Tuckerman (1994)](#references), exploits the fact
that the bulk equation has constant coefficients and can therefore be solved in
closed form. Fixing the integration constants leaves a single scalar equation
per harmonic, which is used to write a matrix eigenvalue problem.

## Harmonic and subharmonic responses

Part 1 wrote the Floquet exponent as $s$, appearing in $\sigma_n \equiv s + i n
\omega$. Split it into its real and imaginary parts,

$$
\begin{aligned}
\sigma_n = \lambda + i(\alpha + n\omega),
\end{aligned}
$$

Because $\alpha$ is defined only modulo $\omega$, it can be restricted to $0 \le
\alpha < \omega$. The Floquet multipliers are eigenvalues of a real map, so they
are real or come in complex-conjugate pairs. This leaves two cases of interest:

- $\alpha = 0$, a **harmonic** response: the interface repeats every forcing
  period $T$.
- $\alpha = \omega/2$, a **subharmonic** response: the interface repeats every
  $2T$, oscillating at half the forcing frequency.

Both endpoints impose a reality condition linking negative to positive
harmonics,

$$
\begin{aligned}
\zeta_{-n} = \zeta_{n}^{*} \quad \text{(harmonic)}, \qquad\qquad
\zeta_{-n} = \zeta_{n-1}^{*} \quad \text{(subharmonic)},
\end{aligned}
$$

and identically for $w_{\beta n}$. Only $n \ge 0$ need therefore be carried.

## Solving each layer in closed form

The bulk equation from part 1,

$$
\begin{aligned}
\left[ \sigma_n - \nu_\beta (\partial_{zz} - k^2) \right] (\partial_{zz} - k^2) \, w_{\beta n} = 0,
\end{aligned}
$$

has constant coefficients in $z$. Its characteristic roots are $\pm k$, from the
right-hand factor, and $\pm q_{\beta n}$ from the left, where

$$
\begin{aligned}
q_{\beta n}^2 = k^2 + \frac{\sigma_n}{\nu_\beta},
\end{aligned}
$$

taking the root with positive real part. The general solution in layer $\beta$
is therefore

$$
\begin{aligned}
w_{\beta n}(z) = a_{\beta n} e^{k z} + b_{\beta n} e^{-k z} + c_{\beta n} e^{q_{\beta n} z} + d_{\beta n} e^{-q_{\beta n} z}.
\end{aligned}
$$

Two special cases collapse this. For an inviscid layer ($\nu_\beta = 0$) the
$q$-roots disappear and only $e^{\pm k z}$ survive, which is the inviscid
problem solved by [Benjamin & Ursell (1954)](#references). When $\sigma_n = 0$ the two pairs of roots coincide at $\pm k$, and the
degenerate solutions $z e^{\pm k z}$ take the place of $e^{\pm q_{\beta n} z}$.

## Matching at the interface

Each layer brings four constants, so eight per harmonic. The FHS supplies
exactly eight conditions once the normal stress balance is set aside: four at the
rigid plates, three matching conditions at the interface, and the kinematic
condition. Writing $\boldsymbol{c}_n = (a_{1n}, b_{1n}, c_{1n}, d_{1n}, a_{2n},
b_{2n}, c_{2n}, d_{2n})^{\mathsf{T}}$ and abbreviating

$$
\begin{aligned}
E_\beta^{\pm} \equiv e^{\pm k h_\beta}, \qquad Q_\beta^{\pm} \equiv e^{\pm q_{\beta n} h_\beta},
\end{aligned}
$$

the eight conditions read $\mathsf{M}_n \boldsymbol{c}_n = \sigma_n \zeta_n
\boldsymbol{e}_3$, with

$$
\begin{aligned}
\mathsf{M}_n =
\begin{bmatrix}
E_1^{-} & E_1^{+} & Q_1^{-} & Q_1^{+} & 0 & 0 & 0 & 0 \\
k E_1^{-} & -k E_1^{+} & q_1 Q_1^{-} & -q_1 Q_1^{+} & 0 & 0 & 0 & 0 \\
1 & 1 & 1 & 1 & 0 & 0 & 0 & 0 \\
1 & 1 & 1 & 1 & -1 & -1 & -1 & -1 \\
k & -k & q_1 & -q_1 & -k & k & -q_2 & q_2 \\
2k^2\mu_1 & 2k^2\mu_1 & \kappa_1 \mu_1 & \kappa_1 \mu_1 & -2k^2\mu_2 & -2k^2\mu_2 & -\kappa_2 \mu_2 & -\kappa_2 \mu_2 \\
0 & 0 & 0 & 0 & E_2^{+} & E_2^{-} & Q_2^{+} & Q_2^{-} \\
0 & 0 & 0 & 0 & k E_2^{+} & -k E_2^{-} & q_2 Q_2^{+} & -q_2 Q_2^{-}
\end{bmatrix},
\end{aligned}
$$

where $\kappa_\beta \equiv k^2 + q_{\beta n}^2$ and the harmonic index has been
dropped from $q_{\beta n}$ inside the matrix. The rows are, in order: 
- no penetration and no slip at $z = -h_1$; 
- the kinematic condition $w_{1n}(0) = \sigma_n \zeta_n$ 
- continuity of normal velocity, of tangential velocity, and of
tangential stress at $z = 0$
- and no penetration and no slip at $z = h_2$. 
The interface sits at $z = 0$, which is why the exponentials collapse to $1$ in rows
three to six.

Solving once with $\zeta_n = 1$ gives every coefficient, and hence $w_{\beta
n}(z)$, becomes a known multiple of the interface amplitude.

## Normal stress balance

The remaining equation is 

$$
\begin{aligned}
\Delta\!\left[ (\rho \sigma_n + 3\mu k^2) \partial_z w_{n} \right]
- \Delta\!\left[ \mu \, \partial_{zzz} w_{n} \right]
- \left( \Delta[\rho]\, g + \gamma k^2 \right) k^2 \zeta_n
= \frac{a \omega^2}{2} \Delta[\rho]\, k^2 \left( \zeta_{n+1} + \zeta_{n-1} \right).
\end{aligned}
$$

Every term on the left is now a known multiple of $\zeta_n$, since the previous
step gave $w_{\beta n}$ in terms of $\zeta_n$ and the derivatives of
exponentials are immediate. Collecting these terms into a single complex
coefficient $A_n$ the entire FHS reduces to

$$
\begin{aligned}
A_n \zeta_n = a \left( \zeta_{n+1} + \zeta_{n-1} \right), \qquad n \ge 0.
\end{aligned}
$$

where $A_n$ depends on $k$, on the fluid properties, and on $\sigma_n$ but not
on the forcing amplitude $a$. 

## A matrix eigenvalue problem for the forcing amplitude

The reality conditions close the system at $n = 0$. In the harmonic case
$\zeta_{-1} = \zeta_1^{*}$, and in the subharmonic case $\zeta_{-1} =
\zeta_0^{*}$, so

$$
\begin{aligned}
A_0 \zeta_0 &= 2a \operatorname{Re}(\zeta_1) && \text{(harmonic)}, \\
A_0 \zeta_0 &= a \left( \zeta_1 + \zeta_0^{*} \right) && \text{(subharmonic)},
\end{aligned}
$$

while $A_n \zeta_n = a(\zeta_{n+1} + \zeta_{n-1})$ for $n \ge 1$. Because
complex conjugation is not complex-linear, these are split into real and
imaginary parts and truncated at $n \le N$, giving a real generalised eigenvalue
problem

$$
\begin{aligned}
\mathbf{A} \boldsymbol{\zeta} = a \mathbf{B} \boldsymbol{\zeta}, \qquad
\boldsymbol{\zeta} = \left( \operatorname{Re}\zeta_0, \operatorname{Im}\zeta_0, \operatorname{Re}\zeta_1, \operatorname{Im}\zeta_1, \ldots, \operatorname{Re}\zeta_N, \operatorname{Im}\zeta_N \right)^{\mathsf{T}}.
\end{aligned}
$$

$\mathbf{A}$ is block diagonal, each harmonic contributing a $2 \times 2$
block that represents multiplication by $A_n$,

$$
\begin{aligned}
\mathbf{A} = \operatorname{diag}\left(
\begin{bmatrix} \operatorname{Re}A_0 & -\operatorname{Im}A_0 \\ \operatorname{Im}A_0 & \operatorname{Re}A_0 \end{bmatrix},
\begin{bmatrix} \operatorname{Re}A_1 & -\operatorname{Im}A_1 \\ \operatorname{Im}A_1 & \operatorname{Re}A_1 \end{bmatrix},
\ldots,
\begin{bmatrix} \operatorname{Re}A_N & -\operatorname{Im}A_N \\ \operatorname{Im}A_N & \operatorname{Re}A_N \end{bmatrix}
\right),
\end{aligned}
$$

while $\mathbf{B}$ carries the neighbour coupling and differs between the two
cases only in its first rows:

$$
\begin{aligned}
\mathbf{B} =
\begin{bmatrix}
0 & 0 & 2 & 0 & 0 & 0 & \cdots \\
0 & 0 & 0 & 0 & 0 & 0 & \cdots \\
1 & 0 & 0 & 0 & 1 & 0 & \cdots \\
0 & 1 & 0 & 0 & 0 & 1 & \cdots \\
0 & 0 & 1 & 0 & 0 & 0 & \cdots \\
\vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \ddots
\end{bmatrix}
\text{(harmonic)},
\qquad
\mathbf{B} =
\begin{bmatrix}
1 & 0 & 1 & 0 & 0 & 0 & \cdots \\
0 & -1 & 0 & 1 & 0 & 0 & \cdots \\
1 & 0 & 0 & 0 & 1 & 0 & \cdots \\
0 & 1 & 0 & 0 & 0 & 1 & \cdots \\
0 & 0 & 1 & 0 & 0 & 0 & \cdots \\
\vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \ddots
\end{bmatrix}
\text{(subharmonic)}.
\end{aligned}
$$

The harmonic case additionally forces $\zeta_0$ to be real, so its
$\operatorname{Im}\zeta_0$ column and row drop out and the system has size $2N+1$
rather than $2N+2$.

Note that we never solve for a growth rate. Setting $\lambda = 0$ and picking
$\alpha = 0$ or $\omega/2$ makes every $A_n$ a number, and the smallest positive
eigenvalue is the critical amplitude $a_c(k)$. Sweeping $k$ traces the marginal
stability tongues, subharmonic and harmonic alternating.

## References

T. B. Benjamin and F. Ursell, *The stability of the plane free surface of a
liquid in vertical periodic motion*, Proceedings of the Royal Society of London
A **225**, 505–515 (1954).
[doi:10.1098/rspa.1954.0218](https://doi.org/10.1098/rspa.1954.0218)

K. Kumar and L. S. Tuckerman, *Parametric instability of the interface between
two fluids*, Journal of Fluid Mechanics **279**, 49–68 (1994).
[doi:10.1017/S0022112094003812](https://doi.org/10.1017/S0022112094003812)
