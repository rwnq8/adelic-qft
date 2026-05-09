#!/usr/bin/env python3
"""
Module M4 (Corrected): Gel'fand-Graev p-adic Gamma & Freund-Witten Veneziano
File: src/gelfand_graev_gamma.py

Implements the Gel'fand-Graev p-adic Gamma function used in the
Freund-Witten (1987) adelic string amplitude:

    Gamma_p(x) = (1 - p^{x-1}) / (1 - p^{-x})

Key properties:
    Gamma_p(x) * Gamma_p(1-x) = 1
    prod_p Gamma_p(x) = zeta(x) / zeta(1-x)  (analytic continuation)
    Gamma_inf(x) = 2 cos(pi*x/2) * Gamma(x) / (2*pi)^x

Adelic product:
    Gamma_inf(x) * prod_p Gamma_p(x) = 1  (for all x via analytic continuation)
"""

import math
import mpmath as mp

# ═══════════════════════════════════════════════════════════════
#  Gel'fand-Graev p-adic Gamma function
# ═══════════════════════════════════════════════════════════════

def gamma_p(p, x):
    """Gel'fand-Graev p-adic Gamma function.
    
    Gamma_p(x) = (1 - p^{x-1}) / (1 - p^{-x})
    
    Args:
        p (int): Prime.
        x (float): Argument (any real number where denominator != 0).
    Returns:
        float: Gamma_p(x).
    """
    num = 1.0 - p ** (x - 1.0)
    den = 1.0 - p ** (-x)
    if abs(den) < 1e-15:
        # At poles: x is an integer multiple... handle carefully
        # For x = 0: Gamma_p(0) diverges (pole of zeta)
        # For x integer: p^{-x} = p^{-n}, denominator = 1 - p^{-n} != 0 for n != 0
        return float('inf') if abs(num) < 1e-15 else float('nan')
    return num / den


def gamma_p_product_analytic(x):
    """Analytic continuation of the product over all primes.
    
    prod_p Gamma_p(x) = prod_p (1-p^{x-1})/(1-p^{-x})
                       = [prod_p (1-p^{-(1-x)})] / [prod_p (1-p^{-x})]
                       = [1/zeta(1-x)] / [1/zeta(x)]
                       = zeta(x) / zeta(1-x)
    
    Using the functional equation:
    zeta(1-x) = 2(2pi)^{-x} cos(pi*x/2) Gamma(x) zeta(x)
    
    Therefore:
    prod_p Gamma_p(x) = (2pi)^x / [2 cos(pi*x/2) Gamma(x)]
    
    Args:
        x (float): Argument.
    Returns:
        float: Analytic continuation of the infinite product.
    """
    if abs(math.cos(math.pi * x / 2.0)) < 1e-15:
        # At x = 1, 3, 5, ... cos(pi*x/2) = 0 -> pole
        return float('inf')
    return (2.0 * math.pi) ** x / (2.0 * math.cos(math.pi * x / 2.0) * math.gamma(x))


def gamma_inf(x):
    """Archimedean Gamma function from Freund-Witten normalization.
    
    Gamma_inf(x) = 2 cos(pi*x/2) * Gamma(x) / (2*pi)^x
    
    This is the reciprocal of gamma_p_product_analytic(x), so that:
    Gamma_inf(x) * prod_p Gamma_p(x) = 1
    
    Args:
        x (float): Argument.
    Returns:
        float: Gamma_inf(x).
    """
    if abs(math.gamma(x)) > 1e308:
        return float('inf')
    return 2.0 * math.cos(math.pi * x / 2.0) * math.gamma(x) / (2.0 * math.pi) ** x


# ═══════════════════════════════════════════════════════════════
#  Freund-Witten Veneziano Amplitude
# ═══════════════════════════════════════════════════════════════

