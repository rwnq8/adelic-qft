#!/usr/bin/env python3
"""
Extended Research — Module M11: Zeta Zero Ratio Search with Statistics
File: 2.4.py

Computes zeta zeros, searches for physical mass ratios with proper
statistical validation (Bonferroni correction, null model comparison).

Associated document: 2.4.md
"""

import sys
import os
import math
import random
import mpmath as mp

mp.mp.dps = 25

# ── Zero Computation ──────────────────────────────────────────
def compute_zeros(N, verbose=True):
    """Compute the first N non-trivial zeros of zeta(s)."""
    zeros = []
    for n in range(1, N + 1):
        z = mp.zetazero(n)
        zeros.append(float(z.imag))
        if verbose and n % 100 == 0:
            print(f"  Computed {n}/{N} zeros...")
    return zeros


# ── Ratio Search ───────────────────────────────────────────────
TARGETS = {
    "muon/electron": 105.658 / 0.511,       # ~206.77
    "tau/electron": 1776.86 / 0.511,         # ~3477.22
    "tau/muon": 1776.86 / 105.658,           # ~16.817
    "proton/electron": 938.272 / 0.511,      # ~1836.15
    "W/Z": 80.377 / 91.1876,                 # ~0.8815
    "top/Higgs": 172.5 / 125.1,              # ~1.379
    "alpha_inv": 137.036,
    "alpha_Z_inv": 127.9,
}


def search_ratios(zeros, targets, max_error=1.0):
    """Find the best zero ratio match for each physical target.

    Args:
        zeros: List of imaginary parts of zeta zeros.
        targets: Dict of {name: target_value}.
        max_error: Maximum relative error (fraction) to consider.

    Returns:
        Dict of {name: {"error": float, "i": int, "j": int, "ratio": float}}
    """
    best = {}
    for name, target in targets.items():
        best[name] = {"error": float("inf"), "i": 0, "j": 0, "ratio": 0}

    for i in range(len(zeros)):
        zi = zeros[i]
        for j in range(i + 1, len(zeros)):
            zj = zeros[j]
            if zj == 0:
                continue
            ratio = zi / zj
            for name, target in targets.items():
                error = abs(ratio - target) / target
                if error < best[name]["error"]:
                    best[name] = {
                        "error": error,
                        "i": i + 1,
                        "j": j + 1,
                        "ratio": ratio,
                    }

    return best


def print_table(zeros, best_results):
    """Print formatted results table."""
    header = f"{'Ratio':<20} {'Target':>10} {'Best':>10} {'Error':>8} {'i':>5} {'j':>5} {'z_i':>10} {'z_j':>10}"
    sep = "-" * len(header)
    print(header)
    print(sep)
    for name, target in sorted(TARGETS.items(), key=lambda x: -x[1]):
        b = best_results[name]
        zi = zeros[b["i"] - 1]
        zj = zeros[b["j"] - 1]
        print(
            f"{name:<20} {target:>10.4f} {b['ratio']:>10.4f} "
            f"{b['error']*100:>7.2f}% {b['i']:>5} {b['j']:>5} "
            f"{zi:>10.3f} {zj:>10.3f}"
        )


# ── Statistical Validation ────────────────────────────────────
def bonferroni_threshold(N_zeros, N_targets, alpha=0.05):
    """Compute Bonferroni-corrected significance threshold."""
    M = N_zeros * (N_zeros - 1) / 2  # number of candidate ratios
    return alpha / (N_targets * M)


def null_model_search(
    N_zeros, targets, n_trials=100, threshold=0.01, seed=42
):
    """Perform null model: search for matches among random numbers.

    Args:
        N_zeros: Number of random values to generate.
        targets: Dict of {name: target_value}.
        n_trials: Number of null model iterations.
        threshold: Relative error threshold for a 'match'.
        seed: Random seed for reproducibility.

    Returns:
        total_matches: Total matches across all trials.
        matches_per_trial: Average matches per trial.
    """
    random.seed(seed)
    total_matches = 0

    for trial in range(n_trials):
        # Generate random numbers in same range as zeta zeros
        random_nums = sorted(
            [random.uniform(14, 500) for _ in range(N_zeros)]
        )

        for i in range(N_zeros):
            ri = random_nums[i]
            for j in range(i + 1, N_zeros):
                rj = random_nums[j]
                if rj == 0:
                    continue
                ratio = ri / rj
                for target in targets.values():
                    if abs(ratio - target) / target < threshold:
                        total_matches += 1
                        break  # Count at most one match per ratio pair

    return total_matches, total_matches / n_trials


