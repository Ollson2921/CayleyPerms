"""Module containing various strategy packs for running TileScope
with tracking."""

# from typing import Optional
from comb_spec_searcher import StrategyPack, AtomStrategy

from clouds.tracked_tiling import TrackedTiling

# from .tracked_strategies import (
#     TrackedFactorStrategy,
#     TrackedShuffleFactorStrategy,
#     TrackedVerticalInsertionEncodingPlacementFactory,
#     TrackedVerticalInsertionEncodingRequirementInsertionFactory,
#     TrackedHorizontalInsertionEncodingPlacementFactory,
#     TrackedHorizontalInsertionEncodingRequirementInsertionFactory,
#     TrackedPointPlacementFactory,
#     TrackedLessThanRowColSeparationStrategy,
#     TrackedLessThanOrEqualRowColSeparationStrategy,
#     TrackedColPlacementFactory,
#     TrackedRemoveEmptyRowsAndColumnsStrategy, TrackedFusionStrategy
# )


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
)
from tilescope.strategies import (
    CellInsertionFactory,
    VerticalInsertionEncodableVerificationStrategy,
    HorizontalInsertionEncodableVerificationStrategy,
    SubclassVerificationStrategy,
)


class TileScopePack(StrategyPack):
    """Strategy packs for TileScope."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
                    CellInsertionFactory(),
                    TrackedPointPlacementFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="point_placement",
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
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="row_placement",
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
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="col_placement",
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
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="row_and_col_placement",
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
                    CellInsertionFactory(),
                    TrackedPointPlacementFactory(),
                    TrackedRowPlacementFactory(),
                    TrackedColPlacementFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="point_row_and_col_placement",
            symmetries=[],
            iterative=False,
        )
