"""This module contains algorithms for computing the maximal independent sets."""

from bitset64 import iterate, length, tostring
from bitset import BitSet

cpdef int recursion(N, long includes, long rest, long excludes):
    if not excludes and not rest:
        return 1

    cdef long u, pivot = 0
    cdef int size, minsize = 999999
    for u in iterate(rest | excludes):
        size = length(rest & N[u])
        if size < minsize:
            pivot = u
            minsize = size

    cdef int count = 0
    for v in iterate(rest & (N[pivot] | pivot)):
        count += recursion(N,
                includes | v,
                rest - (rest & (N[v] | v)),
                excludes - (excludes & N[v])
                )
        rest -= v
        excludes |= v

    return count

cpdef mis_count(N, long vertices):
    """Compute all maximal independent sets."""
    return recursion(N, 0L, vertices, 0L)


