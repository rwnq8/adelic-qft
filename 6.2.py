#!/usr/bin/env python3
"""
Thrust F: Derivation of log(m_mu/m_e) = 16/3 from the Adelic Structure
File: 6.2.py (Phase 3, Thrust F)
Associated report: 6.2.md

OBJECTIVE: Derive or falsify the coincidence:
    log(m_mu/m_e) / pi ~ 16/(3*pi) = b_0^QED(SM)

TASKS:
  F1: Map Veneziano parameter a to energy scale
  F2: Compute Yukawa couplings from worldsheet instantons (analytic)
  F3: Express log(m_mu/m_e) in terms of a
  F4: Compute b_0^QED from the zeta structure
  F5: Connect the two: log(m_mu/m_e) = pi * b_0

KEY IDENTITIES (from Phase 2):
  Gamma_inf(x) = zeta(1-x)/zeta(x)                     [5.6.py]
  A_inf(a,b)  = Gamma_inf(a)*Gamma_inf(b)/Gamma_inf(a+b)
  At a=b=1/3:  A_inf(1/3,1/3) = Gamma_inf(1/3)^3       [symmetric point]
  The adelic product = 1 is the zeta functional equation
"""

import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mpmath import mp, gamma, zeta, psi, pi as mppi, agm
mp.dps = 100

# ===================================================================
#  EXPERIMENTAL DATA
# ===================================================================

# PDG 2024 masses (MeV)
m_e  = 0.51099895000    # electron mass
m_mu = 105.6583745      # muon mass
m_tau = 1776.86         # tau mass (PDG 2024)

mass_ratios = {
    'mu/e':   m_mu / m_e,
    'tau/e':  m_tau / m_e,
    'tau/mu': m_tau / m_mu,
}

log_mass_ratios = {k: math.log(v) for k, v in mass_ratios.items()}

# b_0(QED) in the SM with 3 generations
# Sum_f Q_f^2 = 3 (leptons) + N_c*sum_q Q_q^2 (quarks)
# = 3 + 3*(3*(2/3)^2 + 3*(1/3)^2) = 3 + 3*(4/3 + 1/3) = 3 + 5 = 8
# But careful: 6 quarks * N_c = 18 quark d.o.f.:
#   up-type (u,c,t): 3*3*(4/9) = 4
#   down-type (d,s,b): 3*3*(1/9) = 1
# Total: 3 + 4 + 1 = 8
b0_qed_sm = 2.0 * 8.0 / (3.0 * math.pi)  # = 16/(3*pi)

print("=" * 70)
print("THRUST F: DERIVATION OF log(m_mu/m_e) = 16/3")
print("=" * 70)

print(f"\n--- Experimental Mass Ratios (PDG 2024) ---")
for k, v in mass_ratios.items():
    print(f"  m_{k} = {v:.10f}")

print(f"\n--- Logarithms ---")
for k, v in log_mass_ratios.items():
    print(f"  log(m_{k}) = {v:.10f}")

print(f"\n--- The Coincidence ---")
print(f"  log(m_mu/m_e) = {log_mass_ratios['mu/e']:.10f}")
print(f"  16/3           = {16.0/3.0:.10f}")
print(f"  Difference     = {abs(log_mass_ratios['mu/e'] - 16.0/3.0):.6e}")
print(f"  Relative error = {abs(log_mass_ratios['mu/e'] - 16.0/3.0)/(16.0/3.0):.4e}")
print(f"")
print(f"  b_0(QED) = 16/(3*pi) = {b0_qed_sm:.10f}")
print(f"  log(m_mu/m_e)/pi    = {log_mass_ratios['mu/e']/math.pi:.10f}")
print(f"  Relative error      = {abs(log_mass_ratios['mu/e']/math.pi - b0_qed_sm)/b0_qed_sm:.4e}")

# ===================================================================
#  TASK F1: Map Veneziano parameter a to energy scale
# ===================================================================

print("\n" + "=" * 70)
print("F1: VENEZIANO PARAMETER a AND ENERGY SCALE")
print("=" * 70)

print("""
  The Freund-Witten adelic Veneziano amplitude is:
    A_inf(a,b) = Gamma_inf(a) * Gamma_inf(b) / Gamma_inf(a+b)
  where Gamma_inf(x) = zeta(1-x)/zeta(x).

  The Veneziano parameter a controls the Regge trajectory:
    alpha(s) = alpha' * s + alpha_0
  where alpha(s) = a gives s = (a - alpha_0)/alpha'.

  KEY QUESTION: What is the SYMMETRIC POINT?
  - In the Veneziano amplitude, A(a,b) is symmetric in a,b.
  - The triple-Regge region has a+b+c=1 (from s+t+u constraint).
  - The symmetric point is a = b = c = 1/3.
  - At this point: A_inf(1/3, 1/3) = Gamma_inf(1/3)^3
""")

# Compute Gamma_inf at key points
print("\n--- Gamma_inf(x) at Key Rational Points ---")
print(f"  {'x':>12}  {'Gamma_inf(x)':>20}  {'zeta(1-x)/zeta(x)':>20}  {'Match?':>8}")
print("  " + "-" * 70)

