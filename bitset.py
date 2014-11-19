"""
This module contains datastructures for vertex and edge sets.
We want to be indifferent whether a pointer to a vertex is supplied or a bitset
representation.
"""

from math import log
from itertools import combinations


class BitSet(int):

    """
    A bitset is an int with functionality to make it work like a set.
    We try to reduce the performance overhead as much as possible.
    """

    @staticmethod
    def from_identifier(*args):
        self = 0
        for v in args:
            self += 2 ** v
        return BitSet(self)

    @staticmethod
    def join(*args):
        self = 0
        for v in args:
            self |= v
        return BitSet(self)

    @property
    def identifier(self):
        """If we only contain a single vertex, return its identifier."""
        assert not len(self) > 1
        return int(log(self, 2))

    def __repr__(self):
        return 'BitSet{{{}}}'.format(', '.join(str(v) for v in self))

    def __str__(self):
        if len(self) == 1:
            return str(self.identifier)
        else:
            return repr(self)

    def tolist(self, length):
        result = []
        while length:
            result.append(self % 2)
            self >>= 2
            length -= 1
        return result

    def __hash__(self):
        return self

    def __contains__(self, other):
        return self | other == self

    def __iter__(self):
        n = int(self)
        while n:
            b = n & (~n + 1)
            yield BitSet(b)
            n ^= b

    def subsets(self, minsize=None, maxsize=None):
        """Yield subbitsets from specified size ordered by size ascending."""
        # TODO in 2^n time
        #minsize = minsize or 0
        #maxsize = maxsize or len(self)
        # for k in range(minsize, maxsize + 1):
        # yield from (BitSet.join(*b) for b in combinations(list(self), k))

    def __len__(self):
        return sum(1 for _ in self)

    def __and__(self, other):
        # return BitSet(int.__and__(self, other))
        return BitSet(int(self) & other)

    def __or__(self, other):
        # return BitSet(int.__or__(self, other))
        return BitSet(int(self) | other)

    def __xor__(self, other):
        # return BitSet(int.__xor__(self, other))
        return BitSet(int(self) ^ other)

    def __sub__(self, other):
        # return BitSet(int.__sub__(self, int.__and__(self, other)))
        n = int(self)
        return BitSet(n - (n & other))

    def disjoint(self, other):
        return int(self) & other == 0

    def invert(self, universe_length):
        return BitSet(2 ** universe_length - 1 - self)

    def __eq__(self, other):
        assert isinstance(other, BitSet)
        return int(self) == int(other)

#from numpy import int_, bitwise_and, bitwise_or, bitwise_xor

# class BitSet(int_):

    #"""
    # A bitset is an int with functionality to make it work like a set.
    # We try to reduce the performance overhead as much as possible.
    #"""

    #@staticmethod
    # def from_identifier(*args):
        #self = 0
        # for v in args:
        #self += 2 ** v
        # return BitSet(self)

    #@staticmethod
    # def join(*args):
        #self = 0
        # for v in args:
        #self |= v
        # return BitSet(self)

    #@property
    # def identifier(self):
        #"""If we only contain a single vertex, return its identifier."""
        #assert not len(self) > 1
        # return int(log(self, 2))

    # def __repr__(self):
        # return 'BitSet{{{}}}'.format(', '.join(str(v) for v in self))

    # def __str__(self):
        # if len(self) == 1:
        # return str(self.identifier)
        # else:
        # return repr(self)

    # def __hash__(self):
        # return int(self)

    # def __contains__(self, other):
        #assert isinstance(other, BitSet)
        # return self | other == self

    # def __iter__(self):
        #n = int(self)
        # while n:
        #b = n & (~n + 1)
        # yield BitSet(b)
        #n ^= b

    # def subsets(self, minsize=None, maxsize=None):
        #"""Yield subbitsets from specified size ordered by size ascending."""
        # TODO in 2^n time
        #minsize = minsize or 0
        #maxsize = maxsize or len(self)
        # for k in range(minsize, maxsize + 1):
        # yield from (BitSet.join(*b) for b in combinations(list(self), k))

    # def __len__(self):
        # return sum(1 for _ in self)

    # def __and__(self, other):
        #assert isinstance(other, BitSet)
        # return BitSet(bitwise_and(self, other))

    # def __or__(self, other):
        #assert isinstance(other, BitSet)
        # return BitSet(bitwise_or(self, other))

    # def __xor__(self, other):
        #assert isinstance(other, BitSet)
        # return BitSet(bitwise_xor(self, other))

    # def __sub__(self, other):
        #assert isinstance(other, BitSet)
        # return BitSet(int_.__sub__(self, (self & other)))

    # def disjoint(self, other):
        #assert isinstance(other, BitSet)
        # return self & other == BitSet()

    # def invert(self, universe_length):
        # return BitSet(2 ** universe_length - 1 - self)

    # def __eq__(self, other):
        #assert isinstance(other, BitSet)
        # return int_.__eq__(self, other)


# class BitSet:

    #"""
    # A bitset wraps around an int with functionality to make it work like a set.
    #"""

    # def __init__(self, arg=None):
        #self.i = arg or 0
        #assert isinstance(self.i, int)

    #@staticmethod
    # def from_identifier(*args):
        #self = BitSet()
        # for v in args:
        #self.i |= 2 ** v
        # return self

    #@staticmethod
    # def join(*args):
        #self = BitSet()
        # for v in args:
        #self.i |= v.i
        # return self

    #@property
    # def identifier(self):
        #"""If we only contain a single vertex, return its identifier."""
        #assert not len(self) > 1
        # return int(log(self.i, 2))

    # def __repr__(self):
        # return 'BitSet{{{}}}'.format(', '.join(str(v) for v in self))

    # def __str__(self):
        # if len(self) == 1:
        # return str(self.identifier)
        # else:
        # return repr(self)

    # def __hash__(self):
        # return self.i

    # def __contains__(self, other):
        # return self.i | other.i == self.i

    # def __iter__(self):
        #n = self.i
        # while n:
        #b = n & (~n + 1)
        # yield BitSet(b)
        #n ^= b

    # def subsets(self, minsize=None, maxsize=None):
        #"""Yield subbitsets from specified size ordered by size ascending."""
        # TODO in linear time
        #minsize = minsize or 0
        #maxsize = maxsize or len(self)
        # for k in range(minsize, maxsize + 1):
        # yield from (BitSet.join(*b) for b in combinations(list(self), k))

    # def __bool__(self):
        # return self.i != 0

    # def __len__(self):
        # return sum(1 for _ in self)

    # def __and__(self, other):
        # return BitSet(self.i & other.i)

    # def __or__(self, other):
        # return BitSet(self.i | other.i)

    # def __xor__(self, other):
        # return BitSet(self.i ^ other.i)

    # def __sub__(self, other):
        # return BitSet(self.i - (self.i & other.i))

    # def disjoint(self, other):
        # return self.i & other.i == 0

    # def invert(self, universe_length):
        # return BitSet(2 ** universe_length - 1 - self)

    # def __eq__(self, other):
        #assert isinstance(other, BitSet)
        # return self.i == other.i

    # def __lt__(self, other):
        # return self.i < other.i

    # def __gt__(self, other):
        # return self.i > other.i
