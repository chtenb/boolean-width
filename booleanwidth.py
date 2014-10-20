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
    booldim = {}

    # Precompute all values of booldim
    for subset in subsets(graph.vertices, 1, len(graph.vertices) - 1):
        booldim[BitSet(subset)] = len(list(bron_kerbosch_mis(cut(graph, subset))))

    assert len(booldim) == 2 ** len(graph.vertices) - 2

    return booldim


def boolwidthtable(graph):
    booldim = booleandim(graph)
    vertices = BitSet(graph.vertices)

    bwtable = {}
    for b in vertices:
        bwtable[b] = 2

    for A in subbitsets(vertices, 2):
        bwtable[A] = min(max(booldim[B], booldim[A - B],
                             bwtable[B], bwtable[A - B])
                         for B in subbitsets(A, 1, len(A) - 1))

    print(booldim.values())
    print(bwtable.values())
    return bwtable


def booleanwidth_decomposition(bwtable, A):
    assert isinstance(A, BitSet)
    bound = bwtable[A]
    if len(A) > 1:
        for B in subbitsets(A, 1, len(A) - 1):
            if bwtable[B] <= bound:
                yield B
                yield from booleanwidth_decomposition(bwtable, B)
                yield from booleanwidth_decomposition(bwtable, A - B)
                break


def booleanwidth(graph):
    bwtable = boolwidthtable(graph)
    vbitset = BitSet(graph.vertices)
    return (bwtable[vbitset], list(booleanwidth_decomposition(bwtable, vbitset)))


def booleancost(graph):
    booldim = booleandim(graph)

    # For a fast shortcut we explicitly have hashes as keys
    boolcost = {}
    for v in graph.vertices:
        vbitset = BitSet([v])
        boolcost[vbitset] = 2  # booldim[hash(vset)]

    for k in range(2, len(graph.vertices) + 1):
        for subset in combinations(graph.vertices, k):
            A = BitSet(subset)
            boolcost[A] = min(booldim[B] + booldim[A - B] +
                              boolcost[B] + boolcost[A - B]
                              for B in subsets(subset))

    # Reconstruct decomposition tree
    print(list(booleancost_decomposition(boolcost, graph.vertices)))

    # print(booldim.values())
    # print(boolcost.values())
    return boolcost[BitSet(graph.vertices)]


def booleancost_decomposition(boolcost, vbitset):
    # TODO: make this work correctly
    cost = boolcost[vbitset]
    A = vbitset
    if len(A) > 1:
        for B in subsets(A):
            if boolcost[B] == cost:
                yield B
                booleanwidth_decomposition(boolcost, B)
                booleanwidth_decomposition(boolcost, A - B)
                break
