"""Simplifies a string of Cayley permutations intended to be used as a basis and returns a set."""

from .cayley import CayleyPermutation
from typing import Iterable
import re


def string_to_perms(patts: str) -> tuple[CayleyPermutation, ...]:
    """
    Construct a tuple of Cayley permutations from a string.

    It can be either 0 or 1 based and seperated by anything.
    """
    return tuple(map(CayleyPermutation.standardise, re.findall(r"\d+", patts)))


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
    return minimise(string_to_perms(patts))
