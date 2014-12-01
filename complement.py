from graph import Graph
from bipartite import Bipartite
from tree import Tree
from convexbipartite import ConvexBipartite

from linearbooleanwidth import linearbooleanwidth, compare_linear_balanced, preprocess
from plot import plot_bipartite, plot_circle, plot

from linearbooleanwidth64 import (linearbooleanwidth as linearbooleanwidth64,
        linearbooleanwidth_from_decomposition)
from graph64 import to64
from booleanwidth64 import booleandim

import cProfile

while 1:
#for _ in range(10):
    vertices = 8
    graph = Graph.generate_random(vertices)
    #graph = Graph.load('input/counter.dgf')
    #plot(graph)
    lbw, lbooldim, ldecomposition = linearbooleanwidth64(to64(graph))

    complement = graph.complement()
    #plot(complement, filename='output/test2')
    #lbooldim_complement = booleandim(to64(complement))
    #width_complement = linearbooleanwidth_from_decomposition(lbooldim_complement, ldecomposition)
    lbwc, lbooldimc, ldecompositionc = linearbooleanwidth64(to64(complement))

    if abs(lbw - lbwc) > 1:
        print('linearbooleanwidth: ' + str(lbw))
        print('linear decomposition: ' + ', '.join('({}: {})'.format(
            a, lbooldim[b]) for a, b in ldecomposition))
        print('linearbooleanwidth complement: ' + str(lbwc))
        print('linear decomposition: ' + ', '.join('({}: {})'.format(
            a, lbooldim[b]) for a, b in ldecomposition))
        plot(graph)
        plot(complement, filename='output/test2')
        break

