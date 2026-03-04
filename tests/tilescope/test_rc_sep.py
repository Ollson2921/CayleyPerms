from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from itertools import combinations
from tilescope.strategies.row_column_separation import (
    LessThanOrEqualRowColSeparationFactory,
)


def test_ltoreq_row_col_sep_error1_from_spec():
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
    out = set()
    for strat in LessThanOrEqualRowColSeparationFactory()(til_error_1):
        out.add(strat(til_error_1).children)

    expanded = {
        (
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
                        CayleyPermutation((1, 0, 2, 0)),
                        ((0, 3), (0, 3), (0, 3), (0, 3)),
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((1, 0, 2, 0)),
                        ((0, 3), (0, 3), (0, 3), (1, 3)),
                    ),
                ),
                (),
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
                        CayleyPermutation((1, 0, 2, 0)),
                        ((0, 3), (0, 3), (0, 3), (0, 3)),
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((1, 0, 2, 0)),
                        ((0, 3), (0, 3), (0, 3), (1, 3)),
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
        ),
        (
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
                        CayleyPermutation((1, 0, 2, 0)),
                        ((0, 3), (0, 3), (0, 3), (0, 3)),
                    ),
                ),
                (),
                (3, 4),
            ),
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
                        CayleyPermutation((1, 0, 2, 0)),
                        ((0, 3), (0, 2), (0, 3), (0, 2)),
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((1, 0, 2, 0)),
                        ((0, 3), (0, 2), (0, 3), (1, 2)),
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((1, 0, 2, 0)),
                        ((0, 3), (0, 2), (0, 3), (2, 2)),
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((1, 0, 2, 0)),
                        ((0, 3), (0, 3), (0, 3), (0, 3)),
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
        ),
    }

    assert out == expanded


def test_ltoreq_row_col_sep_error2_from_spec():
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
    til = til_error2
    out = set()
    for strat in LessThanOrEqualRowColSeparationFactory()(til):
        out.add(strat(til).children)
    expanded = {
        (
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (0, 3))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (1, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (2, 3))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 0), (1, 0))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 3), (2, 3))),
                    GriddedCayleyPerm(
                        CayleyPermutation((0, 1, 1)), ((1, 1), (2, 3), (2, 3))
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((0, 1, 1)), ((2, 3), (2, 3), (2, 3))
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((2, 0, 1)), ((0, 3), (1, 0), (1, 1))
                    ),
                ),
                (),
                (3, 4),
            ),
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 3), (2, 3))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (0, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (0, 3))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (0, 3))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (1, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (0, 2))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (2, 3))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 0), (1, 0))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 3), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 3), (2, 3))),
                    GriddedCayleyPerm(
                        CayleyPermutation((0, 1, 1)), ((1, 1), (2, 2), (2, 2))
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((2, 0, 1)), ((0, 2), (1, 0), (1, 1))
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((2, 0, 1)), ((0, 3), (1, 0), (1, 1))
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((2, 0, 1)), ((0, 3), (1, 0), (1, 2))
                    ),
                ),
                (
                    (
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                    ),
                    (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),),
                ),
                (3, 4),
            ),
        ),
        (
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 3),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (1, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 0), (1, 0))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 3), (2, 3))),
                    GriddedCayleyPerm(
                        CayleyPermutation((0, 1, 1)), ((1, 1), (2, 3), (2, 3))
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((0, 1, 1)), ((2, 3), (2, 3), (2, 3))
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((2, 0, 1)), ((0, 1), (1, 0), (1, 1))
                    ),
                ),
                (),
                (3, 4),
            ),
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 3),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (0, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (1, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (0, 2))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 0), (1, 0))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 3), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 3), (2, 3))),
                    GriddedCayleyPerm(
                        CayleyPermutation((0, 1, 1)), ((1, 1), (2, 2), (2, 2))
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((0, 1, 1)), ((1, 1), (2, 3), (2, 3))
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((0, 1, 1)), ((1, 2), (2, 3), (2, 3))
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((0, 1, 1)), ((2, 2), (2, 3), (2, 3))
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((0, 1, 1)), ((2, 3), (2, 3), (2, 3))
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((2, 0, 1)), ((0, 1), (1, 0), (1, 1))
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((2, 0, 1)), ((0, 2), (1, 0), (1, 1))
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
        ),
    }

    assert out == expanded


