"""Strategy for verifying when a tiling is insertion encodable."""

from typing import TypeVar
from gridded_cayley_permutations import Tiling
from tilescope.strategies import (
    VerticalInsertionEncodableVerificationStrategy,
    HorizontalInsertionEncodableVerificationStrategy,
)

HorizontalInsertionEncodableVerificationStrategyT = TypeVar(
    "HorizontalInsertionEncodableVerificationStrategyT",
    bound="HorizontalInsertionEncodableVerificationStrategy",
)

VerticalInsertionEncodableVerificationStrategyT = TypeVar(
    "VerticalInsertionEncodableVerificationStrategyT",
    bound="VerticalInsertionEncodableVerificationStrategy",
)


class TrackedHorizontalInsertionEncodableVerificationStrategy(
    HorizontalInsertionEncodableVerificationStrategy
):

    def pack(self, comb_class: Tiling):
        # pylint: disable=import-outside-toplevel
        # pylint: disable=cyclic-import
        from clouds.tracked_tilescope import TileScopePack

        return TileScopePack.horizontal_ins_enc()


class TrackedVerticalInsertionEncodableVerificationStrategy(
    VerticalInsertionEncodableVerificationStrategy
):
    """
    A strategy for verifying if a tiling is vertical insertion encodable.
    """

    def pack(self, comb_class: Tiling):
        # pylint: disable=import-outside-toplevel
        # pylint: disable=cyclic-import
        from clouds.tracked_tilescope import TileScopePack

        return TileScopePack.vertical_ins_enc()
