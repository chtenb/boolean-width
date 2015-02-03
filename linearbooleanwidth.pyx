from bitset64 import iterate, subsets, size, invert, tostring
from dynamicprogramming import linear_decomposition, booleandim


def linearboolwidthtable(graph):
    """
    bwtable[A] contains the booleanwidth of the subtree of all cuts inside A.
    The cut which produced A itself is thus not included.
    """
    booldim = booleandim(graph)

    cdef long v, A, B

    # Init table
    bwtable = {}
    for v in iterate(graph.V):
        if graph.N[v] == 0L:
            bwtable[v] = 1
        else:
            bwtable[v] = 2

    # Solve recurrence
    for A in subsets(graph.V, 2):
        bwtable[A] = min(max(booldim[B], booldim[A - B],
                             bwtable[B], bwtable[A - B])
                         for B in iterate(A))

    return bwtable, booldim


def linearbooleanwidth(graph):
    bwtable, booldim = linearboolwidthtable(graph)
    return (bwtable[graph.V],
            booldim,
            list(linear_decomposition(bwtable, booldim, graph.V)))


def linearbooleanwidth_decomposition_greedy(bwtable, booldim, long A, int universe):
    """A is unprocessed."""
    bound = bwtable[A]
    if size(A) > 1:
        print('trying greedy')
        # Try greedy step
        for B in iterate(A):
            if size(A) == universe:
                greedybound = 1
            else:
                greedybound = booldim[A]

            print('Current booldim', greedybound)
            print(tostring(B), booldim[A - B])
            if booldim[A - B] < greedybound:
                print('choosing {} greedy'.format(tostring(B)))
                yield (B, A - B)
                yield from linearbooleanwidth_decomposition_greedy(bwtable, booldim, B, universe)
                yield from linearbooleanwidth_decomposition_greedy(bwtable, booldim, A - B, universe)
                return
        print('No greedy step found, trying nongreedy')
        # Perform normal reconstruction
        for B in iterate(A):
            if (bwtable[B] <= bound and booldim[B] <= bound
                    and booldim[A - B] <= bound and bwtable[A - B] <= bound):
                print('choosing {} nongreedy'.format(tostring(B)))
                yield (B, A - B)
                yield from linearbooleanwidth_decomposition_greedy(bwtable, booldim, B, universe)
                yield from linearbooleanwidth_decomposition_greedy(bwtable, booldim, A - B, universe)
                return
