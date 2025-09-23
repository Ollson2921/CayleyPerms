"""
An implementation of the BiSC algorithm.

Input: a set of words S
Output: a set of Cayley mesh patterns P such that Av(P) = S
"""

import abc
from collections import defaultdict
from itertools import combinations, permutations, product
from typing import Iterable, Iterator, Optional

from logzero import logger  # type: ignore
from tqdm import tqdm  # type: ignore

from cayley_permutations import CayleyPermutation

from .mesh_patts import MeshPattern


class AbstractPatternFinder(abc.ABC):
    """
    Abstract class for finding patterns that define a set of words.
    """

    def __init__(
        self,
        max_patt_size: int,
        avoiders: Iterable[tuple[int, ...]],
        containers: Optional[Iterable[tuple[int, ...]]] = None,
    ):
        self.max_patt_size = max_patt_size
        self.avoiders: defaultdict[int, set[tuple[int, ...]]] = defaultdict(set)
        self.containers: defaultdict[int, set[tuple[int, ...]]] = defaultdict(set)
        for word in avoiders:
            self.avoiders[len(word)].add(word)
        if containers is not None:
            for word in containers:
                self.containers[len(word)].add(word)
        else:
            for i in range(max(self.avoiders.keys()) + 1):
                self.containers[i] = set(self.universe_of_size(i) - self.avoiders[i])

    @staticmethod
    @abc.abstractmethod
    def universe_of_size(n: int) -> frozenset[tuple[int, ...]]:
        """
        Returns the set of all words of size n.
        """
        raise NotImplementedError

    def universe_up_to_size(self, n: int) -> frozenset[tuple[int, ...]]:
        """
        Returns the set of all words of size less than or equal to n.
        """
        return frozenset().union(*(self.universe_of_size(i) for i in range(n + 1)))

    def all_avoiders(self, start: int = 0) -> list[tuple[int, ...]]:
        """
        Returns all avoiders of size greater than or equal to start.
        """
        return sorted(
            frozenset().union(
                *(self.avoiders[i] for i in range(start, max(self.avoiders.keys()) + 1))
            ),
            key=len,
        )

    def all_containers(self) -> frozenset[tuple[int, ...]]:
        """
        Returns all containers.
        """
        return frozenset().union(*(self.containers[i] for i in self.containers))

    @staticmethod
    def enumerate_hitting_sets(
        vertices: list[int],
        edges: list[tuple[int, ...]],
        non_vertices: Optional[list[int]] = None,
    ) -> list[set[int]]:
        """
        Find hitting sets

        https://esham.io/files/2012/09/olympic-colors/pkbuch-chap1.pdf
        page 16 - Algorithm 1.4, don't care about k here.
        """
        # edges.sort(key=lambda x: len(x))
        if non_vertices is None:
            non_vertices = []
        if not edges:
            return [set(non_vertices)]
        res = []
        edge = edges[0]
        for v in edge:
            new_vertices = vertices.copy()
            new_vertices.remove(v)
            new_edges = list(e for e in edges[1:] if v not in e)
            new_non_vertices = non_vertices + [v]
            res.extend(
                AbstractPatternFinder.enumerate_hitting_sets(
                    new_vertices, new_edges, new_non_vertices
                )
            )
        return res

    @staticmethod
    def set_cover(
        universe: Iterable[int], subsets_left: list[tuple[int, set[int]]]
    ) -> list[int]:
        """
        Greedy algorithm:
        https://pages.cs.wisc.edu/~shuchi/courses/880-S07/scribe-notes/lecture03.pdf
        algorithm 3.1.4 and theorem 3.1.5 say that this is ln(n/OPT) approximation
        see algorithm 3.1.7 for ln(n) approximation - sort subsets by percentage of
        subset not yet covered
        """
        left = set(universe)
        res = []
        while subsets_left:
            subsets_left.sort(key=lambda x: len(x[1]))
            label, subset = subsets_left.pop()
            res.append(label)
            left -= subset
            subsets_left = [
                (label, old_subset - subset) for label, old_subset in subsets_left
            ]
            subsets_left = [(label, subset) for label, subset in subsets_left if subset]
        if not left:
            return res
        raise ValueError("No basis found, try increasing input parameters")


