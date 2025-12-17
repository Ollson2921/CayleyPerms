from tilescope.strategies import (
    LessThanRowColSeparationStrategy,
    LessThanOrEqualRowColSeparationStrategy,
)
from clouds import TrackedTiling
from clouds.tracked_algos import (
    TrackedLessThanOrEqualRowColSeparation,
    TrackedLessThanRowColSeparation,
)
from .extra_parameters import StrategyWithExtraParameters

Cell = tuple[int, int]


class TrackedLessThanRowColSeparationStrategy(
    LessThanRowColSeparationStrategy, StrategyWithExtraParameters
):
    """A strategy for separating rows and columns with less than constraints."""

    def algorithm(self, comb_class):
        return TrackedLessThanRowColSeparation(comb_class)

    def decomposition_function(
        self, comb_class: TrackedTiling
    ) -> tuple[TrackedTiling, ...]:
        """Return the decomposition function."""
        algo = self.algorithm(comb_class)
        return (next(algo.tracked_row_col_separation()),)


class TrackedLessThanOrEqualRowColSeparationStrategy(
    LessThanOrEqualRowColSeparationStrategy, TrackedLessThanRowColSeparationStrategy
):
    """A strategy for separating rows and columns with less than or equal constraints."""

    def algorithm(self, comb_class):
        return TrackedLessThanOrEqualRowColSeparation(comb_class)

    def decomposition_function(
        self, comb_class: TrackedTiling
    ) -> tuple[TrackedTiling, ...]:
        """Return the decomposition function."""
        algo = self.algorithm(comb_class)
        return tuple(algo.tracked_row_col_separation())

    def maps_for_clouds(self, comb_class: TrackedTiling):
        rc_map = self.algorithm(comb_class).row_col_map
        return (rc_map for _ in self.decomposition_function(comb_class))
