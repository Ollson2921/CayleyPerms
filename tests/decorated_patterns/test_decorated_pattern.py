from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from decorated_patterns import DecoratedPattern
import pytest


@pytest.fixture
def dp1():
    return DecoratedPattern(
        (0, 1),
        [
            GriddedCayleyPerm((1, 0), ((0, 2), (0, 2))),
            GriddedCayleyPerm((1, 0), ((0, 4), (0, 2))),
            GriddedCayleyPerm((1, 0), ((0, 4), (0, 4))),
        ],
    )


def test_tiling(dp1):
    assert dp1.tiling == Tiling(
        (
            GriddedCayleyPerm((0,), ((1, 0),)),
            GriddedCayleyPerm((0,), ((1, 2),)),
            GriddedCayleyPerm((0,), ((1, 4),)),
            GriddedCayleyPerm((0,), ((3, 0),)),
            GriddedCayleyPerm((0,), ((3, 2),)),
            GriddedCayleyPerm((0,), ((3, 4),)),
            GriddedCayleyPerm((0, 0), ((1, 1), (1, 1))),
            GriddedCayleyPerm((0, 0), ((3, 3), (3, 3))),
            GriddedCayleyPerm((0, 1), ((0, 1), (0, 1))),
            GriddedCayleyPerm((0, 1), ((0, 1), (1, 1))),
            GriddedCayleyPerm((0, 1), ((0, 1), (2, 1))),
            GriddedCayleyPerm((0, 1), ((0, 1), (3, 1))),
            GriddedCayleyPerm((0, 1), ((0, 1), (4, 1))),
            GriddedCayleyPerm((0, 1), ((0, 3), (0, 3))),
            GriddedCayleyPerm((0, 1), ((0, 3), (1, 3))),
            GriddedCayleyPerm((0, 1), ((0, 3), (2, 3))),
            GriddedCayleyPerm((0, 1), ((0, 3), (3, 3))),
            GriddedCayleyPerm((0, 1), ((0, 3), (4, 3))),
            GriddedCayleyPerm((0, 1), ((1, 1), (1, 1))),
            GriddedCayleyPerm((0, 1), ((1, 1), (2, 1))),
            GriddedCayleyPerm((0, 1), ((1, 1), (3, 1))),
            GriddedCayleyPerm((0, 1), ((1, 1), (4, 1))),
            GriddedCayleyPerm((0, 1), ((1, 3), (1, 3))),
            GriddedCayleyPerm((0, 1), ((1, 3), (2, 3))),
            GriddedCayleyPerm((0, 1), ((1, 3), (3, 3))),
            GriddedCayleyPerm((0, 1), ((1, 3), (4, 3))),
            GriddedCayleyPerm((0, 1), ((2, 1), (2, 1))),
            GriddedCayleyPerm((0, 1), ((2, 1), (3, 1))),
            GriddedCayleyPerm((0, 1), ((2, 1), (4, 1))),
            GriddedCayleyPerm((0, 1), ((2, 3), (2, 3))),
            GriddedCayleyPerm((0, 1), ((2, 3), (3, 3))),
            GriddedCayleyPerm((0, 1), ((2, 3), (4, 3))),
            GriddedCayleyPerm((0, 1), ((3, 1), (3, 1))),
            GriddedCayleyPerm((0, 1), ((3, 1), (4, 1))),
            GriddedCayleyPerm((0, 1), ((3, 3), (3, 3))),
            GriddedCayleyPerm((0, 1), ((3, 3), (4, 3))),
            GriddedCayleyPerm((0, 1), ((4, 1), (4, 1))),
            GriddedCayleyPerm((0, 1), ((4, 3), (4, 3))),
            GriddedCayleyPerm((1, 0), ((0, 1), (0, 1))),
            GriddedCayleyPerm((1, 0), ((0, 1), (1, 1))),
            GriddedCayleyPerm((1, 0), ((0, 1), (2, 1))),
            GriddedCayleyPerm((1, 0), ((0, 1), (3, 1))),
            GriddedCayleyPerm((1, 0), ((0, 1), (4, 1))),
            GriddedCayleyPerm((1, 0), ((0, 2), (0, 2))),
            GriddedCayleyPerm((1, 0), ((0, 3), (0, 3))),
            GriddedCayleyPerm((1, 0), ((0, 3), (1, 3))),
            GriddedCayleyPerm((1, 0), ((0, 3), (2, 3))),
            GriddedCayleyPerm((1, 0), ((0, 3), (3, 3))),
            GriddedCayleyPerm((1, 0), ((0, 3), (4, 3))),
            GriddedCayleyPerm((1, 0), ((0, 4), (0, 2))),
            GriddedCayleyPerm((1, 0), ((0, 4), (0, 4))),
            GriddedCayleyPerm((1, 0), ((1, 1), (1, 1))),
            GriddedCayleyPerm((1, 0), ((1, 1), (2, 1))),
            GriddedCayleyPerm((1, 0), ((1, 1), (3, 1))),
            GriddedCayleyPerm((1, 0), ((1, 1), (4, 1))),
            GriddedCayleyPerm((1, 0), ((1, 3), (1, 3))),
            GriddedCayleyPerm((1, 0), ((1, 3), (2, 3))),
            GriddedCayleyPerm((1, 0), ((1, 3), (3, 3))),
            GriddedCayleyPerm((1, 0), ((1, 3), (4, 3))),
            GriddedCayleyPerm((1, 0), ((2, 1), (2, 1))),
            GriddedCayleyPerm((1, 0), ((2, 1), (3, 1))),
            GriddedCayleyPerm((1, 0), ((2, 1), (4, 1))),
            GriddedCayleyPerm((1, 0), ((2, 3), (2, 3))),
            GriddedCayleyPerm((1, 0), ((2, 3), (3, 3))),
            GriddedCayleyPerm((1, 0), ((2, 3), (4, 3))),
            GriddedCayleyPerm((1, 0), ((3, 1), (3, 1))),
            GriddedCayleyPerm((1, 0), ((3, 1), (4, 1))),
            GriddedCayleyPerm((1, 0), ((3, 3), (3, 3))),
            GriddedCayleyPerm((1, 0), ((3, 3), (4, 3))),
            GriddedCayleyPerm((1, 0), ((4, 1), (4, 1))),
            GriddedCayleyPerm((1, 0), ((4, 3), (4, 3))),
        ),
        (
            (GriddedCayleyPerm((0,), ((1, 1),)),),
            (GriddedCayleyPerm((0,), ((3, 3),)),),
        ),
        (5, 5),
    )
    assert len(dp1.extra_obs) == 3
    assert dp1.dimensions == (5, 5)


