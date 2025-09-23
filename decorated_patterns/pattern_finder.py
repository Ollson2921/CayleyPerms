"""
Input: a set of words S
Output: a set of Cayley decorated patterns P such that Av(P) = S
"""

from collections import defaultdict
from itertools import chain, combinations
from typing import Iterable, Iterator, Optional

from tqdm import tqdm  # type: ignore

from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import GriddedCayleyPerm
from mesh_patterns.bisc import (
    AbstractPatternFinder,
    AscentSequencePatternFinder,
    CayleyMeshPatternFinder,
    InversionSequencePatternFinder,
    PermutationPatternFinder,
    RestrictedGrowthFunctionPatternFinder,
)

from .decorated_pattern import DecoratedPattern


class DecoratedPatternFinder(AbstractPatternFinder):
    """
    Abstract class for finding decorated patterns that define a set of words.
    """

    def __init__(
        self,
        max_patt_size: int,
        max_obstruction_size: int,
        avoiders: Iterable[tuple[int, ...]],
        containers: Optional[Iterable[tuple[int, ...]]] = None,
    ):
        self.max_obstruction_size = max_obstruction_size
        super().__init__(max_patt_size, avoiders, containers)

    @staticmethod
    def minimal_patterns(patterns: Iterable[DecoratedPattern]) -> set[DecoratedPattern]:
        """
        Returns the set of minimal patterns from the given set of patterns.
        """
        return set(patterns)
        # basis: set[DecoratedPattern] = set()
        # for patt in tqdm(sorted(patterns), desc="Computing minimal patterns"):
        #     if patt.avoids(*basis):
        #         basis.add(patt)
        # return basis

    def find_decorated_basis(self) -> list[DecoratedPattern]:
        """
        Return a list of decorated patterns P such that Av(P) = avoiders
        """
        minimal_patterns_not_contained = self.find_minimal_patterns_avoided()
        patts = self.minimal_patterns(minimal_patterns_not_contained)

        containers = self.all_containers()
        container_labels: dict[tuple[int, ...], int] = {}
        for word in containers:
            container_labels[word] = len(container_labels)

        label_to_patt: dict[int, DecoratedPattern] = {}
        subsets_left = []
        for patt in tqdm(patts, desc="Computing container sets"):
            # do in parallel?
            label = len(label_to_patt)
            label_to_patt[label] = patt
            patt_containers = set(
                container_labels[word]
                for word in containers
                if patt.contained_by_word(word)
            )
            subsets_left.append((label, patt_containers))

        basis_labels = self.set_cover(container_labels.values(), subsets_left)

        return [label_to_patt[label] for label in basis_labels]

    def find_minimal_patterns_avoided(self) -> Iterator[DecoratedPattern]:
        """
        Compute the minimal set of patterns to those contained in avoiders
        """
        maximal_obstruction_sets, classical = (
            self.find_maximal_contained_gridded_cperms()
        )

        for patt in classical:
            yield DecoratedPattern(patt, [])
        for patt, obstructions in tqdm(
            maximal_obstruction_sets.items(), desc="Computing minimal patterns avoided"
        ):
            # Do in parallel?
            ob_sets = [
                frozenset(
                    chain.from_iterable(
                        ob.sub_gridded_cayley_perms(i)
                        for i in range(self.max_patt_size + 1)
                    )
                )
                for ob in obstructions
            ]

            vertices = set()
            edges = set()
            gp_label: dict[GriddedCayleyPerm, int] = {}
            label_gp: dict[int, GriddedCayleyPerm] = {}
            for ob_set in ob_sets:
                edge = []
                for gp in ob_set:
                    if gp not in gp_label:
                        gp_label[gp] = len(gp_label)
                        label_gp[gp_label[gp]] = gp
                        vertices.add(gp_label[gp])
                    edge.append(gp_label[gp])
                edges.add(tuple(sorted(edge)))
            for gp_labels in self.enumerate_hitting_sets(list(vertices), list(edges)):
                obs = [label_gp[v] for v in gp_labels]
                yield DecoratedPattern(patt, obs)

    def find_maximal_contained_gridded_cperms(
        self,
    ) -> tuple[
        defaultdict[CayleyPermutation, set[GriddedCayleyPerm]],
        set[tuple[int, ...]],
    ]:
        """
        Return the maximal sets of obstructions contained in the avoiders, sorted
        by the underlying patterns.
        """
        contained_obstructions: defaultdict[
            CayleyPermutation, set[GriddedCayleyPerm]
        ] = defaultdict(set)
        classical_patterns = set(self.universe_up_to_size(self.max_patt_size))
        ignore = set()
        for word in tqdm(self.all_avoiders(), desc="computing candidate patterns"):
            # do in parallel? Inner loop handled in parent process.
            for cperm, obstructions in self.find_contained_gridded_perms(word).items():
                if cperm in classical_patterns:
                    classical_patterns.remove(cperm)
                if cperm in ignore:
                    continue

                if obstructions == frozenset([GriddedCayleyPerm([], [])]):
                    ignore.add(cperm)
                    if cperm in contained_obstructions:
                        contained_obstructions.pop(cperm)
                    continue

                for gp in obstructions:
                    if gp.avoids(contained_obstructions[cperm]):
                        contained_obstructions[cperm].add(gp)
        return contained_obstructions, classical_patterns

    @staticmethod
    def requirement_implies_requirement(
        req: set[GriddedCayleyPerm] | frozenset[GriddedCayleyPerm],
        other_req: set[GriddedCayleyPerm] | frozenset[GriddedCayleyPerm],
    ) -> bool:
        """Return true if containing req implies containing other req"""
        return all(other_gp.contains(req) for other_gp in other_req)

    def find_contained_gridded_perms(
        self, word: tuple[int, ...]
    ) -> dict[CayleyPermutation, set[GriddedCayleyPerm]]:
        """
        A dictionary is returned with keys being all the classical
        Cayley permutations up to size max_patt_size contained and
        values being all of the gridded permutations contained in the
        complement of an occurrence up to size max_obstruction_size.
        """
        res: defaultdict[CayleyPermutation, set[GriddedCayleyPerm]] = defaultdict(set)
        for i in range(self.max_patt_size + 1):
            for indices in combinations(range(len(word)), i):
                cperm = CayleyPermutation.standardise(word[idx] for idx in indices)
                complement_cperm = CayleyPermutation.standardise(
                    word[idx] for idx in range(len(word)) if idx not in indices
                )
                gridding = DecoratedPattern.gridding_of_occurrence(word, indices)
                complement_gridding = [
                    cell for idx, cell in enumerate(gridding) if idx not in indices
                ]
                gcp = GriddedCayleyPerm(complement_cperm, complement_gridding)
                if gcp.avoids(res[cperm]):
                    res[cperm].add(gcp)
        return res


