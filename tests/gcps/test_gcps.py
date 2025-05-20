"""Tests for the GriddedCayleyPerm class in gridded_cayley_permutations.py."""

import pytest

from gridded_cayley_permutations import GriddedCayleyPerm
from cayley_permutations import CayleyPermutation


@pytest.fixture
def empty_gcp():
    """The empty gridded Cayley permutation."""
    return GriddedCayleyPerm(CayleyPermutation([]), [])


@pytest.fixture
def gcp021():
    """A gridded Cayley permutation on a 2x2 grid."""
    return GriddedCayleyPerm(CayleyPermutation([0, 2, 1]), [(0, 0), (1, 1), (1, 0)])


def test_repr(empty_gcp):
    """Test the __repr__ method of the GriddedCayleyPerm class."""
    assert empty_gcp == eval(repr(empty_gcp))


def test_contains_gcps(gcp021: GriddedCayleyPerm):
    """Test the contains method of the GriddedCayleyPerm class."""
    assert gcp021.contains(
        [GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (1, 0)])]
    )
    assert gcp021.contains(
        [GriddedCayleyPerm(CayleyPermutation([1, 0]), [(1, 1), (1, 0)])]
    )
    assert not gcp021.contains(
        [GriddedCayleyPerm(CayleyPermutation([0, 2, 1]), [(0, 0), (1, 0), (1, 0)])]
    )
