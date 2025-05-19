from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation

import pytest


@pytest.fixture
def all_cperms_tiling():
    return Tiling([], [], (1, 1))


@pytest.fixture
def empty_tiling():
    return Tiling((GriddedCayleyPerm(CayleyPermutation(()), ()),), (), (0, 0))


def test_repr(all_cperms_tiling, empty_tiling):
    assert all_cperms_tiling == eval(repr(all_cperms_tiling))
    assert empty_tiling == eval(repr(empty_tiling)) == eval(repr(Tiling.empty_tiling()))
