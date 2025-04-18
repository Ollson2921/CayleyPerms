from comb_spec_searcher import StrategyFactory, Strategy
from typing import Tuple, Optional, Dict, Set, Iterator
from comb_spec_searcher.exception import StrategyDoesNotApply
from comb_spec_searcher.strategies.constructor import Constructor

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm


class FusionStrategy(Strategy[Tiling, GriddedCayleyPerm]):
    def __init__(self, direction: int, index: int, tracked: bool = False):
        self.direction = direction
        self.index = index
        self.tracked = tracked
        if direction not in [1, 0]:
            raise ValueError("Direction must be 1 or 0")
        if index < 0:
            raise ValueError("Index must be non-negative")
        super().__init__(
            ignore_parent=False, inferrable=True, possibly_empty=False, workable=True
        )

    def decomposition_function(self, tiling: Tiling) -> tuple[Tiling]:
        return (tiling.fuse(self.direction, self.index),)

    def can_be_equivalent(self) -> bool:
        return False

    def is_two_way(self, comb_class: Tiling) -> bool:
        return False

    def is_reversible(self, comb_class: Tiling) -> bool:
        """TODO: We told this to return true to make it work but for tracked tilings and counting will need to change"""
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
        if not comb_class.is_fusable(self.direction, self.index):
            raise StrategyDoesNotApply("Strategy does not apply")
        child = comb_class.fuse(self.direction, self.index)
        assert children is None or children == (child,)
        raise NotImplementedError

    def reverse_constructor(  # pylint: disable=no-self-use
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
        raise NotImplementedError

    def _fuse_parameter(self, comb_class: Tiling) -> str:
        raise NotImplementedError

    def formal_step(self) -> str:
        fusing = "rows" if self.direction == 1 else "columns"
        idx = self.index
        return f"Fuse {fusing} {idx} and {idx+1}"

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
        d["direction"] = self.direction
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
            + f"(direction={self.direction}, index={self.index}, "
            f"tracked={self.tracked})"
        )


class FusionFactory(StrategyFactory[Tiling]):
    def __call__(self, comb_class: Tiling):
        # print("Trying fusion")
        for direction in [1, 0]:
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
