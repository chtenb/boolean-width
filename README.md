graph-tools
===========

Tools for generating and analyzing undirected simple graphs.
Developed with `Python 3.4`.

Dependencies
------------
- `PIL` (Python Imaging Library)
- `numpy`
- `graphviz` https://pypi.python.org/pypi/graphviz

Paradigm
--------
Vertices can be efficiently stored in bitsets.
Bitsets allow set operations to be done in constant time, while enumeration still takes
linear (in the size of the set) time.

Because of this, it is efficient to store vertex neighborhoods as bitsets.
In other words, we store the rows and columns from the adjacency matrix separately.
From this perspective, a graph is essentially a collection of vertices and neighborhoods.

A vertex can be identified with a unique number, or alternatively by the bitset containing
only that vertex. We use the latter representation throughout the code, because it has
several advantages.

The syntax we use to support this paradigm is as follows.
Let `X` be a bitset of vertices.
Then `graph(X)` represents the union of the neighborhoods of all vertices in `X`.
and `graph[X]` represents the union of the neighborhoods of all vertices in `X`, together with
`X` itself.

Check out the definitions of `BitSet` and `Graph` for more details.

