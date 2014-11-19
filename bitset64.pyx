"""
This module contains cython functions for making int64 work like a set.
"""

#from cpython cimport map
#from array import array

#cdef array.array a = array('L', [1,2,3])
#print(a)

cpdef long subtract(long self, long other):
    return self - (self & other)


#cpdef int ffs(long b):
    #return __builtin_ffs(b);


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


#def subsets(long self, int minsize=None, int maxsize=None):
    #"""Yield subbitsets from specified size ordered by size ascending."""
    ## TODO in 2^n time
    #minsize = minsize or 0
    #maxsize = maxsize or length(self)
    #for k in range(minsize, maxsize + 1):
        #yield from (BitSet.join(*b) for b in combinations(list(self), k))

