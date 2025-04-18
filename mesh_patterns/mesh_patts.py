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
Cayley permutation in a larger Cayley permutation, such that the
regions implied by the shaded cells are also shaded in the larger
Cayley permutation, i.e., contain no points.
"""

from cayley_permutations import CayleyPermutation
from typing import Tuple, Iterable, Iterator, Union
from itertools import product

Cell = Tuple[int, int]


class MeshPattern:
    def __init__(
        self,
        pattern: CayleyPermutation,
        shaded_cells: Iterable[Cell],
    ):
        self.pattern = pattern
        self.shaded_cells = tuple(sorted(set(shaded_cells)))
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
        self, indices: tuple[int, ...]
    ) -> tuple[tuple[Cell, ...], tuple[Cell, ...]]:
        """Returns the row and column bounds of the regions implied by projecting
        to the given occurrence."""
        indices = tuple(indices)
        values = tuple(sorted(set(self.pattern[i] for i in indices)))
        col_bounds = (
            [(0, indices[0] + 1)]
            + [(x + 1, y + 1) for x, y in zip(indices, indices[1:])]
            + [(indices[-1] + 1, len(self.pattern) + 1)]
        )
        row_bounds = [(0, values[0] + 1)]
        shift = 0
        for val1, val2 in zip(values, values[1:]):
            row_bounds.append((val1 + 1 + shift, val1 + 2 + shift))
            row_bounds.append((val1 + 2 + shift, val2 + 2 + shift))
            shift += val1 + 1
        row_bounds.append((values[-1] + 1 + shift, values[-1] + 2 + shift))
        row_bounds.append((values[-1] + 2 + shift, 2 * (max(self.pattern) + 1) + 1))
        return row_bounds, col_bounds

    def avoids(self, patts: Iterable["MeshPattern"]) -> bool:
        """Returns True if avoids all of the mesh patterns."""
        return all(self.avoids_patt(mesh_patt) for mesh_patt in patts)

    def contains(self, mesh_patts: Iterable["MeshPattern"]) -> bool:
        """Return True if self contains any of the mesh patterns."""
        return not self.avoids(mesh_patts)

    def contains_patt(self, mesh_patt: "MeshPattern") -> bool:
        """Return True if self contains the mesh pattern."""
        for occ in mesh_patt.occurrences_of_pattern(self.pattern):
            if self.is_shaded_areas_map_correct(mesh_patt, occ):
                return True
        return False

    def avoids_patt(self, mesh_patt: "MeshPattern") -> bool:
        """Return True if self avoids the mesh pattern."""
        return not self.contains_patt(mesh_patt)

    def occurrences_in(
        self, other: Union[CayleyPermutation, "MeshPattern"]
    ) -> Iterator[Tuple[int, ...]]:
        """Yield all occurrences of the mesh pattern in either a
        Cayley permutation or another mesh pattern."""
        if isinstance(other, CayleyPermutation):
            yield from self._occurrences_in_cperm(patt)
        else:
            yield from self._occurrences_in_mesh(patt)

    def _occurrences_in_cperm(
        self, cperm: CayleyPermutation
    ) -> Iterator[Tuple[int, ...]]:
        for occ in self.pattern.occurrences_in(cperm):
            if self.is_valid_occurrence(occ, cperm):
                yield occ

    def _occurrences_in_mesh(
        self, mesh_patt: "MeshPattern"
    ) -> Iterator[Tuple[int, ...]]:
        """Yield all occurrences of the mesh pattern in another mesh pattern."""
        for occ in self._occurrences_in_cperm(mesh_patt.pattern):
            if self.is_shaded_areas_map_correct(mesh_patt, occ):
                yield occ

    def is_avoided_by_cperm(self, cperm: CayleyPermutation) -> bool:
        """Returns true if the Cayely permutation avoids the mesh pattern."""
        return not self.is_contained_in_cperm(cperm)

    def is_contained_by_cperm(self, cperm: CayleyPermutation) -> bool:
        """Returns true if the Cayely permutation contains the mesh pattern."""
        return any(True for _ in self.occurrences_in(cperm))

    def avoids_shading(
        self,
        cperm: CayleyPermutation,
        indices: Tuple[int, ...],
    ) -> bool:
        """Return True if no points in shading that is projected to the
        Cayley permutation according to the indices."""
        for cell in self.shaded_cells:
            (i1, i2), (j1, j2) = self.region_of_perm(cperm, indices, cell)
            if any(i1 <= idx < i2 and j1 <= val < j2 for idx, val in enumerate(cperm)):
                return False
        return True

    def avoids_shaded_cell(
        self, cperm: CayleyPermutation, indices: tuple[int, ...], cell: Cell
    ) -> bool:
        """Returns true if the projected cell contains no points in the
        Cayley permutation with respect to the given indices."""
        (i1, i2), (j1, j2) = self.region_of_perm(cperm, indices, cell)
        return not any(
            i1 <= idx < i2 and j1 <= val < j2 for idx, val in enumerate(cperm)
        )

    def region_of_perm(
        self, cperm: CayleyPermutation, occ: tuple[int, ...], cell: Cell
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        Returns two tuples of the form (i1, i2) and (j1, j2) where
        - i1 and i2 are the lower and upper bounds for indices of the points
          that can be in the shaded region and
        - j1 and j2 are the lower and upper bounds for the values of the points
          that can be in the shaded region.
        """
        indices = tuple(occ)
        values = sorted(set(cperm[idx] for idx in occ))
        col, row = cell
        # get bounds for indices
        i1 = 0 if col == 0 else indices[col - 1]
        i2 = len(cperm) if col == len(occ) else indices[col]
        # get bounds for values
        row_idx = row // 2
        if row % 2:
            # odd, so on a row with a single value
            j1 = values[row_idx]
            j2 = values[row_idx] + 1
        else:
            # even, so on a row with many values
            j1 = 0 if row_idx == 0 else values[row_idx - 1]
            j2 = values[-1] + 1 if row_idx == len(values) else values[row_idx]
        return (i1, i2), (j1, j2)

    def complement(self) -> "MeshPattern":
        """Returns the complement of the mesh pattern - anything
        that was shaded now isn't, anything that wasn't now is
        apart from columns which currently remain unshaded."""
        return MeshPattern(
            self.pattern,
            (
                cell
                for cell in product(
                    range(len(self.pattern)), range(2 * (max(self.pattern) + 1))
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
        if len(self.pattern) == 0:
            return "+-+\n| |\n+-+\n"
        shaded_cell = "x"
        point = "\u25cf"
        n = len(self.pattern)
        m = max(self.pattern) + 1

        # create Cayley permutation
        empty_row = " |" * n
        plus_row = "+".join("-" for _ in range(n + 1))
        rows = [empty_row, plus_row] * m + [empty_row]

        # mark shaded cells
        for idx, val in enumerate(self.pattern):
            row = rows[val * 2 + 1]
            row = row[: idx * 2 + 1] + point + row[idx * 2 + 2 :]
            rows[val * 2 + 1] = row
        for idx, val in self.shaded_cells:
            row = rows[val]
            row = row[: idx * 2] + shaded_cell + row[idx * 2 + 1 :]
            rows[val] = row

        return "\n".join(reversed(rows))

    def __eq__(self, other: "MeshPattern") -> bool:
        if not isinstance(other, MeshPattern):
            return False
        return self.pattern == other.pattern and self.shaded_cells == other.shaded_cells

    def __hash__(self) -> int:
        return hash((self.pattern, self.shaded_cells))

    def __len__(self) -> int:
        return len(self.pattern)

    def __leq__(self, other: "MeshPattern") -> bool:
        return self.pattern <= other.pattern and self.shaded_cells <= other.shaded_cells

    def __lt__(self, other: "MeshPattern") -> bool:
        return self.pattern <= other.pattern and self.shaded_cells < other.shaded_cells

    def __str__(self) -> str:
        return f"MeshPattern({self.pattern}, {self.shaded_cells})"
