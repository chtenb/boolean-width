from graph import Graph
from bitset import BitSet


def squares(width, height):
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


def semisquares(width, height):
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
            graph.split(v, w)

    # Connect vertical edges
    for column in range(width):
        for row in range(height - 1):
            i = row * width + column
            v = BitSet.from_identifier(i)
            w = BitSet.from_identifier(i + width)
            graph.connect(v, w)
            graph.split(v, w)

    return graph


def cliques(width, height):
    """The numbering is from left to right, from top to bottom."""
    graph = Graph()
    graph.add(BitSet.from_identifier(*range(width * height)))

    # Connect horizontal cliques
    for row in range(height):
        for column in range(width - 1):
            i = row * width + column
            for column2 in range(column + 1, width):
                j = row * width + column2
                v = BitSet.from_identifier(i)
                w = BitSet.from_identifier(j)
                graph.connect(v, w)

    # Connect vertical edges
    for column in range(width):
        for row in range(height - 1):
            i = row * width + column
            v = BitSet.from_identifier(i)
            w = BitSet.from_identifier(i + width)
            graph.connect(v, w)

    return graph


def semicliques(width, height):
    """The numbering is from left to right, from top to bottom."""
    graph = Graph()
    graph.add(BitSet.from_identifier(*range(width * height)))

    # Connect horizontal cliques
    for row in range(height):
        for column in range(width - 1):
            i = row * width + column
            for column2 in range(column + 1, width):
                j = row * width + column2
                v = BitSet.from_identifier(i)
                w = BitSet.from_identifier(j)
                graph.connect(v, w)
                graph.split(v, w)

    # Connect vertical edges
    for column in range(width):
        for row in range(height - 1):
            i = row * width + column
            v = BitSet.from_identifier(i)
            w = BitSet.from_identifier(i + width)
            graph.connect(v, w)

    return graph
