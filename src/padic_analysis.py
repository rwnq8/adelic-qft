#!/usr/bin/env python3
"""
Module M2: p-adic Analysis
File: src/padic_analysis.py — Haar measure and integration on Q_p
Associated document: 1.1.md (Definitive Research Plan, M2 specification)

Implements the Haar measure on Q_p: measure of balls and spheres,
and radial integration for functions depending only on |x|_p.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction


# ═══════════════════════════════════════════════════════════════
#  Haar Measure on Q_p
# ═══════════════════════════════════════════════════════════════

def ball_measure(p, n):
    """Haar measure of the ball B_n = {x in Q_p : |x|_p <= p^{-n}}.
    
    Normalization: ∫_{Z_p} dx = 1.
    The ball B_n has radius p^{-n}, measure = p^{-n}.
    
    Args:
        p (int): Prime.
        n (int): Exponent (may be negative; n < 0 means large ball).
    Returns:
        float: p^{-n}
    """
    return float(p) ** (-n)


def sphere_measure(p, n):
    """Haar measure of the sphere S_n = {x in Q_p : |x|_p = p^{-n}}.
    
    S_n = B_n minus B_{n-1}
    μ(S_n) = p^{-n} - p^{-(n-1)} = p^{-n}(1 - 1/p) for n finite.
    For n = -inf (the whole space), infinite — not used.
    
    Args:
        p (int): Prime.
        n (int): Exponent (n >= 0 typically for interior spheres).
    Returns:
        float: p^{-n}(1 - p^{-1})
    """
    return float(p) ** (-n) * (1 - 1/float(p))


def ball_measure_fraction(p, n):
    """Exact Fraction version of ball_measure."""
    return Fraction(1, p ** n) if n >= 0 else Fraction(p ** (-n), 1)


def sphere_measure_fraction(p, n):
    """Exact Fraction version of sphere_measure."""
    return Fraction(p - 1, p ** (n + 1))


# ═══════════════════════════════════════════════════════════════
#  Radial Integration
# ═══════════════════════════════════════════════════════════════

def integrate_radial(f, p, n_min, n_max):
    """Integrate a radial function f(|x|_p) over Q_p between given norms.
    
    For a function that depends only on |x|_p:
        ∫ f(|x|_p) dμ(x) = Σ_{n=-∞}^{∞} f(p^{-n}) * μ(S_n)
    
    Args:
        f (callable): f(r) where r = |x|_p = p^{-n} is a float.
        p (int): Prime.
        n_min (int): Minimum sphere index (inclusive). More negative = larger radius.
        n_max (int): Maximum sphere index (inclusive). More positive = smaller radius.
    Returns:
        float: Integral over the specified range of spheres.
    """
    total = 0.0
    for n in range(n_max, n_min - 1, -1):
        r = float(p) ** (-n)
        total += f(r) * sphere_measure(p, n)
    return total


def integrate_radial_truncated(f, p, n_min, n_max, tol=1e-15):
    """Radial integration with automatic truncation when contributions drop below tol.
    
    Integrates from n = 0 outward in both directions (smaller and larger radii),
    stopping when contributions fall below tolerance.
    
    Args:
        f (callable): f(r) where r = |x|_p.
        p (int): Prime.
        n_min (int): Lower bound on n (most negative to consider).
        n_max (int): Upper bound on n (most positive to consider).
        tol (float): Stop when |contribution| < tol.
    Returns:
        (float, int): Total integral and number of terms summed.
    """
    total = 0.0
    terms = 0
    
    # Start from n = 0 (unit sphere) and go outward
    for n in range(0, n_min - 1, -1):
        r = float(p) ** (-n)
        contrib = f(r) * sphere_measure(p, n)
        total += contrib
        terms += 1
        if abs(contrib) < tol and n < -1:
            break
    
    for n in range(1, n_max + 1):
        r = float(p) ** (-n)
        contrib = f(r) * sphere_measure(p, n)
        total += contrib
        terms += 1
        if abs(contrib) < tol:
            break
    
    # Don't forget the unit ball (n = 0) was already counted in first loop
    # Actually we already did n=0 in the first loop. Let me restructure.
    return total, terms


def integrate_over_unit_ball(f, p):
    """Integrate a radial function over the unit ball Z_p.
    
    ∫_{Z_p} f(|x|_p) dμ(x) = Σ_{n=0}^{∞} f(p^{-n}) * μ(S_n)
    
    Args:
        f (callable): f(r).
        p (int): Prime.
    Returns:
        float: Integral over Z_p.
    """
    total = 0.0
    for n in range(0, 100):  # Large upper bound; series converges
        r = float(p) ** (-n)
        contrib = f(r) * sphere_measure(p, n)
        total += contrib
        if abs(contrib) < 1e-15:
            break
    return total


# ═══════════════════════════════════════════════════════════════
#  Validation & Demo
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("=== Haar Measure Validation ===")
    for p in [2, 3, 5, 7, 11]:
        total = sum(sphere_measure(p, n) for n in range(0, 50))
        print(f"p={p:2d}: sum mu = {total:.10f}  (should be ~1)")
    print()
    print("=== Radial Integration Tests ===")
    def ind(r): return 1.0 if r <= 1.0 else 0.0
    for p in [2, 3, 5]:
        r = integrate_over_unit_ball(ind, p)
        print(f"p={p}: integral of 1 over Z_{p} = {r:.10f}  (should be 1)")
    def nrm(r): return r
    for p in [2, 3, 5, 7]:
        exp = 1.0/(1.0+1.0/p)
        r = integrate_over_unit_ball(nrm, p)
        print(f"p={p}: integral of |x|_p = {r:.6f}  (expected {exp:.6f})")
    print()
    print("=== Done ===")