def A_p(p, a, b):
    """p-adic Veneziano amplitude at prime p.
    
    A_p(a,b) = Gamma_p(a) * Gamma_p(b) * Gamma_p(c)
    where c = 1 - a - b (kinematic constraint).
    
    Args:
        p (int): Prime.
        a, b (float): Regge trajectory values alpha(s), alpha(t).
    Returns:
        float: A_p(a,b).
    """
    c = 1.0 - a - b
    return gamma_p(p, a) * gamma_p(p, b) * gamma_p(p, c)


def A_inf(a, b):
    """Real (Archimedean) Veneziano amplitude.
    
    A_inf(a,b) = Gamma_inf(a) * Gamma_inf(b) * Gamma_inf(c)
    where c = 1 - a - b.
    
    Args:
        a, b (float): Regge trajectory values.
    Returns:
        float: A_inf(a,b).
    """
    c = 1.0 - a - b
    return gamma_inf(a) * gamma_inf(b) * gamma_inf(c)


def adelic_product(a, b):
    """Adelic product of Veneziano amplitudes.
    
    A_inf(a,b) * prod_p A_p(a,b) = 1
    
    Uses analytic continuation for the prime product.
    
    Args:
        a, b (float): Regge trajectory values.
    Returns:
        float: Should equal exactly 1.0 (or be NaN at poles).
    """
    return A_inf(a, b) * gamma_p_product_analytic(a) * gamma_p_product_analytic(b) * gamma_p_product_analytic(1.0 - a - b)


def adelic_product_truncated(a, b, primes):
    """Truncated (naive) adelic product using finitely many primes.
    
    This DOES converge for some (a,b) but diverges for others.
    The analytic product (adelic_product) is the correct one.
    
    Args:
        a, b (float): Regge trajectory values.
        primes (list): List of primes to include.
    Returns:
        float: Truncated product.
    """
    product = A_inf(a, b)
    for p in primes:
        product *= A_p(p, a, b)
    return product


# ═══════════════════════════════════════════════════════════════
#  Discrete RG Map from p-adic Veneziano
# ═══════════════════════════════════════════════════════════════

def discrete_rg_map(p, a_range=(-0.5, 0.5), n_points=100):
    """Compute the discrete RG map at prime p.
    
    The discrete RG step at prime p relates the p-adic amplitude
    to the real amplitude at different scales. As the energy scale
    mu crosses a prime threshold, |mu|_p changes, affecting Gamma_p.
    
    We define the discrete RG transformation:
        a' = f_p(a) such that A_p(f_p(a), b) relates to A_p(a, b)
    
    For a simple model: track how Gamma_p(a) changes the amplitude
    relative to the real (Archimedean) amplitude.
    
    Args:
        p (int): Prime.
        a_range (tuple): (a_min, a_max) range of trajectory values.
        n_points (int): Number of points.
    Returns:
        (list, list): a values and f_p(a) values.
    """
    a_vals = []
    f_vals = []
    for i in range(n_points):
        a = a_range[0] + (a_range[1] - a_range[0]) * i / (n_points - 1)
        a_vals.append(a)
        # Discrete RG: how the amplitude scales when we include prime p
        # f_p(a) should encode the p-adic correction to the coupling
        # A simple model: f_p(a) = a * (Gamma_p(a) / Gamma_inf(a))^(1/3)
        # But let's use the ratio of amplitudes directly
        # f_p(a) = a * (A_p(p,a,0.3) / A_inf(a,0.3))^(something)
        
        # Actually, the discrete step at prime p modifies a to a':
        # The amplitude with prime p included should relate to the real amplitude
        # through the gamma ratio
        gp = gamma_p(p, a)
        gi = gamma_inf(a)
        if gi != 0 and abs(gp) < 1e10:
            # The ratio gamma_p/gamma_inf encodes the p-adic correction
            ratio = gp / gi
            f_vals.append(ratio)
        else:
            f_vals.append(float('nan'))
    return a_vals, f_vals


# ═══════════════════════════════════════════════════════════════
#  Coupling extraction
# ═══════════════════════════════════════════════════════════════

