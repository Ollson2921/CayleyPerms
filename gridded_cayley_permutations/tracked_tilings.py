from typing import Iterable, Iterator
from functools import cached_property
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from comb_spec_searcher.strategies.strategy import StrategyDoesNotApply
from gridded_cayley_permutations.row_col_map import RowColMap
from tilescope.strategies import (
    FactorStrategy,
    RequirementPlacementStrategy,
    LessThanRowColSeparationStrategy,
    LessThanOrEqualRowColSeparationStrategy,
    CellInsertionFactory,
    PointPlacementFactory,
    RowInsertionFactory,
    ColInsertionFactory,
    RequirementInsertionStrategy,
)
from tilescope.strategies.row_column_separation import (
    LessThanRowColSeparation,
    LessThanOrEqualRowColSeparation,
)
from gridded_cayley_permutations.factors import Factors
from gridded_cayley_permutations.point_placements import Directions, PointPlacement

from tilescope.strategies.point_placements import (
    DIR_LEFT_BOT,
    DIR_RIGHT_BOT,
    DIR_LEFT_TOP,
    DIR_RIGHT_TOP,
    DIR_LEFT,
    DIR_RIGHT,
)

Cell = tuple[int, int]


class TrackedTiling(Tiling):
    """A Tiling with clouds which keep track of areas of the tiling."""

    def __init__(
        self,
        tiling: Tiling,
        value_clouds: tuple[tuple[Cell, ...], ...] = (),
        indices_clouds: tuple[tuple[Cell, ...], ...] = (),
        simplify: bool = False,
        intersect_clouds_with_active: bool = False,
    ) -> None:
        self.tiling = tiling
        super().__init__(
            tiling.obstructions, tiling.requirements, tiling.dimensions, simplify
        )
        self.value_clouds = value_clouds
        self.indices_clouds = indices_clouds
        if intersect_clouds_with_active:
            self.value_clouds = tuple(
                tuple(cell for cell in cloud if cell in self.active_cells)
                for cloud in self.value_clouds
            )
            self.indices_clouds = tuple(
                tuple(cell for cell in cloud if cell in self.active_cells)
                for cloud in self.indices_clouds
            )

    def delete_rows_and_columns(
        self, cols: Iterable[int], rows: Iterable[int]
    ) -> "TrackedTiling":
        """Return a new tiling with the given rows and columns removed
        and updated clouds."""
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
        new_til = Tiling(
            new_obstructions, new_requirements, new_dimensions, simplify=False
        )

        def map_cell(cell: Cell) -> Cell:
            return (col_map[cell[0]], row_map[cell[1]])

        new_value_clouds = []
        for cloud in self.value_clouds:
            new_cloud = tuple(
                map_cell(cell)
                for cell in cloud
                if cell[0] not in cols
                and cell[1] not in rows
                and map_cell(cell) in new_til.active_cells
            )
            if new_cloud:
                new_value_clouds.append(new_cloud)
        new_indices_clouds = []
        for cloud in self.indices_clouds:
            new_cloud = tuple(
                map_cell(cell)
                for cell in cloud
                if cell[0] not in cols
                and cell[1] not in rows
                and map_cell(cell) in new_til.active_cells
            )
            if new_cloud:
                new_indices_clouds.append(new_cloud)
        return TrackedTiling(
            new_til,
            value_clouds=tuple(new_value_clouds),
            indices_clouds=tuple(new_indices_clouds),
        )

    def __str__(self) -> str:
        return (
            f"Tiling: \n{self.tiling}\n"
            f"Value clouds: {self.value_clouds},\n"
            f"Indices clouds: {self.indices_clouds}"
        )


