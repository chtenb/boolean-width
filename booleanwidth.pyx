from bitset64 import iterate, subsets, tostring, size
from dynamicprogramming import booleandim

def boolwidthtable(graph):
    """
    bwtable[A] contains the booleanwidth of the subtree of all cuts inside A.
    The cut which produced A itself is thus not included.
    """
    booldim = booleandim(graph)

    # Init table
    bwtable = {}
    for v in iterate(graph.V):
        if graph.N[v] == 0L:
            bwtable[v] = 1
        else:
            bwtable[v] = 2

    # Solve recurrence
    for A in subsets(graph.V, 2):
        try:
            bwtable[A] = min(max(booldim[B],
                booldim[A - B],
                                 bwtable[B],
                                 bwtable[A - B])
                             for B in subsets(A, 1, -2))
        except KeyError:
            for B in subsets(A):#, 1, -1):
                print(tostring(B))
            exit()

    return bwtable, booldim


def decomposition(table, booldim, long A):
    """Reconstruct optimal tree decomposition from DP table."""
    bound = table[A]
    if size(A) > 1:
        for B in subsets(A, 1, -2):
            if (table[B] <= bound and booldim[B] <= bound
                    and booldim[A - B] <= bound and table[A - B] <= bound):
                yield (B, A - B)
                yield from decomposition(table, booldim, B)
                yield from decomposition(table, booldim, A - B)

                break


def booleanwidth(graph):
    bwtable, booldim = boolwidthtable(graph)
    return (bwtable[graph.V],
            booldim,
            list(decomposition(bwtable, booldim, graph.V)))

