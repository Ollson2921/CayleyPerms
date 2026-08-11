import datetime
import logging
import sys
import traceback
from multiprocessing import get_context
from time import time
from typing import List, NamedTuple, Optional

# import dateutil.parser  # type: ignore
import logzero  # type: ignore
import requests

# from db_stuff.spec_checker import SpecChecker
from tqdm import tqdm  # type: ignore

from comb_spec_searcher import CombinatorialSpecification
from cayley_permutations import CayleyPermutation, string_to_basis
from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from tilescope import TileScopePack
from comb_spec_searcher import CombinatorialSpecificationSearcher
from cayley_permutations import Av

import numpy as np

import png
import os
import sys

# sys.setrecursionlimit(2147483647)
# print(f"Recursion limit set to {sys.getrecursionlimit()}.")

# name = "rgf_horizontal_specification"
# # with open(f"{name}.json") as f:
# #     spec = CombinatorialSpecification.from_dict(eval(f.read()))

basis = "10,001"
name = basis
# basis = string_to_basis(basis)
# tiling = Tiling(
#     [GriddedCayleyPerm(p, [(0, 0) for _ in p]) for p in basis],
#     [],
#     (1, 1),
# )
# spec = CombinatorialSpecificationSearcher(
#     tiling, TileScopePack.point_placement()
# ).auto_search()

# basis = (
#     CayleyPermutation((0, 0, 0)),
#     CayleyPermutation((0, 0, 1)),
#     CayleyPermutation((0, 1, 0)),
#     CayleyPermutation((0, 1, 1)),
#     CayleyPermutation((0, 2, 1)),
#     CayleyPermutation((1, 0, 0)),
#     CayleyPermutation((1, 0, 1)),
#     CayleyPermutation((1, 1, 0)),
# )
# name = str(Av(basis))

with open(f"{Av(basis)}.json", "r") as f:
    spec_string = f.read().replace("false", "False").replace("true", "True")
    spec = CombinatorialSpecification.from_dict(eval(spec_string))


# import json

# json_spec = json.dumps(spec.to_jsonable())
# with open(f"{Av(basis)}.json", "w") as f:
#     f.write(json_spec)

sample_length = 200
num_samples = 50

values = [[0 for _ in range(sample_length)] for _ in range(sample_length)]
for _ in range(num_samples + 1):
    cperm = spec.random_sample_object_of_size(sample_length).pattern
    for idx, val in enumerate(cperm):
        values[val][idx] += 1

M = np.array(values)
M = np.flipud(M)


rooter = lambda x: x ** (1 / 3)
Mroot = np.array([rooter(x) for x in M])
max_val = max(map(max, Mroot))

bits = 8
t_max = 2**bits - 1
M = t_max * (1 - Mroot / max_val)

M = M.astype(np.uint8) if bits == 8 else M.astype(np.uint8)

with open(f"samples_specs/{name}.png", "wb") as f:
    w = png.Writer(len(M[0]), len(M), greyscale=True, bitdepth=bits)
    w.write(f, M)
    f.close()
    # os.system(f"pngcrush -brute -newtimestamp .temp.png {file_name}")
    # os.system("rm .temp.png")
