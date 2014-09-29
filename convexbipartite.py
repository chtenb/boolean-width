from random import randint, choice

from bipartite import Bipartite
from graph import Vertex


class BiconvexBipartite(Bipartite):

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

        graph = BiconvexBipartite()

        # For both groups create vertices
        for i in range(size1):
            vertex = Vertex(i)
            graph.add_vertex(vertex, group=1)

        for i in range(size2):
            vertex = Vertex(size1 + i)
            graph.add_vertex(vertex, group=2)

        # Add random edges between groups
        # TODO
        for i in range(nr_edges):
            while 1:
                v = choice(graph.group1)
                w = choice(graph.group2)
                if not w in v.neighbours:
                    break
            graph.connect(v, w)

        return graph
