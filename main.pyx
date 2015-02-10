# encoding: utf-8
# cython: profile=True
# filename: main.pyx

from graph import Graph
from bipartite import Bipartite
from tree import Tree
from graph64 import to64
from bitset64 import tostring, iterate
from plot import plot

from grids import squares, cliques, semicliques, semisquares
from linearbooleanwidth import linearbooleanwidth
from linearbooleancost import linearbooleancost, greedy_lbc, relative_neighborhood
from booleanwidth import booleanwidth, greedy_bw
from booleancost import booleancost
from dynamicprogramming import print_decomposition, booldim


graph = squares(3, 3)
#graph = cliques(4, 4)
#graph = semisquares(3, 4)
#graph = semicliques(3, 3)
#graph = Bipartite.generate_random(5).gridify(2)
#graph = Graph.load('input/triangle4.dgf')
#plot(graph, engine='neato') # squares
plot(graph, engine='dot') # cliques
#plot(graph, engine='fdp') # cliques
#plot(graph, engine='twopi') # cliques
#plot(graph, engine='circo') # cliques
#exit()
#print_decomposition(*linearbooleanwidth(to64(graph)))
#print_decomposition(*linearbooleancost(to64(graph)))
graph64 = to64(graph)
print_decomposition(*greedy_lbc(graph64, depth=1))
print_decomposition(*relative_neighborhood(graph64, depth=1))
#print_decomposition(*greedy_bw(graph64))
#print_decomposition(*greedy_lbc(graph64, depth=2))
#print_decomposition(*greedy_lbc(graph64, depth=3))
exit()
manual = []
todo = graph64.V
for v in iterate(graph64.V):
    manual.append((v, todo - v, booldim(graph64, todo - v)))
    todo -= v
cost = sum(booldim(graph64, A) + booldim(graph64, B) for A, B, _ in manual)
print_decomposition(cost, manual)
#print_decomposition(*booleanwidth(to64(graph)))
#print_decomposition(*booleancost(to64(graph)))

