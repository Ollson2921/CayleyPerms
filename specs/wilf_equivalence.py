"""Takes all of the specs, finds their gfs, buts them in a dict to
find the wilf-equivalence classes."""

from typing import Iterable
from cayley_permutations import CayleyPermutation, Av
import json
from itertools import combinations, permutations
from tilescope import TileScopePack
from useful_functions import lex_min
from comb_spec_searcher import CombinatorialSpecification

pack = TileScopePack.point_placement()


basis_desc = "3s_4x1"  # change descriptor to change file
basis_desc = "3s"


with open(f"all_non_inenc_basis_classes_{basis_desc}.txt", "r") as f:
    successes = eval(f.readline())

couldnt_find = set()

tot = len(successes)
count = 0

gfs_dict = {}

for basis in successes:
    count += 1
    print(count, "out of", tot)
    with open(
        f"{basis_desc}/no fusion/{Av(basis)}_{pack.name}.json",
        "r",
    ) as f:
        spec = json.load(f)
    spec = CombinatorialSpecification.from_dict(spec)
    gf = spec.get_genf()
    if gf in gfs_dict:
        gfs_dict[gf].append(basis)
    else:
        gfs_dict[gf] = [basis]

print("Number of wilf-equivalence classes:", len(gfs_dict))
with open(f"wilf_equivalence_classes_{basis_desc}.txt", "w") as f:
    f.write(repr(gfs_dict))

input()
for gf in gfs_dict:
    print("Class with gf", gf, "has bases:")
    for basis in gfs_dict[gf]:
        print(basis)
    print()
