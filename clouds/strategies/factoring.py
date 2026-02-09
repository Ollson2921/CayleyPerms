"""Strategies for factoring tracked tilings."""

from comb_spec_searcher.strategies.strategy import StrategyDoesNotApply
from tilescope.strategies import AbstractFactorStrategy, AbstractShuffleFactorStrategy
from ..tracked_tiling import TrackedTiling
from ..tracked_algos import TrackedFactors, TrackedShuffleFactors
from .extra_parameters import ExtraParametersForStrategies

Cell = tuple[int, int]


class TrackedFactorStrategy(
    ExtraParametersForStrategies,
    AbstractFactorStrategy[TrackedTiling],
):
    """
    A strategy for finding factors in a tracked tiling.
    """

    def decomposition_function(
        self, comb_class: TrackedTiling
    ) -> tuple[TrackedTiling, ...]:
        factors = tuple(TrackedFactors(comb_class).find_tracked_factors())
        if len(factors) == 1:
            raise StrategyDoesNotApply
        return factors

    def maps_for_clouds(self, comb_class: TrackedTiling):
        positive_point_rows, represantives = TrackedFactors(
            comb_class
        ).positive_point_rows_and_represantive
        res = []
        for factor in self.decomposition_function(comb_class):
            col_map = {i: (i,) for i in range(comb_class.dimensions[0])}
            row_map = {
                i: (i,)
                for i in range(comb_class.dimensions[1])
                if i not in positive_point_rows
                or factor.active_cells.intersection(represantives)
            }
            res.append((col_map, row_map))
        return tuple(res)


class TrackedShuffleFactorStrategy(
    ExtraParametersForStrategies, AbstractShuffleFactorStrategy
):
    # pylint:disable=too-many-ancestors
    """
    A strategy for finding factors in a tracked tiling.
    """

    def decomposition_function(
        self, comb_class: TrackedTiling
    ) -> tuple[TrackedTiling, ...]:
        if 1 not in comb_class.dimensions:
            raise StrategyDoesNotApply(
                "TrackedTiling is not a row or column shuffle of factors."
            )
        factors = tuple(TrackedShuffleFactors(comb_class).find_tracked_factors())
        if len(factors) == 1:
            raise StrategyDoesNotApply
        return factors
