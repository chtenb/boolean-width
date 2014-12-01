# encoding: utf-8
# cython: profile=True
# filename: main.pyx

from graph import Graph
from bipartite import Bipartite
from tree import Tree

from graph64 import to64, to64_2
from bitset64 import index

#from linearbooleanwidth import linearbooleanwidth, compare_linear_balanced, preprocess
#from plot import plot_bipartite, plot_circle, plot

#from linearbooleanwidth64 import (linearbooleanwidth as linearbooleanwidth64,
        #linearbooleanwidth_from_decomposition)
#from booleanwidth64 import booleandim

import cProfile

graph = Graph.generate_random(15)
graph1 = to64(graph)
graph2 = to64_2(graph)

cdef c1 = 2**10
cpdef run1():
    cdef long x
    for i in range(9999999):
        x = graph1.N[c1]
    return x

cdef c2 = 10
cpdef run2():
    cdef long x
    for i in range(9999999):
        x = graph2.N[index(c1)]
    return x

cProfile.runctx('run1()', globals(), locals())
cProfile.runctx('run2()', globals(), locals())
