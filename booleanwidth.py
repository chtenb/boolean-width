from mis import bron_kerbosch_mis, bron_kerbosch_mis_count
from bipartite import Bipartite
from bitset import BitSet


def cut(graph, vertices):
    """Return the bipartite graph of cut induced by given vertex subset."""
    complement = graph.vertices - vertices
    result = Bipartite(vertices, complement)

    for v in vertices:
        result.neighborhoods[v] = graph[v] & complement

    for v in complement:
        result.neighborhoods[v] = graph[v] & vertices

    return result


def booleandim(graph):

    print('Computing booldim')
    booldim = {}
    for subset in graph.vertices.subsets(1, len(graph.vertices) - 1):
        #print('Processing subset ' + str(subset))
        if not subset in booldim:
            complement = graph.vertices - subset
            #result = len(list(bron_kerbosch_mis(cut(graph, subset))))
            result = bron_kerbosch_mis_count(cut(graph, subset))
            booldim[subset] = result
            booldim[complement] = result

    # Verify size
    assert len(booldim) == 2 ** len(graph.vertices) - 2

    # Verify symmetry
    print('Verify booldim symmetry')
    for subset in graph.vertices.subsets(1, len(graph.vertices) - 1):
        complement = graph.vertices - subset
        assert booldim[subset] == booldim[complement]

    return booldim


def boolwidthtable(graph):
    """
    bwtable[A] contains the booleanwidth of the subtree of all cuts inside A.
    The cut which produced A itself is thus not included.
    """
    booldim = booleandim(graph)

    bwtable = {}
    for v in graph:
        bwtable[v] = 2

    print('Solving recurrence')

    for A in graph.vertices.subsets(2):
        bwtable[A] = min(max(booldim[B], booldim[A - B],
                             bwtable[B], bwtable[A - B])
                         for B in A.subsets(1, len(A) - 1))

    return bwtable, booldim


def booleanwidth_decomposition(bwtable, booldim, A):
    bound = bwtable[A]
    if len(A) > 1:
        for B in A.subsets(1, len(A) - 1):
            if (bwtable[B] <= bound and booldim[B] <= bound
                    and booldim[A - B] <= bound and bwtable[A - B] <= bound):

                yield (B, A - B)
                yield from booleanwidth_decomposition(bwtable, booldim, B)
                yield from booleanwidth_decomposition(bwtable, booldim, A - B)
                break


def booleanwidth(graph):
    bwtable, booldim = boolwidthtable(graph)
    print('Computing decomposition')
    return (bwtable[graph.vertices],
            booldim,
            list(booleanwidth_decomposition(bwtable, booldim, graph.vertices)))
