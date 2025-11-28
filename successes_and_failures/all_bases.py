"""Finding all bases, taking into account symmetries,
ins encodable and building up from cperms not contained in the class"""

from cayley_permutations import CayleyPermutation, Av
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from comb_spec_searcher import CombinatorialSpecificationSearcher
from tilescope import TileScopePack
import json
from check_regular_ins_enc import (
    regular_horizontal_insertion_encoding,
    regular_vertical_insertion_encoding,
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
    return sorted([frozenset(cperms), frozenset(b1), frozenset(b2), frozenset(b3)])


all_bases = set()
ins_enc_able_bases = set()
nomial_bases = set()

"""One size 3 pattern"""

for cperm in CayleyPermutation.of_size(3):
    basis = [cperm]
    basis_syms = sym_of_basis(basis)
    initial_basis = basis_syms[0]
    basis_syms = frozenset(set(basis_syms))
    if basis_syms in all_bases or basis_syms in ins_enc_able_bases:
        continue
    if any(
        regular_horizontal_insertion_encoding(b)
        or regular_vertical_insertion_encoding(b)
        for b in basis_syms
    ):
        ins_enc_able_bases.add(basis_syms)
        continue
    all_bases.add(basis_syms)
    nomial_bases.add(initial_basis)

print("Total bases found:", len(all_bases) + len(ins_enc_able_bases))
print("Insertion encodable bases found:", len(ins_enc_able_bases))
print("Non-insertion encodable bases found:", len(all_bases))

for basis in nomial_bases:
    print(Av(list(basis)))

"""All bases with only size 3 patterns"""

for _ in range(16):
    new_nomial_bases = set()
    for basis in nomial_bases:
        for cperm in Av(list(basis)).generate_cperms(3):
            new_basis = list(basis) + [cperm]
            basis_syms = sym_of_basis(new_basis)
            initial_basis = basis_syms[0]
            basis_syms = frozenset(set(basis_syms))
            if basis_syms in all_bases or basis_syms in ins_enc_able_bases:
                continue
            if any(
                regular_horizontal_insertion_encoding(b)
                or regular_vertical_insertion_encoding(b)
                for b in basis_syms
            ):
                ins_enc_able_bases.add(basis_syms)
                continue
            all_bases.add(basis_syms)
            new_nomial_bases.add(initial_basis)
    nomial_bases.update(new_nomial_bases)


# with open(f"all_basis_classes_3s.txt", "w") as f:
#     f.write(repr(all_bases))

"""Bases from before with one size 4 pattern"""

new_nomial_bases = set()
bases_with_size_4s = set()
ins_enc_able_bases_with_size_4s = set()


for basis in nomial_bases:
    for cperm in Av(list(basis)).generate_cperms(4):
        new_basis = list(basis) + [cperm]
        basis_syms = sym_of_basis(new_basis)
        initial_basis = basis_syms[0]
        basis_syms = frozenset(set(basis_syms))
        if basis_syms in all_bases or basis_syms in ins_enc_able_bases:
            continue
        if any(
            regular_horizontal_insertion_encoding(b)
            or regular_vertical_insertion_encoding(b)
            for b in basis_syms
        ):
            # ins_enc_able_bases.add(basis_syms)
            ins_enc_able_bases_with_size_4s.add(basis_syms)
            continue
        # all_bases.add(basis_syms)
        new_nomial_bases.add(initial_basis)
        bases_with_size_4s.add(basis_syms)
nomial_bases.update(new_nomial_bases)

print(
    "Total bases found:", len(bases_with_size_4s) + len(ins_enc_able_bases_with_size_4s)
)
print("Insertion encodable bases found:", len(ins_enc_able_bases_with_size_4s))
print("Non-insertion encodable bases found:", len(bases_with_size_4s))

# with open(f"all_basis_classes_3s_4x1.txt", "w") as f:
#     f.write(repr(bases_with_size_4s))


"""With two size 4s"""
new_nomial_bases = set()
bases_with_2size_4s = set()
ins_enc_able_bases_with_2size_4s = set()

for basis in nomial_bases:
    for cperm in Av(list(basis)).generate_cperms(4):
        new_basis = list(basis) + [cperm]
        basis_syms = sym_of_basis(new_basis)
        initial_basis = basis_syms[0]
        basis_syms = frozenset(set(basis_syms))
        if basis_syms in all_bases or basis_syms in ins_enc_able_bases:
            continue
        if any(
            regular_horizontal_insertion_encoding(b)
            or regular_vertical_insertion_encoding(b)
            for b in basis_syms
        ):
            # ins_enc_able_bases.add(basis_syms)
            ins_enc_able_bases_with_2size_4s.add(basis_syms)
            continue
        # all_bases.add(basis_syms)
        new_nomial_bases.add(initial_basis)
        bases_with_2size_4s.add(basis_syms)
nomial_bases.update(new_nomial_bases)
