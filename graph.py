from random import sample
from vertex import BitSet

# TODO: where to convert id's to bitsets and vice versa?
#       Preferably inside BitSet
# TODO: Differentiate between inclusive and exclusive neighborhood

class Graph:

    def __init__(self, vertices=None, neighborhoods=None):
        self.neighborhoods = neighborhoods or {}
        self.vertices = vertices or BitSet()

    def __repr__(self):
        return 'vertices: {}'.format(list(self.vertices))

    def __str__(self):
        return repr(self)

    def __iter__(self):
        return iter(self.vertices)

    def __contains__(self, v):
        return v in self.vertices

    def __call__(self, vertices):
        result = BitSet()
        for v in vertices:
            result |= self.neighborhoods[v]
        return result

    def __getitem__(self, vertices):
        return self(vertices) | vertices

    @property
    def edges(self):
        for v in self:
            for w in self[v]:
                if w < v:
                    yield (v, w)

    def save(self, filename):
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
                    v = BitSet(int(line[1:]))
                    graph.add_vertex(v)
                elif line[0] == 'e':
                    v, w = BitSet(int(i) for i in line[1:].split())
                    if v not in graph:
                        graph.add_vertex(v)
                    if w not in graph:
                        graph.add_vertex(w)
                    graph.connect(v, w)
        return graph

    def add_vertex(self, v):
        """Add a new vertex to the graph."""
        if v in self:
            raise ValueError

        self.vertices |= v

    def connect(self, v, w):
        """Connect two vertices."""
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

    def disconnect(self, v, w):
        """Disconnect two vertices."""
        if not v in self:
            raise ValueError
        if not w in self:
            raise ValueError

        if not w in self[v]:
            raise ValueError('{} and {} are not connected.'.format(v, w))

        # Only support undirected edges
        assert v in self[w]

        self.neighborhoods[v] -= w
        self.neighborhoods[w] -= v

    def complement(self):
        """Construct a graph representing the complement of self."""
        setlength = len(self.vertices)
        neighborhoods = {v : self[v].invert(setlength) for v in self}
        return Graph(self.vertices, neighborhoods)

    def subgraph(self, vertices):
        """Return a graph which is the subgraph of self induced by given vertex subset."""
        neighborhoods = {v : self[v] & vertices for v in self}
        return Graph(self.vertices, neighborhoods)

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
