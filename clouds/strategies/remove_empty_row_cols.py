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

    def decomposition_function(
        self, comb_class: TrackedTiling
    ) -> tuple[TrackedTiling, ...]:
        rows_and_cols = comb_class.find_empty_rows_and_columns()
        if len(rows_and_cols[0]) == 0 and len(rows_and_cols[1]) == 0:
            raise StrategyDoesNotApply("No empty rows or columns")
        return (comb_class.remove_empty_rows_and_columns(),)

    def maps_for_clouds(
        self, comb_class: TrackedTiling
    ) -> tuple[tuple[dict[int, tuple[int, ...]], dict[int, tuple[int, ...]]], ...]:
        empty_rows, empty_cols = comb_class.find_empty_rows_and_columns()
        rc_map = comb_class.tiling_and_rc_map_after_deleting_rows_and_columns(
            empty_rows, empty_cols
        )[1]
        col_map = rc_map.col_map
        row_map = rc_map.row_map
        col_map = {k: (v,) for k, v in col_map.items()}
        row_map = {k: (v,) for k, v in row_map.items()}
        return ((col_map, row_map),)
