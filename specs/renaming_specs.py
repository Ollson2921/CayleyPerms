"""For changing the names of files of specs."""

from cayley_permutations import Av, CayleyPermutation
import json
from itertools import permutations
from tilescope import TileScopePack
from useful_functions import lex_min, sym_of_basis

pack = TileScopePack.point_placement()


basis_desc = "3s_4x1"  # change descriptor to change file
# basis_desc = "3s"

print(basis_desc)

with open(f"all_non_inenc_basis_classes_{basis_desc}.txt", "r") as f:
    successes = eval(f.readline())

couldnt_find = set()

# with open(f"3s_4x1/second run/Av(000,001,1010,120)_Point Placement.json", "r") as f:
#     spec = json.load(f)
# print(spec)

tot = len(successes)
count = 0
found_count = 0

all_successes = set()

for bases in successes:
    bases = list(bases)
    count += 1
    print(count, "out of", tot)
    print(f"found {found_count}")
    found_spec = False
    for basis in sym_of_basis(bases):
        n = len(basis)
        for shuffled_basis in set(permutations(basis, n)):
            basis_string = ",".join(str(p) for p in shuffled_basis)
            try:
                with open(
                    f"{basis_desc}/no fusion/Av({basis_string})_{pack.name}.json",
                    "r",
                ) as f:
                    spec = json.load(f)
                    found_spec = True
                    print("Found spec!")
                    found_count += 1
                    break
            except FileNotFoundError:
                pass
            if found_spec:
                break
            try:
                with open(
                    f"{basis_desc}/no fusion/Av({basis_string})_Point Placement.json",
                    "r",
                ) as f:
                    spec = json.load(f)
                    found_spec = True
                    print("Found spec!")
                    found_count += 1
                    break
            except FileNotFoundError:
                continue
            if found_spec:
                break
        if found_spec:
            break
    if not found_spec:
        couldnt_find.add(lex_min(bases))
        continue
    with open(
        f"{basis_desc}/all_no_fusion/{Av(lex_min(basis))}_{pack.name}.json",
        "w",
    ) as f:
        f.write(json.dumps(spec))
    all_successes.add(lex_min(basis))

print(f"Couldn't find {len(couldnt_find)} specs")

print("Found", tot - len(couldnt_find))
with open(f"non_fusion_successes_part_2_{basis_desc}.txt", "w") as f:
    f.write(repr(all_successes))
with open(f"to_compute_with_fusion_part_2_{basis_desc}.txt", "w") as f:
    f.write(repr(couldnt_find))
