"""
This module contains datastructures for vertex and edge sets.
"""
from graph import Vertex


class NeighbourhoodSet:

    """
    Contains all neighbourhoods for all vertices.
    Lookup is possible by vertex as well as hash.
    """

    def __init__(self, vertices=None):
        vertices = vertices or []
        self.neighbourhoods = {hash(v): BitSet(0) for v in vertices}

    def __getitem__(self, vertex):
        if isinstance(vertex, Vertex):
            vertex = hash(vertex)
        elif not isinstance(vertex, BitSet):
            raise ValueError

        return self.neighbourhoods[vertex]

    def connect(self, v, w):
        if isinstance(v, Vertex) and isinstance(w, Vertex):
            v = hash(v)
            w = hash(w)
        elif not isinstance(v, BitSet) and isinstance(w, BitSet):
            raise ValueError

        if w in self.neighbourhoods[v]:
            raise ValueError('{} and {} already connected.'.format(v, w))

        # Only support undirected edges
        assert not v in self.neighbourhoods[w]

        self.neighbourhoods[v] |= w
        self.neighbourhoods[w] |= v


class HashSet(dict):

    """
    A hashset is just a dict with some modifications to make it work easier with
    vertices and edges.
    Values must be objects with a hash function.
    """

    def __init__(self, values=None):
        values = values or {}
        dict.__init__(self, {hash(v): v for v in values})

    def __repr__(self):
        return 'HashSet({})'.format(dict.__repr__(self))

    def __str__(self):
        return repr(self)

    def __contains__(self, values):
        return dict.__contains__(self, hash(values))

    def __iter__(self):
        for v in self.values():
            yield v

    def add(self, value):
        if value in self:
            raise ValueError('HashSet already contains item with hash {}'
                             .format(hash(value)))
        self[hash(value)] = value


class BitSet(int):

    """
    A bitset is just an int with some modifications to make it work like a set.
    """

    def __new__(cls, arg):
        if isinstance(arg, int):
            return int.__new__(cls, arg)
        else:
            i = sum(hash(v) for v in arg)
            return int.__new__(cls, i)

    def __repr__(self):
        return 'BitSet({})'.format(int.__repr__(self))

    def __str__(self):
        return repr(self)

    def __contains__(self, vertex):
        return self & hash(vertex) != 0

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

    def __invert__(self):
        return BitSet(int.__invert__(self))

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