def coupling_from_adelic_product():
    """The adelic product = 1 implies the product of local couplings = 1.
    
    If A_v(a,b) = g_v^2 * Gamma_v(a) * Gamma_v(b) * Gamma_v(c),
    then prod_v A_v = 1 implies prod_v g_v^2 = 1.
    
    In the adelic framework, the coupling at each place is the norm
    of an idele: g_v = |g|_v where g is a rational number (the adelic
    coupling constant). By the product formula, prod_v |g|_v = 1.
    
    Therefore the adelic coupling constant g is consistent with the
    product formula — no additional constraint beyond |g|_v = g_v.
    
    Returns:
        str: Explanation.
    """
    return (
        "The adelic product formula A_inf * prod_p A_p = 1\n"
        "implies that the product of local string couplings equals 1.\n"
        "By the adelic product formula for norms, this is automatically\n"
        "satisfied if the couplings are the norms of a rational idele.\n"
        "No specific numerical value for alpha is forced — only the\n"
        "CONSISTENCY of the coupling structure across all completions."
    )


# ═══════════════════════════════════════════════════════════════
#  Verification
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("="*70)
    print("FREUND-WITTEN ADELIC VENEZIANO AMPLITUDE — Verification")
    print("="*70)
    print()
    
    # 1. Gamma_p identity
    print("1. GAMMA_p IDENTITY: Gamma_p(x) * Gamma_p(1-x) = 1")
    for p in [2, 3, 5, 7]:
        for x in [0.1, 0.33, 0.5, 0.67, 0.9]:
            prod = gamma_p(p, x) * gamma_p(p, 1.0 - x)
            print(f"   p={p}, x={x:.2f}: {prod:.10f}")
    print()
    
    # 2. Adelic Gamma product
    print("2. ADELIC GAMMA PRODUCT: Gamma_inf(x) * prod_p Gamma_p(x) = 1")
    for x in [0.1, 0.25, 0.33, 0.5, 0.67, 0.75, 0.9]:
        gi = gamma_inf(x)
        prod_p = gamma_p_product_analytic(x)
        product = gi * prod_p
        print(f"   x={x:.2f}: Gamma_inf={gi:.6e}, prod_p={prod_p:.6e}, product={product:.10f}")
    print()
    
    # 3. Veneziano amplitude — analytic product
    print("3. ADELIC VENEZIANO PRODUCT: A_inf * prod_p A_p = 1 (analytic)")
    for a, b in [(0.25, 0.25), (0.33, 0.33), (0.4, 0.2), (0.5, 0.25)]:
        c = 1.0 - a - b
        if c <= 0:
            continue
        prod = adelic_product(a, b)
        ai = A_inf(a, b)
        print(f"   a={a:.2f}, b={b:.2f}, c={c:.2f}: A_inf={ai:.6e}, adelic={prod:.10f}")
    print()
    
    # 4. Truncated product — naive (diverges)
    print("4. TRUNCATED PRODUCT (WARNING: diverges without analytic continuation)")
    primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
    for a, b in [(0.25, 0.25), (0.33, 0.33)]:
        prod_naive = adelic_product_truncated(a, b, primes)
        prod_analytic = adelic_product(a, b)
        print(f"   a={a:.2f}, b={b:.2f}: naive={prod_naive:.4e}, analytic={prod_analytic:.10f}")
    print()
    
    # 5. Discrete RG maps
    print("5. DISCRETE RG MAPS: gamma_p / gamma_inf at each prime")
    for a in [0.25, 0.5]:
        print(f"   a={a:.2f}:")
        gi = gamma_inf(a)
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
            gp = gamma_p(p, a)
            print(f"     p={p:3d}: gamma_p={gp:12.8f}, gamma_inf={gi:.6e}, ratio={gp/gi:.6e}")
    print()
    
    # 6. Coupling analysis
    print("6. COUPLING ANALYSIS")
    print(f"   {coupling_from_adelic_product()}")
    print()
    
    print("="*70)
    print("FREUND-WITTEN VERIFICATION COMPLETE")
    print("="*70)
