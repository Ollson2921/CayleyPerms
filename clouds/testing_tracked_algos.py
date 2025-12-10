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

print("=====Factoring=====")
til = Tiling.create_vincular_or_bivincular("0")
track_til = TrackedTiling(
    til,
    value_clouds=(((0, 0), (0, 1)),),
    indices_clouds=(((1, 0), (1, 1), (2, 0), (2, 1)),),
    intersect_clouds_with_active=True,
)
print(track_til)
for til in TrackedFactors(track_til).find_tracked_factors():
    print(til)
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
        value_clouds=(((0, 0), (0, 1)),),
        indices_clouds=(((2, 0), (2, 1)),),
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
        value_clouds=((),),
        indices_clouds=(((1, 1),),),
    ),
]

print("=====Row and Column Separation=====")
til = Tiling(
    [GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (0, 1)])], [], (1, 2)
)
track_til = TrackedTiling(
    til,
    value_clouds=(((0, 0), (0, 1)),),
    indices_clouds=(((0, 0),),),
    intersect_clouds_with_active=False,
)
print(track_til)
for til in TrackedLessThanRowColSeparation(track_til).tracked_row_col_separation():
    print(til)
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
        value_clouds=(((1, 0), (0, 1)),),
        indices_clouds=(((1, 0),),),
    )
]

print("=====Less Than or Equal Row and Column Separation=====")
til = Tiling(
    [GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (1, 0)])], [], (2, 1)
)
track_til = TrackedTiling(
    til,
    value_clouds=(((0, 0), (1, 0)),),
    indices_clouds=(((0, 0),),),
    intersect_clouds_with_active=False,
)
print(track_til)
for til in TrackedLessThanOrEqualRowColSeparation(
    track_til
).tracked_row_col_separation():
    print(til)
assert list(
    TrackedLessThanOrEqualRowColSeparation(track_til).tracked_row_col_separation()
) == [
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
        value_clouds=(((0, 2), (1, 0)),),
        indices_clouds=(((0, 2),),),
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
        value_clouds=(((0, 1), (0, 2), (1, 0), (1, 1)),),
        indices_clouds=(((0, 1), (0, 2)),),
    ),
]

print("=====Point Placement=====")
til = Tiling([], [], (2, 2))
tracked_til = TrackedTiling(
    til, value_clouds=(((0, 0), (1, 0)),), indices_clouds=(((0, 1),),)
)
print(tracked_til)
for out in TrackedPointPlacement(tracked_til).tracked_point_placement(
    [GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)])], (0,), 0
):
    print(out)
assert TrackedPointPlacement(tracked_til).tracked_point_placement(
    [GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)])], (0,), 0
) == (
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
        value_clouds=(((0, 0), (0, 1), (0, 2), (1, 1), (3, 0), (3, 1), (3, 2)),),
        indices_clouds=(((0, 3), (2, 3)),),
    ),
)


print("=====Fusion=====")
print("-----Fusing Rows 1, 2-----")
til = Tiling([], [], (3, 3))
tracked_til = TrackedTiling(
    til,
    value_clouds=(((0, 0), (1, 0)),),
    indices_clouds=(((0, 1), (0, 2), (1, 2), (1, 1), (2, 1), (2, 2)),),
)
print(tracked_til)
assert tracked_til.is_fusable(True, 1)
fused = tracked_til.fuse(True, 1)
print(fused)
assert fused == TrackedTiling(
    tiling=Tiling((), (), (3, 2)),
    value_clouds=(((0, 0), (1, 0)), ((0, 1), (1, 1), (2, 1))),
    indices_clouds=(((0, 1), (1, 1), (2, 1)),),
)

print("-----Fusing Columns 1, 2-----")
til = Tiling([], [], (3, 3))
tracked_til = TrackedTiling(
    til, value_clouds=(((0, 0), (0, 1)),), indices_clouds=(((0, 2),),)
)
print(tracked_til)
assert tracked_til.is_fusable(False, 1)
fused = tracked_til.fuse(False, 1)
print(fused)
assert fused == TrackedTiling(
    tiling=Tiling((), (), (2, 3)),
    value_clouds=(((0, 0), (0, 1)),),
    indices_clouds=(((0, 2),), ((1, 0), (1, 1), (1, 2))),
)

print("-----Trying to Fuse Columns 1, 2, clounds in the way-----")
til = Tiling([], [], (3, 3))
tracked_til = TrackedTiling(
    til,
    value_clouds=(((0, 0), (1, 0)),),
    indices_clouds=(((0, 1), (0, 2), (1, 2), (1, 1)),),
)
print(tracked_til)
print("Is fusable:", tracked_til.is_fusable(True, 1))
assert not tracked_til.is_fusable(True, 1)
