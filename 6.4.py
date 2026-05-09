#!/usr/bin/env python3
"""
Thrust H: Extension to Quark Sector and CKM
File: 6.4.py (Phase 3, Thrust H)
Associated report: 6.4.md

OBJECTIVE: Test whether the adelic framework constrains quark mass ratios
or CKM mixing angles, even though the lepton coincidence was falsified.

CONTEXT: Thrusts F and G showed log(m_mu/m_e) ~ 16/3 is NOT derivable from
the adelic structure and does NOT extend to tau. The quark sector is
different: 6 masses, SU(3) color, CKM mixing — richer phenomenology.

STRATEGY:
  H1: Quark analogue of a = 1/3 — test Veneziano-like parameters
  H2: Quark mass ratio patterns — search for adelic/rational expressions
  H3: CKM elements as cross-ratios — test if |V_ij| match rational CRs
  H4: Quark beta function relations — b_0(QCD) vs mass ratio patterns

CAVEAT: Quark masses have large uncertainties (especially u, d, s).
Mass ratios are better constrained than absolute masses.
"""

import sys, os, math, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mpmath import mp, gamma, zeta, pi as mppi
mp.dps = 100

from fractions import Fraction

# ===================================================================
#  QUARK MASS DATA (PDG 2024)
# ===================================================================

# MS-bar masses at 2 GeV (MeV) for light quarks, pole masses for heavy
quark_masses = {
    # (mass_MeV, uncertainty_rel)
    'u': (2.16, 0.25),       # up: 2.16 +/- 0.49 MeV
    'd': (4.67, 0.22),       # down: 4.67 +/- 0.48 MeV
    's': (93.4, 0.08),       # strange: 93.4 +/- 8.6 MeV (at 2 GeV)
    'c': (1270.0, 0.02),     # charm: 1.27 +/- 0.02 GeV (MS-bar at m_c)
    'b': (4180.0, 0.007),    # bottom: 4.18 +/- 0.03 GeV (MS-bar at m_b)
    't': (172500.0, 0.003),  # top: 172.5 +/- 0.5 GeV (pole mass)
}

# Mass ratios (central values)
quark_ratios = {}
quark_names = ['u', 'd', 's', 'c', 'b', 't']
for i, qi in enumerate(quark_names):
    for j, qj in enumerate(quark_names):
        if i >= j:
            continue
        ratio = quark_masses[qj][0] / quark_masses[qi][0]
        # Propagate uncertainties (add in quadrature, relative)
        rel_err = math.sqrt(quark_masses[qi][1]**2 + quark_masses[qj][1]**2)
        abs_err = ratio * rel_err
        quark_ratios[f'{qj}/{qi}'] = (ratio, abs_err)
        quark_ratios[f'log_{qj}/{qi}'] = (math.log(ratio), rel_err / math.log(ratio) if math.log(ratio) > 0 else float('inf'))

# CKM matrix (PDG 2024 global fit, Wolfenstein parameterization)
ckm_magnitudes = {
    '|V_ud|': (0.97373, 0.00031),
    '|V_us|': (0.2243, 0.0008),
    '|V_ub|': (0.00382, 0.00020),
    '|V_cd|': (0.221, 0.004),
    '|V_cs|': (0.975, 0.006),
    '|V_cb|': (0.0408, 0.0014),
    '|V_td|': (0.0086, 0.0002),
    '|V_ts|': (0.0415, 0.0009),
    '|V_tb|': (1.014, 0.029),
}

# ===================================================================
#  HEADER
# ===================================================================

print("=" * 70)
print("THRUST H: EXTENSION TO QUARK SECTOR AND CKM")
print("=" * 70)

print(f"\n--- Quark Masses (PDG 2024, central values) ---")
for q in quark_names:
    m, err = quark_masses[q]
    unit = "MeV" if m < 1000 else ("GeV" if m < 1e6 else "GeV")
    disp = m if m < 1000 else (m/1000 if m < 1e6 else m/1000)
    print(f"  m_{q} = {disp:.4f} {unit}  (+/- {err*100:.1f}%)")

