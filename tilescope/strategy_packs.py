"""Module containing various strategy packs for running TileScope."""

from comb_spec_searcher import StrategyPack, AtomStrategy
from gridded_cayley_permutations import Tiling
from .strategies import (
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
                FactorStrategy(),
                VerticalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[RemoveEmptyRowsAndColumnsStrategy()],
            expansion_strats=[[VerticalInsertionEncodingPlacementFactory()]],
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
                FactorStrategy(),
                HorizontalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[RemoveEmptyRowsAndColumnsStrategy()],
            expansion_strats=[[HorizontalInsertionEncodingPlacementFactory()]],
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
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
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
            ],  # Iterable[Strategy]
            name="point_placement",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_placement_subclass_ver_strat(cls, root: Tiling):
        """Point placements strategy pack."""
        return TileScopePack(
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    CellInsertionFactory(),
                    PointPlacementFactory(),
                    # RowInsertionFactory(),
                    # ColInsertionFactory(),
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
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
                PointPlacementFactory(),
            ],  # Iterable[Strategy]
            initial_strats=[
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
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
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
                CellInsertionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    PointPlacementFactory(),
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
    def point_placements_shuffle(cls):
        """Point placements with shuffle strategy pack."""
        return TileScopePack(
            initial_strats=[
                ShuffleFactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [CellInsertionFactory(), PointPlacementFactory()]
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
    def point_placements_shuffle_initial_cell_insertion(cls):
        """Point placements with shuffle strategy pack with cell
        insertion as an initial strategy.."""
        return TileScopePack(
            initial_strats=[
                ShuffleFactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [CellInsertionFactory(), PointPlacementFactory()]
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
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
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

    @classmethod
    def col_placement(cls):
        """Column placements strategy pack."""
        return TileScopePack(
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    CellInsertionFactory(),
                    ColInsertionFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="Column Placement",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def row_and_col_placement(cls):
        """Point placements strategy pack."""
        return TileScopePack(
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    CellInsertionFactory(),
                    RowInsertionFactory(),
                    ColInsertionFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="Row and Column Placement",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_row_and_col_placement(cls):
        """Point, row and column placements strategy pack."""
        return TileScopePack(
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    CellInsertionFactory(),
                    PointPlacementFactory(),
                    RowInsertionFactory(),
                    ColInsertionFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="Point, Row and Column Placement",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def row_placement_initial_cell_insertion(cls):
        """Row placements strategy pack with cell insertion
        as an initial strategy."""
        return TileScopePack(
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
                CellInsertionFactory(),
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
            name="Row Placement with Cell Insertion initially",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def col_placement_initial_cell_insertion(cls):
        """Column placements strategy pack with cell insertion
        as an initial strategy."""
        return TileScopePack(
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
                CellInsertionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    ColInsertionFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="Column Placement with Cell Insertion initially",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def row_and_col_placement_initial_cell_insertion(cls):
        """Point placements strategy pack with cell insertion
        as an initial strategy."""
        return TileScopePack(
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
                CellInsertionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    RowInsertionFactory(),
                    ColInsertionFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="Row and Column Placement with Cell Insertion initially",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_row_and_col_placement_initial_cell_insertion(cls):
        """Point, row and column placements strategy pack with cell insertion
        as an initial strategy."""
        return TileScopePack(
            inferral_strats=[
                RemoveEmptyRowsAndColumnsStrategy(),
                LessThanRowColSeparationStrategy(),
            ],  # Iterable[Strategy]
            initial_strats=[
                FactorStrategy(),
                LessThanOrEqualRowColSeparationStrategy(),
                CellInsertionFactory(),
            ],  # Iterable[Strategy]
            expansion_strats=[
                [
                    PointPlacementFactory(),
                    RowInsertionFactory(),
                    ColInsertionFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[
                AtomStrategy(),
                VerticalInsertionEncodableVerificationStrategy(),
                HorizontalInsertionEncodableVerificationStrategy(),
                SubclassVerificationStrategy(),
            ],  # Iterable[Strategy]
            name="Point, Row and Column Placement with Cell Insertion initially",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def cell_insertion(cls):
        """Cell insertion strategy pack."""
        return TileScopePack(
            inferral_strats=[],  # Iterable[Strategy]
            initial_strats=[],  # Iterable[Strategy]
            expansion_strats=[
                [
                    CellInsertionFactory(),
                ]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[AtomStrategy()],  # Iterable[Strategy]
            name="Cell Insertion",
            symmetries=[],
            iterative=False,
        )
