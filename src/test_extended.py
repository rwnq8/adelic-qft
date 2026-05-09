#!/usr/bin/env python3
"""Extended test suite. ASCII-only for Windows compatibility."""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from padic_oscillator import Z_inf, Z_p, Z_q
from padic_gamma import morita_gamma, gamma_multiplier
from gelfand_graev_gamma import gamma_p, gamma_inf, gamma_p_product_analytic, A_p, A_inf, adelic_product
from hierarchical_rg import rg_map_dyson, find_fixed_point, critical_exponent_nu
from primes import is_prime, primes_up_to

passed = 0
failed = 0

def test(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS {name}")
    else:
        failed += 1
        print(f"  FAIL {name}  {detail}")

print("=" * 60)
print("EXTENDED TEST SUITE - Oscillator, Gamma, RG, Veneziano")
print("=" * 60)

# --- 1. Partition Functions ---
print("\n--- 1. Partition Functions ---")

test("Z_inf(1) = sqrt(pi)", abs(Z_inf(1.0) - math.sqrt(math.pi)) < 1e-10)
test("Z_inf(2) = sqrt(pi/2)", abs(Z_inf(2.0) - math.sqrt(math.pi/2)) < 1e-10)
test("Z_inf monotonically decreasing", Z_inf(2.0) < Z_inf(1.0))
try:
    Z_inf(0)
    test("Z_inf rejects beta<=0", False, "should raise ValueError")
except (ValueError, ZeroDivisionError):
    test("Z_inf rejects beta<=0", True)

test("Z_p(1, 2) > 0", Z_p(1.0, 2) > 0)
test("Z_p(beta=1000) -> 0", Z_p(1000.0, 2) < 0.1)
test("Z_p larger beta -> smaller Z", Z_p(10.0, 3) < Z_p(1.0, 3))
test("Z_p(1, 97) near exp(-1)", abs(Z_p(1.0, 97) - math.exp(-1)) < 0.01)
try:
    Z_p(-1, 2)
    test("Z_p rejects beta<=0", False, "should raise ValueError")
except (ValueError, ZeroDivisionError):
    test("Z_p rejects beta<=0", True)

test("Z_q matches Z_p for prime q", abs(Z_q(1.0, 5) - Z_p(1.0, 5)) < 1e-12)
try:
    Z_q(0, 2)
    test("Z_q rejects beta<=0", False, "should raise ValueError")
except (ValueError, ZeroDivisionError):
    test("Z_q rejects beta<=0", True)

# --- 2. Morita p-adic Gamma ---
print("\n--- 2. Morita p-adic Gamma ---")

test("Gamma_2(1) = -1", morita_gamma(2, 1) == -1)
test("Gamma_3(1) = -1", morita_gamma(3, 1) == -1)
test("Gamma_5(1) = -1", morita_gamma(5, 1) == -1)
test("Gamma_2(2) = 1", morita_gamma(2, 2) == 1)
test("Gamma_2(3) = -1", morita_gamma(2, 3) == -1)

# --- 3. Gel'fand-Graev & Freund-Witten ---
print("\n--- 3. Gel'fand-Graev & Freund-Witten ---")

test("Gamma_p(2, 0.5) = 1", abs(gamma_p(2, 0.5) - 1.0) < 1e-14)
test("Gamma_p(3, 0.5) = 1", abs(gamma_p(3, 0.5) - 1.0) < 1e-14)
test("Gamma_p(5, 0.5) = 1", abs(gamma_p(5, 0.5) - 1.0) < 1e-14)

for p in [2, 3, 5, 7, 11]:
    for x in [0.2, 0.4, 0.6, 0.8]:
        product = gamma_p(p, x) * gamma_p(p, 1.0 - x)
        test(f"Gamma_{p}({x}).Gamma_{p}({1-x}) = 1", abs(product - 1.0) < 1e-12)

for x in [0.2, 0.4, 0.6, 0.8]:
    product = gamma_inf(x) * gamma_p_product_analytic(x)
    test(f"Gamma_inf({x}).prod(Gamma_p({x})) = 1", abs(product - 1.0) < 1e-10)

test_points = [(0.25, 0.25), (0.33, 0.33), (0.4, 0.3), (0.1, 0.1)]
for a, b in test_points:
    prod = adelic_product(a, b)
    test(f"A_inf.prod(A_p)({a},{b}) = 1", abs(prod - 1.0) < 1e-10)

# --- 4. Hierarchical RG ---
print("\n--- 4. Hierarchical RG ---")

fp2, hist2, conv2 = find_fixed_point(2, rg_map_dyson, lam0=0.1)
test("p=2 converges to trivial FP", fp2 < 0.01)

fp5, hist5, conv5 = find_fixed_point(5, rg_map_dyson, lam0=0.5)
test("p=5 finds non-trivial FP", fp5 > 0.01)

# --- 5. Shared Utilities ---
print("\n--- 5. Shared Utilities ---")

test("is_prime(2) = True", is_prime(2) == True)
test("is_prime(3) = True", is_prime(3) == True)
test("is_prime(4) = False", is_prime(4) == False)
test("is_prime(97) = True", is_prime(97) == True)
test("is_prime(1) = False", is_prime(1) == False)
test("is_prime(0) = False", is_prime(0) == False)

primes_100 = primes_up_to(100)
test("25 primes <= 100", len(primes_100) == 25)
test("First prime = 2", primes_100[0] == 2)
test("Last prime = 97", primes_100[-1] == 97)

print(f"\n{'='*60}")
print(f"RESULTS: {passed} passed, {failed} failed out of {passed + failed}")
print(f"{'='*60}")

if failed > 0:
    sys.exit(1)
