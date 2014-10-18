from random import sample
from vertex import Vertex, VertexSet, NeighbourhoodSet

class Graph:

    def __init__(self, vertices=None):
        self.vertices = VertexSet(vertices)
        self.neighbourhoods = NeighbourhoodSet(vertices)

    def __repr__(self):
        return 'vertices: {}'.format(list(self.vertices))

    def __str__(self):
        return repr(self)

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

        self.neighbourhoods.connect(v, w)

    def complement(self):
        """Construct a graph representing the complement of self."""
        vertices = list(self.vertices)
        graph = Graph(vertices)

        setlength = len(vertices)
        for v, neighbourhood in self.neighbourhoods:
            graph.neighbourhoods[v] = neighbourhood.invert(setlength)

        return graph

    def subgraph(self, vertices):
        """Return a graph which is the subgraph of self induced by given vertex subset."""
        raise NotImplementedError
        #graph = Graph()
        # for v in vertices:
        #assert v in self.vertices
        #new_v = Vertex(v.identifier)
        # graph.add_vertex(new_v)
        # for w in v.neighbours:
        # Only connect if w is already in the graph
        # Otherwise it comes later
        # try:
        #new_w = graph.vertices[w.identifier]
        # except KeyError:
        # pass
        # else:
        #graph.connect(new_v, new_w)

        # return graph

    @staticmethod
    def generate_random(nr_vertices, nr_edges):
        if not nr_edges <= nr_vertices * (nr_vertices - 1) / 2:
            raise ValueError

        vertices = [Vertex(i) for i in range(nr_vertices)]
        graph = Graph(vertices)

        for _ in range(nr_edges):
            while 1:
                v, w = sample(vertices, 2)
                # Don't connect vertices twice
                if not w in graph.neighbourhoods[v]:
                    break
            graph.connect(v, w)

        return graph
