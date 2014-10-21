from graph import Graph, Vertex
from vertex import VertexSet
from random import randint, choice
from utils import DictChain


class Tree(Graph):

    def __init__(self, group1=None, group2=None):
        Graph.__init__(self)

    @staticmethod
    def generate_random(nr_vertices, maxdegree=3):
        if maxdegree < 2:
            raise ValueError

        graph = Graph()
        root = Vertex(0)
        graph.add_vertex(root)

        for i in range(1, nr_vertices):
            while 1:
                v = choice(graph.vertices)
                if len(v.neighbors) < maxdegree:
                    w = Vertex(i)
                    graph.add_vertex(w)
                    graph.connect(v, w)
                    break

        return graph

