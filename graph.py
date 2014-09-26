
class Vertex:

    def __init__(self, identifier):
        self.identifier = identifier
        self.neighbours = []

    def __repr__(self):
        return str(self.identifier)

    def __str__(self):
        return '{}: {}'.format(self.identifier, self.neighbours)

    def add_neighbour(self, neighbour):
        """Add a neighbour."""
        assert isinstance(neighbour, Vertex)

        self.neighbours.append(neighbour)


class Edge:

    def __init__(self, v, w):
        self.v = v
        self.w = w

    def __repr__(self):
        return str((repr(self.v), repr(self.w)))

    def __str__(self):
        return repr(self)

    def __getitem__(self, index):
        if index == 0:
            return self.v
        if index == 1:
            return self.w
        raise IndexError


class Graph:

    def __init__(self):
        self.vertices = []
        self.edges = []

    def __str__(self):
        return 'vertices: {}, edges: {}'.format(self.vertices, self.edges)

    def add_vertex(self, vertex):
        """Add a new vertex to the graph."""
        assert isinstance(vertex, Vertex)
        assert vertex not in self.vertices

        self.vertices.append(vertex)

    def connect(self, v, w):
        """Connect two vertices."""
        assert v in self.vertices
        assert w in self.vertices

        edge = Edge(v, w)
        v.add_neighbour(w)
        w.add_neighbour(v)
        self.edges.append(edge)

    def save(self, filename):
        pass
