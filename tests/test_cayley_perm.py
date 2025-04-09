"""Tests for the CayleyPermutation class."""

import random
import pytest
from cayley_permutations import CayleyPermutation


def test_init_method():
    """Tests the init method."""
    cperm1 = CayleyPermutation([0, 1, 2, 3])
    assert cperm1 == CayleyPermutation((0, 1, 2, 3))
    assert cperm1.cperm == (0, 1, 2, 3)
    assert CayleyPermutation(cperm1) == cperm1

    with pytest.raises(TypeError):
        CayleyPermutation(123)


def test_one_based():
    assert CayleyPermutation.from_one_based((4, 1, 3, 2)) == CayleyPermutation(
        (3, 0, 2, 1)
    )
    assert CayleyPermutation.from_one_based((1,)) == CayleyPermutation((0,))
    assert CayleyPermutation.from_one_based([]) == CayleyPermutation([])

    for _ in range(100):
        p = list(range(1, random.randint(2, 20)))
        random.shuffle(p)
        assert CayleyPermutation.from_one_based(p) == CayleyPermutation(
            [i - 1 for i in p]
        )


def test_left_floor_and_ceiling_permuta_tests():
    iterable = CayleyPermutation([4, 5, 1, 2, 3, 6])
    expected = [
        (-1, -1),  # 4
        (0, -1),  # 5
        (-1, 0),  # 1
        (2, 0),  # 2
        (3, 0),  # 3
        (1, -1),  # 6
    ]
    index = 0
    for fac in iterable._left_floor_and_ceiling():
        assert fac == expected[index]
        index += 1

    iterable = CayleyPermutation([4, 1, 2, 5, 3])
    expected = [(-1, -1), (-1, 0), (1, 0), (0, -1), (2, 0)]  # 4  # 1  # 2  # 5  # 3
    index = 0
    for fac in iterable._left_floor_and_ceiling():
        assert fac == expected[index]
        index += 1

    iterable = CayleyPermutation([1, 2, 3])
    expected = [(-1, -1), (0, -1), (1, -1)]  # 1  # 2  # 3
    index = 0
    for fac in iterable._left_floor_and_ceiling():
        assert fac == expected[index]
        index += 1

    iterable = CayleyPermutation([3, 2, 1])
    expected = [(-1, -1), (-1, 0), (-1, 1)]  # 3  # 2  # 1
    index = 0
    for fac in iterable._left_floor_and_ceiling():
        assert fac == expected[index]
        index += 1
    assert list(CayleyPermutation(())._left_floor_and_ceiling()) == []
    assert list(CayleyPermutation((0,))._left_floor_and_ceiling()) == [(-1, -1)]
    assert list(CayleyPermutation((0, 1))._left_floor_and_ceiling()) == [
        (-1, -1),
        (0, -1),
    ]
    assert list(CayleyPermutation((1, 0))._left_floor_and_ceiling()) == [
        (-1, -1),
        (-1, 0),
    ]
    assert list(CayleyPermutation((2, 1, 0, 3))._left_floor_and_ceiling()) == [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
    ]
    assert list(CayleyPermutation((3, 2, 0, 1))._left_floor_and_ceiling()) == [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (2, 1),
    ]
    assert list(CayleyPermutation((0, 4, 1, 2, 3))._left_floor_and_ceiling()) == [
        (-1, -1),
        (0, -1),
        (0, 1),
        (2, 1),
        (3, 1),
    ]
    assert list(CayleyPermutation((1, 2, 4, 3, 0))._left_floor_and_ceiling()) == [
        (-1, -1),
        (0, -1),
        (1, -1),
        (1, 2),
        (-1, 0),
    ]
    assert list(CayleyPermutation((3, 0, 2, 5, 1, 4))._left_floor_and_ceiling()) == [
        (-1, -1),
        (-1, 0),
        (1, 0),
        (0, -1),
        (1, 2),
        (0, 3),
    ]
    assert list(CayleyPermutation((2, 5, 0, 3, 4, 1))._left_floor_and_ceiling()) == [
        (-1, -1),
        (0, -1),
        (-1, 0),
        (0, 1),
        (3, 1),
        (2, 0),
    ]
    assert list(CayleyPermutation((6, 5, 0, 2, 1, 3, 4))._left_floor_and_ceiling()) == [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (2, 1),
        (2, 3),
        (3, 1),
        (5, 1),
    ]
    assert list(CayleyPermutation((0, 2, 6, 5, 4, 1, 3))._left_floor_and_ceiling()) == [
        (-1, -1),
        (0, -1),
        (1, -1),
        (1, 2),
        (1, 3),
        (0, 1),
        (1, 4),
    ]
    assert list(
        CayleyPermutation((3, 6, 2, 7, 5, 0, 1, 4))._left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (0, -1),
        (-1, 0),
        (1, -1),
        (0, 1),
        (-1, 2),
        (5, 2),
        (0, 4),
    ]
    assert list(
        CayleyPermutation((2, 0, 5, 6, 1, 7, 4, 3))._left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (-1, 0),
        (0, -1),
        (2, -1),
        (1, 0),
        (3, -1),
        (0, 2),
        (0, 6),
    ]
    assert list(
        CayleyPermutation((8, 5, 0, 7, 1, 2, 4, 6, 3))._left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (1, 0),
        (2, 1),
        (4, 1),
        (5, 1),
        (1, 3),
        (5, 6),
    ]
    assert list(
        CayleyPermutation((0, 3, 7, 8, 2, 6, 4, 5, 1))._left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (0, -1),
        (1, -1),
        (2, -1),
        (0, 1),
        (1, 2),
        (1, 5),
        (6, 5),
        (0, 4),
    ]
    assert list(
        CayleyPermutation((5, 3, 4, 1, 7, 9, 0, 6, 8, 2))._left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (-1, 0),
        (1, 0),
        (-1, 1),
        (0, -1),
        (4, -1),
        (-1, 3),
        (0, 4),
        (4, 5),
        (3, 1),
    ]
    assert list(
        CayleyPermutation((9, 2, 0, 5, 3, 6, 1, 8, 7, 4))._left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (1, 0),
        (1, 3),
        (3, 0),
        (2, 1),
        (5, 0),
        (5, 7),
        (4, 3),
    ]
    assert list(
        CayleyPermutation((9, 0, 6, 2, 3, 1, 4, 5, 7, 8, 10))._left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (-1, 0),
        (1, 0),
        (1, 2),
        (3, 2),
        (1, 3),
        (4, 2),
        (6, 2),
        (2, 0),
        (8, 0),
        (0, -1),
    ]
    assert list(
        CayleyPermutation((10, 0, 1, 2, 3, 5, 7, 6, 4, 8, 9))._left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (-1, 0),
        (1, 0),
        (2, 0),
        (3, 0),
        (4, 0),
        (5, 0),
        (5, 6),
        (4, 5),
        (6, 0),
        (9, 0),
    ]
    assert list(
        CayleyPermutation(
            (4, 10, 11, 3, 9, 7, 2, 8, 6, 1, 5, 0)
        )._left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (0, -1),
        (1, -1),
        (-1, 0),
        (0, 1),
        (0, 4),
        (-1, 3),
        (5, 4),
        (0, 5),
        (-1, 6),
        (0, 8),
        (-1, 9),
    ]
    assert list(
        CayleyPermutation(
            (3, 4, 11, 8, 9, 10, 0, 2, 5, 1, 7, 6)
        )._left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (0, -1),
        (1, -1),
        (1, 2),
        (3, 2),
        (4, 2),
        (-1, 0),
        (6, 0),
        (1, 3),
        (6, 7),
        (8, 3),
        (8, 10),
    ]
    assert list(
        CayleyPermutation(
            (2, 9, 8, 4, 1, 5, 10, 12, 7, 3, 11, 0, 6)
        )._left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (0, -1),
        (0, 1),
        (0, 2),
        (-1, 0),
        (3, 2),
        (1, -1),
        (6, -1),
        (5, 2),
        (0, 3),
        (6, 7),
        (-1, 4),
        (5, 8),
    ]
    assert list(
        CayleyPermutation(
            (7, 9, 6, 3, 0, 2, 4, 12, 1, 5, 11, 10, 8)
        )._left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (0, -1),
        (-1, 0),
        (-1, 2),
        (-1, 3),
        (4, 3),
        (3, 2),
        (1, -1),
        (4, 5),
        (6, 2),
        (1, 7),
        (1, 10),
        (0, 1),
    ]
    assert list(
        CayleyPermutation(
            (8, 3, 4, 12, 5, 13, 2, 6, 1, 7, 9, 10, 11, 0)
        )._left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (-1, 0),
        (1, 0),
        (0, -1),
        (2, 0),
        (3, -1),
        (-1, 1),
        (4, 0),
        (-1, 6),
        (7, 0),
        (0, 3),
        (10, 3),
        (11, 3),
        (-1, 8),
    ]
    assert list(
        CayleyPermutation(
            (9, 12, 8, 11, 6, 13, 1, 5, 4, 3, 10, 2, 0, 7)
        )._left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (0, -1),
        (-1, 0),
        (0, 1),
        (-1, 2),
        (1, -1),
        (-1, 4),
        (6, 4),
        (6, 7),
        (6, 8),
        (0, 3),
        (6, 9),
        (-1, 6),
        (4, 2),
    ]
    assert list(
        CayleyPermutation(
            (11, 4, 12, 1, 8, 9, 10, 14, 3, 2, 13, 0, 5, 6, 7)
        )._left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (-1, 0),
        (0, -1),
        (-1, 1),
        (1, 0),
        (4, 0),
        (5, 0),
        (2, -1),
        (3, 1),
        (3, 8),
        (2, 7),
        (-1, 3),
        (1, 4),
        (12, 4),
        (13, 4),
    ]
    assert list(
        CayleyPermutation(
            (8, 3, 16, 0, 17, 5, 9, 10, 6, 19, 18, 2, 11, 14, 12, 13, 15, 4, 7, 1)
        )._left_floor_and_ceiling()
    ) == [
        (-1, -1),
        (-1, 0),
        (0, -1),
        (-1, 1),
        (2, -1),
        (1, 0),
        (0, 2),
        (6, 2),
        (5, 0),
        (4, -1),
        (4, 9),
        (3, 1),
        (7, 2),
        (12, 2),
        (12, 13),
        (14, 13),
        (13, 2),
        (1, 5),
        (8, 0),
        (3, 11),
    ]


