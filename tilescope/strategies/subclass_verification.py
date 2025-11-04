"""Strategy for verifying when a tiling is a subclass of the original class."""

from typing import Optional, Type, TypeVar
from comb_spec_searcher import VerificationStrategy
from gridded_cayley_permutations import GriddedCayleyPerm, Tiling

SubclassVerificationStrategyT = TypeVar(
    "SubclassVerificationStrategyT",
    bound="SubclassVerificationStrategy",
)


class SubclassVerificationStrategy(VerificationStrategy[Tiling, GriddedCayleyPerm]):
    """
    A strategy for verifying if a tiling is a subclass of the original class.
    """

    def __init__(
        self,
        root: Optional[Tiling] = None,
        ignore_parent: bool = False,
    ):
        self._root: Optional[Tiling] = root
        super().__init__(ignore_parent=ignore_parent)

    def change_root(
        self: SubclassVerificationStrategyT,
        tiling: Tiling,
    ) -> SubclassVerificationStrategyT:
        """
        Return a new version of the verification strategy with the given tiling instead
        of the current one.
        """
        return self.__class__(tiling, self.ignore_parent)

    @property
    def root(self) -> Optional[Tiling]:
        """The root tiling."""
        return self._root

    def pack(self, comb_class):
        # pylint: disable=import-outside-toplevel
        # pylint: disable=cyclic-import
        from tilescope.strategy_packs import TileScopePack

        return TileScopePack.point_placement()

    def verified(self, comb_class: Tiling) -> bool:
        if comb_class.dimensions[0] == 1 == comb_class.dimensions[1] and (
            self.root is not None and comb_class.obstructions != self.root.obstructions
        ):
            return True
        return False

    def formal_step(self):
        return "The tiling is a subclass of the original class"

    def to_jsonable(self) -> dict:
        # pylint: disable=duplicate-code
        d: dict = super().to_jsonable()
        if self._root is not None:
            d["root"] = self._root.to_jsonable()
        return d

    @classmethod
    def from_dict(
        cls: Type[SubclassVerificationStrategyT], d: dict
    ) -> SubclassVerificationStrategyT:
        # pylint: disable=duplicate-code
        if "root" in d and d["root"] is not None:
            root: Optional[Tiling] = Tiling.from_dict(d.pop("root"))
        else:
            root = d.pop("root", None)
        return cls(root=root, **d)

    def __repr__(self) -> str:
        args = ", ".join(
            [
                f"root tiling={self._root}",
                f"ignore_parent={self.ignore_parent}",
            ]
        )
        return f"{self.__class__.__name__}({args})"
