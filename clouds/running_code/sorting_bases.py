from cayley_permutations import CayleyPermutation

bases = {
    frozenset(
        {
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((0, 1, 0)),
            CayleyPermutation((2, 1, 0)),
            CayleyPermutation((0, 0, 0)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((0, 1, 2)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((0, 1, 0)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((0, 1, 2)),
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 0)),
        }
    ),
    frozenset({CayleyPermutation((0, 0, 1)), CayleyPermutation((0, 1, 1))}),
    frozenset(
        {
            CayleyPermutation((0, 1, 2)),
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((0, 1, 0)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((0, 1, 2)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((2, 1, 0)),
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((0, 1, 0)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset({CayleyPermutation((1, 0, 0))}),
    frozenset({CayleyPermutation((1, 0, 1)), CayleyPermutation((0, 1, 1))}),
    frozenset(
        {
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 1, 0)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 1, 0)),
            CayleyPermutation((2, 1, 0)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((1, 0, 0)),
        }
    ),
    frozenset({CayleyPermutation((1, 0, 1)), CayleyPermutation((0, 1, 0))}),
    frozenset(
        {
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 1, 0)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((2, 1, 0)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((1, 1, 0)),
        }
    ),
    frozenset({CayleyPermutation((0, 0, 0))}),
    frozenset(
        {
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 1, 0)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((0, 0, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 0, 1)),
        }
    ),
    frozenset({CayleyPermutation((0, 0, 0)), CayleyPermutation((1, 1, 0))}),
    frozenset(
        {
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 1, 0)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((1, 0, 0)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((0, 1, 0)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((0, 1, 0)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((1, 0, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 0, 0)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((2, 1, 0)),
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 1, 0)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 1, 0)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((0, 0, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 1, 0)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset({CayleyPermutation((1, 0, 0)), CayleyPermutation((0, 0, 1))}),
    frozenset(
        {
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 1, 0)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((2, 1, 0)),
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 0, 0)),
        }
    ),
    frozenset({CayleyPermutation((2, 1, 0)), CayleyPermutation((1, 1, 0))}),
    frozenset(
        {
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 1, 0)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset({CayleyPermutation((0, 1, 2)), CayleyPermutation((1, 0, 1))}),
    frozenset(
        {
            CayleyPermutation((0, 1, 2)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset({CayleyPermutation((1, 0, 1))}),
    frozenset(
        {
            CayleyPermutation((2, 1, 0)),
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((1, 1, 0)),
        }
    ),
    frozenset({CayleyPermutation((0, 0, 0)), CayleyPermutation((0, 1, 0))}),
    frozenset({CayleyPermutation((1, 1, 0)), CayleyPermutation((0, 0, 1))}),
    frozenset(
        {
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 0)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((0, 1, 0)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((0, 1, 2)),
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((0, 1, 0)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((0, 1, 2)),
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 0)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 0)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((0, 1, 2)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 1, 0)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((1, 1, 0)),
        }
    ),
    frozenset({CayleyPermutation((1, 0, 0)), CayleyPermutation((1, 0, 1))}),
    frozenset(
        {
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((0, 0, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 1, 0)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((1, 1, 0)),
        }
    ),
    frozenset({CayleyPermutation((1, 0, 0)), CayleyPermutation((0, 1, 2))}),
    frozenset(
        {
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((0, 1, 2)),
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((0, 0, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((0, 1, 0)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((0, 1, 2)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((1, 0, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 0)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 1, 0)),
            CayleyPermutation((0, 0, 0)),
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((0, 0, 1)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset({CayleyPermutation((0, 1, 2)), CayleyPermutation((0, 0, 0))}),
    frozenset(
        {
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 1, 1)),
        }
    ),
    frozenset(
        {
            CayleyPermutation((1, 0, 0)),
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((1, 1, 0)),
            CayleyPermutation((0, 1, 0)),
            CayleyPermutation((2, 1, 0)),
        }
    ),
    frozenset({CayleyPermutation((0, 1, 2))}),
    frozenset(
        {
            CayleyPermutation((0, 1, 2)),
            CayleyPermutation((1, 0, 1)),
            CayleyPermutation((0, 0, 1)),
        }
    ),
}


sorted_bases = set()
for basis in bases:
    sorted_bases.add(tuple(sorted(basis)))
