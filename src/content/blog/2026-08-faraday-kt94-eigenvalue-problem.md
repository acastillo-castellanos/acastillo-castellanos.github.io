---
title: 'Parametric instability of the interface between two fluids, pt. 2'
date: 2026-08-12
description: 'Solving the viscous Faraday problem the way Kumar & Tuckerman (1994) did: analytic solutions per layer, matched at the interface, reduced to an eigenvalue problem for the forcing amplitude.'
tags: ['linear-stability', 'faraday-waves', 'floquet-analysis']
draft: false
---

[Part 1](../2026-08-faraday-linear-stability/) ended with writing full
hydrodynamic system (FHS), for each temporal harmonic $n$. These harmonics are
not independent since the forcing ties $n$ to $n \pm 1$. The approach used by
[Kumar & Tuckerman (1994)](#references), solves the bulk equation in closed
form, leaving a single scalar equation per harmonic, treated as a matrix
eigenvalue problem.

## Harmonic and subharmonic responses

Part 1 wrote the Floquet exponent as $s$, appearing in $\sigma_n \equiv s + i n
\omega$. Split it into its real and imaginary parts,

$$
\begin{aligned}
\sigma_n = \lambda + i(\alpha + n\omega),
\end{aligned}
$$

Because $\alpha$ is defined only modulo $\omega$, it can be restricted to $0 \le
\alpha < \omega$. The Floquet multipliers must be real or come in
complex-conjugate pairs. We are interested in two cases,

- $\alpha = 0$, corresponding to the **harmonic** response.
- $\alpha = \omega/2$, corresponding to the **subharmonic** response.

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

The bulk equation from [part 1](../2026-08-faraday-linear-stability/),

$$
\begin{aligned}
\left[ \sigma_n - \nu_\beta (\partial_{zz} - k^2) \right] (\partial_{zz} - k^2) \, w_{\beta n} = 0,
\end{aligned}
$$

has constant coefficients in $z$, where the characteristic roots are $\pm k$ and
$\pm q_{\beta n}$, where

$$
\begin{aligned}
q_{\beta n}^2 = k^2 + \frac{\sigma_n}{\nu_\beta},
\end{aligned}
$$

taking the root with positive real part. The general solution in layer $\beta$
reads

$$
\begin{aligned}
w_{\beta n}(z) = a_{\beta n} e^{k z} + b_{\beta n} e^{-k z} + c_{\beta n} e^{q_{\beta n} z} + d_{\beta n} e^{-q_{\beta n} z}.
\end{aligned}
$$

For an inviscid layer ($\nu_\beta = 0$) the $q$-roots disappear and only $e^{\pm
k z}$ survive, which is the inviscid problem solved by [Benjamin & Ursell
(1954)](#references). When $\sigma_n = 0$ the two pairs of roots coincide at
$\pm k$, and the degenerate solutions $z e^{\pm k z}$ take the place of $e^{\pm
q_{\beta n} z}$.

## Matching at the interface

The system above gives us four constants per layer, while the FHS (excluding the
normal stress) provides eight equations. Writing $\boldsymbol{c}_n = (a_{1n},
b_{1n}, c_{1n}, d_{1n}, a_{2n}, b_{2n}, c_{2n}, d_{2n})^{\mathsf{T}}$ and
introducing

$$
\begin{aligned}
E_\beta^{\pm} \equiv e^{\pm k h_\beta}, \qquad Q_\beta^{\pm} \equiv e^{\pm q_{\beta n} h_\beta},
\end{aligned}
$$

the equation system reads $\mathsf{M}_n \boldsymbol{c}_n = \sigma_n \zeta_n
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
dropped from $q_{\beta n}$ inside the matrix. Solving once with $\zeta_n = 1$
gives every coefficient.

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

Every term on the left is a known function of $\zeta_n$. Collecting these terms
into a single complex coefficient $A_n$ the entire FHS reduces to

$$
\begin{aligned}
A_n \zeta_n = a \left( \zeta_{n+1} + \zeta_{n-1} \right), \qquad n \ge 0.
\end{aligned}
$$

## A matrix eigenvalue problem for the forcing amplitude

The reality conditions close the system at $n = 0$. 

- In the harmonic case $\zeta_{-1} = \zeta_1^{*}$
$$
\begin{aligned}
A_0 \zeta_0 &= 2a \operatorname{Re}(\zeta_1)
\end{aligned}
$$

- and in the subharmonic case $\zeta_{-1} = \zeta_0^{*}$, so

$$
\begin{aligned}
A_0 \zeta_0 &= a \left( \zeta_1 + \zeta_0^{*} \right)
\end{aligned}
$$


while $A_n \zeta_n = a(\zeta_{n+1} + \zeta_{n-1})$ for $n \ge 1$. 

Splitting into real and imaginary parts and truncated at $n \le N$, gives a
real generalised eigenvalue problem

$$
\begin{aligned}
\mathbf{A} \boldsymbol{\zeta} = a \mathbf{B} \boldsymbol{\zeta}, \qquad
\boldsymbol{\zeta} = \left( \operatorname{Re}\zeta_0, \operatorname{Im}\zeta_0, \operatorname{Re}\zeta_1, \operatorname{Im}\zeta_1, \ldots, \operatorname{Re}\zeta_N, \operatorname{Im}\zeta_N \right)^{\mathsf{T}}.
\end{aligned}
$$

where $\mathbf{A}$ is a block diagonal matrix,

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

while $\mathbf{B}$ carries the coupling,

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

Setting $\lambda = 0$ and picking $\alpha = 0$ or $\omega/2$ makes every $A_n$ a
number, and the smallest positive eigenvalue is the critical amplitude $a_c(k)$.
Sweeping $k$ traces the marginal stability tongues as done in KT94.

## References

T. B. Benjamin and F. Ursell, *The stability of the plane free surface of a
liquid in vertical periodic motion*, Proceedings of the Royal Society of London
A **225**, 505–515 (1954).
[doi:10.1098/rspa.1954.0218](https://doi.org/10.1098/rspa.1954.0218)

K. Kumar and L. S. Tuckerman, *Parametric instability of the interface between
two fluids*, Journal of Fluid Mechanics **279**, 49–68 (1994).
[doi:10.1017/S0022112094003812](https://doi.org/10.1017/S0022112094003812)
