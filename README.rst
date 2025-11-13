###############################
CayleyPerms
###############################

CayleyPerms is a repository for working with Cayley permutations which contains 5 python libraries; ``cayley_permutations``, ``decorated_patterns``, ``gridded_cayley_permutations``, ``mesh_patterns`` and ``tilescope``.

A Cayley permutation is a word ``π ∈ ℕ*`` such that every number between 1 and the maximum value of ``π`` appears at least once. Cayley permutations can be seen as a generalisation of permutations where repeated values are allowed. Definitions of pattern containment and Cayley permutation classes follow the same ideas as defined for permutations where the patterns contained are also Cayley permutations, so the Cayley permutation class Av(11) describes all permutations. Cayley permutations are in bijection with ordered set partitions.
 
If you need support, you can join us in our `Discord support server`_.

.. _Discord support server: https://discord.gg/ngPZVT5

==========
Installing
==========

To install CayleyPerms on your system, run the following after cloning the repository:

.. code-block:: bash

    pip install .

It is also possible to install in development mode to work on the
source code, in which case you run the following after cloning the repository:

.. code-block:: bash

    pip install -e .
    

========================
Using CayleyPerms
========================

The ``cayley_permutations`` module can be used to create Cayley permutations, avoidance classes and fully simplified bases from a string. The input to ``CayleyPermutation`` is a zero-based Cayley permutation and can be created using any iterable. Printing Cayley permutations creates a zero-based string or the function ``ascii_plot`` creates a plot. A basis is an iterable of Cayley permutations. A basis can also be created using the function ``string_to_basis`` which takes a string of zero-based or one-based Cayley permutations separated by anything and creates a tuple of ``CayleyPermutation``.

.. code-block:: python

    >>> from cayley_permutations import CayleyPermutation, string_to_basis
    >>> cperm = CayleyPermutation([0, 1, 2])
    >>> print(cperm)
    012
    >>> print(cperm.ascii_plot())
       |   |   |
    ---+---+---●---
       |   |   |
    ---+---●---+---
       |   |   |
    ---●---+---+---
       |   |   |
    >>> basis = [cperm, CayleyPermutation([1, 2, 0])]
    >>> print(basis)
    [CayleyPermutation((0, 1, 2)), CayleyPermutation((1, 2, 0))]
    >>> basis = string_to_basis("012, 231")
    >>> print(basis)
    (CayleyPermutation((0, 1, 2)), CayleyPermutation((1, 2, 0)))

A basis can be used to check if a Cayley permutation contains or avoids it. Alternatively, the class `Av` can be used to check if a Cayley permutation is in the Cayley permutation class. It can also be used to generate all Cayley permutations in the class of a certain length, or count how many Cayley permutations are in the class up to that length, both by brute force.

