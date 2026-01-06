from typing import Iterator
from clouds.tracked_tiling import TrackedTiling
from tilescope.strategies.requirement_insertions import (
    RequirementInsertionStrategy,
    VerticalInsertionEncodingRequirementInsertionFactory,
    HorizontalInsertionEncodingRequirementInsertionFactory,
    CellInsertionFactory,
)
from .extra_parameters import ExtraParametersForStrategies


class TrackedRequirementInsertionStrategy(
    ExtraParametersForStrategies, RequirementInsertionStrategy
):
    def maps_for_clouds(self, comb_class):
        res = []
        for _ in self.decomposition_function(comb_class):
            col_map = {i: (i,) for i in range(comb_class.dimensions[0])}
            row_map = {i: (i,) for i in range(comb_class.dimensions[1])}
            res.append((col_map, row_map))
        return res


class TrackedCellInsertionFactory(CellInsertionFactory):
    def __call__(
        self, comb_class: TrackedTiling
    ) -> Iterator[TrackedRequirementInsertionStrategy]:
        """ """
        for req_list in self.req_lists_to_insert(comb_class):
            yield TrackedRequirementInsertionStrategy(req_list, self.ignore_parent)
