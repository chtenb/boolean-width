from .graph import Graph
from .bipartite import Bipartite
from .tree import Tree
from .graph128 import to128
from .bitset128 import tostring, iterate
from .plot import plot

from .grids import squares, cliques, semicliques, semisquares
from .lboolc import linearbooleancost, greedy_lbc, relative_neighborhood_lbc
from .lboolw import (linearbooleanwidth, greedy_lbw, relative_neighborhood_lbw,
        compute_lbw, construct_decomposition)
from .boolw import booleanwidth, greedy_bw
from .boolc import booleancost
from .dynamicprogramming import print_decomposition, print_linear_decomposition, compute_booldim

import time

from .experiments import lboolw_exact_vs_heuristic

def run():
    start_time = time.time()

    lboolw_exact_vs_heuristic.run()
    return

    # GENERATE
    graph = Graph.generate_random(16, 0.5)
    #graph = squares(5, 3)
    #graph = cliques(4, 4)
    #graph = semisquares(5, 5)
    #graph = semicliques(3, 3)
    #graph = Bipartite.generate_random(5).gridify(2)
    graph128 = to128(graph)

    # PLOT
    #graph = Graph.load('input/jean.dgf')
    #plot(graph, engine='neato') # squares
    plot(graph, engine='dot') # cliques
    #print('Graph drawn')
    #plot(graph, engine='fdp') # cliques
    #plot(graph, engine='twopi') # cliques
    #plot(graph, engine='circo') # cliques
    #exit()

    # COMPUTE
    lbw, booldim = compute_lbw(graph128)
    result = lbw[graph128.vertices]
    print_decomposition(result, construct_decomposition(lbw, booldim, graph128.vertices))

    #print('--- {} seconds ---'.format(time.time() - start_time))

    #result2, decomposition = linearbooleanwidth(graph128)
    #print_decomposition(result2, decomposition)
    #assert result == result2

    #result3, decomposition = booleanwidth(graph128)
    #print_decomposition(result3, decomposition)

    #print_linear_decomposition(*greedy_lbw(graph128, depth=2))
    #print_linear_decomposition(*relative_neighborhood_lbw(graph128, depth=1))
    #print_decomposition(*greedy_bw(graph128))
    #print_linear_decomposition(*greedy_lbc(graph128, depth=2))
    #print_linear_decomposition(*greedy_lbc(graph128, depth=3))

    print('--- {} seconds ---'.format(time.time() - start_time))

    #manual = []
    #todo = graph128.V
    #for v in iterate(graph128.V):
        #manual.append((v, todo - v, compute_booldim(graph128, todo - v)))
        #todo -= v
    #cost = sum(compute_booldim(graph128, A) + compute_booldim(graph128, B) for A, B, _ in manual)
    #print_decomposition(cost, manual)
    #print_decomposition(*booleanwidth(to128(graph)))
    #print_decomposition(*booleancost(to128(graph)))

