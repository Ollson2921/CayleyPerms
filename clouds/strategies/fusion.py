from typing import Optional
from clouds.tracked_tiling import TrackedTiling
from tilescope.strategies import (
    FusionFactory,
    FusionStrategy,
    FusionPointRowFactory,
    FusionPointRowStrategy,
)
from .extra_parameters import ExtraParametersForStrategies
from .fusion_constructor import FusionConstructor
from comb_spec_searcher.strategies.strategy import StrategyDoesNotApply


Cell = tuple[int, int]


class TrackedFusionStrategy(FusionStrategy, ExtraParametersForStrategies):
    """Tracked fusion strategy."""

    def __init__(self, fuse_rows: bool, index: int, tracked: bool = True):
        super().__init__(fuse_rows=fuse_rows, index=index, tracked=tracked)

    def maps_for_clouds(self, comb_class: TrackedTiling):
        rc_map = (
            comb_class.tiling_and_rc_map_after_deleting_rows_and_columns(
                rows=self.index, cols=[]
            )[1]
            if self.fuse_rows
            else comb_class.tiling_and_rc_map_after_deleting_rows_and_columns(
                rows=[], cols=[self.index]
            )[1]
        )
        return (rc_map,)

    def constructor(
        self,
        comb_class: TrackedTiling,
        children: Optional[tuple[TrackedTiling, ...]] = None,
    ) -> FusionConstructor:
        """
        This is where the details of the 'reliance profile' and 'counting'
        functions are hidden.
        """
        if children is None:
            children = self.decomposition_function(comb_class)
        child = children[0]
        fuse_parameter = child.find_parameter(
            child.col_or_row_cloud(self.fuse_rows, self.index), self.fuse_rows
        )
        extra_parameters = self.extra_parameters(comb_class, children)
        left_sided_parameters, right_sided_parameters, both_sided_parameters = (
            self.sided_parameters(comb_class)
        )
        return FusionConstructor(
            comb_class,
            child,
            fuse_parameter,
            extra_parameters,
            left_sided_parameters,
            right_sided_parameters,
            both_sided_parameters,
            0,
            0,
        )

    def sided_parameters(self, comb_class: TrackedTiling):
        """Determine which parameters are left-sided, right-sided, or both-sided."""
        left_sided_parameters = []
        right_sided_parameters = []
        both_sided_parameters = []
        if self.fuse_rows:
            all_clouds = comb_class.value_clouds
            cell_index = 1
        else:
            all_clouds = comb_class.indices_clouds
            cell_index = 0

        for cloud in all_clouds:
            intersects_left = any(cell[cell_index] == self.index for cell in cloud)
            intersects_right = any(cell[cell_index] == self.index + 1 for cell in cloud)
            if intersects_left and intersects_right:
                both_sided_parameters.append(cloud)
            elif intersects_left:
                left_sided_parameters.append(cloud)
            elif intersects_right:
                right_sided_parameters.append(cloud)
        return left_sided_parameters, right_sided_parameters, both_sided_parameters


class TrackedFusionFactory(FusionFactory):
    """Factory for doing fusion."""

    def __call__(self, comb_class: TrackedTiling):
        for direction in [True, False]:
            for index in range(comb_class.dimensions[direction] - 1):
                if comb_class.is_fusable(direction, index):
                    yield TrackedFusionStrategy(direction, index)


class TrackedFusionPointRowStrategy(
    FusionPointRowStrategy, ExtraParametersForStrategies
):

    def __init__(self, fuse_rows: bool, index: int, tracked: bool = True):
        super().__init__(fuse_rows=fuse_rows, index=index, tracked=tracked)

    def decomposition_function(self, comb_class: TrackedTiling) -> tuple[TrackedTiling]:
        """If self.index is a point row then remove it, otherwise self.index + 1 is a point row so
        remove that."""
        if self.index in comb_class.point_rows:
            return (comb_class.fuse(True, self.index),)
        return (comb_class.fuse(True, self.index + 1),)

    def constructor(
        self,
        comb_class: TrackedTiling,
        children: Optional[tuple[TrackedTiling, ...]] = None,
    ) -> FusionConstructor:
        """
        This is where the details of the 'reliance profile' and 'counting'
        functions are hidden.
        """
        if children is None:
            children = self.decomposition_function(comb_class)
        child = children[0]
        raise StrategyDoesNotApply("Constructor not implemented yet.")
        fuse_parameter = child.find_parameter(
            child.col_or_row_cloud(self.fuse_rows, self.index), self.fuse_rows
        )
        extra_parameters = self.extra_parameters(comb_class, children)
        left_sided_parameters, right_sided_parameters, both_sided_parameters = (
            self.sided_parameters(comb_class)
        )
        return FusionConstructor(
            comb_class,
            child,
            fuse_parameter,
            extra_parameters,
            left_sided_parameters,
            right_sided_parameters,
            both_sided_parameters,
            0,
            0,
        )

    def sided_parameters(self, comb_class: TrackedTiling):
        """Determine which parameters are left-sided, right-sided, or both-sided."""
        left_sided_parameters = []
        right_sided_parameters = []
        both_sided_parameters = []
        raise StrategyDoesNotApply("Sided parameters not implemented yet.")
        if self.fuse_rows:
            all_clouds = comb_class.value_clouds
            cell_index = 1
        else:
            all_clouds = comb_class.indices_clouds
            cell_index = 0

        for cloud in all_clouds:
            intersects_left = any(cell[cell_index] == self.index for cell in cloud)
            intersects_right = any(cell[cell_index] == self.index + 1 for cell in cloud)
            if intersects_left and intersects_right:
                both_sided_parameters.append(cloud)
            elif intersects_left:
                left_sided_parameters.append(cloud)
            elif intersects_right:
                right_sided_parameters.append(cloud)
        return left_sided_parameters, right_sided_parameters, both_sided_parameters


class TrackedFusionPointRowFactory(FusionPointRowFactory):
    """Factory for fusing point rows/columns in tracked tilings."""

    def __call__(self, comb_class: TrackedTiling):
        for row in comb_class.point_rows:
            if comb_class.is_point_row_fuseable(row):
                yield TrackedFusionPointRowStrategy(True, row)
