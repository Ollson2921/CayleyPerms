"""For changing the names of files of specs."""

from cayley_permutations import Av
import json
from itertools import permutations
from tilescope import TileScopePack
from useful_functions import lex_min

pack = TileScopePack.point_placement()


basis_desc = "3s_4x1"  # change descriptor to change file
basis_desc = "3s"

print(basis_desc)

with open(f"all_non_insenc_basis_classes_{basis_desc}.txt", "r") as f:
    successes = eval(f.readline())

couldnt_find = set()

# with open(f"3s/second run/Av(000,102,110,011)_Point Placement.json", "r") as f:
#     spec = json.load(f)
# print(spec)

tot = len(successes)
count = 0

all_successes = set()

for bases in successes:
    count += 1
    print(count, "out of", tot)
    bases = list(bases)
    found_spec = False
    for basis in bases:
        basis = list(basis)
        n = len(basis)
        for shuffled_basis in set(permutations(basis, n)):
            try:
                with open(
                    f"{basis_desc}/no fusion/{Av(shuffled_basis)}_{pack.name}.json",
                    "r",
                ) as f:
                    spec = json.load(f)
                    found_spec = True
                    break
            except FileNotFoundError:
                continue
            if found_spec:
                break
        if found_spec:
            break
    if not found_spec:
        couldnt_find.add(tuple(bases))
        continue
    # with open(
    #     f"{basis_desc}/sorted_second_run/{Av(lex_min(basis))}_{pack.name}.json",
    #     "w",
    # ) as f:
    #     f.write(json.dumps(spec))
    all_successes.add(lex_min(basis))

# print(f"Couldn't find {len(couldnt_find)} specs")
# print(couldnt_find)

print("Found", tot - len(couldnt_find))
with open(f"non_fusion_successes_{basis_desc}.txt", "w") as f:
    f.write(repr(all_successes))
