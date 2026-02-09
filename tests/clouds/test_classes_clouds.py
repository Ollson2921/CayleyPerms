from clouds import TrackedTileScopePack, TrackedSearcher
from cayley_permutations import Av


def test_some_classes_clouds():
    bases = [
        "012_101_001_010",
        "012_101_010",
        "210_101_011",
        "101_010_011",
        "100_110_010_011",
        "101_010",
        "101_110_010_001_011",
        "100_110_001_011",
        "000_010_100_101_210",
    ]
    for basis in bases:
        pack = TrackedTileScopePack.standard_fusion_pack(expansion_methods=["point"])
        searcher = TrackedSearcher(basis, pack, debug=False, max_cvs=1)
        spec = searcher.auto_search(status_update=5)

        # print(spec.get_maple_equations())

        spec = spec.expand_verified()
        # spec.show()
        spec.sanity_check(4)
        # # spec.show()
        spec_counts = [spec.count_objects_of_size(i) for i in range(10)]
        root_counts = Av(basis).counter(9)
        assert spec_counts == root_counts

        # print("[", end="")
        # for i in range(10):
        #     print(spec.root_rule.comb_class.get_terms(i)[tuple()], end="", flush=True)
        #     if i == 9:
        #         print("]")
        #     else:
        #         print(", ", end="")
