from graph import Graph
from bipartite import Bipartite
from tree import Tree
from convexbipartite import ConvexBipartite

from linearbooleanwidth import linearbooleanwidth, compare_linear_balanced, preprocess
from plot import plot_bipartite, plot_circle, plot

# Enable importing Cython modules
import pyximport
pyximport.install()

from linearbooleanwidth64 import (linearbooleanwidth as linearbooleanwidth64,
        linearbooleanwidth_from_decomposition)
from graph64 import to64
from booleanwidth64 import booleandim

#graph = Graph.load('input/counter.dgf')
#graph = Graph.load('input/petersen.dgf')
#graph = Graph.generate_random(10, 10)
#im = plot_bipartite(graph)
#compl = graph.bipartite_complement()
#plot_bipartite(compl, im, color=(0, 128, 0))
#im.save('output/test.png', 'png')


import cProfile
#bw, booldim, decomposition = booleanwidth(graph)
#print('booleanwidth: ' + str(bw))
#print('decomposition: ' + '\n'.join('({}, {}): {},{}'.format(
    #graph[a], graph[b], booldim[a], booldim[b]) for a, b in decomposition))

#graph = Graph.generate_random(20, 50)
#graph = Tree.generate_random(20, 50)
#plot(graph, filename='output/test')
#graph.save('balanced-13.dgf')
#graph = Tree.generate_random_binary(13)
#def run(graph):
    #print(linearbooleanwidth(graph)[0])
#cProfile.run('run(graph)')
#run(graph)
from random import randint
while 1:
#for _ in range(10):
    vertices = 8
    edges = randint(0, int(vertices * (vertices - 1) / 4))
    graph = Graph.generate_random(vertices, edges)
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

#plot_graph(im, graph, color=(178, 0, 0))
#im.save('output/test.png', 'png')
