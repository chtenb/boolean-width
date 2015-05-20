"""
This module contains datastructures for vertex and edge sets.
We want to be indifferent whether a pointer to a vertex is supplied or a bitset
representation.
"""

from math import log
import math


#
# Procedural implementation
#

def index(x):
    """
    Return position of first element in given bitset, counting from 0.
    Return 128 if bitset is empty.
    """
    count = 0
    while not x & 1:
        x >>= 1
        count += 1
    return count


def domain(x):
    """
    Return position of last vertex in given bitset.
    Return 0 if bitset is empty.
    """
    count = 0
    while x:
        x >>= 1
        count += 1
    return count


def size(x):
    """Return size of given uint128."""
    return len(list(iterate(x)))


def bit(position):
    return 1 << position


def bits(*positions):
    result = 0
    for position in positions:
        result |= bit(position)
    return result


def universe(length):
    return (1 << length) - 1


def subtract(self, other):
    return self - (self & other)


def contains(self, other):
    return self | other == self


def disjoint(self, other):
    return self & other == 0


def invert(x, l):
    """Return inverse where universe has length l"""
    return subtract(universe(l), x)


def join(args):
    result = 0
    for v in args:
        result |= v
    return result


def first(n):
    return n & (~n + 1)


def iterate(n):
    while n:
        b = n & (~n + 1)
        yield b
        n ^= b


def subsets(self, minsize=0, maxsize=-1):
    """Yield subbitsets from specified size ordered by size ascending."""
    if minsize < 0:
        minsize = size(self) + 1 + minsize
    if maxsize < 0:
        maxsize = size(self) + 1 + maxsize

    sets = [0]
    for v in iterate(self):
        sets.extend([s | v for s in sets])

    return [s for s in sets if size(s) >= minsize and size(s) <= maxsize]


def nCr(n, r):
    f = math.factorial
    return f(n) / f(r) / f(n - r)


def subsets_of_size(bitset, subsetsize):
    table = [[] for k in range(subsetsize + 1)]
    table[0] = [0]
    for b in iterate(bitset):
        for k in range(1, subsetsize + 1):
            table[k].extend([subset | b for subset in table[k - 1] if not contains(subset, b)])

    #assert len(table[subsetsize]) == nCr(size(bitset), subsetsize)
    return table[subsetsize]


def subsets_by_size(bitset):
    s = size(bitset)
    table = [[] for k in range(s + 1)]
    table[0] = [0]
    for b in iterate(bitset):
        for k in range(1, s + 1):
            table[k].extend([subset | b for subset in table[k - 1] if not contains(subset, b)])

    # print(table)
    # for k in range(1, s + 1):
        #assert len(table[k]) == nCr(s, k)
    return table


def tostring(self):
    return '{{{}}}'.format(', '.join(str(index(v)) for v in iterate(self)))


def tolist(bitset, length):
    result = []
    while length:
        result.append(bitset % 2)
        bitset >>= 1
        length -= 1
    return result



#
# OO implementation
#

class BitSet(int):

    """
    A bitset is an int with functionality to make it work like a set.
    We try to reduce the performance overhead as much as possible.
    """

    @staticmethod
    def from_identifier(*args):
        self = 0
        for v in args:
            self |= 2 ** v
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
            self >>= 1
            length -= 1
        return result

    def ffs(self):
        return next(self).identifier

    def fls(self):
        for v in self:
            last = v
        return last.identifier

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

    def subsets(self, minsize=0, maxsize=-1):
        """Yield subbitsets from specified size ordered by size ascending."""
        if minsize < 0:
            minsize = len(self) + 1 + minsize
        if maxsize < 0:
            maxsize = len(self) + 1 + maxsize

        sets = [BitSet()]
        for v in self:
            sets.extend([s | v for s in sets])

        return [s for s in sets if len(s) >= minsize and len(s) <= maxsize]

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

