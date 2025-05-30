"""This module contains the MinimalGriddedCayleyPerm class, which is used to find
the minimal gridded cayley permutations in a tiling."""

from collections import defaultdict
from functools import lru_cache
from heapq import heapify, heappop, heappush
from itertools import product
from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    # pylint: disable=all
    from gridded_cayley_permutations import GriddedCayleyPerm

Gcptuple = tuple["GriddedCayleyPerm", ...]
Requirements = tuple[Gcptuple, ...]


class QueuePacket:
    """A work packet for the queue in the minimal gridded cperm algorithm.

    gcp: the gridded cperm so far
    gcps: the requirement that we aim to satisfy
    last_cell: the cell that the last point was inserted into
    mindices: the minimum indices for each cell to ensure per column
              that we insert left to right
    still_localising: whether we are still localising, i.e
                      inserting in cells to ensure that local
                      reqs are satisfied
    """

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    # pylint: disable=too-few-public-methods

    # This should realy be a named tuple, but I want to override the __lt__ method

    def __init__(
        self,
        gcp: "GriddedCayleyPerm",
        gcps: Gcptuple,
        last_cell: tuple[int, int],
        mindices: dict[tuple[int, int], int],
        still_localising: bool,
    ) -> None:

        self.gcp = gcp
        self.gcps = gcps
        self.last_cell = last_cell
        self.mindices = mindices
        self.still_localising = still_localising

    def __lt__(self, other: "QueuePacket") -> bool:
        return len(self.gcp) < len(other.gcp)


class MinimalGriddedCayleyPerm:
    """
    This class contains methods for finding the minimal gridded cayley permutations that avoid
    the obstructions and contain the requirements.
    """

    def __init__(self, obstructions: Gcptuple, requirements: Requirements) -> None:
        self.obstructions = obstructions
        self.requirements = requirements
        assert (
            self.requirements
        ), "if no requirements, then minimal just empty gridded cayley perm"
        self.queue: list[QueuePacket] = []
        self.yielded_so_far: list["GriddedCayleyPerm"] = []

    def initialise_queue(self) -> None:
        """Initialises the queue with the minimal gridded cperm."""
        heapify(self.queue)
        for gcps in product(*self.requirements):
            qpacket = QueuePacket(gcps[0], gcps, (-1, -1), {}, True)
            heappush(self.queue, qpacket)

    def minimal_gridded_cperms(
        self,
    ) -> Iterator["GriddedCayleyPerm"]:
        """Returns the minimal gridded cperms for the minimal gridded cperm."""
        if len(self.requirements) == 1:
            yield from self.requirements[0]
            return
        self.initialise_queue()
        while self.queue:
            qpacket = heappop(self.queue)
            yield from self.try_yield(qpacket.gcp)
            for new_qpacket in self.extend_by_one_point(qpacket):
                heappush(self.queue, new_qpacket)

    def try_yield(self, gcp: "GriddedCayleyPerm") -> Iterator["GriddedCayleyPerm"]:
        """Yield if the gridded cperm is minimal and satisfies the requirements."""
        if self.satisfies_requirements(gcp):
            if gcp.avoids(self.yielded_so_far):
                self.yielded_so_far.append(gcp)
                yield gcp

    def extend_by_one_point(self, qpacket: QueuePacket) -> Iterator[QueuePacket]:
        """Extends the minimal gridded cperm by one point."""
        for cell, is_localised in self.cells_to_try(qpacket):
            mindex = qpacket.mindices.get(cell, 0)
            for new_gcp, index in self.insert_point(qpacket.gcp, cell, mindex):
                if self.satisfies_obstructions(new_gcp):
                    new_mindices = {
                        c: i if i <= index else i + 1
                        for c, i in qpacket.mindices.items()
                        if c != cell
                    }
                    new_mindices[cell] = index + 1
                    yield QueuePacket(
                        new_gcp, qpacket.gcps, cell, new_mindices, is_localised
                    )

    def cells_to_try(
        self, qpacket: QueuePacket
    ) -> Iterator[tuple[tuple[int, int], bool]]:
        """Returns the cells to try for the next point."""
        last_cell = qpacket.last_cell
        cells: set[tuple[int, int]] = set()
        for g, req_list in zip(qpacket.gcps, self.requirements):
            if qpacket.gcp.avoids(req_list):
                cells.update(g.positions)
            elif qpacket.gcp.avoids([g]):
                return
        current_cell_count = self.get_max_cell_count((qpacket.gcp,))
        maximum_cell_count = self.get_max_cell_count(qpacket.gcps)
        cells = set(
            cell
            for cell in cells
            if current_cell_count[cell] < maximum_cell_count[cell]
        )
        if qpacket.still_localising:
            for cell in cells:
                localised_pats = self.get_localised_pats(qpacket.gcps, cell)
                if qpacket.gcp.avoids(localised_pats):
                    yield (cell, True)
                    return
        yield from self._try_yield_cell(cells, last_cell, qpacket.gcp)

    def _try_yield_cell(
        self,
        cells: set[tuple[int, int]],
        last_cell: tuple[int, int],
        gcp: "GriddedCayleyPerm",
    ) -> Iterator[tuple[tuple[int, int], bool]]:
        for cell in cells:
            if cell == last_cell:
                yield (cell, False)
            elif cell > last_cell:
                to_the_left_requirements = self.requirements_up_to_cell(cell)
                if all(gcp.contains(req) for req in to_the_left_requirements):
                    yield (cell, False)

    @lru_cache(maxsize=100)
    def requirements_up_to_cell(self, cell: tuple[int, int]) -> Requirements:
        """Returns the requirements up to the cell."""
        return tuple(
            tuple(
                gcp.sub_gridded_cayley_perm(set(c for c in gcp.positions if c < cell))
                for gcp in req_list
            )
            for req_list in self.requirements
        )

    def get_localised_pats(self, gcps: Gcptuple, cell: tuple[int, int]) -> Gcptuple:
        """Returns the localised patterns for the cell."""
        return tuple(gcp.sub_gridded_cayley_perm([cell]) for gcp in gcps)

    @lru_cache(maxsize=100)
    def get_max_cell_count(self, gcps: Gcptuple) -> dict[tuple[int, int], int]:
        """Returns the maximum cell count for each cell."""
        max_cell_count: dict[tuple[int, int], int] = defaultdict(int)
        for gcp in gcps:
            for cell in gcp.positions:
                max_cell_count[cell] += 1
        return max_cell_count

    def insert_point(
        self, gcp: "GriddedCayleyPerm", cell: tuple[int, int], minimum_index: int
    ) -> Iterator[tuple["GriddedCayleyPerm", int]]:
        """Inserts a point into the gridded cperm at the index."""
        mindex, maxdex, minval, maxval = gcp.bounding_box_of_cell(cell)
        mindex = max(mindex, minimum_index)
        for index in range(maxdex, mindex - 1, -1):
            for val in range(minval, maxval + 1):
                for new_gcp in gcp.insert_specific_point(cell, index, val):
                    if self.satisfies_obstructions(new_gcp):
                        yield new_gcp, index

    def satisfies_requirements(self, gcp: "GriddedCayleyPerm") -> bool:
        """Checks if the gridded cperm satisfies the requirements."""
        return all(gcp.contains(req) for req in self.requirements)

    def satisfies_obstructions(self, gcp: "GriddedCayleyPerm") -> bool:
        """Checks if the gridded cperm satisfies the obstructions."""
        return gcp.avoids(self.obstructions)
