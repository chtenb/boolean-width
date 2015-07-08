graph-tools
===========
This repository contains academic (read: hardly documented and messy) code for computing
boolean-width related things on undirected graphs.
Developed for `Python 3.4+` in combination with Cython.
Warning: since developing this code has been an ongoing process throughout my thesis time,
the code may be inconsistent or broken.
However, the code is free to explore and use as a starting base for developing your own code.

Related publications:
- Masters thesis (link to be provided)
- Linear boolean-width (link to be provided)

Dependencies
------------
- `PIL` (Python Imaging Library)
- `graphviz` https://pypi.python.org/pypi/graphviz
- `sage`
- `cython`

We use the sage library to compute the treewidth or pathwidth of small graphs.

Bitset Paradigm
---------------
Vertices can be efficiently stored in bitsets.
Bitsets allow set operations to be done in approximately constant time,
while enumeration still takes linear (in the size of the set) time.

Because of this, it is efficient to store vertex neighborhoods as bitsets.
In other words, we store the rows and columns from the adjacency matrix separately.
From this perspective, a graph is essentially a collection of vertices and neighborhoods,
i.e. a linear sized collection of numbers.

A vertex can be identified with a unique number `i`, or alternatively by the bitset containing
only that vertex, in this case `2^i`.
We use the latter representation throughout the code, because it has several advantages.

Check out the definitions of `bitset.py` and `graph.py` for more details.

###Bitset class
At first I implemented an object oriented bitset class, which can be found in `bitset.py`
under "OO implementation".
This class supports some nice syntactic constructs by overriding several special methods.
However, the function call overhead appeared to be substantial, which is the reason that
I recommend using pythons plain builtin integers. This datatype doesn't have this method
call overhead, probably has several smart optimizations and allows arbitrary sized bitsets.
For convenience I implemented utility functions for common bitset operations, which can be
found in `bitset.py` under "Procedural implementation".

###Fixed bitset size optimization
A performance boost can be gained by using static `uint128` ints as bitsets, instead of our
own bitset type.
We can implement this using Cython.
Two drawbacks are that we don't have pretty syntax and that we can only store so much vertices.
(64 for `unsigned long` and 128 for `unsigned long long`)
The corresponding functionality can be found in `bitset128.pyx`.

Computing #UN
-------------
For the precomputation of #UN several methods have been proposed in the litearature.
We provide a slow and straightforward implementation in `mis.py` and `mis128.pyx`
via computing #MIS.
But as pointed out in the linear boolean-width paper, we can do it worst case assymptotically
faster using #UN directly in the case of linear boolean-width.
This is easier and the corresponding code can be found in `lboolw.pyx`.


Algorithms
----------
All exact algorithms are based upon dynamic programming.
The code for computing the width and cost versions of boolean-width and linear boolean-width
can be found in `boolw.pyx`, `boolc.pyx`, `lboolw.pyx`, `lboolc.pyx`.

Heuristics can be found in `heuristics.pyx`.

Experiments
-----------
In the subpackage `experiments`, the code of the randomized experiments published in my thesis
and the linear boolean-width paper.

All modules starting width "test" contain messy testing code.
