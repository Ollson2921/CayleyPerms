from typing import Optional
from comb_spec_searcher import Strategy
from comb_spec_searcher.strategies.strategy import StrategyDoesNotApply
from clouds.tracked_tiling import TrackedTiling
from gridded_cayley_permutations import GriddedCayleyPerm


class StrategyWithExtraParameters(Strategy[TrackedTiling, GriddedCayleyPerm]):
    """Strategy that has extra parameters function for TrackedTilings."""

    def extra_parameters(
        self,
        comb_class: TrackedTiling,
        children: Optional[tuple[TrackedTiling, ...]] = None,
    ) -> tuple[dict[str, str], ...]:
        if children is None:
            children = self.decomposition_function(comb_class)
        if children is None:
            raise StrategyDoesNotApply("Strategy does not apply")
        dicts = tuple(dict() for _ in range(len(children)))
        for cloud in comb_class.indices_clouds:
            parent_param = comb_class.find_parameter(cloud, row=False)
            for idx, child in enumerate(children):
                child_cloud = tuple(
                    col for col in cloud if col in child.active_col_rows[0]
                )
                child_param = child.find_parameter(child_cloud, row=False)
                dicts[idx][parent_param] = child_param
        for cloud in comb_class.value_clouds:
            parent_param = comb_class.find_parameter(cloud, row=True)
            for idx, child in enumerate(children):
                child_cloud = tuple(
                    row for row in cloud if row in child.active_col_rows[1]
                )
                child_param = child.find_parameter(child_cloud, row=True)
                dicts[idx][parent_param] = child_param
        return dicts
