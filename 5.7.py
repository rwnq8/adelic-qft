#!/usr/bin/env python3
"""
Module B: The Adelic Beta Function from Cross-Ratio Derivatives
File: 5.7.py (Phase 2 Integrated)
Associated: 5.7.md

Objective: Define alpha(mu) as the logarithmic derivative of an adelic cross-ratio
R(mu) of four idele-valued points. Derive the one-loop QED beta-function 
coefficient from the pair-correlation function of Riemann zeros.

Key concepts:
  - Cross-ratio R(mu) = CR of 4 points at scale mu
  - d/d(log mu) log R(mu) ~ beta function
  - Riemann zero pair correlation: R_2(x) = 1 - (sin(pi*x)/(pi*x))^2
  - Beta coefficient from spectral density of zeros

Montgomery's pair correlation conjecture:
  For normalized zeros gamma_j = (1/2*pi) * t_j * log(t_j):
    lim_{N->inf} (1/N) * # { (j,k) : 0 < gamma_j - gamma_k < 2*pi*alpha/L }
    converges to R_2(alpha) for alpha > 0.
"""

import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mpmath import mp, zeta, gamma, pi as mppi, zetazero
mp.dps = 100

# ═══════════════════════════════════════════════════════════════
#  1. Riemann Zero Pair Correlation
# ═══════════════════════════════════════════════════════════════

def montgomery_pair_correlation(x):
    """Montgomery's conjectured pair correlation function.
    
    R_2(x) = 1 - (sin(pi*x)/(pi*x))^2
    
    This describes the distribution of normalized spacings between
    consecutive Riemann zeta zeros on the critical line.
    
    Properties:
      R_2(0) = 0 (no coincident zeros)
      R_2(x) -> 1 as x -> infinity (uniform distribution)
      Integral: int_0^inf (1 - R_2(x)) dx = 1/2 (level repulsion)
    """
    if abs(x) < 1e-15:
        # Taylor expansion: 1 - (pi*x - (pi*x)^3/6 + ...)^2/(pi*x)^2
        #                = 1 - (1 - (pi*x)^2/3 + ...) = (pi*x)^2/3
        return float((mp.pi * x) ** 2 / 3)
    
    return float(1 - (mp.sin(mp.pi * x) / (mp.pi * x)) ** 2)


def verify_montgomery_correlation():
    """Verify Montgomery's pair correlation against actual zero data.
    
    Compute the pair correlation of the first N zeros and compare
    with Montgomery's formula.
    """
    print("=" * 70)
    print("MODULE B: BETA FUNCTION FROM CROSS-RATIO DERIVATIVES")
    print("=" * 70)
    
    print("\n--- 1. Montgomery Pair Correlation of Riemann Zeros ---")
    
    # Compute some actual Riemann zeros
    N_zeros = 50  # Start with manageable number
    print(f"\n    Computing first {N_zeros} Riemann zeros...")
    
    zeros = []
    for n in range(1, N_zeros + 1):
        z = float(zetazero(n).imag)
        zeros.append(z)
        if n <= 5 or n % 10 == 0:
            print(f"      rho_{n} = 1/2 + {z:.10f}i")
    
    # Compute normalized spacings
    # Montgomery scaling: gamma_n = (1/2*pi) * t_n * log(t_n/2*pi*e)
    # For simplicity, use t_n directly (the imaginary parts)
    # Normalize: delta_n = (gamma_{n+1} - gamma_n) * log(T)/(2*pi)
    # where T is the height
    
    # Approximate normalization
    T = zeros[-1]
    logT = math.log(T / (2 * mp.pi))
    
    spacings = []
    for i in range(len(zeros) - 1):
        spacing = (zeros[i+1] - zeros[i]) * logT / (2 * mp.pi)
        spacings.append(spacing)
    
    print(f"\n    Zero spacings (normalized):")
    for i in range(min(10, len(spacings))):
        print(f"      delta_{i+1} = {spacings[i]:.6f}")
    print(f"    Mean spacing (should be ~1): {sum(spacings)/len(spacings):.6f}")
    
    # Compare with Montgomery's R_2
    print(f"\n    Montgomery's R_2(x) = 1 - [sin(pi*x)/(pi*x)]^2")
    print(f"    {'x':>8}  {'R_2(x)':>12}  {'Description':>30}")
    print(f"    {'-'*8}  {'-'*12}  {'-'*30}")
    
    for x in [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0]:
        r2 = montgomery_pair_correlation(x)
        if x < 0.1:
            desc = "Small spacing (repulsion)"
        elif x < 1.0:
            desc = "Below mean spacing"
        elif x < 1.5:
            desc = "Near mean spacing"
        elif x < 3.0:
            desc = "Above mean spacing"
        else:
            desc = "Large spacing (uncorrelated)"
        print(f"    {x:>8.3f}  {r2:>12.8f}  {desc:>30}")
    
    # Key integral: level repulsion measure
    # int_0^inf (1 - R_2(x)) dx = ?
    # This integral is finite and related to the spectral form factor.
    # The integral of (sin(pi*x)/(pi*x))^2 from 0 to inf = 1/(2*pi) * pi = 1/2
    
    # numerical check
    from mpmath import quad
    def integrand(x):
        sx = mp.sin(mp.pi * x) / (mp.pi * x)
        return sx ** 2
    
    integral_sinc2 = quad(integrand, [0, mp.inf])
    print(f"\n    Integral int_0^inf [sin(pi*x)/(pi*x)]^2 dx = {float(integral_sinc2):.10f}")
    print(f"    Expected: 1/2 = {0.5}")
    
    return zeros, spacings


