from gridded_cayley_permutations import (
    Tiling,
    GriddedCayleyPerm,
    ObstructionTransitivity,
)
from cayley_permutations import CayleyPermutation


def test_obs_trans1():
    """Test that we can get the obstructions implied by the obstructions of the tiling."""
    tiling = Tiling(
        [
            GriddedCayleyPerm((0, 1), ((1, 0), (1, 1))),
            GriddedCayleyPerm((0, 1), ((1, 1), (1, 2))),
        ],
        [[GriddedCayleyPerm((0,), ((1, 0),))], [GriddedCayleyPerm((0,), ((1, 1),))]],
        (3, 3),
    )

    obstrans = ObstructionTransitivity(tiling)

    assert obstrans.new_obs() == {
        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (1, 2)))
    }


def test_obs_trans2():
    """Test that we can get all the obstructions implied by the obstructions of a larger tiling."""
    tiling = Tiling(
        [
            GriddedCayleyPerm((0, 1), ((0, 0), (1, 0))),
            GriddedCayleyPerm((1, 0), ((0, 0), (1, 0))),
            GriddedCayleyPerm((0, 1), ((1, 0), (2, 0))),
            GriddedCayleyPerm((0, 0), ((0, 0), (1, 0))),
            GriddedCayleyPerm((0, 1), ((1, 0), (1, 1))),
            GriddedCayleyPerm((0, 1), ((1, 1), (1, 2))),
        ],
        [[GriddedCayleyPerm((0,), ((1, 0),))], [GriddedCayleyPerm((0,), ((1, 1),))]],
        (3, 3),
    )

    obstrans = ObstructionTransitivity(tiling)

    assert obstrans.new_obs() == {
        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (1, 2))),
        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (2, 0))),
        GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
        GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (2, 0))),
    }