class AscentSequenceDecoratedPatternFinder(DecoratedPatternFinder):
    """
    Class for finding decorated patterns that define a set of ascent sequences
    """

    @staticmethod
    def universe_of_size(n: int):
        return AscentSequencePatternFinder.universe_of_size(n)


class CayleyDecoratedPatternFinder(DecoratedPatternFinder):
    """
    Class for finding decorated patterns that define a set of Cayley Permutations
    """

    @staticmethod
    def universe_of_size(n: int):
        return CayleyMeshPatternFinder.universe_of_size(n)


class InversionSequenceDecoratedPatternFinder(DecoratedPatternFinder):
    """
    Class for finding decoratedpatterns that define a set of inversion sequences
    """

    @staticmethod
    def universe_of_size(n: int):
        return InversionSequencePatternFinder.universe_of_size(n)


class PermutationDecoratedPatternFinder(DecoratedPatternFinder):
    """
    Class for finding decorated patterns that define a set of permutations
    """

    @staticmethod
    def universe_of_size(n: int):
        return PermutationPatternFinder.universe_of_size(n)


class RestrictedGrowthFunctionDecoratedPatternFinder(DecoratedPatternFinder):
    """
    Class for finding decorated patterns that define a set of restricted
    growth functions
    """

    @staticmethod
    def universe_of_size(n: int):
        return RestrictedGrowthFunctionPatternFinder.universe_of_size(n)
