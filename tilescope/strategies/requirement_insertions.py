"""Strategies and factories for inserting points of a requirement into a tiling."""

from typing import Dict, Iterable, Iterator, Optional, Tuple
from itertools import product
from comb_spec_searcher import DisjointUnionStrategy, StrategyFactory

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation, Av
from .factor import TilingT

Cell = Tuple[int, int]


class AbstractRequirementInsertionStrategy(
    DisjointUnionStrategy[TilingT, GriddedCayleyPerm]
):
    """Insert a point of a requirement."""

    def __init__(self, gcps: Iterable[GriddedCayleyPerm], ignore_parent: bool = False):
        super().__init__(ignore_parent=ignore_parent)
        self.gcps = frozenset(gcps)

    def formal_step(self):
        return f"Either avoid or contain {self.gcps}"

    def backward_map(
        self,
        comb_class: TilingT,
        objs: Tuple[Optional[GriddedCayleyPerm], ...],
        children: Optional[Tuple[TilingT, ...]] = None,
    ) -> Iterator[GriddedCayleyPerm]:
        raise NotImplementedError

    def forward_map(
        self,
        comb_class: TilingT,
        obj: GriddedCayleyPerm,
        children: Optional[Tuple[TilingT, ...]] = None,
    ) -> Tuple[Optional[GriddedCayleyPerm], ...]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, d: dict) -> "AbstractRequirementInsertionStrategy":
        gcps = tuple(GriddedCayleyPerm.from_dict(gcp) for gcp in d.pop("gcps"))
        return cls(gcps=gcps, **d)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(" f"ignore_parent={self.ignore_parent})"

    def to_jsonable(self) -> dict:
        """Return a dictionary form of the strategy."""
        d: dict = super().to_jsonable()
        d.pop("workable")
        d.pop("inferrable")
        d.pop("possibly_empty")
        d["gcps"] = [gcp.to_jsonable() for gcp in self.gcps]
        return d


class RequirementInsertionStrategy(AbstractRequirementInsertionStrategy[Tiling]):
    """Insert a point of a requirement into a tiling."""

    def decomposition_function(self, comb_class: Tiling) -> Tuple[Tiling, ...]:
        return (
            comb_class.add_obstructions(self.gcps),
            comb_class.add_requirement_list(self.gcps),
        )

    def extra_parameters(
        self, comb_class: Tiling, children: Optional[Tuple[Tiling, ...]] = None
    ) -> Tuple[Dict[str, str], ...]:
        return tuple({} for _ in self.decomposition_function(comb_class))


class VerticalInsertionEncodingRequirementInsertionFactory(StrategyFactory[Tiling]):
    """Factory for creating RequirementInsertionStrategy to make columns positive
    for the vertical insertion encoding."""

    def __call__(self, comb_class: Tiling) -> Iterator[RequirementInsertionStrategy]:
        for col in range(comb_class.dimensions[0]):
            if not comb_class.col_is_positive(col):
                gcps = tuple(
                    GriddedCayleyPerm(CayleyPermutation([0]), [cell])
                    for cell in comb_class.cells_in_col(col)
                )
                strategy = RequirementInsertionStrategy(gcps, ignore_parent=True)
                yield strategy
                return

    @classmethod
    def from_dict(
        cls, d: dict
    ) -> "VerticalInsertionEncodingRequirementInsertionFactory":
        return cls(**d)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return "Make columns positive"


class HorizontalInsertionEncodingRequirementInsertionFactory(StrategyFactory[Tiling]):
    """Factory for creating RequirementInsertionStrategy to make rows positive
    for the horizontal insertion encoding."""

    def __call__(self, comb_class: Tiling) -> Iterator[RequirementInsertionStrategy]:
        for row in range(comb_class.dimensions[1]):
            if not comb_class.row_is_positive(row):
                gcps = tuple(
                    GriddedCayleyPerm(CayleyPermutation([0]), [cell])
                    for cell in comb_class.cells_in_row(row)
                )
                strategy = RequirementInsertionStrategy(gcps, ignore_parent=True)
                yield strategy

    @classmethod
    def from_dict(
        cls, d: dict
    ) -> "HorizontalInsertionEncodingRequirementInsertionFactory":
        return cls(**d)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return "Make rows positive"


class AbstractCellInsertionFactory(StrategyFactory[TilingT]):
    """
    The cell insertion strategy.

    The cell insertion strategy is a disjoint union strategy.
    For each active cell, the strategy considers all patterns (up to some maximum
    length given by `maxreqlen`) and returns two tilings; one which requires the
    pattern in the cell and one where the pattern is obstructed.

    The one_cell_only flag will ensure that the strategy only inserts into the
    'smallest' non-positive cell. This is used for 'insertion' packs where
    we are intending to make every cell positive, so with this setting we have
    a unique path to the fully positive tilings.
    """

    def __init__(
        self,
        maxreqlen: int = 1,
        ignore_parent: bool = False,
        one_cell_only: bool = False,
    ) -> None:
        self.ignore_parent = ignore_parent
        self.maxreqlen = maxreqlen
        self.one_cell_only = one_cell_only

    def req_lists_to_insert(
        self, tiling: TilingT
    ) -> Iterator[Tuple[GriddedCayleyPerm, ...]]:
        """Yields all requirement lists to insert into the tiling."""
        if self.one_cell_only:
            assert self.maxreqlen == 1 and self.ignore_parent
            cells = sorted(tiling.active_cells - tiling.positive_cells())
            if cells:
                yield (
                    GriddedCayleyPerm.create_gcp_in_cell(
                        CayleyPermutation((0,)), cells[0]
                    ),
                )
            return
        active_cells = tiling.active_cells
        bdict = tiling.cell_basis
        for cell, length in product(active_cells, range(1, self.maxreqlen + 1)):
            basis = bdict[cell][0]
            patterns = (
                Av(basis).generate_cperms(length)
                if basis
                else CayleyPermutation.of_size(length)
            )
            yield from (
                (GriddedCayleyPerm.create_gcp_in_cell(patt, cell),)
                for patt in patterns
                if not any(patt in cperm for cperm in bdict[cell][1])
            )

    def to_jsonable(self) -> dict:
        d: dict = super().to_jsonable()
        d["one_cell_only"] = self.one_cell_only
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "AbstractCellInsertionFactory":
        return cls(**d)

    def __str__(self) -> str:
        if self.maxreqlen == 1:
            return "point insertion"
        return f"cell insertion up to length {self.maxreqlen}"

    def __repr__(self) -> str:
        args = ", ".join(
            [
                f"maxreqlen={self.maxreqlen}",
                f"ignore_parent={self.ignore_parent}",
                f"one_cell_only={self.one_cell_only}",
            ]
        )
        return f"{self.__class__.__name__}({args})"


class CellInsertionFactory(AbstractCellInsertionFactory[Tiling]):
    """
    The cell insertion strategy.

    The cell insertion strategy is a disjoint union strategy.
    For each active cell, the strategy considers all patterns (up to some maximum
    length given by `maxreqlen`) and returns two tilings; one which requires the
    pattern in the cell and one where the pattern is obstructed.

    The one_cell_only flag will ensure that the strategy only inserts into the
    'smallest' non-positive cell. This is used for 'insertion' packs where
    we are intending to make every cell positive, so with this setting we have
    a unique path to the fully positive tilings.
    """

    def __call__(self, comb_class: Tiling) -> Iterator[RequirementInsertionStrategy]:
        """
        Iterator over all the requirement insertion rules.
        """
        for req_list in self.req_lists_to_insert(comb_class):
            yield RequirementInsertionStrategy(req_list, self.ignore_parent)
