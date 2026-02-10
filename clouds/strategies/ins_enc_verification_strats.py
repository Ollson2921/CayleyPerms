"""Strategy for verifying when a tiling is insertion encodable."""

from gridded_cayley_permutations import Tiling
from tilescope.strategies import (
    VerticalInsertionEncodableVerificationStrategy,
    HorizontalInsertionEncodableVerificationStrategy,
)


class TrackedHorizontalInsertionEncodableVerificationStrategy(
    HorizontalInsertionEncodableVerificationStrategy
):
    """A strategy for verifying if a tiling is horizontal insertion encodable."""

    def pack(self, comb_class: Tiling):
        # pylint: disable=import-outside-toplevel
        # pylint: disable=cyclic-import
        from clouds.tracked_tilescope import TrackedTileScopePack

        return TrackedTileScopePack.horizontal_ins_enc()


class TrackedVerticalInsertionEncodableVerificationStrategy(
    VerticalInsertionEncodableVerificationStrategy
):
    """
    A strategy for verifying if a tiling is vertical insertion encodable.
    """

    def pack(self, comb_class: Tiling):
        # pylint: disable=import-outside-toplevel
        # pylint: disable=cyclic-import
        from clouds.tracked_tilescope import TrackedTileScopePack

        return TrackedTileScopePack.vertical_ins_enc()