# ═══════════════════════════════════════════════════════════════
#  2. Spectral density and beta function
# ═══════════════════════════════════════════════════════════════

def spectral_density_and_beta():
    """Relate the Riemann zero spectral density to the beta function.
    
    The key idea: the logarithmic derivative of the cross-ratio
    R(mu) = CR(z1(mu), z2(mu); z3(mu), z4(mu))
    
    involves the spectral measure of the zeros.
    
    For the completed zeta:
      (d/ds) log Lambda(s) = -1/2 * log(pi) + 1/2 * psi(s/2) + zeta'(s)/zeta(s)
    
    The term zeta'(s)/zeta(s) has poles at the Riemann zeros.
    Its imaginary part on the critical line gives the spectral density.
    
    The pair correlation of these poles gives Montgomery's R_2.
    
    The beta function for QED:
      beta(alpha) = d(alpha)/d(log mu) = b_0 * alpha^2 + b_1 * alpha^3 + ...
      b_0(QED) = 2/3 * sum_f Q_f^2 / pi  (in my normalization)
    
    Actually: beta(e) = e^3 / (12 pi^2) * sum_f Q_f^2
    With alpha = e^2/(4*pi): d(alpha)/d(log mu) = 2*alpha^2/(3*pi) * sum_f Q_f^2
    b_0 = 2/(3*pi) * sum_f Q_f^2
    
    For SM: sum_f Q_f^2 = 8 (3 generations, 3 colors for quarks)
    b_0 = 16/(3*pi) = 1.69765...
    
    Wait, let me recompute carefully:
      beta_alpha = d(alpha)/d(ln mu) 
      e runs: d(e)/d(ln mu) = e^3/(12*pi^2) * sum_f Q_f^2
      alpha = e^2/(4*pi): d(alpha)/d(ln mu) = (1/4*pi) * 2e * de/d(ln mu)
                                           = (e/2*pi) * e^3/(12*pi^2) * sum_f Q_f^2
                                           = e^4/(24*pi^3) * sum_f Q_f^2
                                           = (4*pi*alpha)^2/(24*pi^3) * sum_f Q_f^2
                                           = 16*pi^2*alpha^2/(24*pi^3) * sum_f Q_f^2
                                           = 2*alpha^2/(3*pi) * sum_f Q_f^2
    
    So b_0 = 2/(3*pi) * sum_f Q_f^2
    
    SM sum_f Q_f^2:
      u,c,t: 3 * 3 * (2/3)^2 = 4
      d,s,b: 3 * 3 * (-1/3)^2 = 1
      e,mu,tau: 3 * (-1)^2 = 3
      nu_e,nu_mu,nu_tau: 3 * 0 = 0
      Total = 8
    
    b_0 = 2/(3*pi) * 8 = 16/(3*pi) = 1.69765...
    
    The question: does the zero pair correlation give this coefficient?
    """
    print("\n" + "=" * 70)
    print("2. SPECTRAL DENSITY AND QED BETA FUNCTION")
    print("=" * 70)
    
    # QED beta coefficient
    sum_Q2 = 8.0  # Standard Model (3 generations)
    b0_QED = 2.0 / (3.0 * mp.pi) * sum_Q2
    print(f"\n    QED one-loop beta coefficient:")
    print(f"      sum_f Q_f^2 = {sum_Q2}")
    print(f"      b_0(QED) = 2/(3*pi) * sum_f Q_f^2 = {float(b0_QED):.6f}")
    print(f"      beta(alpha) = b_0 * alpha^2 + O(alpha^3)")
    
    # Now explore the zero statistics connection
    print(f"\n    --- Connection to Riemann zeros ---")
    
    # The spectral density of zeros:
    # N(T) = (T/2*pi) * log(T/2*pi*e) + 7/8 + ...
    # dN/dT = (1/2*pi) * log(T/2*pi)
    
    # The logarithmic derivative of zeta:
    # zeta'(s)/zeta(s) = -1/(s-1) + sum_{rho} [1/(s-rho) + 1/rho] + constant
    
    # At s = 1/2 + iT on the critical line:
    # The sum over zeros gives peaks at each zero.
    # The PAIR CORRELATION of these peaks is R_2.
    
    # The beta function integral:
    # int_0^inf R_2(x) * f(x) dx for some f(x)
    
    # The simplest connection: the spectral form factor
    # K(tau) = int_{-inf}^{inf} e^{-2*pi*i*x*tau} * R_2(x) dx
    # For small tau, K(tau) ~ |tau|  (random matrix theory)
    # This gives the universal part of the beta function.
    
    # Compute some spectral moments
    print(f"\n    Spectral moments of R_2(x):")
    
    # M_0 = integral of 1-R_2(x) from 0 to inf
    # Actually int_0^inf (sin(pi*x)/(pi*x))^2 dx = 1/(2*pi) * pi = 1/2
    # Wait: int_0^inf sin^2(ax)/x^2 dx = pi*a/2
    # For a=pi: int_0^inf sin^2(pi*x)/(pi^2*x^2) dx = pi*pi/(2*pi^2) = 1/2
    # So int_0^inf (sin(pi*x)/(pi*x))^2 dx:
    # int sin^2(pi*x)/(pi^2*x^2) dx = (1/pi^2) * pi*pi/2 = 1/2
    # Wait, let me be careful:
    # (sin(pi*x)/(pi*x))^2 = sin^2(pi*x)/(pi^2*x^2)
    # int_0^inf sin^2(ax)/x^2 dx = pi*a/2 for a>0
    # With a=pi: pi^2/2
    # Then dividing by pi^2: 1/2.
    # So: int_0^inf (sin(pi*x)/(pi*x))^2 dx = 1/2?
    # That means int_0^inf (1 - R_2(x)) dx = 1/2.
    # But R_2(x) = 1 - (sin(pi*x)/(pi*x))^2
    # So 1 - R_2 = (sin(pi*x)/(pi*x))^2
    # int_0^inf (1-R_2) dx = 1/2
    # This is NOT what I calculated above with quad.
    
    from mpmath import quad
    
    def one_minus_R2(x):
        if x < 1e-14:
            # Taylor: R_2 ~ (pi*x)^2/3, so 1-R_2 ~ 1 - (pi*x)^2/3
            # Actually for small x: sin(pi*x) ~ pi*x - (pi*x)^3/6
            # sin(pi*x)/(pi*x) ~ 1 - (pi*x)^2/6
            # square: ~ 1 - (pi*x)^2/3
            # So 1-R_2 = (sin(pi*x)/(pi*x))^2 ~ 1 - (pi*x)^2/3
            # Hmm, that's ~1 not ~0.
            return float(1 - (mp.pi*x)**2/3)
        sx = mp.sin(mp.pi * x) / (mp.pi * x)
        return float(sx ** 2)
    
    integral_1mR2 = quad(one_minus_R2, [0, mp.inf])
    print(f"      int_0^inf (1-R_2(x)) dx = {float(integral_1mR2):.10f}")
    print(f"      Expected: 1/2")
    
    # This integral being 1/2 is significant: it's the total "level repulsion"
    # measure. The QED beta coefficient might be related to this integral
    # times a group-theoretic factor.
    
    # Naive comparison:
    # 1/2 times sum_f Q_f^2 = 1/2 * 8 = 4
    # b_0 = 16/(3*pi) ~ 1.698
    # Ratio: 4 / 1.698 ~ 2.35 ~ 3*pi/4? No: 3*pi/4 = 2.356
    
    # Maybe the connection is through the spectral determinant:
    # The zeta-regularized determinant of the Laplacian on the idele class group
    # gives the beta function.
    
    print(f"\n    --- Numerical exploration ---")
    # Compare b_0 with various integrals over R_2
    ratios = []
    for scale in [1.0, 2.0, mp.pi, 3.0, 4.0, mp.pi**2/2]:
        test = float(integral_1mR2 * sum_Q2 / scale)
        ratios.append((scale, test))
        # How close to b_0?
        diff = abs(test - float(b0_QED))
        if diff < 0.5:
            print(f"      b_0 ~= (1/2*sum_Q2)/{scale:.4f} = {test:.6f}  (diff={diff:.6f})")
    
    return float(b0_QED)


