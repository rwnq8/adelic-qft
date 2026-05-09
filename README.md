# Adelic Constraints on Quantum Field Theory

**Investigating whether the adelic completion of $\mathbb{Q}$ forces dimensionless physical constants to specific number-theoretic values.**

---

## Overview

This project investigates whether the **adelic** (simultaneous real and $p$-adic) completion of the rational numbers constrains fundamental physical constants — specifically the fine-structure constant $\alpha$ and its renormalization group flow.

### Ostrowski's Theorem

The only non-trivial completions of $\mathbb{Q}$ are:
- The real numbers $\mathbb{R}$ (Archimedean)
- The $p$-adic numbers $\mathbb{Q}_p$ for each prime $p$ (non-Archimedean)

Together they form the **adele ring** $\mathbb{A}_\mathbb{Q}$. The **product formula** states:

$$\lvert q \rvert_\infty \prod_{p} \lvert q \rvert_p = 1 \quad \text{for all } q \in \mathbb{Q}^\times$$

### Principal Finding

The **Freund-Witten (1987) adelic product formula** for the Veneziano string amplitude has been computationally verified:

$$A_\infty(s,t) \prod_{p} A_p(s,t) = 1$$

This establishes that string scattering amplitudes satisfy a consistent adelic structure across all completions of $\mathbb{Q}$.

## Quick Start

```bash
pip install numpy scipy sympy mpmath matplotlib
cd src/
python test_foundations.py          # 30/30 tests — product formula verified
python gelfand_graev_gamma.py       # Freund-Witten verification
```

## Repository Structure

```
├── 1.1.md                 Definitive Research Plan
├── 1.1.1.md               Freund-Witten Normalization Details
├── module_01–09_report.md Module execution reports
├── synthesis_final.md     Project synthesis (M10)
├── src/                   15 Python files
├── images/                9 PNG figures
├── data/                  Checkpoint data directory
└── README.md              This file
```

## Modules

| Module | Title | Status | Key Result |
|:-------|:------|:-------|:-----------|
| M1 | Foundational Library | ✅ | 30/30 tests, product formula verified |
| M2 | $p$-adic Analysis | ✅ | $Z_p \to e^{-\beta}$ (corrected original plan) |
| M3 | Adelic Partition Function | ⚠️ | $\Xi \to 0$ — diverges, pivot to M4 |
| M4 | Freund-Witten Veneziano | ✅ | **Product = 1 verified via analytic continuation** |
| M5 | Hierarchical RG | ⚠️ | Toy model; full recursion needs literature |
| M6 | Zeta Zeros | ✅ | GUE confirmed (Montgomery-Odlyzko) |
| M7 | Cross-Ratio Flow | ✅ | Discrete RG maps computed at each prime |
| M8 | Beta Reconstruction | ✅ | $\propto \alpha^2$ structure recovered |
| M9 | Null Models | ✅ | Strongest findings are mathematical identities |
| M10 | Synthesis | ✅ | Project closeout (synthesis_final.md) |

## Key Insights

1. **Adelic products of norms work** — the product formula is an exact mathematical identity
2. **Adelic products of integrated quantities diverge** — partition functions and Beta functions don't have the "= 1 almost everywhere" property that norms do
3. **The Freund-Witten product formula IS correct** — but requires the Gel'fand-Graev gamma (not Morita's) and analytic continuation via $\zeta(s)$
4. **The adelic framework constrains the STRUCTURE of physical laws** (functional forms) but not all specific numerical values (which may be contingent)

## License

MIT
