import pytest

from mesh_patterns import (
    AscentSequencePatternFinder,
    CayleyMeshPatternFinder,
    InversionSequencePatternFinder,
    MeshPattern,
    PermutationPatternFinder,
    RestrictedGrowthFunctionPatternFinder,
)


@pytest.fixture
def mp1():
    return MeshPattern(
        (0, 2, 1),
        [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)],
    )


def test_cayley_bisc(mp1):
    object_size = 5
    patt_size = 3

    avoiders = set()
    containers = set()
    for i in range(object_size + 1):
        for cperm in CayleyMeshPatternFinder.universe_of_size(i):
            if mp1.is_avoided_by_word(cperm):
                avoiders.add(cperm)
            else:
                containers.add(cperm)

    bisc = CayleyMeshPatternFinder(patt_size, avoiders, containers)
    basis = list(bisc.find_mesh_basis())[0]
    assert basis == [
        MeshPattern(
            (0, 2, 1),
            [(2, 0), (2, 1)],
        )
    ]


def test_universes():
    assert [len(AscentSequencePatternFinder.universe_of_size(i)) for i in range(8)] == [
        1,
        1,
        2,
        5,
        15,
        53,
        217,
        1014,
    ]
    assert [
        len(RestrictedGrowthFunctionPatternFinder.universe_of_size(i)) for i in range(8)
    ] == [1, 1, 2, 5, 15, 52, 203, 877]
    assert [
        len(InversionSequencePatternFinder.universe_of_size(i)) for i in range(8)
    ] == [1, 1, 2, 6, 24, 120, 720, 5040]
    assert [len(CayleyMeshPatternFinder.universe_of_size(i)) for i in range(8)] == [
        1,
        1,
        3,
        13,
        75,
        541,
        4683,
        47293,
    ]
    assert [len(PermutationPatternFinder.universe_of_size(i)) for i in range(8)] == [
        1,
        1,
        2,
        6,
        24,
        120,
        720,
        5040,
    ]


def test_perm():
    avoiders = PermutationPatternFinder.universe_up_to_size(PermutationPatternFinder, 6)
    containers = (
        CayleyMeshPatternFinder.universe_up_to_size(CayleyMeshPatternFinder, 6)
        - avoiders
    )
    bisc = CayleyMeshPatternFinder(3, avoiders, containers)
    basis = list(bisc.find_mesh_basis())[0]
    assert basis == [MeshPattern((0, 0), [])]
