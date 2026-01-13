"""Looking at which bases succeeded."""

from cayley_permutations import CayleyPermutation, Av
import json
from itertools import combinations

basis_desc = "3s_4x1"  # change descriptor to change file
basis_desc = "3s"

print(basis_desc)

with open(f"successes_{basis_desc}.txt", "r") as f:
    successes = eval(f.readline())

with open(f"failures_{basis_desc}.txt", "r") as f:
    failures = eval(f.readline())

print(len(successes), "successes")
print(len(failures), "failures")

"""Looking for containment of perms"""
# def is_perm(cperm: CayleyPermutation) -> bool:
#     """returns True if the cperm is a perm"""
#     for i in range(len(cperm)):
#         for j in range(i + 1, len(cperm)):
#             if cperm[i] == cperm[j]:
#                 return False
#     return True


# yes = []
# no = []
# for basis in failures:
#     if all(is_perm(cperm) for cperm in basis):
#         yes.append(basis)
#         print(Av(basis))
#     else:
#         no.append(basis)

# print("has perms:", len(yes))
# print("has no perms:", len(no))

"""Ordering bases by length"""
# for basis in sorted(failures, key=lambda x: (len(x), x)):
#     print(Av(basis))

"""Looking at which size 3s are contained in all successes/failures"""
# for cperms in combinations(CayleyPermutation.of_size(3), 6):
#     if all(any(cperm in basis for cperm in cperms) for basis in successes):
#         print(f"All successes contain one of {cperms}")
#     if all(any(cperm in basis for cperm in cperms) for basis in failures):
#         print(f"All failures contain one of {cperms}")

"""comparing with species"""


def complement(cperm: CayleyPermutation) -> CayleyPermutation:
    """returns the complement of the cperm"""
    n = len(cperm)
    m = max(cperm)
    return CayleyPermutation(tuple(m - cperm[i] for i in range(n)))


def symmetries(cperm: CayleyPermutation) -> list[CayleyPermutation]:
    """returns the list of symmetries of the cperm"""
    return list(
        set([cperm, complement(cperm), cperm.reverse(), complement(cperm.reverse())])
    )


def sym_of_list(cperms: list[CayleyPermutation]) -> list[CayleyPermutation]:
    """returns the list of symmetries of the list of cperms"""
    syms = set()
    for cperm in cperms:
        syms.update(symmetries(cperm))
    return list(syms)


# yes = []
# no = []
# for basis in failures:
#     cperms = [
#         CayleyPermutation((1, 0, 1)),
#         CayleyPermutation((0, 1, 1)),
#         CayleyPermutation((0, 0, 0)),
#         CayleyPermutation((2, 1, 0)),
#     ]
#     if any(s in basis for s in sym_of_list(cperms)):
#         yes.append(basis)
#     else:
#         no.append(basis)
#         print(Av(basis))

# print("contains:", len(yes))
# print("doesn't contain:", len(no))
