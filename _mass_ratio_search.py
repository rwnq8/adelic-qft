#!/usr/bin/env python3
"""Mass ratio search in zeta zero ratios with statistical significance testing.
Checks whether particle mass ratios match ratios of consecutive zeta zeros
beyond what would be expected by chance.

Uses Bonferroni correction and permutation testing for rigorous p-values.
"""
import pickle, os, sys, math, itertools, random
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))

# Load zeta results
RESULTS = os.path.join(BASE, 'zeta_results_500.pkl')
if not os.path.exists(RESULTS):
    print(f'ERROR: {RESULTS} not found. Run _zeta_compute.py first.')
    sys.exit(1)

with open(RESULTS, 'rb') as f:
    data = pickle.load(f)

zeros = data['zeros']
print(f'Loaded {len(zeros)} zeta zeros')
print(f'Range: {zeros[0]:.2f} to {zeros[-1]:.2f}')
print(f"Mean normalized spacing: {data['mean_norm']:.6f}")
print()

# Known particle mass ratios (from PDG 2024, in GeV unless noted)
# Using central values
MASSES = {
    'electron': 0.00051099895000,
    'muon':     0.1056583755,
    'tau':      1.77686,
    'W':        80.3692,
    'Z':        91.1880,
    'top':      172.57,
    'bottom':   4.18,
    'charm':    1.27,
    'strange':  0.0934,
    'up':       0.00216,    # MeV scale, approximate
    'down':     0.00467,    # MeV scale, approximate
    'Higgs':    125.20,
}

# Mass ratios to test
RATIOS = {
    'm_W/m_Z':      MASSES['W'] / MASSES['Z'],
    'm_top/m_Higgs': MASSES['top'] / MASSES['Higgs'],
    'm_tau/m_mu':   MASSES['tau'] / MASSES['muon'],
    'm_tau/m_e':    MASSES['tau'] / MASSES['electron'],
    'm_mu/m_e':     MASSES['muon'] / MASSES['electron'],
    'm_Z/m_W':      MASSES['Z'] / MASSES['W'],
    'm_bottom/m_charm': MASSES['bottom'] / MASSES['charm'],
}

# Compute zeta zero ratios
# For zeros gamma_n, consider ratios gamma_{n+offset} / gamma_n for small offsets
MAX_OFFSET = 50
TOLERANCE = 0.02  # 2% relative tolerance for "match"

print('=' * 70)
print('MASS RATIO SEARCH IN ZETA ZERO RATIOS')
print(f'N={len(zeros)} zeros, offsets up to {MAX_OFFSET}')
print(f'Tolerance: {TOLERANCE*100:.1f}%')
print('=' * 70)
print()

# Build lookup: for each mass ratio, find best matching zeta zero ratio
matches = []
for ratio_name, target in RATIOS.items():
    best_error = float('inf')
    best_pair = None
    
    for offset in range(1, MAX_OFFSET + 1):
        for i in range(len(zeros) - offset):
            zeta_ratio = zeros[i + offset] / zeros[i]
            error = abs(zeta_ratio - target) / target
            if error < best_error:
                best_error = error
                best_pair = (i + 1, i + 1 + offset, offset, zeta_ratio)
    
    matches.append({
        'name': ratio_name,
        'target': target,
        'best_error': best_error,
        'n1': best_pair[0],
        'n2': best_pair[1],
        'offset': best_pair[2],
        'zeta_ratio': best_pair[3],
    })

# Sort by error
matches.sort(key=lambda x: x['best_error'])

print(f'{"Ratio":<20s} {"Target":>10s} {"Zeta Match":>10s} {"Error":>8s} {"n1":>6s} {"n2":>6s} {"off":>4s}')
print('-' * 70)
for m in matches:
    flag = ' *' if m['best_error'] < TOLERANCE else ''
    print(f'{m["name"]:<20s} {m["target"]:10.6f} {m["zeta_ratio"]:10.6f} '
          f'{m["best_error"]*100:7.3f}% {m["n1"]:6d} {m["n2"]:6d} {m["offset"]:4d}{flag}')

# Statistical significance testing
print()
print('=' * 70)
print('STATISTICAL SIGNIFICANCE TESTING')
print('=' * 70)
print()

def permutation_test(zeros, target, offset, n_perm=10000):
    """Permutation test: how often does a random set of ratios match as well?"""
    # Generate random "particle masses" from uniform distribution
    # over the range of zeta zeros, compute their ratios, and check
    # how many match zeta zero ratios at the observed tolerance level.
    z_min, z_max = zeros[0], zeros[-1]
    count_better = 0
    observed_error = float('inf')  # placeholder
    
    # First, get the observed best error
    for i in range(len(zeros) - offset):
        zr = zeros[i + offset] / zeros[i]
        err = abs(zr - target) / target
        observed_error = min(observed_error, err)
    
    # Now permutation: random "masses" 
    for _ in range(n_perm):
        # Random ratio from uniform masses
        m1_r = random.uniform(z_min, z_max)
        m2_r = random.uniform(z_min, z_max)
        if m1_r == 0 or m2_r == 0:
            continue
        random_ratio = max(m1_r, m2_r) / min(m1_r, m2_r)
        
        # Check if any zeta zero ratio matches this random target
        for i in range(len(zeros) - offset):
            zr = zeros[i + offset] / zeros[i]
            if abs(zr - random_ratio) / random_ratio < TOLERANCE:
                count_better += 1
                break
    
    p_value = count_better / n_perm if n_perm > 0 else 1.0
    return observed_error, p_value

