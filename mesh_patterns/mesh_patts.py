"""
Contains the MeshPattern class.

A mesh pattern is a Cayley permutation together with a set of cells
that are shaded.

We draw the size n Cayley permutation with maximum value k on a grid
of size (n + 1) x 2(k + 1).

For example, consider the mesh pattern (0, 1, 2, 1) with shaded cells
[(0, 2), (1, 3), (3, 0), (3, 1), (3, 2), (3, 3)]. This is drawn on
the 9 x 5 grid as:

     | | | |
    -+-+-●-+-
     | | | |
    -+x●x+-●-
    x| |x| |
    -●-+x+-+-
     | |x| |

An occurrence of a mesh pattern is an occurrence of the underlying
Cayley permutation in a word over the integers, such that the
regions implied by the shaded cells are also shaded in the larger
word, i.e., contain no points.
"""

from itertools import product
from typing import Iterable, Iterator, Tuple, Union

from cayley_permutations import CayleyPermutation

Cell = Tuple[int, int]


class MeshPattern:
    """The MeshPattern class."""

    def __init__(
        self,
        pattern: Iterable[int],
        shaded_cells: Iterable[Cell],
    ):
        self.pattern = CayleyPermutation(pattern)
        self.shaded_cells = frozenset(shaded_cells)
        self._check_init()

    def _check_init(self):
        n = len(self.pattern)
        if n == 0:
            assert self.shaded_cells in (tuple(), ((0, 0),))
        k = max(self.pattern)
        for x, y in self.shaded_cells:
            assert 0 <= x <= n, "Invalid x coordinate"
            assert 0 <= y <= 2 * (k + 1), "Invalid y coordinate"

    @classmethod
    def from_regions(
        cls,
        cperm: CayleyPermutation,
        regions: Iterable[Tuple[Cell, Cell]],
    ):
        """
        Returns a mesh pattern from a Cayley permutation and a
        list of regions to be shaded.

        A region is defined by a pair of cells. The first is the lower
        leftmost cell in the region and the second is the upper rightmost
        cell in the region.
        """

        cells = cls._regions_to_cells(regions)
        return MeshPattern(cperm, cells)

    @staticmethod
    def _regions_to_cells(regions: Iterable[Tuple[Cell, Cell]]) -> set[Cell]:
        """Takes an input of regions and returns them as cells."""
        cells = set()
        for reg in regions:
            i1, v1 = reg[0]
            i2, v2 = reg[1]
            for i in range(i1, i2 + 1):
                for j in range(v1, v2 + 1):
                    cells.add((i, j))
        return cells

    def sub_mesh_pattern(self, indices: Iterable[int]) -> "MeshPattern":
        """Returns a sub mesh pattern of the mesh pattern at the given indices"""
        indices = tuple(indices)
        row_bounds, col_bounds = self.row_col_bounds(indices)
        cells = tuple(
            (i, j)
            for j, row_bound in enumerate(row_bounds)
            for i, col_bound in enumerate(col_bounds)
            if all(
                cell in self.shaded_cells
                for cell in product(range(*col_bound), range(*row_bound))
            )
            and self.avoids_shaded_cell(self.pattern, indices, (i, j))
        )
        pattern = CayleyPermutation.standardise((self.pattern[i] for i in indices))
        # need to ensure there isn't a point in shaded region
        mp = MeshPattern(pattern, cells)
        assert mp.avoids_shading(self.pattern, indices)  # this method is borked
        return mp

    def row_col_bounds(
        self, indices: Tuple[int, ...]
    ) -> tuple[tuple[Cell, ...], tuple[Cell, ...]]:
        """Returns the row and column bounds of the regions implied by projecting
        to the given occurrence."""
        values = tuple(sorted(set(self.pattern[i] for i in indices)))
        col_bounds = (
            [(0, indices[0] + 1)]
            + [(x + 1, y + 1) for x, y in zip(indices, indices[1:])]
            + [(indices[-1] + 1, len(self.pattern) + 1)]
        )

        def rows_below_value(value: int) -> int:
            return 2 * value + 1

        row_bounds = [(0, rows_below_value(values[0]))]

        def insert_rows(n: int, m: int) -> None:
            n = rows_below_value(n)
            m = rows_below_value(m)
            row_bounds.append((n, n + 1))
            row_bounds.append((n + 1, m))

        for val1, val2 in zip(values, values[1:]):
            insert_rows(val1, val2)
        insert_rows(values[-1], max(self.pattern) + 1)

        return tuple(row_bounds), tuple(col_bounds)

    def avoids(self, *mesh_patts: "MeshPattern") -> bool:
        """Returns True if avoids all of the mesh patterns."""
        return all(self.avoids_patt(mesh_patt) for mesh_patt in mesh_patts)

    def contains(self, *mesh_patts: "MeshPattern") -> bool:
        """Return True if self contains any of the mesh patterns."""
        return not self.avoids(*mesh_patts)

    def contains_patt(self, mesh_patt: "MeshPattern") -> bool:
        """Return True if self contains the mesh pattern."""
        return any(True for _ in self.occurrences_in_mesh(mesh_patt))

    def avoids_patt(self, mesh_patt: "MeshPattern") -> bool:
        """Return True if self avoids the mesh pattern."""
        return not self.contains_patt(mesh_patt)

    def occurrences_in(
        self, other: Union[tuple[int, ...], "MeshPattern"]
    ) -> Iterator[Tuple[int, ...]]:
        """Yield all occurrences of the mesh pattern in either a
        word over the natural numbers or another mesh pattern."""
        if isinstance(other, tuple):
            yield from self.occurrences_in_word(other)
        else:
            yield from self.occurrences_in_mesh(other)

    def occurrences_in_word(self, word: tuple[int, ...]) -> Iterator[Tuple[int, ...]]:
        """Yield all occurrences of the mesh pattern in a word over the natural numbers."""
        for occ in self.pattern.occurrences_in(word):
            if self.avoids_shading(word, occ):
                yield occ

    def occurrences_in_mesh(
        self, mesh_patt: "MeshPattern"
    ) -> Iterator[Tuple[int, ...]]:
        """Yield all occurrences of the mesh pattern in another mesh pattern."""
        for occ in self.occurrences_in_word(mesh_patt.pattern):
            if self.shaded_cells <= mesh_patt.sub_mesh_pattern(occ).shaded_cells:
                yield occ

    def is_avoided_by_word(self, word: tuple[int, ...]) -> bool:
        """Returns true if the Cayely permutation avoids the mesh pattern."""
        return not self.is_contained_by_word(word)

    def is_contained_by_word(self, word: tuple[int, ...]) -> bool:
        """Returns true if the Cayely permutation contains the mesh pattern."""
        return any(True for _ in self.occurrences_in(word))

    def avoids_shading(
        self,
        word: tuple[int, ...],
        indices: Tuple[int, ...],
    ) -> bool:
        """Return True if no points in shading that is projected to the
        word over the natural numbers according to the indices."""
        return all(
            self.avoids_shaded_cell(word, indices, cell) for cell in self.shaded_cells
        )

    @staticmethod
    def avoids_shaded_cell(
        word: tuple[int, ...], indices: tuple[int, ...], cell: Cell
    ) -> bool:
        """Returns true if the projected cell contains no points in the
        word over the natural numbers with respect to the given indices."""
        if not indices:
            assert cell == (0, 0)
            return bool(word)
        (i1, i2), (j1, j2) = MeshPattern.region_of_perm(word, indices, cell)
        return not any(
            i1 <= idx < i2 and j1 <= val < j2
            for idx, val in enumerate(word)
            if idx not in indices
        )

    @staticmethod
    def contains_shaded_cell(
        word: tuple[int, ...], indices: tuple[int, ...], cell: Cell
    ) -> bool:
        """
        Return true if word contains a point in the shaded region once
        cell is projected to the occurrenc
        e"""
        return not MeshPattern.avoids_shaded_cell(word, indices, cell)

    @staticmethod
    def region_of_perm(
        word: tuple[int, ...], occ: tuple[int, ...], cell: Cell
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        Returns two tuples of the form (i1, i2) and (j1, j2) where
        - i1 and i2 are the lower and upper bounds for indices of the points
          that can be in the shaded region and
        - j1 and j2 are the lower and upper bounds for the values of the points
          that can be in the shaded region.
        """
        indices = tuple(occ)
        values = sorted(set(word[idx] for idx in occ))
        col, row = cell
        # get bounds for indices
        i1 = 0 if col == 0 else indices[col - 1]
        i2 = len(word) if col == len(occ) else indices[col]
        # get bounds for values
        row_idx = row // 2
        if row % 2:
            # odd, so on a row with a single value
            j1 = values[row_idx]
            j2 = values[row_idx] + 1
        else:
            # even, so on a row with many values
            j1 = 0 if row_idx == 0 else values[row_idx - 1] + 1
            j2 = values[-1] + 1 if row_idx == len(values) else values[row_idx]
        return (i1, i2), (j1, j2)

    @staticmethod
    def non_empty_regions(
        obj: Iterable[int], occurrence: tuple[int, ...]
    ) -> frozenset[tuple[int, int]]:
        """
        Return the set of cells that contain a point when projected onto occurrence.
        """
        obj = tuple(obj)
        occurrence = tuple(occurrence)
        number_of_values = len(set(obj[i] for i in occurrence))
        return frozenset(
            (
                cell
                for cell in product(
                    range(len(occurrence) + 1), range(2 * number_of_values + 1)
                )
                if MeshPattern.contains_shaded_cell(obj, occurrence, cell)
            )
        )

    def complement(self) -> "MeshPattern":
        """Returns the complement of the mesh pattern - anything
        that was shaded now isn't, anything that wasn't now is
        apart from columns which currently remain unshaded."""
        return MeshPattern(
            self.pattern,
            (
                cell
                for cell in product(
                    range(len(self.pattern)), range(2 * max(self.pattern) + 1)
                )
                if cell not in self.shaded_cells
            ),
        )

    def ascii_plot(self) -> str:
        """Returns an ascii plot of the mesh pattern.
        Example:
        >>> print(MeshPattern(CayleyPermutation([1, 2]), [(0, 3), (2, 2)]).ascii_plot())
         | |
        x+-●-
         |x|
        -●-+-
         | |
        """
        shaded_cell = "x"
        point = "\u25cf"

        if len(self.pattern) == 0:
            if self.shaded_cells:
                return f"+-+\n|{shaded_cell}|\n+-+\n"
            return "+-+\n| |\n+-+\n"

        n = len(self.pattern)
        m = max(self.pattern) + 1

        # create the grid
        empty_row = " |" * n
        plus_row = "+".join("-" for _ in range(n + 1))
        rows = [empty_row, plus_row] * m + [empty_row]

        # mark Cayley permutation
        for idx, val in enumerate(self.pattern):
            row = rows[val * 2 + 1]
            row = row[: idx * 2 + 1] + point + row[idx * 2 + 2 :]
            rows[val * 2 + 1] = row

        # mark shaded cells
        for idx, val in self.shaded_cells:
            row = rows[val]
            row = row[: idx * 2] + shaded_cell + row[idx * 2 + 1 :]
            rows[val] = row

        return "\n".join(reversed(rows))

    def __eq__(self, other) -> bool:
        if not isinstance(other, MeshPattern):
            return NotImplemented
        return self.pattern == other.pattern and self.shaded_cells == other.shaded_cells

    def __hash__(self) -> int:
        return hash((self.pattern, self.shaded_cells))

    def __len__(self) -> int:
        return len(self.pattern)

    def __le__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.pattern, sorted(self.shaded_cells)) < (
            other.pattern,
            sorted(other.shaded_cells),
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.pattern, sorted(self.shaded_cells)) <= (
            other.pattern,
            sorted(other.shaded_cells),
        )

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return other.__lt__(self)

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return other.__le__(self)

    def __str__(self) -> str:
        return f"MeshPattern({self.pattern}, {self.shaded_cells})"
