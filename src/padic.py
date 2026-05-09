#!/usr/bin/env python3
"""
Module M1: Foundational Library
File: src/padic.py — PadicNumber class
Associated document: 1.1.md (Definitive Research Plan, M1 specification)
Report: module_01_report.md
Author: LLM agent (DeepSeek V4)
Date: 2026-05-09

Implements p-adic numbers for a fixed prime p. A p-adic number is represented
as a rational number q together with its p-adic valuation, norm, and unit part.
All arithmetic is exact via Python's Fraction.
"""

from fractions import Fraction
from math import gcd as _gcd


class PadicNumber:
    """A rational number viewed through its p-adic completion.

    For a fixed prime p, each non-zero rational q can be uniquely written as
        q = p^v · u
    where v = v_p(q) ∈ ℤ is the p-adic valuation and u is a p-adic unit
    (numerator and denominator not divisible by p).

    Attributes:
        p (int): The prime.
        q (Fraction): The underlying rational number.
        _v (int | float): Valuation v_p(q), or float('inf') for zero.
        _u (Fraction): The unit part u = q · p^{-v}.
    """

    __slots__ = ('p', 'q', '_v', '_u')

    def __init__(self, prime, rational):
        if not isinstance(prime, int) or prime < 2:
            raise ValueError(f"prime must be integer ≥ 2, got {prime}")
        # Verify primality (basic check — sufficient for small primes used in this project)
        if prime > 2:
            for d in range(2, int(prime ** 0.5) + 1):
                if prime % d == 0:
                    raise ValueError(f'prime must be prime, got composite {prime}')

        self.p = prime
        self.q = Fraction(rational)

        if self.q == 0:
            self._v = float('inf')
            self._u = Fraction(0, 1)
            return

        # Compute v_p(q): count factors of p in numerator and denominator
        num = self.q.numerator
        den = self.q.denominator

        # Handle signs: valuation only depends on absolute value
        num = abs(num)

        v_num = 0
        while num % prime == 0:
            num //= prime
            v_num += 1

        v_den = 0
        while den % prime == 0:
            den //= prime
            v_den += 1

        self._v = v_num - v_den

        # Unit part: q · p^{-v}
        # This is the unique p-adic unit satisfying q = p^v · u
        self._u = Fraction(self.q.numerator, self.q.denominator) * Fraction(prime) ** (-self._v)

    # ── Properties ──────────────────────────────────────────────

    @property
    def valuation(self):
        """Return v_p(q) — the exponent of p in the prime factorization.

        Returns float('inf') for the zero element.
        """
        return self._v

    def norm(self):
        """Return the p-adic norm |q|_p = p^{-v_p(q)} as an exact Fraction.

        Returns Fraction(0, 1) for the zero element.
        """
        if self._v == float('inf'):
            return Fraction(0, 1)
        if self._v >= 0:
            return Fraction(1, self.p ** self._v)
        else:
            return Fraction(self.p ** (-self._v), 1)

    def norm_float(self):
        """Return |q|_p as a float (for display/convenience)."""
        if self._v == float('inf'):
            return 0.0
        return float(self.p) ** (-self._v)

    @property
    def unit(self):
        """Return the unit part u = q · p^{-v_p(q)} as a Fraction."""
        return self._u

    # ── Arithmetic ──────────────────────────────────────────────

    def __add__(self, other):
        if not isinstance(other, PadicNumber):
            return NotImplemented
        if self.p != other.p:
            raise ValueError(f"Primes differ: {self.p} ≠ {other.p}")
        return PadicNumber(self.p, self.q + other.q)

    def __radd__(self, other):
        if other == 0:
            return self
        return NotImplemented

    def __sub__(self, other):
        if not isinstance(other, PadicNumber):
            return NotImplemented
        if self.p != other.p:
            raise ValueError(f"Primes differ: {self.p} ≠ {other.p}")
        return PadicNumber(self.p, self.q - other.q)

    def __mul__(self, other):
        if not isinstance(other, PadicNumber):
            return NotImplemented
        if self.p != other.p:
            raise ValueError(f"Primes differ: {self.p} ≠ {other.p}")
        return PadicNumber(self.p, self.q * other.q)

    def __rmul__(self, other):
        if other == 1:
            return self
        return NotImplemented

    def __truediv__(self, other):
        if not isinstance(other, PadicNumber):
            return NotImplemented
        if self.p != other.p:
            raise ValueError(f"Primes differ: {self.p} ≠ {other.p}")
        if other.q == 0:
            raise ZeroDivisionError("division by zero in PadicNumber")
        return PadicNumber(self.p, self.q / other.q)

    def __neg__(self):
        return PadicNumber(self.p, -self.q)

    def __abs__(self):
        return self.norm()  # p-adic absolute value is the norm

    # ── Comparison ──────────────────────────────────────────────

    def __eq__(self, other):
        if not isinstance(other, PadicNumber):
            return NotImplemented
        return self.p == other.p and self.q == other.q

    def __hash__(self):
        return hash((self.p, self.q))

    # ── Representation ──────────────────────────────────────────

    def __repr__(self):
        if self._v == float('inf'):
            return f"PadicNumber(p={self.p}, q=0)"
        return (f"PadicNumber(p={self.p}, q={self.q}, "
                f"v={self._v}, |·|_p={self.norm()})")

    def __str__(self):
        if self._v == float('inf'):
            return f"0 (p={self.p})"
        sign = ""
        if self.q < 0:
            sign = "-"
        return f"{sign}p^{self._v} · {abs(self._u)} (p={self.p})"

    # ── Hensel expansion ────────────────────────────────────────

    def expansion(self, k):
        """Return the first k digits [a_0, a_1, …, a_{k-1}] of the
        Hensel expansion of the p-adic integer component.

        For |q|_p ≤ 1 (v_p ≥ 0):
            q = a_0 + a_1·p + a_2·p² + …    (0 ≤ a_i < p)

        For general q: returns expansion of p^{−v}·q (the shifted
        integer part) with a note about valuation.

        Returns:
            list[int]: k expansion digits (0 ≤ a_i < p).
        """
        if self._v == float('inf'):
            return [0] * k

        # Work with the unit part u (which is a p-adic unit: |u|_p = 1)
        # u = a_0 + a_1·p + a_2·p² + …  （Hensel expansion）
        u_num = self._u.numerator
        u_den = self._u.denominator

        digits = []
        rem_num = u_num
        rem_den = u_den

        for i in range(k):
            if rem_num == 0:
                digits.extend([0] * (k - i))
                break
            try:
                inv_den = pow(rem_den % self.p, -1, self.p)
            except ValueError:
                # Denominator is divisible by p — shouldn't happen for a unit
                digits.append(0)
                continue
            digit = (rem_num * inv_den) % self.p
            digits.append(digit)
            rem_num = (rem_num - digit * rem_den) // self.p

        return digits

    # ── Utility ─────────────────────────────────────────────────

    def is_unit(self):
        """Return True if |q|_p = 1 (i.e., q is a p-adic unit)."""
        return self._v == 0

    def is_integer(self):
        """Return True if |q|_p ≤ 1 (i.e., q is a p-adic integer)."""
        return self._v == float('inf') or self._v >= 0
