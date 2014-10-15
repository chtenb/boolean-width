from random import choice


class Vertex:

    def __init__(self, identifier):
        self.identifier = identifier
        self.neighbours = {}

    def __repr__(self):
        return str(self.identifier)

    def __eq__(self, other):
        return self.identifier == other.identifier

    def __str__(self):
        return '{}: {}'.format(self.identifier, self.neighbours)

    def add_neighbour(self, neighbour):
        """Add a neighbour."""
        assert isinstance(neighbour, Vertex)

        self.neighbours[neighbour.identifier] = neighbour


class Edge:

    def __init__(self, v, w):
        self.v = v
        self.w = w

    def __repr__(self):
        return str((self.v, self.w))

    def __eq__(self, other):
        return (self.v == other.v and self.w is other.w
                or
                self.v == other.w and self.w is other.v)

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
        # Dictionary from identifiers to vertices
        self._vertices = {}
        # Dictionary from vertex identifier pairs to edges
        self._edges = {}

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

    def add_vertex(self, v):
        """Add a new vertex to the graph."""
        if not isinstance(v, Vertex):
            raise ValueError
        if v.identifier in self.vertices:
            raise ValueError

        self.vertices[v.identifier] = v

    def connect(self, v, w):
        """Connect two vertices."""
        if not v.identifier in self.vertices:
            raise ValueError
        if not w.identifier in self.vertices:
            raise ValueError
        if w.identifier in v.neighbours:
            raise ValueError
        if v.identifier in w.neighbours:
            raise ValueError

        edge = Edge(v, w)
        v.add_neighbour(w)
        w.add_neighbour(v)
        self.edges[(v.identifier, w.identifier)] = edge

    def complement(self):
        """Construct a graph representing the complement of self."""
        graph = Graph()

        for identifier in self.vertices:
            v_new = Vertex(identifier)
            graph.add_vertex(v_new)

        for v in graph.vertices.values():
            for w in graph.vertices.values():
                old_v = self.vertices[v.identifier]
                old_w = self.vertices[w.identifier]
                if (not old_w.identifier in old_v.neighbours
                        and not w.identifier in v.neighbours and not w == v):
                    graph.connect(v, w)

        return graph

    def subgraph(self, vertices):
        """Return a graph which is the subgraph of self induced by given vertex subset."""
        graph = Graph()
        for v in vertices.values():
            assert v.identifier in self.vertices
            new_v = Vertex(v.identifier)
            graph.add_vertex(new_v)
            for w in v.neighbours.values():
                # Only connect if w is already in the graph
                # Otherwise it comes later
                try:
                    new_w = graph.vertices[w.identifier]
                except KeyError:
                    pass
                else:
                    graph.connect(new_v, new_w)

        return graph

    @staticmethod
    def generate_random(nr_vertices, nr_edges):
        if not nr_edges <= nr_vertices * (nr_vertices - 1) / 2:
            raise ValueError

        graph = Graph()
        for i in range(nr_vertices):
            vertex = Vertex(i)
            graph.add_vertex(vertex)

        vertices = list(graph.vertices.values())

        for i in range(nr_edges):
            while 1:
                v = choice(vertices)
                w = choice(vertices)
                # Graphs must be simple
                # And we don't want to connect vertices twice
                if v != w and not w.identifier in v.neighbours:
                    break
            graph.connect(v, w)

        return graph
