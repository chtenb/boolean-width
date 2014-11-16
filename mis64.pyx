"""This module contains algorithms for computing the maximal independent sets."""

from bitset64 import iterate, length, tostring
from bitset import BitSet

cpdef int recursion(graph, long _include, long rest, long exclude):
    if not exclude and not rest:
        return 1

    cdef long u, pivot = 0
    cdef int size, minsize = 999999
    for u in iterate(rest | exclude):
        size = length(rest & graph[u])
        if size < minsize:
            pivot = u
            minsize = size

    cdef int count = 0
    for v in iterate(rest & (graph[pivot] | pivot)):
        count += recursion(graph,
                _include | v,
                rest - (rest & (graph[v] | v)),
                exclude - (exclude & graph[v])
                )
        rest -= v
        exclude |= v

    return count

cpdef mis_count(graph, vertices):
    """Compute all maximal independent sets."""
    return recursion(graph, 0L, <long>vertices, 0L)


