"""Module containing various strategy packs for running TileScope
in an easy to use format."""

from typing import Iterable
from comb_spec_searcher import StrategyFactory, StrategyPack, AtomStrategy
from gridded_cayley_permutations import Tiling
from tilescope.strategies import (
    RemoveEmptyRowsAndColumnsStrategy,
    FactorStrategy,
    ShuffleFactorStrategy,
    VerticalInsertionEncodingPlacementFactory,
    VerticalInsertionEncodingRequirementInsertionFactory,
    HorizontalInsertionEncodingPlacementFactory,
    HorizontalInsertionEncodingRequirementInsertionFactory,
    CellInsertionFactory,
    PointPlacementFactory,
    LessThanRowColSeparationStrategy,
    LessThanOrEqualRowColSeparationStrategy,
    RowInsertionFactory,
    ColInsertionFactory,
    VerticalInsertionEncodableVerificationStrategy,
    HorizontalInsertionEncodableVerificationStrategy,
    SubclassVerificationStrategy,
    FusionPointRowFactory,
    FusionFactory,
)


class TileScopePack(StrategyPack):
    """Strategy packs for TileScope."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # General pack creation methods

    @classmethod
    def make_pack(
        cls,
        expansions: Iterable[str],
        root: Tiling | None = None,
        verify: bool = False,
        cell_insertion_initial: bool = False,
        fusion: int = 0,
        shuffle_factors: bool = False,
    ):
        """Make a strategy pack with the given strategies.
        root: The root tiling. Only needed if verify is True.
        expansions: The expansion strategies to use; a list of strings where
            - "point": PointPlacementFactory
            - "row": RowInsertionFactory
            - "col": ColInsertionFactory
        verify: If True then includes all verification strategies, otherwise just AtomStrategy.
        cell_insertion_initial: If True includes cell insertion as an initial strategy, else
        included as an expansion strategy.
        fusion: If 0, no fusion. If 1, standard fusion. If 2, point row fusion. If 3, both.
        shuffle_factors: If True, replaces FactorStrategy with ShuffleFactorStrategy.
        """
        if not expansions and cell_insertion_initial:
            raise ValueError("At least one expansion strategy must be provided.")
        pack = cls.basics()

        exp_strats: list[StrategyFactory] = []
        exp_name = "_and_".join(expansions)
        for strat in expansions:
            if strat == "point":
                exp_strats.append(PointPlacementFactory())
            elif strat == "row":
                exp_strats.append(RowInsertionFactory())
            elif strat == "col":
                exp_strats.append(ColInsertionFactory())
            else:
                raise ValueError(f"Unknown expansion strategy: {strat}")
        exp_name += "_placement"

        if not cell_insertion_initial:
            exp_strats.append(CellInsertionFactory())
            pack = pack.add_expansion(exp_strats, name_ext=exp_name)
        else:
            pack = pack.add_expansion(exp_strats, name_ext=exp_name)
            pack = pack.add_initial(CellInsertionFactory(), "initial_cell_insertion")

        if fusion:
            pack = pack.add_fusion(fusion_type=fusion, apply_first=False)

        if verify:
            if root is None:
                raise ValueError("root Tiling must be provided if verify is True.")
            pack = pack.add_verification_strats(root=root)

        if shuffle_factors:
            pack = pack.remove_strategy(FactorStrategy())
            pack = pack.add_initial(ShuffleFactorStrategy(), "with_shuffle_factors")

        return pack.change_name(pack.name[1:])

    @classmethod
    def basics(cls):
        """Minimum strategies for a pack.
        NOTE: Has no expansion strategies!! Add them in."""
        return TileScopePack(
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            expansion_strats=[],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
            ],  # Iterable[Strategy]
            name="",
            symmetries=[],
            iterative=False,
        )

    def add_verification_strats(
        self,
        root: Tiling,
    ):
        """Return a new pack with the given verification strategies added.
        ver_strats: The verification strategies to add.
        name_ext: The string to append to the name of the pack."""
        pack = self.add_verification(
            strategy=SubclassVerificationStrategy(root), name_ext="with_verification"
        )
        ver_strats = [
            VerticalInsertionEncodableVerificationStrategy(),
            HorizontalInsertionEncodableVerificationStrategy(),
        ]
        for strat in ver_strats:
            pack = pack.add_verification(strat)
        return pack

    def add_fusion(
        self,
        fusion_type: int = 1,
        apply_first: bool = False,
    ) -> "TileScopePack":
        """
        Create a new pack by adding fusion to the current pack.

        If fusion_type is 1, use standard fusion.
        If fusion_type is 2, use point row fusion.
        If fusion_type is 3, use both.
        """
        if fusion_type == 1:
            return self.add_initial(
                FusionFactory(), "with_fusion", apply_first=apply_first
            )
        if fusion_type == 2:
            return self.add_initial(
                FusionPointRowFactory(),
                "with_point_row_fusion",
                apply_first=apply_first,
            )
        if fusion_type == 3:
            pack = self.add_initial(
                FusionFactory(), "with_fusion", apply_first=apply_first
            )
            pack = pack.add_initial(
                FusionPointRowFactory(),
                "and_point_row_fusion",
                apply_first=apply_first,
            )
            return pack
        raise ValueError("fusion_type must be 1, 2, or 3.")

    def change_name(self, new_name: str) -> "TileScopePack":
        """Return a new pack with the given name."""
        return TileScopePack(
            initial_strats=self.initial_strats,
            inferral_strats=self.inferral_strats,
            expansion_strats=self.expansion_strats,
            ver_strats=self.ver_strats,
            name=new_name,
            symmetries=self.symmetries,
            iterative=self.iterative,
        )

    @classmethod
    def point_placement(cls):
        """Point placement strategy pack."""
        return cls.make_pack(expansions=["point"])

    @classmethod
    def row_and_col_placement(cls):
        """Row and column placement strategy pack."""
        return cls.make_pack(expansions=["row", "col"])

    # Other packs

    @classmethod
    def vertical_insertion_encoding(cls):
        """Vertical insertion encoding strategy pack."""
        return TileScopePack(
            initial_strats=[
                FactorStrategy(),
                VerticalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[RemoveEmptyRowsAndColumnsStrategy()],
            expansion_strats=[[VerticalInsertionEncodingPlacementFactory()]],
            ver_strats=[AtomStrategy()],
            name="vertical_insertion_encoding",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def horizontal_insertion_encoding(cls):
        """Horizontal insertion encoding strategy pack."""
        return TileScopePack(
            initial_strats=[
                FactorStrategy(),
                HorizontalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[RemoveEmptyRowsAndColumnsStrategy()],
            expansion_strats=[[HorizontalInsertionEncodingPlacementFactory()]],
            ver_strats=[AtomStrategy()],
            name="horizontal_insertion_encoding",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def cell_insertion(cls, length: int):
        """Cell insertion strategy pack."""
        return TileScopePack(
            inferral_strats=[],
            initial_strats=[],
            expansion_strats=[
                [
                    CellInsertionFactory(maxreqlen=length),
                ]
            ],
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
                SubclassVerificationStrategy(),
            ],
            name=f"cell_insertion_patterns_up_to_length_{length}",
            symmetries=[],
            iterative=False,
        )
