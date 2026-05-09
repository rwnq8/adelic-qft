#!/usr/bin/env python3
"""
Module M4: p-adic Gamma Function (Morita)
File: src/padic_gamma.py

Implements the Morita p-adic gamma function Gamma_p: Z_p -> Z_p^x.
Defined for integer n >= 1 as:
    Gamma_p(n) = (-1)^n * prod_{k=1, p∤k}^{n-1} k

Properties:
    Gamma_p(n+1) = gamma_mult(n) * Gamma_p(n)
    where gamma_mult(n) = n  if p ∤ n
                         -1  if p | n
    Gamma_p(1) = -1
"""

import math
from fractions import Fraction


def morita_gamma(p, n, use_fraction=True):
    """Compute Morita's p-adic gamma function Gamma_p(n).

    Gamma_p(n) = (-1)^n * prod_{k=1}^{n-1} k   (k not divisible by p)

    Args:
        p (int): Prime.
        n (int): Positive integer argument (n >= 1).
        use_fraction (bool): Return Fraction if True, int if False.

    Returns:
        Fraction or int: Gamma_p(n).
    """
    if n < 1:
        raise ValueError(f"Gamma_p defined for n >= 1, got {n}")

    if use_fraction:
        result = Fraction(1, 1)
    else:
        result = 1

    sign = (-1) ** n

    for k in range(1, n):
        if k % p != 0:
            if use_fraction:
                result *= Fraction(k, 1)
            else:
                result *= k

    if use_fraction:
        result *= Fraction(sign, 1)
    else:
        result *= sign

    return result


def morita_gamma_int(p, n):
    """Gamma_p(n) as integer."""
    return morita_gamma(p, n, use_fraction=False)


def morita_gamma_frac(p, n):
    """Gamma_p(n) as Fraction."""
    return morita_gamma(p, n, use_fraction=True)


def gamma_multiplier(p, n):
    """The multiplier epsilon_p(n) such that Gamma_p(n+1) = epsilon_p(n) * Gamma_p(n).

    epsilon_p(n) = n  if n mod p != 0 (p does not divide n)
                 = 1  if n mod p == 0 (p divides n)

    Actually the true relation is:
    Gamma_p(n+1) = gamma_mult(n) * Gamma_p(n)
    where gamma_mult(n) = n if p ∤ n, else -1

    Wait, let me verify. Gamma_p(n) = (-1)^n prod_{k<p∤k}^{n-1} k
    Gamma_p(n+1) = (-1)^{n+1} prod_{k<p∤k}^{n} k
                 = (-1)^{n+1} * [prod_{k<p∤k}^{n-1} k] * (n if p∤n else skip)
                 = (-1) * (-1)^n * prod * (n if p∤n else 1)
                 = (-1) * Gamma_p(n) * (n if p∤n else 1)

    Wait: (-1)^{n+1} = (-1) * (-1)^n
    prod_{k<p∤k}^{n} k = prod_{k<p∤k}^{n-1} k * (n if p∤n else 1)

    So Gamma_p(n+1) = (-1) * Gamma_p(n) * (n if p∤n else 1)

    Hmm, = -n * Gamma_p(n) if p∤n
         = -1 * Gamma_p(n) if p|n

    No wait: Gamma_p(n+1) = (-1)^{n+1} * prod_{k=1, p∤k}^{n} k
    Gamma_p(n) = (-1)^n * prod_{k=1, p∤k}^{n-1} k

    Ratio: Gamma_p(n+1)/Gamma_p(n) = (-1) * (n if p∤n, else 1 because the product skips n)

    Hmm, that gives: Gamma_p(n+1) = -n * Gamma_p(n) if p∤n
                                   = -1 * Gamma_p(n) if p|n

    But the standard relation is:
    Gamma_p(n+1) = -n * Gamma_p(n) if p∤n   (but with sign conventions that differ)

    Let me check numerically rather than derive.

    Args:
        p (int): Prime.
        n (int): n >= 1.

    Returns:
        int: The factor relating Gamma_p(n+1) to Gamma_p(n).
    """
    g_n = morita_gamma_int(p, n)
    g_np1 = morita_gamma_int(p, n + 1)
    return g_np1 // g_n if g_n != 0 else 0


