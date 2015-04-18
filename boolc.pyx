from bitset128 import iterate, subsets, tostring, size
from dynamicprogramming import booldimtable


def boolcosttable(graph):
    """
    bctable[A] contains the booleancost of the subtree of all cuts inside A.
    The cut which produced A itself is thus not included.
    """
    booldim = booldimtable(graph)

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
        bctable[A] = booldim[A] + min(bctable[B] + bctable[A - B] for B in subsets(A, 1, -2))

    print(bctable)
    return bctable, booldim


def decomposition(table, booldim, long A):
    """Reconstruct optimal tree decomposition from DP table."""
    bound = table[A]
    if size(A) > 1:
        for B in subsets(A, 1, -2):
            if table[B] + table[A - B] + booldim[A] == bound:
                yield (B, A - B)
                yield from decomposition(table, booldim, B)
                yield from decomposition(table, booldim, A - B)

                break


def booleancost(graph):
    bctable, booldim = boolcosttable(graph)
    return (bctable[graph.V],
            booldim,
            list(decomposition(bctable, booldim, graph.V)))

