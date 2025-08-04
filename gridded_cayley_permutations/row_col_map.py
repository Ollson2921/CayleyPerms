"""
The RowColMap class is used to map gridded Cayley permutations.

It provides methods for mapping and generating preimages of gridded Cayley permutations.

It is assumed that the pre-image of any row or column is an interval.
"""

from functools import cached_property
from itertools import chain, product
from typing import TYPE_CHECKING, Iterable, Iterator, Tuple

from gridded_cayley_permutations import GriddedCayleyPerm

if TYPE_CHECKING:
    # pylint: disable=all
    from .tilings import Tiling


OBSTRUCTIONS = Tuple[GriddedCayleyPerm, ...]
REQUIREMENTS = Tuple[Tuple[GriddedCayleyPerm, ...], ...]
Cell = Tuple[int, int]


class RowColMap:
    """
    The pre-image of any value is an interval.
    If a > b then every pre-image of a is to the greater than every pre-image of b.
    """

    def __init__(self, col_map: dict[int, int], row_map: dict[int, int]):
        self.row_map = dict(sorted(row_map.items(), key=lambda item: item[1]))
        self.col_map = dict(sorted(col_map.items(), key=lambda item: item[1]))

    def map_gridded_cperm(self, gcp: GriddedCayleyPerm) -> GriddedCayleyPerm:
        """
        Map a gridded Cayley permutation according to the row and column maps.
        """
        new_positions = []
        for cell in gcp.positions:
            new_cell = (self.col_map[cell[0]], self.row_map[cell[1]])
            new_positions.append((new_cell))
        return GriddedCayleyPerm(gcp.pattern, new_positions)

    def map_gridded_cperms(self, gcps: Iterable[GriddedCayleyPerm]) -> OBSTRUCTIONS:
        """
        Map a gridded Cayley permutation according to the column and row maps.
        """
        return tuple(self.map_gridded_cperm(gcp) for gcp in gcps)

    def map_requirements(
        self, requirements: Iterable[Iterable[GriddedCayleyPerm]]
    ) -> REQUIREMENTS:
        """
        Map a list of requirements according to the column and row maps.
        """
        return tuple(self.map_gridded_cperms(req) for req in requirements)

    def preimages_of_rows_and_cols(
        self, cols: Iterable[int], rows: Iterable[int]
    ) -> Tuple[set[int], set[int]]:
        """Returns the preimages of the rows and cols"""
        return set(self.preimages_of_cols(cols)), set(self.preimages_of_rows(rows))

    def image_rows_and_cols(self) -> Tuple[set[int], set[int]]:
        """Gives the indices for the rows and cols in the image"""
        return set(self.col_map.values()), set(self.row_map.values())

    @cached_property
    def image_cells(self) -> set[Cell]:
        """Gives the cells in the image of the map"""
        return set(product(*self.image_rows_and_cols()))

    def preimage_of_gridded_cperm(
        self, gcp: GriddedCayleyPerm
    ) -> Iterator[GriddedCayleyPerm]:
        """
        Return the preimages of a gridded Cayley permutation with respect to the map.
        Only use this on subgcps that are fully in the image.

        If a gcp is not fully in the image cells then
        new_positions will be cells not in the preimage so will raise an error.
        """
        if any(cell not in self.image_cells for cell in gcp.positions):
            raise ValueError(f"The gridded Cayley perm {gcp} does not have a preimage.")
        for cols, rows in product(
            self._product_of_cols(gcp), self._product_of_rows(gcp)
        ):
            new_positions = tuple(zip(cols, rows))

            yield GriddedCayleyPerm(gcp.pattern, new_positions)

    def _product_of_rows(self, gcp: GriddedCayleyPerm) -> Iterator[tuple[int, ...]]:
        """Yields all possible combinations of preimages of the rows of gcp."""
        row_pos = tuple(cell[1] for cell in gcp.positions)
        preimages_of_gcp = (
            self._preimages_of_row_of_gcp(row, gcp) for row in self.row_codomain
        )
        codomain = self.row_codomain
        yield from self._product_of_row_or_columns(row_pos, preimages_of_gcp, codomain)

    def _product_of_cols(self, gcp: GriddedCayleyPerm) -> Iterator[tuple[int, ...]]:
        """Yields all possible combinations of preimages of the columns of gcp."""
        col_pos = tuple(cell[0] for cell in gcp.positions)
        preimages_of_gcp = (
            self._preimages_of_col_of_gcp(col, gcp) for col in self.col_codomain
        )
        codomain = self.col_codomain
        yield from self._product_of_row_or_columns(col_pos, preimages_of_gcp, codomain)

    def _product_of_row_or_columns(
        self,
        positions: tuple[int, ...],
        preimages_of_gcp: Iterable[Iterable[tuple[int, ...]]],
        codomain: tuple[int, ...],
    ) -> Iterator[tuple[int, ...]]:
        indices = {}
        for row in codomain:
            indices[row] = [idx for idx, val in enumerate(positions) if val == row]
        working_list = [-1] * len(positions)
        for row_values_at_indices in product(*preimages_of_gcp):
            for row, values_at_row in zip(codomain, row_values_at_indices):
                for idx, val in zip(indices[row], values_at_row):
                    working_list[idx] = val
            yield tuple(working_list)

    @cached_property
    def row_codomain(self) -> tuple[int, ...]:
        """Return the codomain of the row map."""
        return tuple(sorted(set(self.row_map.values())))

    @cached_property
    def col_codomain(self) -> tuple[int, ...]:
        """Return the codomain of the column map."""
        return tuple(sorted(set(self.col_map.values())))

    @staticmethod
    def _partition(n: int, k: int) -> Iterator[list[int]]:
        """Partition n into k parts

        NOTE: this is slow, be smarter"""
        if k == 1:
            yield [n]
            return
        for i in range(n + 1):
            for result in RowColMap._partition(n - i, k - 1):
                yield [i] + result

    def expand_at_index(
        self, number_of_cols: int, number_of_rows: int, col_index: int, row_index: int
    ) -> "RowColMap":
        """Adds number_of_cols new columns to the at col_index and
        Adds number_of_rows new rows to the map at row_index
            Assumes we've modified the image and preimage cells in the same way"""
        new_col_map, new_row_map = {}, {}
        # This bit moves the existing mappings
        for item in self.col_map.items():
            adjust = int(item[0] >= col_index) * number_of_cols
            new_col_map[item[0] + adjust] = item[1] + adjust
        for item in self.row_map.items():
            adjust = int(item[0] >= row_index) * number_of_rows
            new_row_map[item[0] + adjust] = item[1] + adjust
        # This bit adds the new dictionary items
        original_col, original_row = (
            self.col_map[col_index],
            self.row_map[row_index],
        )
        for i in range(number_of_cols):
            new_col_map[col_index + i] = original_col + i
        for i in range(number_of_rows):
            new_row_map[row_index + i] = original_row + i
        return self.__class__(new_col_map, new_row_map)

    def preimages_of_row(self, row: int) -> tuple[int, ...]:
        """Return the preimages of all values in the row."""
        return tuple(key for key, value in self.row_map.items() if value == row)

    def preimages_of_rows(self, rows: Iterable[int]) -> tuple[int, ...]:
        """Return the preimages of all values in the rows."""
        rows = set(rows)
        return tuple(key for key, value in self.row_map.items() if value in rows)

    def preimages_of_col(self, col: int) -> tuple[int, ...]:
        """Return the preimages of all values in the column."""
        return tuple(key for key, value in self.col_map.items() if value == col)

    def preimages_of_cols(self, cols: Iterable[int]) -> tuple[int, ...]:
        """Return the preimages of all values in the columns."""
        cols = set(cols)
        return tuple(key for key, value in self.col_map.items() if value in cols)

    def _preimages_of_row_of_gcp(
        self, row: int, gcp: GriddedCayleyPerm
    ) -> Iterator[tuple[int, ...]]:
        """Yields tuples of preimages of the values in the row."""
        values_in_row = gcp.values_in_row(row)
        pre_image_values = self.preimages_of_row(row)
        yield from self._preimages_of_values(values_in_row, pre_image_values)

    def _preimages_of_col_of_gcp(
        self, col: int, gcp: GriddedCayleyPerm
    ) -> Iterator[tuple[int, ...]]:
        """Yields tuples of preimages of the values in the column."""
        indices_in_col = gcp.indices_in_col(col)
        pre_image_values = self.preimages_of_col(col)
        yield from self._preimages_of_values(indices_in_col, pre_image_values)

    def _preimages_of_values(
        self, values_in_col: tuple[int, ...], pre_image_values: tuple[int, ...]
    ) -> Iterator[tuple[int, ...]]:
        """Yields tuples of preimages of the given values."""
        if not values_in_col:
            yield tuple()
            return
        number_of_values = max(values_in_col) - min(values_in_col) + 1
        size = len(pre_image_values)
        values_ordered = sorted(set(values_in_col))
        for partition in self._partition(number_of_values, size):
            preimage = [-1] * len(values_in_col)
            seen_so_far = 0
            for idx, part in enumerate(partition):
                new_col = pre_image_values[idx]
                vals = values_ordered[seen_so_far : seen_so_far + part]
                seen_so_far += part
                for idx, val in enumerate(values_in_col):
                    if val in vals:
                        preimage[idx] = new_col
            yield tuple(preimage)

    def preimage_map(
        self,
    ) -> tuple[dict[int, tuple[int, ...]], dict[int, tuple[int, ...]]]:
        """Return the preimage map of the row and column maps."""
        return {i: self.preimages_of_col(i) for i in set(self.col_map.values())}, {
            i: self.preimages_of_row(i) for i in set(self.row_map.values())
        }

    def restriction(
        self, col_values: Iterable[int], row_values: Iterable[int]
    ) -> "RowColMap":
        """
        The restriction of the row col map to only the col_values
        and the row_values of the preimage.
        """
        new_col_map, new_row_map = {}, {}
        for index in col_values:
            new_col_map[index] = self.col_map[index]
        for index in row_values:
            new_row_map[index] = self.row_map[index]
        return self.__class__(new_col_map, new_row_map)

    def standardise_map(self) -> "RowColMap":
        """
        Return the row col map with the keys and the values
        both standardised to the integers 0 to n.
        """
        keys, values = list(set(self.col_map.keys())), list(set(self.col_map.values()))
        key_map, value_map = {key: keys.index(key) for key in keys}, {
            value: values.index(value) for value in values
        }
        new_col_map = {key_map[key]: value_map[self.col_map[key]] for key in keys}
        keys, values = list(set(self.row_map.keys())), list(set(self.row_map.values()))
        key_map, value_map = {key: keys.index(key) for key in keys}, {
            value: values.index(value) for value in values
        }
        new_row_map = {key_map[key]: value_map[self.row_map[key]] for key in keys}
        return self.__class__(new_col_map, new_row_map)

    def preimage_of_obstructions(
        self, obstructions: Iterable[GriddedCayleyPerm]
    ) -> OBSTRUCTIONS:
        """Return the preimages of the obstructions."""
        return tuple(
            chain.from_iterable(
                self.preimage_of_gridded_cperm(ob) for ob in obstructions
            )
        )

    def preimage_of_requirements(
        self, requirements: Iterable[Iterable[GriddedCayleyPerm]]
    ) -> REQUIREMENTS:
        """Return the preimages of the requirements."""
        return tuple(self.preimage_of_obstructions(req) for req in requirements)

    def preimage_of_tiling(self, tiling: "Tiling") -> tuple[OBSTRUCTIONS, REQUIREMENTS]:
        """Return the preimage of the tiling."""
        return self.preimage_of_obstructions(
            tiling.obstructions
        ), self.preimage_of_requirements(tiling.requirements)

    def preimage_of_cell(self, cell: tuple[int, int]) -> tuple[tuple[int, int], ...]:
        """Return the preimage of the cell."""
        return tuple(
            (x, y)
            for x in self.preimages_of_col(cell[0])
            for y in self.preimages_of_row(cell[1])
        )

    def preimage_of_cells(
        self, cells: Iterable[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        """Return the preimage of the cells."""
        return list(chain.from_iterable(self.preimage_of_cell(cell) for cell in cells))

    def __repr__(self) -> str:
        return f"RowColMap({repr(self.col_map)}, {repr(self.row_map)})"

    def __str__(self) -> str:
        return f"RowColMap({self.col_map},\n {self.row_map})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RowColMap):
            return NotImplemented
        return self.col_map == other.col_map and self.row_map == other.row_map

    def __lt__(self, other: "RowColMap") -> bool:
        return (
            tuple(sorted(self.col_map.items())),
            tuple(sorted(self.row_map.items())),
        ) < (tuple(sorted(other.col_map.items())), tuple(sorted(other.row_map.items())))

    def __leq__(self, other: "RowColMap") -> bool:
        return (
            tuple(sorted(self.col_map.items())),
            tuple(sorted(self.row_map.items())),
        ) <= (
            tuple(sorted(other.col_map.items())),
            tuple(sorted(other.row_map.items())),
        )
