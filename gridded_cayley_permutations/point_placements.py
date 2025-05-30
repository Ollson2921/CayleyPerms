"""
This module contains the PointPlacement class and its subclasses,
which includes methods for placing point of a tiling and adding
obstructions and requirements to make the placements unique.
"""

from itertools import combinations

from cayley_permutations import CayleyPermutation

from .gridded_cayley_perms import GriddedCayleyPerm
from .row_col_map import OBSTRUCTIONS, REQUIREMENTS, RowColMap
from .tilings import Tiling

DIR_RIGHT = 0
DIR_RIGHT_TOP = 1
DIR_LEFT_TOP = 2
DIR_LEFT = 3
DIR_LEFT_BOT = 4
DIR_RIGHT_BOT = 5

Directions = [
    DIR_RIGHT,
    DIR_RIGHT_TOP,
    DIR_LEFT_TOP,
    DIR_LEFT,
    DIR_LEFT_BOT,
    DIR_RIGHT_BOT,
]


class MultiplexMap(RowColMap):
    """
        A special class for mapping a point onto its own row and column
        + - + - + - +
        | A | A | A | \
        + - + - + - +    + - +
        | A | o | A | -  | A |
        + - + - + - +    + - +
        | A | A | A | /
        + - + - + - +
        It expands a cell to a three by three grid.
        """

    def __init__(self, cell: tuple[int, int], dimensions: tuple[int, int]):
        """Cell is the cell that is expanded to a three by three grid
        and dimensions are the dimenstions of the grid before it was expanded."""
        self.cell = cell
        self.dimensions = dimensions
        super().__init__(self._col_map(), self._row_map())

    def _row_map(self) -> dict[int, int]:
        """Return the row map."""
        row_width = self.dimensions[1] + 2
        row_map_dict = {}
        for i in range(row_width):
            if i < self.cell[1]:
                row_map_dict[i] = i
            elif self.cell[1] <= i <= self.cell[1] + 2:
                row_map_dict[i] = self.cell[1]
            else:
                row_map_dict[i] = i - 2
        return row_map_dict

    def _col_map(self) -> dict[int, int]:
        """Return the col map."""
        col_width = self.dimensions[0] + 2
        col_map_dict = {}
        for i in range(col_width):
            if i < self.cell[0]:
                col_map_dict[i] = i
            elif self.cell[0] <= i <= self.cell[0] + 2:
                col_map_dict[i] = self.cell[0]
            else:
                col_map_dict[i] = i - 2
        return col_map_dict


class PartialMultiplexMap(MultiplexMap):
    """A map for mapping a point on to its own column
    + - + - + - +    + - +
    | A | o | A | -  | A |
    + - + - + - +    + - +
    It expands a cell to a one by three grid.
    """

    def _row_map(self) -> dict[int, int]:
        """Return the row map."""
        return {i: i for i in range(self.dimensions[1])}