def verify_gamma_identities(p, max_n=20):
    """Verify known identities of Morita's Gamma_p.

    Returns:
        dict: Results of verification.
    """
    results = {}

    # Identity 1: Gamma_p(n+1)/Gamma_p(n) relation
    ratios = []
    for n in range(1, max_n):
        g_n = morita_gamma_int(p, n)
        g_np1 = morita_gamma_int(p, n + 1)
        if g_n != 0:
            ratio = g_np1 // g_n
            if n % p != 0:
                expected = -n  # Gamma_p(n+1) = -n * Gamma_p(n) for p∤n
            else:
                expected = -1  # Gamma_p(n+1) = -Gamma_p(n) for p|n
            ratios.append((n, ratio, expected, ratio == expected))
    results['ratio_identity'] = ratios

    # Identity 2: Reflection formula for n=2
    # Gamma_p(n) * Gamma_p(1-n) ... hmm, this is for p-adic integer arguments
    # Not directly testable with our integer-only implementation

    return results


def compute_beta_p(p, a, b):
    """p-adic Beta function B_p(a,b) = Gamma_p(a) * Gamma_p(b) / Gamma_p(a+b).

    For integer a, b >= 1.

    Args:
        p (int): Prime.
        a, b (int): Positive integers.

    Returns:
        Fraction: B_p(a,b).
    """
    ga = morita_gamma_frac(p, a)
    gb = morita_gamma_frac(p, b)
    gab = morita_gamma_frac(p, a + b)

    if gab == 0:
        return Fraction(0, 1)

    return ga * gb / gab


def compute_beta_real(a, b):
    """Real (Archimedean) Beta function B(a,b) = Gamma(a)Gamma(b)/Gamma(a+b).

    Args:
        a, b (int): Positive integers.

    Returns:
        Fraction: B(a,b) = (a-1)!(b-1)!/(a+b-1)!
    """
    import math as _math
    return Fraction(
        _math.factorial(a - 1) * _math.factorial(b - 1),
        _math.factorial(a + b - 1)
    )


def primes_up_to(n):
    """Return list of primes <= n."""
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n+1, i):
                sieve[j] = False
    return [i for i in range(2, n+1) if sieve[i]]


# ═══════════════════════════════════════════════════════════════
#  Demo / Self-test
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("="*60)
    print("MORITA p-ADIC GAMMA FUNCTION — Verification")
    print("="*60)
    print()

    # Gamma_p values for small n, p
    for p in [2, 3, 5]:
        print(f"Gamma_{p}(n) for n=1..10:")
        vals = [morita_gamma_int(p, n) for n in range(1, 11)]
        print(f"  {vals}")
        print()

    # Ratio identity
    print("Ratio identity Gamma_p(n+1)/Gamma_p(n):")
    for p in [2, 3, 5]:
        results = verify_gamma_identities(p, 12)
        all_ok = all(r[3] for r in results['ratio_identity'])
        status = "PASS" if all_ok else "FAIL"
        print(f"  p={p}: {status}")
        if not all_ok:
            for n, ratio, expected, ok in results['ratio_identity']:
                if not ok:
                    print(f"    n={n}: got {ratio}, expected {expected}")
    print()

    # Beta function values
    print("Beta function B_p(a,b) = Gamma_p(a)Gamma_p(b)/Gamma_p(a+b):")
    for p in [2, 3, 5, 7]:
        for a, b in [(1,1), (2,2), (1,3), (4,4)]:
            bp = compute_beta_p(p, a, b)
            br = compute_beta_real(a, b)
            print(f"  p={p}, B_p({a},{b}) = {bp},  B_real({a},{b}) = {br}")
    print()

    # Adelic product for small a,b
    print("="*60)
    print("ADELIC BETA PRODUCT: B_real * prod_p B_p")
    print("="*60)
    print()

    for a, b in [(1,1), (2,2), (3,3), (1,4), (2,5)]:
        product = compute_beta_real(a, b)
        primes = primes_up_to(50)
        print(f"B_real({a},{b}) = {product}")
        for p in primes:
            bp = compute_beta_p(p, a, b)
            product *= bp
            # Show the first few
            if p <= 7:
                print(f"  * B_{p}({a},{b}) = {bp}  -> product = {product}")
        print(f"  ... (after {len(primes)} primes): adelic product = {float(product):.6e}")
        print()