print(f"\n--- Key Quark Mass Ratios ---")
key_ratios = ['d/u', 's/d', 'c/s', 'b/c', 't/b', 't/u', 't/c']
for key in key_ratios:
    if key in quark_ratios:
        r, err = quark_ratios[key]
        if f'log_{key}' in quark_ratios:
            log_r, log_err = quark_ratios[f'log_{key}']
            print(f"  m_{key} = {r:.4f} +/- {err:.4f}   log = {log_r:.6f}")
        else:
            print(f"  m_{key} = {r:.4f} +/- {err:.4f}")

print(f"\n--- CKM Magnitudes ---")
for name, (val, err) in ckm_magnitudes.items():
    print(f"  {name} = {val:.6f} +/- {err:.6f}")

# ===================================================================
#  H1: Quark analogue of Veneziano parameter a = 1/3
# ===================================================================

print("\n" + "=" * 70)
print("H1: QUARK ANALOGUE OF VENEZIANO PARAMETER a = 1/3")
print("=" * 70)

print("""
  For leptons: the symmetric point a = 1/3 gave
    A_inf(1/3, 1/3) = Gamma_inf(1/3)^3 = 15.8997...
    
  For quarks: the relevant parameter might involve SU(3) color.
  QCD beta function at one loop:
    b_0(QCD) = (11*N_c - 2*n_f) / 3 = (33 - 2*n_f) / 3
    
  With n_f = 6 (all quarks): b_0 = (33 - 12)/3 = 7
  With n_f = 5 (below top):   b_0 = (33 - 10)/3 = 23/3 = 7.667
  With n_f = 4 (below bottom): b_0 = (33 - 8)/3 = 25/3 = 8.333
  With n_f = 3 (below charm):  b_0 = (33 - 6)/3 = 9
  
  For leptons (QED): b_0 = 2*sum Q_f^2 / (3*pi) = 16/(3*pi)
  
  Quark analogue: Could log(m_t/m_b) or log(m_b/m_c) relate to b_0(QCD)?
  
  log(m_t/m_b) = log(172.5/4.18) = log(41.27) = 3.720...
  b_0(QCD, n_f=5) = 23/3 = 7.667...
  log(m_t/m_b) / b_0 = 3.720/7.667 = 0.485...
  
  log(m_b/m_c) = log(4.18/1.27) = log(3.291) = 1.191...
  b_0(QCD, n_f=4) = 25/3 = 8.333...
  log(m_b/m_c) / b_0 = 1.191/8.333 = 0.143...
  
  No obvious simple relationship.
""")

# Systematic check: log ratios vs beta function coefficients
print("  --- H1: Systematic beta function test ---")
beta_qed = 2.0 * 8.0 / (3.0 * math.pi)  # b_0(QED) = 16/(3*pi)
beta_qcd = {nf: (33.0 - 2.0*nf)/3.0 for nf in [3, 4, 5, 6]}

print(f"  b_0(QED, SM) = {beta_qed:.6f}")
for nf, b in beta_qcd.items():
    print(f"  b_0(QCD, n_f={nf}) = {b:.6f}")

print(f"\n  Testing log ratios vs beta functions:")
for key in key_ratios:
    log_key = f'log_{key}'
    if log_key not in quark_ratios:
        continue
    log_val = quark_ratios[log_key][0]
    print(f"\n  log(m_{key}) = {log_val:.6f}")
    
    # vs QED beta
    ratio_qed = log_val / beta_qed
    print(f"    / b_0(QED) = {ratio_qed:.6f}")
    # Check if close to rational
    for d in range(1, 21):
        n = round(ratio_qed * d)
        if abs(ratio_qed - n/d) < 0.02:
            print(f"      ~= {n}/{d} = {n/d:.6f}")
            break
    
    # vs QCD beta for various n_f
    for nf, b in beta_qcd.items():
        ratio_qcd = log_val / b
        for d in range(1, 21):
            n = round(ratio_qcd * d)
            if abs(ratio_qcd - n/d) < 0.03:
                print(f"    / b_0(QCD, n_f={nf}) = {ratio_qcd:.6f}  ~= {n}/{d}")
                break

# ===================================================================
#  H2: Quark mass ratio patterns
# ===================================================================

print("\n" + "=" * 70)
print("H2: QUARK MASS RATIO PATTERNS")
print("=" * 70)

