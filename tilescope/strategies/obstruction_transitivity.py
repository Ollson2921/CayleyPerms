"""Strategy for adding new obstructions to the tiling based on the current obstructions."""

from typing import Iterator, Optional, Tuple
from comb_spec_searcher import DisjointUnionStrategy
from comb_spec_searcher.exception import StrategyDoesNotApply
from gridded_cayley_permutations import (
    ObstructionTransitivity,
    GriddedCayleyPerm,
    Tiling,
)
from gridded_cayley_permutations.point_placements import TilingT


class AbstractObstructionTransitivityStrategy(
    DisjointUnionStrategy[TilingT, GriddedCayleyPerm]
):
    """Removes all the empty rows and columns."""

    # pylint: disable=duplicate-code
    def __init__(
        self,
        ignore_parent: bool = True,
        possibly_empty: bool = False,
    ):
        super().__init__(ignore_parent=ignore_parent, possibly_empty=possibly_empty)

    def extra_parameters(
        self, comb_class: TilingT, children: Optional[Tuple[TilingT, ...]] = None
    ) -> Tuple[dict[str, str], ...]:
        return tuple({} for _ in self.decomposition_function(comb_class))

    def formal_step(self):
        return "Added size 2 obstructions implied by the obstructions on the tiling."

    def backward_map(
        self,
        comb_class: TilingT,
        objs: tuple[Optional[GriddedCayleyPerm], ...],
        children: Optional[tuple[TilingT, ...]] = None,
    ) -> Iterator[GriddedCayleyPerm]:
        raise NotImplementedError

    def forward_map(
        self,
        comb_class: TilingT,
        obj: GriddedCayleyPerm,
        children: Optional[Tuple[TilingT, ...]] = None,
    ) -> Tuple[Optional[GriddedCayleyPerm], ...]:
        raise NotImplementedError

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"ignore_parent={self.ignore_parent}, "
            f"possibly_empty={self.possibly_empty})"
        )

    def to_jsonable(self) -> dict:
        """Return a dictionary form of the strategy."""
        d: dict = super().to_jsonable()
        d.pop("workable")
        d.pop("inferrable")
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "AbstractObstructionTransitivityStrategy":
        return cls(**d)


class ObstructionTransitivityStrategy(AbstractObstructionTransitivityStrategy):
    """A strategy for adding new obstructions to the tiling based on the current obstructions."""

    def decomposition_function(self, comb_class: Tiling) -> Tuple[Tiling, ...]:
        new_obs = ObstructionTransitivity(comb_class).new_obs()
        if not new_obs:
            raise StrategyDoesNotApply("No new obstructions to add.")
        return (comb_class.add_obstructions(new_obs),)
