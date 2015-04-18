from .graph import Graph
from .bitset import BitSet
from random import choice


class Tree(Graph):

    def __init__(self):
        Graph.__init__(self)
        self.root = None

    def depth(self, root=None):
        root = root or self.root

        def recursion(vertex, parent):
            if len(vertex.neighbors) < 2:
                return 1
            return max(recursion(self[bchild], vertex) for bchild in vertex.neighbors
                       if not parent or self[bchild] != parent) + 1

        return recursion(root, None)

    def count_branches(self):
        """
        Count the number of branches, i.e. the sum of all branches exceeding degree 2.
        """
        return sum(len(v.neighbors) - 2 for v in self.vertices if len(v.neighbors) > 2)

    def count_branching_nodes(self):
        """
        Count the number of branches, i.e. the sum of all branches exceeding degree 2.
        """
        return sum(1 for v in self.vertices if len(v.neighbors) > 2)

    @staticmethod
    def generate_random(nr_vertices, maxdegree=3):
        if maxdegree < 2:
            raise ValueError

        graph = Tree()
        graph.root = BitSet.from_identifier(0)
        graph.add(graph.root)

        for i in range(1, nr_vertices):
            while 1:
                v = choice(list(graph.vertices))
                if len(graph(v)) < maxdegree:
                    w = BitSet.from_identifier(i)
                    graph.add(w)
                    graph.connect(v, w)
                    break

        return graph

    @staticmethod
    def generate_random_cubic(nr_vertices):
        graph = Tree()
        graph.root = BitSet.from_identifier(0)
        graph.add(graph.root)

        leaves = [graph.root]
        for i in range(1, nr_vertices):
            v = leaves[0]
            w = BitSet.from_identifier(i)
            graph.add(w)
            graph.connect(v, w)
            leaves.append(w)

            if len(graph(v)) == 3:
                leaves.pop(0)

        return graph