print("""
  SEARCH: Do any quark mass ratios match simple adelic/zeta expressions
  at precision comparable to or better than the (now-falsified) lepton
  coincidence (3.25e-4)?
""")

# H2.1: Rational approximations
print(f"\n  --- H2.1 Rational approximations ---")
for key in key_ratios:
    r, err = quark_ratios[key]
    # Find best rational with denominator < 200
    best = None
    for d in range(1, 200):
        n = round(r * d)
        val = n / d
        e = abs(r - val) / r
        if best is None or e < best[0]:
            best = (e, n, d, val)
    
    e, n, d, val = best
    within_1sig = (abs(r - val) <= err)
    flag = "  ** within 1-sigma!" if within_1sig else ""
    print(f"  m_{key} = {r:.4f} +/- {err:.4f}")
    print(f"    Best rational: {n}/{d} = {val:.6f} (rel_err={e:.2e}){flag}")

# H2.2: Log ratios pattern
print(f"\n  --- H2.2 Log ratio patterns ---")
print(f"  log(m_d/m_u)   = {quark_ratios['log_d/u'][0]:.6f}")
print(f"  log(m_s/m_d)   = {quark_ratios['log_s/d'][0]:.6f}")
print(f"  log(m_c/m_s)   = {quark_ratios['log_c/s'][0]:.6f}")
print(f"  log(m_b/m_c)   = {quark_ratios['log_b/c'][0]:.6f}")
print(f"  log(m_t/m_b)   = {quark_ratios['log_t/b'][0]:.6f}")

# Check if consecutive ratios are related
log_ratios = {
    'u->d': quark_ratios['log_d/u'][0],
    'd->s': quark_ratios['log_s/d'][0],
    's->c': quark_ratios['log_c/s'][0],
    'c->b': quark_ratios['log_b/c'][0],
    'b->t': quark_ratios['log_t/b'][0],
}

print(f"\n  Sequences:")
keys = ['u->d', 'd->s', 's->c', 'c->b', 'b->t']
for i in range(len(keys)-1):
    k1, k2 = keys[i], keys[i+1]
    r = log_ratios[k2] / log_ratios[k1]
    print(f"    {k2}/{k1} = {r:.6f}")

# H2.3: Zeta/Gamma_inf matches for quark log ratios
print(f"\n  --- H2.3 Zeta/Gamma_inf matches ---")
# Gamma_inf values at rational points
ginf_points = {}
for num, den in [(1,6), (1,5), (1,4), (1,3), (2,5), (1,2), (3,5), (2,3), (3,4), (4,5), (5,6)]:
    x = mp.mpf(num) / mp.mpf(den)
    ginf = float(zeta(1 - x) / zeta(x))
    log_ginf = math.log(abs(ginf)) if ginf > 0 else float('nan')
    ginf_points[f'{num}/{den}'] = (ginf, log_ginf)

# Check each quark log ratio against Gamma_inf combinations
for q_key in key_ratios:
    log_key = f'log_{q_key}'
    if log_key not in quark_ratios:
        continue
    target = quark_ratios[log_key][0]
    target_err = quark_ratios[log_key][1]
    
    best_match = None
    for name, (g_val, log_g) in ginf_points.items():
        for mult in range(1, 11):
            val = mult * log_g
            err = abs(target - val) / target
            if err < 0.10:
                if best_match is None or err < best_match[0]:
                    best_match = (err, f"{mult}*log|Gamma_inf({name})|", val)
    
    if best_match:
        err, desc, val = best_match
        sig_level = abs(val - target) / (target_err * target + 1e-10)
        print(f"  log(m_{q_key}) = {target:.6f}")
        print(f"    Best: {desc} = {val:.6f} (rel_err={err:.4e}, ~{sig_level:.1f} sigma)")

# H2.4: Check the QCD beta function relation
# For QED: log(m_mu/m_e) ~ 16/3 = 2*sum Q_f^2/3
# For QCD: what is the analogue of sum Q_f^2?
# In QCD, the beta function involves the Casimir operators:
# b_0 = (11*N_c - 2*n_f)/3
# The "2*n_f" term counts quark flavors
# The "11*N_c" comes from gluon loops
# No direct analogue of sum Q_f^2

