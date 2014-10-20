from graph import Graph, Vertex
from vertex import VertexSet
from random import randint, choice
from utils import DictChain


class Bipartite(Graph):

    def __init__(self, group1=None, group2=None):
        Graph.__init__(self)

        self.group1 = VertexSet(group1)
        self.group2 = VertexSet(group2)

    @property
    def vertices(self):
        return DictChain(self.group1, self.group2)

    def add_vertex(self, vertex, group):
        """Add a new vertex to the graph."""
        if not isinstance(vertex, Vertex):
            raise ValueError
        if not vertex not in self.vertices:
            raise ValueError


        if group == 1:
            self.group1.add(vertex)
        elif group == 2:
            self.group2.add(vertex)
        else:
            raise ValueError

    def connect(self, v, w):
        """Connect two vertices."""
        if not ((v in self.group1 and w in self.group2)
                or
                (v in self.group2 and w in self.group1)):
            raise ValueError

        Graph.connect(self, v, w)

    def subgraph(self, vertices):
        raise NotImplementedError

    def bipartite_complement(self):
        """Construct a graph representing the bipartite complement of self."""
        raise NotImplementedError
        #graph = Bipartite()

        #for v in self.group1:
            #v_new = Vertex(v.identifier)
            #graph.add_vertex(v_new, group=1)
        #for v in self.group2:
            #v_new = Vertex(v.identifier)
            #graph.add_vertex(v_new, group=2)

        #for v in graph.group1:
            #for w in graph.group2:
                #if not self.vertices[v.identifier] in self.vertices[w.identifier].neighbors:
                    #graph.connect(v, w)

        #return graph

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
        group1 = [Vertex(i + 1) for i in range(size1)]
        group2 = [Vertex(size1 + i + 1) for i in range(size2)]

        graph = Bipartite(group1, group2)

        # Add random edges between groups
        for _ in range(nr_edges):
            while 1:
                v = choice(group1)
                w = choice(group2)
                if not w in v.neighbors:
                    break
            graph.connect(v, w)

        return graph
