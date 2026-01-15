"""The class for point unplacement"""

from itertools import product
from typing import Iterable

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

    def cell_in_valid_region(self) -> bool:
        """Makes sure we're not unplacing a boundary point."""
        if (
            0 in self.cell
            or self.tiling.dimensions[0] - 1 == self.cell[0]
            or self.tiling.dimensions[1] - 1 == self.cell[1]
        ):
            return False
        return True

    def point_can_be_unplaced(
        self, check_reqs: tuple[tuple[GriddedCayleyPerm, ...], ...]
    ) -> bool:
        """Checks if the point can be unplaced
        doesn't fully check fusability across the point row"""
        new_tiling = self.tiling
        if not self.cell_in_valid_region():
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
        intersecting_list = self.intersecting_req_list()
        if intersecting_list:
            new_tiling = self.tiling.remove_requirements(intersecting_list[0])
            adjusted_list = self.adjust_reqs(intersecting_list[0])
        else:
            adjusted_list = [
                GriddedCayleyPerm(
                    CayleyPermutation((0,)), [(self.cell[0] - 1, self.cell[1] - 1)]
                )
            ]
        new_tiling = new_tiling.delete_rows_and_columns(
            (self.cell[0], self.cell[0] + 1), (self.cell[1], self.cell[1] + 1)
        )
        new_tiling = new_tiling.add_requirement_list(adjusted_list)
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
            new_pattern = [value_map[i] for i in req.pattern]
            new_pattern.insert(h_cuttoff, v_cuttoff)
            new_positions = list(req.positions)
            new_positions.insert(h_cuttoff, self.cell)
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
        new_tiling = tiling
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
        base_tiling = Tiling(row_obs, row_reqs, new_tiling.dimensions)
        reduced_tiling = new_tiling.delete_rows_and_columns(
            [self.cell[0], self.cell[0] + 1], [self.cell[1], self.cell[1] + 1]
        )
        col_map, row_map = {}, {}
        for i in range(tiling.dimensions[0]):
            col_map[i] = self.cell_correction((i, 0))[0]
        for j in range(tiling.dimensions[1]):
            row_map[j] = self.cell_correction((0, j))[1]
        backmap = RowColMap(col_map, row_map)
        base_tiling = base_tiling.add_obstructions(
            backmap.preimage_of_obstructions(reduced_tiling.obstructions)
        )
        base_tiling = base_tiling.add_requirements(
            backmap.preimage_of_requirements(reduced_tiling.requirements)
        )
        return base_tiling.delete_columns([self.cell[0]]) == tiling.delete_columns(
            [self.cell[0]]
        )