class MeshPatternFinder(AbstractPatternFinder):
    """
    Abstract class for finding a set of mesh patterns that define a set of words
    """

    def word_avoids(self, word: tuple[int, ...], *args: MeshPattern):
        """Return True if the word avoids all of the mesh patterns."""
        return all(mesh_patt.is_avoided_by_word(word) for mesh_patt in args)

    def word_contains(self, word: tuple[int, ...], *args: MeshPattern) -> bool:
        """
        Returns True if the word contains any of the mesh patterns.
        """
        return not self.word_avoids(word, *args)

    @staticmethod
    def minimal_patterns(patterns: Iterable[MeshPattern]) -> set[MeshPattern]:
        """
        Returns the set of minimal patterns from the given set of patterns.
        """
        logger.info("Computing minimal mesh patterns")
        basis: set[MeshPattern] = set()
        for patt in tqdm(sorted(patterns), desc="Computing minimal patterns"):
            if patt.avoids(*basis):
                basis.add(patt)
        return basis

    def find_mesh_basis(self) -> list[MeshPattern]:
        """
        Find the minimal patterns that are not contained in the avoiders.

        This can be modeled as a set cover problem on the containers.
        https://math.stackexchange.com/questions/2750531/finding-the-smallest-set-with-non-empty-intercept-with-of-a-collection-of-sets

        First reduce to the minimal set of mesh patterns according to
        mesh pattern containment.

        Then, compute Co(p) for each pattern p in the minimal set,
        in order to find the mesh basis p1, p2, ..., pk such that
        Co(p1) union Co(p2) union ... union Co(pk)
        is equal to the containers.
        """
        minimal_patterns_not_contained = list(
            self.find_minimal_patterns_not_contained()
        )
        basis = self.minimal_patterns(minimal_patterns_not_contained)

        containers = self.all_containers()
        container_labels: dict[tuple[int, ...], int] = {}
        for word in containers:
            container_labels[word] = len(container_labels)

        logger.info("Computing container set for patterns")
        label_to_patt: dict[int, MeshPattern] = {}
        subsets_left = []
        for patt in tqdm(basis, desc="Computing contained sets"):
            patt_containers = set(
                container_labels[word]
                for word in containers
                if self.word_contains(word, patt)
            )
            label = len(label_to_patt)
            label_to_patt[label] = patt
            subsets_left.append((label, patt_containers))

        basis_labels = self.set_cover(container_labels.values(), subsets_left)
        return [label_to_patt[label] for label in basis_labels]

    def find_minimal_patterns_not_contained(self) -> Iterator[MeshPattern]:
        """
        Compute the minimal incomparable set of patterns to those contained in avoiders
        """
        maximal_shaded_patterns = self.find_maximal_shaded_patterns()
        logger.info("Computing minimal patterns avoided")
        for patt in (
            self.universe_up_to_size(self.max_patt_size)
            - maximal_shaded_patterns.keys()
        ):
            yield MeshPattern(patt, [])

        for patt, shadings in tqdm(
            maximal_shaded_patterns.items(), desc="Computing minimal patterns avoided"
        ):
            vertices = set()
            edges = set()
            cell_label: dict[tuple[int, int], int] = {}
            label_cell: dict[int, tuple[int, int]] = {}
            for shading in shadings:
                edge = []
                for cell in shading:
                    if cell not in cell_label:
                        cell_label[cell] = len(cell_label)
                        label_cell[cell_label[cell]] = cell
                        vertices.add(cell_label[cell])
                    edge.append(cell_label[cell])
                edges.add(tuple(sorted(edge)))
            for shading_labels in self.enumerate_hitting_sets(
                list(vertices), list(edges)
            ):
                cells = [label_cell[v] for v in shading_labels]
                yield MeshPattern(patt, cells)

    def find_maximal_shaded_patterns(
        self,
    ) -> dict[CayleyPermutation, set[frozenset[tuple[int, int]]]]:
        """
        For each word in the avoiders, find the maximal mesh patterns it contains for
        each size of patterns. Here, maximal means the most shading possible.
        """
        # pylint: disable=too-many-nested-blocks
        logger.info("Computing maximal shadded patterns contained")
        contained_patterns: dict[CayleyPermutation, set[frozenset[tuple[int, int]]]] = (
            defaultdict(set)
        )
        for i in range(self.max_patt_size + 1):
            logger.info("Computing size %s patterns", i)
            for word in tqdm(self.all_avoiders(i)):
                minimal_shadings = self.minimal_shadings(word, i)
                for patt, shadings in minimal_shadings.items():
                    for shading in shadings:
                        shading = frozenset(shading)
                        sets_to_remove = set()
                        to_add = True
                        for other_shading in contained_patterns[patt]:
                            if other_shading.issubset(shading):
                                to_add = False
                                break
                            if shading.issubset(other_shading):
                                sets_to_remove.add(other_shading)
                        if to_add:
                            contained_patterns[patt] -= sets_to_remove
                            contained_patterns[patt].add(frozenset(shading))
        return contained_patterns

    @staticmethod
    def minimal_shadings(
        word: tuple[int, ...], i: int
    ) -> dict[CayleyPermutation, set[frozenset[tuple[int, int]]]]:
        """
        Return the minimal shadings implied by all occurrences
        of cayley permutations.
        """
        minimal_shadings: dict[CayleyPermutation, set[frozenset[tuple[int, int]]]] = {}
        for occurrence in combinations(range(len(word)), i):
            patt = CayleyPermutation.standardise(tuple(word[i] for i in occurrence))
            if patt not in minimal_shadings:
                minimal_shadings[patt] = set()
            minimal_shadings[patt].add(MeshPattern.non_empty_regions(word, occurrence))
        return minimal_shadings


