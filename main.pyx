# encoding: utf-8
# cython: profile=True
# filename: main.pyx

from graph import Graph
from bipartite import Bipartite
from tree import Tree
from graph64 import to64
from bitset64 import tostring
from plot import plot

from grids import squares, cliques, semicliques, semisquares
from linearbooleanwidth import linearbooleanwidth
from linearbooleancost import linearbooleancost
from booleanwidth import booleanwidth
from booleancost import booleancost
from dynamicprogramming import print_decomposition

graph = squares(2, 2)
#graph = cliques(4, 4)
#graph = semisquares(3, 3)
#graph = semicliques(3, 3)
#graph = Bipartite.generate_random(5).gridify(2)
#graph = Graph.load('input/bipartite5.dgf')
plot(graph, engine='neato') # squares
#plot(graph, engine='dot') # cliques
#plot(graph, engine='fdp') # cliques
#plot(graph, engine='twopi') # cliques
#plot(graph, engine='circo') # cliques
#exit()
print_decomposition(*linearbooleanwidth(to64(graph)))
print_decomposition(*linearbooleancost(to64(graph)))
#print_decomposition(*booleanwidth(to64(graph)))
#print_decomposition(*booleancost(to64(graph)))