class TrackedFactors(Factors):
    """Factors and tracks clouds"""

    def __init__(self, tracked_tiling: TrackedTiling) -> None:
        self.tracked_tiling = tracked_tiling
        super().__init__(tracked_tiling.tiling)

    def find_tracked_factors(self) -> Iterable[TrackedTiling]:
        """Return the factors of the tracked tiling."""
        factors = self.find_factors()
        for factor in factors:
            value_clouds = []
            indices_clouds = []
            for cloud in self.tracked_tiling.value_clouds:
                value_cloud = tuple(
                    cell for cell in cloud if cell in factor.active_cells
                )
                if value_cloud:
                    value_clouds.append(value_cloud)
            for indices_cloud in self.tracked_tiling.indices_clouds:
                indices_cloud_factor = tuple(
                    cell for cell in indices_cloud if cell in factor.active_cells
                )
                if indices_cloud_factor:
                    indices_clouds.append(indices_cloud_factor)
            yield TrackedTiling(
                factor,
                value_clouds=tuple(value_clouds),
                indices_clouds=tuple(indices_clouds),
            )


class TrackedFactorStrategy(FactorStrategy):
    """
    A strategy for finding factors in a tracked tiling.
    """

    def decomposition_function(self, comb_class: TrackedTiling) -> tuple[Tiling, ...]:
        factors = TrackedFactors(comb_class).find_tracked_factors()
        if len(factors) == 1:
            raise StrategyDoesNotApply
        return factors


# til = Tiling.create_vincular_or_bivincular("0")
# track_til = TrackedTiling(
#     til,
#     value_clouds=(((0, 0), (0, 1)),),
#     indices_clouds=(((1, 0), (1, 1)),),
#     intersect_clouds_with_active=False,
# )
# print(track_til)
# for til in TrackedFactors(track_til).find_tracked_factors():
#     print(til)


class TrackedLessThanRowColSeparation(LessThanRowColSeparation):
    """Separates rows and columns with less than constraints and tracks clouds."""

    def __init__(self, tracked_tiling: TrackedTiling) -> None:
        self.tracked_tiling = tracked_tiling
        super().__init__(tracked_tiling.tiling)

    def map_clouds(
        self, separated_tiling: Tiling
    ) -> tuple[tuple[Cell, ...], tuple[Cell, ...]]:
        """Return the clouds mapped to the separated tiling."""
        value_clouds = []
        indices_clouds = []
        for cloud in self.tracked_tiling.value_clouds:
            value_cloud = tuple(
                self.map_cell(cell)
                for cell in cloud
                if self.map_cell(cell) in separated_tiling.active_cells
            )
            if value_cloud:
                value_clouds.append(value_cloud)
        for cloud in self.tracked_tiling.indices_clouds:
            indices_cloud = tuple(
                self.map_cell(cell)
                for cell in cloud
                if self.map_cell(cell) in separated_tiling.active_cells
            )
            if indices_cloud:
                indices_clouds.append(indices_cloud)
        return tuple(value_clouds), tuple(indices_clouds)

    def tracked_row_col_separation(self) -> Iterable[TrackedTiling]:
        """Yield the separated tilings with tracked clouds."""
        for separated_tiling in self.row_col_separation():
            value_clouds, indices_clouds = self.map_clouds(separated_tiling)
            yield TrackedTiling(
                separated_tiling,
                value_clouds=tuple(value_clouds),
                indices_clouds=tuple(indices_clouds),
            )


