from setuptools import setup

setup(
    name="cayley_perms",
    version="1.0",
    description="A module for using Cayley permutations.",
    author="Reid Acton, Christian Bean, and Abigail Ollson",
    author_email="c.n.bean@keele.ac.uk",
    packages=[
        "cayley_permutations",
        "gridded_cayley_permutations",
        "tilescope_folder",
    ],
    install_requires=["comb_spec_searcher"],  # external packages as dependencies
)