def test_gridding_of_occurrence(dp1):
    word = (3, 2, 0, 1)
    assert dp1._col_values(word, [2, 3]) == [(0, 2), (2, 3), (3, 3), (3, 4), (4, 4)]
    assert dp1._row_values(word, [2, 3]) == [(0, 0), (0, 1), (1, 1), (1, 2), (2, 4)]
    assert dp1.gridding_of_occurrence(word, [2, 3]) == ((0, 4), (0, 4), (1, 1), (3, 3))
    assert list(dp1.occurrences_in_word(word)) == []
    assert dp1.avoided_by_word(word)
    assert not dp1.contained_by_word(word)
    word = (3, 1, 0, 2)
    assert dp1._col_values(word, [2, 3]) == [(0, 2), (2, 3), (3, 3), (3, 4), (4, 4)]
    assert dp1._row_values(word, [2, 3]) == [(0, 0), (0, 1), (1, 2), (2, 3), (3, 4)]
    assert dp1.gridding_of_occurrence(word, [2, 3]) == ((0, 4), (0, 2), (1, 1), (3, 3))
    assert list(dp1.occurrences_in_word(word)) == [(1, 3)]
    assert dp1.contained_by_word(word)
    assert not dp1.avoided_by_word(word)
    word = (2, 3, 0, 1)
    assert list(dp1.occurrences_in_word(word)) == [(0, 1), (2, 3)]
    assert dp1.contained_by_word(word)
    assert not dp1.avoided_by_word(word)
    word = (1, 3, 0, 2)
    assert list(dp1.occurrences_in_word(word)) == [(0, 1), (0, 3), (2, 3)]
    assert dp1.contained_by_word(word)
    assert not dp1.avoided_by_word(word)
