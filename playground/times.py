from cayley_permutations import CayleyPermutation, Av
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from comb_spec_searcher import CombinatorialSpecificationSearcher
from tilescope import TileScopePack
import json


basis_desc = "3s"  # change descriptor to change file

# The to_run folder contains files with bases to run
with open(f"to_run/to_run_{basis_desc}.txt", "r") as f:
    bases_to_run = eval(f.readline())

bases_subset = bases_to_run[350:400]  # can take a subset of the bases in the file
part = 2


with open(f"summaries/did_compute_{basis_desc}_part_{part}.txt", "r") as f:
    bases_found_specs = eval(f.readline())

n = 0
for basis in bases_subset:
    if basis not in bases_found_specs:
        n += 1

print(f"Basis to compute: {n}")
hours = n * 13 * 2
print(f"Hours: {hours}")
days = hours / 24
print(f"Days: {days}")