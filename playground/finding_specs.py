"""Takes a txt file with an iterable of bases and a list of packs and tries
to find specs. For each success, it checks the counts and adds the json of
the spec to the specs folder if the counts are correct. If they are incorrect
then adds the json spec to the wrong_counts folder and adds the basis and pack
to a list which is saved to wrong_counts.txt. If no pack works for a basis,
then adds the basis to a list which is saved to didnt_compute.txt."""

from cayley_permutations import CayleyPermutation, Av
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from comb_spec_searcher import CombinatorialSpecificationSearcher
from tilescope import TileScopePack
import json

# All packs to try
all_packs = [
    TileScopePack.point_placement(),
    TileScopePack.point_placement_initial_place_points(),
    TileScopePack.point_placement_initial_cell_insertion(),
    TileScopePack.point_placements_shuffle(),
    TileScopePack.point_placements_shuffle_initial_cell_insertion(),
    TileScopePack.row_placement(),
    TileScopePack.col_placement(),
    TileScopePack.row_and_col_placement(),
    TileScopePack.point_row_and_col_placement(),
    TileScopePack.row_placement_initial_cell_insertion(),
    TileScopePack.col_placement_initial_cell_insertion(),
    TileScopePack.row_and_col_placement_initial_cell_insertion(),
    TileScopePack.point_row_and_col_placement_initial_cell_insertion(),
]

# The to_run folder contains files with bases to run
with open("to_run/to_run_3.txt", "r") as f:
    bases = eval(f.readline())

counted = set()
wrong_counts = []
didnt_compute = []

for basis in bases:
    tiling = Tiling(
        [GriddedCayleyPerm(p, [(0, 0) for _ in p]) for p in basis],
        [],
        (1, 1),
    )
    for pack in all_packs:
        if tuple(basis) in counted:
            break
        searcher = CombinatorialSpecificationSearcher(tiling, pack, debug=False)
        try:
            spec = searcher.auto_search(max_expansion_time=36000)  # set maxtime
            spec_count = [spec.count_objects_of_size(n) for n in range(10)]
            brute_force_count = Av(basis).counter(9)
            json_spec = json.dumps(spec.to_jsonable())
            if spec_count == brute_force_count:
                counted.add(tuple(basis))
                with open(f"specs/{basis}_{pack.name}.json", "w") as f:
                    f.write(json_spec)
            else:
                wrong_counts.append((basis, pack.name))
                with open(f"wrong_counts/{basis}_{pack.name}.json", "w") as f:
                    f.write(json_spec)
        except Exception as e:
            print(f"Didn't compute {basis} with {pack.name}: {e}")
            continue
    basis = tuple(basis)
    if basis not in counted:
        didnt_compute.append(basis)

"""Makes a file with a list of tuples where each tuple has a basis and a pack which
failed to count correctly. Each of these should have a corresponding json spec in
the wrong_counts folder."""
with open("wrong_counts.txt", "w") as f:
    f.write(repr(wrong_counts))

"""Makes a file with a list of bases which didn't compute with any pack."""
with open("didnt_compute.txt", "w") as f:
    f.write(repr(didnt_compute))

"""Makes a file with a list of bases which did compute with any pack."""
with open("did_compute.txt", "w") as f:
    f.write(repr(counted))
    f.write(f"Basis computed correctly: {len(counted)}")
