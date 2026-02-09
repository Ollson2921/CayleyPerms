"""Types for abstract strategies."""

from typing import TypeVar
from gridded_cayley_permutations import Tiling


TilingType = TypeVar("TilingType", bound="Tiling")