class PartialUnplacement:
    """Methods for partial unplacement points.
    PartialUnplacement.auto_unplace"""

    def __init__(self, tiling: Tiling):
        self.tiling = tiling
        self.points = tiling.point_cells()

    def auto_unplace(self) -> Tiling:
        """Does all valid unplacements for the tiling's point cells"""
        return self.unplace(*self.valid_cols_and_rows(self.points))

    def unplace(self, unplace_cols: set[int], unplace_rows: set[int]) -> Tiling:
        """Partially unplaces at all selected cols and rows"""
        cols_to_remove, rows_to_remove = set[int](), set[int]()
        for col in unplace_cols:
            cols_to_remove.update({col, col + 1})
        for row in unplace_rows:
            rows_to_remove.update({row, row + 1})
        temp_tiling = Tiling(
            self.tiling.obstructions, [], self.tiling.dimensions
        ).delete_rows_and_columns(cols_to_remove, rows_to_remove)

        points = self.points
        adjust = self.adjustment_map(unplace_cols, unplace_rows)
        obs = set(temp_tiling.obstructions)
        for col, row in points:
            if row in unplace_rows and col not in unplace_cols:
                obs.remove(
                    adjust.map_gridded_cperm(GriddedCayleyPerm((0,), ((col, row),)))
                )
                obs.update(
                    set(
                        adjust.map_gridded_cperms(
                            (
                                GriddedCayleyPerm((0, 0), ((col, row), (col, row))),
                                GriddedCayleyPerm((0, 1), ((col, row), (col, row))),
                                GriddedCayleyPerm((1, 0), ((col, row), (col, row))),
                            )
                        )
                    )
                )
        return Tiling(obs, [], temp_tiling.dimensions).add_requirement_list(
            self.new_reqs(unplace_cols, unplace_rows)
        )

    def valid_cols_and_rows(self, points: Iterable[Cell]) -> tuple[set[int], set[int]]:
        """Returns the set of cols that can be unplaced and the set of rows that can be unplaced"""
        valid_points = {cell for cell in points if self.cell_in_valid_region(cell)}
        return self.fusable_check(valid_points)

    def cell_in_valid_region(self, cell: Cell) -> bool:
        """Makes sure we're not unplacing a boundary point."""
        if (
            0 in cell
            or self.tiling.dimensions[0] - 1 == cell[0]
            or self.tiling.dimensions[1] - 1 == cell[1]
        ):
            return False
        return True

    def fusable_check(self, points: Iterable[Cell]) -> tuple[set[int], set[int]]:
        """Returns a set of cols that can be fused and the set of rows that can be fused"""
        temp_tiling = Tiling(
            self.tiling.obstructions, [], self.tiling.dimensions
        ).add_obstructions({GriddedCayleyPerm((0,), [point]) for point in points})
        check = tuple(map(set[int], zip(*points)))
        final_cols, final_rows = set[int](), set[int]()
        # Check row fusability
        for row in check[1]:
            obs = {
                ob
                for ob in temp_tiling.obstructions
                if all((pos[1] == row for pos in ob.positions))
            }
            reduced_tiling = temp_tiling.delete_rows_and_columns([], [row, row + 1])
            backmap = self.adjustment_map(set[int](), {row})
            check_tiling = Tiling([], [], temp_tiling.dimensions).add_obstructions(
                obs | set(backmap.preimage_of_obstructions(reduced_tiling.obstructions))
            )
            if check_tiling == temp_tiling:
                final_rows.add(row)
        # Check col fusability
        for col in check[0]:
            obs = {
                ob
                for ob in temp_tiling.obstructions
                if all((pos[0] == col for pos in ob.positions))
            }
            reduced_tiling = temp_tiling.delete_rows_and_columns([col, col + 1], [])
            backmap = self.adjustment_map({col}, set[int]())
            check_tiling = Tiling([], [], temp_tiling.dimensions).add_obstructions(
                obs | set(backmap.preimage_of_obstructions(reduced_tiling.obstructions))
            )
            if check_tiling == temp_tiling:
                final_cols.add(col)
        return final_cols, final_rows

    def adjustment_map(
        self, unplaced_cols: set[int], unplaced_rows: set[int]
    ) -> RowColMap:
        """Returns a RowColMap that tracks unplacement"""
        col_correction = dict[int, int]()
        col_adjust = 0
        for col in range(self.tiling.dimensions[0]):
            if {col, col - 1} & unplaced_cols:
                col_correction[col] = col_correction[col - 1]
                col_adjust += 1
            else:
                col_correction[col] = col - col_adjust
        row_correction = dict[int, int]()
        row_adjust = 0
        for row in range(self.tiling.dimensions[1]):
            if {row, row - 1} & unplaced_rows:
                row_correction[row] = row_correction[row - 1]
                row_adjust += 1
            else:
                row_correction[row] = row - row_adjust
        return RowColMap(col_correction, row_correction)

    def new_reqs(
        self, unplaced_cols: set[int], unplaced_rows: set[int]
    ) -> tuple[GriddedCayleyPerm, ...]:
        """Yields minimal GCPS with their positions adjusted according to unplaced cols and rows"""
        adjust = self.adjustment_map(unplaced_cols, unplaced_rows)
        return adjust.map_gridded_cperms(self.tiling.minimal_gridded_cperms())
