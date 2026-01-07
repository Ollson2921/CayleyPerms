from typing import Iterable
from cayley_permutations.simplify_basis import lex_min
from cayley_permutations import CayleyPermutation, Av
from itertools import combinations


def all_subsets_of_size_n_cayley_perms(n: int) -> set[tuple[CayleyPermutation, ...]]:
    bases = set()
    cperms = CayleyPermutation.of_size(n)
    for i in range(len(cperms) + 1):
        for basis in combinations(cperms, i):
            bases.add(lex_min(basis))
    return bases


def n_by_m_etc(sizes: Iterable[tuple[int, int]]) -> set[tuple[CayleyPermutation, ...]]:
    """
    Pass a list of tuples with (size, amount) to create bases.
    E.g, 2x4_3x5 is n_by_m_etc([(2, 4), (3, 5)])
    """
    sizes = sorted(sizes, key=lambda x: (x[1], x[0]))
    assert len(set(x[1] for x in sizes)) == len(sizes), "size given more than once"
    bases = {tuple()}
    for n, m in sizes:
        new_bases = set()
        for basis in bases:
            cperms = Av(basis).generate_cperms(m)
            for new_bit in combinations(cperms, n):
                new_bases.add(lex_min(basis + new_bit))
        bases = new_bases
    return bases


if __name__ == "__main__":
    print(n_by_m_etc([(1, 2), (1, 3)]))
    print(all_subsets_of_size_n_cayley_perms(2))
