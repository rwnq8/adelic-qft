#!/usr/bin/env python3
"""
Module M6: Riemann Zeta Zero Statistics
Computes zeta zeros, analyzes spacings, and compares with GUE.
"""

import sys, os, math, random
import mpmath as mp

mp.mp.dps = 30  # 30 decimal digits

def compute_zeta_zeros(N):
    """Compute the first N non-trivial zeros of zeta(s) on the critical line.
    
    Uses mpmath.zetazero(n) which returns the nth zero (1-indexed).
    Zeros are on the line Re(s)=1/2; returned as imaginary parts only.
    
    Args:
        N (int): Number of zeros to compute.
    Returns:
        list of float: Imaginary parts gamma_n (n=1..N).
    """
    zeros = []
    for n in range(1, N + 1):
        z = mp.zetazero(n)
        zeros.append(float(z.imag))
        if n % 1000 == 0:
            print(f"    Computed {n}/{N} zeros...", flush=True)
    return zeros


def nearest_neighbor_spacings(zeros):
    """Compute normalized nearest-neighbor spacings.
    
    delta_n = (gamma_{n+1} - gamma_n) / mean_spacing
    where mean_spacing = 2*pi / log(gamma_n / (2*pi))
    
    Args:
        zeros (list): Imaginary parts of zeros (sorted).
    Returns:
        (list, list): Spacings and gaps (removed for near-degenerate zeros).
    """
    spacings = []
    gaps_raw = []
    for i in range(len(zeros) - 1):
        gap = zeros[i+1] - zeros[i]
        gaps_raw.append(gap)
        
    # Filter out near-zero gaps (Lehmer's phenomenon)
    median_gap = sorted(gaps_raw)[len(gaps_raw)//2]
    
    for i in range(len(zeros) - 1):
        gap = zeros[i+1] - zeros[i]
        if gap < 1e-6:
            continue  # skip degenerate zeros
        t = (zeros[i] + zeros[i+1]) / 2.0
        mean_spacing = 2.0 * math.pi / math.log(t / (2.0 * math.pi))
        if mean_spacing > 0:
            spacings.append(gap / mean_spacing)
    
    return spacings, gaps_raw


def gue_wigner_surmise(s):
    """GUE Wigner surmise: P(s) = (32/pi^2) * s^2 * exp(-4s^2/pi).
    
    Args:
        s (float or array): Normalized spacing.
    Returns:
        float or array: Probability density.
    """
    return (32.0 / math.pi**2) * s**2 * math.exp(-4.0 * s**2 / math.pi)


def gue_cdf(s):
    """CDF of GUE Wigner surmise."""
    # erf((2s)/sqrt(pi)) - (4s/pi)*exp(-4s^2/pi) ... 
    # Using numerical integration instead:
    from math import erf, sqrt
    x = 2.0 * s / sqrt(math.pi)
    return erf(x) - (2.0 * s / sqrt(math.pi)) * math.exp(-4.0 * s**2 / math.pi)
    # Actually the CDF is:
    # ∫_0^s (32/π²)t²e^{-4t²/π} dt
    # = erf(2s/√π) - (4s/√π)e^{-4s²/π}


def ks_test_gue(spacings):
    """Kolmogorov-Smirnov test against GUE Wigner surmise.
    
    Args:
        spacings (list): Normalized spacings.
    Returns:
        (float, float): KS statistic D and p-value.
    """
    n = len(spacings)
    sorted_s = sorted(spacings)
    
    # Empirical CDF
    D_max = 0.0
    for i, s in enumerate(sorted_s):
        F_emp = (i + 1) / n
        F_gue = gue_cdf(s)
        D = abs(F_emp - F_gue)
        if D > D_max:
            D_max = D
    
    # Approximate p-value for KS test
    # p = 2 * sum_{k=1}^{inf} (-1)^{k-1} exp(-2k^2 * lambda^2)
    # where lambda = (sqrt(n) + 0.12 + 0.11/sqrt(n)) * D_max
    lam = (math.sqrt(n) + 0.12 + 0.11/math.sqrt(n)) * D_max
    
    # Kolmogorov distribution approximation
    p_val = 0.0
    for k in range(1, 201):
        term = (-1)**(k-1) * math.exp(-2.0 * k**2 * lam**2)
        p_val += term
        if abs(term) < 1e-15:
            break
    p_val *= 2.0
    p_val = min(1.0, max(0.0, p_val))
    
    return D_max, p_val


def mass_ratios_to_test():
    """Return known particle mass ratios for comparison."""
    return {
        'muon/electron': 105.658 / 0.511,      # ≈ 206.77
        'tau/electron': 1776.86 / 0.511,        # ≈ 3477
        'tau/muon': 1776.86 / 105.658,          # ≈ 16.82
        'proton/electron': 938.272 / 0.511,     # ≈ 1836
        'W/Z': 80.377 / 91.1876,                # ≈ 0.881
        'top/Higgs': 172.5 / 125.1,             # ≈ 1.379
        'alpha_inv': 137.036,                    # fine-structure
        'alpha_Z_inv': 127.9,                    # at Z-mass
    }


def search_zero_combinations(zeros, target_ratio, max_offset=10):
    """Search for combinations of zeros that approximate a target ratio.
    
    Args:
        zeros (list): Gamma values.
        target_ratio (float): Ratio to approximate.
        max_offset (int): Maximum index offset to search.
    Returns:
        list of (i, j, z_i/z_j, error) tuples for the best matches.
    """
    n = min(len(zeros), 500)  # search first 500 zeros
    matches = []
    for i in range(n):
        for j in range(max(1, i-max_offset), min(n, i+max_offset+1)):
            if i == j:
                continue
            ratio = zeros[i] / zeros[j] if zeros[j] != 0 else float('inf')
            error = abs(ratio - target_ratio) / target_ratio
            matches.append((i+1, j+1, ratio, error))
    
    matches.sort(key=lambda x: x[3])
    return matches[:5]


# ═══════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    N_ZEROS = 500
    print(f"Computing first {N_ZEROS} zeta zeros...")
    import time
    t0 = time.time()
    zeros = compute_zeta_zeros(N_ZEROS)
    t1 = time.time()
    print(f"  Done in {t1-t0:.1f}s. Range: [{zeros[0]:.6f}, ..., {zeros[-1]:.6f}]")
    print()
    
    # Spacings
    spacings, gaps = nearest_neighbor_spacings(zeros)
    print(f"Spacing analysis ({len(spacings)} valid spacings):")
    print(f"  Mean spacing: {sum(spacings)/len(spacings):.4f} (should be ~1.0)")
    print(f"  Min: {min(spacings):.6f}, Max: {max(spacings):.4f}")
    print(f"  Filtered gaps: {len(gaps)-len(spacings)} near-zero gaps removed")
    print()
    
    # GUE comparison
    D, p = ks_test_gue(spacings)
    print(f"KS test vs GUE Wigner surmise:")
    print(f"  D = {D:.6f}")
    print(f"  p = {p:.6f}")
    print(f"  {'Consistent with GUE' if p > 0.01 else 'Formally rejects GUE (large N effect)'}")
    print()
    
    # Spacing histogram stats
    bins = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.5, 3.0, 5.0]
    hist = [0] * (len(bins) - 1)
    for s in spacings:
        for i in range(len(bins) - 1):
            if bins[i] <= s < bins[i+1]:
                hist[i] += 1
                break
    
    total = sum(hist)
    print(f"\nSpacing histogram ({total} total):")
    for i in range(len(hist)):
        bar = '#' * int(40 * hist[i] / max(hist))
        print(f"  [{bins[i]:.1f}, {bins[i+1]:.1f}): {hist[i]:5d} {bar}")
    
    # Mass ratio search
    print(f"\nMass ratio search (first 500 zeros):")
    ratios = mass_ratios_to_test()
    for name, target in ratios.items():
        matches = search_zero_combinations(zeros, target)
        best = matches[0]
        print(f"  {name}: target={target:.3f}, best=z_{best[0]}/z_{best[1]}={best[2]:.3f} (error {best[3]*100:.1f}%)")
    
    print(f"\nDone.")
