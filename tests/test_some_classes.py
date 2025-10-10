"""Some tests for quick classes with point placement pack."""

from cayley_permutations import string_to_basis
from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from comb_spec_searcher import (
    CombinatorialSpecificationSearcher,
    CombinatorialSpecification,
)
from tilescope import TileScopePack
import json


def test_pop_stack_sortable():
    """Test the enumeration for pop-stack sortable Cayley permutations."""
    basis = "231,312,2121"
    start_class = Tiling(
        [GriddedCayleyPerm(p, [(0, 0) for _ in p]) for p in string_to_basis(basis)],
        [],
        (1, 1),
    )
    pack = TileScopePack.point_placement()
    searcher = CombinatorialSpecificationSearcher(start_class, pack, debug=False)
    spec = searcher.auto_search()
    assert [spec.count_objects_of_size(i) for i in range(10)] == [
        1,
        1,
        3,
        11,
        41,
        151,
        553,
        2023,
        7401,
        27079,
    ]
    json_dict = spec.to_jsonable()
    json_str = json.dumps(json_dict)
    load_dict = json.loads(json_str)
    reloaded_spec = CombinatorialSpecification.from_dict(load_dict)
    assert spec == reloaded_spec
    assert [spec.count_objects_of_size(i) for i in range(10)] == [
        1,
        1,
        3,
        11,
        41,
        151,
        553,
        2023,
        7401,
        27079,
    ]


def test_012_021():
    """Test the enumeration for a rational class."""
    basis = "012_021"
    start_class = Tiling(
        [GriddedCayleyPerm(p, [(0, 0) for _ in p]) for p in string_to_basis(basis)],
        [],
        (1, 1),
    )
    pack = TileScopePack.point_placement()
    searcher = CombinatorialSpecificationSearcher(start_class, pack, debug=False)
    spec = searcher.auto_search()
    print([spec.count_objects_of_size(i) for i in range(10)])
    assert [spec.count_objects_of_size(i) for i in range(10)] == [
        1,
        1,
        3,
        11,
        43,
        171,
        683,
        2731,
        10923,
        43691,
    ]
    json_dict = spec.to_jsonable()
    json_str = json.dumps(json_dict)
    load_dict = json.loads(json_str)
    reloaded_spec = CombinatorialSpecification.from_dict(load_dict)
    assert spec == reloaded_spec
    assert [spec.count_objects_of_size(i) for i in range(10)] == [
        1,
        1,
        3,
        11,
        43,
        171,
        683,
        2731,
        10923,
        43691,
    ]
