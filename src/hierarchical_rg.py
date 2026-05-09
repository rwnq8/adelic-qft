#!/usr/bin/env python3
"""
Module M5: Hierarchical RG & Adelic Fixed Points
File: src/hierarchical_rg.py

Implements hierarchical RG recursion maps for phi^4 theory on p-adic trees
(Bethe lattice with coordination number z = p+1).
Computes fixed points and critical exponents for multiple primes.
"""

import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ═══════════════════════════════════════════════════════════════
#  Recursion Maps
# ═══════════════════════════════════════════════════════════════

def rg_map_dyson(lam, p, c=1.0):
    """Dyson hierarchical model recursion.
    
    lambda_{n+1} = c * (p+1) * lambda_n^2 / (1 + lambda_n)^2
    
    This is a simplified map capturing the essential nonlinearity.
    For the exact map, see Lerner & Missarov (1989).
    
    Args:
        lam (float): Current coupling.
        p (int): Prime (tree valence = p+1).
        c (float): Model-dependent constant (c=1 for toy model).
    Returns:
        float: Next coupling.
    """
    z = p + 1
    denom = (1.0 + lam) ** 2
    return c * z * lam**2 / denom


def rg_map_simple(lam, p):
    """Simplest non-trivial recursion: lambda -> z * lambda^2.
    
    This is the leading-order approximation, valid for small lambda.
    """
    z = p + 1
    return z * lam**2


def rg_map_exponential(lam, p, beta=2.0):
    """Exponential-type recursion: lambda -> z * (1 - e^{-beta*lam})."""
    z = p + 1
    return z * (1.0 - math.exp(-beta * lam))


# ═══════════════════════════════════════════════════════════════
#  Fixed Point Analysis
# ═══════════════════════════════════════════════════════════════

def find_fixed_point(p, map_func, lam0=0.5, max_iter=200, tol=1e-12):
    """Find the non-trivial fixed point of an RG recursion.
    
    Iterates lam_{n+1} = f(lam_n) until convergence.
    
    Args:
        p (int): Prime.
        map_func (callable): f(lam, p) -> lam'.
        lam0 (float): Initial guess.
        max_iter (int): Maximum iterations.
        tol (float): Convergence tolerance.
    Returns:
        (float, list, bool): Fixed point, iteration history, converged flag.
    """
    history = [lam0]
    lam = lam0
    
    for i in range(max_iter):
        lam_next = map_func(lam, p)
        history.append(lam_next)
        if abs(lam_next - lam) < tol:
            return lam_next, history, True
        lam = lam_next
    
    return lam, history, False


def critical_exponent_nu(p, lam_star, map_func, dh=1e-6):
    """Compute critical exponent nu from the RG eigenvalue.
    
    nu = log(z) / log(y_T) where:
    - z = p+1 is the coordination number (scale factor)
    - y_T = f'(lambda*) is the thermal eigenvalue
    
    Args:
        p (int): Prime.
        lam_star (float): Fixed point coupling.
        map_func (callable): f(lam, p).
        dh (float): Step size for numerical derivative.
    Returns:
        float: nu.
    """
    z = p + 1
    
    # Numerical derivative f'(lambda*)
    f_plus = map_func(lam_star + dh, p)
    f_minus = map_func(lam_star - dh, p)
    fp = (f_plus - f_minus) / (2 * dh)
    
    if fp <= 0 or fp >= z:
        return float('nan')
    
    y_T = fp
    nu = math.log(z) / math.log(y_T)
    return nu


# ═══════════════════════════════════════════════════════════════
#  Adelic Combinations
# ═══════════════════════════════════════════════════════════════

def adelic_combinations(fixed_points):
    """Compute various adelic combinations of fixed points.
    
    Args:
        fixed_points (dict): {p: lambda_star} for multiple primes.
    Returns:
        dict of combination names -> values.
    """
    vals = list(fixed_points.values())
    primes = list(fixed_points.keys())
    
    results = {}
    
    # Product
    prod = 1.0
    for v in vals:
        prod *= v
    results['product'] = prod
    
    # Sum
    results['sum'] = sum(vals)
    
    # Weighted product (by 1/log(p))
    wprod = 1.0
    for p, v in fixed_points.items():
        wprod *= v ** (1.0 / math.log(p))
    results['weighted_product'] = wprod
    
    # Harmonic mean
    if all(v > 0 for v in vals):
        results['harmonic_mean'] = len(vals) / sum(1.0/v for v in vals)
    
    return results


# ═══════════════════════════════════════════════════════════════
#  Demo
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("="*60)
    print("HIERARCHICAL RG — Fixed Points & Critical Exponents")
    print("="*60)
    print()
    
    # Use the Dyson-like map
    map_func = rg_map_dyson
    
    print("Fixed points (Dyson-like map):")
    print("-"*40)
    fpoints = {}
    for p in [2, 3, 5, 7, 11]:
        lam_star, history, conv = find_fixed_point(p, map_func, lam0=0.5)
        nu = critical_exponent_nu(p, lam_star, map_func)
        fpoints[p] = lam_star
        status = "converged" if conv else "DID NOT CONVERGE"
        iters = len(history)
        print(f"  p={p:2d}: lambda* = {lam_star:.10f}  ({status} in {iters} iters)")
        print(f"         nu = {nu:.6f}" if not math.isnan(nu) else f"         nu = N/A")
    print()
    
    # Real RG: using 4-epsilon expansion (mean field-like)
    # In 4-epsilon dimensions, the Wilson-Fisher fixed point:
    # lambda* ~ epsilon/3 + O(epsilon^2)
    # For a toy comparison, use the 2D Ising exact value nu=1
    print("Real (Archimedean) reference values:")
    print("-"*40)
    print("  2D Ising: nu = 1.000000 (exact)")
    print("  3D Ising: nu = 0.630 (approx)")
    print("  Mean field: nu = 0.500000")
    print()
    
    # Adelic combinations
    print("Adelic combinations of fixed points:")
    print("-"*40)
    combos = adelic_combinations(fpoints)
    for name, val in combos.items():
        print(f"  {name}: {val:.10f}")
    print()
    
    # Compare with known constants
    print("Comparison with physical constants:")
    print("-"*40)
    print(f"  Product of lambda*: {combos['product']:.10f}")
    print(f"  alpha ~ 1/137.036 = {1/137.036:.10f}")
    print(f"  alpha (Z-mass) ~ 1/127.9 = {1/127.9:.10f}")
    print(f"  Ratio: {combos['product'] / (1/137.036):.6f}")
    print()
    
    # Cobweb data for p=2
    print("Cobweb data for p=2 (first 10 iterations):")
    print("-"*40)
    lam = 0.5
    for i in range(10):
        lam_next = map_func(lam, 2)
        print(f"  iter {i}: {lam:.10f} -> {lam_next:.10f}")
        lam = lam_next
    print()
    
    print("="*60)
    print("M5 COMPLETE")
    print("="*60)
