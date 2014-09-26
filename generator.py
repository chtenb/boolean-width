from graph import Graph, Vertex
from random import choice

def generate_random(nr_vertices, nr_edges):
    assert nr_edges <= nr_vertices ** 2

    graph = Graph()
    for i in range(nr_vertices):
        vertex = Vertex(i)
        graph.add_vertex(vertex)

    for i in range(nr_edges):
        v = choice(graph.vertices)
        w = choice(graph.vertices)
        graph.connect(v, w)

    return graph

