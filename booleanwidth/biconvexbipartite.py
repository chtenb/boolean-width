
from random import randint
from numpy import diff

from .bipartite import Bipartite
from .graph import Vertex


class BiconvexBipartite(Bipartite):

    def verify_biconvexity(self):
        """Check that we are indeed biconvex."""
        def verify_group(group):
            for v in group:
                ids = [w.identifier for w in v.neighbors]
                ids.sort()
                differences = diff(ids)
                if differences.size > 0 and max(differences) > 1:
                    return False

        return verify_group(self.group1) and verify_group(self.group2)

    @staticmethod
    def generate_random(nr_vertices, nr_edges):
        return NotImplemented

    def subgraph(self, vertices):
        return NotImplemented