key_points = [
    mp.mpf(1)/mp.mpf(6),
    mp.mpf(1)/mp.mpf(4),
    mp.mpf(1)/mp.mpf(3),
    mp.mpf(1)/mp.mpf(2),
    mp.mpf(2)/mp.mpf(3),
    mp.mpf(3)/mp.mpf(4),
    mp.mpf(5)/mp.mpf(6),
]

for x in key_points:
    # Direct computation
    g_dir = float(2 * mp.cos(mp.pi*x/2) * gamma(x) / (2*mppi)**x)
    # Zeta representation
    g_zeta = float(zeta(1 - x) / zeta(x))
    match = "YES" if abs(g_dir - g_zeta) < 1e-90 else "NO"
    print(f"  {float(x):>12.8f}  {g_dir:>20.15f}  {g_zeta:>20.15f}  {match:>8}")

# Special: Gamma_inf(1/3)
x13 = mp.mpf('1/3')
g13 = float(zeta(1 - x13) / zeta(x13))
g13_cubed = g13 ** 3

print(f"\n--- The Symmetric Point a = 1/3 ---")
print(f"  Gamma_inf(1/3)   = {g13:.15f}")
print(f"  Gamma_inf(1/3)^3 = {g13_cubed:.15f}")
print(f"  This is A_inf(1/3, 1/3) at the symmetric point.")

# Express Gamma_inf(1/3)^3 in terms of Gamma(1/3)
# Using zeta functional equation:
# zeta(2/3) = 2^{2/3} * pi^{-1/3} * sin(pi/3) * Gamma(1/3) * zeta(1/3)
# Gamma_inf(1/3) = zeta(2/3)/zeta(1/3)
# = 2^{2/3} * pi^{-1/3} * sin(pi/3) * Gamma(1/3)
# = 2^{2/3} * pi^{-1/3} * (sqrt(3)/2) * Gamma(1/3)
# = 2^{-1/3} * pi^{-1/3} * sqrt(3) * Gamma(1/3)

g13_from_gamma = float(2**(-1/3) * mppi**(-1/3) * mp.sqrt(3) * gamma(mp.mpf('1/3')))
print("\n  Analytic form: Gamma_inf(1/3) = 2^{-1/3} * pi^{-1/3} * sqrt(3) * Gamma(1/3)")
print(f"  Numeric check:  {g13_from_gamma:.15f}")
print(f"  Match: {abs(g13 - g13_from_gamma) < 1e-15}")

# Gamma_inf(1/3)^3 = 2^{-1} * pi^{-1} * 3*sqrt(3) * Gamma(1/3)^3
g13_cubed_analytic = float(0.5 * mppi**(-1) * 3 * mp.sqrt(3) * gamma(mp.mpf('1/3'))**3)
print(f"\n  Analytic: Gamma_inf(1/3)^3 = (3*sqrt(3))/(2*pi) * Gamma(1/3)^3")
print(f"  Numeric check: {g13_cubed_analytic:.15f}")
print(f"  Match: {abs(g13_cubed - g13_cubed_analytic) < 1e-15}")

# ===================================================================
#  TASK F4: Compute b_0 from the zeta structure
# ===================================================================

print("\n" + "=" * 70)
print("F4: b_0(QED) FROM THE ZETA STRUCTURE")
print("=" * 70)

print(f"""
  QED beta function at one loop:
    d(alpha)/d(ln mu) = b_0 * alpha^2
    b_0 = (2/(3*pi)) * sum_f Q_f^2

  In the SM with 3 generations:
    sum_f Q_f^2 = 8
    b_0 = 16/(3*pi) = {b0_qed_sm:.10f}

  KEY QUESTION: Where does 16/3 come from in the zeta/adeles?

  APPROACH 1: Zero-statistics integral (Module B)
    From 5.7.py: integral_0^inf (1 - R_2(x)) dx = 1/2
    where R_2(x) is the 2-point level spacing distribution.
    This 1/2 is "universal" from zeta zero statistics.
    
    If b_0 = K * (1/2), then K = 2*b_0 = 32/(3*pi).
    This doesn't give a clean number.

  APPROACH 2: Zeta values at special arguments
    zeta(0)  = -1/2
    zeta(-1) = -1/12
    zeta(2)  = pi^2/6
    zeta(3)  ~ 1.202... (Apery's constant)

    None directly give 16/3.

  APPROACH 3: The number 16/3 as an adelic invariant
    16/3 can appear as:
    - A ratio of zeta values
    - A value of the logarithmic derivative (beta function)
    - A combination of Euler Gamma values at rational points
""")

# Search for combinations that give 16/3
print("--- Search for Combinations Giving 16/3 ---")

target = 16.0 / 3.0

# Approach 3a: log of Gamma_inf values
print(f"\n  Approach 3a: log(Gamma_inf) values")
for x in [mp.mpf(1)/mp.mpf(3), mp.mpf(1)/mp.mpf(2), mp.mpf(2)/mp.mpf(3)]:
    g_val = float(zeta(1-x) / zeta(x))
    log_g = math.log(abs(g_val)) if g_val != 0 else float('-inf')
    print(f"    log|Gamma_inf({float(x):.4f})| = {log_g:.10f}")

