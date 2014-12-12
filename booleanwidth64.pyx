from mis64 import mis_count
from bitset64 import iterate, subsets, tostring, size
from graph64 import Graph


def cut(long V, N, long vertices):
    """Return the neighborhoods of the cut induced by given vertex subset."""
    complement = V - vertices

    newN = {}

    for v in iterate(vertices):
        newN[v] = N[v] & complement

    for v in iterate(complement):
        newN[v] = N[v] & vertices

    return newN


def booleandim(graph):
    #print('Computing booldim')
    V = graph.V
    N = graph.N
    booldim = {}
    for subset in subsets(V, 1, -2):
        #print('Processing subset ' + tostring(subset))
        if not subset in booldim:
            complement = V - subset
            result = mis_count(cut(V, N, subset), V)
            booldim[subset] = result
            booldim[complement] = result

    # Verify size
    assert len(booldim) == 2 ** size(V) - 2

    # Verify symmetry
    #print('Verify booldim symmetry')
    #for subset in subsets(V, 1, -2):
        #complement = V - subset
        #assert booldim[subset] == booldim[complement]

    return booldim


#def boolwidthtable(graph):
    #"""
    #bwtable[A] contains the booleanwidth of the subtree of all cuts inside A.
    #The cut which produced A itself is thus not included.
    #"""
    #booldim = booleandim(graph)

    #bwtable = {}
    #for v in graph:
        #bwtable[v] = 2

    #print('Solving recurrence')

    #for A in graph.vertices.subsets(2):
        #bwtable[A] = min(max(booldim[B], booldim[A - B],
                             #bwtable[B], bwtable[A - B])
                         #for B in A.subsets(1, len(A) - 1))

    #return bwtable, booldim


#def booleanwidth_decomposition(bwtable, booldim, A):
    #bound = bwtable[A]
    #if len(A) > 1:
        #for B in A.subsets(1, len(A) - 1):
            #if (bwtable[B] <= bound and booldim[B] <= bound
                    #and booldim[A - B] <= bound and bwtable[A - B] <= bound):

                #yield (B, A - B)
                #yield from booleanwidth_decomposition(bwtable, booldim, B)
                #yield from booleanwidth_decomposition(bwtable, booldim, A - B)
                #break


#def booleanwidth(graph):
    #bwtable, booldim = boolwidthtable(graph)
    #print('Computing decomposition')
    #return (bwtable[graph.vertices],
            #booldim,
            #list(booleanwidth_decomposition(bwtable, booldim, graph.vertices)))
