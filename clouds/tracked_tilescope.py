"""Module containing various strategy packs for running TileScope
with tracking."""

from typing import Iterable
from cayley_permutations import CayleyPermutation
from comb_spec_searcher import StrategyPack, AtomStrategy

from clouds.tracked_tiling import TrackedTiling

from .strategies import (
    TrackedVerticalInsertionEncodingPlacementFactory as VerticalInsertionEncodingPlacementFactory,
    TrackedColPlacementFactory as ColPlacementFactory,
    TrackedFusionPointRowFactory as FusionPointRowFactory,
    TrackedFactorStrategy as FactorStrategy,
    TrackedHorizontalInsertionEncodingPlacementFactory as HorizontalInsertionEncodingPlacementFactory,
    TrackedHorizontalInsertionEncodingRequirementInsertionFactory as HorizontalInsertionEncodingRequirementInsertionFactory,
    TrackedVerticalInsertionEncodingRequirementInsertionFactory as VerticalInsertionEncodingRequirementInsertionFactory,
    TrackedShuffleFactorStrategy as ShuffleFactorStrategy,
    TrackedLessThanRowColSeparationStrategy as LessThanRowColSeparationStrategy,
    TrackedLessThanOrEqualRowColSeparationStrategy as LessThanOrEqualRowColSeparationStrategy,
    TrackedPointPlacementFactory as PointPlacementFactory,
    TrackedRemoveEmptyRowsAndColumnsStrategy as RemoveEmptyRowsAndColumnsStrategy,
    TrackedFusionFactory as FusionFactory,
    TrackedRowPlacementFactory as RowPlacementFactory,
    TrackedVerticalInsertionEncodableVerificationStrategy as VerticalInsertionEncodableVerificationStrategy,
    TrackedHorizontalInsertionEncodableVerificationStrategy as HorizontalInsertionEncodableVerificationStrategy,
    TrackedCellInsertionFactory as CellInsertionFactory,
    AddCloudFactory,
)
from tilescope.strategies import (
    SubclassVerificationStrategy,
)

# from tilescope import TileScopePack as BaseTileScopePack


class TrackedTileScopePack(StrategyPack):
    """Strategy packs for TileScope."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_basis(self, basis: Iterable[CayleyPermutation]) -> "TrackedTileScopePack":
        raise NotImplementedError

    @classmethod
    def vertical_ins_enc(cls):
        """Vertical insertion encoding strategy pack."""
        return TrackedTileScopePack(
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
    def horizontal_ins_enc(cls):
        """Horizontal insertion encoding strategy pack."""
        return TrackedTileScopePack(
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
    def standard_fusion_pack(cls, expansion_methods: Iterable[str] = ["point"]):
        """Minimum strategies for a pack. Specify the expansion strategies."""
        if not expansion_methods:
            raise ValueError("At least one expansion strategy must be specified.")
        expansion_strats = []
        name = ""
        if "point" in expansion_methods:
            expansion_strats.append(PointPlacementFactory())
            expansion_strats.append(CellInsertionFactory())
            name += "point_"
        if "row" in expansion_methods:
            expansion_strats.append(RowPlacementFactory())
            name += "row_"
        if "col" in expansion_methods:
            expansion_strats.append(ColPlacementFactory())
            name += "col_"
        name += "fusion_pack"
        return TrackedTileScopePack(
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                AddCloudFactory(),
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
                FusionPointRowFactory(),
                FusionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[expansion_strats],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
            ],  # Iterable[Strategy]
            name=name,
            symmetries=[],
            iterative=False,
        )

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

        return TrackedTileScopePack(
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                AddCloudFactory(),
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
                FusionPointRowFactory(),
                FusionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    CellInsertionFactory(),
                    PointPlacementFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
                SubclassVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="point_placement_with_fusion",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def row_placement(cls):
        """Row placements strategy pack."""
        return TrackedTileScopePack(
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                AddCloudFactory(),
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
                FusionPointRowFactory(),
                FusionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    RowPlacementFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
                SubclassVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="row_placement_with_fusion",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def col_placement(cls):
        """Column placements with fusion strategy pack."""
        return TrackedTileScopePack(
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                AddCloudFactory(),
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
                FusionPointRowFactory(),
                FusionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    ColPlacementFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
                SubclassVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="col_placement_with_fusion",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def row_and_col_placement(cls):
        """Point placements strategy pack."""
        return TrackedTileScopePack(
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                AddCloudFactory(),
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
                FusionPointRowFactory(),
                FusionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    RowPlacementFactory(),
                    ColPlacementFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
                SubclassVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="row_and_col_placement_with_fusion",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_row_and_col_placement(cls):
        """Point, row and column placements strategy pack."""
        return TrackedTileScopePack(
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                AddCloudFactory(),
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
                FusionPointRowFactory(),
                FusionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    CellInsertionFactory(),
                    PointPlacementFactory(),
                    RowPlacementFactory(),
                    ColPlacementFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
                SubclassVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="point_row_and_col_placement_with_fusion",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_and_col_placement(cls):
        """Point, row and column placements strategy pack."""
        return TrackedTileScopePack(
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
                FusionPointRowFactory(),
                FusionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    CellInsertionFactory(),
                    RowPlacementFactory(),
                    ColPlacementFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
                SubclassVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="point_and_col_placement_with_fusion",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_and_row_placement(cls):
        """Point, row and column placements strategy pack."""
        return TrackedTileScopePack(
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
                FusionPointRowFactory(),
                FusionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    CellInsertionFactory(),
                    PointPlacementFactory(),
                    RowPlacementFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
                SubclassVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="point_and_row_placement_with_fusion",
            symmetries=[],
            iterative=False,
        )
