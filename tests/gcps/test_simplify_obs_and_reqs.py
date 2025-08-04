from itertools import chain, product
from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
import pytest


def from_old_tiling(obstructions, requirements):
    """
    In the old tilings, active cells are all the cells appearing
    in an input, the dimensions is determined by the maximum of
    this set, the other cells are assumed empty, and empty rows
    and columns are removed."""
    active_cells = set()
    for gp in chain(obstructions, chain.from_iterable(requirements)):
        active_cells.update(gp.positions)
    max_x, max_y = 0, 0
    for x, y in active_cells:
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
    dimensions = (max_x + 1, max_y + 1)
    empty_cells = tuple(
        GriddedCayleyPerm((0,), (cell,))
        for cell in product(range(dimensions[0]), range(dimensions[1]))
        if cell not in active_cells
    )
    tiling = Tiling(tuple(obstructions) + empty_cells, requirements, dimensions)
    print(tiling.remove_empty_rows_and_columns())
    return tiling.remove_empty_rows_and_columns()


def test_duplicate_req_lists():
    a = from_old_tiling(
        obstructions=(
            GriddedCayleyPerm((0, 1, 2), ((0, 0), (0, 1), (0, 1))),
            GriddedCayleyPerm((0, 1, 2), ((0, 0), (0, 1), (0, 2))),
            GriddedCayleyPerm((0, 1, 2), ((0, 0), (0, 2), (0, 2))),
            GriddedCayleyPerm((0, 2, 1), ((0, 0), (0, 0), (1, 0))),
            GriddedCayleyPerm((0, 2, 1), ((0, 0), (1, 2), (1, 0))),
            GriddedCayleyPerm((1, 2, 0), ((0, 1), (0, 1), (0, 1))),
            GriddedCayleyPerm((1, 2, 0), ((0, 1), (0, 2), (0, 1))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (0, 2), (0, 1))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (0, 2), (0, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (0, 2), (1, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (1, 2), (1, 2))),
            GriddedCayleyPerm((1, 2, 0), ((1, 2), (1, 2), (1, 2))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (0, 0), (0, 0), (0, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (0, 0), (0, 1), (0, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (0, 0), (0, 2), (0, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (1, 0), (1, 0), (1, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((1, 0), (1, 0), (1, 0), (1, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((1, 0), (1, 0), (1, 2), (1, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((1, 0), (1, 2), (1, 2), (1, 0))),
        ),
        requirements=(
            (
                GriddedCayleyPerm((0,), ((0, 1),)),
                GriddedCayleyPerm((0,), ((0, 2),)),
                GriddedCayleyPerm((0,), ((1, 2),)),
            ),
        ),
    )
    b = from_old_tiling(
        obstructions=(
            GriddedCayleyPerm((0, 1, 2), ((0, 0), (0, 1), (0, 1))),
            GriddedCayleyPerm((0, 1, 2), ((0, 0), (0, 1), (0, 2))),
            GriddedCayleyPerm((0, 1, 2), ((0, 0), (0, 2), (0, 2))),
            GriddedCayleyPerm((0, 2, 1), ((0, 0), (0, 0), (1, 0))),
            GriddedCayleyPerm((0, 2, 1), ((0, 0), (1, 2), (1, 0))),
            GriddedCayleyPerm((1, 2, 0), ((0, 1), (0, 1), (0, 1))),
            GriddedCayleyPerm((1, 2, 0), ((0, 1), (0, 2), (0, 1))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (0, 2), (0, 1))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (0, 2), (0, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (0, 2), (1, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (1, 2), (1, 2))),
            GriddedCayleyPerm((1, 2, 0), ((1, 2), (1, 2), (1, 2))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (0, 0), (0, 0), (0, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (0, 0), (0, 1), (0, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (0, 0), (0, 2), (0, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (1, 0), (1, 0), (1, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((1, 0), (1, 0), (1, 0), (1, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((1, 0), (1, 0), (1, 2), (1, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((1, 0), (1, 2), (1, 2), (1, 0))),
        ),
        requirements=(
            (
                GriddedCayleyPerm((0,), ((0, 1),)),
                GriddedCayleyPerm((0,), ((0, 2),)),
                GriddedCayleyPerm((0,), ((1, 2),)),
            ),
            (
                GriddedCayleyPerm((0,), ((0, 1),)),
                GriddedCayleyPerm((0,), ((0, 2),)),
                GriddedCayleyPerm((0,), ((1, 2),)),
            ),
        ),
    )

    assert a == b


def test_remove_subset_req():
    a = from_old_tiling(
        obstructions=(
            GriddedCayleyPerm((0, 1, 2), ((0, 0), (0, 1), (0, 1))),
            GriddedCayleyPerm((0, 1, 2), ((0, 0), (0, 1), (0, 2))),
            GriddedCayleyPerm((0, 1, 2), ((0, 0), (0, 2), (0, 2))),
            GriddedCayleyPerm((0, 2, 1), ((0, 0), (0, 0), (1, 0))),
            GriddedCayleyPerm((0, 2, 1), ((0, 0), (1, 2), (1, 0))),
            GriddedCayleyPerm((1, 2, 0), ((0, 1), (0, 1), (0, 1))),
            GriddedCayleyPerm((1, 2, 0), ((0, 1), (0, 2), (0, 1))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (0, 2), (0, 1))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (0, 2), (0, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (0, 2), (1, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (1, 2), (1, 2))),
            GriddedCayleyPerm((1, 2, 0), ((1, 2), (1, 2), (1, 2))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (0, 0), (0, 0), (0, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (0, 0), (0, 1), (0, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (0, 0), (0, 2), (0, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (1, 0), (1, 0), (1, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((1, 0), (1, 0), (1, 0), (1, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((1, 0), (1, 0), (1, 2), (1, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((1, 0), (1, 2), (1, 2), (1, 0))),
        ),
        requirements=(
            (
                GriddedCayleyPerm((0,), ((0, 1),)),
                GriddedCayleyPerm((0,), ((0, 2),)),
            ),
        ),
    )
    b = from_old_tiling(
        obstructions=(
            GriddedCayleyPerm((0, 1, 2), ((0, 0), (0, 1), (0, 1))),
            GriddedCayleyPerm((0, 1, 2), ((0, 0), (0, 1), (0, 2))),
            GriddedCayleyPerm((0, 1, 2), ((0, 0), (0, 2), (0, 2))),
            GriddedCayleyPerm((0, 2, 1), ((0, 0), (0, 0), (1, 0))),
            GriddedCayleyPerm((0, 2, 1), ((0, 0), (1, 2), (1, 0))),
            GriddedCayleyPerm((1, 2, 0), ((0, 1), (0, 1), (0, 1))),
            GriddedCayleyPerm((1, 2, 0), ((0, 1), (0, 2), (0, 1))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (0, 2), (0, 1))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (0, 2), (0, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (0, 2), (1, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (1, 2), (1, 2))),
            GriddedCayleyPerm((1, 2, 0), ((1, 2), (1, 2), (1, 2))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (0, 0), (0, 0), (0, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (0, 0), (0, 1), (0, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (0, 0), (0, 2), (0, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (1, 0), (1, 0), (1, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((1, 0), (1, 0), (1, 0), (1, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((1, 0), (1, 0), (1, 2), (1, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((1, 0), (1, 2), (1, 2), (1, 0))),
        ),
        requirements=(
            (
                GriddedCayleyPerm((0,), ((0, 1),)),
                GriddedCayleyPerm((0,), ((0, 2),)),
            ),
            (
                GriddedCayleyPerm((0,), ((0, 1),)),
                GriddedCayleyPerm((0,), ((0, 2),)),
                GriddedCayleyPerm((0,), ((1, 2),)),
            ),
        ),
    )

    assert a == b


@pytest.mark.skip("see minimal_obs in tilings/algorithms/gridded_perm_reduction.py")
def test_req_list_implies_empty():
    tiling = from_old_tiling(
        obstructions=(
            GriddedCayleyPerm((0, 1), ((0, 0), (0, 1))),
            GriddedCayleyPerm((0, 1), ((0, 0), (1, 2))),
            GriddedCayleyPerm((0, 1), ((0, 0), (1, 3))),
            GriddedCayleyPerm((0, 1), ((0, 3), (0, 3))),
            GriddedCayleyPerm((0, 1), ((0, 3), (1, 3))),
            GriddedCayleyPerm((0, 1), ((1, 3), (1, 3))),
            GriddedCayleyPerm((0, 1, 2), ((0, 0), (0, 2), (0, 2))),
            GriddedCayleyPerm((0, 1, 2), ((0, 0), (0, 2), (0, 3))),
            GriddedCayleyPerm((0, 1, 2), ((0, 1), (0, 2), (0, 2))),
            GriddedCayleyPerm((0, 1, 2), ((0, 1), (0, 2), (0, 3))),
            GriddedCayleyPerm((0, 1, 2), ((1, 0), (1, 2), (1, 2))),
            GriddedCayleyPerm((0, 1, 2), ((1, 0), (1, 2), (1, 3))),
            GriddedCayleyPerm((0, 2, 1), ((0, 0), (0, 0), (1, 0))),
            GriddedCayleyPerm((0, 2, 1), ((0, 0), (0, 0), (2, 0))),
            GriddedCayleyPerm((0, 2, 1), ((0, 0), (1, 0), (2, 0))),
            GriddedCayleyPerm((0, 2, 1), ((0, 0), (2, 2), (2, 0))),
            GriddedCayleyPerm((0, 2, 1), ((0, 0), (2, 3), (2, 0))),
            GriddedCayleyPerm((0, 2, 1), ((1, 0), (1, 0), (2, 0))),
            GriddedCayleyPerm((0, 2, 1), ((1, 0), (2, 2), (2, 0))),
            GriddedCayleyPerm((0, 2, 1), ((1, 0), (2, 3), (2, 0))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (0, 2), (0, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (0, 2), (1, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (0, 2), (2, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (0, 3), (0, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (0, 3), (1, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (0, 3), (2, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (1, 2), (1, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (1, 2), (2, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (1, 3), (1, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (1, 3), (2, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (2, 2), (2, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 2), (2, 3), (2, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 3), (2, 3), (2, 2))),
            GriddedCayleyPerm((1, 2, 0), ((0, 3), (2, 3), (2, 3))),
            GriddedCayleyPerm((1, 2, 0), ((1, 2), (1, 2), (1, 2))),
            GriddedCayleyPerm((1, 2, 0), ((1, 2), (1, 2), (2, 2))),
            GriddedCayleyPerm((1, 2, 0), ((1, 2), (1, 3), (1, 2))),
            GriddedCayleyPerm((1, 2, 0), ((1, 2), (1, 3), (2, 2))),
            GriddedCayleyPerm((1, 2, 0), ((1, 2), (2, 2), (2, 2))),
            GriddedCayleyPerm((1, 2, 0), ((1, 2), (2, 3), (2, 2))),
            GriddedCayleyPerm((1, 2, 0), ((1, 3), (2, 3), (2, 2))),
            GriddedCayleyPerm((1, 2, 0), ((1, 3), (2, 3), (2, 3))),
            GriddedCayleyPerm((1, 2, 0), ((2, 2), (2, 2), (2, 2))),
            GriddedCayleyPerm((1, 2, 0), ((2, 2), (2, 3), (2, 2))),
            GriddedCayleyPerm((1, 2, 0), ((2, 3), (2, 3), (2, 2))),
            GriddedCayleyPerm((1, 2, 0), ((2, 3), (2, 3), (2, 3))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (0, 0), (0, 0), (0, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (0, 0), (0, 2), (0, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (0, 0), (0, 3), (0, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (1, 0), (1, 0), (1, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 0), (2, 0), (2, 0), (2, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 1), (0, 1), (0, 1), (0, 1))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 1), (0, 1), (0, 2), (0, 1))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 1), (0, 1), (0, 3), (0, 1))),
            GriddedCayleyPerm((0, 2, 3, 1), ((1, 0), (1, 0), (1, 0), (1, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((1, 0), (1, 0), (1, 2), (1, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((1, 0), (1, 0), (1, 3), (1, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((1, 0), (2, 0), (2, 0), (2, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((2, 0), (2, 0), (2, 0), (2, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((2, 0), (2, 0), (2, 2), (2, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((2, 0), (2, 0), (2, 3), (2, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((2, 0), (2, 2), (2, 2), (2, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((2, 0), (2, 2), (2, 3), (2, 0))),
            GriddedCayleyPerm((0, 2, 3, 1), ((2, 0), (2, 3), (2, 3), (2, 0))),
        ),
        requirements=(
            (
                GriddedCayleyPerm((0,), ((0, 3),)),
                GriddedCayleyPerm((0,), ((1, 3),)),
                GriddedCayleyPerm((0,), ((2, 3),)),
            ),
            (GriddedCayleyPerm((0,), ((1, 2),)), GriddedCayleyPerm((0,), ((1, 3),))),
            (GriddedCayleyPerm((0,), ((2, 2),)),),
        ),
    )
    assert (0, 0) not in tiling.active_cells


@pytest.mark.skip("see minimal_obs in tilings/algorithms/gridded_perm_reduction.py")
def test_reduce_but_keep_bigger_sub_ob():
    obs1 = GriddedCayleyPerm((0, 1), ((0, 0), (1, 2)))
    obs2 = GriddedCayleyPerm((1, 0, 2), ((0, 0), (0, 0), (2, 1)))
    req1 = GriddedCayleyPerm((0,), ((1, 2),))
    req2 = GriddedCayleyPerm((0,), ((2, 1),))
    t = from_old_tiling([obs1, obs2], [[req1, req2]])
    expected = from_old_tiling(
        obstructions=(
            GriddedCayleyPerm((0, 1), ((0, 0), (1, 2))),
            GriddedCayleyPerm((1, 0), ((0, 0), (0, 0))),
        ),
        requirements=(
            (GriddedCayleyPerm((0,), ((1, 2),)), GriddedCayleyPerm((0,), ((2, 1),))),
        ),
    )
    assert t == expected


@pytest.mark.skip("see minimal_obs in tilings/algorithms/gridded_perm_reduction.py")
def test_reduce_to_join_of_subobs():
    obs1 = GriddedCayleyPerm((0, 1, 2), ((0, 0), (1, 2), (3, 3)))
    obs2 = GriddedCayleyPerm((0, 1, 2), ((0, 0), (2, 1), (3, 3)))
    req1 = GriddedCayleyPerm((0, 1), ((1, 2), (3, 3)))
    req2 = GriddedCayleyPerm((0, 1), ((0, 0), (2, 1)))
    t = from_old_tiling([obs1, obs2], [[req1, req2]])
    expected = from_old_tiling(
        obstructions=(GriddedCayleyPerm((0, 1), ((0, 0), (3, 3))),),
        requirements=(
            (
                GriddedCayleyPerm((0, 1), ((0, 0), (2, 1))),
                GriddedCayleyPerm((0, 1), ((1, 2), (3, 3))),
            ),
        ),
    )
    assert t == expected


def test_minimal_req_duplicate():
    assert from_old_tiling(
        obstructions=(
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 1), (0, 1), (0, 1), (1, 1))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 1), (0, 1), (1, 1), (1, 1))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 1), (1, 1), (1, 1), (1, 1))),
            GriddedCayleyPerm((0, 3, 2, 1), ((0, 1), (0, 1), (0, 1), (1, 1))),
            GriddedCayleyPerm((0, 3, 2, 1), ((0, 1), (0, 1), (1, 1), (1, 1))),
            GriddedCayleyPerm((0, 3, 2, 1), ((0, 1), (1, 1), (1, 1), (1, 1))),
            GriddedCayleyPerm((1, 0, 2, 3), ((1, 0), (1, 0), (1, 1), (1, 1))),
            GriddedCayleyPerm((1, 0, 3, 2), ((1, 0), (1, 0), (1, 1), (1, 1))),
            GriddedCayleyPerm((1, 2, 0, 3), ((1, 0), (1, 1), (1, 0), (1, 1))),
            GriddedCayleyPerm((1, 2, 3, 0), ((1, 0), (1, 1), (1, 1), (1, 0))),
            GriddedCayleyPerm((1, 3, 0, 2), ((1, 0), (1, 1), (1, 0), (1, 1))),
            GriddedCayleyPerm((1, 3, 2, 0), ((1, 0), (1, 1), (1, 1), (1, 0))),
            GriddedCayleyPerm((2, 0, 3, 1), ((0, 1), (0, 1), (0, 1), (1, 1))),
            GriddedCayleyPerm((2, 0, 3, 1), ((0, 1), (0, 1), (1, 1), (1, 1))),
            GriddedCayleyPerm((2, 1, 0, 3), ((0, 1), (1, 0), (1, 0), (1, 1))),
            GriddedCayleyPerm((2, 1, 0, 3), ((1, 1), (1, 0), (1, 0), (1, 1))),
            GriddedCayleyPerm((2, 1, 3, 0), ((0, 1), (1, 0), (1, 1), (1, 0))),
            GriddedCayleyPerm((2, 1, 3, 0), ((1, 1), (1, 0), (1, 1), (1, 0))),
            GriddedCayleyPerm(
                (1, 0, 3, 4, 2), ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1))
            ),
            GriddedCayleyPerm(
                (1, 0, 3, 4, 2), ((1, 0), (1, 0), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 0, 3, 4, 2), ((1, 0), (1, 0), (1, 0), (1, 1), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 0, 3, 4, 2), ((1, 1), (1, 0), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 0, 3, 4, 2), ((1, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 0, 4, 3, 2), ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1))
            ),
            GriddedCayleyPerm(
                (1, 0, 4, 3, 2), ((1, 0), (1, 0), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 0, 4, 3, 2), ((1, 0), (1, 0), (1, 1), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 0, 4, 3, 2), ((1, 1), (1, 0), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 0, 4, 3, 2), ((1, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 3, 0, 4, 2), ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1))
            ),
            GriddedCayleyPerm(
                (1, 3, 0, 4, 2), ((1, 0), (1, 0), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 3, 0, 4, 2), ((1, 0), (1, 0), (1, 0), (1, 1), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 3, 0, 4, 2), ((1, 1), (1, 1), (1, 0), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 3, 0, 4, 2), ((1, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 3, 4, 0, 2), ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1))
            ),
            GriddedCayleyPerm(
                (1, 3, 4, 0, 2), ((1, 0), (1, 0), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 3, 4, 0, 2), ((1, 0), (1, 0), (1, 1), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 3, 4, 0, 2), ((1, 1), (1, 1), (1, 1), (1, 0), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 3, 4, 0, 2), ((1, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 4, 0, 3, 2), ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1))
            ),
            GriddedCayleyPerm(
                (1, 4, 0, 3, 2), ((1, 0), (1, 0), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 4, 0, 3, 2), ((1, 0), (1, 1), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 4, 0, 3, 2), ((1, 1), (1, 1), (1, 0), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 4, 0, 3, 2), ((1, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 4, 3, 0, 2), ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1))
            ),
            GriddedCayleyPerm(
                (1, 4, 3, 0, 2), ((1, 0), (1, 0), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 4, 3, 0, 2), ((1, 0), (1, 1), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 4, 3, 0, 2), ((1, 1), (1, 1), (1, 1), (1, 0), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 4, 3, 0, 2), ((1, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 0, 4, 2), ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 0, 4, 2), ((0, 1), (1, 1), (1, 0), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 0, 4, 2), ((0, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 0, 4, 2), ((1, 0), (1, 0), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (3, 1, 0, 4, 2), ((1, 0), (1, 0), (1, 0), (1, 1), (1, 0))
            ),
            GriddedCayleyPerm(
                (3, 1, 0, 4, 2), ((1, 1), (1, 1), (1, 0), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 0, 4, 2), ((1, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 4, 0, 2), ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 4, 0, 2), ((0, 1), (1, 1), (1, 1), (1, 0), (1, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 4, 0, 2), ((0, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 4, 0, 2), ((1, 0), (1, 0), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (3, 1, 4, 0, 2), ((1, 0), (1, 0), (1, 1), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (3, 1, 4, 0, 2), ((1, 1), (1, 1), (1, 1), (1, 0), (1, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 4, 0, 2), ((1, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
        ),
        requirements=((GriddedCayleyPerm((1, 0), ((1, 0), (1, 0))),),),
    ) == from_old_tiling(
        obstructions=(
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 1), (0, 1), (0, 1), (1, 1))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 1), (0, 1), (1, 1), (1, 1))),
            GriddedCayleyPerm((0, 2, 3, 1), ((0, 1), (1, 1), (1, 1), (1, 1))),
            GriddedCayleyPerm((0, 3, 2, 1), ((0, 1), (0, 1), (0, 1), (1, 1))),
            GriddedCayleyPerm((0, 3, 2, 1), ((0, 1), (0, 1), (1, 1), (1, 1))),
            GriddedCayleyPerm((0, 3, 2, 1), ((0, 1), (1, 1), (1, 1), (1, 1))),
            GriddedCayleyPerm((1, 0, 2, 3), ((1, 0), (1, 0), (1, 1), (1, 1))),
            GriddedCayleyPerm((1, 0, 3, 2), ((1, 0), (1, 0), (1, 1), (1, 1))),
            GriddedCayleyPerm((1, 2, 0, 3), ((1, 0), (1, 1), (1, 0), (1, 1))),
            GriddedCayleyPerm((1, 2, 3, 0), ((1, 0), (1, 1), (1, 1), (1, 0))),
            GriddedCayleyPerm((1, 3, 0, 2), ((1, 0), (1, 1), (1, 0), (1, 1))),
            GriddedCayleyPerm((1, 3, 2, 0), ((1, 0), (1, 1), (1, 1), (1, 0))),
            GriddedCayleyPerm((2, 0, 3, 1), ((0, 1), (0, 1), (0, 1), (1, 1))),
            GriddedCayleyPerm((2, 0, 3, 1), ((0, 1), (0, 1), (1, 1), (1, 1))),
            GriddedCayleyPerm((2, 1, 0, 3), ((0, 1), (1, 0), (1, 0), (1, 1))),
            GriddedCayleyPerm((2, 1, 0, 3), ((1, 1), (1, 0), (1, 0), (1, 1))),
            GriddedCayleyPerm((2, 1, 3, 0), ((0, 1), (1, 0), (1, 1), (1, 0))),
            GriddedCayleyPerm((2, 1, 3, 0), ((1, 1), (1, 0), (1, 1), (1, 0))),
            GriddedCayleyPerm(
                (1, 0, 3, 4, 2), ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1))
            ),
            GriddedCayleyPerm(
                (1, 0, 3, 4, 2), ((1, 0), (1, 0), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 0, 3, 4, 2), ((1, 0), (1, 0), (1, 0), (1, 1), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 0, 3, 4, 2), ((1, 1), (1, 0), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 0, 3, 4, 2), ((1, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 0, 4, 3, 2), ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1))
            ),
            GriddedCayleyPerm(
                (1, 0, 4, 3, 2), ((1, 0), (1, 0), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 0, 4, 3, 2), ((1, 0), (1, 0), (1, 1), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 0, 4, 3, 2), ((1, 1), (1, 0), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 0, 4, 3, 2), ((1, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 3, 0, 4, 2), ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1))
            ),
            GriddedCayleyPerm(
                (1, 3, 0, 4, 2), ((1, 0), (1, 0), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 3, 0, 4, 2), ((1, 0), (1, 0), (1, 0), (1, 1), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 3, 0, 4, 2), ((1, 1), (1, 1), (1, 0), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 3, 0, 4, 2), ((1, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 3, 4, 0, 2), ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1))
            ),
            GriddedCayleyPerm(
                (1, 3, 4, 0, 2), ((1, 0), (1, 0), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 3, 4, 0, 2), ((1, 0), (1, 0), (1, 1), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 3, 4, 0, 2), ((1, 1), (1, 1), (1, 1), (1, 0), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 3, 4, 0, 2), ((1, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 4, 0, 3, 2), ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1))
            ),
            GriddedCayleyPerm(
                (1, 4, 0, 3, 2), ((1, 0), (1, 0), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 4, 0, 3, 2), ((1, 0), (1, 1), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 4, 0, 3, 2), ((1, 1), (1, 1), (1, 0), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 4, 0, 3, 2), ((1, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 4, 3, 0, 2), ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1))
            ),
            GriddedCayleyPerm(
                (1, 4, 3, 0, 2), ((1, 0), (1, 0), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 4, 3, 0, 2), ((1, 0), (1, 1), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (1, 4, 3, 0, 2), ((1, 1), (1, 1), (1, 1), (1, 0), (1, 1))
            ),
            GriddedCayleyPerm(
                (1, 4, 3, 0, 2), ((1, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 0, 4, 2), ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 0, 4, 2), ((0, 1), (1, 1), (1, 0), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 0, 4, 2), ((0, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 0, 4, 2), ((1, 0), (1, 0), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (3, 1, 0, 4, 2), ((1, 0), (1, 0), (1, 0), (1, 1), (1, 0))
            ),
            GriddedCayleyPerm(
                (3, 1, 0, 4, 2), ((1, 1), (1, 1), (1, 0), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 0, 4, 2), ((1, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 4, 0, 2), ((0, 1), (0, 1), (0, 1), (0, 1), (0, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 4, 0, 2), ((0, 1), (1, 1), (1, 1), (1, 0), (1, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 4, 0, 2), ((0, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 4, 0, 2), ((1, 0), (1, 0), (1, 0), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (3, 1, 4, 0, 2), ((1, 0), (1, 0), (1, 1), (1, 0), (1, 0))
            ),
            GriddedCayleyPerm(
                (3, 1, 4, 0, 2), ((1, 1), (1, 1), (1, 1), (1, 0), (1, 1))
            ),
            GriddedCayleyPerm(
                (3, 1, 4, 0, 2), ((1, 1), (1, 1), (1, 1), (1, 1), (1, 1))
            ),
        ),
        requirements=((GriddedCayleyPerm((1, 0), ((1, 0), (1, 0))),),),
    )