class PointPlacement:
    """
    A class for placing points in a tiling
            + - + - + - +
            | A |   | A |
    + - +   + - + - + - +
    | A | = | A | o | A |
    + - +   + - + - + - +
            | A |   | A |
            + - + - + - +
    Obstruction and requirements are added to ensure that a unique
    point is placed onto its own row and column. Additional
    obstructions are added to ensure that the middle row
    contains only one value.
    """

    DIRECTIONS = [
        DIR_RIGHT,
        DIR_RIGHT_TOP,
        DIR_LEFT_TOP,
        DIR_LEFT,
        DIR_LEFT_BOT,
        DIR_RIGHT_BOT,
    ]

    def __init__(self, tiling: Tiling) -> None:
        self.tiling = tiling

    def point_obstructions_and_requirements(
        self, cell: tuple[int, int]
    ) -> tuple[OBSTRUCTIONS, REQUIREMENTS]:
        """
        The obstructions and requirements needed to ensure that the middle cell is a point on
        its own row and columns, and that the middle row contains only one value.
        """
        cell = self.placed_cell(cell)
        x, y = self.new_dimensions()
        col_obs = [
            GriddedCayleyPerm(CayleyPermutation([0]), [(cell[0], i)])
            for i in range(y)
            if i != cell[1]
        ]
        row_obs: list[GriddedCayleyPerm] = []
        row = cell[1]
        for col in range(x):
            row_obs.append(
                GriddedCayleyPerm(CayleyPermutation([0, 1]), [(col, row), (col, row)])
            )
            row_obs.append(
                GriddedCayleyPerm(CayleyPermutation([1, 0]), [(col, row), (col, row)])
            )
        for col1, col2 in combinations(range(x), 2):
            row_obs.append(
                GriddedCayleyPerm(CayleyPermutation([0, 1]), [(col1, row), (col2, row)])
            )
            row_obs.append(
                GriddedCayleyPerm(CayleyPermutation([1, 0]), [(col1, row), (col2, row)])
            )

        return (
            (
                GriddedCayleyPerm(CayleyPermutation((0, 1)), [cell, cell]),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), [cell, cell]),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), [cell, cell]),
            )
            + tuple(col_obs)
            + tuple(row_obs),
            ((GriddedCayleyPerm(CayleyPermutation([0]), [cell]),),),
        )

    def placed_cell(self, cell: tuple[int, int]) -> tuple[int, int]:
        """Return the cell that has the placed point."""
        return (cell[0] + 1, cell[1] + 1)

    def multiplex_map(self, cell: tuple[int, int]) -> MultiplexMap:
        """Return the multiplex map for the given cell."""
        return MultiplexMap(cell, self.tiling.dimensions)

    def forced_obstructions(
        self,
        cell: tuple[int, int],
        requirement_list: tuple[GriddedCayleyPerm, ...],
        indices: tuple[int, ...],
        direction: int,
    ) -> OBSTRUCTIONS:
        """
        Return the obstructions that are needed to ensure that the placed point is unique.
        This is the point which is farthest in the given direction at the given indices.
        """
        multiplex_map = self.multiplex_map(cell)
        cell = self.placed_cell(cell)
        obstructions = []
        for idx, gcp in zip(indices, requirement_list):
            for stretched_gcp in multiplex_map.preimage_of_gridded_cperm(gcp):
                if self.farther(stretched_gcp.positions[idx], cell, direction):
                    obstructions.append(stretched_gcp)
        return tuple(obstructions)

    @staticmethod
    def farther(cell1: tuple[int, int], cell2: tuple[int, int], direction: int) -> bool:
        """Return True if cell1 is farther in the given direction than cell2."""
        if direction == DIR_RIGHT:
            return cell1[0] > cell2[0]
        if direction == DIR_RIGHT_TOP:
            return cell1[1] > cell2[1] or (cell1[1] == cell2[1] and cell1[0] > cell2[0])
        if direction == DIR_LEFT_TOP:
            return cell1[1] > cell2[1] or (cell1[1] == cell2[1] and cell1[0] < cell2[0])
        if direction == DIR_LEFT:
            return cell1[0] < cell2[0]
        if direction == DIR_LEFT_BOT:
            return cell1[1] < cell2[1] or (cell1[1] == cell2[1] and cell1[0] < cell2[0])
        if direction == DIR_RIGHT_BOT:
            return cell1[1] < cell2[1] or (cell1[1] == cell2[1] and cell1[0] > cell2[0])
        raise ValueError(f"Direction {direction} is not valid.")

    def point_placement(
        self,
        requirement_list: tuple[GriddedCayleyPerm, ...],
        indices: tuple[int, ...],
        direction: int,
    ) -> tuple[Tiling, ...]:
        """
        Return the tilings that are obtained by placing the points of the gridded permutations
        in requirement_list in the given direction."""
        if direction not in self.DIRECTIONS:
            raise ValueError(f"Direction {direction} is not a valid direction.")
        cells = []
        for idx, gcp in zip(indices, requirement_list):
            cells.append(gcp.positions[idx])
        cells = sorted(set(cells))
        return tuple(
            self.point_placement_in_cell(requirement_list, indices, direction, cell)
            for cell in cells
        )

    def point_placement_in_cell(
        self,
        requirement_list: tuple[GriddedCayleyPerm, ...],
        indices: tuple[int, ...],
        direction: int,
        cell: tuple[int, int],
    ) -> Tiling:
        """
        Return the tiling which has placed the point in cell with respect to the given
        requirement_list and indices.
        """
        multiplex_map = self.multiplex_map(cell)
        multiplex_obs, multiplex_reqs = multiplex_map.preimage_of_tiling(self.tiling)
        point_obs, point_reqs = self.point_obstructions_and_requirements(cell)
        forced_obs = self.forced_obstructions(
            cell, requirement_list, indices, direction
        )
        obstructions = multiplex_obs + point_obs + forced_obs
        requirements = multiplex_reqs + point_reqs
        return Tiling(obstructions, requirements, self.new_dimensions())

    def new_dimensions(self) -> tuple[int, int]:
        """The dimensions of a placed tiling."""
        return (
            self.tiling.dimensions[0] + 2,
            self.tiling.dimensions[1] + 2,
        )

    def directionless_point_placement(self, cell: tuple[int, int]) -> Tiling:
        """
        Return the tiling obtained by placing the point in the given cell.
        As this is directionless, the placed point is not necessarily unique.
        """
        multiplex_map = self.multiplex_map(cell)
        multiplex_obs, multiplex_reqs = multiplex_map.preimage_of_tiling(self.tiling)
        point_obs, point_reqs = self.point_obstructions_and_requirements(cell)
        obstructions = multiplex_obs + point_obs
        requirements = multiplex_reqs + point_reqs
        return Tiling(
            obstructions,
            requirements,
            self.new_dimensions(),
        )


class PartialPointPlacements(PointPlacement):
    """
    A class for partially placing points in a tiling
    + - +   + - + - + - +
    | A | = | A | o | A |
    + - +   + - + - + - +
    Obstruction and requirements are added to ensure that a unique
    point is placed onto its own column.
    """

    DIRECTIONS = [DIR_LEFT, DIR_RIGHT]

    def point_obstructions_and_requirements(
        self, cell: tuple[int, int]
    ) -> tuple[OBSTRUCTIONS, REQUIREMENTS]:
        cell = self.placed_cell(cell)
        _, y = self.new_dimensions()
        col_obs = tuple(
            GriddedCayleyPerm(CayleyPermutation([0]), [(cell[0], i)])
            for i in range(y)
            if i != cell[1]
        )
        return (
            (
                GriddedCayleyPerm(CayleyPermutation((0, 1)), [cell, cell]),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), [cell, cell]),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), [cell, cell]),
            )
            + col_obs,
            ((GriddedCayleyPerm(CayleyPermutation([0]), [cell]),),),
        )

    def placed_cell(self, cell: tuple[int, int]) -> tuple[int, int]:
        return (cell[0] + 1, cell[1])

    def multiplex_map(self, cell: tuple[int, int]) -> MultiplexMap:
        return PartialMultiplexMap(cell, self.tiling.dimensions)

    def new_dimensions(self):
        return (self.tiling.dimensions[0] + 2, self.tiling.dimensions[1])
