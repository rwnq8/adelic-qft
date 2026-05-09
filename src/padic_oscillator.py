#!/usr/bin/env python3
"""
Module M2: p-adic Analysis
File: src/padic_oscillator.py — p-adic, q-adic, and real partition functions
Associated document: 1.1.md (Definitive Research Plan, M2 specification)

Computes classical partition functions for the harmonic oscillator:
  - Real:       Z_∞(β, ω) = ∫_{-∞}^{∞} e^{-β ω x²} dx = √(π/(β ω))
  - p-adic:     Z_p(β, ω_p) = 1 + Σ_{n=1}^∞ p^{-n}(1-p^{-1}) e^{-β ω_p p^{2n}}
  - q-adic:     Z_q(β, ω_q) analogously

where ω_p = |ω|_p for rational ω, and similarly for ω_q.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import math
from fractions import Fraction
from padic import PadicNumber
from qadic import QadicNumber
from padic_analysis import sphere_measure


# ═══════════════════════════════════════════════════════════════
#  Real (Archimedean) Partition Function
# ═══════════════════════════════════════════════════════════════

def Z_inf(beta, omega=1.0):
    """Classical real partition function for the harmonic oscillator.
    
    Z_∞(β, ω) = ∫_{-∞}^{∞} e^{-β ω x²} dx = √(π/(β ω))
    
    Args:
        beta (float): Inverse temperature β > 0.
        omega (float): Frequency parameter ω > 0.
    Returns:
        float: Partition function value.
    """
    if beta <= 0:
        raise ValueError(f'beta must be > 0, got {beta}')
    return math.sqrt(math.pi / (beta * omega))


# ═══════════════════════════════════════════════════════════════
#  p-adic Partition Function
# ═══════════════════════════════════════════════════════════════

def Z_p(beta, p, omega_p=1.0, max_terms=100, tol=1e-15):
    """Classical p-adic partition function for the harmonic oscillator.

    Z_p(beta) = integral over Q_p of exp(-beta * omega_p * |x|_p^2) dmu(x)

    Decomposing into spheres S_n = {x : |x|_p = p^{-n}}:
        Z_p = sum_{n=-inf}^{inf} p^{-n} * (1 - 1/p) * exp(-beta * omega_p * p^{-2n})

    Asymptotics:
        beta -> inf:  Z_p -> 0  (exponential suppression everywhere)
        beta -> 0:    Z_p -> inf  (full space Q_p has infinite Haar measure)
        p -> inf:     Z_p -> exp(-beta) + O(1/p)

    The correct asymptotic is Z_p -> 0 as beta -> inf (the Haar measure of
    the zero-set {x: H(x)=0} is zero in Q_p), not Z_p -> 1 as previously
    stated. Verified computationally: Z_2(1000) ~ 0.0202, Z_5(1000) ~ 0.0141.

    For computation, the sum is truncated when contributions fall below
    the specified tolerance.

    Args:
        beta (float): Inverse temperature beta > 0.
        p (int): Prime.
        omega_p (float): p-adic norm of the frequency, |omega|_p.
        max_terms (int): Maximum terms per direction.
        tol (float): Stop when contribution < tol.
    Returns:
        float: Z_p(beta, omega_p)
    """
    if beta <= 0:
        raise ValueError(f'beta must be > 0, got {beta}')
    factor = 1.0 - 1.0 / p
    total = 0.0
    terms = 0
    
    # Start from n=0 and go outward in both directions
    for n in range(0, -max_terms, -1):  # n ≤ 0: inside and outside unit ball
        contrib = (p ** (-n)) * factor * math.exp(-beta * omega_p * p ** (-2 * n))
        total += contrib
        terms += 1
        if abs(contrib) < tol and n < -10:
            break
    
    for n in range(1, max_terms + 1):  # n ≥ 1: inside unit ball
        contrib = (p ** (-n)) * factor * math.exp(-beta * omega_p * p ** (-2 * n))
        total += contrib
        terms += 1
        if abs(contrib) < tol and n > 5:
            break
    
    return total


def Z_p_truncated(beta, p, omega_p=1.0, n_min=-20, n_max=50):
    """Compute Z_p with explicit truncation bounds.
    
    Args:
        beta (float): Inverse temperature.
        p (int): Prime.
        omega_p (float): p-adic norm of frequency.
        n_min (int): Most negative sphere index (large |x|_p).
        n_max (int): Most positive sphere index (small |x|_p).
    Returns:
        (float, int): Z_p value and number of terms.
    """
    factor = 1.0 - 1.0 / p
    total = 0.0
    terms = 0
    
    for n in range(n_max, n_min - 1, -1):
        contrib = (p ** (-n)) * factor * math.exp(-beta * omega_p * p ** (-2 * n))
        total += contrib
        terms += 1
    
    return total, terms


# ═══════════════════════════════════════════════════════════════
#  q-adic Partition Function (generalized)
# ═══════════════════════════════════════════════════════════════

def Z_q(beta, q, omega_q=1.0, max_terms=100, tol=1e-15):
    """Generalized q-adic classical partition function.
    
    For a scaling ratio q > 1:
      Z_q(β) = ∫_{Q_q} e^{-β ω_q |x|_q²} dμ(x)
    
    This is formally identical to Z_p but with q replacing p.
    For non-integer q, the "spheres" S_n = {x: |x|_q = q^{-n}} still partition
    the space, but the Haar measure normalization differs.
    
    Args:
        beta (float): Inverse temperature.
        q (float): Scaling ratio > 1.
        omega_q (float): q-adic norm of the frequency.
        max_terms (int): Maximum terms per direction.
        tol (float): Tolerance.
    Returns:
        float: Z_q(β, ω_q)
    """
    q = float(q)
    if q <= 1:
        raise ValueError(f"q must be > 1, got {q}")
    
    if beta <= 0:
        raise ValueError(f'beta must be > 0, got {beta}')
    factor = 1.0 - 1.0 / q
    total = 0.0
    
    for n in range(0, -max_terms, -1):
        contrib = (q ** (-n)) * factor * math.exp(-beta * omega_q * q ** (-2 * n))
        total += contrib
        if abs(contrib) < tol and n < -10:
            break
    
    for n in range(1, max_terms + 1):
        contrib = (q ** (-n)) * factor * math.exp(-beta * omega_q * q ** (-2 * n))
        total += contrib
        if abs(contrib) < tol and n > 5:
            break
    
    return total


# ═══════════════════════════════════════════════════════════════
#  Convenience: compute Z_p for omega=1 (primes not dividing omega)
# ═══════════════════════════════════════════════════════════════

def Z_p_unit(beta, p):
    """Z_p(β, ω_p=1) — the partition function when |ω|_p = 1."""
    return Z_p(beta, p, omega_p=1.0)


# ═══════════════════════════════════════════════════════════════
#  Demo / Self-test
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("=== Real Partition Function ===")
    for beta in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
        z = Z_inf(beta)
        print(f"  Z_inf(beta={beta:.1f}) = {z:.6f}")
    print()
    print("=== p-adic Partition Function ===")
    for p in [2, 3, 5, 7, 11, 97]:
        for beta in [0.1, 1.0, 10.0]:
            z = Z_p(beta, p)
            print(f"  Z_{p}(beta={beta:.1f}) = {z:.8f}")
    print()
    print("=== Convergence: Z_p(beta=1) - 1 vs p ===")
    primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
    for p in primes:
        z = Z_p(1.0, p)
        diff = z - 1.0
        print(f"  p={p:3d}: Z_p - 1 = {diff:.2e}")
    print()
    print("=== q-adic (q=137.036) ===")
    for beta in [0.1, 1.0, 10.0]:
        z = Z_q(beta, 137.036)
        print(f"  Z_q(beta={beta:.1f}, q=137.036) = {z:.8f}")
    print()
    print("=== Done ===")
