"""The algorithms for tracked tilings."""

from typing import Iterable
from gridded_cayley_permutations import GriddedCayleyPerm
from gridded_cayley_permutations.factors import Factors, ShuffleFactors
from gridded_cayley_permutations.point_placements import PointPlacement
from tilescope.strategies.row_column_separation import (
    LessThanRowColSeparation,
    LessThanOrEqualRowColSeparation,
)
from clouds import TrackedTiling

Cell = tuple[int, int]


class TrackedFactors(Factors):
    """Factors and tracks clouds"""

    def __init__(self, tracked_tiling: TrackedTiling) -> None:
        self.tracked_tiling = tracked_tiling
        super().__init__(tracked_tiling.tiling)

    def find_tracked_factors(self) -> Iterable[TrackedTiling]:
        """Return the factors of the tracked tiling."""
        factors = self.find_factors()
        for factor in factors:
            yield TrackedTiling(
                factor,
                value_clouds=tuple(self.tracked_tiling.value_clouds),
                indices_clouds=tuple(self.tracked_tiling.indices_clouds),
                intersect_clouds_with_active=True,
            )


class TrackedShuffleFactors(ShuffleFactors, TrackedFactors):
    """
    Return the interleaving factors, which drops the condition
    of cells being in the same row or column and trackes clouds.

    This is structurally sound, but no longer counted by Cartesian products.
    """


class TrackedLessThanRowColSeparation(LessThanRowColSeparation):
    """Separates rows and columns with less than constraints and tracks clouds."""

    def __init__(self, tracked_tiling: TrackedTiling) -> None:
        self.tracked_tiling = tracked_tiling
        super().__init__(tracked_tiling.tiling)

    def tracked_row_col_separation(self) -> Iterable[TrackedTiling]:
        """Yield the separated tilings with tracked clouds."""
        for separated_tiling in self.row_col_separation():
            value_clouds, indices_clouds = TrackedTiling.map_clouds(
                self.tracked_tiling.value_clouds,
                self.tracked_tiling.indices_clouds,
                self.row_col_map,
            )
            yield TrackedTiling(
                separated_tiling,
                value_clouds=tuple(value_clouds),
                indices_clouds=tuple(indices_clouds),
                intersect_clouds_with_active=True,
            )


class TrackedLessThanOrEqualRowColSeparation(
    LessThanOrEqualRowColSeparation, TrackedLessThanRowColSeparation
):
    """Separates rows and columns with less than or equal constraints and tracks clouds."""


class TrackedPointPlacement(PointPlacement):
    """Point placement tracking clouds."""

    def __init__(self, tracked_tiling: TrackedTiling) -> None:
        self.tracked_tiling = tracked_tiling
        super().__init__(tracked_tiling.tiling)

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
            value_clouds, indices_clouds = TrackedTiling.map_clouds(
                self.tracked_tiling.value_clouds,
                self.tracked_tiling.indices_clouds,
                map_for_cells,
            )
            all_tracked_tilings.append(
                TrackedTiling(
                    tiling,
                    value_clouds,
                    indices_clouds,
                    intersect_clouds_with_active=True,
                )
            )
        return tuple(all_tracked_tilings)
