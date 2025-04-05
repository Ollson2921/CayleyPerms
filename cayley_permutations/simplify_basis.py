"""Simplifies a string of Cayley permutations intended to be used as a basis and returns a set."""

from .cayley import CayleyPermutation
from typing import Tuple
import re


def string_to_basis(patts: str) -> Tuple[CayleyPermutation, ...]:
    """Construct a basis from a string. It can be either 0 or 1 based and seperated by anything.
    Then simplifies basis by removing any Cayley permutations which are contained in another Cayley
    permutation in the basis."""
    as_cperms = tuple(map(CayleyPermutation.standardise, re.findall(r"\d+", patts)))

    min_length = min(len(cperm) for cperm in as_cperms)
    simplified_basis = set([cperm for cperm in as_cperms if len(cperm) == min_length])
    remaining_cperms = sorted(
        set([cperm for cperm in as_cperms if len(cperm) != min_length]), key=len
    )
    for cperm in remaining_cperms:
        if not cperm.contains(simplified_basis):
            simplified_basis.add(cperm)
    return simplified_basis
