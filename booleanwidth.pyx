from bitset64 import iterate, subsets, tostring, size
from graph64 import Graph
from dynamicprogramming import decomposition, booleandim

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



def booleanwidth(graph):
    bwtable, booldim = boolwidthtable(graph)
    return (bwtable[graph.V],
            booldim,
            list(decomposition(bwtable, booldim, graph.V)))

