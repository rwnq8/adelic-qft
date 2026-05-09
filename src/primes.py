#!/usr/bin/env python3
"""Shared prime number utilities.
Centralized deduplication of primality checks and prime generation
from padic.py, qadic.py, adelic_product.py, padic_gamma.py.
Used by: All modules that need prime lists or primality tests.
"""

import math


def is_prime(n):
    """Test whether n is a prime number.
    
    Args:
        n (int): Integer to test.
    Returns:
        bool: True if n is prime (or 2), False otherwise.
    """
    if not isinstance(n, int) or n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for d in range(3, int(n ** 0.5) + 1, 2):
        if n % d == 0:
            return False
    return True


def primes_up_to(limit):
    """Generate all primes ≤ limit using simple trial division.
    
    For limits < 10^6 this is fast enough. For larger limits,
    use a sieve or the primesieve library.
    
    Args:
        limit (int): Upper bound (inclusive).
    Returns:
        list: Primes ≤ limit, in ascending order.
    """
    if limit < 2:
        return []
    result = [2]
    for n in range(3, limit + 1, 2):
        if is_prime(n):
            result.append(n)
    return result


def prime_factors(n):
    """Return sorted list of prime factors of n (with multiplicity).
    
    Args:
        n (int): Integer to factor.
    Returns:
        list: Prime factors in ascending order, with repetitions.
    """
    if n < 2:
        return []
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1 if d == 2 else 2  # check 2 once, then odd numbers
    if n > 1:
        factors.append(n)
    return factors
