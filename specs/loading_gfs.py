from sympy import symbols, sqrt
from cayley_permutations import CayleyPermutation, Av
import json
from sympy.printing.latex import latex
from comb_spec_searcher import CombinatorialSpecification

x = symbols("x")

basis_desc = "3s"

with open(f"wilf_equivalence_classes_{basis_desc}.txt", "r") as f:
    gfs_dict = eval(f.readline())

no_gfs = [
    [1, 1, 3, 10, 37, 144, 585, 2450, 10506, 45899],
    [1, 1, 3, 11, 47, 211, 997, 4861, 24319, 124059],
    [1, 1, 3, 10, 38, 154, 654, 2871, 12925, 59345],
    [1, 1, 3, 10, 38, 154, 654, 2871, 12925, 59345],
    [1, 1, 3, 9, 30, 107, 399, 1537, 6069, 24434],
]

# for idx, counts in enumerate(gfs_dict.keys()):
#     if counts[1] in no_gfs:
#         print(f"Index {idx} of dict is same as {counts[1]} in no gf.")


"""Printing in the terminal"""
# for gf, bases in gfs_dict.items():
#     print("Generating function:")
#     print(gf[0])
#     print("Counts:")
#     print(gf[1])
#     # print("Number of bases in this class:", len(bases))
#     # print("Bases:")
#     for basis in bases:
#         basis_str = ", ".join(str(p) for p in basis)
#         print(f"Av({basis_str})")
#     print()

"""For latex, create the rows for a table
bases | gf | counts | oeis (blank)"""

# count = 0
# for gf, bases in gfs_dict.items():
#     count += 1
#     if 50 <= count:  # for only printing some of the output
#         str_gf = "$" + latex(gf[0]) + "$"
#         counts = gf[1]
#         print(
#             f"$\\{Av(bases[0])}$",
#             " & ",
#             str_gf,
#             " & ",
#             str(counts)[1:-1],
#             "& \\\\ \n",
#         )
#         for basis in bases[1:]:
#             # assert Av(basis).counter() == counts
#             print(f"$\\{Av(basis)}$", " &  &  &\\\\ \n")
#         print("\\hline\n")


# with open("took_too_long_3s.txt", "r") as f:
#     bases = eval(f.readline())

# for basis in bases:
#     print(Av(basis))
#     with open(
#         f"{basis_desc}/no fusion/{Av(basis)}_point_placement.json",
#         "r",
#     ) as f:
#         spec = json.load(f)
#     spec = CombinatorialSpecification.from_dict(spec)
#     counts = [spec.count_objects_of_size(n) for n in range(10)]
#     print(counts)
