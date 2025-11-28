"""sorting all bases into a file of success and a file of failures"""

from cayley_permutations import CayleyPermutation, Av
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from comb_spec_searcher import CombinatorialSpecificationSearcher
from tilescope import TileScopePack
import json


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


basis_desc = "3s_4x1"  # change descriptor to change file
# basis_desc = "3s"

with open(f"all_basis_classes_{basis_desc}.txt", "r") as f:
    all_bases_classes = eval(f.readline())

with open(f"successes_{basis_desc}.txt", "r") as f:
    successes = eval(f.readline())
success_classes = set(
    [frozenset(set(sym_of_basis(list(basis)))) for basis in successes]
)
print("successes loaded:")
print(len(successes))
print("success classes:")
print(len(success_classes))

with open(f"failures_{basis_desc}.txt", "r") as f:
    failures = eval(f.readline())
failure_classes = set([frozenset(set(sym_of_basis(list(basis)))) for basis in failures])
print("failures loaded:")
print(len(failures))
print("failure classes:")
print(len(failure_classes))

actual_successes = []
actual_failures = []
not_computed = []

for basis in all_bases_classes:
    if basis in success_classes:
        actual_successes.append(basis)
    elif basis in failure_classes:
        actual_failures.append(basis)
    else:
        not_computed.append(basis)


print("successes:", len(set(actual_successes)))
print("total failures:", len(set(actual_failures)))
print("not computed:", len(set(not_computed)))

print(len(set(actual_successes)) + len(set(actual_failures)))
print(len(set(all_bases_classes)))


with open(f"actual_successes_{basis_desc}.txt", "w") as f:
    f.write(repr(actual_successes))

with open(f"actual_failures_{basis_desc}.txt", "w") as f:
    f.write(repr(actual_failures))

with open(f"to_compute_{basis_desc}.txt", "w") as f:
    f.write(repr(not_computed))
