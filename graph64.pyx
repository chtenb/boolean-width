from random import sample
from bitset64 import iterate, domain, index
#from libcpp.unordered_map cimport unordered_map
from cpython cimport array
from array import array

cpdef to64(graph):
    V = <long>graph.vertices

    N = {}
    for key in graph.vertices:
        N[<long>key] = <long>graph.neighborhoods[key]

    return Graph(V, N)

cpdef to64_2(graph):
    V = <long>graph.vertices

    cdef array.array N = array('L', domain(V) * [0L])
    for key in graph.vertices:
        N[index(<int>key)] = <long>graph.neighborhoods[key]

    return Graph2(V, N)


class Graph:

    def __init__(self, long V=0L, N=None):
        self.V = V
        self.N = N or {}

cdef class Graph2:

    cdef public long V
    cdef public array.array N

    def __cinit__(self, long V, array.array N):
        self.V = V
        self.N = N


#
# TESTING
#


#import cProfile

#graph = Graph.generate_random(15)
#graph1 = to64(graph)
#graph2 = to64_2(graph)

#cdef c1 = 2**10
#cpdef run1():
    #cdef long x
    #for i in range(9999999):
        #x = graph1.N[c1]
    #return x

#cdef c2 = 10
#cpdef run2():
    #cdef long x
    #for i in range(9999999):
        #x = graph2.N[index(c1)]
    #return x

#cProfile.runctx('run1()', globals(), locals())
#cProfile.runctx('run2()', globals(), locals())
