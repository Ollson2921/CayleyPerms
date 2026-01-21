from cayley_permutations import Av, CayleyPermutation
import json
from clouds import TrackedTileScopePack
from comb_spec_searcher import CombinatorialSpecification

# basis_desc = "3s_4x1"  # change descriptor to change file
basis_desc = "3s"

all_packs = TrackedTileScopePack.all_packs()

# Load bases from file
with open(f"fusion_to_run_{basis_desc}.txt", "r") as f:
    bases = eval(f.readline())

for basis in bases:
    for pack in all_packs:
        try:
            with open(f"specs/{Av(basis)}_{pack.name}.json", "r") as f:
                spec = json.load(f)
            spec = CombinatorialSpecification.from_dict(spec)
            try:
                spec.get_genf()
            except NotImplementedError:
                input()
                continue
        except FileNotFoundError:
            continue
