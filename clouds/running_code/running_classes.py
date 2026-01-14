import requests
import time
from datetime import timedelta
from cayley_permutations import Av, CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
import json
from clouds import TrackedTiling, TileScopePack, TrackedSearcher

# Load bases from file
with open("final_to_compute_with_fusion_3s_4x1.txt", "r") as f:
    bases = eval(f.readline())

all_packs = [
    TileScopePack.point_placement(),
    TileScopePack.point_row_and_col_placement(),
    TileScopePack.col_placement(),
    TileScopePack.row_and_col_placement(),
    TileScopePack.row_placement(),
    TileScopePack.point_and_col_placement(),
    TileScopePack.point_and_row_placement(),
]

basis_desc = "3s_4x1"  # change descriptor to change file
# basis_desc = "3s"


counted = set()
wrong_counts = []
didnt_compute = []
total = len(bases)
n = 0

for basis in list(bases):
    basis = tuple(sorted(basis))
    tiling = TrackedTiling(
        Tiling(
            [GriddedCayleyPerm(p, [(0, 0) for _ in p]) for p in basis],
            [],
            (1, 1),
        ),
        [],
        [],
    )
    for pack in all_packs:
        print(f"Trying basis {Av(basis)} with pack {pack.name}")
        # if tuple(basis) in counted: # for breaking as soon as found a correct spec
        #     break
        searcher = TrackedSearcher(tiling, pack, debug=False)
        try:
            start_time = time.time()
            spec = searcher.auto_search(max_expansion_time=3600 * 5)  # set maxtime
            # spec.show()
            time_taken = timedelta(seconds=int(time.time() - start_time))
            print(f"Pack: {pack.name} took {time_taken}")
            message = f"Computed a spec for {Av(basis)}, Pack: {pack.name}. \nTook {time_taken}."
            json_spec = json.dumps(spec.to_jsonable())
            with open(f"specs/{Av(basis)}_{pack.name}.json", "w") as f:
                f.write(json_spec)

            print("checking counts")
            spec_count = [spec.count_objects_of_size(n) for n in range(10)]
            brute_force_count = Av(basis).counter(9)
            if spec_count == brute_force_count:
                counted.add(tuple(basis))
                message += " Found correct counts."
            else:
                wrong_counts.append((basis, pack.name))
                message += f" But WRONG counts! Spec counts: \n{spec_count},\n Brute force counts: \n{brute_force_count}"

            # Send to discord
            # webhookurl = "https://discord.com/api/webhooks/1446479214629883997/Ct682I4szno9aF4mpskSHVoeCpXA37IfWddC1SVycmI-CYbHmbrFsmQNhAxEC2yCu1mT"
            # headers = {"User-Agent": "hildur", "Content-Type": "application/json"}
            # data = json.dumps({"content": message})
            # requests.post(webhookurl, headers=headers, data=data)
            print(message)
        except Exception as e:
            print(f"Didn't compute {Av(basis)} with {pack.name}: {e}")
            continue
    if basis not in counted:
        didnt_compute.append(basis)
    n += 1
    print(f"Tried {n}/{total}")
    print(f"Counted: {len(counted)}")
    print(f"Didn't compute: {len(didnt_compute)}")

"""Makes a file with a list of tuples where each tuple has a basis and a pack which
failed to count correctly. Each of these should have a corresponding json spec in
the wrong_counts folder."""
with open("wrong_counts.txt", "w") as f:
    f.write(repr(wrong_counts))

"""Makes a file with a list of bases which didn't compute with any pack."""
with open("didnt_compute.txt", "w") as f:
    f.write(repr(didnt_compute))
    f.write(f"\nBasis didn't compute: {len(didnt_compute)}")

"""Makes a file with a list of bases which did compute with any pack."""
with open("did_compute.txt", "w") as f:
    f.write(repr(counted))
    f.write(f"\nBasis computed correctly: {len(counted)}")
