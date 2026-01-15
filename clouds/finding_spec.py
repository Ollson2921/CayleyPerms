from clouds import TrackedTiling, TrackedTileScopePack, TrackedSearcher
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
basis = "000_010_100_101_210"
# basis = "210_100_110_010" # done

basis = "001,010,110"

pack = TrackedTileScopePack.standard_fusion_pack(expansion_methods=["point"])
searcher = TrackedSearcher(basis, pack, debug=False, max_cvs=1)
spec = searcher.auto_search(status_update=5)

spec.show()
# print(spec.get_maple_equations())

spec = spec.expand_verified()
# spec.sanity_check(4)
# # spec.show()
# print([spec.count_objects_of_size(i) for i in range(10)])
# print("[", end="")
# for i in range(10):
#     print(spec.root_rule.comb_class.get_terms(i)[tuple()], end="", flush=True)
#     if i == 9:
#         print("]")
#     else:
#         print(", ", end="")

print(spec.get_genf())