# Approach 3b: Beta function (logarithmic derivative)
print(f"\n  Approach 3b: Beta_inf(x) = d/dx log|Gamma_inf(x)|")
print(f"  Beta_inf(x) = -zeta'(1-x)/zeta(1-x) - zeta'(x)/zeta(x)")
print(f"  Evaluating at key points:")

def beta_inf_closed(x):
    """Closed form for beta_inf using known functional equation.
    
    beta_inf(x) = d/dx log|Gamma_inf(x)|
    = d/dx log|zeta(1-x)/zeta(x)|
    = d/dx [log|zeta(1-x)| - log|zeta(x)|]
    = -zeta'(1-x)/zeta(1-x) - zeta'(x)/zeta(x)
    
    But we can also use:
    Gamma_inf(x) = 2 cos(pi*x/2) * Gamma(x) / (2*pi)^x
    log Gamma_inf(x) = log 2 + log|cos(pi*x/2)| + log Gamma(x) - x*log(2*pi)
    d/dx = -(pi/2)*tan(pi*x/2) + psi(0,x) - log(2*pi)
    """
    return float(-(mppi/2) * mp.tan(mppi*x/2) + psi(0, x) - mp.log(2*mppi))

for x_val in [mp.mpf('1/6'), mp.mpf('1/4'), mp.mpf('1/3'), mp.mpf('1/2')]:
    b_val = beta_inf_closed(x_val)
    print(f"    beta_inf({float(x_val):.4f}) = {b_val:.10f}")

# Check: beta_inf(1/3) = ?
b13 = beta_inf_closed(mp.mpf('1/3'))
print(f"\n  beta_inf(1/3) = {b13:.10f}")
print(f"  16/3         = {target:.10f}")
print(f"  Difference   = {abs(b13 - target):.6f}")

# Approach 3c: Derivatives of the completed zeta
print("\n  Approach 3c: Completed zeta Lambda(s) = pi^{-s/2} * Gamma(s/2) * zeta(s)")
print("  Lambda(s) = Lambda(1-s) [functional equation]")
print("  At s = 1/2: Lambda'(1/2) = 0 [from symmetry]")
print("  At s = 1/3: Lambda(1/3) and Lambda(2/3) are related")

# Compute Lambda at rational points
def Lambda_s(s):
    """Completed zeta function"""
    return float(mppi**(-s/2) * gamma(s/2) * zeta(s))

for s_val in [mp.mpf('1/3'), mp.mpf('1/2'), mp.mpf('2/3')]:
    L = Lambda_s(s_val)
    print(f"    Lambda({float(s_val):.4f}) = {L:.15f}")

# ===================================================================
#  TASK F3/F5: Express log(m_mu/m_e) in terms of a
# ===================================================================

print("\n" + "=" * 70)
print("F3/F5: CONNECTING log(m_mu/m_e) TO THE ADELIC STRUCTURE")
print("=" * 70)

print("""
  THE DERIVATION CHAIN (from 6.0.md):
    1. Veneziano pole cross-ratios (rational)
    2. M13 compactification dictionary (Kaehler modulus a)
    3. Calabi-Yau cycle volumes
    4. Gauge kinetic functions f_a ~ Vol(Sigma_a)
    5. Yukawa couplings y_f (from worldsheet instantons)
    6. Lepton masses m_f = y_f * v / sqrt(2)
  
  CRITICAL STEP: Step 2 is where a = 1/3 enters.
  The Kaehler modulus T = B + i*Vol determines the gauge coupling:
    f_a = k_a * T / (2*pi)
  where k_a is the Kac-Moody level.
  
  For the standard embedding (E8 x E8 heterotic):
    k_a = 1 for the observable E6
    g^{-2} = Re(T) at tree level
  
  The Veneziano parameter a is identified with the Kaehler modulus
  through the Freund-Witten compactification dictionary.
""")

# Compute what a = 1/3 implies for the gauge coupling
print("\n--- Consequences of a = 1/3 ---")
print(f"  If Kaehler modulus T ~ a = 1/3:")
print(f"    g^2 ~ 1/Re(T) = 3")
print(f"    alpha = g^2/(4*pi) = {3.0/(4*math.pi):.6f}")
print(f"  Compare: alpha(m_Z) ~ 1/128 = {1.0/128:.6f}")

# The key question: what fixes a = 1/3?
print(f"""
  KEY INSIGHT: The value a = 1/3 is not arbitrary.
  
  At a = 1/3, the Veneziano amplitude factorizes:
    A_inf(1/3, 1/3) = Gamma_inf(1/3)^3
  
  This is the symmetric point of the s-t-u crossing.
  The full amplitude A(s,t) + A(t,u) + A(u,s) at this point
  is 3 * Gamma_inf(1/3)^3.
  
  The factor 3 comes from the three channels.
  
  Question: Does this factor 3 relate to the 3 generations?
  
  If we identify:
    Gamma_inf(1/3)^3 = exp(16/3) * [some scale factor]
  
  Then log Gamma_inf(1/3)^3 = 3 * log Gamma_inf(1/3)
  
  Let me compute: log Gamma_inf(1/3)^3 = {math.log(g13_cubed):.10f}
  Compare: 16/3 = {target:.10f}
  Difference: {abs(math.log(g13_cubed) - target):.6f}
""")

