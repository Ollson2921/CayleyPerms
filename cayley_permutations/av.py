"""This module contains the class Av which
generates Cayley permutations avoiding a given basis."""

from typing import Iterable
from .cayley import CayleyPermutation
from .simplify_basis import string_to_basis


class Av:
    """
    Generates Cayley permutations avoiding the input.
    """

    def __init__(self, basis: Iterable[CayleyPermutation] | str):
        """Input can be a list of Cayley permutations or a string of zero-based
        or one-based Cayley permutations separated by anything.
        Cache is a list of dictionaries. The nth dictionary contains the Cayley
        permutations of size n which avoid the basis and a tuple of lists.
        The  first list is the indices where a new maximum can be inserted
        and the second is the indices where the same maximum can be inserted."""
        if isinstance(basis, str):
            basis = string_to_basis(basis)
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
        current_cperms = [CayleyPermutation([0])]
        count = 1
        while count < size:
            next_cperms = self.next_sized_cperms_in_class(current_cperms)
            count += 1
            current_cperms = next_cperms
        return current_cperms

    def next_sized_cperms_in_class(
        self, last_cperms: list[CayleyPermutation]
    ) -> list[CayleyPermutation]:
        """Finds the Cayley permutations in the class which are one longer than
        the Cayley permutations in 'last_cperms'.

        Example:
        >>> Av([CayleyPermutation((0, 1))]).next_sized_cperms_in_class([CayleyPermutation((0,))])
        [CayleyPermutation((1, 0)), CayleyPermutation((0, 0))]"""
        next_cperms: list[CayleyPermutation] = []
        for cperm in last_cperms:
            for next_cperm in cperm.add_maximum():
                if self.in_class(next_cperm):
                    next_cperms.append(next_cperm)
        return next_cperms

    def generate_cperms_dict(self, size: int) -> dict[int, list[CayleyPermutation]]:
        """Returns a dictionary of Cayley permutations of length n in the class
        for n up to 'size'.

        Example:
        >>> for item in Av([CayleyPermutation((0, 1))]).generate_cperms_dict(2).items():
        >>>    print(item)
        (0, [CayleyPermutation(())])
        (1, [CayleyPermutation((0,))])
        (2, [CayleyPermutation((1, 0)), CayleyPermutation((0, 0))])
        """
        all_lengths: dict[int, list[CayleyPermutation]] = {0: [CayleyPermutation([])]}
        if size == 0:
            return all_lengths
        all_lengths[1] = [CayleyPermutation([0])]
        current_size = 1
        while current_size < size:
            current_size += 1
            all_lengths[current_size] = self.generate_cperms(current_size)
        return all_lengths

    def counter(self, ran: int = 7) -> list[int]:
        """
        Returns a list of the number of cperms for each size in range 'ran'
        starting at size 0 (the empty Cayley permutation).

        Examples:
        >>> print(Av([CayleyPermutation([0, 1]), CayleyPermutation([1, 0])]).counter(3))
        [1, 1, 1, 1]

        >>> print(Av([CayleyPermutation((0, 1))]).counter(10))
        [1, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
        """
        if ran == 0:
            return [1]
        current_cperms = [CayleyPermutation([0])]
        counts: list[int] = [1, 1]
        curr_size = 1
        while curr_size < ran:
            next_cperms = self.next_sized_cperms_in_class(current_cperms)
            counts.append(len(next_cperms))
            curr_size += 1
            current_cperms = next_cperms
        return counts

    def condition(self) -> bool:
        """Returns True if can skip pattern avoidance."""
        return False

    def pretty_print_generate_cperms(self, size: int) -> str:
        """Prints the Cayley permutations of size 'size' in the class
        in a more readable format."""
        return f"{','.join(str(x) for x in self.generate_cperms(size))}"

    def __str__(self) -> str:
        return f"Av({','.join(str(x) for x in self.basis)})"

    def __repr__(self) -> str:
        return f"Av([{','.join(repr(cperm) for cperm in self.basis)}])"


class CanonicalAv(Av):
    """Generates restricted growth functions avoiding the basis."""

    def in_class(self, cperm: CayleyPermutation, require_last: int = 0) -> bool:
        return (
            not cperm.contains(self.basis, require_last=require_last) and cperm.is_rgf()
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
