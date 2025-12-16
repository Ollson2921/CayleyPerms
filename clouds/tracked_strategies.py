"""The strategies for tracked tilings."""

from typing import Iterator, Optional
from comb_spec_searcher.strategies.strategy import StrategyDoesNotApply
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from tilescope.strategies import (
    FactorStrategy,
    ShuffleFactorStrategy,
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
    TrackedFactors,
    TrackedShuffleFactors,
    TrackedLessThanOrEqualRowColSeparation,
    TrackedPointPlacement,
)

Cell = tuple[int, int]


class TrackedFactorStrategy(FactorStrategy):
    """
    A strategy for finding factors in a tracked tiling.
    """

    def decomposition_function(self, comb_class: TrackedTiling) -> tuple[Tiling, ...]:
        factors = tuple(TrackedFactors(comb_class).find_tracked_factors())
        if len(factors) == 1:
            raise StrategyDoesNotApply
        return factors

    def extra_parameters(
        self,
        comb_class: TrackedTiling,
        children: Optional[tuple[TrackedTiling, ...]] = None,
    ) -> tuple[dict[str, str], ...]:
        if children is None:
            children = self.decomposition_function(comb_class)
        if children is None:
            raise StrategyDoesNotApply("Strategy does not apply")
        dicts = tuple(dict() for _ in range(len(children)))
        for cloud in comb_class.indices_clouds:
            parent_param = comb_class.find_parameter(cloud, row=False)
            for idx, child in enumerate(children):
                child_cloud = tuple(
                    cell for cell in cloud if cell in child.active_cells
                )
                child_param = child.find_parameter(child_cloud, row=False)
                dicts[idx][parent_param] = child_param
        for cloud in comb_class.value_clouds:
            parent_param = comb_class.find_parameter(cloud, row=True)
            for idx, child in enumerate(children):
                child_cloud = tuple(
                    cell for cell in cloud if cell in child.active_cells
                )
                child_param = child.find_parameter(child_cloud, row=True)
                dicts[idx][parent_param] = child_param
        return dicts


class TrackedShuffleFactorStrategy(ShuffleFactorStrategy):
    """
    A strategy for finding factors in a tracked tiling.
    """

    def decomposition_function(self, comb_class: TrackedTiling) -> tuple[Tiling, ...]:
        if 1 not in comb_class.dimensions:
            raise StrategyDoesNotApply(
                "Tiling is not a row or column shuffle of factors."
            )
        factors = TrackedShuffleFactors(comb_class).find_tracked_factors()
        if len(factors) == 1:
            raise StrategyDoesNotApply
        return factors


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


from tilescope.strategies import (
    RemoveEmptyRowsAndColumnsStrategy,
    VerticalInsertionEncodableVerificationStrategy,
    HorizontalInsertionEncodableVerificationStrategy,
    SubclassVerificationStrategy,
    FusionFactory,
    FusionStrategy,
    FusionPointRowFactory,
    CellInsertionFactory,
    ColInsertionFactory,
    RowInsertionFactory,
)
from comb_spec_searcher.strategies import StrategyFactory


class TrackedColInsertionFactory(ColInsertionFactory):
    """Factory for having a point requirement on a column."""

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


class TrackedRemoveEmptyRowsAndColumnsStrategy(RemoveEmptyRowsAndColumnsStrategy):
    """Removes all the empty rows and columns from a tiling."""

    def decomposition_function(self, comb_class: Tiling) -> tuple[Tiling, ...]:
        rows_and_cols = comb_class.find_empty_rows_and_columns()
        if len(rows_and_cols[0]) == 0 and len(rows_and_cols[1]) == 0:
            raise StrategyDoesNotApply("No empty rows or columns")
        print(repr(comb_class))
        return (comb_class.remove_empty_rows_and_columns(),)