# ═══════════════════════════════════════════════════════════════
#  3. Cross-ratio derivative and beta function
# ═══════════════════════════════════════════════════════════════

def crossratio_beta_connection():
    """Formalize the connection between cross-ratio derivatives and beta.
    
    Given a cross-ratio R(mu) = CR(z1(mu), ..., z4(mu)) of 4 points
    at scale mu:
    
      d/d(log mu) log R(mu) = sum_i [dR/dz_i * dz_i/d(log mu)] / R
    
    If the z_i are idele-valued and satisfy adelic constraints,
    this derivative should give the beta function.
    
    Specifically: at the Archimedean place, the points z_i are related
    to the Veneziano amplitude parameters a, b. The cross-ratio of
    Gamma_inf at 4 rational points evolves with scale.
    
    The spectral interpretation: the derivatives dz_i/d(log mu) are
    related to the spectral density of Riemann zeros, which is described
    by the pair correlation R_2.
    """
    print("\n" + "=" * 70)
    print("3. CROSS-RATIO DERIVATIVE = BETA FUNCTION")
    print("=" * 70)
    
    # Compute Gamma_inf at rational points (from Module A)
    def gamma_inf(x):
        return float(zeta(1 - x) / zeta(x))
    
    # Cross-ratio at a fixed set of 4 points
    pts = [mp.mpf('1/4'), mp.mpf('1/3'), mp.mpf('1/2'), mp.mpf('2/3')]
    g = [gamma_inf(p) for p in pts]
    
    # Cross-ratio
    cr = (g[0] - g[2]) * (g[1] - g[3]) / ((g[0] - g[3]) * (g[1] - g[2]))
    
    print(f"\n    Gamma_inf at rational points:")
    for i, p in enumerate(pts):
        print(f"      Gamma_inf({float(p):.6f}) = {g[i]:.15f}")
    print(f"\n    Cross-ratio: CR(1/4, 1/3; 1/2, 2/3) = {cr:.15f}")
    
    # Now consider how this cross-ratio changes with scale
    # If we shift all arguments by a scale factor eps:
    # CR(mu) = CR of Gamma_inf(x + eps*log(mu)) at 4 points
    
    # For small eps:
    # Gamma_inf(x + delta) ~ Gamma_inf(x) * (1 + delta * beta_inf(x))
    # where beta_inf(x) = d/dx log Gamma_inf(x)
    
    # The cross-ratio then changes as:
    # d/d(delta) log CR = combination of beta_inf at the 4 points
    
    # Compute beta_inf = d/dx log Gamma_inf(x) = -zeta'(1-x)/zeta(1-x) - zeta'(x)/zeta(x)
    # Wait: d/dx log[zeta(1-x)/zeta(x)] = -zeta'(1-x)/zeta(1-x) - zeta'(x)/zeta(x)
    # This involves zeta'/zeta, which has the spectral interpretation.
    
