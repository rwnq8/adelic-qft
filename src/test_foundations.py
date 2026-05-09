#!/usr/bin/env python3
"""
Module M1: Foundational Library — Test Suite
File: src/test_foundations.py

25+ tests for PadicNumber, QadicNumber, and Adele classes.
Verifies product formula, arithmetic, edge cases, and Hensel expansion.

Run: python -m pytest src/test_foundations.py -v
Or:  python src/test_foundations.py
"""

import sys
import os
import random
from fractions import Fraction
from itertools import product

# Ensure src/ is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from padic import PadicNumber
from qadic import QadicNumber
from adele import Adele

# ================================================================
#  PadicNumber Tests
# ================================================================

def test_padic_construction_basic():
    """PadicNumber should compute valuation and norm correctly for simple cases."""
    x = PadicNumber(2, 2)
    assert x.valuation == 1
    assert x.norm() == Fraction(1, 2)
    assert x.unit == Fraction(1, 1)
    assert x.q == Fraction(2, 1)


def test_padic_norm_of_one():
    """|1|_p should be 1 for any prime p (unit)."""
    for p in [2, 3, 5, 7, 11, 97]:
        x = PadicNumber(p, 1)
        assert x.valuation == 0, f"v_{p}(1) should be 0"
        assert x.norm() == Fraction(1, 1), f"|1|_{p} should be 1"
        assert x.is_unit()


def test_padic_zero():
    """Zero should have infinite valuation and norm 0."""
    x = PadicNumber(2, 0)
    assert x.valuation == float('inf')
    assert x.norm() == Fraction(0, 1)
    # Zero is a p-adic integer: |0|_p = 0 ≤ 1
    assert x.is_integer()
    # But zero is NOT a p-adic unit (|0|_p ≠ 1)
    assert not x.is_unit()


def test_padic_norm_multiplicativity():
    """|xy|_p = |x|_p · |y|_p."""
    random.seed(42)
    for _ in range(10):
        p = random.choice([2, 3, 5, 7, 11])
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        x = PadicNumber(p, Fraction(a, b))
        y = PadicNumber(p, Fraction(b, a))
        xy = x * y
        assert abs(xy.norm() - x.norm() * y.norm()) < 1e-15


def test_padic_valuation_additivity():
    """v_p(xy) = v_p(x) + v_p(y)."""
    x = PadicNumber(2, Fraction(2, 1))
    y = PadicNumber(2, Fraction(8, 1))  # 2^3
    xy = x * y
    assert xy.valuation == x.valuation + y.valuation  # 1 + 3 = 4


def test_padic_ultrametric_inequality():
    """The strong triangle inequality: |x + y|_p ≤ max(|x|_p, |y|_p)."""
    p = 7
    for a, b in [(1, 7), (7, 49), (14, 21)]:
        x = PadicNumber(p, a)
        y = PadicNumber(p, b)
        z = x + y
        assert z.norm() <= max(x.norm(), y.norm()), \
            f"Failed: |{a}+{b}|_7 = {z.norm()}, max = {max(x.norm(), y.norm())}"


def test_padic_arithmetic_add():
    """Addition of p-adic numbers."""
    x = PadicNumber(3, Fraction(1, 3))
    y = PadicNumber(3, Fraction(2, 3))
    z = x + y
    assert z.q == Fraction(1, 1)


def test_padic_arithmetic_mul():
    """Multiplication of p-adic numbers."""
    x = PadicNumber(5, Fraction(5, 2))
    y = PadicNumber(5, Fraction(2, 5))
    z = x * y
    assert z.q == Fraction(1, 1)


def test_padic_arithmetic_div():
    """Division of p-adic numbers."""
    x = PadicNumber(2, Fraction(12, 5))
    y = PadicNumber(2, Fraction(3, 5))
    z = x / y
    assert z.q == Fraction(4, 1)


def test_padic_arithmetic_sub():
    """Subtraction of p-adic numbers."""
    x = PadicNumber(2, Fraction(3, 2))
    y = PadicNumber(2, Fraction(1, 2))
    z = x - y
    assert z.q == Fraction(1, 1)


def test_padic_negative():
    """Negative numbers: v_p(-q) = v_p(q), |-q|_p = |q|_p."""
    x = PadicNumber(2, 4)
    nx = PadicNumber(2, -4)
    assert x.valuation == nx.valuation
    assert x.norm() == nx.norm()


def test_padic_large_valuation():
    """Numbers with large valuation should have correctly computed norms."""
    x = PadicNumber(2, 2**20)  # 2^20, so v_2 = 20
    assert x.valuation == 20
    assert x.norm() == Fraction(1, 2**20)


def test_padic_negative_valuation():
    """Numbers with negative valuation (denominator has p factors)."""
    x = PadicNumber(3, Fraction(1, 9))  # v_3(1/9) = -2
    assert x.valuation == -2
    assert x.norm() == Fraction(9, 1)


def test_padic_expansion_unit():
    """Hensel expansion of a p-adic unit should produce correct digits."""
    x = PadicNumber(5, Fraction(3, 1))  # 3 mod 5 = 3
    digits = x.expansion(5)
    assert digits[0] == 3  # 3 mod 5
    # 3 = 3 + 0·5 + 0·5² + ...
    assert all(d == 0 for d in digits[1:])


def test_padic_expansion_known():
    """Test Hensel expansion against a known case."""
    # -1 in ℚ₂: -1 = 1 + 2 + 4 + 8 + ... (all digits 1)
    x = PadicNumber(2, -1)
    digits = x.expansion(5)
    assert digits == [1, 1, 1, 1, 1], f"Got {digits}"


