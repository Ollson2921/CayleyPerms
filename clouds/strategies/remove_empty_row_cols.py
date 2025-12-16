"""The strategies for tracked tilings."""

from comb_spec_searcher.strategies.strategy import StrategyDoesNotApply
from clouds import TrackedTiling
from tilescope.strategies import (
    RemoveEmptyRowsAndColumnsStrategy,
)


Cell = tuple[int, int]


class TrackedRemoveEmptyRowsAndColumnsStrategy(RemoveEmptyRowsAndColumnsStrategy):
    """Removes all the empty rows and columns from a tiling."""

    def decomposition_function(
        self, comb_class: TrackedTiling
    ) -> tuple[TrackedTiling, ...]:
        rows_and_cols = comb_class.find_empty_rows_and_columns()
        if len(rows_and_cols[0]) == 0 and len(rows_and_cols[1]) == 0:
            raise StrategyDoesNotApply("No empty rows or columns")
        return (comb_class.remove_empty_rows_and_columns(),)
