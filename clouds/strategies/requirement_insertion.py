"""Strategy and Factory for requirement insertion on TrackedTilings."""

from typing import Iterator
from tilescope.strategies.requirement_insertions import (
    AbstractRequirementInsertionStrategy,
    AbstractCellInsertionFactory,
)
from .extra_parameters import ExtraParametersForStrategies
from ..tracked_tiling import TrackedTiling


class TrackedRequirementInsertionStrategy(
    ExtraParametersForStrategies,
    AbstractRequirementInsertionStrategy[TrackedTiling],
):
    """A strategy for inserting requirements into a tracked tiling."""

    def maps_for_clouds(self, comb_class):
        res = []
        for _ in self.decomposition_function(comb_class):
            col_map = {i: (i,) for i in range(comb_class.dimensions[0])}
            row_map = {i: (i,) for i in range(comb_class.dimensions[1])}
            res.append((col_map, row_map))
        return tuple(res)

    def decomposition_function(
        self, comb_class: TrackedTiling
    ) -> tuple[TrackedTiling, ...]:
        return (
            comb_class.add_obstructions(self.gcps),
            comb_class.add_requirement_list(self.gcps),
        )


class TrackedCellInsertionFactory(AbstractCellInsertionFactory[TrackedTiling]):
    """Factory for inserting cell requirements into a tracked tiling."""

    def __call__(
        self, comb_class: TrackedTiling
    ) -> Iterator[TrackedRequirementInsertionStrategy]:
        """ """
        for req_list in self.req_lists_to_insert(comb_class):
            yield TrackedRequirementInsertionStrategy(req_list, self.ignore_parent)
