from mis import bron_kerbosch_mis
from bipartite import Bipartite
from graph import Vertex
from sets import VertexSet, VertexBitSet
from itertools import combinations


def cutsets(vertices):
    """Return a subvertexsets except the empty and the entire set."""
    for k in range(1, len(vertices)):
        yield from (VertexSet(subset) for subset in combinations(vertices, k))


def cutbitsets(vertices):
    """Return a subvertexbitsets except the empty and the entire set."""
    for k in range(1, len(vertices)):
        yield from (VertexBitSet(subset) for subset in combinations(vertices, k))


def cut(graph, vertices):
    """Return the bipartite graph of cut induced by given vertex subset."""
    result = Bipartite()
    complement = VertexSet(v for v in graph.vertices if v not in vertices)

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


def booleanwidth(graph):
    booldim = booleandim(graph)

    # For a fast shortcut we explicitly have hashes as keys
    boolwidth = {}
    for v in graph.vertices:
        vbitset = VertexBitSet([v])
        boolwidth[vbitset] = 2  # booldim[hash(vset)]

    for k in range(2, len(graph.vertices) + 1):
        for subset in combinations(graph.vertices, k):
            A = VertexBitSet(subset)
            boolwidth[A] = min(max(booldim[B], booldim[A - B],
                                   boolwidth[B], boolwidth[A - B])
                               for B in cutbitsets(subset))
    # Reconstruct decomposition tree
    booleanwidth_decomposition(boolwidth, graph.vertices)

    # print(booldim.values())
    # print(boolwidth.values())
    return boolwidth[hash(graph.vertices)]


def booleanwidth_decomposition(boolwidth, vbitset):
    bound = boolwidth[vbitset]
    A = vbitset
    if len(A) > 1:
        for B in cutsets(A):
            if boolwidth[B] <= bound:
                yield B
                booleanwidth_decomposition(boolwidth, B)
                booleanwidth_decomposition(boolwidth, A - B)
                break


def booleancost(graph):
    booldim = booleandim(graph)

    # For a fast shortcut we explicitly have hashes as keys
    boolcost = {}
    for v in graph.vertices:
        vset = VertexSet([v])
        boolcost[hash(vset)] = 2  # booldim[hash(vset)]

    for k in range(2, len(graph.vertices) + 1):
        for subset in combinations(graph.vertices, k):
            A = VertexSet(subset)
            boolcost[hash(A)] = min(booldim[hash(B)] + booldim[hash(A) - hash(B)] +
                                    boolcost[hash(B)] + boolcost[hash(A) - hash(B)]
                                    for B in cutsets(A))

    # Reconstruct decomposition tree
    print(list(booleancost_decomposition(boolcost, graph.vertices)))

    # print(booldim.values())
    # print(boolcost.values())
    return boolcost[hash(graph.vertices)]


def booleancost_decomposition(boolcost, vset):
    # TODO: make this work correctly
    cost = boolcost[hash(vset)]
    A = vset
    if len(A) > 1:
        for B in cutsets(A):
            if boolcost[hash(B)] == cost:
                yield B
                booleanwidth_decomposition(boolcost, B)
                booleanwidth_decomposition(boolcost, A.minus(B))
                break
