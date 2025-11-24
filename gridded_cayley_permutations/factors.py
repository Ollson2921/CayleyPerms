"""
This module contains the Factors class, which contains methods for finding the factors of a tiling.
"""

from itertools import chain, combinations
from functools import cached_property

from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import GriddedCayleyPerm

from .tilings import Tiling


class Factors:
    """
    This class contains methods for finding the factors of a tiling.

    A factor is a subtiling determined by cells.

    Two cells are in the same factor if
    - they are in the same row or column (excluding point row) or
    - there is an obstruction or requirement that connects them.
    """

    def __init__(self, tiling: Tiling) -> None:
        self.tiling = tiling
        self.cells = list(sorted(self.tiling.active_cells))
        self.cells_dict = {cell: cell for cell in self.cells}

    def combine_cells_in_row_or_col(self) -> None:
        """Combines cells that are in the same column or row unless in a point row."""
        cells = self.cells
        for cell, cell2 in combinations(cells, 2):
            if cell[0] == cell2[0] or (
                cell[1] == cell2[1] and cell[1] not in self.tiling.point_rows
            ):
                self.combine_cells(cell, cell2)

    def combine_cells(self, cell, cell2) -> None:
        """Combines two cells in the dictionary cells_dict."""
        cells_dict = self.cells_dict
        if cells_dict[cell] != cells_dict[cell2]:
            to_change = cells_dict[cell2]
            for key, val in cells_dict.items():
                if val == to_change:
                    cells_dict[key] = cells_dict[cell]

    def combine_cells_in_obs_and_reqs(self) -> None:
        """Combine cells with respect to obstructions and requirements.

        TODO: make function for the copied code (from find_factors in gridded_cayley_permutations.)
        """
        for gcp in self.tiling.obstructions:
            if not self.point_row_ob(gcp):
                for cell, cell2 in combinations((gcp.find_active_cells()), 2):
                    self.combine_cells(cell, cell2)
        for cell, cell2 in chain.from_iterable(
            combinations(
                chain.from_iterable(req.find_active_cells() for req in req_list), 2
            )
            for req_list in self.tiling.requirements
        ):
            self.combine_cells(cell, cell2)

    def point_row_ob(self, ob: GriddedCayleyPerm) -> bool:
        """
        Return true if the obstruction is a size 2 obstruction
        fully contained in a point row of the tiling.
        """
        return (
            ob.pattern in (CayleyPermutation([0, 1]), CayleyPermutation([1, 0]))
            and ob.positions[0][1] == ob.positions[1][1]
            and ob.positions[0][1] in self.tiling.point_rows
        )

    def find_factors(self) -> tuple[Tiling, ...]:
        """Return the factors of the tiling."""
        factors = self.find_factors_as_cells
        return tuple(
            self.tiling.sub_tiling(factor, simplify=False) for factor in factors
        )

    def rgf_find_factors(self):
        """Find factors for RGF."""
        for cell in self.tiling.active_cells - self.tiling.point_cells():
            for cell2 in self.tiling.active_cells - self.tiling.point_cells():
                self.combine_cells(cell, cell2)
        return self.find_factors()

    @cached_property
    def find_factors_as_cells(self) -> tuple[tuple[tuple[int, int], ...], ...]:
        """Return the factors of the tiling as cells."""
        self.combine_cells_in_row_or_col()
        self.combine_cells_in_obs_and_reqs()
        factors = []
        for val in set(self.cells_dict.values()):
            factor = []
            for cell in self.cells:
                if self.cells_dict[cell] == val:
                    factor.append(cell)
            factors.append(factor)
        return tuple(sorted(tuple(sorted(f)) for f in factors))


class ShuffleFactors(Factors):
    """
    Return the interleaving factors, which drops the condition
    of cells being in the same row or column.

    This is structurally sound, but no longer counted by Cartesian products.
    """

    def combine_cells_in_row_or_col(self) -> None:
        """Don't combine them!"""

    def combine_cells_in_obs_and_reqs(self) -> None:
        for gcp in self.tiling.obstructions:
            if gcp.pattern != CayleyPermutation([0, 0]):
                for cell, cell2 in combinations((gcp.find_active_cells()), 2):
                    self.combine_cells(cell, cell2)
        for cell, cell2 in chain.from_iterable(
            combinations(
                chain.from_iterable(req.find_active_cells() for req in req_list), 2
            )
            for req_list in self.tiling.requirements
        ):
            self.combine_cells(cell, cell2)
