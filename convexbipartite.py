from random import randint, randrange
from numpy import diff

from bipartite import Bipartite
from graph import Vertex


def random_partition(n, k, limit):
    """
    Return a random partition of integer n in k parts,
    with a maximum of limit per part.
    """
    if n > k * limit:
        raise ValueError

    partition = [0] * k
    for _ in range(n):
        while 1:
            i = randrange(k)
            if partition[i] < limit:
                partition[i] += 1
                break
    return partition


class ConvexBipartite(Bipartite):

    def verify_convexity(self):
        """Check that we are indeed convex."""
        for v in self.group2:
            ids = [w.identifier for w in v.neighbours]
            ids.sort()
            differences = diff(ids)
            if differences.size > 0 and max(differences) > 1:
                return False
        return True

    @staticmethod
    def generate_random(nr_vertices, nr_edges):
        """There is probably a bias in this generation algorithm."""
        if not nr_edges <= (nr_vertices / 2) ** 2:
            raise ValueError

        # Split the number of vertices on both sides
        # such that enough edges can be placed
        while 1:
            size1 = randint(1, nr_vertices - 1)
            size2 = nr_vertices - size1
            if size1 * size2 >= nr_edges:
                break

        graph = ConvexBipartite()

        # For both groups create vertices
        for i in range(size1):
            vertex = Vertex(i)
            graph.add_vertex(vertex, group=1)

        for i in range(size2):
            vertex = Vertex(size1 + i)
            graph.add_vertex(vertex, group=2)

        # For each vertex in group2 we can determine the neighbourhood by
        # a starting vertex and the length of the neighbourhood.
        len_group1 = len(graph.group1)
        neighbourhoodlengths = random_partition(nr_edges,
                                                len(graph.group2),
                                                len_group1)
        for i, v in enumerate(graph.group2):
            length = neighbourhoodlengths[i]
            start = randint(0, len_group1 - length)
            for j in range(start, start + length):
                graph.connect(graph.group1[j], v)
        return graph
