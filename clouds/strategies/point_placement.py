from typing import Iterator
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm, RowColMap
from tilescope.strategies import (
    RequirementPlacementStrategy,
    CellInsertionFactory,
    PointPlacementFactory,
    RowInsertionFactory,
    ColInsertionFactory,
    RequirementInsertionStrategy,
)
from tilescope.strategies.point_placements import (
    DIR_LEFT_BOT,
    DIR_RIGHT_BOT,
    DIR_LEFT_TOP,
    DIR_RIGHT_TOP,
    DIR_LEFT,
    DIR_RIGHT,
    Directions,
)
from clouds import TrackedTiling
from clouds.tracked_algos import (
    TrackedPointPlacement,
)
from .extra_parameters import ExtraParametersForStrategies

Cell = tuple[int, int]


class TrackedRequirementPlacementStrategy(
    RequirementPlacementStrategy, ExtraParametersForStrategies
):
    """
    A strategy for placing requirements with tracked clouds.
    """

    def algorithm(self, tiling):
        return TrackedPointPlacement(tiling)

    def decomposition_function(
        self, comb_class: TrackedTiling
    ) -> tuple[TrackedTiling, ...]:
        """Return the decomposition function for the strategy."""
        return (comb_class.add_obstructions(self.gcps),) + self.algorithm(
            comb_class
        ).tracked_point_placement(self.gcps, self.indices, self.direction)

    def maps_for_clouds(self, comb_class: TrackedTiling):
        obs_child = (
            {i: (i,) for i in range(comb_class.dimensions[0])},
            {i: (i,) for i in range(comb_class.dimensions[1])},
        )
        maps_for_children = [obs_child]
        for cell in self.algorithm(comb_class).cells_to_place_in(
            self.gcps, self.indices
        ):
            preimage_rc_map = self.algorithm(comb_class).multiplex_map(cell)
            col_map = {
                idx: preimage_rc_map.preimages_of_col(idx)
                for idx in range(comb_class.dimensions[0])
            }
            row_map = {
                idx: preimage_rc_map.preimages_of_row(idx)
                for idx in range(comb_class.dimensions[1])
            }
            rc_map = (col_map, row_map)
            maps_for_children.append(rc_map)
        return tuple(maps_for_children)


class TrackedPointPlacementFactory(PointPlacementFactory):
    """
    A factory for creating point placement strategies for tracked tilings.
    """

    def __call__(
        self, comb_class: TrackedTiling
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

    def __call__(
        self, comb_class: TrackedTiling
    ) -> Iterator[TrackedRequirementPlacementStrategy]:
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

    def __call__(
        self, comb_class: TrackedTiling
    ) -> Iterator[RequirementInsertionStrategy]:
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

    def __call__(
        self, comb_class: TrackedTiling
    ) -> Iterator[RequirementPlacementStrategy]:
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

    def __call__(
        self, comb_class: TrackedTiling
    ) -> Iterator[RequirementInsertionStrategy]:
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
        self, comb_class: TrackedTiling
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
