"""Testing out the functions, checking clouds map correctly."""

from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from clouds import TrackedTiling
from clouds.tracked_algos import (
    TrackedFactors,
    TrackedLessThanRowColSeparation,
    TrackedLessThanOrEqualRowColSeparation,
    TrackedPointPlacement,
)


def test_factoring_clouds():
    """Test factoring with tracked tilings."""
    til = Tiling.create_vincular_or_bivincular("0")
    track_til = TrackedTiling(
        til,
        value_clouds=((0, 1), (2,)),
        indices_clouds=((1, 2),),
        intersect_clouds_with_active=True,
    )
    assert list(TrackedFactors(track_til).find_tracked_factors()) == [
        TrackedTiling(
            tiling=Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (2, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1))),
                ),
                (),
                (3, 3),
            ),
            indices_clouds=((2,),),
            value_clouds=((0,), (2,)),
        ),
        TrackedTiling(
            tiling=Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
                ),
                ((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),),),
                (3, 3),
            ),
            indices_clouds=((1,),),
            value_clouds=((1,),),
        ),
    ]


def test_lt_rc_sep_clouds():
    """Test less than row and column separation with tracked tilings."""
    til = Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (0, 1)])], [], (1, 2)
    )
    track_til = TrackedTiling(
        til,
        value_clouds=(
            (0,),
            (1,),
        ),
        indices_clouds=((0,),),
        intersect_clouds_with_active=False,
    )
    assert list(
        TrackedLessThanRowColSeparation(track_til).tracked_row_col_separation()
    ) == [
        TrackedTiling(
            tiling=Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                ),
                (),
                (2, 2),
            ),
            indices_clouds=((0, 1),),
            value_clouds=((0,), (1,)),
        )
    ]


def test_lte_rc_sep_clouds():
    """Test less than or equal row and column separation with tracked tilings."""
    til = Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (1, 0)])], [], (2, 1)
    )
    track_til = TrackedTiling(
        til,
        value_clouds=((0,),),
        indices_clouds=(),
        intersect_clouds_with_active=False,
    )
    assert set(
        TrackedLessThanOrEqualRowColSeparation(track_til).tracked_row_col_separation()
    ) == {
        TrackedTiling(
            tiling=Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                ),
                (),
                (2, 3),
            ),
            indices_clouds=(),
            value_clouds=((0, 2),),
        ),
        TrackedTiling(
            tiling=Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
                ),
                (
                    (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),),
                    (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),),
                ),
                (2, 3),
            ),
            indices_clouds=(),
            value_clouds=((0, 1, 2),),
        ),
    }


def test_point_placement_clouds():
    """Test point placement with tracked tilings."""
    til = Tiling([], [], (2, 2))
    tracked_til = TrackedTiling(til, value_clouds=((0,),), indices_clouds=((0,), (1,)))
    assert list(
        TrackedPointPlacement(tracked_til).tracked_point_placement(
            [GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)])], (0,), 0
        )
    ) == [
        TrackedTiling(
            tiling=Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 1), (3, 1))),
                ),
                ((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),),),
                (4, 4),
            ),
            indices_clouds=((0, 1, 2), (3,)),
            value_clouds=((0, 1, 2),),
        )
    ]


def test_fusion_with_clouds():
    """Test fusion with tracked tilings."""
    "-----Fusing Rows 1, 2-----"
    til = Tiling([], [], (3, 3))
    tracked_til = TrackedTiling(
        til,
        value_clouds=((0,),),
        indices_clouds=((0, 1),),
    )
    assert tracked_til.is_fusable(True, 1)
    fused = tracked_til.fuse(True, 1)
    assert fused == TrackedTiling(
        tiling=Tiling((), (), (3, 2)),
        indices_clouds=((0, 1),),
        value_clouds=((0,), (1,)),
    )

    "-----Fusing Columns 1, 2-----"
    til = Tiling([], [], (3, 3))
    tracked_til = TrackedTiling(
        til,
        value_clouds=((0,), (2,)),
        indices_clouds=((0,),),
    )
    assert tracked_til.is_fusable(False, 1)
    fused = tracked_til.fuse(False, 1)
    assert fused == TrackedTiling(
        tiling=Tiling((), (), (2, 3)),
        indices_clouds=((0,), (1,)),
        value_clouds=((0,), (2,)),
    )
