"""
This module contains datastructures for vertex and edge sets.
We want to be indifferent whether a pointer to a vertex is supplied or a bitset
representation.
"""


class Vertex:

    def __init__(self, identifier):
        if not isinstance(identifier, int):
            raise ValueError
        if identifier < 1:
            raise ValueError
        self.identifier = identifier
        self.neighbors = BitSet(0)

    def __repr__(self):
        return 'Vertex({})'.format(self.identifier)

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return self.identifier == other.identifier


class VertexSet(dict):

    """
    A VertexSet is dict with some modifications to make it work easier with vertices.
    """

    def __init__(self, vertices=None):
        vertices = vertices or {}
        dict.__init__(self, {BitSet(v): v for v in vertices})

    def __repr__(self):
        return 'VertexSet({})'.format(dict.__repr__(self))

    def __str__(self):
        return repr(self)

    def __contains__(self, vertex):
        return dict.__contains__(self, BitSet(vertex))

    def __iter__(self):
        for v in self.values():
            yield v

    def __getitem__(self, index):
        """
        Support access by identifier, and bitset representation.
        If a bitset contains more vertices, return a list of vertices.
        """
        # Get by bitset representation
        if isinstance(index, BitSet):
            result = [dict.__getitem__(self, b) for b in index]
            if len(result) == 1:
                return result[0]
            return result

        # Get by identifier
        if isinstance(index, int):
            for v in self:
                if v.identifier == index:
                    return v


    def add(self, vertex):
        if vertex in self:
            raise ValueError('VertexSet already contains item with identifier {}'
                             .format(vertex.identifier))
        self[BitSet(vertex)] = vertex


class BitSet:

    """
    A bitset wraps around an int with functionality to make it work like a set.
    """

    def __init__(self, arg):
        if isinstance(arg, int):
            self.i = arg
        elif isinstance(arg, BitSet):
            self.i = arg.i
        elif isinstance(arg, Vertex):
            self.i = 2 ** arg.identifier
        else:
            self.i = 0
            for v in arg:
                self.i |= BitSet(v).i

    def __repr__(self):
        return 'BitSet({})'.format(self.i)

    def __str__(self):
        return repr(self)

    def __hash__(self):
        return self.i

    def __eq__(self, other):
        return self.i == other.i

    def __contains__(self, vertex):
        return self.i & BitSet(vertex).i != 0

    def __iter__(self):
        n = self.i
        while n:
            b = n & (~n + 1)
            yield BitSet(b)
            n ^= b

    def __len__(self):
        return len(list(self.__iter__()))

    def __and__(self, other):
        return BitSet(self.i & other.i)

    def __or__(self, other):
        return BitSet(self.i | other.i)

    def __xor__(self, other):
        return BitSet(self.i ^ other.i)

    def __sub__(self, other):
        return BitSet(self.i - (self.i & other.i))

    def invert(self, length):
        # TODO: optionally provide universe against which the complement is computed
        return BitSet(2 ** length - 1 - self.i)

