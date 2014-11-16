"""
This module contains cython functions for making int64 work like a set.
"""

#from cpython cimport array
#from array import array

cpdef long subtract(long self, long other):
    return self - (self & other)


def iterate(long n):
    cdef long b
    while n:
        b = n & (~n + 1)
        yield b
        n ^= b


cpdef int length(long self):
    cdef result = 0
    for _ in iterate(self):
        result += 1
    return result


cpdef long join(args):
    cdef long v, result = 0
    for v in args:
        result |= v
    return result


from math import log

def tostring(self):
    return 'BitSet{{{}}}'.format(', '.join(str(int(log(v, 2))) for v in iterate(self)))

cpdef to64(graph):
    result = {}
    for key in graph.vertices:
        result[<long>key] = <long>graph.neighborhoods[key]
    return result


#def subsets(self, minsize=None, maxsize=None):
    #"""Yield subbitsets from specified size ordered by size ascending."""
    ## TODO in 2^n time
    #minsize = minsize or 0
    #maxsize = maxsize or len(self)
    #for k in range(minsize, maxsize + 1):
        #yield from (BitSet.join(*b) for b in combinations(list(self), k))