class CayleyMeshPatternFinder(MeshPatternFinder):
    """
    Class for finding patterns that define a set of Cayley Permutations
    """

    @staticmethod
    def universe_of_size(n: int) -> frozenset[CayleyPermutation]:
        return frozenset(CayleyPermutation.of_size(n))


class InversionSequencePatternFinder(MeshPatternFinder):
    """
    Class for finding patterns that define a set of inversion sequences
    """

    @staticmethod
    def universe_of_size(n: int) -> frozenset[tuple[int, ...]]:
        return frozenset(product(*[range(i) for i in range(1, n + 1)]))


class PermutationPatternFinder(MeshPatternFinder):
    """
    Class for finding patterns that define a set of permutations
    """

    @staticmethod
    def universe_of_size(n: int) -> frozenset[tuple[int, ...]]:
        return frozenset(permutations(range(n)))


class AscentSequencePatternFinder(MeshPatternFinder):
    """
    Class for finding patterns that define a set of ascent sequences
    """

    @staticmethod
    def universe_of_size(n: int) -> frozenset[tuple[int, ...]]:
        def number_of_ascents(seq: tuple[int, ...]) -> int:
            return sum(1 for a, b in zip(seq, seq[1:]) if a < b)

        def ascent_sequences(n: int) -> Iterator[tuple[int, ...]]:
            if n == 0:
                yield tuple()
                return
            if n == 1:
                yield (0,)
                return
            for seq in ascent_sequences(n - 1):
                for value in range(number_of_ascents(seq) + 2):
                    yield seq + (value,)

        return frozenset(ascent_sequences(n))


class RestrictedGrowthFunctionPatternFinder(MeshPatternFinder):
    """
    Class for finding patterns that define a set of restricted growth functions
    """

    @staticmethod
    def universe_of_size(n: int) -> frozenset[tuple[int, ...]]:
        def rgf(n: int) -> Iterator[tuple[int, ...]]:
            if n == 0:
                yield tuple()
                return
            if n == 1:
                yield (0,)
                return
            for cperm in rgf(n - 1):
                for value in range(max(cperm) + 2):
                    yield cperm + (value,)

        return frozenset(rgf(n))
