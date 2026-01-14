"""Module containing various strategy packs for running TileScope
with tracking."""

from typing import Iterable
from cayley_permutations import CayleyPermutation
from comb_spec_searcher import StrategyPack, AtomStrategy

from clouds.tracked_tiling import TrackedTiling

from .strategies import (
    TrackedVerticalInsertionEncodingPlacementFactory,
    TrackedColPlacementFactory,
    TrackedFusionPointRowFactory,
    TrackedFactorStrategy,
    TrackedHorizontalInsertionEncodingPlacementFactory,
    TrackedHorizontalInsertionEncodingRequirementInsertionFactory,
    TrackedVerticalInsertionEncodingRequirementInsertionFactory,
    TrackedShuffleFactorStrategy,
    TrackedLessThanRowColSeparationStrategy,
    TrackedLessThanOrEqualRowColSeparationStrategy,
    TrackedPointPlacementFactory,
    TrackedRemoveEmptyRowsAndColumnsStrategy,
    TrackedFusionFactory,
    TrackedRowPlacementFactory,
    TrackedVerticalInsertionEncodableVerificationStrategy,
    TrackedHorizontalInsertionEncodableVerificationStrategy,
    TrackedCellInsertionFactory,
)
from tilescope.strategies import (
    SubclassVerificationStrategy,
)


class TileScopePack(StrategyPack):
    """Strategy packs for TileScope."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_basis(self, basis: Iterable[CayleyPermutation]) -> "TileScopePack":
        raise NotImplementedError

    @classmethod
    def vertical_ins_enc(cls):
        """Vertical insertion encoding strategy pack."""
        return TileScopePack(
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
        return TileScopePack(
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
    def point_placement(cls):
        """Point placements strategy pack with both types of fusion."""
        return TileScopePack(
            inferral_strats=[
                TrackedRemoveEmptyRowsAndColumnsStrategy(),
                TrackedLessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                TrackedFactorStrategy(),
                TrackedLessThanOrEqualRowColSeparationStrategy(),
                TrackedFusionPointRowFactory(),
                TrackedFusionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    TrackedCellInsertionFactory(),
                    TrackedPointPlacementFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                TrackedVerticalInsertionEncodableVerificationStrategy(),
                TrackedHorizontalInsertionEncodableVerificationStrategy(),
                SubclassVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="point_placement_with_fusion",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def row_placement(cls):
        """Row placements strategy pack."""
        return TileScopePack(
            inferral_strats=[
                TrackedRemoveEmptyRowsAndColumnsStrategy(),
                TrackedLessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                TrackedFactorStrategy(),
                TrackedLessThanOrEqualRowColSeparationStrategy(),
                TrackedFusionPointRowFactory(),
                TrackedFusionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    TrackedRowPlacementFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                TrackedVerticalInsertionEncodableVerificationStrategy(),
                TrackedHorizontalInsertionEncodableVerificationStrategy(),
                SubclassVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="row_placement_with_fusion",
            symmetries=[],
            iterative=False,
        )

    def make_fusion(
        self,
        point_rows: bool = False,
        apply_first: bool = False,
    ) -> "TileScopePack":
        """
        Create a new pack by adding fusion to the current pack.

        If point_rows, it will add point rows fusion.
        If apply_first, it will add fusion to the front of the initial strategies.
        """
        name = (
            self.name + " with point row fusion"
            if point_rows
            else self.name + " with fusion"
        )
        fusion_strat = (
            TrackedFusionPointRowFactory() if point_rows else TrackedFusionFactory()
        )
        pack = self.add_initial(fusion_strat, name, apply_first=apply_first)
        return pack

    @classmethod
    def col_placement(cls):
        """Column placements with fusion strategy pack."""
        return TileScopePack(
            inferral_strats=[
                TrackedRemoveEmptyRowsAndColumnsStrategy(),
                TrackedLessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                TrackedFactorStrategy(),
                TrackedLessThanOrEqualRowColSeparationStrategy(),
                TrackedFusionPointRowFactory(),
                TrackedFusionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    TrackedColPlacementFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                TrackedVerticalInsertionEncodableVerificationStrategy(),
                TrackedHorizontalInsertionEncodableVerificationStrategy(),
                SubclassVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="col_placement_with_fusion",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def row_and_col_placement(cls):
        """Point placements strategy pack."""
        return TileScopePack(
            inferral_strats=[
                TrackedRemoveEmptyRowsAndColumnsStrategy(),
                TrackedLessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                TrackedFactorStrategy(),
                TrackedLessThanOrEqualRowColSeparationStrategy(),
                TrackedFusionPointRowFactory(),
                TrackedFusionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    TrackedRowPlacementFactory(),
                    TrackedColPlacementFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                TrackedVerticalInsertionEncodableVerificationStrategy(),
                TrackedHorizontalInsertionEncodableVerificationStrategy(),
                SubclassVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="row_and_col_placement_with_fusion",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_row_and_col_placement(cls):
        """Point, row and column placements strategy pack."""
        return TileScopePack(
            inferral_strats=[
                TrackedRemoveEmptyRowsAndColumnsStrategy(),
                TrackedLessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                TrackedFactorStrategy(),
                TrackedLessThanOrEqualRowColSeparationStrategy(),
                TrackedFusionPointRowFactory(),
                TrackedFusionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    TrackedCellInsertionFactory(),
                    TrackedPointPlacementFactory(),
                    TrackedRowPlacementFactory(),
                    TrackedColPlacementFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                TrackedVerticalInsertionEncodableVerificationStrategy(),
                TrackedHorizontalInsertionEncodableVerificationStrategy(),
                SubclassVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="point_row_and_col_placement_with_fusion",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_and_col_placement(cls):
        """Point, row and column placements strategy pack."""
        return TileScopePack(
            inferral_strats=[
                TrackedRemoveEmptyRowsAndColumnsStrategy(),
                TrackedLessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                TrackedFactorStrategy(),
                TrackedLessThanOrEqualRowColSeparationStrategy(),
                TrackedFusionPointRowFactory(),
                TrackedFusionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    TrackedCellInsertionFactory(),
                    TrackedRowPlacementFactory(),
                    TrackedColPlacementFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                TrackedVerticalInsertionEncodableVerificationStrategy(),
                TrackedHorizontalInsertionEncodableVerificationStrategy(),
                SubclassVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="point_and_col_placement_with_fusion",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_and_row_placement(cls):
        """Point, row and column placements strategy pack."""
        return TileScopePack(
            inferral_strats=[
                TrackedRemoveEmptyRowsAndColumnsStrategy(),
                TrackedLessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                TrackedFactorStrategy(),
                TrackedLessThanOrEqualRowColSeparationStrategy(),
                TrackedFusionPointRowFactory(),
                TrackedFusionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    TrackedCellInsertionFactory(),
                    TrackedPointPlacementFactory(),
                    TrackedRowPlacementFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                TrackedVerticalInsertionEncodableVerificationStrategy(),
                TrackedHorizontalInsertionEncodableVerificationStrategy(),
                SubclassVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="point_and_row_placement_with_fusion",
            symmetries=[],
            iterative=False,
        )
