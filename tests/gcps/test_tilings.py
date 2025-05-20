"""Tests for the Tiling class in gridded_cayley_permutations.py."""

import pytest

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation


@pytest.fixture
def all_cperms_tiling():
    """The 1x1 tiling which contains all gridded Cayley permutations."""
    return Tiling([], [], (1, 1))


@pytest.fixture
def empty_tiling():
    """The empty tiling."""
    return Tiling((GriddedCayleyPerm(CayleyPermutation(()), ()),), (), (0, 0))


def test_repr(all_cperms_tiling, empty_tiling):
    """Test the __repr__ method of the Tiling class."""
    assert all_cperms_tiling == eval(repr(all_cperms_tiling))
    assert empty_tiling == eval(repr(empty_tiling)) == eval(repr(Tiling.empty_tiling()))
