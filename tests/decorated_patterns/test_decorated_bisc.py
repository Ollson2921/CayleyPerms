from cayley_permutations import CayleyPermutation
from decorated_patterns import PermutationDecoratedPatternFinder, DecoratedPattern
from gridded_cayley_permutations import GriddedCayleyPerm


def test_two_patterns():
    avoiders = [
        CayleyPermutation.standardise(p)
        for p in [
            "",
            "0",
            "10",
            "210",
            "3210",
            "43210",
            "542310",
            "543210",
            "6523410",
            "6524310",
            "6532410",
            "6534210",
            "6542310",
            "6543210",
        ]
    ]
    basis = PermutationDecoratedPatternFinder(2, 2, avoiders).find_decorated_basis()
    patt1 = DecoratedPattern(
        CayleyPermutation((0, 1)),
        (GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 0), (4, 0))),),
    )
    patt2 = DecoratedPattern(
        CayleyPermutation((0, 1)),
        (GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (0, 4))),),
    )
    assert patt1 in basis
    assert patt2 in basis
    assert len(basis) == 2
