"""
This module contains cython functions for making int64 work like a set.
"""

cdef extern int __builtin_ctzl(unsigned long x)
cdef extern int __builtin_clzl(unsigned long x)
cdef extern int __builtin_popcountl(unsigned long x)

cpdef int index(long x):
    """Return position of first vertex in given bitset."""
    return __builtin_ctzl(x)

cpdef int domain(long x):
    """Return position of last vertex in given bitset."""
    return 64 - __builtin_clzl(x)

cpdef int size(long x):
    """Return size of given bitset."""
    return __builtin_popcountl(x)

#cpdef int length(long self):
    #cdef result = 0
    #for _ in iterate(self):
        #result += 1
    #return result


#from cpython cimport map
#from array import array

#cdef array.array a = array('L', [1,2,3])
#print(a)

cpdef long subtract(long self, long other):
    return self - (self & other)


def iterate(long n):
    cdef long b
    while n:
        b = n & (~n + 1)
        yield b
        n ^= b


cpdef long join(args):
    cdef long v, result = 0
    for v in args:
        result |= v
    return result


def tostring(self):
    return 'BitSet{{{}}}'.format(', '.join(str(index(v)) for v in iterate(self)))


def subsets(long self, int minsize=0, int maxsize=-1):
    """Yield subbitsets from specified size ordered by size ascending."""
    if minsize < 0:
        minsize = size(self) + 1 + minsize
    if maxsize < 0:
        maxsize = size(self) + 1 + maxsize

    sets = [0L]
    for v in iterate(self):
        sets.extend([s | v for s in sets])

    return [s for s in sets if size(s) >= minsize and size(s) <= maxsize]

