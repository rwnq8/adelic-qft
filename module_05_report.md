# Module M5: Hierarchical RG — Fixed Points (Exploratory)

**Date:** 2026-05-09
**Status:** Complete — toy model analyzed; realistic RG requires more sophisticated implementation
**Associated files:** `src/hierarchical_rg.py`

---

## 1. Results

### Analytic Fixed Points (Dyson-like map)

| p | z=p+1 | λ* (unstable) | f'(λ*) | ν |
|:--|:------|:--------------|:-------|:--|
| 2 | 3 | None (discriminant < 0) | — | — |
| 3 | 4 | 1.0 (degenerate) | 1.0 | ∞ |
| 5 | 6 | 0.268 | 1.577 | 3.93 |
| 7 | 8 | 0.172 | 1.707 | 3.89 |
| 11 | 12 | 0.101 | 1.817 | 4.16 |

The fixed points are correct solutions of λ = (p+1)λ²/(1+λ)², but ν values (~4) are far from physical critical exponents (0.5–1.0). This is expected — the Dyson-like toy map lacks the non-trivial integral kernel needed for realistic critical phenomena.

### 2. Assessment

The hierarchical RG on p-adic trees is a genuine research topic (Lerner & Missarov, 1989). A proper implementation requires the full recursion integral over p-adic spheres, which depends on the specific potential. This is beyond the scope of a single-module computation.

## 3. Recommendation

Proceed to M6 (Zeta Zeros). The completed zeta function has a genuine adelic functional equation — it is the one object in the program known to satisfy an adelic constraint.

## 4. References

- Lerner & Missarov (1989). "Scalar models of p-adic QFT and hierarchical models." *Theor. Math. Phys.*, 78(2), 177–184. `[UNVERIFIED-LLM]`
