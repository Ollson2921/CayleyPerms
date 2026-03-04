from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from itertools import combinations

"""Error from spec Av(012,1020), fusion"""
til_error_1 = Tiling(
    (
        GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
        GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 0))),
        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 1))),
        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (2, 1))),
        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))),
        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 0), (0, 0))),
        GriddedCayleyPerm(CayleyPermutation((0, 1, 2)), ((0, 0), (0, 1), (0, 1))),
        GriddedCayleyPerm(CayleyPermutation((0, 1, 2)), ((0, 1), (0, 1), (0, 1))),
        GriddedCayleyPerm(CayleyPermutation((1, 0, 2)), ((0, 1), (0, 0), (0, 1))),
        GriddedCayleyPerm(
            CayleyPermutation((1, 0, 2, 0)), ((0, 1), (0, 1), (0, 1), (0, 1))
        ),
        GriddedCayleyPerm(
            CayleyPermutation((1, 0, 2, 0)), ((0, 1), (0, 1), (0, 1), (1, 1))
        ),
        GriddedCayleyPerm(
            CayleyPermutation((1, 0, 2, 0)), ((0, 1), (0, 1), (0, 1), (2, 1))
        ),
    ),
    (),
    (3, 2),
)

"""Error from spec Av(021,120,0122,2001)"""
til_error2 = Tiling(
    (
        GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
        GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (1, 0))),
        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (2, 1))),
        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 0), (1, 0))),
        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (2, 1))),
        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1))),
        GriddedCayleyPerm(CayleyPermutation((0, 1, 1)), ((1, 1), (2, 1), (2, 1))),
        GriddedCayleyPerm(CayleyPermutation((0, 1, 1)), ((2, 1), (2, 1), (2, 1))),
        GriddedCayleyPerm(CayleyPermutation((2, 0, 1)), ((0, 1), (1, 0), (1, 1))),
    ),
    (),
    (3, 2),
)


"""5x1 tiling with less than or equal row separation."""
obs = []
cells = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
for cell1, cell2 in combinations(cells, 2):
    obs.append(GriddedCayleyPerm(CayleyPermutation([0, 1]), [cell1, cell2]))

til_large_separation = Tiling(
    obs,
    (),
    (5, 1),
)


"""Three rows of the tiling can separate."""
til_multiple_rows = Tiling(
    (
        GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
        GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (2, 0))),
        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (1, 1))),
        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (2, 1))),
        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (2, 1))),
        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1))),
        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 2))),
    ),
    (),
    (3, 3),
)
