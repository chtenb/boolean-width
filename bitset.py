"""
This module contains datastructures for vertex and edge sets.
We want to be indifferent whether a pointer to a vertex is supplied or a bitset
representation.
"""

from math import log


class BitSet:

    """
    A bitset wraps around an int with functionality to make it work like a set.
    """

    def __init__(self, arg=None):
        self.i = arg or 0
        if not isinstance(self.i, int):
            raise ValueError

    @staticmethod
    def from_identifier(*args):
        self = BitSet()
        for v in args:
            self.i |= 2 ** v
        return self

    def identifier(self):
        """If we only contain a single vertex, return its identifier."""
        if len(self) > 1:
            raise ValueError
        return int(log(self.i, 2))

    def __repr__(self):
        return 'BitSet.from_identifier({})'.format(', '.join(str(v) for v in self))

    def __str__(self):
        if len(self) == 1:
            return str(self.identifier())
        else:
            return repr(self)

    def __hash__(self):
        return self.i

    def __eq__(self, other):
        return isinstance(other, BitSet) and self.i == other.i

    def __lt__(self, other):
        return self.i < other.i

    def __gt__(self, other):
        return self.i > other.i

    def __contains__(self, other):
        return self.i | other.i == self.i

    def disjoint(self, other):
        return self.i & other.i == 0

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

    # def invert(self, length):
        # TODO: provide universe against which the complement is computed
        # return BitSet(2 ** length - 1 - self.i)
