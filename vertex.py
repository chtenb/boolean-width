"""
This module contains datastructures for vertex and edge sets.
"""


class Vertex:

    def __init__(self, identifier):
        if not isinstance(identifier, int):
            raise ValueError
        self.identifier = identifier

    def __repr__(self):
        return 'Vertex({})'.format(self.identifier)

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return self.identifier == other.identifier


class NeighbourhoodSet:

    """
    Contains all neighbourhoods for all vertices.
    Lookup is possible by vertex as well as bitset.
    """

    def __init__(self, vertices=None):
        vertices = vertices or []
        self.neighbourhoods = {BitSet(v): BitSet(0) for v in vertices}

    def __getitem__(self, vertex):
        if not isinstance(vertex, BitSet):
            vertex = BitSet(vertex)

        assert isinstance(vertex, BitSet)

        return self.neighbourhoods[vertex]

    def connect(self, v, w):
        if not isinstance(v, BitSet) and not isinstance(w, BitSet):
            v = BitSet(v)
            w = BitSet(w)

        assert isinstance(v, BitSet) and isinstance(w, BitSet)

        if w in self.neighbourhoods[v]:
            raise ValueError('{} and {} already connected.'.format(v, w))

        # Only support undirected edges
        assert not v in self.neighbourhoods[w]

        self.neighbourhoods[v] |= w
        self.neighbourhoods[w] |= v


class VertexSet(dict):

    """
    A VertexSet is just a dict with some modifications to make it work easier with
    vertices.
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

    def add(self, vertex):
        if vertex in self:
            raise ValueError('VertexSet already contains item with identifier {}'
                             .format(vertex.identifier))
        self[BitSet(vertex)] = vertex


class BitSet(int):

    """
    A bitset is just an int with some modifications to make it work like a set.
    """

    def __new__(cls, arg):
        if isinstance(arg, int):
            return int.__new__(cls, arg)
        elif isinstance(arg, Vertex):
            return int.__new__(cls, 2 ** arg.identifier)
        else:
            i = sum(BitSet(v) for v in arg)
            return int.__new__(cls, i)

    def __repr__(self):
        return 'BitSet({})'.format(int.__repr__(self))

    def __str__(self):
        return repr(self)

    def __contains__(self, vertex):
        return self & BitSet(vertex) != 0

    def __iter__(self):
        n = int(self)
        while n:
            b = n & (~n + 1)
            yield BitSet(b)
            n ^= b

    def __len__(self):
        return len(list(self.__iter__()))

    def __and__(self, other):
        return BitSet(int.__and__(self, other))

    def __or__(self, other):
        return BitSet(int.__or__(self, other))

    def __xor__(self, other):
        return BitSet(int.__xor__(self, other))

    def __sub__(self, other):
        return BitSet(int.__sub__(self, (self & other)))

    def invert(self, length):
        # TODO: optionally provide universe against which the complement is computed
        return BitSet(int.__sub__(2 ** length, 1) - self)

    def __invert__(self):
        raise NotImplementedError

    def __add__(self, other):
        raise NotImplementedError

    def __mul__(self, other):
        raise NotImplementedError

    def __truediv__(self, other):
        raise NotImplementedError

    def __floordiv__(self, other):
        raise NotImplementedError

    def __divmod__(self, other):
        raise NotImplementedError

    def __mod__(self, other):
        raise NotImplementedError

    def __pow__(self, other):
        raise NotImplementedError

    def __lshift__(self, other):
        raise NotImplementedError

    def __rshift__(self, other):
        raise NotImplementedError