def test_ltoreq_row_col_sep_large_separation():
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
    til = til_large_separation
    out = set()
    for strat in LessThanOrEqualRowColSeparationFactory()(til):
        out.add(strat(til).children)
    expected = {
        (
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 0), (4, 0))),
                ),
                (),
                (5, 3),
            ),
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 0), (4, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 0), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 1), (4, 1))),
                ),
                (
                    (
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                    ),
                    (
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 1),)),
                    ),
                ),
                (5, 3),
            ),
        ),
        (
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 0), (3, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 0), (4, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 0), (4, 0))),
                ),
                (),
                (5, 3),
            ),
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 0), (3, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 0), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 0), (4, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 0), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 0), (4, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 0), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 1), (4, 1))),
                ),
                (
                    (
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                    ),
                    (
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 1),)),
                    ),
                ),
                (5, 3),
            ),
        ),
        (
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (3, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (3, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 2), (3, 2))),
                ),
                (),
                (5, 3),
            ),
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (3, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (3, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (3, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (3, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (3, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 2), (3, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 1), (4, 1))),
                ),
                (
                    (
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)),
                    ),
                    (GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 1),)),),
                ),
                (5, 3),
            ),
        ),
        (
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (2, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (3, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (4, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 0), (3, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 0), (4, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 0), (4, 0))),
                ),
                (),
                (5, 3),
            ),
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (2, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (3, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (4, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 0), (3, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 0), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 0), (4, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 0), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 0), (4, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 0), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 1), (4, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 1), (4, 1))),
                ),
                (
                    (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),),
                    (
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 1),)),
                    ),
                ),
                (5, 3),
            ),
        ),
    }

    assert out == expected


def test_less_than_or_equal_row_col_separation_multiple_rows():
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

    til = til_multiple_rows
    out = set()
    for strat in LessThanOrEqualRowColSeparationFactory()(til):
        out.add(strat(til).children)
    expected = {(Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 8),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 8),)), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 5)))), (),(3, 9)), Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 8),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 8),)), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 5)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),)),(3, 9)), Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 8),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 8),)), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (0, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (0, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 5)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),))), (GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),)),)),(3, 9)), Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 8),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 8),)), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 7), (0, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 7), (0, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 5)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 7),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 7),)),)),(3, 9)), Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 8),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 8),)), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (0, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (0, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 5)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),))), (GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),)),)),(3, 9)), Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 8),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 8),)), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 7), (0, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 7), (0, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 5)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 7),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 7),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),)),(3, 9)), Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 8),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 8),)), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (0, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 7), (0, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (0, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 7), (0, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 5)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),))), (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 7),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 7),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),)),)),(3, 9)), Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 8),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 8),)), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (0, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 7), (0, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (0, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 7), (0, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 5)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),))), (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 7),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 7),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),)),)),(3, 9))), (Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 8),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 8),)), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (1, 5))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (2, 5))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 5)))), (),(3, 9)), Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 8),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 8),)), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (1, 5))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (2, 5))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 5)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),)),(3, 9)), Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 8),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 8),)), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (0, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (0, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (1, 5))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (2, 5))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 5)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 4),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),)))),(3, 9)), Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 8),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 8),)), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 7), (0, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 7), (0, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (1, 5))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (2, 5))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 5)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 7),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 7),)),)),(3, 9)), Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 8),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 8),)), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (0, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (0, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (1, 5))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (2, 5))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 5)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 4),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),))), (GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),)),(3, 9)), Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 8),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 8),)), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 7), (0, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 7), (0, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (1, 5))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (2, 5))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 5)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 7),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 7),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),)),(3, 9)), Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 8),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 8),)), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (0, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 7), (0, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (0, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 7), (0, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (1, 5))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (2, 5))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 5)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 4),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 7),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),))), (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 7),)),)),(3, 9)), Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 8),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 6),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 8),)), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (0, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 7), (0, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (0, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 7), (0, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (1, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (1, 5))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 5), (2, 5))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 7), (1, 7))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 5), (2, 5)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 4),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 7),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),))), (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 7),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),)),(3, 9)))}
    assert out == expected

