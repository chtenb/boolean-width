
class Vertex:

    def __init__(self, identifier):
        self.identifier = identifier
        self.edges = []

    def __str__(self):
        return '{}: {}'.format(self.identifier, self.edges)

    def add_edge(self, edge):
        self.edges.append(edge)


class Edge:

    def __init__(self, v, w):
        self.v = v
        self.w = w


class Graph:

    def __init__(self):
        self.vertices = []
        self.edges = []

    def add_vertex(self, vertex):
        """Add a new vertex to the graph."""
        assert vertex not in self.vertices

        self.vertices.append(vertex)

    def connect(self, v, w):
        """Connect two vertices."""
        assert v in self.vertices
        assert w in self.vertices

        edge = Edge(v, w)
        self.edges.append(edge)
