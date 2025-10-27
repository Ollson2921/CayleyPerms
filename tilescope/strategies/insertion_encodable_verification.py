"""Strategy for verifying when a tiling has no parameters."""

from typing import Optional, Type, TypeVar
from comb_spec_searcher import VerificationStrategy
from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from check_regular_ins_enc import (
    regular_horizontal_insertion_encoding,
    regular_vertical_insertion_encoding,
)

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
        rootmt: Optional[Tiling] = None,
        ignore_parent: bool = False,
    ):
        self._rootmt: Optional[Tiling] = rootmt
        super().__init__(ignore_parent=ignore_parent)

    def change_root(
        self: HorizontalInsertionEncodableVerificationStrategyT,
        tiling: Tiling,
    ) -> HorizontalInsertionEncodableVerificationStrategyT:
        """
        Return a new version of the verification strategy with the given tiling instead
        of the current one.
        """
        return self.__class__(tiling, self.ignore_parent)

    @property
    def rootmt(self) -> Optional[Tiling]:
        """The root tiling."""
        return self._rootmt

    def pack(self, comb_class):
        # pylint: disable=import-outside-toplevel
        # pylint: disable=cyclic-import
        from tilescope.strategy_packs import TileScopePack

        return TileScopePack.horizontal_insertion_encoding()

    def verified(self, comb_class: Tiling) -> bool:
        if comb_class.dimensions[1] == 1:
            for cell in comb_class.active_cells:
                patterns_in_cell = tuple(
                    gcp.pattern
                    for gcp in comb_class.obstructions
                    if all(c[1] == cell[1] for c in gcp.positions)
                )
                if regular_horizontal_insertion_encoding(patterns_in_cell):
                    return True
        return False

    def formal_step(self):
        return "The tiling is horizontal insertion encodable"

    def to_jsonable(self) -> dict:
        d: dict = super().to_jsonable()
        if self._rootmt is not None:
            d["rootmt"] = self._rootmt.to_jsonable()
        return d

    @classmethod
    def from_dict(
        cls: Type[HorizontalInsertionEncodableVerificationStrategyT], d: dict
    ) -> HorizontalInsertionEncodableVerificationStrategyT:
        if "rootmt" in d and d["rootmt"] is not None:
            rootmt: Optional[Tiling] = Tiling.from_dict(d.pop("rootmt"))
        else:
            rootmt = d.pop("rootmt", None)
        return cls(rootmt=rootmt, **d)

    def __repr__(self) -> str:
        args = ", ".join(
            [
                f"root tiling={self._rootmt}",
                f"ignore_parent={self.ignore_parent}",
            ]
        )
        return f"{self.__class__.__name__}({args})"


class VerticalInsertionEncodableVerificationStrategy(
    HorizontalInsertionEncodableVerificationStrategy
):
    """
    A strategy for verifying if a tiling is vertical insertion encodable.
    """

    def pack(self, comb_class):
        # pylint: disable=import-outside-toplevel
        # pylint: disable=cyclic-import
        from tilescope.strategy_packs import TileScopePack

        return TileScopePack.vertical_insertion_encoding()

    def verified(self, comb_class: Tiling) -> bool:
        if comb_class.dimensions[0] == 1:
            for cell in comb_class.active_cells:
                patterns_in_cell = tuple(
                    gcp.pattern
                    for gcp in comb_class.obstructions
                    if all(c[1] == cell[1] for c in gcp.positions)
                )
                if regular_vertical_insertion_encoding(patterns_in_cell):
                    return True
        return False

    def formal_step(self):
        return "The tiling is vertical insertion encodable"
