#!/usr/bin/env python3
"""
Module M3: Adelic Partition Function — Structure, Divergence & Regularization
File: src/adelic_product.py
Associated document: 1.1.md (Definitive Research Plan, M3 specification)

Computes the adelic partition function and investigates its structure.
M2 revealed that the bare product diverges to zero — M3 characterizes this
and evaluates regularization strategies.
"""

import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from padic import PadicNumber
from padic_oscillator import Z_p, Z_inf, Z_q
from padic_analysis import sphere_measure

# ═══════════════════════════════════════════════════════════════
#  Adelic Product — bare (divergent) version
# ═══════════════════════════════════════════════════════════════

def Xi_bare(beta, omega_num=1, omega_den=1, P_max=50):
    """Bare adelic partition function (diverges to zero).
    
    Xi(beta, omega) = Z_inf(beta, omega) * prod_{p <= P_max} Z_p(beta, omega_p)
    
    As P_max increases, Xi -> 0 because Z_p -> e^{-beta} < 1 for most primes.
    
    Args:
        beta (float): Inverse temperature.
        omega_num, omega_den (int): Rational frequency omega = num/den.
        P_max (int): Maximum prime to include.
    Returns:
        (float, int): Xi value and number of primes.
    """
    omega = omega_num / omega_den
    xi = Z_inf(beta, omega)
    count = 0
    
    # Primes up to P_max
    primes = _primes_up_to(P_max)
    
    for p in primes:
        # Compute omega_p = |omega|_p
        omega_p = _padic_norm_float(p, omega_num, omega_den)
        zp = Z_p(beta, p, omega_p)
        xi *= zp
        count += 1
    
    return xi, count


def Xi_convergence_study(beta, omega_num=1, omega_den=1, P_values=None):
    """Study Xi as function of truncation prime.
    
    Returns:
        list of (P_max, Xi, cumulative_log)
    """
    if P_values is None:
        P_values = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
    
    omega = omega_num / omega_den
    xi = Z_inf(beta, omega)
    results = []
    primes_so_far = []
    
    for p in P_values:
        omega_p = _padic_norm_float(p, omega_num, omega_den)
        zp = Z_p(beta, p, omega_p)
        xi *= zp
        primes_so_far.append(p)
        log_xi = math.log(xi) if xi > 0 else float('-inf')
        results.append((p, xi, log_xi, zp))
    
    return results


# ═══════════════════════════════════════════════════════════════
#  Free Energy Approach
# ═══════════════════════════════════════════════════════════════

def Xi_free_energy(beta, omega_num=1, omega_den=1, P_max=50):
    """Adelic free energy: F_ad = -beta^{-1} ln Xi
    
    Since ln Xi = ln Z_inf + sum_p ln Z_p, and each ln Z_p is negative
    (Z_p < 1 for beta > 0), the sum diverges to -infinity.
    The divergence is linear in the number of primes.
    
    Returns:
        (F, dF_dprime): Free energy and estimate of per-prime contribution.
    """
    omega = omega_num / omega_den
    f_ad = -math.log(Z_inf(beta, omega)) / beta
    primes = _primes_up_to(P_max)
    per_prime = []
    
    for p in primes:
        omega_p = _padic_norm_float(p, omega_num, omega_den)
        zp = Z_p(beta, p, omega_p)
        df = -math.log(zp) / beta
        f_ad += df
        per_prime.append(df)
    
    avg_per_prime = sum(per_prime) / len(per_prime) if per_prime else 0
    return f_ad, per_prime, avg_per_prime


# ═══════════════════════════════════════════════════════════════
#  Ratio Regularization
# ═══════════════════════════════════════════════════════════════

def Xi_ratio(beta1, beta2, omega_num=1, omega_den=1, P_max=50):
    """Ratio of adelic products at two temperatures.
    
    R = Xi(beta1) / Xi(beta2)
    
    For large p, Z_p(beta1)/Z_p(beta2) -> e^{-(beta1-beta2)}.
    So R still diverges (or goes to zero) unless beta1 = beta2.
    
    Returns:
        (ratio, convergence_flag)
    """
    xi1, n1 = Xi_bare(beta1, omega_num, omega_den, P_max)
    xi2, n2 = Xi_bare(beta2, omega_num, omega_den, P_max)
    
    if xi2 == 0:
        return float('inf'), False
    
    ratio = xi1 / xi2
    # For beta1 != beta2, this diverges or goes to zero
    stable = abs(beta1 - beta2) < 0.01
    return ratio, stable


# ═══════════════════════════════════════════════════════════════
#  Regularization: subtract the divergent part
# ═══════════════════════════════════════════════════════════════

