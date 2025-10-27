"""Package for checking when different types of insertion encoding
on Cayley permutations, restricted growth functions and restricted
growth functions of mapplings are regular."""

from .check_regular_vert import regular_vertical_insertion_encoding
from .check_regular_hori import (
    regular_horizontal_insertion_encoding,
)

__all__ = [
    "regular_vertical_insertion_encoding",
    "regular_horizontal_insertion_encoding",
]