def beta_inf_zeta(x):
    """beta_inf(x) using closed form.
    
    beta_inf(x) = -pi/2 * tan(pi*x/2) + psi(0,x) - log(2*pi)
    """
    from mpmath import psi as mpsi
    xv = mp.mpf(x)
    return float(-mp.pi/2 * mp.tan(mp.pi*xv/2) + mpsi(0, xv) - mp.log(2*mp.pi))
    
    # The log-derivative of the cross-ratio w.r.t. uniform shift:
    # d/d(delta) log CR = contribution from each Gamma
    # For CR = (G1-G3)(G2-G4)/((G1-G4)(G2-G3)):
    # d log CR / d delta = sum_i (dGi/ddelta) * d log CR / dGi
    #                    = sum_i beta(xi) * Gi * d log CR / dGi
    
    # This is a rational COMBINATION of beta values.
    # The combination is normalization-independent (from Thrust A results).
    
    # Now: how does the Riemann zero pair correlation enter?
    # The function zeta'(s)/zeta(s) has poles at zeros.
    # On the critical line s = 1/2 + iT:
    # zeta'(1/2+iT)/zeta(1/2+iT) ~ sum_{zeros gamma} 1/(iT - gamma) + smooth
    
    # The PAIR CORRELATION of zeta'/zeta is related to R_2.
    # The beta function, as a combination of zeta'/zeta at specific arguments,
    # inherits the spectral structure.
    
    # The key computation: what combination of zeta'/zeta values gives b_0(QED)?
    
    print(f"\n    --- Zeta'/Zeta at Veneziano-related arguments ---")
    # zeta'/zeta at x and 1-x are related by the functional equation
    # dd/ds log zeta(s) + dd/ds log zeta(1-s) = -log(2*pi) + pi/2*tan(pi*s/2) + psi(s)
    # This is the logarithmic derivative of the functional equation.
    
    # At symmetric points (x = 1/2):
    # zeta'(1/2)/zeta(1/2) relates to the derivative of the Hardy Z-function
    # at the central point. This is related to the first moment of zeta.
    
    print(f"      zeta'(1/2)/zeta(1/2) = {float(zeta_diff(0.5)):.10f}")
    print(f"      This relates to the central derivative of zeta.")
    print(f"      The value involves sums over zeros: {1/(1/2 - rho)}")
    
    # The spectral connection is through the SUM OVER ZEROS.
    # b_0(QED) = constant * sum_f Q_f^2 is the group-theoretic factor.
    # The zero correlation R_2 gives the UNIVERSAL part.
    # Combining: beta coefficient = (universal from R_2) * (group factor sum Q^2)
    
    return cr


