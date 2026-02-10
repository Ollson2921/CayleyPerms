"""Simplifies a string of Cayley permutations intended to be used as a basis and returns a set."""

import re
from typing import Iterable

from .cayley import CayleyPermutation


def as_zero_based(
    patts: tuple[CayleyPermutation, ...],
) -> tuple[CayleyPermutation, ...]:
    """Turns a tuple of Cayley permutations which are one based or
    zero based into zero based Cayley permutations.
    Raises an error if the input is not a valid one based or zero
    based Cayley permutation."""
    all_cperms = []
    for cperm in patts:
        if cperm.is_cayley_perm():
            all_cperms.append(cperm)
        else:
            one_based_cperm = CayleyPermutation.from_one_based(cperm)
            if one_based_cperm.is_cayley_perm():
                all_cperms.append(one_based_cperm)
            else:
                raise ValueError(f"The input {cperm} is not a Cayley permutation")
    return tuple(all_cperms)


def string_to_cperms(patts: str) -> tuple[CayleyPermutation, ...]:
    """
    Construct a tuple of Cayley permutations from a string.

    It can be either 0 or 1 based and seperated by anything.
    """
    return as_zero_based(
        tuple(map(CayleyPermutation.standardise, re.findall(r"\d+", patts)))
    )


def minimise(patts: Iterable[CayleyPermutation]) -> tuple[CayleyPermutation, ...]:
    """
    Returns the minimal Cayley permutations.
    """
    patts = sorted(patts, key=len)
    if not patts:
        return tuple()
    simplified_basis: list[CayleyPermutation] = []
    for cperm in patts:
        if cperm.avoids(simplified_basis):
            simplified_basis.append(cperm)
    return tuple(simplified_basis)


def string_to_basis(patts: str) -> tuple[CayleyPermutation, ...]:
    """
    Return the minimal patts inputted as a string.
    """
    return minimise(string_to_cperms(patts))


def lex_min(patts: Iterable[CayleyPermutation]):
    """Finds the lexicographically minimal tuple of Cayley permutations among
    the input and its reverse, complement and reverse complement."""
    basis = tuple(sorted(patts))
    return min(
        basis,
        tuple(sorted(map(CayleyPermutation.reverse, basis))),
        tuple(sorted(map(CayleyPermutation.complement, basis))),
        tuple(sorted(map(CayleyPermutation.reverse_complement, basis))),
    )
