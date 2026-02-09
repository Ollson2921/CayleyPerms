"""Strategy and Factory for requirement insertion on TrackedTilings."""

from typing import Iterator
from tilescope.strategies.requirement_insertions import (
    RequirementInsertionStrategy,
    CellInsertionFactory,
)
from .extra_parameters import ExtraParametersForStrategies
from ..tracked_tiling import TrackedTiling


class TrackedRequirementInsertionStrategy(
    ExtraParametersForStrategies, RequirementInsertionStrategy
):
    """A strategy for inserting requirements into a tracked tiling."""

    def maps_for_clouds(self, comb_class):
        res = []
        for _ in self.decomposition_function(comb_class):
            col_map = {i: (i,) for i in range(comb_class.dimensions[0])}
            row_map = {i: (i,) for i in range(comb_class.dimensions[1])}
            res.append((col_map, row_map))
        return res


class TrackedCellInsertionFactory(CellInsertionFactory):
    """Factory for inserting cell requirements into a tracked tiling."""

    def __call__(
        self, comb_class: TrackedTiling
    ) -> Iterator[TrackedRequirementInsertionStrategy]:
        """ """
        for req_list in self.req_lists_to_insert(comb_class):
            yield TrackedRequirementInsertionStrategy(req_list, self.ignore_parent)