def test_occurrences_in_from_permuta():
    assert list(
        CayleyPermutation([]).occurrences_in(CayleyPermutation([4, 1, 2, 3, 0]))
    ) == [()]
    assert sorted(
        CayleyPermutation([0]).occurrences_in(CayleyPermutation([4, 1, 2, 3, 0]))
    ) == [
        (0,),
        (1,),
        (2,),
        (3,),
        (4,),
    ]
    assert sorted(
        CayleyPermutation([0, 1]).occurrences_in(CayleyPermutation([4, 1, 2, 3, 0]))
    ) == [
        (1, 2),
        (1, 3),
        (2, 3),
    ]
    assert sorted(
        CayleyPermutation([1, 0]).occurrences_in(CayleyPermutation([4, 1, 2, 3, 0]))
    ) == [
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (1, 4),
        (2, 4),
        (3, 4),
    ]
    assert (
        list(CayleyPermutation([4, 1, 2, 3, 0]).occurrences_in(CayleyPermutation([])))
        == []
    )
    assert (
        list(
            CayleyPermutation([4, 1, 2, 3, 0]).occurrences_in(CayleyPermutation([1, 0]))
        )
        == []
    )
    # Test with colours
    assert sorted(
        CayleyPermutation([0]).occurrences_in(
            CayleyPermutation([4, 1, 2, 3, 0]), [1], [0, 0, 1, 1, 0]
        )
    ) == [(2,), (3,)]
    assert sorted(
        CayleyPermutation([1, 0]).occurrences_in(
            CayleyPermutation([4, 1, 2, 3, 0]), [1, 0], [1, 0, 1, 2, 0]
        )
    ) == [(0, 1), (0, 4), (2, 4)]


