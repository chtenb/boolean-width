from random import choice
from copy import deepcopy
from sets import HashSet, BitSet, NeighbourhoodSet


class Vertex:

    def __init__(self, identifier):
        if not isinstance(identifier, int):
            raise ValueError
        self.identifier = identifier

    def __repr__(self):
        return 'vertex ' + str(self.identifier)

    def __eq__(self, other):
        return self.identifier == other.identifier

    def __hash__(self):
        return 2 ** self.identifier

    def __str__(self):
        return 'Vertex({})'.format(self.identifier)


class Edge:

    def __init__(self, v, w):
        self.v = v
        self.w = w

    def __repr__(self):
        return str((self.v, self.w))

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return (self.v == other.v and self.w is other.w
                or
                self.v == other.w and self.w is other.v)

    def __hash__(self):
        return (2 ** self.v.identifier) * (3 ** self.w.identifier)

    def __getitem__(self, index):
        if index == 0:
            return self.v
        if index == 1:
            return self.w
        raise IndexError



class Graph:

    def __init__(self):
        self.vertices = HashSet()
        self.edges = HashSet()
        self.neighbourhoods = NeighbourhoodSet()

    def __str__(self):
        return 'vertices: {}, edges: {}'.format(list(self.vertices), list(self.edges))

    def __repr__(self):
        return 'vertices: {}, edges: {}'.format(list(self.vertices), list(self.edges))

    def save(self, filename):
        # TODO
        with open(filename, 'w') as f:
            f.write(repr(self))

    def load(self, filename):
        # TODO
        with open(filename, 'r') as f:
            pass

    def add_vertex(self, v):
        """Add a new vertex to the graph."""
        if not isinstance(v, Vertex):
            raise ValueError
        if v in self.vertices:
            raise ValueError

        self.vertices.add(v)

    def connect(self, v, w):
        """Connect two vertices."""
        if not v in self.vertices:
            raise ValueError
        if not w in self.vertices:
            raise ValueError

        edge = Edge(v, w)
        self.edges.add(edge)
        self.neighbourhoods.connect(v, w)

    def complement(self):
        """Construct a graph representing the complement of self."""
        graph = Graph()
        graph.vertices = deepcopy(self.vertices)

        for v in graph.vertices:
            for w in graph.vertices:
                old_v = self.vertices[v.identifier]
                old_w = self.vertices[w.identifier]
                if (not old_w in old_v.neighbours
                        and not w in v.neighbours and not w == v):
                    graph.connect(v, w)

        return graph

    def subgraph(self, vertices):
        """Return a graph which is the subgraph of self induced by given vertex subset."""
        graph = Graph()
        for v in vertices:
            assert v in self.vertices
            new_v = Vertex(v.identifier)
            graph.add_vertex(new_v)
            for w in v.neighbours:
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

        vertices = list(graph.vertices)

        for i in range(nr_edges):
            while 1:
                v = choice(vertices)
                w = choice(vertices)
                # Graphs must be simple
                # And we don't want to connect vertices twice
                if v != w and not w in v.neighbours:
                    break
            graph.connect(v, w)

        return graph
