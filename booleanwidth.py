from mis import bron_kerbosch_mis
from bipartite import Bipartite
from graph import Vertex, VertexSet
from itertools import combinations


def cutsets(vertices):
    for k in range(len(vertices) + 1):
        yield from (VertexSet(subset, hashcode=i)
                    for i, subset in enumerate(combinations(vertices, k)))


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


def booleanwidth(graph):
    booldim = {}

    # Precompute all values of booldim
    for subset in cutsets(graph.vertices):
        booldim[subset] = len(list(bron_kerbosch_mis(cut(graph, subset))))

    assert len(booldim) == 2 ** len(graph.vertices)

    return booldim