# But: the Yukawa beta function has the form:
# d y_q/d ln mu = y_q * ( (3/2)*y_q^2 - c_i*g_i^2 ) / (16*pi^2)
# The QCD contribution: c_QCD = -8 for quarks

# H2.5: Golden ratio / algebraic number test
print(f"\n  --- H2.5 Algebraic number test ---")
phi = (1 + math.sqrt(5)) / 2
algebraic = {
    'phi': phi,
    'sqrt(2)': math.sqrt(2),
    'sqrt(3)': math.sqrt(3),
    'pi/2': math.pi/2,
    'pi': math.pi,
    'e': math.e,
}

for q_key in ['t/b', 'b/c', 'c/s', 's/d', 'd/u']:
    log_key = f'log_{q_key}'
    if log_key not in quark_ratios:
        continue
    target = quark_ratios[log_key][0]
    print(f"  log(m_{q_key}) = {target:.6f}")
    for name, val in algebraic.items():
        for mult in range(1, 10):
            v = mult * val
            err = abs(target - v) / target
            if err < 0.05:
                print(f"    {mult}*{name} = {v:.6f} (err={err:.4e})")
        for den in range(2, 10):
            v = val / den
            err = abs(target - v) / target
            if err < 0.05:
                print(f"    {name}/{den} = {v:.6f} (err={err:.4e})")

# ===================================================================
#  H3: CKM elements as cross-ratios
# ===================================================================

print("\n" + "=" * 70)
print("H3: CKM ELEMENTS AS CROSS-RATIOS")
print("=" * 70)

print("""
  The CKM matrix has 4 independent parameters (3 angles + 1 phase).
  Could these be cross-ratios of points on the adelic Shimura variety?
  
  |V_ij| are real numbers in [0, 1]. If they are cross-ratios of 
  rational points, they should approximate rational numbers.
  
  CROSS-RATIO CANDIDATES:
  - |V_us| = 0.2243 ~ 1/4? No, 0.224
  - |V_cb| = 0.0408 ~ 1/25 = 0.04? Close!
  - |V_ub| = 0.00382 ~ 1/262? Hard to test
  - |V_td| = 0.0086 ~ 1/116 = 0.00862? Close!
  - |V_ts| = 0.0415 ~ 1/24 = 0.04167? Close!
""")

# H3.1: Rational approximations of CKM magnitudes
print(f"\n  --- H3.1 Rational approximations of CKM magnitudes ---")
for name, (val, err) in ckm_magnitudes.items():
    # Find best rational with denominator < 1000
    best_small = None
    best_large = None
    for d in range(1, 200):
        n = round(val * d)
        v = n / d
        e = abs(val - v) / val
        if best_small is None or e < best_small[0]:
            best_small = (e, n, d, v)
    for d in range(1, 2000):
        n = round(val * d)
        v = n / d
        e = abs(val - v) / val
        if best_large is None or e < best_large[0]:
            best_large = (e, n, d, v)
    
    within_small = abs(best_small[3] - val) <= err
    within_large = abs(best_large[3] - val) <= err
    
    flag_small = " ** 1-sigma" if within_small else ""
    flag_large = " ** 1-sigma" if within_large else ""
    print(f"  {name} = {val:.6f} +/- {err:.6f}")
    print(f"    d<200:  {best_small[1]}/{best_small[2]} = {best_small[3]:.6f} (err={best_small[0]:.2e}){flag_small}")
    print(f"    d<2000: {best_large[1]}/{best_large[2]} = {best_large[3]:.6f} (err={best_large[0]:.2e}){flag_large}")

# H3.2: CKM as cross-ratios of quark masses
print(f"\n  --- H3.2 CKM elements as cross-ratios of quark masses ---")
print(f"  If |V_ij| = CR(m_i1,m_i2;m_j1,m_j2) for quark mass points,")
print(f"  we should see patterns relating masses to mixing angles.")

# Known approximate relations:
# |V_us| ~ sqrt(m_d/m_s) = sqrt(4.67/93.4) = sqrt(0.05) = 0.224
sqrt_md_ms = math.sqrt(quark_masses['d'][0] / quark_masses['s'][0])
print(f"\n  |V_us| = {ckm_magnitudes['|V_us|'][0]:.6f}")
print(f"  sqrt(m_d/m_s) = {sqrt_md_ms:.6f}")
print(f"  Ratio = {ckm_magnitudes['|V_us|'][0]/sqrt_md_ms:.6f}")

