from booleanwidth64 import booleandim
from bitset64 import iterate, subsets


def linearboolwidthtable(graph):
    """
    bwtable[A] contains the booleanwidth of the subtree of all cuts inside A.
    The cut which produced A itself is thus not included.
    """
    booldim = booleandim(graph)

    cdef long v, A, B

    bwtable = {}
    for v in iterate(graph.V):
        bwtable[v] = 2

    print('Solving recurrence')

    for A in subsets(graph.V, 2):
        bwtable[A] = min(max(booldim[B], booldim[A - B],
                             bwtable[B], bwtable[A - B])
                         for B in iterate(A))

    return bwtable, booldim


#def linearbooleanwidth_decomposition(bwtable, booldim, A):
    #assert isinstance(A, BitSet)
    #bound = bwtable[A]
    #if len(A) > 1:
        #for B in A.subsets(1, 1):
            #assert B in A
            #if (bwtable[B] <= bound and booldim[B] <= bound
                    #and booldim[A - B] <= bound and bwtable[A - B] <= bound):
                ##print(bound, bwtable[B], bwtable[A - B])
                #yield (B, A - B)
                #yield from linearbooleanwidth_decomposition(bwtable, booldim, B)
                #yield from linearbooleanwidth_decomposition(bwtable, booldim, A - B)
                ## print(B)
                ##booleanwidth_decomposition(bwtable, B, rec+1)
                ##booleanwidth_decomposition(bwtable, A - B, rec+1)

                #break


def linearbooleanwidth(graph):
    bwtable, booldim = linearboolwidthtable(graph)
    return bwtable[graph.V]
    #print('Computing decomposition')
    #return (bwtable[graph.vertices],
            #booldim,
            #list(linearbooleanwidth_decomposition(bwtable, booldim, graph.vertices)))


