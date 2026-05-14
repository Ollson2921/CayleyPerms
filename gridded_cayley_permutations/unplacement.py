"""The class for point unplacement"""

from itertools import product, chain
from typing import Iterable, Callable
from functools import cached_property
from collections import defaultdict

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
        self.dimensions = tiling.dimensions
        try:
            self.positive_cols, self.positive_rows = map(
                set[int], zip(*tiling.positive_cells())
            )
        except ValueError:
            self.positive_cols, self.positive_rows = set[int](), set[int]()
        self.point_cols = tiling.point_cols
        self.point_rows = tiling.point_rows
        self.obs_by_direction = tiling.obs_by_col_and_row()

    @cached_property
    def restricted_obs_by_direction(
        self,
    ) -> tuple[dict[int, set[GriddedCayleyPerm]], dict[int, set[GriddedCayleyPerm]]]:
        """Restricts obs by direction so that each key contains only obs fully contained
        in that row or col."""
        by_col = defaultdict[int, set[GriddedCayleyPerm]](set)
        by_row = defaultdict[int, set[GriddedCayleyPerm]](set)

        def col_filter(col: int) -> Callable[[GriddedCayleyPerm], bool]:
            def wrapper(gcp: GriddedCayleyPerm) -> bool:
                return all(pos[0] == col for pos in gcp.positions)

            return wrapper

        def row_filter(row: int) -> Callable[[GriddedCayleyPerm], bool]:
            def wrapper(gcp: GriddedCayleyPerm) -> bool:
                return all(pos[1] == row for pos in gcp.positions)

            return wrapper

        for col in self.point_cols:
            by_col[col] = set(filter(col_filter(col), self.obs_by_direction[0][col]))
        for row in self.point_rows:
            by_row[row] = set(filter(row_filter(row), self.obs_by_direction[1][row]))

        return by_col, by_row

    @cached_property
    def all_point_col_obs(self) -> set[GriddedCayleyPerm]:
        """Returns point obstructions in point cols"""
        return set(chain.from_iterable(self.restricted_obs_by_direction[0].values()))

    @cached_property
    def expected_obs(self) -> set[GriddedCayleyPerm]:
        """Returns the set of all gcps implied by point rows/cols"""
        from_point_rows = set(
            chain.from_iterable(
                Tiling([], [], self.dimensions).add_point_row(row).obstructions
                for row in self.point_rows
            )
        )
        return from_point_rows | self.all_point_col_obs

    def find_cols_and_rows(self) -> tuple[set[int], set[int]]:
        """Uses the initialiser to find all valid rows and cols to unfuse"""
        return self.check_cols_and_rows(self.point_cols, self.point_rows)

    def check_cols_and_rows(
        self, check_cols: set[int], check_rows: set[int]
    ) -> tuple[set[int], set[int]]:
        """Filters the input cols and rows to only include those which can be unplaced."""
        # First, we make sure we're not on the border
        valid_cols = {
            col
            for col in check_cols & self.positive_cols
            if (0 < col < self.dimensions[0] - 1)
        }
        valid_rows = {
            row
            for row in check_rows & self.positive_rows
            if (0 < row < self.dimensions[1] - 1)
        }

        # This makes sure every point row ob can be unplaced
        valid_rows = set(filter(self.row_ob_check, valid_rows))

        # Now we check that the fusion/unfusion is valid
        valid_cols = set(filter(self.col_fuse_check, valid_cols))
        valid_rows = set(filter(self.row_fuse_check, valid_rows))

        return valid_cols, valid_rows

    def col_fuse_check(self, col: int) -> bool:
        """Returns True if col can be unplaced"""
        maps = self.default_maps()
        maps[0][col] = col - 1
        maps[0][col + 1] = col - 1
        unfusion_map = RowColMap(*maps)

        # left_obs are the obs in the col to the left of the point
        left_obs = self.obs_by_direction[0][col - 1]

        # Get the original obs to compare against fusion/unfusion
        old_obs = (
            left_obs | self.obs_by_direction[0][col] | self.obs_by_direction[0][col + 1]
        )

        # Unfuse the obs in the left col, then add in obs we expect in a point col
        new_obs = set[GriddedCayleyPerm](
            unfusion_map.preimage_of_obstructions(left_obs)
        )
        center_obs = self.restricted_obs_by_direction[0][col]
        new_obs.update(center_obs)

        # Simplify new obs to get rid of redundant obstructions, then compare
        old_tiling = Tiling(old_obs, [], self.dimensions)
        new_tiling = Tiling(new_obs, [], self.dimensions)
        return old_tiling == new_tiling

    def row_ob_check(self, row: int) -> bool:
        """Returns False if there is an obstruction that can't be unplaced"""
        positive_cells = (
            cell for cell in self.tiling.positive_cells() if cell[1] == row
        )
        for ob in self.obs_by_direction[1][row] - self.expected_obs:
            if any(ob.positions.count(cell) > 1 for cell in positive_cells):
                return False
        return True

    def row_fuse_check(self, row: int) -> bool:
        """Returns True if row can be unplaced."""
        maps = self.default_maps()
        maps[1][row] = row - 1
        maps[1][row + 1] = row - 1
        unfusion_map = RowColMap(*maps)

        lower_obs = self.obs_by_direction[1][row - 1]

        old_obs = (
            lower_obs
            | self.obs_by_direction[1][row]
            | self.obs_by_direction[1][row + 1]
        )

        # Before unfusing lower_obs, remove obstructions from point cols
        recover_obs = self.all_point_col_obs & old_obs
        new_obs = set[GriddedCayleyPerm](
            unfusion_map.preimage_of_obstructions(lower_obs - recover_obs)
        )
        center_obs = self.restricted_obs_by_direction[1][row]

        # Bring back the point col obstructions
        new_obs.update(center_obs | recover_obs)

        old_tiling = Tiling(old_obs, [], self.dimensions)
        new_tiling = Tiling(new_obs, [], self.dimensions)
        return old_tiling == new_tiling

    def default_maps(self) -> list[dict[int, int]]:
        """Basic identity maps for convenience"""
        col_map = dict(enumerate(range(self.dimensions[0])))
        row_map = dict(enumerate(range(self.dimensions[1])))
        return [col_map, row_map]

    def pre_adjust_obs(
        self, unplaced_rows: Iterable[int]
    ) -> tuple[set[GriddedCayleyPerm], set[GriddedCayleyPerm]]:
        """Adds neccecary 00... obstructions and shifts point cols as needed"""
        add_obs, remove_obs = set[GriddedCayleyPerm](), set[GriddedCayleyPerm]()
        for row in unplaced_rows:
            points = self.tiling.positive_cells() & self.tiling.cells_in_row(row)
            abnormal_cells = tuple(
                ob.positions
                for ob in self.restricted_obs_by_direction[1][row] - self.expected_obs
            )
            for point in points:
                shift_cell = (point[0], point[1] - 1)
                if point[0] in self.point_cols:
                    remove_obs.add(GriddedCayleyPerm((0,), (shift_cell,)))
                    add_obs.update(
                        {
                            GriddedCayleyPerm((0, 0), (shift_cell, shift_cell)),
                            GriddedCayleyPerm((0, 1), (shift_cell, shift_cell)),
                            GriddedCayleyPerm((1, 0), (shift_cell, shift_cell)),
                        }
                    )
                for grouping in abnormal_cells:
                    positions = sorted(grouping + (point,))
                    positions = [(cell[0], cell[1] - 1) for cell in positions]
                    add_obs.add(GriddedCayleyPerm((0,) * len(positions), positions))
        return add_obs, remove_obs

    def auto_unplace(self) -> Tiling:
        """Does all valid unplacements for the tiling's point cells"""
        temp = self.unplace(set(), self.find_cols_and_rows()[1])
        new_algo = PartialUnplacement(temp)
        return new_algo.unplace(new_algo.find_cols_and_rows()[0], set())

    def unplace(self, unplace_cols: set[int], unplace_rows: set[int]) -> Tiling:
        """Partially unplaces at all selected cols and rows"""

        if not any((unplace_cols, unplace_rows)):
            return self.tiling

        cols_to_remove, rows_to_remove = set[int](), set[int]()

        # pre_adjust_obs makes sure our reqs don't end up on point obs
        add_obs, remove_obs = self.pre_adjust_obs(unplace_rows)

        updated_obs = (set(self.tiling.obstructions) | set(add_obs)) - set(remove_obs)

        # Make the req free tiling to prepare for fusion
        temp_tiling = Tiling(updated_obs, [], self.dimensions)

        for col in unplace_cols:
            cols_to_remove.update({col, col + 1})
        for row in unplace_rows:
            rows_to_remove.update({row, row + 1})
        temp_tiling = temp_tiling.delete_rows_and_columns(
            cols_to_remove, rows_to_remove
        )

        # Bring the reqs back
        return temp_tiling.add_requirement_list(
            self.new_reqs(unplace_cols, unplace_rows)
        )

    def adjustment_map(
        self, unplaced_cols: set[int], unplaced_rows: set[int]
    ) -> RowColMap:
        """Returns a RowColMap that tracks unplacement"""
        col_correction = dict[int, int]()
        col_adjust = 0
        for col in range(self.dimensions[0]):
            if {col, col - 1} & unplaced_cols:
                col_correction[col] = col_correction[col - 1]
                col_adjust += 1
            else:
                col_correction[col] = col - col_adjust
        row_correction = dict[int, int]()
        row_adjust = 0
        for row in range(self.dimensions[1]):
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
