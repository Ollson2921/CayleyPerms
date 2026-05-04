"""OBstruction transitivity strategy for tracked tilings."""

from comb_spec_searcher.exception import StrategyDoesNotApply
from tilescope.strategies.obstruction_transitivity import (
    AbstractObstructionTransitivityStrategy,
)
from gridded_cayley_permutations import ObstructionTransitivity
from .extra_parameters import ExtraParametersForStrategies
from ..tracked_tiling import TrackedTiling


class TrackedObstructionTransitivityStrategy(
    ExtraParametersForStrategies, AbstractObstructionTransitivityStrategy
):
    """A strategy for adding new obstructions to the tiling based on the current obstructions."""

    def decomposition_function(
        self, comb_class: TrackedTiling
    ) -> tuple[TrackedTiling, ...]:
        new_obs = ObstructionTransitivity(comb_class).new_obs()
        if not new_obs:
            raise StrategyDoesNotApply("No new obstructions to add.")
        return (comb_class.add_obstructions(new_obs),)

    def maps_for_clouds(self, comb_class: TrackedTiling):
        col_map = {i: (i,) for i in range(comb_class.dimensions[0])}
        row_map = {i: (i,) for i in range(comb_class.dimensions[1])}
        return ((col_map, row_map),)
