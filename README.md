# Adelic Constraints on Quantum Field Theory

**Investigating whether the adelic completion of $\mathbb{Q}$ forces dimensionless physical constants to specific number-theoretic values.**

**Status: Phase 1 Complete — Project Closed. See [5.1.md](5.1.md) for Lessons Learned, [5.0.md](5.0.md) for Phase 2 Research Plan, [4.1.md](4.1.md) for Full Narrative, or [4.0.md](4.0.md) for Structured Capstone.**

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

---

## Phase 1: Key Results (Complete)

| # | Finding | Classification | Confidence |
|:--|:--------|:--------------|:-----------|
| 1 | Freund-Witten adelic product $= 1$ verified to $< 10^{-12}$ | `[CODE-EXECUTED]` | Mathematical identity |
| 2 | Adelic beta constraint: $\beta_\infty + \sum\beta_p = 0$ for all $a$ | `[CODE-EXECUTED]` | Mathematical identity ($< 10^{-13}$) |
| 3 | $\beta_\infty(a)$ and $\beta_{\text{QED}}(\alpha)$ are fundamentally different — $10^2$–$10^6\times$ apart | `[CODE-EXECUTED]` | Verified |
| 4 | Compactification ratio $R(0.5) = 8.44$ — pure mathematical constant ($\gamma, \ln 2, \ln\pi, \pi$) | `[CODE-EXECUTED]` | Verified |
| 5 | RG time stretch factor $S = 3,240$ — quantitative constraint on Veneziano-QED bridge | `[CODE-EXECUTED]` | Verified |
| 6 | Zeta zero mass ratio matches: **STATISTICALLY FALSIFIED** (Bonferroni + null model) | `[CODE-EXECUTED]` | Falsified |
| 7 | Adelic structure constrains functional forms, not numerical values | `[LLM-INFERRED]` | Synthesis |
| 8 | Compactification dictionary: master equation relates $\beta_\infty$ to $\beta_{\text{QED}}$ | `[CODE-EXECUTED]` | M13 |

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run all tests (88/88 passing)
cd src/
python test_foundations.py          # 30 core tests
python test_extended.py             # 58 extended tests

# 3. Reproduce key results
cd ..
python 2.9.py    # D1: Adelic beta constraint
python 3.0.py    # D3: Physical scale comparison
python 3.4.py    # D6: Adelic RG trajectory
python 3.5.py    # R9: Full adelic beta synthesis
python 3.7.py    # M13: Compactification geometry

