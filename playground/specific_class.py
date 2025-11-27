"""Finds the generating function for a Cayley permutation class
with a given basis. A basis is input as a string.

'spec' has the same functions as in the insertion encoding repo so
you can create specifications, print the counts etc. in the same way.

I've set the pack to point_placement, this is generally the best one
but you can have a play around with different packs if point placement
doesn't work.
(Note: can not guarantee success with any packs!)"""

from cayley_permutations import string_to_basis
from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from comb_spec_searcher import (
    CombinatorialSpecificationSearcher,
)
from tilescope import TileScopePack

# Input basis
basis = "120,201,1010"

start_class = Tiling(
    [GriddedCayleyPerm(p, [(0, 0) for _ in p]) for p in string_to_basis(basis)],
    [],
    (1, 1),
)
searcher = CombinatorialSpecificationSearcher(
    start_class, TileScopePack.point_placement()
)
spec = searcher.auto_search()
# spec.get_genf()
print([spec.count_objects_of_size(i) for i in range(10)])
