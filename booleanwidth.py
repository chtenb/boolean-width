from mis import bron_kerbosch_mis
from bipartite import Bipartite
from graph import Vertex, VertexSet
from itertools import combinations


def cutsets(vertices):
    """Return a subvertexsets except the empty and the entire set."""
    for k in range(1, len(vertices)):
        yield from (VertexSet(subset) for subset in combinations(vertices, k))


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

    # TODO: make sure this works
    for e in graph.edges:
        if (e.v in vertices and e.w in complement or
                e.w in vertices and e.v in complement):
            result.connect(result.vertices[e.v.identifier],
                           result.vertices[e.w.identifier])

    return result


def booleanwidth(graph):
    booldim = {}

    # Precompute all values of booldim
    for subset in cutsets(graph.vertices):
        booldim[subset] = len(list(bron_kerbosch_mis(cut(graph, subset))))

    assert len(booldim) == 2 ** len(graph.vertices) - 2

    # For a fast shortcut we explicitly have hashes as keys
    boolwidth = {}
    for v in graph.vertices:
        vset = VertexSet([v])
        boolwidth[hash(vset)] = booldim[vset]

    for k in range(2, len(graph.vertices) + 1):
        for subset in combinations(graph.vertices, k):
            A = VertexSet(subset)
            boolwidth[hash(A)] = min(max(booldim[B], boolwidth[hash(B)],
                                         boolwidth[hash(A) - hash(B)])
                                     for B in cutsets(A))

    return boolwidth[hash(graph.vertices)]
