"""Module containing various strategy packs for running TileScope
with tracking."""

from typing import Iterable
from comb_spec_searcher import StrategyPack, AtomStrategy, StrategyFactory
from cayley_permutations import CayleyPermutation
from tilescope.strategies import (
    SubclassVerificationStrategy,
)
from .strategies import (
    TrackedVerticalInsertionEncodingPlacementFactory,
    TrackedColPlacementFactory,
    TrackedFusionPointRowFactory,
    TrackedFactorStrategy,
    TrackedHorizontalInsertionEncodingPlacementFactory,
    TrackedHorizontalInsertionEncodingRequirementInsertionFactory,
    TrackedVerticalInsertionEncodingRequirementInsertionFactory,
    TrackedLessThanRowColSeparationStrategy,
    TrackedLessThanOrEqualRowColSeparationStrategy,
    TrackedPointPlacementFactory,
    TrackedRemoveEmptyRowsAndColumnsStrategy,
    TrackedFusionFactory,
    TrackedRowPlacementFactory,
    TrackedVerticalInsertionEncodableVerificationStrategy,
    TrackedHorizontalInsertionEncodableVerificationStrategy,
    TrackedCellInsertionFactory,
    AddCloudFactory,
)


class TrackedTileScopePack(StrategyPack):
    """Strategy packs for TileScope."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_basis(self, basis: Iterable[CayleyPermutation]) -> "TrackedTileScopePack":
        """For adding a basis to the pack."""
        raise NotImplementedError

    @classmethod
    def vertical_ins_enc(cls):
        """Vertical insertion encoding strategy pack."""
        return TrackedTileScopePack(
            initial_strats=[
                TrackedFactorStrategy(),
                TrackedVerticalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[TrackedRemoveEmptyRowsAndColumnsStrategy()],
            expansion_strats=[[TrackedVerticalInsertionEncodingPlacementFactory()]],
            ver_strats=[AtomStrategy()],
            name="vertical_insertion_encoding",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def horizontal_ins_enc(cls):
        """Horizontal insertion encoding strategy pack."""
        return TrackedTileScopePack(
            initial_strats=[
                TrackedFactorStrategy(),
                TrackedHorizontalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[TrackedRemoveEmptyRowsAndColumnsStrategy()],
            expansion_strats=[[TrackedHorizontalInsertionEncodingPlacementFactory()]],
            ver_strats=[AtomStrategy()],
            name="horizontal_insertion_encoding",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def standard_fusion_pack(
        cls,
        expansion_methods: Iterable[str] = ["point"],
        subclass_verification: bool = False,
        base_tiling: TrackedTiling | None = None,
    ):
        """Minimum strategies for a pack. Specify the expansion strategies."""
        # pylint: disable=dangerous-default-value
        if not expansion_methods:
            raise ValueError("At least one expansion strategy must be specified.")
        expansion_strats: list[StrategyFactory] = []
        name = ""
        if "point" in expansion_methods:
            expansion_strats.append(TrackedPointPlacementFactory())
            expansion_strats.append(TrackedCellInsertionFactory())
            name += "point_"
        if "row" in expansion_methods:
            expansion_strats.append(TrackedRowPlacementFactory())
            name += "row_"
        if "col" in expansion_methods:
            expansion_strats.append(TrackedColPlacementFactory())
            name += "col_"
        name += "placement_fusion_pack"
        pack = TrackedTileScopePack(
            inferral_strats=[
                TrackedRemoveEmptyRowsAndColumnsStrategy(),
                TrackedLessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                AddCloudFactory(),
                TrackedFactorStrategy(),
                TrackedLessThanOrEqualRowColSeparationStrategy(),
                TrackedFusionPointRowFactory(),
                TrackedFusionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[expansion_strats],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                TrackedVerticalInsertionEncodableVerificationStrategy(),
                TrackedHorizontalInsertionEncodableVerificationStrategy(),
            ],  # Iterable[Strategy]
            name=name,
            symmetries=[],
            iterative=False,
        )
        if subclass_verification:
            pack.add_verification(SubclassVerificationStrategy(root=base_tiling))
        return pack

    @classmethod
    def all_packs(cls) -> Iterable["TrackedTileScopePack"]:
        """All strategy packs with fusion."""
        return [
            TrackedTileScopePack.standard_fusion_pack(expansion_methods=["point"]),
            TrackedTileScopePack.standard_fusion_pack(
                expansion_methods=["point", "col"]
            ),
            TrackedTileScopePack.standard_fusion_pack(
                expansion_methods=["point", "row"]
            ),
            TrackedTileScopePack.standard_fusion_pack(
                expansion_methods=["point", "row", "col"]
            ),
            TrackedTileScopePack.standard_fusion_pack(expansion_methods=["row"]),
            TrackedTileScopePack.standard_fusion_pack(expansion_methods=["col"]),
            TrackedTileScopePack.standard_fusion_pack(expansion_methods=["row", "col"]),
        ]

    @classmethod
    def point_placement(cls):
        """Point placements strategy pack with both types of fusion."""

        return TrackedTileScopePack.standard_fusion_pack(expansion_methods=["point"])

    @classmethod
    def row_placement(cls):
        """Row placements strategy pack."""
        return TrackedTileScopePack.standard_fusion_pack(expansion_methods=["row"])

    @classmethod
    def col_placement(cls):
        """Column placements with fusion strategy pack."""
        return TrackedTileScopePack.standard_fusion_pack(expansion_methods=["col"])

    @classmethod
    def row_and_col_placement(cls):
        """Point placements strategy pack."""
        return TrackedTileScopePack.standard_fusion_pack(
            expansion_methods=["row", "col"]
        )

    @classmethod
    def point_row_and_col_placement(cls):
        """Point, row and column placements strategy pack."""
        return TrackedTileScopePack.standard_fusion_pack(
            expansion_methods=["point", "row", "col"]
        )

    @classmethod
    def point_and_col_placement(cls):
        """Point, row and column placements strategy pack."""
        return TrackedTileScopePack.standard_fusion_pack(
            expansion_methods=["point", "col"]
        )

    @classmethod
    def point_and_row_placement(cls):
        """Point, row and column placements strategy pack."""
        return TrackedTileScopePack.standard_fusion_pack(
            expansion_methods=["point", "row"]
        )
