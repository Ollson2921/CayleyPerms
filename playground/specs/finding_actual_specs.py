from cayley_permutations import CayleyPermutation, Av
import json
from itertools import combinations

basis_desc = "3s_4x1"  # change descriptor to change file
basis_desc = "3s"

print(basis_desc)

with open(f"actual_successes_{basis_desc}.txt", "r") as f:
    successes = eval(f.readline())
