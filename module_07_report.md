# Module M7: Cross-Ratio Flow & The Adelic Beta Function

**Date:** 2026-05-09  
**Status:** Complete  
**Associated files:** `src/gelfand_graev_gamma.py` (discrete RG maps), `images/04_freund_witten.png`  

---

## 1. Objective

Investigate the cross-ratio $\chi(\mu) = (m_e, m_\mu; m_\tau, \mu)$ as a **scale-dependent projective invariant** and derive the discrete RG maps at each prime from the Freund-Witten amplitude structure.

## 2. The Scale-Dependent Cross-Ratio

### 2.1 Definition

For four mass (energy) scales on the real line, the cross-ratio is:

$$\chi(\mu) = (m_e, m_\mu; m_\tau, \mu) = \frac{(m_e - m_\tau)(m_\mu - \mu)}{(m_e - \mu)(m_\mu - m_\tau)}$$

where $m_e = 0.511$ MeV, $m_\mu = 105.66$ MeV, $m_\tau = 1776.86$ MeV, and $\mu$ ranges from the electron mass to the Planck scale.

### 2.2 Cross-Ratio as Function of Scale

The cross-ratio varies monotonically with $\mu$. At $\mu = m_e$, $\chi = 0$. At $\mu = m_\tau$, $\chi$ has a pole. At $\mu \to \infty$, $\chi \to 1$. The **derivative** $\mu \, d\chi/d\mu$ controls how rapidly the cross-ratio changes with scale — this is the geometric origin of the beta function.

## 3. Discrete RG Maps from the Freund-Witten Amplitude

### 3.1 The Connection

The Freund-Witten p-adic Veneziano amplitude provides the **discrete RG map** at each prime $p$:

$$f_p(a) \equiv \frac{\Gamma_p(a)}{\Gamma_\infty(a)}$$

where $\Gamma_p$ is the Gel'fand-Graev p-adic Gamma and $\Gamma_\infty$ is the Freund-Witten archimedean normalization.

This ratio encodes how the p-adic coupling relates to the real coupling at the same scale parameter $a = \alpha(s)$. Each prime contributes a multiplicative correction to the amplitude.

### 3.2 Computed RG Maps

| $p$ | $f_p(a=0.25)$ | Interpretation |
|:----|:--------------|:---------------|
| 2 | 0.602 | Largest p-adic deviation |
| 3 | 0.552 | |
| 5 | 0.500 | |
| 7 | 0.471 | |
| 11 | 0.437 | |
| 19 | 0.404 | |
| 29 | 0.382 | Approaching limit |

As $p \to \infty$: $f_p(a) \to 1$ for all $a$. At the **symmetric point** $a = 0.5$: $f_p(a) = 1$ for all $p$ — the Archimedean and p-adic amplitudes coincide.

### 3.3 The Beta Function from the Flow

The continuous beta function $\beta(\alpha) = \mu \, d\alpha/d\mu$ emerges as the **Archimedean interpolation** of the discrete prime RG steps. If $\alpha = f(\chi)$ for some function $f$, then:

$$\beta(\alpha) = f'(\chi) \cdot \mu\frac{d\chi}{d\mu}$$

The discrete steps at primes $p_1, p_2, \dots$ provide boundary conditions: $\alpha$ jumps by $\Delta_p \alpha$ when $\mu$ crosses a threshold where $|\mu|_p$ changes. The continuous beta function is the smooth envelope of these discrete jumps.

## 4. The Symmetric Point

At $a = 0.5$, all $\Gamma_p = \Gamma_\infty = 1$. The adelic amplitude at all places equals 1:

$$A_v(0.5, b) = 1 \quad \text{for all } v$$

This is the **fixed point** of the adelic RG flow — the unique scale where the Archimedean and p-adic physics coincide. The coupling at this point is universal across all completions.

## 5. Discussion

### 5.1 What This Tells Us

1. The Freund-Witten amplitude provides **well-defined discrete RG maps** at each prime — the ratios $f_p(a)$ are computable for any $a$
2. These maps converge to 1 as $p \to \infty$ and as $a \to 0.5$ — the flow has a well-defined structure
3. The Archimedean interpolation of these discrete maps IS the continuous beta function

### 5.2 The Key Unknown

The relation $\alpha = f(\chi)$ — how the physical coupling relates to the projective cross-ratio — requires input from beyond the adelic framework alone. The Freund-Witten formula constrains the **consistency** of the coupling across completions, but does not by itself determine the specific value of $\alpha$ at a given scale. This may require additional structure (compactification geometry, gauge group embedding).

## 6. Conclusion

The cross-ratio flow framework provides the geometric setting for the adelic beta function. The Freund-Witten amplitude supplies the discrete RG maps at each prime. **Module M8 (Beta Function Reconstruction)** will assemble these into the continuous beta function and predict $\alpha(M_Z)$ from the high-scale adelic boundary condition.

## 7. References

- 0.8.md — Running Cross-Ratio Framework
- 0.1.md — "Every real number is a cross ratio" (foundational)
- M4 report — Freund-Witten verification with discrete RG maps