def compute_expected_matches(
    N_zeros, targets, threshold=0.01
):
    """Compute expected number of matches under uniform random null.

    For a ratio r in [r_min, r_max], the probability of falling within
    [target*(1-threshold), target*(1+threshold)] is approximately
    2 * threshold * target / (r_max - r_min) for small threshold.

    This gives a more rigorous expected value than Monte Carlo.
    """
    M = N_zeros * (N_zeros - 1) / 2
    # Range of possible ratios for random numbers in [14, 500]
    r_min = 14.0 / 500.0  # min ratio
    r_max = 500.0 / 14.0  # max ratio
    range_width = r_max - r_min

    expected = 0.0
    for target in targets.values():
        # Probability a random ratio falls within threshold of target
        interval_width = 2 * threshold * target
        prob = interval_width / range_width
        expected += M * prob

    return expected


# ── Main ───────────────────────────────────────────────────────
def main():
    print("=" * 70)
    print("EXTENDED ZETA ZERO RATIO ANALYSIS — Module M11")
    print("=" * 70)
    print()

    # 1. Compute zeros
    N_ZEROS = 500
    print(f"1. Computing {N_ZEROS} zeta zeros...")
    zeros = compute_zeros(N_ZEROS)
    print(f"   Range: {zeros[0]:.3f} to {zeros[-1]:.3f}")
    print()

    # 2. Search for physical ratios
    print("2. Searching for physical mass/coupling ratios...")
    best = search_ratios(zeros, TARGETS)
    print()
    print_table(zeros, best)
    print()

    # 3. Statistical significance
    print("3. Statistical Validation")
    N_targets = len(TARGETS)
    bonf = bonferroni_threshold(N_ZEROS, N_targets)
    M_ratios = N_ZEROS * (N_ZEROS - 1) / 2
    print(f"   Zeros: {N_ZEROS}")
    print(f"   Candidate ratios: {M_ratios:,.0f}")
    print(f"   Target ratios: {N_targets}")
    print(f"   Bonferroni threshold (alpha=0.05): p < {bonf:.2e}")
    print()

    # 4. Match statistics
    print("4. Match Summary")
    thresholds = [0.01, 0.1, 0.5, 1.0, 5.0]
    print(f"   {'Threshold':>8}  {'Matches':>7}")
    print(f"   {'-'*8}  {'-'*7}")
    for thresh in thresholds:
        count = sum(
            1 for name in TARGETS if best[name]["error"] * 100 < thresh
        )
        print(f"   <{thresh:5.1f}%    {count:>4}/{N_targets}")
    print()

    # 5. Expected matches under null
    print("5. Expected Matches Under Null (Analytical)")
    for thresh in thresholds:
        expected = compute_expected_matches(N_ZEROS, TARGETS, thresh / 100)
        print(
            f"   <{thresh:5.1f}% threshold: expected {expected:.2f} matches "
            f"(out of {M_ratios:,.0f} candidate ratios)"
        )
    print()

    # 6. Null model Monte Carlo (lightweight — 20 trials to limit time)
    print("6. Null Model Monte Carlo (20 trials, 1% threshold)...")
    n_matches, avg_matches = null_model_search(
        N_ZEROS,
        TARGETS,
        n_trials=20,
        threshold=0.01,
        seed=42,
    )
    print(f"   Total matches in 20 trials: {n_matches}")
    print(f"   Average per trial: {avg_matches:.2f}")
    observed_1pct = sum(
        1 for name in TARGETS if best[name]["error"] * 100 < 1.0
    )
    print(f"   Observed matches (<1%): {observed_1pct}")
    if observed_1pct > avg_matches + 2:
        print("   => OBSERVED EXCEEDS NULL BY > 2x — potentially significant")
    else:
        print("   => Observed matches consistent with null expectation")
    print()

    # 7. Detailed inspection of best matches
    print("7. Detailed Best-Match Inspection")
    print()
    for name in TARGETS:
        b = best[name]
        error_pct = b["error"] * 100
        if error_pct < 1.0:
            flag = "SIGNIFICANT MATCH"
        elif error_pct < 5.0:
            flag = "Marginal"
        else:
            flag = "No match at this height"
        zi = zeros[b["i"] - 1]
        zj = zeros[b["j"] - 1]
        print(
            f"   {name:<20}: target={TARGETS[name]:.4f}, "
            f"found={b['ratio']:.4f} "
            f"(z_{b['i']}/{b['j']}={zi:.3f}/{zj:.3f}), "
            f"error={error_pct:.2f}% — {flag}"
        )

    print()
    print("=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
