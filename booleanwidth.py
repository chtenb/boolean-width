from copy import deepcopy
from mis import bron_kerbosch_mis
from bipartite import Bipartite
from vertex import BitSet
from itertools import combinations


def subsets(vertices, minsize=None, maxsize=None):
    """Return subsets from specified size ordered by size ascending."""
    minsize = minsize or 0
    maxsize = maxsize or len(vertices)
    for k in range(minsize, maxsize + 1):
        yield from combinations(vertices, k)
    # yield from (BitSet(i) for i in range(1, 2 ** (len(vertices) - 1)))
    # for k in range(1, len(vertices)):
        # yield from (BitSet(subset) for subset in combinations(vertices, k))


def subbitsets(vertices, minsize=None, maxsize=None):
    """Return subbitsets from specified size ordered by size ascending."""
    minsize = minsize or 0
    maxsize = maxsize or len(vertices)
    for k in range(minsize, maxsize + 1):
        yield from (BitSet(b) for b in combinations(vertices, k))


def cut(graph, vertices):
    """Return the bipartite graph of cut induced by given vertex subset."""
    vertices = deepcopy(vertices)
    complement = deepcopy([v for v in graph.vertices if v not in vertices])

    bvertices = BitSet(vertices)
    bcomplement = BitSet(complement)

    for v in vertices:
        v.neighbors &= bcomplement

    for v in complement:
        v.neighbors &= bvertices

    return Bipartite(vertices, complement)


def booleandim(graph):
    print('Computing booldim')
    booldim = {}
    for subset in subsets(graph.vertices, 1, len(graph.vertices) - 1):
        print('Processing subset ' + str(subset))
        subbitset = BitSet(subset)
        if not subbitset in booldim:
            complement = BitSet(graph.vertices) - subbitset
            result = len(list(bron_kerbosch_mis(cut(graph, subset))))
            booldim[subbitset] = result
            booldim[complement] = result

    assert len(booldim) == 2 ** len(graph.vertices) - 2

    # Verify symmetry
    #print('Verify booldim symmetry')
    #for subset in subsets(graph.vertices, 1, len(graph.vertices) - 1):
        #set1 = BitSet(subset)
        #set2 = BitSet(graph.vertices) - set1
        #assert booldim[set1] == booldim[set2]

    return booldim


def boolwidthtable(graph):
    """
    bwtable[A] contains the booleanwidth of the subtree of all cuts inside A.
    The cut which produced A itself is thus not included.
    """
    booldim = booleandim(graph)
    vertices = BitSet(graph.vertices)

    bwtable = {}
    for b in vertices:
        bwtable[b] = 2

    print('Solving recurrence')

    for A in subbitsets(vertices, 2):
        bwtable[A] = min(max(booldim[B], booldim[A - B],
                             bwtable[B], bwtable[A - B])
                         for B in subbitsets(A, 1, len(A) - 1))

    return bwtable, booldim


def booleanwidth_decomposition(bwtable, booldim, A, rec=0):
    assert isinstance(A, BitSet)
    bound = bwtable[A]
    if len(A) > 1:
        for B in subbitsets(A, 1, len(A) - 1):
            assert B in A
            if (bwtable[B] <= bound and booldim[B] <= bound
                    and booldim[A - B] <= bound and bwtable[A - B] <= bound):
                #print(bound, bwtable[B], bwtable[A - B])
                yield (B, A - B)
                yield from booleanwidth_decomposition(bwtable, booldim, B)
                yield from booleanwidth_decomposition(bwtable, booldim, A - B)
                # print(B)
                #booleanwidth_decomposition(bwtable, B, rec+1)
                #booleanwidth_decomposition(bwtable, A - B, rec+1)

                break


def booleanwidth(graph):
    bwtable, booldim = boolwidthtable(graph)
    vbitset = BitSet(graph.vertices)
    print('Computing decomposition')
    return bwtable[vbitset], booldim, list(booleanwidth_decomposition(bwtable, booldim, vbitset))
