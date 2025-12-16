from clouds import TrackedTiling, TileScopePack
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from comb_spec_searcher import CombinatorialSpecificationSearcher

til = TrackedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation((0, 1, 2)), ((0, 0), (0, 0), (0, 0)))],
        [],
        (1, 1),
    )
)


pack = TileScopePack.col_placement_fusion()
searcher = CombinatorialSpecificationSearcher(til, pack, debug=False)
spec = searcher.auto_search()
spec.show()
spec.get_genf()
