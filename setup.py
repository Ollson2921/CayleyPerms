from setuptools import setup, find_namespace_packages

setup(
    name="cayley_perms",
    version="1.0",
    description="A module for using Cayley permutations.",
    author="Reed Acton, Christian Bean, and Abigail Ollson",
    author_email="c.n.bean@keele.ac.uk",
    packages=find_namespace_packages(),
    install_requires=[
        "comb_spec_searcher @ git+https://github.com/PermutaTriangle/comb_spec_searcher",
        "tqdm",
    ],  # external packages as dependencies
)
