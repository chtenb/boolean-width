from mis import bron_kerbosch_mis
from bipartite import Bipartite
from graph import Vertex
from sets import HashSet, BitSet
from itertools import combinations


def cutsets(vertices):
    """Return a subvertexsets except the empty and the entire set."""
    for k in range(1, len(vertices)):
        yield from (BitSet(subset) for subset in combinations(vertices, k))


def cut(graph, vertices):
    """Return the bipartite graph of cut induced by given vertex subset."""
    result = Bipartite()
    # TODO: this can be done in O(1) time
    complement = BitSet(v for v in graph.vertices if v not in vertices)

    for v in vertices:
        assert v in graph.vertices
        new_v = Vertex(v.identifier)
        result.add_vertex(new_v, group=1)

    for v in complement:
        assert v in graph.vertices
        new_v = Vertex(v.identifier)
        result.add_vertex(new_v, group=2)

    for e in graph.edges:
        if (e.v in vertices and e.w in complement or
                e.w in vertices and e.v in complement):
            result.connect(result.vertices[e.v.identifier],
                           result.vertices[e.w.identifier])

    return result


def booleandim(graph):
    booldim = {}

    # Precompute all values of booldim
    for subset in cutsets(graph.vertices):
        booldim[hash(subset)] = len(list(bron_kerbosch_mis(cut(graph, subset))))

    assert len(booldim) == 2 ** len(graph.vertices) - 2

    return booldim


def boolwidthtable(graph):
    booldim = booleandim(graph)

    bwtable = {}
    for v in graph.vertices:
        vbitset = BitSet([v])
        bwtable[vbitset] = 2  # booldim[hash(vset)]

    for k in range(2, len(graph.vertices) + 1):
        for subset in combinations(graph.vertices, k):
            A = BitSet(subset)
            bwtable[A] = min(max(booldim[B], booldim[A - B],
                                 bwtable[B], bwtable[A - B])
                             for B in cutsets(subset))

    # print(booldim.values())
    # print(boolwidth.values())
    return bwtable


def booleanwidth_decomposition(bwtable, vbitset):
    try:
        assert isinstance(vbitset, BitSet)
        bound = bwtable[vbitset]
    except:
        print(repr(vbitset))
        print(bwtable)
        raise
    A = vbitset
    if len(A) > 1:
        for B in cutsets(A):
            if bwtable[B] <= bound:
                yield B
                booleanwidth_decomposition(bwtable, B)
                booleanwidth_decomposition(bwtable, A - B)
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
                              for B in cutsets(subset))

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
        for B in cutsets(A):
            if boolcost[B] == cost:
                yield B
                booleanwidth_decomposition(boolcost, B)
                booleanwidth_decomposition(boolcost, A - B)
                break