# Simplified statistical test: Bonferroni correction
n_comparisons = len(RATIOS) * MAX_OFFSET * len(zeros)  # Total comparisons made
bonferroni_alpha = 0.05 / n_comparisons

print(f'Total comparisons: {n_comparisons:,}')
print(f'Bonferroni threshold (alpha=0.05): {bonferroni_alpha:.2e}')
print()

# For each ratio, estimate the expected number of matches by chance
print('Expected vs. observed matches:')
print(f'{"Ratio":<20s} {"Obs Error":>8s} {"Within Tol?":>10s} {"P(rand match)":>14s} {"Bonf Sig?":>10s}')
print('-' * 70)

# Compute probability of random match for each ratio
for m in matches:
    # Probability that a random ratio falls within tolerance of target
    # over all zeta zero ratios tested
    within_tol = m['best_error'] < TOLERANCE
    
    # Estimate: for each offset, how many zeta ratios fall within tolerance of the target?
    count_within = 0
    total_checked = 0
    for offset in range(1, MAX_OFFSET + 1):
        for i in range(len(zeros) - offset):
            zr = zeros[i + offset] / zeros[i]
            total_checked += 1
            if abs(zr - m['target']) / m['target'] < TOLERANCE:
                count_within += 1
    
    # Probability of at least one match by chance
    # Under null: each ratio is independent, probability of match = count_within / total_checked
    p_match = count_within / total_checked if total_checked > 0 else 0
    # Probability of at least one match in N=total_checked trials
    p_at_least_one = 1 - (1 - p_match) ** total_checked if p_match < 1 else 1.0
    
    # Bonferroni-adjusted
    bonf_significant = p_at_least_one < bonferroni_alpha if p_match > 0 else False
    
    flag = '*' if within_tol else ''
    sig = 'YES' if bonf_significant else 'no'
    print(f'{m["name"]:<20s} {m["best_error"]*100:7.3f}% {str(within_tol):>10s} '
          f'{p_at_least_one:14.2e} {sig:>10s}{flag}')

print()
print('CONCLUSION:')
matches_within_tol = [m for m in matches if m['best_error'] < TOLERANCE]
print(f'  {len(matches_within_tol)}/{len(RATIOS)} ratios match within {TOLERANCE*100:.0f}% tolerance')
print(f'  With {n_comparisons:,} total comparisons, coincidental matches are expected.')
print(f'  The Bonferroni threshold is {bonferroni_alpha:.2e}.')

if any(1 - (1 - m['best_error']) ** n_comparisons < bonferroni_alpha for m in matches if m['best_error'] < TOLERANCE):
    print('  Some matches survive Bonferroni correction.')
else:
    print('  NO MATCHES survive Bonferroni correction — consistent with chance.')

# Null model: random mass spectrum
print()
print('=' * 70)
print('NULL MODEL: Random mass spectrum')
print('=' * 70)

random.seed(42)
n_null = 1000
null_matches = []
for _ in range(n_null):
    # Generate 7 random "masses" from log-uniform over zeta range
    null_masses = [10 ** random.uniform(math.log10(zeros[0]), math.log10(zeros[-1])) 
                   for _ in range(7)]
    # Compute 7 choose 2 = 21 ratios
    null_ratios = []
    for i in range(len(null_masses)):
        for j in range(i+1, len(null_masses)):
            null_ratios.append(max(null_masses[i], null_masses[j]) / 
                              min(null_masses[i], null_masses[j]))
    
    # Count how many of these random ratios match zeta zero ratios
    count = 0
    for nr in null_ratios:
        for offset in range(1, MAX_OFFSET + 1):
            for i in range(len(zeros) - offset):
                if abs(zeros[i+offset]/zeros[i] - nr) / nr < TOLERANCE:
                    count += 1
                    break
            if count > 0:
                break
    null_matches.append(count)

avg_null = sum(null_matches) / len(null_matches)
print(f'Null model ({n_null} trials, 21 random ratios each):')
print(f'  Average matches per trial: {avg_null:.2f}')
print(f'  Our observed matches within {TOLERANCE*100:.0f}%: {len(matches_within_tol)}')

if len(matches_within_tol) <= avg_null + 2 * (sum((x-avg_null)**2 for x in null_matches)/len(null_matches))**0.5:
    print('  Observed matches NOT significantly different from random.')
else:
    print('  Observed matches EXCEED random expectation (p < 0.05).')

print()
print('=' * 70)
print('DONE: Mass ratio search complete.')
print('=' * 70)
