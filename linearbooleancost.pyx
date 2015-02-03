from bitset64 import iterate, subsets, size, invert, tostring
from dynamicprogramming import linear_decomposition, booleandim


def linearboolcosttable(graph):
    """
    bctable[A] contains the booleancost of the subtree of all cuts inside A.
    The cut which produced A itself is thus not included.
    """
    booldim = booleandim(graph)

    cdef long v, A, B

    # Init table
    bctable = {}
    for v in iterate(graph.V):
        if graph.N[v] == 0L:
            bctable[v] = 1
        else:
            bctable[v] = 2

    # Solve recurrence
    for A in subsets(graph.V, 2):
        bctable[A] = min(sum([booldim[B], booldim[A - B],
                             bctable[B], bctable[A - B]])
                         for B in iterate(A))

    return bctable, booldim


def linearbooleancost(graph):
    bctable, booldim = linearboolcosttable(graph)
    return (bctable[graph.V],
            booldim,
            list(linear_decomposition(bctable, booldim, graph.V)))

