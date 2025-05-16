from itertools import product
from typing import Iterable

from cayley_permutations import CayleyPermutation

from .gridded_cayley_perms import GriddedCayleyPerm
from .row_col_map import OBSTRUCTIONS, REQUIREMENTS, RowColMap
from .tilings import Tiling

Cell = tuple[int, int]


class PointUnplacement:
    def __init__(self, tiling: Tiling, cell: Cell):
        self.tiling = tiling
        self.cell = cell
        self.surrounding_cells = set(
            product((cell[0] - 1, cell[0] + 1), (cell[1] - 1, cell[1], cell[1] + 1))
        )

    def intersecting_req_list(self) -> tuple[tuple[GriddedCayleyPerm, ...], ...]:
        """Identifies a valid req list that can be merged with the point to be unplaced"""
        found_lists = tuple[tuple[GriddedCayleyPerm, ...], ...]()
        for req_list in self.tiling.requirements:
            reqs_intersect = (
                bool(set(req.positions).intersection(self.surrounding_cells))
                for req in req_list
            )
            if any(reqs_intersect):
                found_lists = found_lists + (req_list,)
        return found_lists

    def point_can_be_unplaced(
        self, check_reqs: tuple[tuple[GriddedCayleyPerm, ...], ...]
    ) -> bool:
        """Checks if the point can be unplaced"""
        new_tiling = self.tiling
        if check_reqs:
            if len(check_reqs) > 1:
                return False
            if not all(
                bool(set(req.positions).intersection(self.surrounding_cells))
                for req in check_reqs[0]
            ):
                return False
            new_tiling = self.tiling.remove_requirements(check_reqs[0])
        if (
            0 in self.cell
            or self.tiling.dimensions[0] == self.cell[0]
            or self.tiling.dimensions[1] == self.cell[1]
        ):
            return False
        new_tiling = new_tiling.delete_rows_and_columns((self.cell[0],), (self.cell[1],))
        if not new_tiling.is_fusable(0, self.cell[0] - 1):
            return False
        if not new_tiling.is_fusable(1, self.cell[1] - 1):
            return False
        return True

    def unplace_point(self) -> Tiling:
        """Tries to unplace a point in cell"""
        new_tiling = self.tiling
        intersecting_list = self.intersecting_req_list()[0]
        if intersecting_list:
            new_tiling = self.tiling.remove_requirements(intersecting_list)
        new_tiling = new_tiling.delete_rows_and_columns((self.cell[0],self.cell[0] +1), (self.cell[1],self.cell[1] +1))
        return new_tiling

