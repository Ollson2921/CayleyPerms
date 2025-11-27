"""sorting all bases into a file of success and a file of failures"""

from cayley_permutations import CayleyPermutation, Av
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from comb_spec_searcher import CombinatorialSpecificationSearcher
from tilescope import TileScopePack
import json


basis_desc = "3s_4x1"  # change descriptor to change file
# basis_desc = "3s"

successes_3s = []

for part in range(31):
    try:
        with open(f"summaries/did_compute_{basis_desc}_part_{part}.txt", "r") as f:
            successes = eval(f.readline())
        successes_3s.extend(successes)
    except FileNotFoundError:
        continue
    try:
        with open(f"long_run/did_compute_{basis_desc}_part_{part}.txt", "r") as f:
            long_run_successes = eval(f.readline())
        successes_3s.extend(long_run_successes)
    except FileNotFoundError:
        continue

successes_3s = set(successes_3s)

print("successes:", len(set(successes_3s)))
with open(f"successes_{basis_desc}.txt", "w") as f:
    f.write(repr(set(successes_3s)))


with open(f"to_run/to_run_{basis_desc}.txt", "r") as f:
    all_bases = eval(f.readline())

failures_3s = []
for basis in all_bases:
    if any(len(cperm) == 3 for cperm in basis):
        if basis not in successes_3s:
            failures_3s.append(basis)
print("total failures:", len(set(failures_3s)))

print(len(set(successes_3s)) + len(set(failures_3s)))
print(len(set(all_bases)))


with open(f"failures_{basis_desc}.txt", "w") as f:
    f.write(repr(set(failures_3s)))
