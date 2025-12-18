from clouds import TrackedTiling, TileScopePack
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation, string_to_basis
from comb_spec_searcher import CombinatorialSpecificationSearcher

basis = "012"
tiling = Tiling(
    [GriddedCayleyPerm(p, [(0, 0) for _ in p]) for p in string_to_basis(basis)],
    [],
    (1, 1),
)
tracked_tiling = TrackedTiling(tiling, [], [])


pack = TileScopePack.col_placement_fusion()
searcher = CombinatorialSpecificationSearcher(tracked_tiling, pack, debug=True)
spec = searcher.auto_search(status_update=5)

# print(spec.get_maple_equations())

# spec.sanity_check(4)

print([spec.count_objects_of_size(i) for i in range(10)])
