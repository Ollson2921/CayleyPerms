from functools import cached_property
from typing import Iterable
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap

Cell = tuple[int, int]
Clouds = tuple[tuple[int, ...], ...]


class TrackedTiling(Tiling):
    """A Tiling with clouds which keep track of areas of the tiling.
    One type of cloud tracks the number of values in the cells and the other
    tracks the number of indices in the cells."""

    def __init__(
        self,
        tiling: Tiling,
        indices_clouds: Iterable[Iterable[int]] = (),
        value_clouds: Iterable[Iterable[int]] = (),
        simplify: bool = False,
        intersect_clouds_with_active: bool = False,
    ) -> None:
        self.tiling = tiling
        super().__init__(
            tiling.obstructions, tiling.requirements, tiling.dimensions, simplify
        )
        self.value_clouds = tuple(sorted(tuple(sorted(c)) for c in value_clouds))
        self.indices_clouds = tuple(sorted(tuple(sorted(c)) for c in indices_clouds))
        if intersect_clouds_with_active:
            active_rows, active_cols = self.active_col_rows
            self.value_clouds = tuple(
                sorted(
                    c
                    for c in [
                        tuple(sorted(row for row in cloud if row in active_rows))
                        for cloud in value_clouds
                    ]
                    if c
                )
            )
            self.indices_clouds = tuple(
                sorted(
                    c
                    for c in [
                        tuple(sorted(col for col in cloud if col in active_cols))
                        for cloud in indices_clouds
                    ]
                    if c
                )
            )

    @cached_property
    def active_col_rows(self) -> tuple[set[int], set[int]]:
        """Returns the columns and rows in the tiling that have active cells."""
        active_rows = set()
        active_cols = set()
        for cell in self.active_cells:
            active_cols.add(cell[0])
            active_rows.add(cell[1])
        return active_cols, active_rows

    @classmethod
    def map_clouds(
        cls,
        indices_clouds: Clouds,
        value_clouds: Clouds,
        tiling_map: RowColMap,
    ) -> tuple[Clouds, Clouds]:
        """For a given row-col map of self.tiling to a new tiling,
        updates the clouds to match the new tiling.

        Can add this to the new tiling, check that intersects active cells."""
        new_value_clouds = tuple(
            sorted(
                c
                for c in [
                    tuple(sorted(tiling_map.preimages_of_rows(cloud)))
                    for cloud in value_clouds
                ]
                if c
            )
        )
        new_indices_clouds = tuple(
            sorted(
                c
                for c in [
                    tuple(sorted(tiling_map.preimages_of_cols(cloud)))
                    for cloud in indices_clouds
                ]
                if c
            )
        )
        return (
            new_indices_clouds,
            new_value_clouds,
        )

    def delete_rows_and_columns(
        self, cols: Iterable[int], rows: Iterable[int]
    ) -> "TrackedTiling":
        """Return a new tiling with the given rows and columns removed
        and updated clouds."""
        new_til, rc_map = self.tiling_and_rc_map_after_deleting_rows_and_columns(
            cols, rows
        )
        row_map, col_map = rc_map.row_map, rc_map.col_map
        new_value_clouds = tuple(
            sorted(
                tuple(sorted(row_map[row] for row in cloud if row not in rows))
                for cloud in self.value_clouds
            )
        )
        new_indices_clouds = tuple(
            sorted(
                tuple(sorted(col_map[col] for col in cloud if col not in cols))
                for cloud in self.indices_clouds
            )
        )
        return TrackedTiling(
            new_til,
            value_clouds=new_value_clouds,
            indices_clouds=new_indices_clouds,
        )

    def fuse(self, fuse_rows: bool, index: int) -> "Tiling":
        """If fuse_rows, tries to fuse rows, otherwise, tries to fuse cols.
        Creates a cloud at index 'index' of rows if fuse_rows else columns."""
        new_cloud = (index,)
        if fuse_rows is False:
            tracked_til = self.delete_rows_and_columns(cols=[index], rows=[])
            new_indices_clouds = tracked_til.indices_clouds + (new_cloud,)
            return TrackedTiling(
                tracked_til.tiling,
                indices_clouds=new_indices_clouds,
                value_clouds=tracked_til.value_clouds,
            )
        tracked_til = self.delete_rows_and_columns(cols=[], rows=[index])
        return TrackedTiling(
            tracked_til.tiling,
            indices_clouds=tracked_til.indices_clouds,
            value_clouds=tracked_til.value_clouds + (new_cloud,),
        )

    def is_fusable(self, fuse_rows: bool, index: int) -> bool:
        """If fuse rows, checks if the rows at index and index+1 are fuseable,
        otherwise does the same for cols at index and index+1.

        can't fuse rows/cols if a cloud maps onto only part of the rows/cols to be fused,
        must map to all or none of it."""
        if fuse_rows:
            if any(
                index in cloud and (index + 1) not in cloud
                for cloud in self.value_clouds
            ) or any(
                index not in cloud and (index + 1) in cloud
                for cloud in self.value_clouds
            ):
                return False
            if any(
                req.positions[1] == index or req.positions[1] == index + 1
                for req_list in self.requirements
                for req in req_list
            ):
                return False
        else:
            if any(
                index in cloud and (index + 1) not in cloud
                for cloud in self.indices_clouds
            ) or any(
                index not in cloud and (index + 1) in cloud
                for cloud in self.indices_clouds
            ):
                return False
            if any(
                req.positions[0] == index or req.positions[0] == index + 1
                for req_list in self.requirements
                for req in req_list
            ):
                return False

        if fuse_rows:
            test_tiling = self.delete_rows_and_columns(cols=[], rows=[index])
        else:
            test_tiling = self.delete_rows_and_columns(cols=[index], rows=[])
        test_tiling = test_tiling.split_row_or_col(fuse_rows, index)
        return test_tiling == self

    def add_obstructions(self, gcps: Iterable[GriddedCayleyPerm]) -> "Tiling":
        """
        Returns a new tiling with the given gridded Cayley permutations added as obstructions.
        """
        return TrackedTiling(
            Tiling(self.obstructions + tuple(gcps), self.requirements, self.dimensions),
            indices_clouds=self.indices_clouds,
            value_clouds=self.value_clouds,
        )

    def add_requirements(
        self, requirements: Iterable[Iterable[GriddedCayleyPerm]]
    ) -> "Tiling":
        """
        Returns a new tiling with the given requirements added.
        """
        return TrackedTiling(
            Tiling(
                self.obstructions,
                self.requirements + tuple(requirements),
                self.dimensions,
            ),
            indices_clouds=self.indices_clouds,
            value_clouds=self.value_clouds,
        )

    # CSS methods
    @property
    def extra_parameters(self) -> tuple[str, ...]:
        """Indices are first, then values."""
        index_cloud_params = [f"i_{i}" for i in range(len(self.indices_clouds))]
        value_cloud_params = [f"v_{i}" for i in range(len(self.value_clouds))]
        return tuple(index_cloud_params + value_cloud_params)

    def find_parameter(self, cloud: tuple[int, ...], row: bool) -> str:
        """Finds the name of the parameter for the cloud."""
        try:
            index = (
                self.value_clouds.index(cloud)
                if row
                else self.indices_clouds.index(cloud)
            )
        except ValueError as exc:
            raise ValueError("Cloud not found in tracked tiling.") from exc
        return f"i_{index}" if row else f"v_{index}"

    def __str__(self) -> str:
        return (
            f"Tiling: \n{self.tiling}\n"
            f"Indices clouds: {self.indices_clouds}\n"
            f"Value clouds: {self.value_clouds},"
        )

    def __repr__(self) -> str:
        return (
            f"TrackedTiling(tiling={repr(self.tiling)}, "
            f"indices_clouds={repr(self.indices_clouds)}, "
            f"value_clouds={repr(self.value_clouds)})"
        )
