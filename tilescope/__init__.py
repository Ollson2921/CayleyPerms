"""
A package for finding combinatorial specifications
for Cayley permutation classes
"""

from .searcher import TileScope
from .strategy_packs import TileScopePack

__all__ = ("TileScope", "TileScopePack")
