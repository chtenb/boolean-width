# encoding: utf-8
# cython: profile=True
# filename: main.pyx

from graph import Graph
from bipartite import Bipartite
from tree import Tree
from graph64 import to64
from plot import plot

import test_bipartite_components

#from linearbooleanwidth64 import linearbooleanwidth

#original = Graph.load('input/original5.dgf')
#reduced = Graph.load('input/reduced5.dgf')

#plot(original)

#print(linearbooleanwidth(to64(original))[0])
#print(linearbooleanwidth(to64(reduced))[0])
