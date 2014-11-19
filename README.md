graph-tools
===========

Tools for generating and analyzing undirected simple graphs.
Developed with `Python 3.4`.

Dependencies
------------
- `PIL` (Python Imaging Library)
- `graphviz` https://pypi.python.org/pypi/graphviz
- `sage` 
- `cython` 

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
Let `vertices` be a bitset of vertices.
Then `graph(vertices)` represents the union of the neighborhoods of all vertices in `vertices`,
while `graph[vertices]` represents the union of the neighborhoods of all vertices in `vertices`
together with `vertices` itself.

Check out the definitions of `BitSet` and `Graph` for more details.

Fixed bitset size optimization
------------------------------
A huge performance boost can be gained by using static `long` ints as bitsets, instead of our
own bitset type.
We can implement this using Cython.
Two drawbacks are that we don't have pretty syntax and that we can only store so much vertices.
(64 for `unsigned long`s and 128 for `unsigned long long`s)