log_g13_cubed = math.log(g13_cubed)
print(f"  log(Gamma_inf(1/3)^3) = {log_g13_cubed:.15f}")
print(f"  16/3                   = {target:.15f}")
print(f"  Ratio                  = {log_g13_cubed / target:.10f}")

# ===================================================================
#  DERIVATION ATTEMPT 1: Direct zeta product
# ===================================================================

print("\n" + "=" * 70)
print("DERIVATION ATTEMPT 1: Zeta Product at Symmetric Point")
print("=" * 70)

print("""
  Starting point: Gamma_inf(1/3) = zeta(2/3)/zeta(1/3)
  
  Using the zeta functional equation:
    zeta(s) = 2^s * pi^{s-1} * sin(pi*s/2) * Gamma(1-s) * zeta(1-s)
  
  At s = 2/3:
    zeta(2/3) = 2^{2/3} * pi^{-1/3} * sin(pi/3) * Gamma(1/3) * zeta(1/3)
  
  So:
    Gamma_inf(1/3) = 2^{2/3} * pi^{-1/3} * sin(pi/3) * Gamma(1/3)
  
  sin(pi/3) = sqrt(3)/2, so:
    Gamma_inf(1/3) = 2^{-1/3} * pi^{-1/3} * sqrt(3) * Gamma(1/3)
  
  Gamma_inf(1/3)^3 = (1/2) * pi^{-1} * 3*sqrt(3) * Gamma(1/3)^3
  
  Now, Gamma(1/3) is a transcendental number.
  log Gamma(1/3) = ? No simple closed form.
  
  RESULT: Gamma_inf(1/3)^3 does NOT simplify to exp(16/3).
  The value is:
""")

print(f"  Gamma_inf(1/3)^3 = {g13_cubed:.15f}")
print(f"  exp(16/3)         = {math.exp(16.0/3.0):.15f}")
print(f"  Ratio = {g13_cubed / math.exp(16.0/3.0):.10f}")
print(f"  VERDICT: Gamma_inf(1/3)^3 != exp(16/3)")

# ===================================================================
#  DERIVATION ATTEMPT 2: The factor 3 and the Veneziano symmetry
# ===================================================================

print("\n" + "=" * 70)
print("DERIVATION ATTEMPT 2: Veneziano Triple-Channel Structure")
print("=" * 70)

print("""
  The full Veneziano amplitude has three channels:
    A_full(s,t,u) = A(s,t) + A(t,u) + A(u,s)
  
  At the symmetric point s = t = u, a = b = c = 1/3:
    A_full = 3 * Gamma_inf(1/3)^2 / Gamma_inf(2/3)
           = 3 * Gamma_inf(1/3)^3          (since Gamma_inf(2/3) = 1/Gamma_inf(1/3))
  
  So: A_full(1/3, 1/3, 1/3) = 3 * Gamma_inf(1/3)^3
  
  The factor 3 counts the three channels.
  The factor 1/3 in the argument comes from s+t+u symmetry.
  
  Key question: Is there a factor of 3 from the number of lepton generations?
  The SM has 3 generations: e, mu, tau.
  The QED beta function sums over all 3: sum Q_f^2 includes all 3.
  
  But 3 * Gamma_inf(1/3)^3 still does not equal exp(16/3).
""")

a_full_3chan = 3.0 * g13_cubed
print(f"  3 * Gamma_inf(1/3)^3 = {a_full_3chan:.15f}")
print(f"  exp(16/3)             = {math.exp(16.0/3.0):.15f}")
print(f"  Ratio = {a_full_3chan / math.exp(16.0/3.0):.10f}")

# ===================================================================
#  DERIVATION ATTEMPT 3: The b_0 coefficient from adelic RG
# ===================================================================

print("\n" + "=" * 70)
print("DERIVATION ATTEMPT 3: b_0 from Adelic Renormalization Group")
print("=" * 70)

print("""
  From Phase 2 (5.8.py): The adelic RG flow has boundedness.
  The Landau pole is cancelled by p-adic compensation.
  
  The beta function beta_inf(x) = d/dx log Gamma_inf(x) is:
    beta_inf(x) = -(pi/2)*tan(pi*x/2) + psi(0,x) - log(2*pi)
  
  This is the "beta" of the Veneziano amplitude structure, not QED.
  But perhaps there is a relationship.
  
  At x = 1/3:
""")

