from typing import Iterable
from gridded_cayley_permutations import Tiling
from gridded_cayley_permutations.row_col_map import RowColMap

Cell = tuple[int, int]
Clouds = tuple[tuple[Cell, ...], ...]


class TrackedTiling(Tiling):
    """A Tiling with clouds which keep track of areas of the tiling.
    One type of cloud tracks the number of values in the cells and the other
    tracks the number of indices in the cells."""

    def __init__(
        self,
        tiling: Tiling,
        value_clouds: Clouds = (),
        indices_clouds: Clouds = (),
        simplify: bool = False,
        intersect_clouds_with_active: bool = False,
    ) -> None:
        self.tiling = tiling
        super().__init__(
            tiling.obstructions, tiling.requirements, tiling.dimensions, simplify
        )
        self.value_clouds = value_clouds
        self.indices_clouds = indices_clouds
        if intersect_clouds_with_active:
            self.value_clouds = tuple(
                tuple(cell for cell in cloud if cell in self.active_cells)
                for cloud in self.value_clouds
            )
            self.indices_clouds = tuple(
                tuple(cell for cell in cloud if cell in self.active_cells)
                for cloud in self.indices_clouds
            )

    @classmethod
    def map_clouds(
        cls,
        value_clouds: Clouds,
        indices_clouds: Clouds,
        tiling_map: RowColMap,
    ) -> tuple[tuple[Cell, ...], tuple[Cell, ...]]:
        """For a given row-col map of self.tiling to a new tiling,
        updates the clouds to match the new tiling.

        Can add this to the new tiling, check that intersects active cells."""
        col_row_preimages = cls.col_row_preimages(tiling_map)
        new_value_clouds = []
        new_indices_clouds = []
        for cloud in value_clouds:
            value_cloud = []
            for cell in cloud:
                for mapped_cell in cls.map_cells_for_clouds(cell, col_row_preimages):
                    value_cloud.append(mapped_cell)
            value_cloud = tuple(value_cloud)
            if value_cloud:
                new_value_clouds.append(value_cloud)
        for cloud in indices_clouds:
            indices_cloud = []
            for cell in cloud:
                for mapped_cell in cls.map_cells_for_clouds(cell, col_row_preimages):
                    indices_cloud.append(mapped_cell)
            indices_cloud = tuple(indices_cloud)
            if indices_cloud:
                new_indices_clouds.append(indices_cloud)
        return tuple(new_value_clouds), tuple(new_indices_clouds)

    @classmethod
    def col_row_preimages(
        cls, tiling_map: RowColMap
    ) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
        """The preimages of rows and cols in the tiling."""
        row_preimages = [
            tiling_map.preimages_of_row(i)
            for i in range(len(tiling_map.row_map.items()))
        ]
        col_preimages = [
            tiling_map.preimages_of_col(j)
            for j in range(len(tiling_map.col_map.items()))
        ]
        return col_preimages, row_preimages

    @classmethod
    def map_cells_for_clouds(
        cls,
        cell: Cell,
        col_row_preimages: tuple[dict[int, list[int]], dict[int, list[int]]],
    ) -> tuple[Cell, ...]:
        """
        Map the cell to its new positions, allowing for multiple new positions.
        """
        cells_mapping_to = []
        for i in col_row_preimages[0][cell[0]]:
            for j in col_row_preimages[1][cell[1]]:
                cells_mapping_to.append((i, j))
        return tuple(cells_mapping_to)

    def delete_rows_and_columns(
        self, cols: Iterable[int], rows: Iterable[int]
    ) -> "TrackedTiling":
        """Return a new tiling with the given rows and columns removed
        and updated clouds."""
        rows, cols = set(rows), set(cols)
        col_map = {}
        counter = 0
        for ind in range(self.dimensions[0]):
            if ind in cols:
                continue
            col_map[ind] = counter
            counter += 1
        row_map = {}
        counter = 0
        for ind in range(self.dimensions[1]):
            if ind in rows:
                continue
            row_map[ind] = counter
            counter += 1
        rc_map = RowColMap(col_map, row_map)
        new_obstructions = tuple(
            ob
            for ob in self.obstructions
            if all(x not in cols and y not in rows for x, y in ob.positions)
        )
        new_obstructions = rc_map.map_gridded_cperms(new_obstructions)
        new_requirements = []
        for req_list in self.requirements:
            new_req_list = tuple(
                req
                for req in req_list
                if all(x not in cols and y not in rows for x, y in req.positions)
            )
            if new_req_list:
                new_requirements.append(new_req_list)
        new_requirements = list(rc_map.map_requirements(new_requirements))
        new_dimensions = (
            self.dimensions[0] - len(cols),
            self.dimensions[1] - len(rows),
        )
        new_til = Tiling(
            new_obstructions, new_requirements, new_dimensions, simplify=False
        )

        def map_cell(cell: Cell) -> Cell:
            return (col_map[cell[0]], row_map[cell[1]])

        new_value_clouds = []
        for cloud in self.value_clouds:
            new_cloud = tuple(
                map_cell(cell)
                for cell in cloud
                if cell[0] not in cols
                and cell[1] not in rows
                and map_cell(cell) in new_til.active_cells
            )
            if new_cloud:
                new_value_clouds.append(new_cloud)
        new_indices_clouds = []
        for cloud in self.indices_clouds:
            new_cloud = tuple(
                map_cell(cell)
                for cell in cloud
                if cell[0] not in cols
                and cell[1] not in rows
                and map_cell(cell) in new_til.active_cells
            )
            if new_cloud:
                new_indices_clouds.append(new_cloud)
        return TrackedTiling(
            new_til,
            value_clouds=tuple(new_value_clouds),
            indices_clouds=tuple(new_indices_clouds),
        )

    def fuse(self, fuse_rows: bool, index: int) -> "Tiling":
        """If fuse_rows, tries to fuse rows, otherwise, tries to fuse cols.
        Creates a cloud at index 'index' of rows if fuse_rows else columns."""
        if fuse_rows is False:
            tracked_til = self.delete_rows_and_columns(cols=[index], rows=[])
            new_cloud = tracked_til.col_or_row_cloud(row=False, index=index)
            return TrackedTiling(
                tracked_til.tiling,
                tracked_til.value_clouds,
                tracked_til.indices_clouds + (new_cloud,),
            )
        tracked_til = self.delete_rows_and_columns(cols=[], rows=[index])
        new_cloud = tracked_til.col_or_row_cloud(row=True, index=index)
        return TrackedTiling(
            tracked_til.tiling,
            tracked_til.value_clouds + (new_cloud,),
            tracked_til.indices_clouds,
        )

    def col_or_row_cloud(self, row: bool, index: int) -> tuple[Cell, ...]:
        """Returns the cloud that would be created at the column or row."""
        if row:
            return tuple(
                (col, index)
                for col in range(self.dimensions[0])
                if (col, index) in self.active_cells
            )
        return tuple(
            (index, row)
            for row in range(self.dimensions[1])
            if (index, row) in self.active_cells
        )

    def is_fusable(self, fuse_rows: bool, index: int) -> bool:
        """If fuse rows, checks if the rows at index and index+1 are fuseable,
        otherwise does the same for cols at index and index+1.

        can't fuse rows/cols if a cloud maps onto only part of the rows/cols to be fused,
        must map to all or none of it."""
        if fuse_rows:
            cells_fusing = [(col, index) for col in range(self.dimensions[0])] + [
                (col, index + 1) for col in range(self.dimensions[0])
            ]
        else:
            cells_fusing = [(index, row) for row in range(self.dimensions[1])] + [
                (index + 1, row) for row in range(self.dimensions[1])
            ]
        for cloud in self.value_clouds + self.indices_clouds:
            cloud_in_fusion_area = [cell for cell in cloud if cell in cells_fusing]
            if 0 < len(cloud_in_fusion_area) < len(cells_fusing):
                return False

        if fuse_rows:
            test_tiling = self.delete_rows_and_columns(cols=[], rows=[index])
        else:
            test_tiling = self.delete_rows_and_columns(cols=[index], rows=[])
        test_tiling = test_tiling.split_row_or_col(fuse_rows, index)
        return test_tiling == self

    # CSS methods
    @property
    def extra_parameters(self) -> tuple[str, ...]:
        """Indices are first, then values."""
        value_cloud_params = [f"v_{i}" for i in range(len(self.value_clouds))]
        index_cloud_params = [f"i_{i}" for i in range(len(self.indices_clouds))]
        return tuple(index_cloud_params + value_cloud_params)

    def find_parameter(self, cloud: tuple[Cell, ...], row: bool) -> str:
        """Finds the name of the parameter for the cloud."""
        try:
            index = (
                self.value_clouds.index(cloud)
                if not row
                else self.indices_clouds.index(cloud)
            )
        except ValueError:
            raise ValueError("Cloud not found in tracked tiling.")
        return f"i_{index}" if row else f"v_{index}"

    def __str__(self) -> str:
        return (
            f"Tiling: \n{self.tiling}\n"
            f"Value clouds: {self.value_clouds},\n"
            f"Indices clouds: {self.indices_clouds}"
        )

    def __repr__(self) -> str:
        return (
            f"TrackedTiling(tiling={repr(self.tiling)}, "
            f"value_clouds={repr(self.value_clouds)}, "
            f"indices_clouds={repr(self.indices_clouds)})"
        )
