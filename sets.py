"""
This module contains datastructures for vertex and edge sets.
"""

class VertexSet(dict):

    """
    A vertexset is just a dict with some modifications to make it work easier with
    vertices.
    """

    def __init__(self, vertices=None):
        vertices = vertices or {}
        dict.__init__(self, {v.identifier: v for v in vertices})

    def __repr__(self):
        return 'VertexSet({})'.format(hash(self))

    def __str__(self):
        return dict.__repr__(self)

    def __contains__(self, vertex):
        return dict.__contains__(self, vertex.identifier)

    def __iter__(self):
        for v in self.values():
            yield v

    def __hash__(self):
        return sum(2 ** v.identifier for v in self)

    def add(self, vertex):
        if vertex in self:
            raise ValueError('VertexSet already contains a vertex with identifier {}'
                             .format(vertex.identifier))
        self[vertex.identifier] = vertex

    def minus(self, vset):
        return VertexSet(value for value in self if value not in vset)


class EdgeSet(dict):

    """
    A edgeset is just a dict with some modifications to make it work easier with edges.
    """

    def __init__(self, edges=None):
        edges = edges or {}
        dict.__init__(self, {hash(e): e for e in edges})

    def __repr__(self):
        return 'EdgeSet({})'.format(hash(self))

    def __str__(self):
        return str(self)

    def __contains__(self, edge):
        return dict.__contains__(self, hash(edge))

    def __iter__(self):
        for e in self.values():
            yield e

    def __hash__(self):
        return sum(2 ** hash(e) for e in self)

    def add(self, edge):
        if edge in self:
            raise ValueError('EdgeSet already contains a edge with hash {}'
                             .format(hash(edge)))
        self[hash(edge)] = edge


class VertexBitSet(int):

    """
    A vertexbitset is just an int with some modifications to make it work easier with
    vertices.
    """

    def __new__(cls, arg):
        if type(arg) == int:
            return int.__new__(cls, arg)
        else:
            i = sum(2 ** v.identifier for v in arg)
            return int.__new__(cls, i)

    def __repr__(self):
        return 'VertexBitSet({})'.format(int.__repr__(self))

    def __str__(self):
        return repr(self)

    def __contains__(self, vertex):
        return self & (2 ** vertex.identifier) != 0

    def __iter__(self):
        # TODO
        return NotImplemented

    def __len__(self):
        sum(int(char) for char in bin(self)[2:])

    def __and__(self, other):
        return VertexBitSet(int.__and__(self, other))

    def __or__(self, other):
        return VertexBitSet(int.__and__(self, other))

    def __xor__(self, other):
        return VertexBitSet(int.__and__(self, other))

    def __sub__(self, other):
        return VertexBitSet(int.__sub__(self, (self & other)))

    def __add__(self, other):
        return NotImplemented

    def __mul__(self, other):
        return NotImplemented

    def __truediv__(self, other):
        return NotImplemented

    def __floordiv__(self, other):
        return NotImplemented

    def __divmod__(self, other):
        return NotImplemented

    def __mod__(self, other):
        return NotImplemented

    def __pow__(self, other):
        return NotImplemented

    def __lshift__(self, other):
        return NotImplemented

    def __rshift__(self, other):
        return NotImplemented

