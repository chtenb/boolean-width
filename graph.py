from random import sample
from vertex import Vertex, VertexSet, BitSet
from copy import deepcopy

# TODO: make sure that assignments with bitsets are call by value
# TODO: where to convert id's to bitsets and vice versa?
#       Preferably inside BitSet

class Graph:

    def __init__(self, vertices=None):
        self.neighborhoods = {}
        self._vertices = BitSet()

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        for v in self:
            for w in self[v]:
                if w < v:
                    yield (v, w)

    def __repr__(self):
        return 'vertices: {}'.format(list(self.vertices))

    def __str__(self):
        return repr(self)

    def __getitem__(self, index):
        result = BitSet()
        for v in index:
            result |= self.neighborhoods[v]
        return result

    def __iter__(self):
        return iter(self.vertices)

    def __contains__(self, v):
        return v in self.vertices

    def save(self, filename):
        # TODO
        raise NotImplementedError

    @staticmethod
    def load(filename):
        graph = Graph()
        with open(filename, 'r') as f:
            while 1:
                line = f.readline()
                print('Parsing `{}`'.format(line[:-1]))
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
        if v in self:
            raise ValueError

        self.vertices |= v

    def connect(self, v, w):
        """Connect two vertices."""
        #if (isinstance(v, BitSet) and isinstance(w, BitSet) or
                #(isinstance(v, int) and isinstance(w, int))):
            #v = self.vertices[v]
            #w = self.vertices[w]

        if not v in self:
            raise ValueError
        if not w in self:
            raise ValueError

        if w in self[v]:
            raise ValueError('{} and {} already connected.'.format(v, w))

        # Only support undirected edges
        assert not v in self[w]

        self.neighborhoods[v] |= w
        self.neighborhoods[w] |= v

    def complement(self):
        """Construct a graph representing the complement of self."""
        graph = Graph()
        graph._vertices = self.vertices

        setlength = len(self.vertices)
        for v in self:
            self[v] = self[v].invert(setlength)

        return graph

    def subgraph(self, vertices):
        """Return a graph which is the subgraph of self induced by given vertex subset."""
        graph = Graph()
        graph._vertices = vertices

        for v in graph:
            graph.neighborhoods[v] = self[v] & vertices

        return graph

    @staticmethod
    def generate_random(nr_vertices, nr_edges):
        if not nr_edges <= nr_vertices * (nr_vertices - 1) / 2:
            raise ValueError

        graph = Graph()
        for i in range(nr_vertices):
            graph.add_vertex(BitSet(i))

        for _ in range(nr_edges):
            while 1:
                v, w = sample(graph.vertices, 2)
                # Don't connect vertices twice
                if not w in graph[v]:
                    break
            graph.connect(v, w)

        return graph