.. code-block:: python

    >>> from cayley_permutations import CayleyPermutation, string_to_basis, Av
    >>> cperm = CayleyPermutation([0, 1, 2, 3])
    >>> basis = string_to_basis("123, 231")
    >>> print(cperm.contains(basis))
    True
    >>> print((cperm.avoids(basis))
    False
    >>> print(Av(basis).in_class(cperm))
    False
    >>> print(Av(basis).generate_cperms(3))
    [CayleyPermutation((2, 1, 0)), CayleyPermutation((1, 0, 2)), CayleyPermutation((1, 1, 0)), CayleyPermutation((2, 0, 1)), CayleyPermutation((0, 2, 1)), CayleyPermutation((1, 0, 1)), CayleyPermutation((0, 1, 1)), CayleyPermutation((1, 0, 0)), CayleyPermutation((0, 1, 0)), CayleyPermutation((0, 0, 1)), CayleyPermutation((0, 0, 0))]
    >>> print(Av(basis).counter(10))
    [1, 1, 3, 11, 41, 145, 483, 1531, 4677, 13925, 40775]
    
The modules ``gridded_cayley_permutations`` and ``tilescope`` are used to find generating functions for Cayley permutation classes using the ``comb_spec_searcher`` module. By changing the basis in the following code the searcher will try to find a combinatorial specification for the corresponding Cayley permutation class. Note that not all classes can be counted with the following code and the argument ``max_expansion_time`` can be used to set the maximum amount of time the algorithm is run for. It is currently set to 10 minutes.

.. code-block:: python

    >>> from cayley_permutations import string_to_basis
    >>> from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
    >>> from comb_spec_searcher import (
    >>>     CombinatorialSpecificationSearcher,
    >>> )
    >>> from tilescope import TileScopePack
    >>> basis = "120,201,1010"  # Input basis
    >>> start_class = Tiling(
    >>>     [GriddedCayleyPerm(p, [(0, 0) for _ in p]) for p in string_to_basis(basis)],
    >>>     [],
    >>>     (1, 1),
    >>> )
    >>> searcher = CombinatorialSpecificationSearcher(start_class, TileScopePack.point_placement())
    >>> spec = searcher.auto_search(max_expansion_time=600) # Set max time to run the algorithm
    [I 251104 12:30:01 comb_spec_searcher:515] Auto search started
        Initialising CombSpecSearcher for the combinatorial class:
        +-+
        |0|
        +-+
        Key:
        0: Av(120,201,1010)
        Crossing obstructions:
    
        Looking for recursive combinatorial specification with the strategies:
        Inferral: Removed empty rows and columns, Separate rows and columns
        Initial: Factor the tiling into factors, Separate rows and columns allowing interleaving in top/bottom rows
        Verification: verify atoms
        Set 1: Cell Insertion, Point placement
    
    [I 251104 12:30:03 comb_spec_searcher:554] Specification detected.
    [I 251104 12:30:03 base:307] Minimizing for 0 seconds.
    [I 251104 12:30:03 base:268] Found specification with 15 rules.
    [I 251104 12:30:04 comb_spec_searcher:470] Specification built
        Time taken: 0:00:02
        CSS status:
            Total time accounted for: 0:00:02
                                                                                     Number of                                Number of
                                                                                  applications    Time spent    Percentage        rules
            ------------------------------------------------------------------  --------------  ------------  ------------  -----------
            Point placement                                                                 19       0:00:01           76%           54
            verify atoms                                                                   215       0:00:00            0%           13
            Removed empty rows and columns                                                 149       0:00:00            0%          104
            Separate rows and columns                                                       76       0:00:00           10%           14
            has specification                                                               21       0:00:00            0%            -
            Factor the tiling into factors                                                  76       0:00:00            0%           30
            Separate rows and columns allowing interleaving in top/bottom rows              46       0:00:00            7%            4
            Cell Insertion                                                                  19       0:00:00            2%           38
            add rule                                                                       257       0:00:00            1%            -
    
        ClassDB status:
            Total number of combinatorial classes found is 218
            is_empty check applied 105 time. Time spent: 0:00:00
        Queue status (currently on level 4):
            Queue              Size
            ---------------  ------
            working              26
            current (set 1)      49
            next                 22
            The size of the current queues at each level: 1, 2, 19, 66
        RuleDB status:
                                                       Total number
            ---------------------------------------  --------------
            Combinatorial rules                                  76
            Equivalence rules                                   154
            Combintorial rules up to equivalence                 76
            Strategy verified combinatorial classes              13
            Verified combinatorial classes                       54
            combinatorial classes up to equivalence              71
            Called find equiv path 21 times, for total time of 0.0 seconds.
    
        Memory Status:
            ------------  --------
            OS Allocated  74.2 MiB
            CSS            2.1 MiB
            ClassDB        1.9 MiB
            ClassQueue      32 KiB
            RuleDB         2.1 MiB
            ------------  --------
        Specification found has 35 rules

The specification returned is a ``CombinatorialSpecification`` from the ``comb_spec_searcher`` module. To view a ``CombinatorialSpecification`` you can use ``print(spec)`` for a string representation or use ``spec.show()`` to see the specification in a proof tree format.
There are many useful functions on ``CombinatorialSpecification``, in particular from a specification a generating function can be found as well as a faster method for counting the number of Cayley permutations in the class.

.. code-block:: python

    >>> spec.get_genf()
    [I 251104 12:29:42 specification:397] Computing initial conditions
    [I 251104 12:29:42 specification:371] Computing initial conditions
    [I 251104 12:29:42 specification:399] The system of 35 equations
        root_func := F_0:
        eqs := [
        F_0 = F_1 + F_2,
        F_1 = 1,
        F_2 = F_3,
        F_3 = F_34*F_4,
        F_4 = F_5,
        F_5 = F_28 + F_6,
        F_6 = F_7,
        F_7 = F_12 + F_8,
        F_8 = F_9,
        F_9 = F_10 + F_11,
        F_10 = F_0,
        F_11 = F_3,
        F_12 = F_13,
        F_13 = F_14*F_15*F_21,
        F_14 = F_0,
        F_15 = F_16,
        F_16 = F_1 + F_17,
        F_17 = F_18,
        F_18 = F_19*F_20,
        F_19 = F_16,
        F_20 = x,
        F_21 = F_22,
        F_22 = F_23,
        F_23 = F_24*F_26*F_27,
        F_24 = F_25,
        F_25 = F_1 + F_22,
        F_26 = F_16,
        F_27 = x,
        F_28 = F_29,
        F_29 = F_30*F_31*F_32*F_33,
        F_30 = F_11,
        F_31 = F_16,
        F_32 = F_25,
        F_33 = F_17,
        F_34 = x
        ]:
        count := [1, 1, 3, 11, 41, 151, 553]:
    [I 251104 12:29:42 specification:405] Solving...
    [I 251104 12:29:43 specification:416] Checking initial conditions for: (2*x**3 - 4*x**2 + 4*x - 1)/(4*x**3 - 6*x**2 + 5*x - 1)
    >>> print([spec.count_objects_of_size(i) for i in range(10)])
    [1, 1, 3, 11, 41, 151, 553, 2023, 7401, 27079]
