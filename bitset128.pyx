"""
This module contains cython functions for making int64 work like a set.
"""
cdef extern from "uint128.h":
    ctypedef unsigned long long uint128


cdef extern int __builtin_popcountll(unsigned long long x)
cdef extern int __builtin_popcount(unsigned int x)
cdef extern int __builtin_ctzll(unsigned long long x)


cpdef int index(uint128 x):
    """
    Return position of first element in given bitset, counting from 0.
    Return 128 if bitset is empty.
    """
    cdef int part1 = __builtin_ctzll(<unsigned long long>x)
    cdef int part2 = __builtin_ctzll(<unsigned long long>(x >> 64))
    return part1 if part1 < 64 else 64 + part2


cpdef int domain(uint128 x):
    """Return position of last vertex in given bitset."""
    raise NotImplementedError
    return 64 - __builtin_clzl(x)


cpdef int size(uint128 x):
    """Return size of given uint128."""
    return __builtin_popcountll(x) + __builtin_popcountll(<unsigned long long>(x >> 64))


cpdef uint128 bit(int position):
    return (<uint128>1 << position)


cpdef uint128 universe = ((<uint128>1 << 127) - 1) + (<uint128>1 << 127)


cpdef uint128 subtract(uint128 self, uint128 other):
    return self - (self & other)


cpdef contains(uint128 self, uint128 other):
    return self & other == self


cpdef uint128 invert(uint128 x, unsigned int l):
    """Return inverse where universe has length l"""
    l = 128 - l
    return subtract(((universe << l) >> l), x)


cpdef uint128 join(args):
    cdef uint128 v, result = 0
    for v in args:
        result |= v
    return result


def iterate(uint128 n):
    cdef uint128 b
    while n:
        b = n & (~n + 1)
        yield b
        n ^= b


def subsets(uint128 self, int minsize=0, int maxsize=-1):
    """Yield subbitsets from specified size ordered by size ascending."""
    if minsize < 0:
        minsize = size(self) + 1 + minsize
    if maxsize < 0:
        maxsize = size(self) + 1 + maxsize

    sets = [0L]
    for v in iterate(self):
        sets.extend([s | v for s in sets])

    return [s for s in sets if size(s) >= minsize and size(s) <= maxsize]

def tostring(self):
    return '{{{}}}'.format(', '.join(str(index(v)) for v in iterate(self)))

#cdef extern int __builtin_ctzl(unsigned long x)
#cdef extern int __builtin_clzl(unsigned long x)
#cdef extern int __builtin_popcountl(unsigned long x)

#cpdef int index(long x):
    #"""Return position of first vertex in given bitset."""
    #return __builtin_ctzl(x)

#cpdef int domain(long x):
    #"""Return position of last vertex in given bitset."""
    #return 64 - __builtin_clzl(x)

#cpdef int size(long x):
    #"""Return size of given bitset."""
    #return __builtin_popcountl(x)


#cpdef long subtract(long self, long other):
    #return self - (self & other)


#cpdef long join(args):
    #cdef long v, result = 0
    #for v in args:
        #result |= v
    #return result


#cpdef long invert(long x, long l):
    #"""Return inverse where universe has length l"""
    #return 2 ** l - 1 - x


#def iterate(long n):
    #cdef long b
    #while n:
        #b = n & (~n + 1)
        #yield b
        #n ^= b


#def contains(long self, long other):
    #return self & other == self


#def tostring(self):
    #return 'BitSet{{{}}}'.format(', '.join(str(index(v)) for v in iterate(self)))


#def subsets(long self, int minsize=0, int maxsize=-1):
    #"""Yield subbitsets from specified size ordered by size ascending."""
    #if minsize < 0:
        #minsize = size(self) + 1 + minsize
    #if maxsize < 0:
        #maxsize = size(self) + 1 + maxsize

    #sets = [0L]
    #for v in iterate(self):
        #sets.extend([s | v for s in sets])

    #return [s for s in sets if size(s) >= minsize and size(s) <= maxsize]

