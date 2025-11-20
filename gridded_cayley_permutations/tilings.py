"""
The Tiling class, that inherits from CombinatorialClass.

A tiling represents the set of gridded Cayley permutations with cells coming up to a given
dimension, that avoid a set of obstructions and contain a set of requirements.
"""

from collections import defaultdict
from copy import copy
from functools import cached_property
from itertools import chain, product
from math import factorial
from typing import Iterable, Iterator

from comb_spec_searcher import CombinatorialClass

from cayley_permutations import CayleyPermutation
from check_regular_ins_enc import (
    regular_vertical_insertion_encoding,
    regular_horizontal_insertion_encoding,
)

from .gridded_cayley_perms import GriddedCayleyPerm
from .minimal_gridded_cperms import MinimalGriddedCayleyPerm
from .row_col_map import RowColMap
from .simplify_obstructions_and_requirements import SimplifyObstructionsAndRequirements


def binomial(x: int, y: int) -> int:
    """Return the binomial coefficient x choose y."""
    try:
        return factorial(x) // factorial(y) // factorial(x - y)
    except ValueError:
        return 0


class Tiling(CombinatorialClass):
    """A tiling represents the set of gridded Cayley permutations with cells coming up to a given
    dimension, that avoid a set of obstructions and contain a set of requirements."""

    # pylint: disable=too-many-public-methods
    def __init__(
        self,
        obstructions: Iterable[GriddedCayleyPerm],
        requirements: Iterable[Iterable[GriddedCayleyPerm]],
        dimensions: tuple[int, int],
        simplify=True,
    ) -> None:
        self.obstructions = tuple(obstructions)
        self.requirements = tuple(tuple(req) for req in requirements)
        self.dimensions = (dimensions[0], dimensions[1])

        algorithm = SimplifyObstructionsAndRequirements(
            self.obstructions, self.requirements, self.dimensions
        )
        if simplify:
            algorithm.simplify()
        self.obstructions = algorithm.obstructions
        self.requirements = algorithm.requirements

    def _gridded_cayley_permutations(self, size: int) -> Iterator[GriddedCayleyPerm]:
        """
        Generating gridded Cayley permutations of size 'size'.
        """
        if size == 0:
            if not GriddedCayleyPerm(CayleyPermutation([]), []) in self.obstructions:
                yield GriddedCayleyPerm(CayleyPermutation([]), [])
            return
        for gcp in self._gridded_cayley_permutations(size - 1):
            next_ins = gcp.next_insertions(self.dimensions)
            for val, cell in next_ins:
                next_gcp = gcp.insertion_different_value(val, cell)
                if self.satisfies_obstructions(next_gcp):
                    yield next_gcp
                if val in gcp.pattern:
                    if cell[1] == gcp.row_containing_value(val):
                        next_gcp = gcp.insertion_same_value(val, cell)
                        if self.satisfies_obstructions(next_gcp):
                            yield next_gcp

    def gridded_cayley_permutations(self, size: int) -> Iterator[GriddedCayleyPerm]:
        """Generating gridded Cayley permutations of size 'size' (that satisfy the requirements)."""
        yield from filter(
            self.satisfies_requirements, self._gridded_cayley_permutations(size)
        )

    def satisfies_obstructions(self, gcp: GriddedCayleyPerm) -> bool:
        """
        Checks whether a single gridded Cayley permutation satisfies the obstructions.
        """
        return not gcp.contains(self.obstructions)

    def satisfies_requirements(self, gcp: GriddedCayleyPerm) -> bool:
        """
        Checks whether a single gridded Cayley permutation satisfies the requirements.
        """
        for req in self.requirements:
            if not gcp.contains(req):
                return False
        return True

    def gcp_in_tiling(self, gcp: GriddedCayleyPerm) -> bool:
        """
        Checks whether a single gridded Cayley permutation is in the tiling.
        """
        return (
            all(
                x < self.dimensions[0] and y < self.dimensions[1]
                for x, y in gcp.positions
            )
            and self.satisfies_obstructions(gcp)
            and self.satisfies_requirements(gcp)
        )

    @cached_property
    def active_cells(self) -> set[tuple[int, int]]:
        """Returns the set of active cells in the tiling.
        (Cells are active if they do not contain a point obstruction.)"""
        return SimplifyObstructionsAndRequirements(
            self.obstructions, self.requirements, self.dimensions
        ).active_cells()

    def positive_cells(self) -> set[tuple[int, int]]:
        """Returns a set of cells that are positive in the tiling.
        (Cells are positive if they contain a point requirement.)"""
        positive_cells = set()
        for req_list in self.requirements:
            current = set(req_list[0].positions)
            for req in req_list:
                current = current.intersection(req.positions)
            positive_cells.update(current)
        return positive_cells

    def point_cells(self) -> set[tuple[int, int]]:
        """Returns the set of cells that can only contain a point."""
        # can this be made more efficient?
        point_cells = set()
        for cell in self.positive_cells():
            if (
                GriddedCayleyPerm(CayleyPermutation([0, 1]), [cell, cell])
                in self.obstructions
                and GriddedCayleyPerm(CayleyPermutation([1, 0]), [cell, cell])
                in self.obstructions
                and GriddedCayleyPerm(CayleyPermutation([0, 0]), [cell, cell])
                in self.obstructions
            ):
                point_cells.add(cell)
        return point_cells

    def not_blank_cells(self) -> set[tuple[int, int]]:
        """Returns the set of cells that are a position for some ob or req."""
        if not self.obstructions and not self.requirements:
            return set()
        combined_obs_and_reqs = self.obstructions + tuple(chain(*self.requirements))
        return set(chain(*(gcp.positions for gcp in combined_obs_and_reqs)))

    def blank_cells(self) -> set[tuple[int, int]]:
        """Returns the set of cells that contain no obs or reqs."""
        return (
            set(product(range(self.dimensions[0]), range(self.dimensions[1])))
            - self.not_blank_cells()
        )

    def delete_columns(self, cols: Iterable[int]) -> "Tiling":
        """
        Deletes columns at indices specified
        from the tiling and returns the new tiling.
        """
        return self.delete_rows_and_columns(cols, [])

    def delete_rows(self, rows: Iterable[int]) -> "Tiling":
        """
        Deletes rows at indices specified
        from the tiling and returns the new tiling.
        """
        return self.delete_rows_and_columns([], rows)

    def delete_rows_and_columns(
        self, cols: Iterable[int], rows: Iterable[int]
    ) -> "Tiling":
        """
        Deletes rows and columns at indices specified
        from the tiling and returns the new tiling.
        """
        rows, cols = set(rows), set(cols)
        col_map = {}
        counter = 0
        for ind in range(self.dimensions[0]):
            if ind in cols:
                continue
            col_map[ind] = counter
            counter += 1

        row_map = {}
        counter = 0
        for ind in range(self.dimensions[1]):
            if ind in rows:
                continue
            row_map[ind] = counter
            counter += 1
        rc_map = RowColMap(col_map, row_map)
        new_obstructions = tuple(
            ob
            for ob in self.obstructions
            if all(x not in cols and y not in rows for x, y in ob.positions)
        )

        new_obstructions = rc_map.map_gridded_cperms(new_obstructions)
        new_requirements = []
        for req_list in self.requirements:
            new_req_list = tuple(
                req
                for req in req_list
                if all(x not in cols and y not in rows for x, y in req.positions)
            )
            if new_req_list:
                new_requirements.append(new_req_list)
        new_requirements = list(rc_map.map_requirements(new_requirements))
        new_dimensions = (
            self.dimensions[0] - len(cols),
            self.dimensions[1] - len(rows),
        )
        return Tiling(
            new_obstructions, new_requirements, new_dimensions, simplify=False
        )

    def find_empty_rows_and_columns(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """Returns a list of the indices of empty rows and
        a list of the indices of empty columns."""
        if self.dimensions == (0, 0):
            return tuple(), tuple()
        col_count: dict[int, int] = defaultdict(int)
        row_count: dict[int, int] = defaultdict(int)
        for ob in self.obstructions:
            if len(ob) == 1:
                col_count[ob.positions[0][0]] += 1
                row_count[ob.positions[0][1]] += 1
        empty_cols = tuple(
            col for col, count in col_count.items() if count == self.dimensions[1]
        )
        empty_rows = tuple(
            row for row, count in row_count.items() if count == self.dimensions[0]
        )
        return empty_cols, empty_rows

    def find_blank_columns_and_rows(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """Returns a list of the indices of blank columns and
        a list of the indices of blank rows."""
        if self.dimensions == (0, 0):
            return tuple(), tuple()
        if not self.obstructions and not self.requirements:
            return tuple(range(self.dimensions[0])), tuple(range(self.dimensions[1]))
        not_blank_cols, not_blank_rows = zip(*self.not_blank_cells())
        blank_cols = tuple(set(range(self.dimensions[0])) - set(not_blank_cols))
        blank_rows = tuple(set(range(self.dimensions[1])) - set(not_blank_rows))
        return blank_cols, blank_rows

    def remove_empty_rows_and_columns(self) -> "Tiling":
        """Deletes any rows and columns in the gridding that are empty"""
        empty_cols, empty_rows = self.find_empty_rows_and_columns()
        return self.delete_rows_and_columns(empty_cols, empty_rows)

    def remove_empty_columns(self) -> "Tiling":
        """Deletes any columns in the gridding that are empty"""
        empty_cols, _ = self.find_empty_rows_and_columns()
        return self.delete_columns(empty_cols)

    def sub_tiling(self, cells: Iterable[tuple[int, int]], simplify=True) -> "Tiling":
        """
        Returns a sub-tiling of the tiling at the given cells.
        """
        cells = set(cells)
        obstructions = []
        for ob in self.obstructions:
            if all(cell in cells for cell in ob.positions):
                obstructions.append(ob)
        requirements = []
        for req_list in self.requirements:
            new_req_list = []
            for req in req_list:
                if all(cell in cells for cell in req.positions):
                    new_req_list.append(req)
            if new_req_list:
                requirements.append(new_req_list)
                # assert len(new_req_list) == len(req_list)

        for cell in product(range(self.dimensions[0]), range(self.dimensions[1])):
            if cell not in cells:
                obstructions.append(GriddedCayleyPerm(CayleyPermutation([0]), [cell]))

        return Tiling(obstructions, requirements, self.dimensions, simplify=simplify)

    # Requirement insertion methods

    def remove_requirements(self, reqs: Iterable[GriddedCayleyPerm]) -> "Tiling":
        """
        Returns a new tiling with the given requirements removed. (requirements, not req lists)
        """
        new_requirements = []
        for req_list in self.requirements:
            new_req_list = [req for req in req_list if req not in reqs]
            if new_req_list:
                new_requirements.append(new_req_list)
        return Tiling(self.obstructions, new_requirements, self.dimensions)

    def add_obstructions(self, gcps: Iterable[GriddedCayleyPerm]) -> "Tiling":
        """
        Returns a new tiling with the given gridded Cayley permutations added as obstructions.
        """
        return Tiling(
            self.obstructions + tuple(gcps), self.requirements, self.dimensions
        )

    def add_obstruction(self, gcp: GriddedCayleyPerm) -> "Tiling":
        """
        Returns a new tiling with the given gridded Cayley permutation added as an obstruction.
        """
        return self.add_obstructions([gcp])

    def add_requirements(
        self, requirements: Iterable[Iterable[GriddedCayleyPerm]]
    ) -> "Tiling":
        """
        Returns a new tiling with the given requirements added.
        """
        return Tiling(
            self.obstructions, self.requirements + tuple(requirements), self.dimensions
        )

    def add_requirement_list(
        self, requirement_list: Iterable[GriddedCayleyPerm]
    ) -> "Tiling":
        """
        Returns a new tiling with the given requirement list added.
        """
        return self.add_requirements([requirement_list])

    @cached_property
    def point_rows(self) -> set[int]:
        """Returns the set of rows which only contain points of the same value."""
        return SimplifyObstructionsAndRequirements(
            self.obstructions, self.requirements, self.dimensions
        ).point_rows()

    def cells_in_row(self, row: int) -> set[tuple[int, int]]:
        """Returns the set of active cells in the given row."""
        cells = set()
        for cell in self.active_cells:
            if cell[1] == row:
                cells.add(cell)
        return cells

    def cells_in_col(self, col: int) -> set[tuple[int, int]]:
        """Returns the set of active cells in the given column."""
        cells = set()
        for cell in self.active_cells:
            if cell[0] == col:
                cells.add(cell)
        return cells

    def col_is_positive(self, col: int) -> bool:
        """Return true if the column must contain at least one point."""
        req_list = tuple(
            GriddedCayleyPerm(CayleyPermutation([0]), [cell])
            for cell in self.cells_in_col(col)
        )
        return self.add_obstructions(req_list).is_empty()

    def row_is_positive(self, row: int) -> bool:
        """Return true if the row must contain at least one point."""
        req_list = tuple(
            GriddedCayleyPerm(CayleyPermutation([0]), [cell])
            for cell in self.cells_in_row(row)
        )
        return self.add_obstructions(req_list).is_empty()

    # Fusion methods

    def fuse(self, fuse_rows: bool, index: int) -> "Tiling":
        """If fuse_rows, tries to fuse rows, otherwise, tries to fuse cols."""
        if fuse_rows == 0:
            return self.delete_columns([index])
        return self.delete_rows([index])

    def can_fuse_row(self, index: int) -> bool:
        """Returns true if row at index is fusable"""
        return self.is_fusable(True, index)

    def can_fuse_col(self, index: int) -> bool:
        """Returns true if row at index is fusable"""
        return self.is_fusable(False, index)

    def is_fusable(self, fuse_rows: bool, index: int) -> bool:
        """If fuse rows, checks if the rows at index and index+1 are fuseable,
        otherwise does the same for cols at index and index+1."""
        if fuse_rows:
            test_tiling = self.delete_rows([index])
        else:
            test_tiling = self.delete_columns([index])
        test_tiling = test_tiling.split_row_or_col(fuse_rows, index)
        return test_tiling == self

    def split_row_or_col(self, unfuse_rows: bool, index: int) -> "Tiling":
        """Unfuses a row (if unfuse_rows) or col (otherwise)
        at index without simplifying the Tiling."""
        direction_map = {
            i: i - int(i > index) for i in range(self.dimensions[unfuse_rows] + 1)
        }
        identity_map = {i: i for i in range(self.dimensions[not unfuse_rows])}
        if unfuse_rows:
            new_map = RowColMap(identity_map, direction_map)
            new_dimensions = (self.dimensions[0], self.dimensions[1] + 1)
        else:
            new_map = RowColMap(direction_map, identity_map)
            new_dimensions = (self.dimensions[0] + 1, self.dimensions[1])
        new_obstructions = new_map.preimage_of_obstructions(self.obstructions)
        new_requirements = new_map.preimage_of_requirements(self.requirements)
        return Tiling(
            new_obstructions, new_requirements, new_dimensions, simplify=False
        )

    # Construction methods

    @staticmethod
    def from_vincular(cperm: CayleyPermutation, adjacencies: Iterable[int]) -> "Tiling":
        """
        Both cperm and adjacencies must be 0 based. Creates a tiling from a
        vincular pattern. Adjacencies is a list of positions where i in
        adjacencies means positions i and i+1 must be adjacent.
        """
        dimensions = (len(cperm), max(cperm) + 1)
        all_obs, all_reqs = [], []
        perm_cells = [(2 * k + 1, 2 * cperm[k] + 1) for k in range(dimensions[0])]
        cols, rows = [2 * i + 1 for i in range(dimensions[0])] + [
            2 * i + 2 for i in adjacencies
        ], [2 * i + 1 for i in range(dimensions[1])]
        col_cells = [
            cell
            for cell in product(cols, range(2 * dimensions[1] + 1))
            if cell not in perm_cells
        ]  # this is all the cells that will have point obstructions
        for cell in col_cells:
            all_obs.append(GriddedCayleyPerm(CayleyPermutation([0]), [cell]))
        for i in rows:  # this puts the 01,10 obstructions across each row
            for j in range(2 * dimensions[0] + 1):
                cell1 = (j, i)
                if cell1 not in col_cells:
                    for k in range(j, 2 * dimensions[0] + 1):
                        cell2 = (k, i)
                        if cell2 not in col_cells:
                            all_obs.append(
                                GriddedCayleyPerm(
                                    CayleyPermutation([0, 1]), [cell1, cell2]
                                )
                            )
                            all_obs.append(
                                GriddedCayleyPerm(
                                    CayleyPermutation([1, 0]), [cell1, cell2]
                                )
                            )
        for (
            cell
        ) in (
            perm_cells
        ):  # this puts the point requirement and the 00 obstruction according to the permutation
            all_reqs.append([GriddedCayleyPerm(CayleyPermutation([0]), [cell])])
            all_obs.append(GriddedCayleyPerm(CayleyPermutation([0, 0]), [cell, cell]))
        return Tiling(all_obs, all_reqs, (2 * dimensions[0] + 1, 2 * dimensions[1] + 1))

    # CSS methods

    def to_jsonable(self) -> dict:
        res = {
            "obstructions": [ob.to_jsonable() for ob in self.obstructions],
            "requirements": [
                [req.to_jsonable() for req in req_list]
                for req_list in self.requirements
            ],
            "dimensions": self.dimensions,
        }
        res.update(super().to_jsonable())
        return res

    @classmethod
    def from_dict(cls, d: dict) -> "Tiling":
        return Tiling(
            [GriddedCayleyPerm.from_dict(ob) for ob in d["obstructions"]],
            [
                [GriddedCayleyPerm.from_dict(req) for req in req_list]
                for req_list in d["requirements"]
            ],
            d["dimensions"],
        )

    def maximum_length_of_minimal_gridded_cayley_perm(self) -> int:
        """Return an upper bound on the length of a minimal gridded Cayley permutation."""
        return sum(max(len(gcp) for gcp in req_list) for req_list in self.requirements)

    def is_empty(self) -> bool:
        return any(len(ob) == 0 for ob in self.obstructions) or self._is_empty()

    def _is_empty(self) -> bool:
        for _ in self.minimal_gridded_cperms():
            return False
        return True

    def is_horizontal_insertion_encodable(self) -> bool:
        """Returns True if the tiling has a horizontal insertion encoding."""
        if self.dimensions[1] == 1:
            patterns_in_cells: list[tuple[CayleyPermutation]] = []
            for cell in self.active_cells:
                patterns_in_cells.append(tuple(
                    gcp.pattern
                    for gcp in self.obstructions
                    if all(c[0] == cell[0] for c in gcp.positions)
                ))
            if all(regular_horizontal_insertion_encoding(patterns_in_cell) for patterns_in_cell in patterns_in_cells):
                    return True
        return False

    def is_vertical_insertion_encodable(self) -> bool:
        """Returns True if the tiling has a vertical insertion encoding."""
        if self.dimensions[0] == 1:
            patterns_in_cells: list[tuple[CayleyPermutation]] = []
            for cell in self.active_cells:
                patterns_in_cells.append(tuple(
                    gcp.pattern
                    for gcp in self.obstructions
                    if all(c[1] == cell[1] for c in gcp.positions)
                ))
            if all(regular_vertical_insertion_encoding(patterns_in_cell) for patterns_in_cell in patterns_in_cells):
                    return True
        return False

    def is_subset(self, other: "Tiling") -> bool:
        """
        Return True if the set of gridded permutations on self
        is a subset of the set of gridded permutations on other.
        """
        if not self.dimensions == other.dimensions:
            return False
        return set(self.obstructions).issubset(set(other.obstructions)) and set(
            self.requirements
        ).issubset(set(other.requirements))

    def minimal_gridded_cperms(self) -> Iterator[GriddedCayleyPerm]:
        """Returns an iterator of minimal gridded Cayley permutations."""
        if self.requirements:
            yield from MinimalGriddedCayleyPerm(
                self.obstructions, self.requirements
            ).minimal_gridded_cperms()
        else:
            yield GriddedCayleyPerm(CayleyPermutation([]), [])

    def is_atom(self) -> bool:
        """Return True if tiling is a single gridded permutation."""
        return (
            (self.active_cells == self.point_cells())
            and self.fully_isolated()
            and not any(len(ob.positions) == 0 for ob in self.obstructions)
        )

    def fully_isolated(self) -> bool:
        """Check if all cells are isolated on their rows and columns."""
        seen_col: list[int] = []
        point_rows = self.point_rows
        for i, j in self.active_cells:
            if i in seen_col or j not in point_rows:
                return False
            seen_col.append(i)
        return True

    def minimum_size_of_object(self) -> int:
        """Or a lower bound."""
        if self.is_empty():
            return 0
        i = 0
        while True:
            for _ in self.objects_of_size(i):
                return i
            i += 1

    def objects_of_size(self, n: int, **parameters: int) -> Iterator[GriddedCayleyPerm]:
        yield from self.gridded_cayley_permutations(n)

    @classmethod
    def empty_tiling(cls) -> "Tiling":
        """Return the tiling that is the empty set."""
        return Tiling([GriddedCayleyPerm(CayleyPermutation([]), [])], [], (0, 0))

    def copy(self) -> "Tiling":
        """Return a copy of the tiling."""
        return Tiling(self.obstructions, self.requirements, self.dimensions)

    def __repr__(self) -> str:
        return (
            f"Tiling({repr(self.obstructions)}, {repr(self.requirements)},"
            + f"{repr(self.dimensions)})"
        )

    def __str__(self) -> str:
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-locals
        if self.dimensions == (0, 0):
            return "+-+\n|\u03b5|\n+-+\n"
        crossing_string = "Crossing obstructions: \n"
        point_rows = self.point_rows

        cell_basis = defaultdict(list)
        for ob in self.obstructions:
            if ob.is_local() and len(ob) > 0:
                cell_basis[ob.positions[0]].append(ob.pattern)
            elif (
                len(ob.pattern) == 2
                and ob.positions[0][1] == ob.positions[1][1]
                and ob.positions[0][1] in point_rows
            ):
                continue
            else:
                crossing_string += str(ob) + "\n"
        basis_key: dict[tuple[CayleyPermutation, ...], int] = {}
        cell_key: dict[tuple[int, int], str] = {}
        for cell, basis in cell_basis.items():
            if tuple(basis) not in basis_key:
                if all(
                    p in basis
                    for p in [
                        CayleyPermutation([0, 0]),
                        CayleyPermutation([0, 1]),
                        CayleyPermutation([1, 0]),
                    ]
                ):
                    if cell in self.positive_cells():
                        cell_key[cell] = "\u25cf"
                    else:
                        cell_key[cell] = "\u25cb"
                    continue
                if CayleyPermutation([0]) in basis:
                    cell_key[cell] = "#"
                    continue
                basis_key[tuple(basis)] = len(basis_key)
            cell_key[cell] = str(basis_key[tuple(basis)])

        requirements_string = ""
        for i, req_list in enumerate(self.requirements):
            requirements_string += f"Requirements {i}: \n"
            for req in req_list:
                requirements_string += f"{req} \n"

        n, m = self.dimensions
        edge_row = "-".join("+" for _ in range(n + 1)) + "\n"
        fill_row = " ".join("|" for _ in range(n + 1)) + "\n"
        grid = fill_row.join(edge_row for _ in range(m + 1))
        fill_rows = [copy(fill_row) for _ in range(m)]
        for cell, key in cell_key.items():
            i, j = cell
            fill_rows[j] = fill_rows[j][: i * 2 + 1] + key + fill_rows[j][i * 2 + 2 :]

        for pr in point_rows:
            fill_rows[pr] = fill_rows[pr][:-1] + "*\n"

        grid = edge_row + edge_row.join(reversed(fill_rows)) + edge_row

        key_string = "Key: \n"
        for patts, label in basis_key.items():
            basis_string = f"Av({','.join(str(p) for p in patts)})"
            key_string += f"{label}: {basis_string} \n"

        return grid + key_string + crossing_string + requirements_string

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tiling):
            return NotImplemented
        return (
            self.obstructions == other.obstructions
            and self.requirements == other.requirements
            and self.dimensions == other.dimensions
        )

    def __hash__(self) -> int:
        return hash((self.obstructions, self.requirements, self.dimensions))

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Tiling):
            return NotImplemented
        return self.dimensions < other.dimensions or (
            self.dimensions == other.dimensions
            and len(self.obstructions) < len(other.obstructions)
        )

    def __leq__(self, other: object) -> bool:
        if not isinstance(other, Tiling):
            return NotImplemented
        return self < other or self == other
