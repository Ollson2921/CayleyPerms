"""Module containing various strategy packs for running TileScope with."""

from comb_spec_searcher import StrategyPack, AtomStrategy
from .strategies import (
    RemoveEmptyRowsAndColumnsStrategy,
    FactorStrategy,
    ShuffleFactorStrategy,
    InsertionEncodingRequirementInsertionFactory,
    InsertionEncodingPlacementFactory,
    CellInsertionFactory,
    PointPlacementFactory,
    LessThanRowColSeparationStrategy,
    LessThanOrEqualRowColSeparationStrategy,
    RowInsertionFactory,
    ColInsertionFactory,
    FusionFactory,
)


class TileScopePack(StrategyPack):
    """A strategy pack for TileScope."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def insertion_encoding(cls):
        """Insertion encoding strategy."""
        return TileScopePack(
            initial_strats=[
                FactorStrategy(),
                InsertionEncodingRequirementInsertionFactory(),
            ],  # Iterable[Strategy]
            inferral_strats=[RemoveEmptyRowsAndColumnsStrategy()],  # Iterable[Strategy]
            expansion_strats=[
                [InsertionEncodingPlacementFactory()]
            ],  # Iterable[Iterable[Strategy]]
            ver_strats=[AtomStrategy()],  # Iterable[Strategy]
            name="Insertion Encoding",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_placement(cls):
        """Point placements strategy."""
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
            ver_strats=[AtomStrategy()],  # Iterable[Strategy]
            name="Point Placement",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_placements_shuffle(cls):
        """Point placements with shuffle strategy."""
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
            ver_strats=[AtomStrategy()],  # Iterable[Strategy]
            name="Point Placements Shuffle",
            symmetries=[],
            iterative=False,
        )
