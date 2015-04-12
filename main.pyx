# encoding: utf-8
# cython: profile=True
# filename: main.pyx

from graph import Graph
from bipartite import Bipartite
from tree import Tree
from graph128 import to128
from bitset128 import tostring, iterate
from plot import plot

from grids import squares, cliques, semicliques, semisquares
from linearbooleancost import linearbooleancost, greedy_lbc, relative_neighborhood_lbc
from linearbooleanwidth import linearbooleanwidth, greedy_lbw, relative_neighborhood_lbw
from booleanwidth import booleanwidth, greedy_bw
from booleancost import booleancost
from dynamicprogramming import print_decomposition, print_linear_decomposition, booldim

import time

def run():
    start_time = time.time()
    graph = squares(5, 5)
    #graph = cliques(4, 4)
    #graph = semisquares(5, 5)
    #graph = semicliques(3, 3)
    #graph = Bipartite.generate_random(5).gridify(2)
    #graph = Graph.load('input/jean.dgf')
    plot(graph, engine='neato') # squares
    #plot(graph, engine='dot') # cliques
    print('Graph drawn')
    #plot(graph, engine='fdp') # cliques
    #plot(graph, engine='twopi') # cliques
    #plot(graph, engine='circo') # cliques
    #exit()
    #print_decomposition(*linearbooleanwidth(to128(graph)))
    #print_decomposition(*linearbooleancost(to128(graph)))
    graph128 = to128(graph)
    #print_linear_decomposition(*greedy_lbw(graph128, depth=2))
    #print_linear_decomposition(*relative_neighborhood_lbw(graph128, depth=1))
    print_decomposition(*greedy_bw(graph128))
    #print_linear_decomposition(*greedy_lbc(graph128, depth=2))
    #print_linear_decomposition(*greedy_lbc(graph128, depth=3))
    print("--- {} seconds ---".format(time.time() - start_time))
    exit()
    #manual = []
    #todo = graph128.V
    #for v in iterate(graph128.V):
        #manual.append((v, todo - v, booldim(graph128, todo - v)))
        #todo -= v
    #cost = sum(booldim(graph128, A) + booldim(graph128, B) for A, B, _ in manual)
    #print_decomposition(cost, manual)
    #print_decomposition(*booleanwidth(to128(graph)))
    #print_decomposition(*booleancost(to128(graph)))