def test_sub_cperm():
    assert sorted(CayleyPermutation((0, 2, 1, 2, 1, 3, 2)).sub_cperms()) == [
        CayleyPermutation(()),
        CayleyPermutation((0,)),
        CayleyPermutation((0, 0)),
        CayleyPermutation((0, 1)),
        CayleyPermutation((1, 0)),
        CayleyPermutation((0, 0, 0)),
        CayleyPermutation((0, 0, 1)),
        CayleyPermutation((0, 1, 0)),
        CayleyPermutation((0, 1, 1)),
        CayleyPermutation((0, 1, 2)),
        CayleyPermutation((0, 2, 1)),
        CayleyPermutation((1, 0, 0)),
        CayleyPermutation((1, 0, 1)),
        CayleyPermutation((1, 0, 2)),
        CayleyPermutation((1, 1, 0)),
        CayleyPermutation((0, 0, 1, 0)),
        CayleyPermutation((0, 0, 2, 1)),
        CayleyPermutation((0, 1, 0, 1)),
        CayleyPermutation((0, 1, 0, 2)),
        CayleyPermutation((0, 1, 1, 1)),
        CayleyPermutation((0, 1, 1, 2)),
        CayleyPermutation((0, 1, 2, 1)),
        CayleyPermutation((0, 1, 2, 2)),
        CayleyPermutation((0, 1, 2, 3)),
        CayleyPermutation((0, 1, 3, 2)),
        CayleyPermutation((0, 2, 1, 1)),
        CayleyPermutation((0, 2, 1, 2)),
        CayleyPermutation((0, 2, 1, 3)),
        CayleyPermutation((0, 2, 2, 1)),
        CayleyPermutation((1, 0, 0, 1)),
        CayleyPermutation((1, 0, 0, 2)),
        CayleyPermutation((1, 0, 1, 0)),
        CayleyPermutation((1, 0, 1, 1)),
        CayleyPermutation((1, 0, 1, 2)),
        CayleyPermutation((1, 0, 2, 1)),
        CayleyPermutation((1, 1, 0, 1)),
        CayleyPermutation((1, 1, 0, 2)),
        CayleyPermutation((0, 1, 0, 2, 1)),
        CayleyPermutation((0, 1, 1, 2, 1)),
        CayleyPermutation((0, 1, 1, 3, 2)),
        CayleyPermutation((0, 1, 2, 1, 2)),
        CayleyPermutation((0, 1, 2, 1, 3)),
        CayleyPermutation((0, 1, 2, 3, 2)),
        CayleyPermutation((0, 2, 1, 1, 2)),
        CayleyPermutation((0, 2, 1, 1, 3)),
        CayleyPermutation((0, 2, 1, 2, 1)),
        CayleyPermutation((0, 2, 1, 2, 2)),
        CayleyPermutation((0, 2, 1, 2, 3)),
        CayleyPermutation((0, 2, 1, 3, 2)),
        CayleyPermutation((0, 2, 2, 1, 2)),
        CayleyPermutation((0, 2, 2, 1, 3)),
        CayleyPermutation((1, 0, 0, 2, 1)),
        CayleyPermutation((1, 0, 1, 0, 1)),
        CayleyPermutation((1, 0, 1, 0, 2)),
        CayleyPermutation((1, 0, 1, 2, 1)),
        CayleyPermutation((1, 1, 0, 2, 1)),
        CayleyPermutation((0, 1, 2, 1, 3, 2)),
        CayleyPermutation((0, 2, 1, 1, 3, 2)),
        CayleyPermutation((0, 2, 1, 2, 1, 2)),
        CayleyPermutation((0, 2, 1, 2, 1, 3)),
        CayleyPermutation((0, 2, 1, 2, 3, 2)),
        CayleyPermutation((0, 2, 2, 1, 3, 2)),
        CayleyPermutation((1, 0, 1, 0, 2, 1)),
        CayleyPermutation((0, 2, 1, 2, 1, 3, 2)),
    ]


def test_repr():
    for _ in range(100):
        p = list(range(random.randint(2, 20)))
    random.shuffle(p)
    cperm = CayleyPermutation(p)
    assert cperm == eval(repr(cperm))
