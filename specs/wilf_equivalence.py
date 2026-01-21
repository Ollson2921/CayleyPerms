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
# basis_desc = "3s"

if __name__ == "__main__":
    from multiprocessing import freeze_support

    freeze_support()
    run = 0
    print("run", run)

    with open(f"{basis_desc}/non_fusion_successes_{basis_desc}.txt", "r") as f:
        all_successes = list(eval(f.readline()))

    to_run = all_successes[:200]
    to_run += all_successes[400:]
    successes = to_run

    # with open(f"{basis_desc}/all_non_inenc_basis_classes_{basis_desc}.txt", "r") as f:
    #     all_bases = list(eval(f.readline()))

    # with open(f"took_too_long_{basis_desc}.txt", "r") as f:
    #     successes = eval(f.readline())

    # with open(f"wilf_equivalence_classes_{basis_desc}.txt", "r") as f:
    #     gfs_dict = eval(f.readline())

    couldnt_find = set()
    took_too_long = set()

    tot = len(successes)
    count = 0
    no_spec_count = 0

    gfs_dict = {}

    for basis in successes:
        count += 1
        print(count, "out of", tot)
        print(f"found {len(gfs_dict)} wilf-equivalence classes so far")
        print(f"Specs that took too long so far: {no_spec_count}")
        with open(
            f"{basis_desc}/no fusion/{Av(basis)}_{pack.name}.json",
            "r",
        ) as f:
            spec = json.load(f)
        spec = CombinatorialSpecification.from_dict(spec)
        try:  # only trying for 2hrs currently
            gf = spec.get_genf()
            if gf in gfs_dict:
                gfs_dict[gf].append(basis)
            else:
                gfs_dict[gf] = [basis]
        except Exception as e:
            print("Couldn't get gf for basis", basis)
            took_too_long.add(basis)
            no_spec_count += 1
            continue

    print("Number of wilf-equivalence classes:", len(gfs_dict))
    print(f"Out of {len(gfs_dict.items())} bases")

    with open(
        f"fusion_wilf_equivalence_classes_{basis_desc}_run_{run}.txt",
        "w",
    ) as f:
        f.write(repr(gfs_dict))

    print("Number of specs that took too long to get gf for:", len(took_too_long))
    with open(f"fusion_took_too_long_{basis_desc}_run_{run}.txt", "w") as f:
        f.write(repr(took_too_long))

    input()
    for gf in gfs_dict:
        print(gf)
        # print("Class with gf", gf, "has bases:")
        for basis in gfs_dict[gf]:
            print(Av(basis))
        print()