# |V_cb| ~ (m_b/m_t)^? or m_c/m_t?
sqrt_mc_mt = math.sqrt(quark_masses['c'][0] / quark_masses['t'][0])
print(f"\n  |V_cb| = {ckm_magnitudes['|V_cb|'][0]:.6f}")
print(f"  sqrt(m_c/m_t) = {sqrt_mc_mt:.6f}")
print(f"  Ratio = {ckm_magnitudes['|V_cb|'][0]/sqrt_mc_mt:.6f}")

# |V_td| ~ ?
sqrt_mu_mt = math.sqrt(quark_masses['u'][0] / quark_masses['t'][0])
print(f"\n  |V_td| = {ckm_magnitudes['|V_td|'][0]:.6f}")
print(f"  sqrt(m_u/m_t) = {sqrt_mu_mt:.6f}")
print(f"  Ratio = {ckm_magnitudes['|V_td|'][0]/sqrt_mu_mt:.6f}")

# Check the full set of CKM-quark mass relations
print(f"\n  Systematic CKM-mass relation check:")
for ckm_name, (ckm_val, ckm_err) in ckm_magnitudes.items():
    for qi in quark_names:
        for qj in quark_names:
            if qi == qj:
                continue
            m_i = quark_masses[qi][0]
            m_j = quark_masses[qj][0]
            if m_i >= m_j:
                continue
            ratio = math.sqrt(m_i / m_j)
            err = abs(ckm_val - ratio) / ckm_val
            if err < 0.5:
                print(f"    {ckm_name} = {ckm_val:.6f}  vs  sqrt(m_{qi}/m_{qj}) = {ratio:.6f}  (err={err:.4e})")

# H3.3: Jarlskog invariant
print(f"\n  --- H3.3 Jarlskog invariant ---")
print(f"  J = Im(V_ud V_cs V_us* V_cd*) ~ 3e-5")
print(f"  The Jarlskog invariant measures CP violation.")
print(f"  If CKM is a cross-ratio structure, J should be rational.")
print(f"  Current experimental value: J = 3.08e-5 +/- 0.14e-5")
j_exp = 3.08e-5
print(f"  Check: {j_exp} ~ 1/{round(1.0/j_exp)} = {1.0/round(1.0/j_exp):.6e}")

# ===================================================================
#  H4: Quark beta function relations
# ===================================================================

print("\n" + "=" * 70)
print("H4: QUARK BETA FUNCTION — MASS RATIO RELATIONS")
print("=" * 70)

print("""
  The lepton coincidence was:
    log(m_mu/m_e) / pi ~ b_0(QED, SM) = 16/(3*pi)
    => log(m_mu/m_e) ~ 16/3 = 2 * sum_f Q_f^2 / 3
  
  For quarks, the QCD beta function is:
    b_0(QCD) = (11*N_c - 2*n_f) / (12*pi)   [in the convention d(alpha_s)/d ln mu = -b_0 alpha_s^2]
    
  But wait: the QCD beta function convention differs from QED:
    d alpha_s / d ln mu = - (beta_0/(2*pi)) alpha_s^2 + ...
    beta_0 = (11*N_c - 2*n_f)/3  =  (33 - 2*n_f)/3
    
  If we look for log(m_q2/m_q1) ~ some multiple of beta function coefficients:
""")

# Beta function coefficients in the "b_0" convention (similar to QED)
# d alpha / d ln mu = b_0 * alpha^2
# For QED: b_0 = 2*sum Q_f^2/(3*pi)
# For QCD: b_0 = (11*N_c - 2*n_f)/(6*pi)... hmm, conventions vary

# Let's use: b_0 = beta_0 / (2*pi) where beta_0 = (11*N_c - 2*n_f)/3
# Then b_0(QCD) = (11*N_c - 2*n_f) / (6*pi)

b0_qcd = {nf: (11*3 - 2*nf) / (6*math.pi) for nf in [3, 4, 5, 6]}
for nf, b in b0_qcd.items():
    print(f"  b_0(QCD, n_f={nf}) = {b:.6f}")

