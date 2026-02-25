from itertools import product

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from functools import cached_property
from collections import defaultdict
from cayley_permutations import CayleyPermutation


class ObstructionTransitivity:
    def __init__(self, tiling: Tiling):
        self.tiling = tiling

    @cached_property
    def ineqs(
        self,
    ) -> tuple[
        dict[int, set[tuple[int, int]]],
        dict[int, set[tuple[int, int]]],
        dict[int, set[tuple[int, int]]],
        dict[int, set[tuple[int, int]]],
    ]:
        col_less_than: dict[int, set[tuple[int, int]]] = defaultdict(set)
        row_less_than: dict[int, set[tuple[int, int]]] = defaultdict(set)
        row_less_than_or_equal: dict[int, set[tuple[int, int]]] = defaultdict(set)
        not_equal: dict[int, set[tuple[int, int]]] = defaultdict(set)
        for ob in self.tiling.obstructions:
            if len(ob) == 2 and ob.positions[0] != ob.positions[1]:
                (a, b), (c, d) = ob.positions
                if ob.pattern[0] == ob.pattern[1]:
                    not_equal[b].add((a, c))
                    not_equal[b].add((c, a))
                    continue
                if a == c:
                    col_less_than[a].add((d, b))
                else:
                    # b == d
                    if ob.pattern[0] == 0:
                        if (
                            GriddedCayleyPerm(CayleyPermutation((0, 0)), ob.positions)
                            in self.tiling.obstructions
                        ):
                            row_less_than[b].add((c, a))
                        row_less_than_or_equal[b].add((c, a))
                    else:
                        if (
                            GriddedCayleyPerm(CayleyPermutation((0, 0)), ob.positions)
                            in self.tiling.obstructions
                        ):
                            row_less_than[b].add((a, c))
                        row_less_than_or_equal[b].add((a, c))
        return col_less_than, row_less_than, row_less_than_or_equal, not_equal

    @cached_property
    def col_less_than(self) -> dict[int, list[tuple[int, int]]]:
        return self.ineqs[0]

    @cached_property
    def row_less_than(self) -> dict[int, list[tuple[int, int]]]:
        return self.ineqs[1]

    @cached_property
    def row_less_than_or_equal(self) -> dict[int, list[tuple[int, int]]]:
        return self.ineqs[2]

    @cached_property
    def not_equal(self) -> dict[int, list[tuple[int, int]]]:
        return self.ineqs[3]

    @cached_property
    def positive_cells(self) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
        rows, cols = defaultdict(set), defaultdict(set)
        for a, b in self.tiling.positive_cells():
            rows[b].add(a)
            cols[a].add(b)
        return rows, cols

    @cached_property
    def positive_cols_in_row(self) -> tuple[dict[int, list[int]]]:
        return self.positive_cells[0]

    @cached_property
    def postive_rows_in_col(self) -> tuple[dict[int, list[int]]]:
        return self.positive_cells[1]

    @staticmethod
    def closure(
        less_than: set[tuple[int, int]],
        less_than_or_equal: set[tuple[int, int]],
        not_equal: set[tuple[int, int]],
        positive_cells: set[int],  # the positive rows or cols
    ) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        new_less_than: set[tuple[int, int]] = set()
        new_less_than_or_equal: set[tuple[int, int]] = set()
        lt, gt, lte, gte = (
            defaultdict(list),
            defaultdict(list),
            defaultdict(list),
            defaultdict(list),
        )
        for a, b in less_than:
            lt[a].append(b)
            gt[b].append(a)
        for a, b in less_than_or_equal:
            lte[a].append(b)
            gte[b].append(a)

        to_analyse = positive_cells
        while to_analyse:
            cur = to_analyse.pop()
            not_existing_lt = set()
            not_existing_lt.update(
                filter(lambda x: x not in less_than, product(gt[cur], lt[cur]))
            )
            not_existing_lt.update(
                filter(lambda x: x not in less_than, product(gte[cur], lt[cur]))
            )
            not_existing_lt.update(
                filter(lambda x: x not in less_than, product(gt[cur], lte[cur]))
            )
            not_existing_lte = filter(
                lambda x: x not in less_than, product(gte[cur], lte[cur])
            )
            for a, b in not_existing_lt:
                less_than.add((a, b))
                new_less_than.add((a, b))
                if a in positive_cells:
                    to_analyse.add(a)
                if b in positive_cells:
                    to_analyse.add(b)
            for a, b in not_existing_lte:
                if (a, b) in not_equal:
                    less_than.add((a, b))
                    new_less_than.add((a, b))
                less_than_or_equal.add((a, b))
                new_less_than_or_equal.add((a, b))
                if a in positive_cells:
                    to_analyse.add(a)
                if b in positive_cells:
                    to_analyse.add(b)
        # remove the reflexive from second set (x, x)
        return new_less_than, new_less_than_or_equal - new_less_than

    @staticmethod
    def less_than_or_equal_to_ob(
        cell1: tuple[int, int], cell2: tuple[int, int]
    ) -> GriddedCayleyPerm:
        (a, b), (c, d) = cell1, cell2
        if cell1 == cell2:
            return GriddedCayleyPerm((0,), (cell1,))
        if a == c:
            if b < d:
                return GriddedCayleyPerm((1, 0), ((cell2, cell1)))
            elif d < b:
                return GriddedCayleyPerm((0, 1), ((cell2, cell1)))
        else:
            # b == d
            if a < c:
                return GriddedCayleyPerm((1, 0), (cell1, cell2))
            elif c < a:
                return GriddedCayleyPerm((0, 1), (cell2, cell1))

    @staticmethod
    def less_than_to_ob(
        cell1: tuple[int, int], cell2: tuple[int, int]
    ) -> tuple[GriddedCayleyPerm, ...]:
        if cell1 == cell2:
            return (GriddedCayleyPerm((0,), (cell1,)),)
        if cell1[0] == cell2[0]:
            return (ObstructionTransitivity.less_than_or_equal_to_ob(cell1, cell2),)
        # cell1[1] == cell2[1]
        if cell1[0] > cell2[0]:
            position = (cell2, cell1)
        else:
            position = (cell1, cell2)

        return (
            ObstructionTransitivity.less_than_or_equal_to_ob(cell1, cell2),
            GriddedCayleyPerm((0, 0), position),
        )

    def new_obs(self):
        obs = set()
        for row in range(self.tiling.dimensions[1]):
            new_less_than, new_less_than_or_equal = self.closure(
                self.row_less_than[row],
                self.row_less_than_or_equal[row],
                self.not_equal[row],
                self.positive_cols_in_row[row],
            )
            for col1, col2 in new_less_than:
                obs.update(self.less_than_to_ob((col1, row), (col2, row)))
            for col1, col2 in new_less_than_or_equal:
                if col1 != col2:
                    obs.add(self.less_than_or_equal_to_ob((col1, row), (col2, row)))
        for col in range(self.tiling.dimensions[0]):
            print(self.col_less_than[col])
            _, new_less_than_or_equal = self.closure(
                set(), self.col_less_than[col], set(), self.postive_rows_in_col[col]
            )
            for row1, row2 in new_less_than_or_equal:
                obs.add(self.less_than_or_equal_to_ob((col, row1), (col, row2)))
        return obs


if __name__ == "__main__":
    tiling = Tiling(
        [
            # GriddedCayleyPerm((0, 1), ((0, 0), (1, 0))),
            # GriddedCayleyPerm((1, 0), ((0, 0), (1, 0))),
            # GriddedCayleyPerm((0, 1), ((1, 0), (2, 0))),
            # GriddedCayleyPerm((0, 0), ((0, 0), (1, 0))),
            GriddedCayleyPerm((0, 1), ((1, 0), (1, 1))),
            GriddedCayleyPerm((0, 1), ((1, 1), (1, 2))),
        ],
        [[GriddedCayleyPerm((0,), ((1, 0),))], [GriddedCayleyPerm((0,), ((1, 1),))]],
        (3, 3),
    )
    print(tiling)

    obstrans = ObstructionTransitivity(tiling)

    less_than = obstrans.row_less_than[0]
    less_than_or_equal = obstrans.row_less_than_or_equal[0]
    not_equal = obstrans.not_equal[0]
    positive_cells = obstrans.positive_cols_in_row[0]

    # print(
    #     obstrans.closure(less_than, less_than_or_equal, not_equal, positive_cells)
    # )
    # print(obstrans.less_than_to_ob((0, 0), (0, 0)))

    print(obstrans.new_obs())
