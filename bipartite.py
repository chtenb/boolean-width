from graph import Graph, Vertex
from itertools import chain
from random import randint, choice


class Bipartite(Graph):

    def __init__(self):
        Graph.__init__(self)

        self.group1 = []
        self.group2 = []

    @property
    def vertices(self):
        return chain(self.group1, self.group2)

    def count_vertices(self):
        return len(self.group1) + len(self.group2)

    def add_vertex(self, vertex, group):
        """Add a new vertex to the graph."""
        if not isinstance(vertex, Vertex):
            raise ValueError
        if not vertex not in self.vertices:
            raise ValueError


        if group == 1:
            self.group1.append(vertex)
        elif group == 2:
            self.group2.append(vertex)
        else:
            raise ValueError

    def connect(self, v, w):
        """Connect two vertices."""
        if not ((v in self.group1 and w in self.group2)
                or
                (v in self.group2 and w in self.group1)):
            raise ValueError

        Graph.connect(self, v, w)

    def bipartite_complement(self):
        """Construct a graph representing the bipartite complement of self."""
        graph = Bipartite()
        bijection = {}

        for v in self.group1:
            v_new = Vertex(v.identifier)
            bijection[v_new] = v
            graph.add_vertex(v_new, group=1)
        for v in self.group2:
            v_new = Vertex(v.identifier)
            bijection[v_new] = v
            graph.add_vertex(v_new, group=2)

        for v in graph.group1:
            for w in graph.group2:
                if not bijection[w] in bijection[v].neighbours:
                    graph.connect(v, w)

        return graph

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

        graph = Bipartite()

        # For both groups create vertices
        for i in range(size1):
            vertex = Vertex(i)
            graph.add_vertex(vertex, group=1)

        for i in range(size2):
            vertex = Vertex(size1 + i)
            graph.add_vertex(vertex, group=2)

        # Add random edges between groups
        for i in range(nr_edges):
            while 1:
                v = choice(graph.group1)
                w = choice(graph.group2)
                if not w in v.neighbours:
                    break
            graph.connect(v, w)

        return graph
