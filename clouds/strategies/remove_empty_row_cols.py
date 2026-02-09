"""The strategies for tracked tilings."""

from comb_spec_searcher.strategies.strategy import StrategyDoesNotApply
from tilescope.strategies import (
    AbstractRemoveEmptyRowsAndColumnsStrategy,
)
from .extra_parameters import ExtraParametersForStrategies
from ..tracked_tiling import TrackedTiling

Cell = tuple[int, int]


class TrackedRemoveEmptyRowsAndColumnsStrategy(
    ExtraParametersForStrategies,
    AbstractRemoveEmptyRowsAndColumnsStrategy[TrackedTiling],
):
    """Removes all the empty rows and columns from a tiling."""

    def decomposition_function(
        self, comb_class: TrackedTiling
    ) -> tuple[TrackedTiling, ...]:
        rows_and_cols = comb_class.find_empty_rows_and_columns()
        if len(rows_and_cols[0]) == 0 and len(rows_and_cols[1]) == 0:
            raise StrategyDoesNotApply("No empty rows or columns")
        return (comb_class.remove_empty_rows_and_columns(),)

    def maps_for_clouds(self, comb_class: TrackedTiling):
        empty_rows, empty_cols = comb_class.find_empty_rows_and_columns()
        rc_map = comb_class.tiling_and_rc_map_after_deleting_rows_and_columns(
            empty_rows, empty_cols
        )[1]
        col_map = rc_map.col_map
        row_map = rc_map.row_map
        col_map = {k: col_map[k] for k in col_map.keys()}
        row_map = {k: row_map[k] for k in row_map.keys()}
        return ((col_map, row_map),)
