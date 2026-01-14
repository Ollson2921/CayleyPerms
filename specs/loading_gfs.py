from sympy import symbols, sqrt
from cayley_permutations import CayleyPermutation, Av
import json
from comb_spec_searcher import CombinatorialSpecification

# x = symbols("x")

basis_desc = "3s"

# with open("wilf_equivalence_classes_3s.txt", "r") as f:
#     gfs_dict = eval(f.readline())

# for gf, bases in gfs_dict.items():
#     print("Generating function:", gf)
#     print("Number of bases in this class:", len(bases))
#     print("Bases:")
#     for basis in bases:
#         basis_str = ", ".join(str(p) for p in basis)
#         print(f"Av({basis_str})")
#     print()


with open("took_too_long_3s.txt", "r") as f:
    bases = eval(f.readline())

for basis in bases:
    print(Av(basis))
    with open(
        f"{basis_desc}/no fusion/{Av(basis)}_point_placement.json",
        "r",
    ) as f:
        spec = json.load(f)
    spec = CombinatorialSpecification.from_dict(spec)
    counts = [spec.count_objects_of_size(n) for n in range(10)]
    print(counts)