class TrackedLessThanOrEqualRowColSeparation(
    LessThanOrEqualRowColSeparation, TrackedLessThanRowColSeparation
):
    """Separates rows and columns with less than or equal constraints and tracks clouds."""

    @cached_property
    def col_row_preimages(self) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
        """The preimages of rows and cols in the tiling."""
        row_preimages = [
            self.row_col_map.preimages_of_row(i)
            for i in range(self.tiling.dimensions[0])
        ]
        col_preimages = [
            self.row_col_map.preimages_of_col(j)
            for j in range(self.tiling.dimensions[1])
        ]
        return col_preimages, row_preimages

    def map_cells_for_clouds(self, cell: Cell) -> tuple[Cell, ...]:
        """
        Map the cell to its new positions, allowing for multiple from interleaving
        rows.
        """
        cells_mapping_to = []
        for i in self.col_row_preimages[0][cell[0]]:
            for j in self.col_row_preimages[1][cell[1]]:
                cells_mapping_to.append((i, j))
        return tuple(cells_mapping_to)

    def map_clouds(
        self, separated_tiling: Tiling
    ) -> tuple[tuple[Cell, ...], tuple[Cell, ...]]:
        """Return the clouds mapped to the separated tiling."""
        value_clouds = []
        indices_clouds = []
        for cloud in self.tracked_tiling.value_clouds:
            value_cloud = []
            for cell in cloud:
                for mapped_cell in self.map_cells_for_clouds(cell):
                    if mapped_cell in separated_tiling.active_cells:
                        value_cloud.append(mapped_cell)
            value_cloud = tuple(value_cloud)
            if value_cloud:
                value_clouds.append(value_cloud)
        for cloud in self.tracked_tiling.indices_clouds:
            indices_cloud = []
            for cell in cloud:
                for mapped_cell in self.map_cells_for_clouds(cell):
                    if mapped_cell in separated_tiling.active_cells:
                        indices_cloud.append(mapped_cell)
            indices_cloud = tuple(indices_cloud)
            if indices_cloud:
                indices_clouds.append(indices_cloud)
        return tuple(value_clouds), tuple(indices_clouds)


class TrackedLessThanRowColSeparationStrategy(LessThanRowColSeparationStrategy):
    """A strategy for separating rows and columns with less than constraints."""

    def decomposition_function(self, comb_class: Tiling) -> tuple[Tiling, ...]:
        """Return the decomposition function."""
        algo = LessThanRowColSeparation(comb_class)
        return (next(algo.row_col_separation()),)


class TrackedLessThanOrEqualRowColSeparationStrategy(
    LessThanOrEqualRowColSeparationStrategy
):
    """A strategy for separating rows and columns with less than or equal constraints."""

    def decomposition_function(self, comb_class: Tiling) -> tuple[Tiling, ...]:
        """Return the decomposition function."""
        algo = TrackedLessThanOrEqualRowColSeparation(comb_class)
        return tuple(algo.row_col_separation())


# til = Tiling(
#     [GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (0, 1)])], [], (1, 2)
# )
# track_til = TrackedTiling(
#     til,
#     value_clouds=(((0, 0), (0, 1)),),
#     indices_clouds=(((0, 0),),),
#     intersect_clouds_with_active=False,
# )
# print(track_til)

# for til in TrackedLessThanRowColSeparation(track_til).tracked_row_col_separation():
#     print(til)


# til = Tiling(
#     [GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (1, 0)])], [], (2, 1)
# )
# track_til = TrackedTiling(
#     til,
#     value_clouds=(((0, 0), (1, 0)),),
#     indices_clouds=(((0, 0),),),
#     intersect_clouds_with_active=False,
# )
# print(track_til)

# for til in TrackedLessThanOrEqualRowColSeparation(
#     track_til
# ).tracked_row_col_separation():
#     print(til)