b_inf_13 = beta_inf_closed(mp.mpf('1/3'))
print(f"  beta_inf(1/3) = {b_inf_13:.10f}")
print(f"  The QED beta coefficient is 16/(3*pi) = {b0_qed_sm:.10f}")
print(f"  These are DIFFERENT quantities (different dimensions).")
print(f"  beta_inf is dimensionless; b_0 has dimensions of 1/energy^2...")
print(f"  Actually b_0 is dimensionless (d alpha / d ln mu has same dimension as alpha).")
print(f"  But beta_inf is the log derivative of Gamma_inf, not related to gauge coupling.")

# Check: does beta_inf at some special point equal something?
print(f"\n  Searching for b_0-related values in beta_inf:")
# beta_inf(x) = -pi/2 * tan(pi*x/2) + psi(0,x) - log(2*pi)
# At x -> 0: beta_inf ~ -1/x - gamma - log(2*pi) (diverges)
# At x = 1/2: tan(pi/4) = 1
b_inf_12 = beta_inf_closed(mp.mpf('1/2'))
print(f"  beta_inf(1/2) = {b_inf_12:.10f}")
# At x = 1:
b_inf_1 = beta_inf_closed(mp.mpf('1'))
print(f"  beta_inf(1)   = {b_inf_1:.10f}")

# ===================================================================
#  DERIVATION ATTEMPT 4: The number 8 = sum Q_f^2 from zeta
# ===================================================================

print("\n" + "=" * 70)
print("DERIVATION ATTEMPT 4: sum Q_f^2 FROM ZETA STRUCTURE")
print("=" * 70)

print("""
  The number 16/3 in b_0 comes from sum_f Q_f^2 = 8.
  b_0 = (2/(3*pi)) * 8 = 16/(3*pi).
  
  Can sum_f Q_f^2 = 8 be derived from the zeta/adeles?
  
  The SM fermion charges squared:
    Leptons:  3 * (1)^2  = 3  (e, mu, tau)
    Up-type:  3 * 3 * (2/3)^2 = 3 * 3 * 4/9 = 4  (u,c,t; Nc=3)
    Down-type: 3 * 3 * (1/3)^2 = 3 * 3 * 1/9 = 1  (d,s,b; Nc=3)
    Total = 8
  
  The number 8 appears elsewhere:
    - zeta(0) * (-16) = (-1/2) * (-16) = 8
    - zeta(2) * 48/pi^2 = (pi^2/6) * 48/pi^2 = 8
    - 2^3 = 8 (three generations, each with 2 isospin states?)
  
  But none of these are compelling derivations from the adelic structure.
  
  The sum of squares of charges = 8 is a consequence of anomaly cancellation:
    [SU(3)]^2 U(1):  sum_{quarks} Q_q = 3*(2/3 + 2/3 + 2/3 - 1/3 - 1/3 - 1/3) = 0
    [SU(2)]^2 U(1):  sum_{doublets} Q = -1/2 ... etc.
    
  Anomaly cancellation is a consistency condition, not derivable from zeta.
""")

# ===================================================================
#  DERIVATION ATTEMPT 5: log(m_mu/m_e) from Yukawa RG evolution
# ===================================================================

print("\n" + "=" * 70)
print("DERIVATION ATTEMPT 5: log(m_mu/m_e) FROM RG EVOLUTION")
print("=" * 70)

print("""
  The Yukawa coupling y_f runs with energy:
    dy_f / d ln mu = beta_y(y_f, g_i)
  
  At one loop (SM):
    beta_{y_e}  ~ y_e * (3*y_e^2/32/pi^2 + ... gauge terms)
    beta_{y_mu} ~ y_mu * (3*y_mu^2/32/pi^2 + ... gauge terms)
  
  Since y_e << y_mu, the dominant difference comes from the gauge terms.
  
  The gauge contribution to the Yukawa beta function:
    Delta beta_y / y = -9/4 * g^2/16*pi^2 - 9/4 * g'^2/16*pi^2 + ...
  
  The ratio log(m_mu/m_e) = log(y_mu/y_e) could arise from integrating
  the beta function between two scales.
  
  If the running is dominated by QED (g = e):
    d/d(ln mu) log y ~ - (9/4) * (e^2/16*pi^2)
                      = - (9/64*pi^2) * e^2
                      = - (9/16*pi) * alpha
  
  Integrating from M_GUT to m_mu gives log(y_mu/y_e).
  
  BUT: this is standard SM RG evolution, not adelic structure!
  
  The question is whether the adelic structure FIXES the boundary
  condition at the GUT/string scale such that log(m_mu/m_e) = 16/3.
""")

# ===================================================================
#  DERIVATION ATTEMPT 6: M13 Compactification Dictionary
# ===================================================================

print("\n" + "=" * 70)
print("DERIVATION ATTEMPT 6: M13 COMPACTIFICATION DICTIONARY")
print("=" * 70)

