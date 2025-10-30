"""Imports all of the strategies."""

from .requirement_insertions import (
    RequirementInsertionStrategy,
    VerticalInsertionEncodingRequirementInsertionFactory,
    HorizontalInsertionEncodingRequirementInsertionFactory,
    CellInsertionFactory,
)
from .point_placements import (
    RequirementPlacementStrategy,
    VerticalInsertionEncodingPlacementFactory,
    HorizontalInsertionEncodingPlacementFactory,
    PointPlacementFactory,
    RowInsertionFactory,
    ColInsertionFactory,
)
from .remove_empty_rows_and_cols import RemoveEmptyRowsAndColumnsStrategy
from .factor import FactorStrategy, ShuffleFactorStrategy
from .row_column_separation import (
    LessThanRowColSeparationStrategy,
    LessThanOrEqualRowColSeparationStrategy,
)
from .subclass_verification import SubclassVerificationStrategy

from .fusion import FusionFactory, FusionStrategy

__all__ = (
    "RequirementInsertionStrategy",
    "VerticalInsertionEncodingRequirementInsertionFactory",
    "HorizontalInsertionEncodingRequirementInsertionFactory",
    "CellInsertionFactory",
    "RequirementPlacementStrategy",
    "VerticalInsertionEncodingPlacementFactory",
    "HorizontalInsertionEncodingPlacementFactory",
    "PointPlacementFactory",
    "RowInsertionFactory",
    "CellInsertionFactory",
    "ColInsertionFactory",
    "RemoveEmptyRowsAndColumnsStrategy",
    "FactorStrategy",
    "ShuffleFactorStrategy",
    "LessThanOrEqualRowColSeparationStrategy",
    "LessThanRowColSeparationStrategy",
    "FusionFactory",
    "FusionStrategy",
    "SubclassVerificationStrategy",
)
