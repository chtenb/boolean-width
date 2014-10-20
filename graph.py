from random import sample
from vertex import Vertex, VertexSet, BitSet
from copy import deepcopy


class Graph:

    def __init__(self, vertices=None):
        self._vertices = VertexSet(vertices)

    @property
    def vertices(self):
        return self._vertices

    def __repr__(self):
        return 'vertices: {}'.format(list(self.vertices))

    def __str__(self):
        return repr(self)

    def __getitem__(self, index):
        return self.vertices[index]

    def save(self, filename):
        # TODO
        with open(filename, 'w') as f:
            f.write(repr(self))

    @staticmethod
    def load(filename):
        graph = Graph()
        with open(filename, 'r') as f:
            while 1:
                line = f.readline()
                print('Parsing `{}`'.format(line))
                if line == '':
                    break
                if line == '\n':
                    continue

                if line[0] == 'n':
                    v = Vertex(int(line[1:]))
                    graph.add_vertex(v)
                elif line[0] == 'e':
                    v, w = (int(i) for i in line[1:].split())
                    if v not in graph.vertices:
                        graph.add_vertex(Vertex(v))
                    if w not in graph.vertices:
                        graph.add_vertex(Vertex(w))
                    graph.connect(v, w)
        return graph

    def add_vertex(self, v):
        """Add a new vertex to the graph."""
        if not isinstance(v, Vertex):
            raise ValueError
        if v in self.vertices:
            raise ValueError

        self.vertices.add(v)

    def connect(self, v, w):
        """Connect two vertices."""
        if (isinstance(v, BitSet) and isinstance(w, BitSet) or
                (isinstance(v, int) and isinstance(w, int))):
            v = self.vertices[v]
            w = self.vertices[w]

        if not v in self.vertices:
            raise ValueError
        if not w in self.vertices:
            raise ValueError

        if w in v.neighbors:
            raise ValueError('{} and {} already connected.'.format(v, w))

        # Only support undirected edges
        assert not v in w.neighbors

        v.neighbors |= BitSet(w)
        w.neighbors |= BitSet(v)

    def complement(self):
        """Construct a graph representing the complement of self."""
        vertices = deepcopy(list(self.vertices))
        graph = Graph(vertices)

        setlength = len(vertices)
        for v in self.vertices:
            v.neighbors = v.neighbors.invert(setlength)

        return graph

    def subgraph(self, vertices):
        """Return a graph which is the subgraph of self induced by given vertex subset."""
        vertices = deepcopy(list(self.vertices))
        graph = Graph(vertices)

        vertices_bitset = BitSet(vertices)
        for v in self.vertices:
            v.neighbors &= vertices_bitset

        return graph

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
                if not w in v.neighbors:
                    break
            graph.connect(v, w)

        return graph
