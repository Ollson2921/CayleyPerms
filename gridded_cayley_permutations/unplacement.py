"""The class for point unplacement"""

from itertools import product

from cayley_permutations import CayleyPermutation

from .gridded_cayley_perms import GriddedCayleyPerm
from .row_col_map import RowColMap
from .tilings import Tiling

Cell = tuple[int, int]


class PointUnplacement:
    """Methods for unplacing points"""

    def __init__(self, tiling: Tiling, cell: Cell):
        assert cell in tiling.point_cells()
        self.tiling = tiling
        self.cell = cell
        self.surrounding_cells = set(
            product((cell[0] - 1, cell[0] + 1), (cell[1] - 1, cell[1], cell[1] + 1))
        )

    def intersecting_req_list(self) -> tuple[tuple[GriddedCayleyPerm, ...], ...]:
        """Identifies a valid req list that can be merged with the point to be unplaced"""
        found_lists: tuple[tuple[GriddedCayleyPerm, ...], ...] = tuple()
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
        """Checks if the point can be unplaced
        doesn't fully check fusability across the point row"""
        new_tiling = self.tiling
        if (
            0 in self.cell
            or self.tiling.dimensions[0] == self.cell[0]
            or self.tiling.dimensions[1] == self.cell[1]
        ):
            return False
        if check_reqs:
            if len(check_reqs) > 1:
                return False
            if not all(
                bool(set(req.positions).intersection(self.surrounding_cells))
                for req in check_reqs[0]
            ):
                return False
            new_tiling = self.tiling.remove_requirements(check_reqs[0])
        return self.check_fusability(new_tiling)

    def unplace_point(self) -> Tiling:
        """Tries to unplace a point in cell"""
        new_tiling = self.tiling
        intersecting_list = self.intersecting_req_list()[0]
        if intersecting_list:
            new_tiling = self.tiling.remove_requirements(intersecting_list)
            adjusted_list = self.adjust_reqs(intersecting_list)
        else:
            adjusted_list = [
                GriddedCayleyPerm(
                    CayleyPermutation((0,)), [(self.cell[0] - 1, self.cell[1] - 1)]
                )
            ]
        new_tiling = new_tiling.delete_rows_and_columns(
            (self.cell[0], self.cell[0] + 1), (self.cell[1], self.cell[1] + 1)
        )
        new_tiling.add_requirement_list(adjusted_list)
        return new_tiling

    def adjust_reqs(self, req_list: tuple[GriddedCayleyPerm, ...]):
        """Adds the point to"""
        new_req_list = list[GriddedCayleyPerm]()
        for req in req_list:
            values = {req.pattern[i]: req.positions[i][1] for i in range(len(req))}
            value_map = {
                value: value + int(values[value] > self.cell[1]) for value in values
            }
            h_cuttoff = sum(cell[0] < self.cell[0] for cell in req.positions)
            v_cuttoff = sum(value < self.cell[1] for value in values.values())
            new_pattern, new_positions = list(req.pattern), list(req.positions)
            new_pattern.insert(h_cuttoff, v_cuttoff)
            new_positions.insert(h_cuttoff, self.cell)
            new_pattern = [value_map[i] for i in new_pattern]
            new_positions = list(map(self.cell_correction, new_positions))
            new_req_list.append(
                GriddedCayleyPerm(CayleyPermutation(new_pattern), new_positions)
            )
        return new_req_list

    def cell_correction(self, cell: Cell) -> Cell:
        """Finds where a cell would map to after the unplacement"""
        x = cell[0] - int(cell[0] >= self.cell[0]) - int(cell[0] > self.cell[0])
        y = cell[1] - int(cell[1] >= self.cell[1]) - int(cell[1] > self.cell[1])
        return (x, y)

    def check_fusability(self, tiling: Tiling) -> bool:
        """Checks if tiling is fusable for point unplacement.
        This is done after intersecting requirements have been removed."""
        new_tiling = tiling.delete_columns([self.cell[0]])
        row_cells = new_tiling.cells_in_row(self.cell[1])
        row_obs = [
            ob
            for ob in new_tiling.obstructions
            if all(pos in row_cells for pos in ob.positions)
        ]
        row_reqs = []
        for req_list in new_tiling.requirements:
            new_req_list = [
                req
                for req in req_list
                if all(pos in row_cells for pos in req.positions)
            ]
            if new_req_list:
                row_reqs.append(new_req_list)
        base_tiling = Tiling(row_obs, row_reqs, tiling.dimensions)
        reduced_tiling = new_tiling.delete_rows_and_columns(
            [self.cell[0]], [self.cell[1], self.cell[1] + 1]
        )
        col_map, row_map = {}, {}
        for i in range(tiling.dimensions[0]):
            col_map[i] = self.cell_correction((i, 0))[0]
        for j in range(tiling.dimensions[1]):
            row_map[i] = self.cell_correction((0, j))[1]
        backmap = RowColMap(col_map, row_map)
        base_tiling = base_tiling.add_obstructions(
            backmap.preimage_of_obstructions(reduced_tiling.obstructions)
        )
        base_tiling = base_tiling.add_requirements(
            backmap.preimage_of_requirements(reduced_tiling.requirements)
        )
        return base_tiling == tiling