print("""
  The M13 compactification dictionary (Phase 1, Modules 07-11) maps:
  
    Veneziano parameter a  <-->  Kaehler modulus T of Calabi-Yau
    Veneziano pole CRs     <-->  CY intersection numbers
    Adelic product = 1     <-->  Zeta functional equation
  
  For the heterotic string on a CY threefold:
    - Gauge kinetic function: f_a = S (dilaton) for standard embedding
    - For non-standard embedding: f_a = k_a * T + ...
    - Yukawa couplings: y_ijk ~ exp(-A_ijk) from worldsheet instantons
  
  The worldsheet instanton action:
    A_ijk = 2*pi * T * q_ijk
  where q_ijk are the instanton numbers (integers).
  
  For the lepton Yukawa couplings:
    y_e  ~ exp(-2*pi * T * q_e)
    y_mu ~ exp(-2*pi * T * q_mu)
    y_tau ~ exp(-2*pi * T * q_tau)
  
  Then: log(m_mu/m_e) = log(y_mu/y_e) = 2*pi * T * (q_e - q_mu)
  
  If T = a = 1/3 and q_e - q_mu = 8/pi^2 ...?
  Actually: log(m_mu/m_e) = 16/3 implies:
    2*pi * (1/3) * Delta_q = 16/3
    => Delta_q = 8/pi
  
  This is not an integer, so the worldsheet instanton interpretation
  fails unless T is not exactly 1/3 or the identification is different.
""")

delta_q = (16.0/3.0) / (2.0 * math.pi * (1.0/3.0))
print(f"  If T = 1/3: Delta_q = {delta_q:.10f} (should be integer for instantons)")
print(f"  VERDICT: Delta_q = 8/pi is NOT an integer.")

# Alternative: T might not be 1/3
T_from_log = log_mass_ratios['mu/e'] / (2.0 * math.pi)
print(f"\n  If Delta_q = 1 (simplest instanton): T = {T_from_log:.10f}")
print(f"  If Delta_q = 2: T = {T_from_log/2:.10f}")
print(f"  If Delta_q = 3: T = {T_from_log/3:.10f}")

# ===================================================================
#  DERIVATION ATTEMPT 7: Cross-ratios of Rational Points
# ===================================================================

print("\n" + "=" * 70)
print("DERIVATION ATTEMPT 7: CROSS-RATIOS OF VENEZIANO POLES")
print("=" * 70)

print("""
  From 5.4.py: Veneziano pole cross-ratios are rational numbers.
  CR(n1,n2;n3,n4) = (n1-n3)(n2-n4)/((n1-n4)(n2-n3))
  
  For n1=0, n2=3, n3=8, n4=infinity:
    CR ~ (0-8)(3-inf)/((0-inf)(3-8)) ~ 8/5... not 16/3.
  
  Cross-ratios are typically rational numbers with small denominators.
  16/3 has denominator 3, which could appear.
  
  Let me search for cross-ratios that give 16/3.
""")

from fractions import Fraction

print("\n  Searching for Veneziano pole CRs that give 16/3:")
found = []
for n1 in range(0, 15):
    for n2 in range(n1+1, 15):
        for n3 in range(n2+1, 15):
            for n4 in range(n3+1, 15):
                num = (n1 - n3) * (n2 - n4)
                den = (n1 - n4) * (n2 - n3)
                if den == 0:
                    continue
                cr = Fraction(num, den)
                if cr.numerator == 16 and cr.denominator == 3:
                    found.append((n1, n2, n3, n4))
                # Also check reciprocal
                if cr.numerator == 3 and cr.denominator == 16:
                    found.append((n1, n2, n3, n4))

if found:
    for n1, n2, n3, n4 in found[:10]:
        num = (n1-n3)*(n2-n4)
        den = (n1-n4)*(n2-n3)
        cr = Fraction(num, den)
        print(f"    CR({n1},{n2};{n3},{n4}) = {cr}")
else:
    print("    No Veneziano pole CR equals 16/3 for n_i in [0, 14]")
    
# Broader search: what CRs are close to 16/3?
print(f"\n  Veneziano pole CRs closest to 16/3 ({target:.6f}):")
close_crs = []
for n1 in range(0, 20):
    for n2 in range(n1+1, 20):
        for n3 in range(n2+1, 20):
            for n4 in range(n3+1, 20):
                num = (n1 - n3) * (n2 - n4)
                den = (n1 - n4) * (n2 - n3)
                if den == 0:
                    continue
                cr = float(Fraction(num, den))
                diff = abs(cr - target)
                if diff < 0.5:
                    close_crs.append((diff, n1, n2, n3, n4, Fraction(num, den)))

close_crs.sort()
for diff, n1, n2, n3, n4, cr in close_crs[:10]:
    print(f"    CR({n1},{n2};{n3},{n4}) = {float(cr):.6f} (diff={diff:.4f})")

# ===================================================================
#  DERIVATION ATTEMPT 8: log(m_mu/m_e) as zeta derivative ratio
# ===================================================================

print("\n" + "=" * 70)
print("DERIVATION ATTEMPT 8: log RATIO AS ZETA DERIVATIVE")
print("=" * 70)

