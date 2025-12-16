from comb_spec_searcher.strategies.strategy import StrategyDoesNotApply
from clouds.tracked_tiling import TrackedTiling
from gridded_cayley_permutations import Tiling
from tilescope.strategies import FactorStrategy, ShuffleFactorStrategy
from .extra_parameters import StrategyWithExtraParameters
from clouds.tracked_algos import TrackedFactors, TrackedShuffleFactors

Cell = tuple[int, int]


class TrackedFactorStrategy(FactorStrategy, StrategyWithExtraParameters):
    """
    A strategy for finding factors in a tracked tiling.
    """

    def decomposition_function(self, comb_class: TrackedTiling) -> tuple[Tiling, ...]:
        factors = tuple(TrackedFactors(comb_class).find_tracked_factors())
        if len(factors) == 1:
            raise StrategyDoesNotApply
        return factors


class TrackedShuffleFactorStrategy(ShuffleFactorStrategy, StrategyWithExtraParameters):
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