# 4. Read the final report
#    4.0.md — Phase 1 Capstone Report (start here)
#    2.8.md — Detailed technical report (M1-M11)
#    3.7.md — M13 compactification details
```

---

## Repository Structure

```
Adelic Constraints on Quantum Field Theory/
├── 4.0.md                      ★ FINAL REPORT — Start here
├── 2.8.md                         Comprehensive Technical Report (previous capstone)
├── 1.1.md                         Definitive Research Plan v1.0
│
├── Phase 2 Research Directions:
│   ├── 2.9.md / 2.9.py            D1: Adelic Beta Constraint
│   ├── 2.10.md                    D2: Zeta Zero Mass Ratios (FALSIFIED)
│   ├── 3.0.md / 3.0.py            D3: Physical Scale Comparison
│   ├── 3.1.md / 3.1.py            D4/R8: L-Functions & Hierarchical RG
│   ├── 3.2.md / 3.2.py            D4: Completed Adelic L-Functions
│   ├── 3.3.md / 3.3.py            D5: Unification / Symmetric Point
│   ├── 3.4.md / 3.4.py            D6: Adelic RG Trajectory
│   ├── 3.5.md / 3.5.py            R9: Full Adelic Beta Synthesis
│   ├── 3.6.md / 3.6.py            R10: SM Gauge Couplings
│   └── 3.7.md / 3.7.py            M13: Compactification Geometry
│
├── Phase 1 Module Reports:
│   ├── module_01–11_report.md     M1-M11 execution reports
│   └── synthesis_final.md         M10 project synthesis
│
├── Planning:
│   └── 0.1–0.8.md, 1.1.1.md      Initial design documents
│
├── src/                           15 Python source files
│   ├── padic.py                   Core p-adic number class
│   ├── qadic.py                   Generalized q-adic valuation
│   ├── adele.py                   Adele ring & product formula
│   ├── gelfand_graev_gamma.py     Freund-Witten Veneziano amplitude
│   ├── hierarchical_rg.py         Hierarchical RG on p-adic trees
│   ├── primes.py                  Shared primality utilities
│   ├── test_foundations.py        30/30 core tests
│   └── test_extended.py           58/58 extended tests
│
├── Research PDFs:                 6 reference papers
│   ├── tmf4734.pdf                Freund-Witten (1987)
│   ├── 1104178001.pdf             Lerner & Missarov (1989)
│   └── ... (4 more)
│
└── images/                        9 PNG figures
```

---

## Research Directions Map

| # | Version | Title | Status |
|:--|:--------|:------|:------:|
| D1 | 2.9 | Adelic Beta Constraint — $\beta_\infty + \sum\beta_p = 0$ | ✅ Complete |
| D2 | 2.10 | Zeta Zero Mass Ratio Search | ❌ **Falsified** |
| D3 | 3.0 | Physical Scale Comparison — $\beta_\infty$ vs $\beta_{\text{QED}}$ | ✅ Complete |
| D4 | 3.1–3.2 | Adelic L-Functions & Langlands Program | ✅ Complete |
| D5 | 3.3 | Unification / Symmetric Point ($\mu \sim 10^{89}$ GeV) | ✅ Complete |
| D6 | 3.4 | Adelic RG Trajectory — $S = 3,240$ | ✅ Complete |
| R8 | 3.1 | Proper Hierarchical RG (Lerner & Missarov 1989) | ✅ Complete |
| R9 | 3.5 | Full Adelic Beta Function Synthesis (6 panels) | ✅ Complete |
| R10 | 3.6 | Standard Model Gauge Couplings | ✅ Complete |
| M13 | 3.7 | Compactification Geometry — The Veneziano-QED Bridge | ✅ Complete |
| **Final** | **4.0** | **Phase 1 Capstone Report** | ✅ **Complete** |

---

## Key Numerical Constants

| Symbol | Value | Origin |
|:------:|:-----:|:-------|
| $R(0.5)$ | $8.438606$ | Pure math: $\frac{\pi}{2}[\gamma + 2\ln 2 + \ln(2\pi) + \pi/2]$ |
| $S_{\text{total}}$ | $3,237$ | Veneziano/QED RG time ratio |
| $\beta_\infty(0.5)$ | $-5.372183$ | $\psi(1/2) - \ln(2\pi) - \pi/2$ |
| $\beta_0$ (QED) | $0.636620$ | $2/\pi$ |
| Max adelic error | $< 10^{-13}$ | $\max|\beta_\infty + \sum\beta_p|$ |
| Freund-Witten error | $< 10^{-12}$ | $\max|A_\infty \cdot \prod A_p - 1|$ |
| Landau pole | $\sim 10^{90}$ GeV | Where $\alpha \to 1$ |

---

## Open Questions (Phase 2)

See [4.0.md §8](4.0.md#8-open-questions--future-directions) for the full list. Priority items:

1. **Specific Calabi-Yau:** Does there exist a CY with intersection numbers producing $R \approx 8.44$?
2. **Bruhat-Tits connection:** Do $p$-adic hierarchical RG critical exponents relate to CY Hodge numbers?
3. **Falsifiable prediction:** Can the adelic structure produce a testable deviation from the Standard Model?
4. **Adelic Calabi-Yau:** Does the "compactification" need BOTH Archimedean AND $p$-adic geometry?

---

## License

MIT