class TrackedPointPlacement(PointPlacement):
    """Point placement tracking clouds."""

    def __init__(self, tracked_tiling: TrackedTiling) -> None:
        self.tracked_tiling = tracked_tiling
        super().__init__(tracked_tiling.tiling)

    def col_row_preimages(
        self, row_col_map
    ) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
        """The preimages of rows and cols in the tiling."""
        row_preimages = [
            row_col_map.preimages_of_row(i) for i in range(self.tiling.dimensions[0])
        ]
        col_preimages = [
            row_col_map.preimages_of_col(j) for j in range(self.tiling.dimensions[1])
        ]
        return col_preimages, row_preimages

    def map_cells_for_clouds(self, cell: Cell, map_for_cells) -> tuple[Cell, ...]:
        """
        Map the cell to its new positions, allowing for multiple from interleaving
        rows.
        """
        cells_mapping_to = []
        for i in map_for_cells[0][cell[0]]:
            for j in map_for_cells[1][cell[1]]:
                cells_mapping_to.append((i, j))
        return tuple(cells_mapping_to)

    def tracked_point_placement(
        self,
        requirement_list: tuple[GriddedCayleyPerm, ...],
        indices: tuple[int, ...],
        direction: int,
    ) -> tuple[TrackedTiling]:
        """Yield the tilings with tracked clouds after point placement."""
        if direction not in self.DIRECTIONS:
            raise ValueError(f"Direction {direction} is not a valid direction.")
        cells = []
        for idx, gcp in zip(indices, requirement_list):
            cells.append(gcp.positions[idx])
        cells = sorted(set(cells))
        all_tracked_tilings = []
        for placed_cell in cells:
            tiling = self.point_placement_in_cell(
                requirement_list, indices, direction, placed_cell
            )
            map_for_cells = self.multiplex_map(placed_cell)
            reverse_map = self.col_row_preimages(map_for_cells)
            value_clouds = []
            indices_clouds = []
            for cloud in self.tracked_tiling.value_clouds:
                value_cloud = []
                for cell in cloud:
                    for mapped_cell in self.map_cells_for_clouds(cell, reverse_map):
                        if mapped_cell in tiling.active_cells:
                            value_cloud.append(mapped_cell)
                value_cloud = tuple(value_cloud)
                if value_cloud:
                    value_clouds.append(value_cloud)
            for cloud in self.tracked_tiling.indices_clouds:
                indices_cloud = []
                for cell in cloud:
                    for mapped_cell in self.map_cells_for_clouds(cell, reverse_map):
                        if mapped_cell in tiling.active_cells:
                            indices_cloud.append(mapped_cell)
                indices_cloud = tuple(indices_cloud)
                if indices_cloud:
                    indices_clouds.append(indices_cloud)
            all_tracked_tilings.append(
                TrackedTiling(tiling, tuple(value_clouds), tuple(indices_clouds))
            )
        return tuple(all_tracked_tilings)


class TrackedRequirementPlacementStrategy(RequirementPlacementStrategy):
    """
    A strategy for placing requirements with tracked clouds.
    """

    def algorithm(self, tiling):
        return TrackedPointPlacement(tiling)

    def decomposition_function(self, comb_class: Tiling) -> tuple[Tiling, ...]:
        """Return the decomposition function for the strategy."""
        return (comb_class.add_obstructions(self.gcps),) + self.algorithm(
            comb_class
        ).tracked_point_placement(self.gcps, self.indices, self.direction)


# til = Tiling([], [], (2, 2))
# tracked_til = TrackedTiling(
#     til, value_clouds=(((0, 0), (1, 0)),), indices_clouds=(((0, 1),),)
# )
# print(tracked_til)
# for out in TrackedPointPlacement(tracked_til).tracked_point_placement(
#     [GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)])], (0,), 0
# ):
#     print(out)


class TrackedPointPlacementFactory(PointPlacementFactory):
    """
    A factory for creating point placement strategies for tracked tilings.
    """

    def __call__(
        self, comb_class: Tiling
    ) -> Iterator[TrackedRequirementPlacementStrategy]:
        for cell in comb_class.positive_cells():
            for direction in Directions:
                gcps = (GriddedCayleyPerm(CayleyPermutation([0]), (cell,)),)
                indices = (0,)
                yield TrackedRequirementPlacementStrategy(gcps, indices, direction)


class TrackedRowPlacementFactory(RowInsertionFactory):
    """A factory for placing the minimum points in the rows of tilings."""

    def __call__(self, comb_class: Tiling) -> Iterator[RequirementPlacementStrategy]:
        not_point_rows = set(range(comb_class.dimensions[1])) - comb_class.point_rows
        for row in not_point_rows:
            all_gcps = []
            for col in range(comb_class.dimensions[0]):
                cell = (col, row)
                if cell in comb_class.active_cells:
                    gcps = GriddedCayleyPerm(CayleyPermutation([0]), (cell,))
                    all_gcps.append(gcps)
            indices = tuple(0 for _ in all_gcps)
            for direction in [DIR_LEFT_BOT, DIR_RIGHT_BOT, DIR_LEFT_TOP, DIR_RIGHT_TOP]:
                yield TrackedRequirementPlacementStrategy(all_gcps, indices, direction)


