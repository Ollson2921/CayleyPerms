from cayley_permutations import CayleyPermutation
from typing import Iterable


def lex_min(patts: Iterable[CayleyPermutation]):
    basis = tuple(sorted(patts))
    return min(
        basis,
        tuple(sorted(map(CayleyPermutation.reverse, basis))),
        tuple(sorted(map(CayleyPermutation.complement, basis))),
        tuple(sorted(map(CayleyPermutation.reverse_complement, basis))),
    )


def complement(cperm: CayleyPermutation) -> CayleyPermutation:
    """returns the complement of the cperm"""
    n = len(cperm)
    m = max(cperm)
    return CayleyPermutation(tuple(m - cperm[i] for i in range(n)))


def symmetries(cperm: CayleyPermutation) -> frozenset[CayleyPermutation]:
    """returns the list of symmetries of the cperm"""
    return list(
        frozenset(
            [cperm, complement(cperm), cperm.reverse(), complement(cperm.reverse())]
        )
    )


def sym_of_basis(cperms: list[CayleyPermutation]) -> list[frozenset[CayleyPermutation]]:
    """returns the list of symmetries of the list of cperms"""
    b1 = []
    b2 = []
    b3 = []
    for cperm in cperms:
        b1.append(cperm.reverse())
        b2.append(complement(cperm))
        b3.append(complement(cperm.reverse()))
    return sorted(
        [frozenset(cperms), frozenset(b1), frozenset(b2), frozenset(b3)],
        key=lambda x: (len(x), x),
        # key=lambda x: sorted(list(x))[0],
    )
