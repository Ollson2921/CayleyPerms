"""For finding the total number of bases, number of symmetry classes,
and how many symmetry classes are insertion encodable or not."""

from cayley_permutations import CayleyPermutation, Av
from cayley_permutations.simplify_basis import minimise
from useful_functions import lex_min, sym_of_basis
from typing import Iterable
from itertools import combinations, permutations
from check_regular_ins_enc import (
    regular_horizontal_insertion_encoding,
    regular_vertical_insertion_encoding,
)

"""Taking into account symmetries"""

all_bases = set()
initial_basis = set()
ins_enc_bases = set()
non_ins_enc_bases = set()
non_ins_enc_bases_lex_min = set()
all_bases_in_classes = set()
for n in range(1, 20):
    for basis in combinations(CayleyPermutation.of_size(3), n):
        basis = lex_min(minimise(set(basis)))
        basis_syms = sym_of_basis(basis)
        basis_syms = frozenset(set(basis_syms))
        if basis_syms in all_bases:
            continue
        if any(
            regular_horizontal_insertion_encoding(b)
            or regular_vertical_insertion_encoding(b)
            for b in basis_syms
        ):
            ins_enc_bases.add(basis_syms)
        else:
            non_ins_enc_bases.add(basis_syms)
            non_ins_enc_bases_lex_min.add(basis)
        all_bases.add(basis_syms)
        initial_basis.add(basis)
        for b in basis_syms:
            all_bases_in_classes.add(frozenset(set(b)))

print("Total bases found 3s:", len(all_bases))
print("Insertion encodable bases found:", len(ins_enc_bases))
print("Non-insertion encodable bases found:", len(non_ins_enc_bases))
print("Non-insertion encodable bases lex min found:", len(non_ins_enc_bases_lex_min))
print("All bases in classes found:", len(all_bases_in_classes))


with open(f"all_non_inenc_basis_classes_3s.txt", "w") as f:
    f.write(repr(non_ins_enc_bases_lex_min))

with_size_4s = set()
initial_basis_with_4s = set()
new_ins_enc_bases = set()
new_non_ins_enc_bases = set()
new_non_ins_enc_bases_lex_min = set()
new_all_bases_in_classes = set()
for basis in initial_basis:
    for cperm in CayleyPermutation.of_size(4):
        new_basis = lex_min(minimise(set(list(basis) + [cperm])))
        basis_syms = sym_of_basis(new_basis)
        basis_syms = frozenset(set(basis_syms))
        if basis_syms in all_bases or basis_syms in with_size_4s:
            continue
        if any(
            regular_horizontal_insertion_encoding(b)
            or regular_vertical_insertion_encoding(b)
            for b in basis_syms
        ):
            new_ins_enc_bases.add(basis_syms)
        else:
            new_non_ins_enc_bases.add(basis_syms)
            new_non_ins_enc_bases_lex_min.add(new_basis)
        with_size_4s.add(basis_syms)
        initial_basis_with_4s.add(new_basis)
        for b in basis_syms:
            new_all_bases_in_classes.add(frozenset(set(b)))


print("\nTotal bases found 3s_4x1:", len(with_size_4s))
print("Insertion encodable bases found:", len(new_ins_enc_bases))
print("Non-insertion encodable bases found:", len(new_non_ins_enc_bases))
print(
    "Non-insertion encodable bases lex min found:", len(new_non_ins_enc_bases_lex_min)
)
print("All bases in classes found:", len(new_all_bases_in_classes))


with open(f"all_non_inenc_basis_classes_3s_4x1.txt", "w") as f:
    f.write(repr(new_non_ins_enc_bases_lex_min))
