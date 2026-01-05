from clouds import TrackedTiling, TileScopePack
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation, string_to_basis
from comb_spec_searcher import CombinatorialSpecificationSearcher

basis = "012_101_001_010"  # done
basis = "012_101_010"  # done
basis = "210_101_011"  # done
basis = "101_010_011"  # done
basis = "100_110_010_011"  # done
basis = "101_010"  # done
basis = "101_110_010_001_011"  # done
basis = "100_110_001_011"  # done
# basis = "210_100_110_010" # done

tiling = Tiling(
    [GriddedCayleyPerm(p, [(0, 0) for _ in p]) for p in string_to_basis(basis)],
    [],
    (1, 1),
)
tracked_tiling = TrackedTiling(tiling, [], [])


pack = TileScopePack.col_placement_fusion()
searcher = CombinatorialSpecificationSearcher(tracked_tiling, pack, debug=False)
spec = searcher.auto_search(status_update=5)

# print(spec.get_maple_equations())

# spec.sanity_check(4)
# spec.show()
print([spec.count_objects_of_size(i) for i in range(10)])
print("[", end="")
for i in range(10):
    print(spec.root_rule.comb_class.get_terms(i)[tuple()], end="", flush=True)
    if i == 9:
        print("]")
    else:
        print(", ", end="")
