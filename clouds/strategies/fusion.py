"""Tracked fusion strategies for tilings."""

from typing import Optional
from comb_spec_searcher.strategies.constructor import Constructor
from tilescope.strategies import (
    AbstractFusionFactory,
    AbstractFusionStrategy,
)
from ..tracked_tiling import TrackedTiling
from .extra_parameters import ExtraParametersForStrategies
from .fusion_constructor import (
    FusionConstructor,
    PointRowFusionConstructor,
    ReverseFusionConstructor,
)


Cell = tuple[int, int]


class AbstractTrackedFusionStrategy(
    ExtraParametersForStrategies, AbstractFusionStrategy[TrackedTiling]
):
    """Abstract fusion strategy for tracked tilings."""

    def maps_for_clouds(self, comb_class: TrackedTiling):
        if self.fuse_rows:
            col_map = {x: (x,) for x in range(comb_class.dimensions[0])}
            row_map = {
                x: (x,) if x <= self.index else (x - 1,)
                for x in range(comb_class.dimensions[1])
            }
        else:
            row_map = {x: (x,) for x in range(comb_class.dimensions[1])}
            col_map = {
                x: (x,) if x <= self.index else (x - 1,)
                for x in range(comb_class.dimensions[0])
            }
        return ((col_map, row_map),)

    def sided_parameters(self, comb_class: TrackedTiling):
        """Determine which parameters are left-sided, right-sided, or both-sided."""
        left_sided_parameters = []
        right_sided_parameters = []
        both_sided_parameters = []
        if self.fuse_rows:
            all_clouds = comb_class.value_clouds
        else:
            all_clouds = comb_class.indices_clouds

        for cloud in all_clouds:
            intersects_left = any(idx == self.index for idx in cloud)
            intersects_right = any(idx == self.index + 1 for idx in cloud)
            if intersects_left and intersects_right:
                both_sided_parameters.append(
                    comb_class.find_parameter(cloud, self.fuse_rows)
                )
            elif intersects_left:
                left_sided_parameters.append(
                    comb_class.find_parameter(cloud, self.fuse_rows)
                )
            elif intersects_right:
                right_sided_parameters.append(
                    comb_class.find_parameter(cloud, self.fuse_rows)
                )
        return left_sided_parameters, right_sided_parameters, both_sided_parameters


class TrackedFusionStrategy(
    AbstractTrackedFusionStrategy,
):
    """Tracked fusion strategy."""

    def __init__(self, fuse_rows: bool, index: int, tracked: bool = True):
        super().__init__(fuse_rows=fuse_rows, index=index, tracked=tracked)

    def decomposition_function(self, comb_class: TrackedTiling) -> tuple[TrackedTiling]:
        return (comb_class.fuse(self.fuse_rows, self.index),)

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
        fuse_parameter = child.find_parameter((self.index,), self.fuse_rows)
        extra_parameters = self.extra_parameters(comb_class, children)
        left_sided_parameters, right_sided_parameters, both_sided_parameters = (
            self.sided_parameters(comb_class)
        )
        return FusionConstructor(
            comb_class,
            child,
            fuse_parameter,
            extra_parameters[0],
            left_sided_parameters,
            right_sided_parameters,
            both_sided_parameters,
            0,
            0,
        )

    def reverse_constructor(self, idx, comb_class, children=None):
        if children is None:
            children = self.decomposition_function(comb_class)
        child = children[0]
        fuse_parameter = child.find_parameter((self.index,), self.fuse_rows)
        extra_parameters = self.extra_parameters(comb_class, children)
        left_sided_parameters, right_sided_parameters, _ = self.sided_parameters(
            comb_class
        )
        return ReverseFusionConstructor(
            comb_class,
            child,
            fuse_parameter,
            extra_parameters[0],
            left_sided_parameters,
            right_sided_parameters,
            0,
            0,
        )

    def is_reversible(self, comb_class: TrackedTiling):
        row_map, col_map = self.maps_for_clouds(comb_class)[0]
        child = self.decomposition_function(comb_class)[0]
        fuse_cloud = (self.index,)
        if self.fuse_rows:
            value_clouds = [
                self.map_cloud(cloud, row_map, child, rows=True)
                for cloud in comb_class.value_clouds
            ]
            return fuse_cloud in value_clouds
        index_clouds = [
            self.map_cloud(cloud, col_map, child, rows=False)
            for cloud in comb_class.indices_clouds
        ]
        return fuse_cloud in index_clouds


class TrackedFusionFactory(AbstractFusionFactory):
    """Factory for doing fusion."""

    def __call__(self, comb_class: TrackedTiling):
        for direction in [True, False]:
            for index in range(comb_class.dimensions[direction] - 1):
                if comb_class.is_fusable(direction, index):
                    yield TrackedFusionStrategy(direction, index)


class TrackedFusionPointRowStrategy(AbstractTrackedFusionStrategy):
    """Tracked point row fusion strategy for fusing together rows,
    at least one of which is a point row."""

    def __init__(self, fuse_rows: bool, index: int, tracked: bool = True):
        super().__init__(fuse_rows=fuse_rows, index=index, tracked=tracked)

    def decomposition_function(self, comb_class: TrackedTiling) -> tuple[TrackedTiling]:
        """If self.index is a point row then remove it, otherwise self.index + 1 is a point row so
        remove that."""
        return (comb_class.fuse(True, self.index),)

    def formal_step(self) -> str:
        idx = self.index
        return f"Point row fusion of row {idx} and row {idx + 1}"

    def constructor(
        self,
        comb_class: TrackedTiling,
        children: Optional[tuple[TrackedTiling, ...]] = None,
    ) -> PointRowFusionConstructor:
        """
        This is where the details of the 'reliance profile' and 'counting'
        functions are hidden.
        """
        if children is None:
            children = self.decomposition_function(comb_class)
        child = children[0]
        fuse_parameter = child.find_parameter((self.index,), self.fuse_rows)
        extra_parameters = self.extra_parameters(comb_class, children)
        left_sided_parameters, right_sided_parameters, _ = self.sided_parameters(
            comb_class
        )
        above = self.index + 1 in comb_class.point_rows
        return PointRowFusionConstructor(
            comb_class,
            child,
            fuse_parameter,
            extra_parameters[0],
            left_sided_parameters,
            right_sided_parameters,
            above,
        )

    def reverse_constructor(
        self,
        idx: int,
        comb_class: TrackedTiling,
        children: Optional[tuple[TrackedTiling, ...]] = None,
    ) -> Constructor:
        raise NotImplementedError


class TrackedFusionPointRowFactory(AbstractFusionFactory):
    """Factory for fusing point rows/columns in tracked tilings."""

    def __call__(self, comb_class: TrackedTiling):
        for row in range(comb_class.dimensions[1] - 1):
            if comb_class.is_point_row_fuseable(row):
                yield TrackedFusionPointRowStrategy(True, row)

    def __str__(self) -> str:
        return "Fusion for point rows factory"