def Xi_regularized(beta, omega_num=1, omega_den=1, P_max=50, scheme='subtract'):
    """Regularized adelic product.
    
    scheme='subtract': Define Z_p^{reg} = Z_p(beta, omega_p) / e^{-beta}
                       so that Z_p^{reg} -> 1 as p -> infinity.
                       Then Xi_reg = Z_inf * prod_p Z_p^{reg}.
    
    This is equivalent to replacing each Z_p with Z_p * e^{+beta}.
    Since there are infinitely many primes, this adds an infinite constant.
    But the REGULARIZED product (per prime) is well-behaved.
    
    Returns:
        (Xi_reg, per_prime_factors)
    """
    omega = omega_num / omega_den
    primes = _primes_up_to(P_max)
    
    if scheme == 'subtract':
        # Regularize: divide each Z_p by its asymptotic value e^{-beta}
        xi_reg = Z_inf(beta, omega)
        per_prime_factors = []
        
        for p in primes:
            omega_p = _padic_norm_float(p, omega_num, omega_den)
            zp = Z_p(beta, p, omega_p)
            zp_reg = zp / math.exp(-beta)  # normalize to approach 1
            xi_reg *= zp_reg
            per_prime_factors.append((p, zp, zp_reg))
        
        return xi_reg, per_prime_factors
    
    elif scheme == 'zeta':
        # Zeta regularization: define the adelic product as
        # exp( sum_p [log Z_p - log(e^{-beta})] ) * Z_inf * prod e^{-beta}
        # The infinite product of e^{-beta} is 0, but we "regularize" by
        # subtracting the divergent part.
        log_xi = math.log(Z_inf(beta, omega))
        per_prime_factors = []
        
        for p in primes:
            omega_p = _padic_norm_float(p, omega_num, omega_den)
            zp = Z_p(beta, p, omega_p)
            log_xi += math.log(zp) - (-beta)  # subtract divergent part
            per_prime_factors.append((p, zp, math.log(zp) + beta))
        
        xi_reg = math.exp(log_xi)
        return xi_reg, per_prime_factors
    
    else:
        raise ValueError(f"Unknown scheme: {scheme}")


# ═══════════════════════════════════════════════════════════════
#  Helper: p-adic norm of rational omega = num/den
# ═══════════════════════════════════════════════════════════════

def _padic_norm_float(p, num, den):
    """Compute |num/den|_p as a float."""
    x = PadicNumber(p, Fraction(num, den))
    return x.norm_float()


def _primes_up_to(n):
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
#  Demo / Analysis
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    beta = 1.0
    omega = (1, 1)
    print("="*60)
    print("MODULE M3: ADELIC PARTITION FUNCTION ANALYSIS")
    print("="*60)
    print()
    
    # 1. Bare product convergence
    print("1. BARE ADELIC PRODUCT (diverges to zero)")
    print("-"*40)
    results = Xi_convergence_study(beta, 1, 1, 
        [2,3,5,7,11,13,17,19,23,29])
    for p, xi, log_xi, zp in results:
        print(f"  After p<={p:3d}: Xi = {xi:.2e}, log Xi = {log_xi:.2f}, Z_{p} = {zp:.6f}")
    print()
    
    # 2. Free energy approach
    print("2. FREE ENERGY APPROACH")
    print("-"*40)
    F, per_prime, avg = Xi_free_energy(beta, 1, 1, 50)
    print(f"  F_ad(beta=1) for p<=50: {F:.3f}")
    print(f"  Average per-prime contribution to log Xi: {-avg*beta:.4f}")
    print(f"  (Each prime adds ~{avg*beta:.4f} to -beta*F)")
    print(f"  Since Z_p -> e^(-beta) = {math.exp(-beta):.4f},")
    print(f"  each prime contributes log(e^(-beta)) = {-beta:.4f}.")
    print(f"  Sum over infinitely many primes -> -infinity -> Xi = 0")
    print()
    
    # 3. Ratio regularization
    print("3. RATIO REGULARIZATION")
    print("-"*40)
    for b2 in [0.5, 1.0, 2.0]:
        r, stable = Xi_ratio(beta, b2, 1, 1, 50)
        print(f"  Xi(1.0)/Xi({b2}) = {r:.2e}  (stable={stable})")
    print(f"  Ratio only well-defined if beta1 ~ beta2")
    print()
    
    # 4. Regularized product (subtract divergent part)
    print("4. REGULARIZED PRODUCT (Z_p / e^{-beta})")
    print("-"*40)
    xi_reg, factors = Xi_regularized(beta, 1, 1, 50, 'subtract')
    print(f"  Xi_reg (subtract, p<=50) = {xi_reg:.6f}")
    print(f"  This is finite but depends on P_max (each factor ~1)")
    print()
    
    # 5. Varying omega
    print("5. FREQUENCY DEPENDENCE")
    print("-"*40)
    for num, den in [(1,1), (2,1), (1,2), (3,2), (137,1)]:
        xi, n = Xi_bare(beta, num, den, 50)
        print(f"  omega={num}/{den} ({num/den:.3f}): Xi = {xi:.2e}  ({n} primes)")
    print()
    
    # 6. Conclusion
    print("="*60)
    print("CONCLUSION")
    print("="*60)
    print("The bare adelic partition function diverges to zero for all beta > 0.")
    print("This is because Z_p(beta,1) = e^{-beta} + O(1/p) < 1,")
    print("and the infinite product of numbers < 1 converges to zero.")
    print()
    print("The product formula constrains NORMS, not partition functions.")
    print("Three paths forward:")
    print("  1. Regularize (subtract divergent part) - mathematically ad hoc")
    print("  2. Use Veneziano amplitude (M4) - KNOWN adelic product formula")
    print("  3. Use zeta function (M6) - KNOWN adelic functional equation")
    print()
    print("RECOMMENDATION: Proceed directly to M4-M8.")
    print("The partition function approach is not the correct adelic object.")
    print("="*60)
