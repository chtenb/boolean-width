from random import choice


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
        return str((self.v, self.w))

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
        self._vertices = []
        self._edges = []

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return self._edges

    def count_vertices(self):
        return len(self.vertices)

    def __str__(self):
        return 'vertices: {}, edges: {}'.format(list(self.vertices), list(self.edges))

    def add_vertex(self, vertex):
        """Add a new vertex to the graph."""
        if not isinstance(vertex, Vertex):
            raise ValueError
        if vertex in self.vertices:
            raise ValueError

        self.vertices.append(vertex)

    def connect(self, v, w):
        """Connect two vertices."""
        if not v in self.vertices:
            raise ValueError
        if not w in self.vertices:
            raise ValueError
        if w in v.neighbours:
            raise ValueError
        if v in w.neighbours:
            raise ValueError

        edge = Edge(v, w)
        v.add_neighbour(w)
        w.add_neighbour(v)
        self.edges.append(edge)

    def complement(self):
        """Construct a graph representing the complement of self."""
        graph = Graph()
        bijection = {}

        for v in self.vertices:
            v_new = Vertex(v.identifier)
            bijection[v_new] = v
            graph.add_vertex(v_new)

        for v in graph.vertices:
            for w in graph.vertices:
                if (not bijection[w] in bijection[v].neighbours
                        and not w in v.neighbours and not w == v):
                    graph.connect(v, w)

        return graph

    @staticmethod
    def generate_random(nr_vertices, nr_edges):
        if not nr_edges <= nr_vertices * (nr_vertices - 1) / 2:
            raise ValueError

        graph = Graph()
        for i in range(nr_vertices):
            vertex = Vertex(i)
            graph.add_vertex(vertex)

        for i in range(nr_edges):
            while 1:
                v = choice(graph.vertices)
                w = choice(graph.vertices)
                # Graphs must be simple
                # And we don't want to connect vertices twice
                if v != w and not w in v.neighbours:
                    break
            graph.connect(v, w)

        return graph
