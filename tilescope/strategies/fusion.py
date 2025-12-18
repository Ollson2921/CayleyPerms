"""Module for fusion strategy and factory"""

from typing import Tuple, Optional, Dict, Set, Iterator
from comb_spec_searcher import StrategyFactory, Strategy
from comb_spec_searcher.exception import StrategyDoesNotApply
from comb_spec_searcher.strategies.constructor import Constructor
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm


class FusionStrategy(Strategy[Tiling, GriddedCayleyPerm]):
    """Strategy that fuses two rows or columns of a tiling together."""

    def __init__(self, fuse_rows: bool, index: int, tracked: bool = False):
        self.fuse_rows = fuse_rows
        self.index = index
        self.tracked = tracked
        if index < 0:
            raise ValueError("Index must be non-negative")
        super().__init__(
            ignore_parent=False, inferrable=True, possibly_empty=False, workable=True
        )

    def decomposition_function(self, comb_class: Tiling) -> tuple[Tiling]:
        return (comb_class.fuse(self.fuse_rows, self.index),)

    def can_be_equivalent(self) -> bool:
        return False

    def is_two_way(self, comb_class: Tiling) -> bool:
        return False

    def is_reversible(self, comb_class: Tiling) -> bool:
        """TODO: We told this to return true to make it work but
        for tracked tilings and counting will need to change"""
        return True

    def shifts(
        self, comb_class: Tiling, children: Optional[Tuple[Tiling, ...]] = None
    ) -> Tuple[int, ...]:
        return (0,)

    def constructor(
        self, comb_class: Tiling, children: Optional[Tuple[Tiling, ...]] = None
    ):
        if not self.tracked:
            # constructor only enumerates when tracked.
            raise NotImplementedError("The fusion strategy was not tracked.")
        # Need to recompute some info to count, so ignoring passed in children
        if not comb_class.is_fusable(self.fuse_rows, self.index):
            raise StrategyDoesNotApply("Strategy does not apply")
        child = comb_class.fuse(self.fuse_rows, self.index)
        assert children is None or children == (child,)
        raise NotImplementedError

    def reverse_constructor(
        self,
        idx: int,
        comb_class: Tiling,
        children: Optional[Tuple[Tiling, ...]] = None,
    ) -> Constructor:
        raise NotImplementedError

    def extra_parameters(
        self, comb_class: Tiling, children: Optional[Tuple[Tiling, ...]] = None
    ) -> Tuple[Dict[str, str]]:
        raise NotImplementedError

    def left_right_both_sided_parameters(
        self, comb_class: Tiling
    ) -> Tuple[Set[str], Set[str], Set[str]]:
        """Returns parameters."""
        raise NotImplementedError

    def _fuse_parameter(self, comb_class: Tiling) -> str:
        raise NotImplementedError

    def formal_step(self) -> str:
        fusing = "rows" if self.fuse_rows else "columns"
        idx = self.index
        return f"Fuse {fusing} {idx} and {idx + 1}"

    # pylint: disable=arguments-differ
    def backward_map(
        self,
        comb_class: Tiling,
        objs: Tuple[Optional[GriddedCayleyPerm], ...],
        children: Optional[Tuple[Tiling, ...]] = None,
        left_points: Optional[int] = None,
    ) -> Iterator[GriddedCayleyPerm]:
        """
        The backward direction of the underlying bijection used for object
        generation and sampling.
        """
        raise NotImplementedError

    def forward_map(
        self,
        comb_class: Tiling,
        obj: GriddedCayleyPerm,
        children: Optional[Tuple[Tiling, ...]] = None,
    ) -> Tuple[Optional[GriddedCayleyPerm], ...]:
        """
        The forward direction of the underlying bijection used for object
        generation and sampling.
        """
        raise NotImplementedError

    def to_jsonable(self) -> dict:
        d = super().to_jsonable()
        d.pop("ignore_parent")
        d.pop("inferrable")
        d.pop("possibly_empty")
        d.pop("workable")
        d["fuse_rows"] = self.fuse_rows
        d["index"] = self.index
        d["tracked"] = self.tracked
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "FusionStrategy":
        return cls(**d)

    @staticmethod
    def get_op_symbol() -> str:
        return "⚮"

    @staticmethod
    def get_eq_symbol() -> str:
        return "↣"

    def __repr__(self) -> str:
        return (
            self.__class__.__name__
            + f"(fuse_rows={self.fuse_rows}, index={self.index}, "
            f"tracked={self.tracked})"
        )


class FusionFactory(StrategyFactory[Tiling]):
    """Factory for doing fusion."""

    def __call__(self, comb_class: Tiling):
        for direction in [True, False]:
            for index in range(comb_class.dimensions[direction] - 1):
                if comb_class.is_fusable(direction, index):
                    yield FusionStrategy(direction, index)

    @classmethod
    def from_dict(cls, d: dict) -> "FusionFactory":
        return cls(**d)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return "Fusion factory"


class FusionPointRowStrategy(FusionStrategy):
    """Strategy that fuses a point row with an adjacent row of a tiling together."""

    def decomposition_function(self, comb_class: Tiling) -> tuple[Tiling]:
        """If self.index is a point row then remove it, otherwise self.index + 1 is a point row so
        remove that."""
        if self.index in comb_class.point_rows:
            return (comb_class.fuse(True, self.index),)
        return (comb_class.fuse(True, self.index + 1),)

    def formal_step(self) -> str:
        idx = self.index
        return f"Point row fusion of row {idx} and row {idx + 1}"


class FusionPointRowFactory(FusionFactory):
    """Factory for doing fusion with point rows."""

    def __call__(self, comb_class: Tiling):
        for row in comb_class.point_rows:
            if comb_class.is_point_row_fuseable(row):
                yield FusionPointRowStrategy(True, row)

    def __str__(self) -> str:
        return "Fusion for point rows factory"
