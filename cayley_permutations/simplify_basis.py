"""Simplifies a list of Cayley permutations intended to be used as a basis."""

from .cayley import CayleyPermutation
from typing import Iterable, List


def simplify_basis(basis: Iterable[CayleyPermutation]) -> List[CayleyPermutation]:
    """Simplifies a list of Cayley permutations intended to be used as a basis
    by removing any Cayley permutations which are contained in another Cayley
    permutation in the basis."""
    min_length = min(len(cperm) for cperm in basis)
    simplified_basis = set([cperm for cperm in basis if len(cperm) == min_length])
    remaining_cperms = sorted(
        set([cperm for cperm in basis if len(cperm) != min_length]), key=len
    )
    for cperm in remaining_cperms:
        if not cperm.contains(simplified_basis):
            simplified_basis.add(cperm)
    return simplified_basis
