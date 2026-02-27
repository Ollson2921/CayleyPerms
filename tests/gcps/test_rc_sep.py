from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from tilescope.strategies.row_column_separation import LessThanOrEqualRowColSeparation


def test_ltoreq_rc_sep():
    """One row separates in 3 columns, make sure can still have
    gcps going across the whole row."""
    tiling = Tiling(
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

    out = {
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (0, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (2, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (2, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (2, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (1, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (2, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 2), (2, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 0), (0, 0))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (0, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (1, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (2, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (1, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (2, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 2), (2, 2))),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2)), ((0, 0), (0, 2), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2)), ((0, 0), (0, 3), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2)), ((0, 2), (0, 3), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2)), ((0, 3), (0, 3), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2)), ((0, 2), (0, 0), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2)), ((0, 3), (0, 0), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2, 0)), ((0, 3), (0, 2), (0, 3), (0, 2))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2, 0)), ((0, 3), (0, 2), (0, 3), (1, 2))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2, 0)), ((0, 3), (0, 2), (0, 3), (2, 2))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2, 0)), ((0, 3), (0, 3), (0, 3), (0, 3))
                ),
            ),
            (
                (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),),
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                ),
            ),
            (3, 4),
        ),
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (0, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (2, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (1, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (1, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (1, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (2, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 3), (1, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 2), (2, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 0), (0, 0))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (0, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (1, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (2, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (1, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (2, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 2), (2, 2))),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2)), ((0, 0), (0, 2), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2)), ((0, 0), (0, 3), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2)), ((0, 2), (0, 3), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2)), ((0, 3), (0, 3), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2)), ((0, 2), (0, 0), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2)), ((0, 3), (0, 0), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2)), ((0, 3), (0, 2), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2, 0)), ((0, 3), (0, 3), (0, 3), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2, 0)), ((0, 3), (0, 3), (0, 3), (1, 3))
                ),
            ),
            (
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                ),
                (GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),),
            ),
            (3, 4),
        ),
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (2, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 0), (0, 0))),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2)), ((0, 0), (0, 3), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2)), ((0, 3), (0, 3), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2)), ((0, 3), (0, 0), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2, 0)), ((0, 3), (0, 3), (0, 3), (0, 3))
                ),
            ),
            (),
            (3, 4),
        ),
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (1, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 3), (1, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 0), (0, 0))),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2)), ((0, 0), (0, 3), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2)), ((0, 3), (0, 3), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2)), ((0, 3), (0, 0), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2, 0)), ((0, 3), (0, 3), (0, 3), (0, 3))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2, 0)), ((0, 3), (0, 3), (0, 3), (1, 3))
                ),
            ),
            (),
            (3, 4),
        ),
    }

    assert set(LessThanOrEqualRowColSeparation(tiling).row_col_separation()) == out
