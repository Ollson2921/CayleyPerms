"""Test for MeshPattern class"""

import pytest

from mesh_patterns import MeshPattern


@pytest.fixture
def mp1():
    cperm = (0, 1, 2, 1)
    cells = [(0, 2), (1, 3), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3)]
    return MeshPattern(cperm, cells)


@pytest.fixture
def mp2():
    return MeshPattern(
        (0, 2, 1), [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)]
    )


def test_ascii_plot(mp1, mp2):
    assert (
        mp1.ascii_plot()
        == " | | | |\n-+-+-●-+-\n | |x| |\n-+x●x+x●-\nx| | |x|\n-●-+-+x+-\n | | |x|"
    )
    assert (
        mp2.ascii_plot() == " | |x|\n-+-●x+-\n | |x|\n-+-+x●-\n | |x|\n-●-+x+-\n | |x|"
    )


def test_sub_pattern(mp1):
    assert mp1.sub_mesh_pattern([0, 3]) == MeshPattern((0, 1), [(0, 2)])
    assert mp1.sub_mesh_pattern([0, 1]) == MeshPattern((0, 1), [(0, 2), (1, 3)])
    assert mp1.sub_mesh_pattern([2, 3]) == MeshPattern((1, 0), [(1, 0), (1, 1)])
    assert mp1.sub_mesh_pattern([0, 1, 2]) == MeshPattern(
        (0, 1, 2), [(0, 2), (1, 3), (2, 3), (2, 4)]
    )


def test_row_col_bounds(mp1):
    assert mp1.row_col_bounds([2, 3]) == (
        ((0, 3), (3, 4), (4, 5), (5, 6), (6, 7)),
        (
            (0, 3),
            (3, 4),
            (4, 5),
        ),
    )


def test_avoid_and_contains(mp2):
    cperm = (0, 2, 1)
    assert not mp2.is_avoided_by_word(cperm)
    cperm = (1, 3, 0, 2)
    assert mp2.is_avoided_by_word(cperm)


def test_lt():
    mp1 = MeshPattern((0, 1, 0), frozenset())
    mp2 = MeshPattern((0, 0), frozenset())
    assert mp2 < mp1
    assert mp2 <= mp1
