from graph import Graph
from bitset import BitSet


class Grid(Graph):

    @staticmethod
    def generate_random(width, height):
        """The numbering is from left to right, from top to bottom."""
        graph = Graph()
        graph.add(BitSet.from_identifier(*range(width * height)))

        # Connect horizontal edges
        for row in range(height):
            for column in range(width - 1):
                i = row * width + column
                v = BitSet.from_identifier(i)
                w = BitSet.from_identifier(i + 1)
                graph.connect(v, w)

        # Connect vertical edges
        for column in range(width):
            for row in range(height - 1):
                i = row * width + column
                v = BitSet.from_identifier(i)
                w = BitSet.from_identifier(i + width)
                graph.connect(v, w)

        return graph
