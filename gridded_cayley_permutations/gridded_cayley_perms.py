"""Gridded Cayley permutations."""

from itertools import combinations
from typing import Iterable, Iterator

from comb_spec_searcher import CombinatorialObject

from cayley_permutations import CayleyPermutation


class GriddedCayleyPerm(CombinatorialObject):
    """A Cayley permutation as a gridding."""

    # pylint: disable=too-many-public-methods
    def __init__(
        self,
        pattern: Iterable[int],
        positions: Iterable[tuple[int, int]],
        validate=False,
    ) -> None:
        self.pattern = CayleyPermutation(pattern)
        self.positions: tuple[tuple[int, int], ...] = tuple(
            (x, y) for x, y in positions
        )
        assert len(self.pattern) == len(self.positions)

        if validate:
            for cell in self.positions:
                if cell[0] < 0 or cell[1] < 0:
                    raise ValueError("Positions must be positive values.")

            if len(self.positions) != len(self.pattern):
                if len(self.positions) == 1:
                    self.positions = self.positions * len(self.pattern)
                else:
                    raise ValueError(
                        "Number of positions must be equal to number of "
                        "points in Cayley permutation."
                    )
            assert not self.contradictory()

    def contradictory(self) -> bool:
        """Checks if the points of the gridding
        contradicts the Cayley permutation."""
        return not self.increasing_are_above() or not self.indices_left_to_right()

    def increasing_are_above(self) -> bool:
        """Checks if a larger value is in a cell greater than or equal to the current one."""
        for j, val in enumerate(self.pattern):
            for i in range(j):
                if self.pattern[i] < val:
                    if self.positions[i][1] > self.positions[j][1]:
                        return False
                if self.pattern[i] > val:
                    if self.positions[i][1] < self.positions[j][1]:
                        return False
                if self.pattern[i] == val:
                    if self.positions[i][1] != self.positions[j][1]:
                        return False
        return True

    def indices_left_to_right(self) -> bool:
        """Checks if the indices of the gridding are left to right."""
        for i in range(len(self.positions) - 1):
            if self.positions[i][0] > self.positions[i + 1][0]:
                return False
        return True

    def avoids(self, patterns: Iterable["GriddedCayleyPerm"]) -> bool:
        """Checks if the gridding avoids the pattern."""
        return not self.contains(patterns)

    def contains(self, patterns: Iterable["GriddedCayleyPerm"]) -> bool:
        """Checks if the gridding contains anything from a list of patterns."""
        return any(self.contains_gridded_cperm(pattern) for pattern in patterns)

    def contains_gridded_cperm(self, gcperm: "GriddedCayleyPerm") -> bool:
        """Checks if the gridding contains another gridded Cayley permutation."""
        return any(True for _ in gcperm.occurrences_in(self))

    def occurrences_in(self, other: "GriddedCayleyPerm") -> Iterator[tuple[int, ...]]:
        """Returns all occurrences of self in other."""
        yield from self.pattern.occurrences_in(
            other.pattern, self.positions, other.positions
        )

    def contains_grid(self, gcperm: "GriddedCayleyPerm") -> bool:
        """Checks if the gridding contains the cells from another gridding."""
        for cell in gcperm.positions:
            if not gcperm.positions.count(cell) <= self.positions.count(cell):
                return False
        return True

    def indices_where_contains(
        self, gcperm: "GriddedCayleyPerm"
    ) -> list[tuple[int, ...]]:
        """Returns a list of the indices of the gridded Cayley permutation
        that contains another gridded Cayley permutation."""
        good_indices = []
        for indices in combinations(range(len(self.positions)), len(gcperm.positions)):
            subset_of_cells = []
            for idx in indices:
                subset_of_cells.append(self.positions[idx])
            if tuple(subset_of_cells) == gcperm.positions:
                good_indices.append(indices)
        return good_indices

    def insert_specific_point(
        self, cell: tuple[int, int], index: int, value: int
    ) -> Iterator["GriddedCayleyPerm"]:
        """Inserts a point into the gridded Cayley permutation at the index."""
        new_positions = self.positions[:index] + (cell,) + self.positions[index:]
        if value in self.values_in_row(cell[1]):
            new_pattern = CayleyPermutation(
                self.pattern[:index] + (value,) + self.pattern[index:]
            )
            yield GriddedCayleyPerm(new_pattern, new_positions)
        updated_pattern = tuple(val if val < value else val + 1 for val in self.pattern)
        new_pattern = CayleyPermutation(
            updated_pattern[:index] + (value,) + updated_pattern[index:]
        )
        yield GriddedCayleyPerm(new_pattern, new_positions)

    def insertion_different_value(
        self, value: int, cell: tuple[int, int]
    ) -> "GriddedCayleyPerm":
        """Inserts value to the end of the Cayley permutation
        then increases any values that were greater than or equal to it by one
        and adds cell to the positions."""
        new_positions = self.positions + (cell,)
        new_pattern = [val if val < value else val + 1 for val in self.pattern]
        new_pattern = new_pattern + [value]
        return GriddedCayleyPerm(CayleyPermutation(new_pattern), new_positions)

    def insertion_same_value(
        self, value: int, cell: tuple[int, int]
    ) -> "GriddedCayleyPerm":
        """Inserts value to the end of the Cayley permutation as a repeat
        and adds cell to the positions."""
        assert value in self.pattern
        new_positions = self.positions + (cell,)
        new_pattern = CayleyPermutation(self.pattern + (value,))
        return GriddedCayleyPerm(new_pattern, new_positions)

    def min_max_values_in_row(self, row_index: int) -> tuple[int, int]:
        """Returns the minimum and maximum values of elements in the row."""
        cells_in_row_or_below = []
        for cell in self.positions:
            if cell[1] == row_index:
                cells_in_row_or_below.append(cell)
        indices = self.indices_in_cells(cells_in_row_or_below)
        cperm = []
        for idx in indices:
            cperm.append(self.pattern[idx])
        if not cperm:
            if row_index == 0:
                return (-1, -1)
            min_value = self.min_max_values_in_row(row_index - 1)[1]
            return (min_value, min_value)
        return (min(cperm) - 1, max(cperm))

    def indices_in_row(self, row: int) -> tuple[int, ...]:
        """Returns all indices in the row."""
        return tuple(idx for idx, cell in enumerate(self.positions) if cell[1] == row)

    def values_in_row(self, row: int) -> tuple[int, ...]:
        """Returns all values in the row."""
        return tuple(self.pattern[i] for i in self.indices_in_row(row))

    def indices_in_col(self, col: int) -> tuple[int, ...]:
        """Returns all indices in the column."""
        return tuple(idx for idx, cell in enumerate(self.positions) if cell[0] == col)

    def values_in_col(self, col: int) -> tuple[int, ...]:
        """Returns all values in the column."""
        return tuple(self.pattern[i] for i in self.indices_in_col(col))

    def contains_index(self, direction: int, index: int) -> bool:
        """
        Returns True if the gridded Cayley permutation contains a point in the
        row/cols at index or index+1. (if direction = 0 then checks cols, else rows).
        """
        indices = [index, index + 1]
        for cell in self.positions:
            if cell[direction] in indices:
                return True
        return False

    def bounding_box_of_cell(self, cell: tuple[int, int]) -> tuple[int, int, int, int]:
        """Returns the minimum index, maximum index, minimum value and maximum value
        that can be inserted into the cell."""
        row_vals = self.values_in_row(cell[1])
        if row_vals:
            min_row_val = min(row_vals)
            max_row_val = max(row_vals) + 1
        else:
            for row in range(cell[1], -1, -1):
                smaller_row_vals = self.values_in_row(row)
                if smaller_row_vals:
                    min_row_val = max(smaller_row_vals) + 1
                    max_row_val = min_row_val
                    break
            else:
                min_row_val = 0
                max_row_val = 0
        col_indices = self.indices_in_col(cell[0])
        if col_indices:
            mindex = min(col_indices)
            maxdex = max(col_indices) + 1
        else:
            for col in range(cell[0], -1, -1):
                smaller_col_indices = self.indices_in_col(col)
                if smaller_col_indices:
                    mindex = max(smaller_col_indices) + 1
                    maxdex = mindex
                    break
            else:
                mindex = 0
                maxdex = 0
        return (mindex, maxdex, min_row_val, max_row_val)

    def indices_in_cells(self, cells: Iterable[tuple[int, int]]) -> tuple[int, ...]:
        """Returns the indices of the gridded Cayley permutation that are in the cells."""
        cells = set(cells)
        return tuple(idx for idx, cell in enumerate(self.positions) if cell in cells)

    def next_insertions(
        self, dimensions: tuple[int, int]
    ) -> Iterator[tuple[int, tuple[int, int]]]:
        """inserting the next index"""
        n, m = dimensions
        if not self.positions:
            for i in range(n):
                for j in range(m):
                    yield (0, (i, j))
            return
        last_cell = max(self.positions)
        next_cells = []
        for i in range(last_cell[0], n):
            for j in range(m):
                next_cells.append((i, j))
        for cell in next_cells:
            min_value, max_value = self.min_max_values_in_row(cell[1])
            for val in range(min_value + 1, max_value + 2):
                yield (val, cell)

    def row_containing_value(self, value: int) -> int:
        """Returns the row containing the value."""
        for i, patt_value in enumerate(self.pattern):
            if patt_value == value:
                return self.positions[i][1]
        raise ValueError("Value not in GriddedCayleyPerm.")

    def is_local(self):
        """Return True if only one cell in the positions."""
        for cell in self.positions:
            if cell != self.positions[0]:
                return False
        return True

    def find_active_cells(self) -> set[tuple[int, int]]:
        """Returns a set of cell that contain a value."""
        active_cells = set()
        for cell in self.positions:
            active_cells.add(cell)
        return active_cells

    def find_factors(self, point_rows):
        """Returns a list of the factors of the gridded Cayley permutation.
        If two different cells are in the same row or column then label them
        as together in component list using union sort.
        Then put together the cells that are in the same factors and return
        the sub gridded Cayley permutation of the cells."""
        cells = list(self.find_active_cells())
        n = len(cells)
        component = list(range(n))
        for idx, cell in enumerate(cells):
            for idx2, cell2 in enumerate(cells):
                if idx != idx2:
                    if cell[0] == cell2[0] or (
                        cell[1] == cell2[1]
                        and (
                            cell[1] not in point_rows
                            or self.pattern
                            in (CayleyPermutation([0, 1]), CayleyPermutation([1, 0]))
                        )
                    ):
                        component[idx2] = component[idx]
        factors = []
        for i in set(component):
            factor = []
            for j in range(n):
                if component[j] == i:
                    factor.append(cells[j])
            factors.append(factor)
        return [self.sub_gridded_cayley_perm(cells) for cells in factors]

    def sub_gridded_cayley_perm(
        self, cells: Iterable[tuple[int, int]]
    ) -> "GriddedCayleyPerm":
        """Returns the sub gridded Cayley permutation of the cells."""
        cells = set(cells)
        new_positions = []
        new_pattern = []
        for idx, cell in enumerate(self.positions):
            if cell in cells:
                new_positions.append(cell)
                new_pattern.append(self.pattern[idx])
        return GriddedCayleyPerm(
            CayleyPermutation.standardise(new_pattern), new_positions
        )

    def sub_gridded_cayley_perms_at_indices(
        self, indices: tuple[int, ...]
    ) -> "GriddedCayleyPerm":
        """Return the sub gridded cayley perm at the given indices"""
        return GriddedCayleyPerm(
            self.pattern.subperm_from_indices(indices),
            tuple(self.positions[idx] for idx in indices),
        )

    def sub_gridded_cayley_perms(self, size: int) -> frozenset["GriddedCayleyPerm"]:
        """Return all the gridded cayley permutations of given size contained in self"""
        return frozenset(
            self.sub_gridded_cayley_perms_at_indices(indices)
            for indices in combinations(range(len(self)), size)
        )

    def to_jsonable(self) -> dict:
        """Returns a jsonable dictionary of the gridded Cayley permutation."""
        return {"pattern": self.pattern.to_jsonable(), "positions": self.positions}

    @classmethod
    def from_dict(cls, d: dict) -> "GriddedCayleyPerm":
        """Returns a GriddedCayleyPerm from a dictionary."""
        return GriddedCayleyPerm(
            CayleyPermutation.from_dict(d["pattern"]), d["positions"]
        )

    def __len__(self) -> int:
        return len(self.pattern)

    def __repr__(self) -> str:
        return f"GriddedCayleyPerm({repr(self.pattern)}, {self.positions})"

    def __str__(self) -> str:
        if len(self) == 0:
            return "empty"
        return f"{self.pattern}: {','.join(str(cell) for cell in self.positions)}"

    def __lt__(self, other: "GriddedCayleyPerm") -> bool:
        return (self.pattern, self.positions) < (other.pattern, other.positions)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GriddedCayleyPerm):
            return False
        return self.pattern == other.pattern and self.positions == other.positions

    def __hash__(self) -> int:
        return hash((self.pattern, self.positions))
