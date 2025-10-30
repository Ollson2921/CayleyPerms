"""Module containing various strategy packs for running TileScope."""

from comb_spec_searcher import StrategyPack, AtomStrategy
from gridded_cayley_permutations import Tiling
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
    SubclassVerificationStrategy,
)


class TileScopePack(StrategyPack):
    """Strategy packs for TileScope."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def insertion_encoding(cls):
        """Insertion encoding strategy pack."""
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
            ],  # Iterable[Strategy]
            name="Point Placement",
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
