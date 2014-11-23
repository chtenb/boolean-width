from booleanwidth64 import booleandim
from bitset64 import iterate, subsets, length


def linearboolwidthtable(graph):
    """
    bwtable[A] contains the booleanwidth of the subtree of all cuts inside A.
    The cut which produced A itself is thus not included.
    """
    booldim = booleandim(graph)

    cdef long v, A, B

    bwtable = {}
    for v in iterate(graph.V):
        if graph.N[v] == 0L:
            bwtable[v] = 1
        else:
            bwtable[v] = 2

    #print('Solving recurrence')

    for A in subsets(graph.V, 2):
        bwtable[A] = min(max(booldim[B], booldim[A - B],
                             bwtable[B], bwtable[A - B])
                         for B in iterate(A))

    return bwtable, booldim


def linearbooleanwidth_decomposition(bwtable, booldim, long A):
    bound = bwtable[A]
    if length(A) > 1:
        for B in iterate(A):
            if (bwtable[B] <= bound and booldim[B] <= bound
                    and booldim[A - B] <= bound and bwtable[A - B] <= bound):
                yield (B, A - B)
                yield from linearbooleanwidth_decomposition(bwtable, booldim, B)
                yield from linearbooleanwidth_decomposition(bwtable, booldim, A - B)

                break


def linearbooleanwidth(graph):
    bwtable, booldim = linearboolwidthtable(graph)
    #return bwtable[graph.V]
    #print('Computing decomposition')
    return (bwtable[graph.V],
            booldim,
            list(linearbooleanwidth_decomposition(bwtable, booldim, graph.V)))


def linearbooleanwidth_from_decomposition(booldim, decomposition):
    return max(booldim[A] for _, A in decomposition)
