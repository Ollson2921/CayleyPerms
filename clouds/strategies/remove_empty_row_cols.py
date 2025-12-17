"""The strategies for tracked tilings."""

from comb_spec_searcher.strategies.strategy import StrategyDoesNotApply
from clouds import TrackedTiling
from tilescope.strategies import (
    RemoveEmptyRowsAndColumnsStrategy,
)
from gridded_cayley_permutations import RowColMap
from .extra_parameters import ExtraParametersForStrategies

Cell = tuple[int, int]


class TrackedRemoveEmptyRowsAndColumnsStrategy(
    RemoveEmptyRowsAndColumnsStrategy, ExtraParametersForStrategies
):
    """Removes all the empty rows and columns from a tiling."""

    def empty_rows_and_columns(
        self, comb_class: TrackedTiling
    ) -> tuple[tuple[int, ...], tuple[int, ...]]:
        return comb_class.find_empty_rows_and_columns()

    def decomposition_function(
        self, comb_class: TrackedTiling
    ) -> tuple[TrackedTiling, ...]:
        rows_and_cols = self.empty_rows_and_columns(comb_class)
        if len(rows_and_cols[0]) == 0 and len(rows_and_cols[1]) == 0:
            raise StrategyDoesNotApply("No empty rows or columns")
        return (comb_class.remove_empty_rows_and_columns(),)

    def maps_for_clouds(self, comb_class: TrackedTiling) -> tuple[RowColMap, ...]:
        rc_map = comb_class.tiling_and_rc_map_after_deleting_rows_and_columns(
            self.empty_rows_and_columns(comb_class)
        )[1]
        return (rc_map,)