print("""
  From the completed zeta Lambda(s) = pi^{-s/2} * Gamma(s/2) * zeta(s):
  Lambda(s) = Lambda(1-s)
  
  Taking log derivative:
    Lambda'/Lambda (s) = -Lambda'/Lambda (1-s)
  
  At s = 1/3:
    Lambda'/Lambda (1/3) = -Lambda'/Lambda (2/3)
  
  The values Lambda'/Lambda at rational points involve:
    - (1/2)*log(pi)
    - (1/2)*psi(s/2)
    - zeta'(s)/zeta(s)
  
  Could log(m_mu/m_e) = zeta'(1/3)/zeta(1/3) - zeta'(2/3)/zeta(2/3)?
  That would be = -d/ds log(Gamma_inf(1/3)) = ...
  
  Actually: Gamma_inf(1/3) = zeta(2/3)/zeta(1/3)
  log Gamma_inf(1/3) = log|zeta(2/3)| - log|zeta(1/3)|
  
  But log Gamma_inf(1/3)^3 = 3 * (log|zeta(2/3)| - log|zeta(1/3)|)
  
  This is:
""")

log_zeta_23 = float(mp.log(abs(zeta(mp.mpf('2/3')))))
log_zeta_13 = float(mp.log(abs(zeta(mp.mpf('1/3')))))
log_diff = 3.0 * (log_zeta_23 - log_zeta_13)

print(f"  3 * (log|zeta(2/3)| - log|zeta(1/3)|) = {log_diff:.15f}")
print(f"  log Gamma_inf(1/3)^3                 = {log_g13_cubed:.15f}")
print(f"  16/3                                  = {target:.15f}")
print(f"  NOT equal to 16/3.")

# ===================================================================
#  DERIVATION ATTEMPT 9: p-adic contributions
# ===================================================================

print("\n" + "=" * 70)
print("DERIVATION ATTEMPT 9: p-ADIC CONTRIBUTIONS")
print("=" * 70)

print("""
  The adelic product formula:
    Gamma_inf(x) * prod_p Gamma_p(x) = 1
  
  where Gamma_p(x) = (1 - p^{-x})/(1 - p^{-(1-x)}) (Euler factor form).
  
  At x = 1/3:
    Gamma_p(1/3) = (1 - p^{-1/3})/(1 - p^{-2/3})
  
  The product over p of Gamma_p(1/3) = 1/Gamma_inf(1/3).
  
  Could the product over primes give a factor related to 16/3?
  
  Let me check: prod_p Gamma_p(1/3) = ?
""")

# Compute adelic product at x=1/3
max_prime = 10000
prod_p13 = mp.mpf(1.0)
for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
    gp = (1.0 - p**(-1.0/3.0)) / (1.0 - p**(-2.0/3.0))
    prod_p13 *= gp

print(f"  prod_p Gamma_p(1/3) for primes <= 37 = {float(prod_p13):.10f}")
print(f"  1/Gamma_inf(1/3)                     = {1.0/g13:.10f}")

# ===================================================================
#  DERIVATION ATTEMPT 10: The "16" from the SM field content
# ===================================================================

print("\n" + "=" * 70)
print("DERIVATION ATTEMPT 10: THE NUMBER 16 FROM SM FIELD CONTENT")
print("=" * 70)

print("""
  b_0(QED) = 16/(3*pi) comes from sum_f Q_f^2 = 8.
  
  In the SM with 3 generations:
    - 3 charged leptons (e, mu, tau): each Q = -1, Q^2 = 1
    - 3 up-type quarks x N_c=3: each Q = 2/3, Q^2 = 4/9, total = 3*3*4/9 = 4
    - 3 down-type quarks x N_c=3: each Q = -1/3, Q^2 = 1/9, total = 3*3*1/9 = 1
    
    sum Q_f^2 = 3 + 4 + 1 = 8
  
  SO(10) grand unification:
    - One generation fits in a 16-dimensional spinor representation
    - 16 = 10 + 5* + 1 under SU(5)
    - The number 16 appears as the dimension of the SO(10) spinor!
  
  b_0 = 16/(3*pi) could arise from:
    - The 16 of SO(10) divided by (3*pi) where 3 = N_generations?
    - No: 3 generations is already in sum Q_f^2 = 8.
  
  Alternative: b_0 = 2*N_g*sum_per_gen Q_f^2 / (3*pi) = 2*3*(8/3)/(3*pi) 
                      = 16/(3*pi)
  
  So 16 = 2 * N_g * sum_per_gen Q_f^2.
  And 3 in denominator = 3 from the beta function normalization?
  Actually it's just 3*pi from the loop integral.
  
  The number 16 is NOT intrinsic to the adelic/zeta structure.
  It comes from the SM field content.
""")

# ===================================================================
#  SYNTHESIS
# ===================================================================

print("\n" + "=" * 70)
print("SYNTHESIS: CAN log(m_mu/m_e) = 16/3 BE DERIVED?")
print("=" * 70)