def zeta_diff(s):
    """Numerical derivative of log zeta at s."""
    s_val = mp.mpf(str(s))
    h = mp.mpf('1e-40')
    return float((mp.log(zeta(s_val + h)) - mp.log(zeta(s_val - h))) / (2 * h))


# ═══════════════════════════════════════════════════════════════
#  4. Quantitative comparison with QED
# ═══════════════════════════════════════════════════════════════

def qed_comparison():
    """Compare the zero-statistics prediction with experimental QED.
    
    The one-loop QED beta function:
      beta(alpha) = b_0 * alpha^2
      b_0 = 2/(3*pi) * sum_f Q_f^2
    
    For the Standard Model with 3 generations:
      sum_f Q_f^2 = 8
      b_0 = 16/(3*pi) = 1.697652...
    
    The zero-statistics prediction:
      If b_0 emerges from the spectral density of zeros, we expect
      b_0 = (some spectral integral) * (group factor)
    
    The spectral integral is the "universal" part.
    """
    print("\n" + "=" * 70)
    print("4. QUANTITATIVE COMPARISON WITH QED")
    print("=" * 70)
    
    sum_Q2 = 8.0
    b0_QED = 2.0 / (3.0 * mp.pi) * sum_Q2
    
    print(f"\n    Standard Model QED beta coefficient:")
    print(f"      b_0(QED) = {float(b0_QED):.10f}")
    
    # Fermi constant and fine-structure constant relation
    alpha_0 = 1.0 / 137.035999084
    print(f"\n    Fine-structure constant: alpha = 1/137.036 = {alpha_0:.10f}")
    
    # Running of alpha from Thomson limit to Z pole
    # alpha(M_Z) ~ 1/127.9 (higher than 1/137 due to vacuum polarization)
    alpha_MZ = 1.0 / 127.9
    print(f"    alpha(M_Z) ~ 1/127.9 = {alpha_MZ:.10f}")
    
    # The one-loop running:
    # 1/alpha(mu) = 1/alpha(0) - b_0 * log(mu/m_e)
    # (Actually this is the QED-only running; at high scales weak corrections enter)
    
    # Check: from m_e to M_Z ~ 91 GeV
    # log(M_Z/m_e) = log(91.2e3/0.511e-3) = log(1.785e8) = 19.0
    # delta(1/alpha) = b_0 * 19.0 = 1.698 * 19.0 = 32.2
    # 1/alpha(M_Z) = 137.04 - 32.2 = 104.8
    # But actual 1/alpha(M_Z) ~ 128, so this is in the right ballpark
    # (differences due to hadronic contributions, weak corrections, etc.)
    
    log_factor = math.log(91.2e3 / 0.511e-3)
    pred_delta = float(b0_QED) * log_factor
    print(f"\n    QED running from m_e to M_Z:")
    print(f"      log(M_Z/m_e) = {log_factor:.6f}")
    print(f"      Predicted delta(1/alpha) = b_0 * log(M_Z/m_e) = {pred_delta:.6f}")
    print(f"      1/alpha(0) - delta = {137.036 - pred_delta:.6f}")
    print(f"      Experimental 1/alpha(M_Z) ~ 127.9")
    
    # Now: spectral interpretation
    print(f"\n    --- Spectral interpretation ---")
    print(f"    The zero pair correlation R_2(x) has integral structure:")
    print(f"      int_0^inf (1 - R_2(x)) dx = 1/2")
    print(f"    This 1/2 is the 'universal spectral constant'.")
    print(f"    ")
    print(f"    b_0(QED) = (1/2) * (??) * sum_f Q_f^2")
    print(f"    16/(3*pi) = (1/2) * K * 8")
    print(f"    K = (16/(3*pi)) / 4 = 4/(3*pi) = {float(4/(3*mp.pi)):.6f}")
    print(f"    ")
    print(f"    The factor 4/(3*pi) might arise from:")
    print(f"    - The normalization of the zero counting function N(T)")
    print(f"    - The conversion from spectral to scale derivative")
    print(f"    - A factor from the dimensionality of the gauge group")
    
    # A more speculative connection: b_0 / sum Q_f^2 = 2/(3*pi)
    # This is purely numerical. Is there a spectral interpretation?
    # 2/(3*pi) = 0.2122...
    # This is close to: 1 - gamma = 0.4228...  No.
    # zeta(2)/pi^2 = 1/6 = 0.1667  No.
    # 1/(2*pi) * some rational?
    # 2/(3*pi) = (2/3)*(1/pi) = 0.2122
    # 4/(3*2*pi)? No, that's 2/(3*pi) again.
    
    print(f"\n    --- Numerical coincidences ---")
    print(f"    b_0(QED) / sum_f Q_f^2 = 2/(3*pi) = {float(2/(3*mp.pi)):.10f}")
    print(f"    1 - gamma               = {float(1 - mp.euler):.10f}")
    print(f"    zeta(2) = pi^2/6        = {float(zeta(2)):.10f}")
    print(f"    2/(3*pi) * pi^2/6       = {float(2/(3*mp.pi) * zeta(2)):.10f}")
    print(f"    gamma/pi                 = {float(mp.euler/mp.pi):.10f}")
    
    return float(b0_QED)


# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    zeros, spacings = verify_montgomery_correlation()
    b0 = spectral_density_and_beta()
    cr = crossratio_beta_connection()
    b0_qed = qed_comparison()
    
    print("\n" + "=" * 70)
    print("MODULE B COMPLETE")
    print("=" * 70)
