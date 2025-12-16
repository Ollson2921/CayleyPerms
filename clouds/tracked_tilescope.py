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
#     TrackedColInsertionFactory,
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
)


class TileScopePack(StrategyPack):
    """Strategy packs for TileScope."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def vertical_insertion_encoding(cls):
        """Vertical insertion encoding strategy pack."""
        return TileScopePack(
            initial_strats=[
                TrackedFactorStrategy(),
                TrackedVerticalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[TrackedRemoveEmptyRowsAndColumnsStrategy()],
            expansion_strats=[[TrackedVerticalInsertionEncodingPlacementFactory()]],
            ver_strats=[AtomStrategy()],
            name="Vertical Insertion Encoding",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def horizontal_insertion_encoding(cls):
        """Horizontal insertion encoding strategy pack."""
        return TileScopePack(
            initial_strats=[
                TrackedFactorStrategy(),
                TrackedHorizontalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[TrackedRemoveEmptyRowsAndColumnsStrategy()],
            expansion_strats=[[TrackedHorizontalInsertionEncodingPlacementFactory()]],
            ver_strats=[AtomStrategy()],
            name="Horizontal Insertion Encoding",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_placement(cls):
        """Point placements strategy pack."""
        return TileScopePack(
            inferral_strats=[
                TrackedRemoveEmptyRowsAndColumnsStrategy(),
                TrackedLessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                TrackedFactorStrategy(),
                TrackedLessThanOrEqualRowColSeparationStrategy(),
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
            name="Point Placement",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_placements_shuffle(cls):
        """Point placements with shuffle strategy pack."""
        return TileScopePack(
            initial_strats=[
                TrackedShuffleFactorStrategy(),
                TrackedLessThanOrEqualRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            inferral_strats=[
                TrackedRemoveEmptyRowsAndColumnsStrategy(),
                TrackedLessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [CellInsertionFactory(), TrackedPointPlacementFactory()]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="Point Placements Shuffle",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_placement_fusion_point_row(cls):
        """Point placements strategy pack with fusion of point rows."""
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
            name="Point Placement with Fusion of Point Rows",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_placement_subclass_ver_strat(cls, root: TrackedTiling):
        """Point placements strategy pack."""
        return TileScopePack(
            inferral_strats=[
                TrackedRemoveEmptyRowsAndColumnsStrategy(),
                TrackedLessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                TrackedFactorStrategy(),
                TrackedLessThanOrEqualRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    CellInsertionFactory(),
                    TrackedPointPlacementFactory(),
                    # RowInsertionFactory(),
                    # TrackedColInsertionFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                SubclassVerificationStrategy(root),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="Point Placement with subclass verification",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_placement_initial_place_points(cls):
        """Point placements strategy pack, place points initially."""
        return TileScopePack(
            inferral_strats=[
                TrackedRemoveEmptyRowsAndColumnsStrategy(),
                TrackedLessThanRowColSeparationStrategy(),
                TrackedPointPlacementFactory(),
            ],  # Iterable[Strategy]
            initial_strats=[
                TrackedFactorStrategy(),
                TrackedLessThanOrEqualRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    CellInsertionFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="Point Placement initially place points",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_placement_initial_cell_insertion(cls):
        """Point placements strategy pack with cell insertion
        as an initial strategy."""
        return TileScopePack(
            inferral_strats=[
                TrackedRemoveEmptyRowsAndColumnsStrategy(),
                TrackedLessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                TrackedFactorStrategy(),
                TrackedLessThanOrEqualRowColSeparationStrategy(),
                CellInsertionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    TrackedPointPlacementFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="Point Placement, initial cell insertion",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_placements_shuffle_initial_cell_insertion(cls):
        """Point placements with shuffle strategy pack with cell
        insertion as an initial strategy.."""
        return TileScopePack(
            initial_strats=[
                TrackedFactorStrategy(),
                TrackedLessThanOrEqualRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            inferral_strats=[
                TrackedRemoveEmptyRowsAndColumnsStrategy(),
                TrackedLessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [CellInsertionFactory(), TrackedPointPlacementFactory()]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="Point Placements Shuffle, initial cell insertion",
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
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    RowInsertionFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="Row Placement",
            symmetries=[],
            iterative=False,
        )

    # def make_fusion(
    #     self,
    #     point_rows: bool = False,
    #     apply_first: bool = False,
    # ) -> "TileScopePack":
    #     """
    #     Create a new pack by adding fusion to the current pack.

    #     If point_rows, it will add point rows fusion.
    #     If apply_first, it will add fusion to the front of the initial strategies.
    #     """
    #     name = (
    #         self.name + " with point row fusion"
    #         if point_rows
    #         else self.name + " with fusion"
    #     )
    #     fusion_strat = (
    #         TrackedFusionPointRowFactory() if point_rows else TrackedFusionFactory()
    #     )
    #     pack = self.add_initial(fusion_strat, name, apply_first=apply_first)
    #     return pack

    @classmethod
    def col_placement_fusion(cls):
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
                # VerticalInsertionEncodableVerificationStrategy(),
                # HorizontalInsertionEncodableVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="Column Placement with Fusion",
            symmetries=[],
            iterative=False,
        )

    # @classmethod
    # def row_and_col_placement(cls):
    #     """Point placements strategy pack."""
    #     return TileScopePack(
    #         inferral_strats=[
    #             TrackedRemoveEmptyRowsAndColumnsStrategy(),
    #             TrackedLessThanRowColSeparationStrategy(),
    #         ],  # Iterable[Strategy]
    #         initial_strats=[
    #             TrackedFactorStrategy(),
    #             TrackedLessThanOrEqualRowColSeparationStrategy(),
    #         ],  # Iterable[Strategy]
    #         expansion_strats=[
    #             [
    #                 CellInsertionFactory(),
    #                 RowInsertionFactory(),
    #                 TrackedColInsertionFactory(),
    #             ]
    #         ],  # Iterable[Iterable[Strategy]]
    #         ver_strats=[
    #             AtomStrategy(),
    #             VerticalInsertionEncodableVerificationStrategy(),
    #             HorizontalInsertionEncodableVerificationStrategy(),
    #         ],  # Iterable[Strategy]
    #         name="Row and Column Placement",
    #         symmetries=[],
    #         iterative=False,
    #     )

    # @classmethod
    # def point_row_and_col_placement(cls):
    #     """Point, row and column placements strategy pack."""
    #     return TileScopePack(
    #         inferral_strats=[
    #             TrackedRemoveEmptyRowsAndColumnsStrategy(),
    #             TrackedLessThanRowColSeparationStrategy(),
    #         ],  # Iterable[Strategy]
    #         initial_strats=[
    #             TrackedFactorStrategy(),
    #             TrackedLessThanOrEqualRowColSeparationStrategy(),
    #         ],  # Iterable[Strategy]
    #         expansion_strats=[
    #             [
    #                 CellInsertionFactory(),
    #                 TrackedPointPlacementFactory(),
    #                 RowInsertionFactory(),
    #                 TrackedColInsertionFactory(),
    #             ]
    #         ],  # Iterable[Iterable[Strategy]]
    #         ver_strats=[
    #             AtomStrategy(),
    #             VerticalInsertionEncodableVerificationStrategy(),
    #             HorizontalInsertionEncodableVerificationStrategy(),
    #         ],  # Iterable[Strategy]
    #         name="Point, Row and Column Placement",
    #         symmetries=[],
    #         iterative=False,
    #     )

    # @classmethod
    # def row_placement_initial_cell_insertion(cls):
    #     """Row placements strategy pack with cell insertion
    #     as an initial strategy."""
    #     return TileScopePack(
    #         inferral_strats=[
    #             TrackedRemoveEmptyRowsAndColumnsStrategy(),
    #             TrackedLessThanRowColSeparationStrategy(),
    #         ],  # Iterable[Strategy]
    #         initial_strats=[
    #             TrackedFactorStrategy(),
    #             TrackedLessThanOrEqualRowColSeparationStrategy(),
    #             CellInsertionFactory(),
    #         ],  # Iterable[Strategy]
    #         expansion_strats=[
    #             [
    #                 RowInsertionFactory(),
    #             ]
    #         ],  # Iterable[Iterable[Strategy]]
    #         ver_strats=[
    #             AtomStrategy(),
    #             VerticalInsertionEncodableVerificationStrategy(),
    #             HorizontalInsertionEncodableVerificationStrategy(),
    #         ],  # Iterable[Strategy]
    #         name="Row Placement with Cell Insertion initially",
    #         symmetries=[],
    #         iterative=False,
    #     )

    # @classmethod
    # def col_placement_initial_cell_insertion(cls):
    #     """Column placements strategy pack with cell insertion
    #     as an initial strategy."""
    #     return TileScopePack(
    #         inferral_strats=[
    #             TrackedRemoveEmptyRowsAndColumnsStrategy(),
    #             TrackedLessThanRowColSeparationStrategy(),
    #         ],  # Iterable[Strategy]
    #         initial_strats=[
    #             TrackedFactorStrategy(),
    #             TrackedLessThanOrEqualRowColSeparationStrategy(),
    #             CellInsertionFactory(),
    #         ],  # Iterable[Strategy]
    #         expansion_strats=[
    #             [
    #                 TrackedColInsertionFactory(),
    #             ]
    #         ],  # Iterable[Iterable[Strategy]]
    #         ver_strats=[
    #             AtomStrategy(),
    #             VerticalInsertionEncodableVerificationStrategy(),
    #             HorizontalInsertionEncodableVerificationStrategy(),
    #         ],  # Iterable[Strategy]
    #         name="Column Placement with Cell Insertion initially",
    #         symmetries=[],
    #         iterative=False,
    #     )

    # @classmethod
    # def row_and_col_placement_initial_cell_insertion(cls):
    #     """Point placements strategy pack with cell insertion
    #     as an initial strategy."""
    #     return TileScopePack(
    #         inferral_strats=[
    #             TrackedRemoveEmptyRowsAndColumnsStrategy(),
    #             TrackedLessThanRowColSeparationStrategy(),
    #         ],  # Iterable[Strategy]
    #         initial_strats=[
    #             TrackedFactorStrategy(),
    #             TrackedLessThanOrEqualRowColSeparationStrategy(),
    #             CellInsertionFactory(),
    #         ],  # Iterable[Strategy]
    #         expansion_strats=[
    #             [
    #                 RowInsertionFactory(),
    #                 TrackedColInsertionFactory(),
    #             ]
    #         ],  # Iterable[Iterable[Strategy]]
    #         ver_strats=[
    #             AtomStrategy(),
    #             VerticalInsertionEncodableVerificationStrategy(),
    #             HorizontalInsertionEncodableVerificationStrategy(),
    #         ],  # Iterable[Strategy]
    #         name="Row and Column Placement with Cell Insertion initially",
    #         symmetries=[],
    #         iterative=False,
    #     )

    # @classmethod
    # def point_row_and_col_placement_initial_cell_insertion(cls):
    #     """Point, row and column placements strategy pack with cell insertion
    #     as an initial strategy."""
    #     return TileScopePack(
    #         inferral_strats=[
    #             TrackedRemoveEmptyRowsAndColumnsStrategy(),
    #             TrackedLessThanRowColSeparationStrategy(),
    #         ],  # Iterable[Strategy]
    #         initial_strats=[
    #             TrackedFactorStrategy(),
    #             TrackedLessThanOrEqualRowColSeparationStrategy(),
    #             CellInsertionFactory(),
    #         ],  # Iterable[Strategy]
    #         expansion_strats=[
    #             [
    #                 TrackedPointPlacementFactory(),
    #                 RowInsertionFactory(),
    #                 TrackedColInsertionFactory(),
    #             ]
    #         ],  # Iterable[Iterable[Strategy]]
    #         ver_strats=[
    #             AtomStrategy(),
    #             VerticalInsertionEncodableVerificationStrategy(),
    #             HorizontalInsertionEncodableVerificationStrategy(),
    #             SubclassVerificationStrategy(),
    #         ],  # Iterable[Strategy]
    #         name="Point, Row and Column Placement with Cell Insertion initially",
    #         symmetries=[],
    #         iterative=False,
    #     )

    # @classmethod
    # def cell_insertion(cls):
    #     """Cell insertion strategy pack."""
    #     return TileScopePack(
    #         inferral_strats=[],  # Iterable[Strategy]
    #         initial_strats=[],  # Iterable[Strategy]
    #         expansion_strats=[
    #             [
    #                 CellInsertionFactory(),
    #             ]
    #         ],  # Iterable[Iterable[Strategy]]
    #         ver_strats=[AtomStrategy()],  # Iterable[Strategy]
    #         name="Cell Insertion",
    #         symmetries=[],
    #         iterative=False,
    #     )