class TrackedColPlacementFactory(ColInsertionFactory):
    """A factory for placing the leftmost or rightmost points in
    the columns of tilings."""

    def __call__(self, comb_class: Tiling) -> Iterator[RequirementPlacementStrategy]:
        not_point_cols = set(range(comb_class.dimensions[0])) - set(
            cell[0] for cell in comb_class.point_cells()
        )
        for col in not_point_cols:
            all_gcps = []
            for row in range(comb_class.dimensions[1]):
                cell = (col, row)
                gcps = GriddedCayleyPerm(CayleyPermutation([0]), (cell,))
                all_gcps.append(gcps)
            indices = tuple(0 for _ in all_gcps)
            for direction in [DIR_LEFT, DIR_RIGHT]:
                yield TrackedRequirementPlacementStrategy(all_gcps, indices, direction)


class TrackedVerticalInsertionEncodingRequirementInsertionFactory(CellInsertionFactory):
    """A factory for making columns positive in Tracked tilings for vertical insertion encoding."""

    def __call__(self, comb_class: Tiling) -> Iterator[RequirementInsertionStrategy]:
        for col in range(comb_class.dimensions[0]):
            if not comb_class.col_is_positive(col):
                gcps = tuple(
                    GriddedCayleyPerm(CayleyPermutation([0]), [cell])
                    for cell in comb_class.cells_in_col(col)
                )
                yield RequirementInsertionStrategy(gcps, ignore_parent=True)
                return

    @classmethod
    def from_dict(
        cls, d: dict
    ) -> "TrackedVerticalInsertionEncodingRequirementInsertionFactory":
        return cls(**d)

    def __str__(self) -> str:
        return "Make columns positive"


class TrackedVerticalInsertionEncodingPlacementFactory(TrackedRowPlacementFactory):
    """A factory for placing the bottom leftmost points in Tracked tilings."""

    def __call__(self, comb_class: Tiling) -> Iterator[RequirementPlacementStrategy]:
        cells = comb_class.active_cells
        gcps = tuple(
            GriddedCayleyPerm(CayleyPermutation([0]), [cell]) for cell in cells
        )
        indices = tuple(0 for _ in gcps)
        direction = DIR_LEFT_BOT
        yield TrackedRequirementPlacementStrategy(gcps, indices, direction)

    @classmethod
    def from_dict(cls, d: dict) -> "TrackedVerticalInsertionEncodingPlacementFactory":
        return cls(**d)

    def __str__(self) -> str:
        return "Place next point of insertion encoding"


class TrackedHorizontalInsertionEncodingRequirementInsertionFactory(
    CellInsertionFactory
):
    """A factory for making rows positive in Tracked tilings for horizontal insertion encoding."""

    def __call__(self, comb_class: Tiling) -> Iterator[RequirementInsertionStrategy]:
        for row in range(comb_class.dimensions[1]):
            if not comb_class.row_is_positive(row):
                gcps = tuple(
                    GriddedCayleyPerm(CayleyPermutation([0]), [cell])
                    for cell in comb_class.cells_in_row(row)
                )
                yield RequirementInsertionStrategy(gcps, ignore_parent=True)

    @classmethod
    def from_dict(
        cls, d: dict
    ) -> "TrackedHorizontalInsertionEncodingRequirementInsertionFactory":
        return cls(**d)

    def __str__(self) -> str:
        return "Make rows positive"


class TrackedHorizontalInsertionEncodingPlacementFactory(TrackedColPlacementFactory):
    """A factory for placing the leftmost points in Tracked tilings."""

    def __call__(
        self, comb_class: Tiling
    ) -> Iterator[TrackedRequirementPlacementStrategy]:
        cells = comb_class.active_cells
        gcps = tuple(
            GriddedCayleyPerm(CayleyPermutation([0]), [cell]) for cell in cells
        )
        indices = tuple(0 for _ in gcps)
        direction = DIR_LEFT
        yield TrackedRequirementPlacementStrategy(gcps, indices, direction)

    @classmethod
    def from_dict(cls, d: dict) -> "TrackedHorizontalInsertionEncodingPlacementFactory":
        return cls(**d)

    def __str__(self) -> str:
        return "Place next point of insertion encoding"
