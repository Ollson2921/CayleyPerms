"""This module contains the class Av which
generates Cayley permutations avoiding a given basis."""

from .cayley import CayleyPermutation


class Av:
    """
    Generates Cayley permutations avoiding the input.
    """

    def __init__(self, basis: list[CayleyPermutation]):
        """Cache is a list of dictionaries. The nth dictionary contains the Cayley
        permutations of size n which avoid the basis and a tuple of lists.
        The  first list is the indices where a new maximum can be inserted
        and the second is the indices where the same maximum can be inserted."""
        self.basis = basis
        self.cache: list[dict[CayleyPermutation, tuple[list[int], list[int]]]] = [
            {CayleyPermutation([]): ([0], [])}
        ]

    def in_class(self, cperm: CayleyPermutation, require_last: int = 0) -> bool:
        """
        Returns True if the Cayley permutation avoids the basis.

        Searches for bad patterns that must use the last [require_last] entries.

        Examples:
        >>> av = Av([CayleyPermutation([0, 1]), CayleyPermutation([1, 0])])
        >>> av.in_class(CayleyPermutation([0, 0, 0]))
        True
        >>> av = Av([CayleyPermutation([0, 1]), CayleyPermutation([1, 0])])
        >>> av.in_class(CayleyPermutation([0, 1, 0]))
        False
        """
        return not cperm.contains(self.basis, require_last)

    def generate_cperms(self, size: int) -> list[CayleyPermutation]:
        """Generate Cayley permutations of size 'size' which
        avoid the basis by checking avoidance at each step.

        Examples:
        >>> Av([CayleyPermutation([0, 1]), CayleyPermutation([1, 0])]).generate_cperms(3)
        [000]

        >>> Av([CayleyPermutation([0, 0]), CayleyPermutation([1, 0])]).generate_cperms(4)
        [0123]
        """
        if size == 0:
            return [CayleyPermutation([])]
        cperms = [CayleyPermutation([0])]
        count = 1
        next_cperms: list[CayleyPermutation] = []
        while count < size:
            for cperm in cperms:
                for next_cperm in cperm.add_maximum():
                    if self.in_class(next_cperm):
                        next_cperms.append(next_cperm)
            count += 1
            cperms = next_cperms
            next_cperms = []
        return cperms

    def counter(self, ran: int = 7) -> list[int]:
        """
        Returns a list of the number of cperms for each size in range 'ran'
        starting at size 0 (the empty Cayley permutation).

        Examples:
        >>> print(Av([CayleyPermutation([0, 1]), CayleyPermutation([1, 0])]).counter(3))
        [1, 1, 1, 1]

        >>> print(Av([CayleyPermutation([1, 0])]).counter(4))
        [1, 1, 2, 4, 8]
        """
        count = []
        for size in range(ran + 1):
            count.append(len(self.generate_cperms(size)))
        return count

    def condition(self) -> bool:
        """Returns True if can skip pattern avoidance."""
        return False

    def __str__(self) -> str:
        return f"Av({','.join(str(x) for x in self.basis)})"


class CanonicalAv(Av):
    """Generates canonical Cayley permutations avoiding the basis."""

    def in_class(self, cperm: CayleyPermutation, require_last: int = 0) -> bool:
        return (
            not cperm.contains(self.basis, require_last=require_last)
            and cperm.is_canonical()
        )

    def get_canonical_basis(self) -> list[CayleyPermutation]:
        """Turns a basis into canonical form using as_canonical() from the CayleyPermutation class.

        Example:
        >>> print(CanonicalAv([CayleyPermutation([1, 0])]).get_canonical_basis())
        [010]
        """
        basis: set[CayleyPermutation] = set()
        for cperm in self.basis:
            basis.update(cperm.as_canonical())
        res: list[CayleyPermutation] = []
        for cperm in sorted(basis, key=len):
            if not cperm.contains(res):
                res.append(cperm)
        return res

    def new_max_valid_insertions(
        self, cperm: CayleyPermutation, max_basis_value: int
    ) -> frozenset[int]:
        """Returns a list of indices where a new maximum can be inserted into cperm."""
        res = None
        if len(cperm) <= max_basis_value:
            acceptable_indices = []
            for idx in range(len(cperm) + 1):
                if self.new_max_okay(cperm, idx):
                    acceptable_indices.append(idx)
            return frozenset(acceptable_indices)
        for index in cperm.indices_above_value(max(cperm) - max_basis_value):
            sub_cperm = cperm.delete_index(index)
            indices = self.cache[len(sub_cperm)][sub_cperm][0]
            valid_indices = [i for i in indices if i <= index]
            valid_indices.extend([i + 1 for i in indices if i >= index])
            if res is None:
                res = frozenset(valid_indices)
            else:
                res = res.intersection(valid_indices)
            if not res:
                break
        assert res is not None
        return res

    def new_max_okay(self, cperm: CayleyPermutation, index: int) -> bool:
        """Returns True if the new maximum at index is okay for canonical form."""
        if len(cperm) == 0:
            return True
        for idx, val in enumerate(cperm):
            if idx < index:
                if val == max(cperm):
                    return True
        return False
