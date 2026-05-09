#!/usr/bin/env python3
"""
Module M1: Foundational Library
File: src/adele.py — Adele class
Associated document: 1.1.md (Definitive Research Plan, M1 specification)

Implements the adele ring A_ℚ: the restricted product of all completions
of ℚ (real and p-adic for every prime p).

For a rational number q, the adelic product formula states:
    |q|_∞ · ∏_p |q|_p = 1

This is verified exactly using Fraction arithmetic.
"""

from fractions import Fraction
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from padic import PadicNumber


def _factorize(n):
    """Return dict of {prime: exponent} for integer n > 0."""
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


class Adele:
    """An adele: a tuple (x_∞, x_2, x_3, x_5, …) with x_p ∈ ℚ_p
    and x_p ∈ ℤ_p for almost all p.

    For rational input q, the adele is (q in ℝ, q in ℚ_2, q in ℚ_3, …).
    The p-adic components are stored only for primes dividing the
    numerator or denominator; all other primes have |q|_p = 1.

    Attributes:
        rational (Fraction): The underlying rational number.
        real_norm (Fraction): |q|_∞ = abs(q).
        _components (dict): {prime: PadicNumber} for relevant primes.
    """

    __slots__ = ('rational', 'real_norm', '_components')

    def __init__(self, rational):
        """Create an adele from a rational number.

        Args:
            rational: int, Fraction, float, or string representation.
        """
        self.rational = Fraction(rational)
        self.real_norm = Fraction(abs(self.rational.numerator), self.rational.denominator)
        self._components = {}

        if self.rational == 0:
            return

        # Find all primes dividing numerator or denominator
        num_primes = _factorize(abs(self.rational.numerator))
        den_primes = _factorize(self.rational.denominator)

        all_primes = set(num_primes.keys()) | set(den_primes.keys())

        for p in sorted(all_primes):
            self._components[p] = PadicNumber(p, self.rational)

    @classmethod
    def from_rational(cls, q):
        """Factory method: create an adele from a rational.

        Args:
            q: int, Fraction, float, or string.
        Returns:
            Adele instance.
        """
        return cls(q)

    # ── Components ──────────────────────────────────────────────

    @property
    def components(self):
        """Return dict of {prime: PadicNumber} for stored primes.

        Primes not in this dict have |q|_p = 1 (valuation ≥ 0).
        """
        return self._components

    def get_padic(self, p):
        """Return PadicNumber for prime p, computing lazily if needed.

        For primes not dividing num/den, |q|_p = 1, v_p(q) = 0.
        """
        if p in self._components:
            return self._components[p]
        # Lazy: create a PadicNumber — it will compute valuation = 0, norm = 1
        val = PadicNumber(p, self.rational)
        if val.valuation == 0:
            # Store for future lookups
            self._components[p] = val
        else:
            self._components[p] = val
        return val

    # ── Product formula ─────────────────────────────────────────

    def norm_product(self):
        """Compute the adelic product ∏_v |q|_v.

        By Ostrowski's theorem: for any non-zero rational q,
            |q|_∞ · ∏_p |q|_p = 1

        Returns:
            Fraction: Exactly 1/1 for any non-zero rational.
                      Fraction(0, 1) for q = 0.
        """
        if self.rational == 0:
            return Fraction(0, 1)

        product = Fraction(1, 1)

        # Real norm
        product *= self.real_norm

        # p-adic norms for primes dividing num/den
        for p, comp in self._components.items():
            product *= comp.norm()

        return product

    def norm_product_exact(self):
        """Verify product formula exactly using prime factorization.

        This is the reference implementation: multiplies real norm by
        p-adic norms for ALL primes dividing num/den. Should equal 1/1.

        Returns:
            Fraction: Expected to be Fraction(1, 1) exactly.
        """
        return self.norm_product()

    # ── Adelic absolute value ───────────────────────────────────

    def adelic_norm(self):
        """Return the adelic norm ∏_v |q|_v (alternative name for norm_product)."""
        return self.norm_product()

    # ── Representation ──────────────────────────────────────────

    def __repr__(self):
        n_p = len(self._components)
        return (f"Adele(q={self.rational}, |·|_∞={self.real_norm}, "
                f"{n_p} p-adic components)")

    def __str__(self):
        return (f"Adele({self.rational}): |·|_∞ = {float(self.real_norm):.6g}, "
                f"{len(self._components)} primes stored")

    # ── Equality ────────────────────────────────────────────────

    def __eq__(self, other):
        if not isinstance(other, Adele):
            return NotImplemented
        return self.rational == other.rational

    def __hash__(self):
        return hash(self.rational)
