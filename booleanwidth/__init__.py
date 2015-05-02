from .graph import Graph
from .bipartite import Bipartite
from .tree import Tree
from .graph128 import to128
from .bitset128 import (tostring, iterate, subsets_of_size, subsets_by_size, index, domain)
from .plot import plot
from .components import components, bfs

from .grids import squares, cliques, semicliques, semisquares
from .lboolw import (linearbooleanwidth, greedy_lbw, relative_neighborhood_lbw,
                     compute_lboolw, construct_lboolw_decomposition)
from .heuristic import (greedy, check_decomposition, first_improvement, greedy_cost,
        greedy_cost_step, check_decomposition, check_decomposition_cost, greedy_lun,
        greedy_cost_ties)
from .lboolc import compute_lboolc, construct_lboolc_decomposition, linearbooleancost
from .boolw import booleanwidth, greedy_bw
from .boolc import booleancost
from .dynamicprogramming import print_decomposition, print_linear_decomposition, compute_booldim

import time
import math

from .experiments import lboolw_exact_vs_heuristic, heuristics
from .profiling import profile

def run():
    start_time = time.time()

    #lboolw_exact_vs_heuristic.run()
    #heuristics.run()
    #return

    #print(0, domain(0))
    #print(1, domain(1))

    #print('------')

    #for i in range(128):
        #print(i, domain(1 << i))
        #print(i, index(1 << i))
    #return

    #print(subsets_by_size(15))
    #return


    # GENERATE
    #graph = Graph.load('input/mainuk.dgf')
    #graph = Graph.load('input/david-pp.dgf')
    #graph = Graph.load('input/1aba.dgf')
    #graph = Graph.load('input/1ail.dgf')
    #graph = Graph.load('input/queen5_5.dgf')
    #graph = Graph.load('input/queen6_6.dgf')
    #graph = Graph.load('input/queen7_7.dgf')
    #graph = Graph.load('input/david.dgf')
    graph = Graph.load('input/alarm.dgf')
    #graph = Graph.load('input/pr152.dgf')
    #graph = Graph.load('input/BN_100.dgf')
    #graph = Graph.generate_random(35, 0.5)
    #graph.save('input/rand.dgf')
    #return
    #graph = squares(5, 3)
    #graph = cliques(4, 4)
    #graph = semisquares(5, 5)
    #graph = semicliques(3, 3)
    #graph = Bipartite.generate_random(5).gridify(2)

    #graph = to128(graph)

    # PLOT
    # plot(graph, engine='neato') # squares
    #plot(graph, engine='dot')  # cliques
    #print('Graph drawn')
    # plot(graph, engine='fdp') # cliques
    # plot(graph, engine='twopi') # cliques
    # plot(graph, engine='circo') # cliques

    #print(list(components(graph128)))
    #print(list(bfs(graph128, 1)))
    #return

    # COMPUTE
    # WIDTH
    #lboolw, booldim = compute_lboolw(graph128)
    #result = lboolw[graph128.vertices]
    #print(math.log(result, 2))
    #print_decomposition(result, construct_lboolw_decomposition(lboolw, booldim, graph128.vertices))

    #with open('output/ZOMG', 'r') as f:
        #decomposition = [2**int(line) for line in f]
    #lboolw = check_decomposition(graph128, decomposition)
    #print(lboolw)
    #print(math.log(lboolw, 2))
    #return

    #print('depth = ' + str(i))
    print('greedy')
    def f():
        lboolw, decomposition = greedy_cost_ties(graph, 100)
        #lboolw, decomposition = greedy_cost(graph, 0)
        #lboolw, decomposition = greedy(graph, 3)
        print(lboolw)
        print(math.log(lboolw, 2))
        real_lboolw = check_decomposition(graph, decomposition)
        #real_lboolw = check_decomposition_cost(graph, decomposition)
        print(real_lboolw)
        print(math.log(real_lboolw, 2))
    profile(f)

    #print('greedy cost')
    #def f():
        #result, decomposition = greedy_cost(graph128, 0)
        #print(result)
        #print(decomposition)
        #print(check_decomposition_cost(graph128, decomposition))
    #profile(f)
    #print(math.log(lboolc / 18, 2))

    #print('first_improvement')
    #lboolw, decomposition = first_improvement(graph128, i)
    #print(lboolw)
    #print(math.log(lboolw, 2))
    #print('-------')
    #with open('output/ZOMG', 'w') as f:
        #for vertex in decomposition:
            #v = index(vertex)
            #print(v)
            #f.write('{}\n'.format(v))


    #print('--- {} seconds ---'.format(time.time() - start_time))

    #result2, decomposition = linearbooleanwidth(graph128)
    #print_decomposition(result2, decomposition)
    #assert result == result2

    # COST
    #print('exact cost')
    #lboolc, booldim = compute_lboolc(graph128)
    #result = lboolc[graph128.vertices]
    #decomposition = list(construct_lboolc_decomposition(lboolc, booldim, graph128.vertices))
    #print(result)
    #print(decomposition)
    #print(check_decomposition_cost(graph128, decomposition))
    #print_decomposition(result, decomposition)

    #result2, decomposition = linearbooleancost(graph128)
    #print_decomposition(result2, decomposition)
    #assert result == result2

    #result3, decomposition = booleanwidth(graph128)
    #print_decomposition(result3, decomposition)

    #print_linear_decomposition(*greedy_lbw(graph128, depth=2))
    #print_linear_decomposition(*relative_neighborhood_lbw(graph128, depth=1))
    # print_decomposition(*greedy_bw(graph128))
    #print_linear_decomposition(*greedy_lbc(graph128, depth=2))
    #print_linear_decomposition(*greedy_lbc(graph128, depth=3))

    print('--- {} seconds ---'.format(time.time() - start_time))

    #manual = []
    #todo = graph128.V
    # for v in iterate(graph128.V):
    #manual.append((v, todo - v, compute_booldim(graph128, todo - v)))
    #todo -= v
    #cost = sum(compute_booldim(graph128, A) + compute_booldim(graph128, B) for A, B, _ in manual)
    #print_decomposition(cost, manual)
    # print_decomposition(*booleanwidth(to128(graph)))
    # print_decomposition(*booleancost(to128(graph)))
