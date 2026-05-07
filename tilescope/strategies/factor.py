"""Factors the tiling into sections that are independent of each other."""

import abc
from typing import Dict, Iterator, Optional, Tuple
from comb_spec_searcher import CartesianProductStrategy, Strategy
from comb_spec_searcher.exception import StrategyDoesNotApply
from comb_spec_searcher.strategies.constructor import Constructor
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.factors import Factors, ShuffleFactors
from gridded_cayley_permutations.point_placements import TilingT


class AbstractFactorStrategy(CartesianProductStrategy[TilingT, GriddedCayleyPerm]):
    """Abstract strategy for factoring a tiling."""

    def __init__(
        self,
        ignore_parent: bool = True,
        workable: bool = True,
    ):
        super().__init__(
            ignore_parent=ignore_parent, workable=workable, inferrable=True
        )

    def extra_parameters(
        self, comb_class: TilingT, children: Optional[Tuple[TilingT, ...]] = None
    ) -> Tuple[Dict[str, str], ...]:
        if children is None:
            children = self.decomposition_function(comb_class)
            if children is None:
                raise StrategyDoesNotApply("Strategy does not apply")
        return tuple({} for _ in children)

    def formal_step(self) -> str:
        return "Factor the tiling into factors"

    def backward_map(
        self,
        comb_class: TilingT,
        objs: Tuple[Optional[GriddedCayleyPerm], ...],
        children: Optional[Tuple[TilingT, ...]] = None,
    ) -> Iterator[GriddedCayleyPerm]:
        if children is None:
            children = self.decomposition_function(comb_class)
        # find preimages of objs mapping from factors in children to com_class, combine in all possible ways
        preimage_objs = []
        for gcps, factor in zip(objs, self.algorithm(comb_class).find_factors_as_cells):
            add_to_len = min(cell[0] for cell in factor)
            add_to_val = min(cell[1] for cell in factor)
            preimage_gcps = []
            for gcp in gcps:
                preimage_gcp = gcp.add_to_positions(add_to_len, add_to_val)
                preimage_gcps.append(preimage_gcp)
            preimage_objs.append(tuple(preimage_gcps))
        raise NotImplementedError("TODO: combine preimage_objs in all possible ways")

    def forward_map(
        self,
        comb_class: TilingT,
        obj: GriddedCayleyPerm,
        children: Optional[Tuple[TilingT, ...]] = None,
    ) -> Tuple[GriddedCayleyPerm, ...]:
        if children is None:
            children = self.decomposition_function(comb_class)
        return tuple(
            obj.sub_gridded_cayley_perm(factor)
            for factor in self.algorithm(comb_class).find_factors_as_cells
        )

    @abc.abstractmethod
    def algorithm(self, comb_class: TilingT) -> Factors:
        """Return the factor algorithm for the tiling."""

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"ignore_parent={self.ignore_parent}, "
            f"workable={self.workable})"
        )

    # JSON methods

    def to_jsonable(self) -> dict:
        """Return a dictionary form of the strategy."""
        d: dict = super().to_jsonable()
        d.pop("inferrable")
        d.pop("possibly_empty")
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "AbstractFactorStrategy":
        return cls(**d)


class FactorStrategy(AbstractFactorStrategy[Tiling]):
    """Factors the tiling into sections that are independent of each other."""

    def algorithm(self, comb_class: Tiling) -> Factors:
        return Factors(comb_class)

    def decomposition_function(self, comb_class: Tiling) -> Tuple[Tiling, ...]:
        factors = self.algorithm(comb_class).find_factors()
        if len(factors) == 1:
            raise StrategyDoesNotApply("Strategy does not apply")
        return factors


class AbstractShuffleFactorStrategy(
    AbstractFactorStrategy[TilingT],
    Strategy[TilingT, GriddedCayleyPerm],
):
    """Abstract strategy for finding shuffle factors."""

    def constructor(
        self, comb_class: TilingT, children: Tuple[TilingT, ...] | None = None
    ) -> Constructor:
        """TODO: shouldn't be catesian product"""
        raise NotImplementedError

    def can_be_equivalent(self) -> bool:
        return True

    def is_reversible(self, comb_class: TilingT) -> bool:
        return False

    def is_two_way(self, comb_class: TilingT) -> bool:
        return False

    def reverse_constructor(
        self,
        idx: int,
        comb_class: TilingT,
        children: Tuple[TilingT, ...] | None = None,
    ) -> Constructor:
        """TODO: shouldn't be catesian product"""
        raise NotImplementedError

    def shifts(
        self, comb_class: TilingT, children: Optional[Tuple[TilingT, ...]] = None
    ) -> Tuple[int, ...]:
        if children is None:
            children = self.decomposition_function(comb_class)
        if children is None:
            raise StrategyDoesNotApply("Strategy does not apply")
        min_sizes = tuple(child.minimum_size_of_object() for child in children)
        point_sum = sum(min_sizes)
        return tuple(point_sum - min_size for min_size in min_sizes)


class ShuffleFactorStrategy(FactorStrategy, Strategy[Tiling, GriddedCayleyPerm]):
    """Strategy for finding shuffle factors."""

    def decomposition_function(self, comb_class: Tiling) -> Tuple[Tiling, ...]:
        if 1 not in comb_class.dimensions:
            raise StrategyDoesNotApply(
                "Tiling is not a row or column shuffle of factors."
            )
        factors = ShuffleFactors(comb_class).find_factors()
        if len(factors) == 1:
            raise StrategyDoesNotApply
        return factors
