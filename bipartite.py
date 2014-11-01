from graph import Graph
from bitset import BitSet
from random import randint, choice
from utils import DictChain
from copy import deepcopy


class Bipartite(Graph):

    def __init__(self, group1=None, group2=None):
        Graph.__init__(self)

        self.group1 = group1 or BitSet()
        self.group2 = group2 or BitSet()

        for v in self.vertices:
            self.neighborhoods[v] = BitSet()

    @property
    def vertices(self):
        return self.group1 | self.group2

    def add(self, vertices, group):
        """Add a new vertex to the graph."""
        if not self.vertices.disjoint(vertices):
            raise ValueError('Graph already contain some of [{}]'.format(vertices))

        if group == 1:
            self.group1 |= vertices
        elif group == 2:
            self.group2 |= vertices
        else:
            raise ValueError

        for v in vertices:
            self.neighborhoods[v] = BitSet()

    def connect(self, v, w):
        """Connect two vertices."""
        if not ((v in self.group1 and w in self.group2)
                or
                (v in self.group2 and w in self.group1)):
            raise ValueError

        Graph.connect(self, v, w)

    def subgraph(self, vertices):
        """Return a graph which is the subgraph of self induced by given vertex subset."""
        graph = Bipartite(self.group1 & vertices, self.group2 & vertices)

        for v in graph.vertices:
            graph.neighborhoods[v] &= vertices

        return graph

    def bipartite_complement(self):
        """Construct a graph representing the bipartite complement of self."""
        raise NotImplementedError
        #graph = Bipartite()

        # for v in self.group1:
        #v_new = Vertex(v.identifier)
        #graph.add(v_new, group=1)
        # for v in self.group2:
        #v_new = Vertex(v.identifier)
        #graph.add(v_new, group=2)

        # for v in graph.group1:
        # for w in graph.group2:
        # if not self.vertices[v.identifier] in self.vertices[w.identifier].neighbors:
        #graph.connect(v, w)

        # return graph

    @staticmethod
    def generate_random(nr_vertices, nr_edges):
        if not nr_edges <= (nr_vertices / 2) ** 2:
            raise ValueError

        # Split the number of vertices on both sides
        # such that enough edges can be placed
        while 1:
            size1 = randint(1, nr_vertices - 1)
            size2 = nr_vertices - size1
            if size1 * size2 >= nr_edges:
                break

        # For both groups create vertices
        group1 = range(size1)
        group2 = range(size1, size1 + size2)

        graph = Bipartite(BitSet.from_identifier(*group1), BitSet.from_identifier(*group2))

        # Add random edges between groups
        for _ in range(nr_edges):
            while 1:
                v = BitSet.from_identifier(choice(group1))
                w = BitSet.from_identifier(choice(group2))
                if not w in graph(v):
                    break
            graph.connect(v, w)

        return graph