def test_padic_different_primes_error():
    """Cannot do arithmetic across different primes."""
    x = PadicNumber(2, 1)
    y = PadicNumber(3, 1)
    try:
        _ = x + y
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


# ================================================================
#  QadicNumber Tests
# ================================================================

def test_qadic_prime_degenerate():
    """For q = prime, QadicNumber should match PadicNumber norm."""
    x = QadicNumber(2, Fraction(4, 1))
    assert x.valuation == 2
    assert abs(x.norm() - 0.25) < 1e-15


def test_qadic_composite():
    """For q = 6 (composite), compute v_6(36) = 2."""
    x = QadicNumber(6, Fraction(36, 1))
    assert x.valuation == 2  # 36 = 6², v_6(36) = 2


def test_qadic_composite_numerator():
    """For q = 6, v_6(12) = 1 since 12 = 6·2."""
    x = QadicNumber(6, Fraction(12, 1))
    assert x.valuation == 1


def test_qadic_pi():
    """For transcendental q = π, v_π(r) = 0 for all non-zero rationals."""
    x = QadicNumber('pi', Fraction(100, 1))
    assert x.valuation == 0
    assert abs(x.norm() - 1.0) < 1e-15


def test_qadic_phi():
    """For q = φ (golden ratio), v(r) = 0 for rationals."""
    x = QadicNumber('phi', Fraction(5, 3))
    assert x.valuation == 0


def test_qadic_zero():
    """QadicNumber of zero should have infinite valuation, norm 0."""
    x = QadicNumber(2, 0)
    assert x.valuation == float('inf')
    assert x.norm() == 0.0


# ================================================================
#  Adele Tests
# ================================================================

def test_adele_product_formula_simple():
    """Product formula for q = 2/3: |2/3|_∞ · |2/3|_2 · |2/3|_3 = 1."""
    a = Adele.from_rational(Fraction(2, 3))
    result = a.norm_product()
    assert result == Fraction(1, 1), f"Got {result}, expected 1"


def test_adele_product_formula_integer():
    """Product formula for q = 12."""
    a = Adele.from_rational(12)
    assert a.norm_product() == Fraction(1, 1)


def test_adele_product_formula_one():
    """Product formula for q = 1."""
    a = Adele.from_rational(1)
    assert a.norm_product() == Fraction(1, 1)


def test_adele_product_formula_large():
    """Product formula for q = 144/625 (2⁴·3² / 5⁴)."""
    a = Adele.from_rational(Fraction(144, 625))
    assert a.norm_product() == Fraction(1, 1)


def test_adele_product_formula_zero():
    """Product formula for q = 0 should return 0."""
    a = Adele.from_rational(0)
    assert a.norm_product() == Fraction(0, 1)


def test_adele_product_formula_random():
    """Product formula verified for 100 random rationals."""
    random.seed(42)
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    passed = 0
    for _ in range(100):
        # Generate random rational with controlled factorization
        num = 1
        den = 1
        for p in primes:
            exp = random.randint(-3, 3)
            if exp > 0:
                num *= p ** exp
            elif exp < 0:
                den *= p ** (-exp)
        q = Fraction(num, den)
        a = Adele.from_rational(q)
        result = a.norm_product()
        if result == Fraction(1, 1):
            passed += 1
        else:
            print(f"  FAILED: q={q}, product={result}")
    assert passed == 100, f"{passed}/100 passed product formula"


def test_adele_real_norm():
    """The real component of an adele should be |q|_∞ = abs(q)."""
    a = Adele.from_rational(Fraction(-3, 7))
    assert a.real_norm == Fraction(3, 7)


def test_adele_components_count():
    """Adele should store components only for primes dividing num/den."""
    # 12/35 = 2²·3 / (5·7) → primes: 2, 3, 5, 7
    a = Adele.from_rational(Fraction(12, 35))
    assert set(a.components.keys()) == {2, 3, 5, 7}


# ================================================================
#  Run
# ================================================================

if __name__ == '__main__':
    import traceback

    tests = [
        # PadicNumber
        test_padic_construction_basic,
        test_padic_norm_of_one,
        test_padic_zero,
        test_padic_norm_multiplicativity,
        test_padic_valuation_additivity,
        test_padic_ultrametric_inequality,
        test_padic_arithmetic_add,
        test_padic_arithmetic_mul,
        test_padic_arithmetic_div,
        test_padic_arithmetic_sub,
        test_padic_negative,
        test_padic_large_valuation,
        test_padic_negative_valuation,
        test_padic_expansion_unit,
        test_padic_expansion_known,
        test_padic_different_primes_error,
        # QadicNumber
        test_qadic_prime_degenerate,
        test_qadic_composite,
        test_qadic_composite_numerator,
        test_qadic_pi,
        test_qadic_phi,
        test_qadic_zero,
        # Adele
        test_adele_product_formula_simple,
        test_adele_product_formula_integer,
        test_adele_product_formula_one,
        test_adele_product_formula_large,
        test_adele_product_formula_zero,
        test_adele_product_formula_random,
        test_adele_real_norm,
        test_adele_components_count,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
            print(f"  PASS {test.__name__}")
        except Exception as e:
            failed += 1
            print(f"  FAIL {test.__name__}: {e}")
            traceback.print_exc()

    print(f"\n{'='*50}")
    print(f"Results: {passed}/{passed + failed} tests passed")
    if failed == 0:
        print("ALL TESTS PASSED -- Validation Gate G1 satisfied")
    else:
        print(f"{failed} TEST(S) FAILED")
    print(f"{'='*50}")
