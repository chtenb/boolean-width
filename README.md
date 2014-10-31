graph-tools
===========

Tools for generating and analyzing undirected simple graphs.
Developed with `Python 3.4`.

Dependencies
------------
- Python Imaging Library (`PIL`).
- NumPy (`numpy`).
- graphviz https://pypi.python.org/pypi/graphviz

Paradigm
--------
Vertices can be efficiently stored in bitsets.
Bitsets allow set operations to be done in constant time, while enumeration still takes
linear (in the size of the set) time.

Because of this, it is efficient to store vertex neighborhoods as bitsets.
In other words, we have an adjacency matrix, but cut into rows in columns.
So from this perspective, a graph is essentially a collection of vertices and neighborhoods.

A vertex can be identified with a unique number, or alternatively by the bitset containing
only that vertex.

The most efficient syntax for this paradigm would be as follows.
Let `v` be a vertex.
Then `graph[v]` represents the neighborhood of `v`.
Let `X` be a bitset of vertices.
Then `graph[X]` represents the union of the neighborhoods of all vertices in `X`.

To loop over all pairs of connected vertices in linear time,
the iterable `graph.edges` would be appropriate.

