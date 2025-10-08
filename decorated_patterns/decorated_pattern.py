"""
The DecoratedPattern class.

A decorated pattern is a pair (p, O) for some Cayley permutation p
and some set of obstructions O. If the size of p is n and the number
of values in p is m, then O is a subset of gridded permutation on an
(2n + 1) x (2m + 1) grid.

This is stored as a (2n + 1) x (2m + 1) tiling.

A word over the natural numbers contains an occurrence of the
decorated pattern if there is an occurrence of the pattern in the
word, such that the complement of the occurrence in the word avoids
all of the obstructions when drawn on the tiling in the obvious way
"""

from functools import cached_property
from itertools import combinations_with_replacement
from typing import Iterable, Iterator

from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import GriddedCayleyPerm, Tiling


class DecoratedPattern:
    """The DecoratedPattern class"""

    def __init__(self, cperm: Iterable[int], obstructions: Iterable[GriddedCayleyPerm]):
        self.cperm = CayleyPermutation(cperm)
        new_obs = tuple(obstructions)
        self.tiling = Tiling(
            self._obs_to_add.union(new_obs),
            self._reqs_to_add,
            self.dimensions,
            simplify=bool(new_obs),
        )

    @cached_property
    def _obs_to_add(self) -> frozenset[GriddedCayleyPerm]:
        point_cell_obs = [
            GriddedCayleyPerm((0, 0), [(2 * x + 1, 2 * y + 1)] * 2)
            for x, y in enumerate(self.cperm)
        ]
        col_obs = [
            GriddedCayleyPerm((0,), [(x, y)])
            for x in range(1, self.dimensions[0], 2)
            for y in range(0, self.dimensions[1], 2)
        ]
        point_row_obs = [
            GriddedCayleyPerm(patt, [(x1, y), (x2, y)])
            for patt in (CayleyPermutation((0, 1)), CayleyPermutation((1, 0)))
            for x1, x2 in combinations_with_replacement(range(self.dimensions[0]), 2)
            for y in range(1, self.dimensions[1], 2)
        ]
        return frozenset(point_cell_obs + col_obs + point_row_obs)

    @cached_property
    def _reqs_to_add(self):
        return [[GriddedCayleyPerm((0,), [cell])] for cell in self.point_cells]

    @cached_property
    def dimensions(self) -> tuple[int, int]:
        """The dimensions of the underlying tiling"""
        return (2 * len(self) + 1, 2 * self.number_of_values + 1)

    @cached_property
    def point_cells(self) -> frozenset[tuple[int, int]]:
        """The point cells in the underlying tiling"""
        return frozenset((2 * x + 1, 2 * y + 1) for x, y in enumerate(self.cperm))

    @cached_property
    def extra_obs(self) -> frozenset[GriddedCayleyPerm]:
        """The obstructions that are not coming from point row/col obs"""
        return frozenset(ob for ob in self.obstructions if ob not in self._obs_to_add)

    @cached_property
    def number_of_values(self) -> int:
        """The number of unique values in the Cayley permutation"""
        if not self.cperm:
            return 0
        return max(self.cperm) + 1

    # containment/avoidance methods

    def occurrences_in_word(self, word: tuple[int, ...]) -> Iterator[tuple[int, ...]]:
        """
        Yield all of the occurrences of the pattern in a word over the
        natural numbers.
        """
        for occ in self.cperm.occurrences_in(word):
            gridding = self.gridding_of_occurrence(word, occ)
            if self.avoids_obstructions(word, gridding):
                yield occ

    def contained_by_word(self, word: tuple[int, ...]) -> bool:
        """
        Return true if there is an occurence of the decorated pattern
        in the word over the natural numbers
        """
        return any(True for _ in self.occurrences_in_word(word))

    def avoided_by_word(self, word: tuple[int, ...]) -> bool:
        """
        Return True if there is NO occurrence of the decorated pattern
        in the word over the natural numbers
        """
        return not self.contained_by_word(word)

    def avoids_obstructions(
        self, word: tuple[int, ...], gridding: tuple[tuple[int, int], ...]
    ) -> bool:
        """Return True if the gridded word avoids the patterns obstructions"""
        return all(self._avoids_ob(ob, word, gridding) for ob in self.obstructions)

    @staticmethod
    def _avoids_ob(
        ob: GriddedCayleyPerm,
        word: tuple[int, ...],
        gridding: tuple[tuple[int, int], ...],
    ):
        return not DecoratedPattern._contains_ob(ob, word, gridding)

    @staticmethod
    def _contains_ob(
        ob: GriddedCayleyPerm,
        word: tuple[int, ...],
        gridding: tuple[tuple[int, int], ...],
    ):
        return any(
            True for _ in ob.pattern.occurrences_in(word, ob.positions, gridding)
        )

    @staticmethod
    def gridding_of_occurrence(
        word: tuple[int, ...], occ: tuple[int, ...]
    ) -> tuple[tuple[int, int], ...]:
        """
        Return the unique gridding of a word implied by the given occurrence.

        Its assumed that the occurrence is an occurrence of the Cayley
        permutation. If the occurrence is not an occurrence of the Cayley
        permutation then this will return a gridding not on the tiling.
        """
        col_values = DecoratedPattern._col_values(word, occ)
        row_values = DecoratedPattern._row_values(word, occ)

        def find_col_index(idx: int) -> int:
            for i, (a, b) in enumerate(col_values):
                if a <= idx < b:
                    return i
            raise ValueError("col_values borked")

        def find_row_index(val: int) -> int:
            for j, (a, b) in enumerate(row_values):
                if a <= val < b:
                    return j
            raise ValueError("row_values borked")

        return tuple(
            (find_col_index(idx), find_row_index(val)) for idx, val in enumerate(word)
        )

    @staticmethod
    def _col_values(
        word: tuple[int, ...], occ: tuple[int, ...]
    ) -> list[tuple[int, int]]:
        if len(occ) == 0:
            return [(0, len(word) + 1)]
        col_values = [(0, occ[0])]
        for idx1, idx2 in zip(occ, occ[1:]):
            col_values.append((idx1, idx1 + 1))
            col_values.append((idx1 + 1, idx2))
        col_values.append((occ[-1], occ[-1] + 1))
        col_values.append((occ[-1] + 1, len(word)))
        return col_values

    @staticmethod
    def _row_values(
        word: tuple[int, ...], occ: tuple[int, ...]
    ) -> list[tuple[int, int]]:
        if len(occ) == 0:
            if len(word) == 0:
                return [(0, 0)]
            return [(0, max(word) + 1)]
        values = sorted(set(word[idx] for idx in occ))
        row_values = [(0, values[0])]
        for val1, val2 in zip(values, values[1:]):
            row_values.append((val1, val1 + 1))
            row_values.append((val1 + 1, val2))
        row_values.append((values[-1], values[-1] + 1))
        row_values.append((values[-1] + 1, max(word) + 1))
        return row_values

    # shortcuts to tiling properties

    @property
    def obstructions(self) -> tuple[GriddedCayleyPerm, ...]:
        """The underlying tiling's obstructions"""
        return self.tiling.obstructions

    @property
    def requirements(self) -> tuple[tuple[GriddedCayleyPerm, ...], ...]:
        """The underlying tilings requirements"""
        return self.requirements

    def __len__(self):
        return len(self.cperm)

    def __repr__(self):
        return f"DecoratedTiling({repr(self.cperm)}, {repr(tuple(sorted(self.extra_obs)))})"

    def __str__(self):
        res = self.cperm.ascii_plot()
        res += "with extra obs:\n" + "\n".join(str(gp) for gp in self.extra_obs)
        res += "\nOr as a tiling:\n" + str(self.tiling)
        return res
