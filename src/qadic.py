#!/usr/bin/env python3
"""
Module M1: Foundational Library
File: src/qadic.py — QadicNumber class (generalized scaling ratio)
Associated document: 1.1.md (Definitive Research Plan, M1 specification)

Generalizes p-adic numbers to arbitrary scaling ratios q.
For q = p (prime), this degenerates to PadicNumber.
For integer q, valuation is computed via prime factorization.
For rational q = a/b, valuation counts powers of the ratio.
For transcendental q (π, e, φ), all non-zero rationals have valuation 0.
"""

from fractions import Fraction
from math import isclose
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from padic import PadicNumber


class QadicNumber:
    """A rational number viewed through a generalized q-adic valuation.

    For a scaling ratio q > 1, the q-adic valuation v_q(r) measures how
    many powers of q "divide" the rational r.

    Attributes:
        q_val (float | Fraction): The scaling ratio.
        rational (Fraction): The underlying rational number.
        _v (float): Valuation v_q(r), or float('inf') for zero.
        _is_prime (bool): True if q is an integer prime (degenerate case).
    """

    __slots__ = ('q_val', 'rational', '_v', '_is_prime', '_padic')

    def __init__(self, ratio, rational):
        """Initialize a q-adic number.

        Args:
            ratio: Scaling ratio (int, float, Fraction, or str like 'pi','e','phi').
                   Must be > 1.
            rational: The rational number (int, Fraction, or float).
        """
        self.rational = Fraction(rational)

        # Parse ratio
        if isinstance(ratio, str):
            ratio_map = {'pi': 3.141592653589793, 'e': 2.718281828459045,
                        'phi': 1.618033988749895, 'golden': 1.618033988749895}
            if ratio.lower() in ratio_map:
                self.q_val = ratio_map[ratio.lower()]
            else:
                raise ValueError(f"Unknown symbolic ratio: {ratio}")
        else:
            self.q_val = float(ratio) if not isinstance(ratio, Fraction) else ratio

        if float(self.q_val) <= 1:
            raise ValueError(f"Scaling ratio must be > 1, got {self.q_val}")

        # Check if q is an integer prime (degenerate to PadicNumber)
        self._is_prime = False
        if isinstance(self.q_val, (int, float)) and self.q_val == int(self.q_val):
            q_int = int(self.q_val)
            if q_int >= 2 and self.is_prime(q_int):
                self._is_prime = True
                self._padic = PadicNumber(q_int, self.rational)

        # Compute valuation
        if self.rational == 0:
            self._v = float('inf')
        elif self._is_prime:
            self._v = self._padic.valuation
        elif isinstance(self.q_val, (int, float)) and self.q_val == int(self.q_val):
            self._v = self._compute_integer_q_valuation(int(self.q_val))
        else:
            # For non-integer q (transcendental, rational fraction, etc.):
            # v_q(r) = 0 for all non-zero rationals r
            # This is because transcendental/fractional "bases" don't divide rationals
            self._v = 0

    @staticmethod
    
    def _compute_integer_q_valuation(self, q):
        """Compute v_q(r) for integer q (possibly composite).

        For composite q with prime factorization q = ∏ p_i^{e_i}:
        v_q(r) = min_i ⌊v_{p_i}(r) / e_i⌋
        """
        if q == 1:
            return float('inf') if self.rational == 0 else 0

        # Factor q into primes
        factors = {}
        n = q
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors[d] = factors.get(d, 0) + 1
                n //= d
            d += 1
        if n > 1:
            factors[n] = factors.get(n, 0) + 1

        # For each prime factor p_i with exponent e_i,
        # compute v_{p_i}(r) and divide by e_i
        num = self.rational.numerator
        den = self.rational.denominator

        min_val = float('inf')
        for p, e in factors.items():
            # v_p(r)
            n_copy = abs(num)
            v_num = 0
            while n_copy % p == 0:
                n_copy //= p
                v_num += 1
            d_copy = den
            v_den = 0
            while d_copy % p == 0:
                d_copy //= p
                v_den += 1
            v_p = v_num - v_den
            v_q_for_p = v_p // e
            min_val = min(min_val, v_q_for_p)

        return min_val if min_val != float('inf') else 0

    # ── Properties ──────────────────────────────────────────────

    @property
    def valuation(self):
        """Return v_q(r) — the q-adic valuation."""
        return self._v

    def norm(self):
        """Return the q-adic norm |r|_q = q^{-v_q(r)} as a float.

        Returns 0.0 for the zero element.
        Returns exactly 1.0 for q-adic units (valuation 0).
        """
        if self._v == float('inf'):
            return 0.0
        return float(self.q_val) ** (-self._v)

    @property
    def is_unit(self):
        """Return True if |r|_q = 1."""
        return self._v == 0

    @property
    def is_prime_case(self):
        """Return True if this is a standard p-adic number (q is prime)."""
        return self._is_prime

    # ── Arithmetic ──────────────────────────────────────────────

    def __add__(self, other):
        if not isinstance(other, QadicNumber):
            return NotImplemented
        if self.q_val != other.q_val:
            raise ValueError(f"Scaling ratios differ: {self.q_val} ≠ {other.q_val}")
        return QadicNumber(self.q_val, self.rational + other.rational)

    def __sub__(self, other):
        if not isinstance(other, QadicNumber):
            return NotImplemented
        if self.q_val != other.q_val:
            raise ValueError(f"Scaling ratios differ: {self.q_val} ≠ {other.q_val}")
        return QadicNumber(self.q_val, self.rational - other.rational)

    def __mul__(self, other):
        if not isinstance(other, QadicNumber):
            return NotImplemented
        if self.q_val != other.q_val:
            raise ValueError(f"Scaling ratios differ: {self.q_val} ≠ {other.q_val}")
        return QadicNumber(self.q_val, self.rational * other.rational)

    def __truediv__(self, other):
        if not isinstance(other, QadicNumber):
            return NotImplemented
        if self.q_val != other.q_val:
            raise ValueError(f"Scaling ratios differ: {self.q_val} ≠ {other.q_val}")
        if other.rational == 0:
            raise ZeroDivisionError("division by zero")
        return QadicNumber(self.q_val, self.rational / other.rational)

    # ── Comparison ──────────────────────────────────────────────

    def __eq__(self, other):
        if not isinstance(other, QadicNumber):
            return NotImplemented
        return (self.q_val == other.q_val and self.rational == other.rational)

    def __hash__(self):
        return hash((self.q_val, self.rational))

    # ── Representation ──────────────────────────────────────────

    def __repr__(self):
        if self._v == float('inf'):
            return f"QadicNumber(q={self.q_val}, r=0)"
        return (f"QadicNumber(q={self.q_val}, r={self.rational}, "
                f"v={self._v})")

    def __str__(self):
        if self._v == float('inf'):
            return f"0 (q={self.q_val})"
        return f"{self.rational} (q={self.q_val}, v={self._v})"
