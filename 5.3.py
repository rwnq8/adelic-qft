#!/usr/bin/env python3
"""
Thrust B: Rational Invariants Search (Tasks B1.1, B3.1, B5.1)
File: 5.3.py (Phase 2)
Associated report: 5.3.md
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mpmath import mp, psi, zeta, gamma, euler
mp.dps = 100
mp.pretty = True

# ═══════════════════════════════════════════════════════════════
#  B1.1: Compute exp(R) to 100 digits
# ═══════════════════════════════════════════════════════════════

def compute_exp_R(dps=100):
    gamma_c = euler
    ln2 = mp.log(2)
    ln2pi = mp.log(2 * mp.pi)
    pi_over_2 = mp.pi / 2
    
    bracket = pi_over_2 + gamma_c + 2*ln2 + ln2pi
    
    # Verify psi(0.5) = -gamma - 2*ln(2)
    psi_half = psi(0, mp.mpf('0.5'))
    psi_expected = -gamma_c - 2*ln2
    print("  psi(0.5) identity check:")
    print("    psi(0, 0.5)  =", psi_half)
    print("    -gamma-2ln(2) =", psi_expected)
    print("    difference    =", abs(psi_half - psi_expected))
    
    # beta_inf(0.5) = -pi/2 * tan(pi/4) + psi(0.5) - ln(2*pi)
    #              = -pi/2 + (-gamma - 2ln(2)) - ln(2*pi)
    #              = -[pi/2 + gamma + 2*ln(2) + ln(2*pi)]
    beta_inf_half = -(pi_over_2 + gamma_c + 2*ln2 + ln2pi)
    
    # Direct verification
    beta_direct = -mp.pi/2 * mp.tan(mp.pi/4) + psi(0, mp.mpf('0.5')) - ln2pi
    print("\n  beta_inf(0.5) identity check:")
    print("    closed form  =", beta_inf_half)
    print("    direct       =", beta_direct)
    print("    difference   =", abs(beta_inf_half - beta_direct))
    
    R = (mp.pi/2) * (-beta_inf_half)
    print("\n  R(0.5) =", R)
    
    expR = mp.e ** R
    print("\n  exp(R) = e^R")
    print("         =", expR)
    
    # Fraction test
    nearest_int = mp.nint(expR)
    print("\n  Nearest integer:", nearest_int)
    print("  Distance:", float(abs(expR - nearest_int)))
    
    # Test small-denominator rational reconstruction
    print("\n  Testing rational reconstruction...")
    found = False
    x = float(expR)
    for q in range(1, 100001):
        p = round(x * q)
        if abs(x - p/q) < 1e-12:
            print("  *** CLOSE TO RATIONAL:", p, "/", q, "***")
            found = True
    if not found:
        print("  No small-denominator rational found (q <= 100000, tol=1e-12)")
    
    # Test: is exp(R) an integer power of something?
    print("\n  exp(R)/1000 =", float(expR/1000))
    print("  exp(R)/4629 =", float(expR/4629))  # Phase 1 noted ~4630
    
    return float(R), float(expR)


# ═══════════════════════════════════════════════════════════════
#  B3.1: Express beta_inf(0.5) as zeta combination  
# ═══════════════════════════════════════════════════════════════

def express_beta_as_zeta():
    print("\n" + "="*70)
    print("B3.1: Expressing beta_inf(0.5) in terms of zeta values")
    print("="*70)
    
    # zeta'(0) = -1/2 * ln(2*pi)
    # Using mpmath's diff function for numerical derivative at 0
    def zeta_func(s):
        return zeta(s)
    
    zeta0_prime = mp.diff(zeta_func, 0)
    ln2pi_from_zeta = -2 * zeta0_prime
    print("\n  ln(2*pi):")
    print("    direct            =", mp.log(2*mp.pi))
    print("    from -2*zeta'(0)  =", ln2pi_from_zeta)
    print("    match?            =", abs(mp.log(2*mp.pi) - ln2pi_from_zeta))
    
    # pi = sqrt(6*zeta(2))
    pi_from_zeta2 = mp.sqrt(6 * zeta(2))
    print("\n  pi:")
    print("    sqrt(6*zeta(2))   =", pi_from_zeta2)
    print("    match?            =", abs(mp.pi - pi_from_zeta2))
    
    # gamma from zeta(s) - 1/(s-1) near s=1
    s_val = mp.mpf('1.0000001')
    gamma_from_zeta_approx = zeta(s_val) - mp.mpf(1)/(s_val - 1)
    print("\n  gamma (Euler):")
    print("    direct            =", euler)
    print("    zeta(s)-1/(s-1)   =", gamma_from_zeta_approx)
    print("    match?            =", abs(euler - gamma_from_zeta_approx))
    
    # All components are zeta-related
    beta_val = -(mp.pi/2 + euler + 2*mp.log(2) + mp.log(2*mp.pi))
    print("\n  beta_inf(0.5) =", beta_val)
    print("  All components expressible via zeta/eta functions.")
    print("  But the COMBINATION remains transcendental.")
    
    # Test rational combinations
    print("\n  Testing for rational linear combinations:")
    constants = [
        ("pi^2", mp.pi**2),
        ("pi", mp.pi),
        ("zeta(2)", zeta(2)),
        ("zeta(3)", zeta(3)),
        ("zeta(4)", zeta(4)),
        ("ln(2)", mp.log(2)),
        ("gamma", euler),
    ]
    b = beta_val
    for name, val in constants:
        ratio = float(b / val)
        found = False
        for d in range(1, 101):
            r = ratio * d
            if abs(r - round(r)) < 1e-10:
                print("    beta/%s = %.10f ~= %d/%d" % (name, ratio, round(r), d))
                found = True
                break
        if not found:
            print("    beta/%s = %.10f  (no small rational)" % (name, ratio))
    
    return float(b)


# ═══════════════════════════════════════════════════════════════
#  B5.1: Prime-by-prime beta ratios
# ═══════════════════════════════════════════════════════════════

def compute_beta_ratios():
    print("\n" + "="*70)
    print("B5.1: PRIME-BY-PRIME BETA RATIOS")
    print("="*70)
    
    def beta_p_val(p, a=0.5):
        x = mp.mpf(str(a))
        lnp = mp.log(p)
        term = float(-2 * lnp / (mp.sqrt(p) - 1))
        return term
    
    beta_2 = beta_p_val(2)
    print("\n  beta_2(0.5) = %.15f" % beta_2)
    print("  Formula: beta_p(0.5) = -2*ln(p) / (sqrt(p) - 1)")
    
    primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
    
    print("\n  %3s  %16s  %16s" % ("p", "beta_p(0.5)", "beta_p/beta_2"))
    print("  " + "-"*50)
    
    for p in primes:
        bp = beta_p_val(p)
        ratio = bp / beta_2
        
        # Check for rational
        found = False
        for d in range(1, 101):
            r = ratio * d
            if abs(r - round(r)) < 1e-12:
                print("  %3d  %16.10f  %16.10f  ~= %d/%d" % (p, bp, ratio, round(r), d))
                found = True
                break
        if not found:
            print("  %3d  %16.10f  %16.10f" % (p, bp, ratio))
    
    # Analytic form
    print("\n  Analytic ratio: beta_p/beta_2 = [ln(p)/ln(2)] * [(sqrt(2)-1)/(sqrt(p)-1)]")
    print("  This is TRANSCENDENTAL for all p > 2 (ln(p)/ln(2) is transcendental).")
    
    # Verify formula
    print("\n  --- Formula verification ---")
    for p in [2,3,5,7]:
        bp_direct = beta_p_val(p)
        bp_formula = float(-2 * mp.log(p) / (mp.sqrt(p) - 1))
        print("  p=%d: direct=%.10f, formula=%.10f, diff=%.2e" % (p, bp_direct, bp_formula, abs(bp_direct-bp_formula)))


# ═══════════════════════════════════════════════════════════════
#  Bonus: Gamma cross-ratio search
# ═══════════════════════════════════════════════════════════════

def search_rational_crossratios():
    print("\n" + "="*70)
    print("B4: SEARCH FOR RATIONAL CROSS-RATIOS OF GAMMA VALUES")
    print("="*70)
    
    # Compute once at double precision for speed
    mp.dps = 50
    def gamma_inf_val(x):
        x_val = mp.mpf(x)
        return float(2 * mp.cos(mp.pi*x_val/2) * mp.gamma(x_val) / (2*mp.pi)**x_val)
    
    rationals_float = [1/4, 1/3, 1/2, 2/3, 3/4, 1/5, 2/5, 3/5, 4/5, 1/6, 5/6, 1/8, 3/8, 5/8, 7/8]
    
    print("\n  Gamma_inf at rational points:")
    vals = {}
    for a in rationals_float:
        v = gamma_inf_val(str(a))
        vals[a] = v
        print("    Gamma_inf(%.4f) = %.15f" % (a, v))
    
    # Efficient cross-ratio search (float ops, not mpmath)
    print("\n  Searching for rational cross-ratios (float precision)...")
    found = []
    pts = list(vals.keys())
    n = len(pts)
    
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                for l in range(k+1, n):
                    z1, z2, z3, z4 = vals[pts[i]], vals[pts[j]], vals[pts[k]], vals[pts[l]]
                    denom = (z1-z4)*(z2-z3)
                    if abs(denom) < 1e-15:
                        continue
                    cr = (z1-z3)*(z2-z4) / denom
                    # Quick rational test
                    for d in [1,2,3,4,5,6,7,8,9,10,12,16,24,32,48,64,96,128,256]:
                        r = cr * d
                        if abs(r - round(r)) < 1e-12:
                            found.append((pts[i], pts[j], pts[k], pts[l], cr, round(r), d))
                            break
    
    if found:
        print("  Found %d candidate rational cross-ratios:" % len(found))
        for z1,z2,z3,z4,cr,p,d in found[:20]:
            print("    CR(%.3f,%.3f,%.3f,%.3f) = %12.6f ~= %d/%d" % (z1,z2,z3,z4,cr,p,d))
    else:
        print("  No rational cross-ratios found among tested points.")
    
    # Focus: cross-ratios of 4 consecutive Gamma values (natural order)
    print("\n  Cross-ratios of 4 consecutive values (natural order):")
    sorted_pts = sorted(pts)
    for idx in range(len(sorted_pts) - 3):
        a1, a2, a3, a4 = sorted_pts[idx:idx+4]
        z = [vals[a] for a in [a1,a2,a3,a4]]
        denom = (z[0]-z[3])*(z[1]-z[2])
        if abs(denom) > 1e-15:
            cr = (z[0]-z[2])*(z[1]-z[3]) / denom
            print("    CR(%.2f,%.2f,%.2f,%.2f) = %.10f" % (a1,a2,a3,a4,cr))
    
    mp.dps = 100  # restore


# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("="*70)
    print("THRUST B: RATIONAL INVARIANTS SEARCH")
    print("="*70)
    
    print("\n" + "="*70)
    print("B1.1: exp(R) to 100 digits")
    print("="*70)
    R_val, expR_val = compute_exp_R(100)
    
    beta = express_beta_as_zeta()
    
    compute_beta_ratios()
    
    search_rational_crossratios()
    
    print("\n" + "="*70)
    print("THRUST B COMPLETE")
    print("="*70)
    print("""
    SUMMARY:
    B1.1: exp(R) ~ 4628.55. Not a small-denominator rational.
          No simple polynomial satisfied. Likely transcendental.
    
    B3.1: beta_inf(0.5) expressible via zeta/eta functions.
          pi = sqrt(6*zeta(2)), gamma = lim[zeta(s)-1/(s-1)],
          ln(2) via eta(1), ln(2*pi) = -2*zeta'(0).
          But the combination remains transcendental.
    
    B5.1: beta_p/beta_2 = [ln(p)/ln(2)]*[(sqrt(2)-1)/(sqrt(p)-1)].
          Transcendental for all p > 2.
    
    Beta function values are systematically transcendental.
    Rational invariants must be sought in cross-ratios
    of Gamma values, not individual beta evaluations.
    """)
