#!/usr/bin/env python3
"""3.4.py — The Adelic RG Trajectory (D6)
===========================================
Solves da/d(ln mu) = beta_inf(a) with adaptive step sizing.
Corrected finding: beta_inf(a) < 0 for ALL a in (0,1).
No sign change, no separatrix. One basin flowing to a=0 in UV.
"""

import math, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
import mpmath as mp


def beta_inf(a):
    psi = float(mp.digamma(a))
    tan_t = float(mp.tan(mp.pi * a / 2))
    return psi - float(mp.log(2 * mp.pi)) - (float(mp.pi) / 2.0) * tan_t


def rk4_step(a, dl):
    b = beta_inf
    k1 = b(a)
    k2 = b(a + 0.5 * dl * k1)
    k3 = b(a + 0.5 * dl * k2)
    k4 = b(a + dl * k3)
    return a + (dl / 6.0) * (k1 + 2*k2 + 2*k3 + k4)


def integrate_forward(a0, l_max, dl=1e-6, verbose=False):
    """Integrate da/dl = beta_inf(a) from a0 for RG time l_max.
    Adaptive: dl_eff = min(dl, 0.01*|a|/|beta|) to handle stiffness near a=0.
    Returns (a_vals, l_vals)."""
    a_vals, l_vals = [a0], [0.0]
    a, l = a0, 0.0
    while l < l_max and a > 1e-8 and a < 0.999:
        b = beta_inf(a)
        if abs(b) < 1e-15: break
        dl_eff = min(dl, 0.005 * a / abs(b)) if abs(b) > 0 else dl
        a_new = rk4_step(a, dl_eff)
        if a_new <= 1e-8 or a_new >= 0.9999: break
        a, l = a_new, l + dl_eff
        a_vals.append(a); l_vals.append(l)
        if verbose and len(a_vals) % 1000 == 0:
            print(f"  l={l:.6f} a={a:.6e} b={b:.2f}")
    return a_vals, l_vals


def main():
    print("=" * 72)
    print("THE ADELIC RG TRAJECTORY (D6) — Corrected")
    print("da/d(ln mu) = beta_inf(a) with adaptive step sizing")
    print("=" * 72)
    print()
    
    alpha_me = 1.0 / 137.036
    a_sym = 0.5
    
    # Verify: beta_inf(a) < 0 for ALL a
    print("SECTION A: beta_inf(a) is NEGATIVE for all a (0,1)")
    print("-" * 72)
    test_a = [0.001, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]
    all_neg = True
    for a in test_a:
        b = beta_inf(a)
        if b >= 0: all_neg = False
        print(f"  beta_inf({a:.3f}) = {b:14.6f}")
    
    print(f"\n  All negative: {all_neg}")
    print("  -> a ALWAYS decreases with increasing energy.")
    print("  -> Veneziano RG flows toward a=0 in the UV (asymptotic freedom-like)")
    print("  -> QED RG flows toward alpha=infinity in the UV (Landau pole)")
    print("  -> OPPOSITE behaviors — confirming D3.")
    
    # RG time from symmetric point
    print()
    print("SECTION B: RG Time from Symmetric Point to Small a")
    print("-" * 72)
    
    # Flow from a=0.5 forward (UV direction): a decreases
    # Compute l needed to go from a=0.5 to a=alpha_me
    # Since beta_inf < 0, forward l means a decreases
    # l_forward = time to go from a=0.5 down to a=alpha_me
    
    a_vals, l_vals = integrate_forward(0.5, 1.0, dl=1e-5)
    
    print(f"  From a=0.5 forward (UV): {len(a_vals)} steps")
    print(f"  Final a = {a_vals[-1]:.6e}")
    print(f"  RG time l = {l_vals[-1]:.6f}")
    print(f"  Scale ratio = exp({l_vals[-1]:.4f}) = {math.exp(l_vals[-1]):.2e}")
    
    # Find l at specific a values
    target_a = [0.4, 0.3, 0.2, 0.1, 0.05, 0.01, alpha_me]
    print(f"\n  RG time to reach each a (from a=0.5):")
    print(f"  {'a_target':>10s}  {'l':>12s}  {'|beta_inf|':>14s}  {'mu/mu(0.5)':>16s}")
    print(f"  {'-'*10}  {'-'*12}  {'-'*14}  {'-'*16}")
    for ta in target_a:
        l_at = None
        for i, av in enumerate(a_vals):
            if av <= ta:
                l_at = l_vals[i]
                break
        if l_at is not None:
            print(f"  {ta:10.4f}  {l_at:12.6f}  {abs(beta_inf(ta)):14.4f}  {math.exp(l_at):16.2e}")
    
    # QED comparison
    print()
    print("SECTION C: Comparison with QED RG Time")
    print("-" * 72)
    beta0 = 2.0 / math.pi
    l_qed = (1.0/alpha_me - 1.0/a_sym) / beta0
    l_adelic = None
    for i, av in enumerate(a_vals):
        if av <= alpha_me:
            l_adelic = l_vals[i]
            break
    
    print(f"  QED:    l(from alpha(m_e) to alpha=0.5) = {l_qed:.2f}")
    print(f"  Adelic: l(from a=0.5 to a=alpha(m_e)) = {l_adelic:.6f}" if l_adelic else "")
    if l_adelic:
        ratio_l = l_qed / l_adelic
        print(f"  Ratio l(QED) / l(adelic) = {ratio_l:.2e}")
        print(f"  This ratio IS the compactification factor:")
        print(f"  The Veneziano a-parameter evolves {ratio_l:.1e} times FASTER")
        print(f"  than the QED coupling alpha. The compactification must")
        print(f"  provide this factor to match observed running.")
    
    # Trajectory shape
    print()
    print("SECTION D: Trajectory Shape Summary")
    print("-" * 72)
    print(f"  |beta_inf(a)| minimum at a=0.5: {abs(beta_inf(0.5)):.4f}")
    print(f"  |beta_inf(a)| maximum at a->0: diverges as ~1/a")
    print(f"  beta_inf(a) < 0 everywhere: monotonic decrease of a with energy")
    print(f"  No fixed points in (0,1): a always flows to a=0")
    print(f"  The symmetric point a=0.5 is just the slowest-flow point")
    
    print()
    print("=" * 72)
    print("CONCLUSION")
    print("=" * 72)
    print("  The Veneziano amplitude's RG flow is toward asymptotic")
    print("  freedom (a->0) in the UV — opposite to QED's Landau pole.")
    print("  The compactification must INVERT this UV behavior, mapping")
    print("  the Veneziano free UV to QED's strong-coupling UV.")
    print("  The RG time ratio provides a quantitative compactification")
    print("  constraint: the Veneziano a-parameter evolves much faster")
    print("  than the physical coupling, requiring a geometric factor.")
    print("=" * 72)


if __name__ == '__main__':
    main()
