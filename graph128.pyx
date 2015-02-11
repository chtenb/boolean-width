from random import sample
from bitset128 import iterate, domain, index
from bitset128 cimport uint128
#from libcpp.unordered_map cimport unordered_map
from cpython cimport array
from array import array

cpdef to128(graph):
    vertices = <uint128>graph.vertices
    neighborhoods = {}
    for key in graph.vertices:
        neighborhoods[<uint128>key] = <uint128>graph.neighborhoods[key]

    return Graph(vertices, neighborhoods)


class Graph:

    def __init__(self, uint128 vertices=0L, neighborhoods=None):
        self.vertices = vertices
        self.neighborhoods = neighborhoods or {}


cpdef to128_2(graph):
    vertices = <uint128>graph.vertices

    cdef array.array neighborhoods = array('L', domain(vertices) * [0L])
    for key in graph.vertices:
        neighborhoods[index(<int>key)] = <uint128>graph.neighborhoods[key]

    return Graph2(vertices, neighborhoods)


cdef class Graph2:

    cdef public uint128 vertices
    cdef public array.array neighborhoods

    def __cinit__(self, uint128 vertices, array.array neighborhoods):
        self.vertices = vertices
        self.neighborhoods = neighborhoods


#
# TESTING
#


#import cProfile

#graph = Graph.generate_random(15)
#graph1 = to128(graph)
#graph2 = to128_2(graph)

#cdef c1 = 2**10
#cpdef run1():
    #cdef uint128 x
    #for i in range(9999999):
        #x = graph1.N[c1]
    #return x

#cdef c2 = 10
#cpdef run2():
    #cdef uint128 x
    #for i in range(9999999):
        #x = graph2.N[index(c1)]
    #return x

#cProfile.runctx('run1()', globals(), locals())
#cProfile.runctx('run2()', globals(), locals())
