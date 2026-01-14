from sympy import symbols, sqrt
from cayley_permutations import CayleyPermutation

x = symbols("x")

with open("wilf_equivalence_classes_3s.txt", "r") as f:
    gfs_dict = eval(f.readline())

for gf, bases in gfs_dict.items():
    print("Generating function:", gf)
    print("Number of bases in this class:", len(bases))
    print("Bases:")
    for basis in bases:
        basis_str = ", ".join(str(p) for p in basis)
        print(f"Av({basis_str})")
    print()
