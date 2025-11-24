"""Strategy for verifying when a tiling is insertion encodable."""

from typing import TypeVar
from comb_spec_searcher import VerificationStrategy
from gridded_cayley_permutations import GriddedCayleyPerm, Tiling

HorizontalInsertionEncodableVerificationStrategyT = TypeVar(
    "HorizontalInsertionEncodableVerificationStrategyT",
    bound="HorizontalInsertionEncodableVerificationStrategy",
)

VerticalInsertionEncodableVerificationStrategyT = TypeVar(
    "VerticalInsertionEncodableVerificationStrategyT",
    bound="VerticalInsertionEncodableVerificationStrategy",
)


class HorizontalInsertionEncodableVerificationStrategy(
    VerificationStrategy[Tiling, GriddedCayleyPerm]
):
    """
    A strategy for verifying if a tiling is horizontal insertion encodable.
    """

    def __init__(
        self,
        ignore_parent: bool = False,
    ):
        super().__init__(ignore_parent=ignore_parent)

    def pack(self, comb_class: Tiling):
        # pylint: disable=import-outside-toplevel
        # pylint: disable=cyclic-import
        from tilescope.strategy_packs import TileScopePack

        return TileScopePack.horizontal_insertion_encoding()

    def verified(self, comb_class: Tiling) -> bool:
        return comb_class.is_horizontal_insertion_encodable()

    def formal_step(self):
        return "The tiling is horizontal insertion encodable"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(" f"workable={self.workable})"

    @classmethod
    def from_dict(cls, d: dict) -> "HorizontalInsertionEncodableVerificationStrategy":
        return cls(**d)


class VerticalInsertionEncodableVerificationStrategy(
    HorizontalInsertionEncodableVerificationStrategy
):
    """
    A strategy for verifying if a tiling is vertical insertion encodable.
    """

    def pack(self, comb_class: Tiling):
        # pylint: disable=import-outside-toplevel
        # pylint: disable=cyclic-import
        from tilescope.strategy_packs import TileScopePack

        return TileScopePack.vertical_insertion_encoding()

    def verified(self, comb_class: Tiling) -> bool:
        return comb_class.is_vertical_insertion_encodable()

    def formal_step(self):
        return "The tiling is vertical insertion encodable"