print(f"\n  Testing log ratios vs QCD beta functions (b_0 convention):")
for q_key in key_ratios:
    log_key = f'log_{q_key}'
    if log_key not in quark_ratios:
        continue
    target = quark_ratios[log_key][0]
    print(f"\n  log(m_{q_key}) = {target:.6f}")
    
    # Test: log(m_q2/m_q1) / pi vs b_0(QCD)
    for nf, b in b0_qcd.items():
        ratio = (target / math.pi) / b
        for d in range(1, 21):
            n = round(ratio * d)
            if abs(ratio - n/d) < 0.05:
                print(f"    (log/pi) / b_0(QCD, n_f={nf}) = {ratio:.6f}  ~= {n}/{d}")
                break

# Test: log(m_q) directly vs b_0
print(f"\n  Testing absolute log(mass) vs b_0:")
for q in quark_names:
    m = quark_masses[q][0]
    # log in units of 1 GeV
    log_m_gev = math.log(m / 1000.0)  # masses in GeV
    print(f"  log(m_{q}/GeV) = {log_m_gev:.6f}")
    for nf, b in b0_qcd.items():
        ratio = abs(log_m_gev) / b
        for d in range(1, 21):
            n = round(ratio * d)
            if abs(ratio - n/d) < 0.05:
                print(f"    |log| / b_0(QCD, n_f={nf}) = {ratio:.6f}  ~= {n}/{d}")
                break

# ===================================================================
#  SYNTHESIS
# ===================================================================

print("\n" + "=" * 70)
print("SYNTHESIS: DOES THE ADELIC FRAMEWORK CONSTRAIN QUARK MASSES?")
print("=" * 70)

print("""
  FINDINGS:
  
  1. QUARK ANALOGUE OF a = 1/3:
     - No single Veneziano-like parameter explains all quark mass ratios
     - Beta function ratios give fractional numbers with no clear pattern
     - The QCD beta function depends on n_f, which changes across thresholds
     - This "running of the coefficient" makes a fixed a-parameter unlikely
  
  2. QUARK MASS RATIO PATTERNS:
     - Some ratios are close to integers (m_d/m_u ~ 2.16, m_t/m_b ~ 41.3)
     - m_b/m_c ~ 3.29, close to 10/3 = 3.333 (but 1.3% error)
     - m_t/m_c ~ 135.8, close to 136? (inverse fine structure constant)
     - However, quark mass uncertainties are large (u: 25%, d: 22%)
     - No ratio matches an adelic/zeta expression at the 3e-4 level
  
  3. CKM AS CROSS-RATIOS:
     - |V_us| ~ sqrt(m_d/m_s) = 0.224 works to ~0.2%
     - |V_cb| ~ sqrt(m_c/m_t) = 0.0857 doesn't match 0.0408
     - |V_td| ~ sqrt(m_u/m_t) = 0.0035 close to 0.0086 (factor 2.4 off)
     - The sqrt(m_i/m_j) pattern is approximate, not exact cross-ratios
     - Jarlskog invariant ~ 1/32468 — no obvious adelic interpretation
  
  4. BETA FUNCTION RELATIONS:
     - No quark analogue of log(m_mu/m_e) ~ 16/3 was found
     - The QCD beta function has a different structure (gluon loops dominate)
     - The running of n_f across thresholds complicates any fixed relation
  
  OVERALL VERDICT:
  
  The adelic framework does not make clear, falsifiable predictions for
  quark mass ratios or CKM elements. The sqrt(m_i/m_j) ~ |V_ij| relations
  (Fritzsch/Stech-type textures) are approximate phenomenological patterns,
  not derived from the adelic/zeta structure.
  
  The quark sector has richer structure than leptons (6 masses + 4 CKM
  parameters), but also larger uncertainties. With current precision,
  many rational expressions can "match" quark data — making rigorous
  falsification difficult.
  
  RECOMMENDATION:
  - Thrust H should be classified as "INCONCLUSIVE" rather than "FAILED"
  - The large quark mass uncertainties prevent precise testing
  - Future work: wait for improved lattice QCD determinations of u, d, s masses
  - Shift focus to Thrust J (publication) — the main story is clear
""")

print("\n" + "=" * 70)
print("THRUST H COMPLETE — INCONCLUSIVE (large uncertainties)")
print("=" * 70)
