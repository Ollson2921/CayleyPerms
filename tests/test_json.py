"""Test the to_json and from_json methods of CayleyPermutation, GriddedCayleyPerm, Tiling,
and RowColMap."""

import json
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import GriddedCayleyPerm, Tiling, RowColMap


def test_cayley_perm_json():
    """Test the to_json and from_json methods of CayleyPermutation."""
    for cperm in CayleyPermutation.of_size(4):
        assert cperm == CayleyPermutation.from_dict(
            json.loads(json.dumps(cperm.to_jsonable()))
        )


def test_gridded_cayley_perm_json():
    """Test the to_json and from_json methods of GriddedCayleyPerm."""
    for cperm in CayleyPermutation.of_size(4):
        gcp = GriddedCayleyPerm(cperm, [(0, 0), (0, 0), (0, 0), (0, 0)])
        assert gcp == GriddedCayleyPerm.from_dict(
            json.loads(json.dumps(gcp.to_jsonable()))
        )


def test_tiling_json():
    """Test the to_json and from_json methods of Tiling."""
    for cperm in CayleyPermutation.of_size(4):
        gcp1 = GriddedCayleyPerm(cperm, [(0, 0), (0, 0), (0, 0), (0, 0)])
        gcp2 = GriddedCayleyPerm(cperm, [(1, 1), (1, 1), (1, 1), (1, 1)])
        gcp3 = GriddedCayleyPerm(cperm, [(0, 1), (0, 1), (0, 1), (0, 1)])
        gcp4 = GriddedCayleyPerm(cperm, [(1, 0), (1, 0), (1, 0), (1, 0)])
        tiling = Tiling([gcp1], [[gcp2, gcp3], [gcp4]], (2, 2))
        assert tiling == Tiling.from_dict(json.loads(json.dumps(tiling.to_jsonable())))


def test_row_col_map_json():
    """Test the to_json and from_json methods of RowColMap."""
    for n in range(5):
        row_col_map = RowColMap({x: 0 for x in range(n)}, {x: 0 for x in range(n)})
        assert row_col_map == RowColMap.from_dict(
            json.loads(json.dumps(row_col_map.to_jsonable()))
        )