print(f"""
  SUMMARY OF ATTEMPTS:
  
  1. Zeta product at symmetric point:
     Gamma_inf(1/3)^3 = {g13_cubed:.6f}
     exp(16/3)         = {math.exp(16.0/3.0):.6f}
     NOT equal. FAILS.
  
  2. Triple-channel Veneziano structure:
     3 * Gamma_inf(1/3)^3 = {3.0*g13_cubed:.6f}
     Still not equal to exp(16/3). FAILS.
  
  3. b_0 from adelic RG:
     beta_inf(x) is the log derivative of Gamma_inf, not related
     to the QED beta function coefficient. FAILS.
  
  4. sum Q_f^2 from zeta:
     No derivation of sum Q_f^2 = 8 from zeta properties.
     The number 8 comes from SM field content and anomaly cancellation.
     FAILS (no derivation path).
  
  5. log(m_mu/m_e) from RG evolution:
     The RG evolution of Yukawa couplings is standard SM, not adelic.
     The adelic structure would need to fix the boundary condition
     at the GUT/string scale. Not demonstrated. INCOMPLETE.
  
  6. M13 compactification dictionary:
     Worldsheet instanton action: A = 2*pi*T*Delta_q
     With T=1/3: Delta_q = 8/pi (NOT integer). FAILS.
     With Delta_q integral: T must be a transcendental number. FAILS.
  
  7. Cross-ratios of Veneziano poles:
     All Veneziano pole CRs are rational with small denominators.
     No CR = 16/3 found for n_i in [0,14].
     16/3 does not appear as a simple Veneziano cross-ratio.
     FAILS (no match found).
  
  8. log ratio as zeta derivative:
     3*(log|zeta(2/3)| - log|zeta(1/3)|) = {log_diff:.6f}
     Not equal to 16/3. FAILS.
  
  9. p-adic contributions:
     Product over primes at x=1/3 converges to 1/Gamma_inf(1/3).
     No factor of 16/3 emerges. FAILS.
  
  10. The number 16 from SM field content:
      16 = 2 * N_g * sum_per_gen Q_f^2.
      This is a property of the SM, not derivable from the adelic structure.
      The adelic structure does not determine the SM gauge group or
      fermion content. NOT DERIVABLE.
""")

print("\n--- VERDICT ---")
print("""
  NONE of the 10 derivation attempts succeed.
  
  The coincidence log(m_mu/m_e)/pi ~ 16/(3*pi) appears to be:
    (a) A numerological coincidence, OR
    (b) Derivative from physics not captured by the adelic framework alone.
  
  The number 16/3 decomposes as:
    16/3 = 2 * (sum_f Q_f^2) / 3 = 2 * 8 / 3
  
  where sum_f Q_f^2 = 8 is a property of the SM with 3 generations.
  The adelic structure does not determine the SM gauge group or its
  fermion representations. Therefore, the adelic structure CANNOT
  uniquely predict 16/3.
  
  ALTERNATIVE PERSPECTIVE:
  If future work discovers that the adelic/zeta structure DOES constrain
  the SM gauge group and representations (e.g., through anomaly cancellation
  expressed adelically), then a derivation of 16/3 might be possible.
  But at present, no such constraint has been identified.
  
  RECOMMENDATION:
  Proceed to Thrust G (falsification): test whether the coincidence
  extends to m_tau/m_mu. If log(m_tau/m_mu) also matches an adelic
  expression, the coincidence is more than numerology. If not,
  the coincidence is falsified.
""")

# ===================================================================
#  BONUS: Direct numerical check of the coincidence precision
# ===================================================================

print("\n" + "=" * 70)
print("BONUS: PRECISE NUMERICAL CHECK WITH UPDATED PDG 2024 VALUES")
print("=" * 70)

# Using most precise values
m_e_pdg2024  = 0.51099895000   # MeV, PDG 2024
m_mu_pdg2024 = 105.6583745     # MeV, PDG 2024 (now known to ~2e-8 relative)

ratio_mu_e = m_mu_pdg2024 / m_e_pdg2024
log_ratio = math.log(ratio_mu_e)

print(f"  m_mu (PDG 2024) = {m_mu_pdg2024} MeV")
print(f"  m_e  (PDG 2024) = {m_e_pdg2024} MeV")
print(f"  m_mu/m_e        = {ratio_mu_e:.10f}")
print(f"  log(m_mu/m_e)   = {log_ratio:.10f}")
print(f"  16/3            = {16.0/3.0:.10f}")
print(f"")
print(f"  Absolute error  = {abs(log_ratio - 16.0/3.0):.6e}")
print(f"  Relative error  = {abs(log_ratio - 16.0/3.0) / (16.0/3.0):.4e}")
print(f"")
print(f"  In terms of experimental precision:")
print(f"  delta(m_mu/m_e)/(m_mu/m_e) ~ {5e-9:.1e} (dominated by m_e)")
print(f"  The deviation from 16/3 is {abs(log_ratio - 16.0/3.0)/(16.0/3.0):.2e}")
print(f"  This is ~{abs(log_ratio - 16.0/3.0)/(16.0/3.0)/5e-9:.0f} sigma in experimental terms")
print(f"  The deviation is HIGHLY significant. 16/3 is NOT equal to log(m_mu/m_e).")
print(f"  It is a close approximation but NOT exact.")

print("\n" + "=" * 70)
print("THRUST F COMPLETE")
print("=" * 70)
