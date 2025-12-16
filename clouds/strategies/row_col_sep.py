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

    def decomposition_function(
        self, comb_class: TrackedTiling
    ) -> tuple[TrackedTiling, ...]:
        """Return the decomposition function."""
        algo = TrackedLessThanRowColSeparation(comb_class)
        return (next(algo.tracked_row_col_separation()),)


class TrackedLessThanOrEqualRowColSeparationStrategy(
    LessThanOrEqualRowColSeparationStrategy, StrategyWithExtraParameters
):
    """A strategy for separating rows and columns with less than or equal constraints."""

    def decomposition_function(
        self, comb_class: TrackedTiling
    ) -> tuple[TrackedTiling, ...]:
        """Return the decomposition function."""
        algo = TrackedLessThanOrEqualRowColSeparation(comb_class)
        return tuple(algo.tracked_row_col_separation())
