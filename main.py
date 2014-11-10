from PIL import Image

from plot import plot_bipartite, plot_circle, plot
from bipartite import Bipartite
from graph import Graph
from bitset import BitSet
from tree import Tree
from linearbooleanwidth import linearbooleanwidth
from convexbipartite import ConvexBipartite

#from booleanwidth import booleanwidth, booleandim
#from linearbooleanwidth import linearbooleanwidth

#graph = Graph.load('input/petersen.dgf')
graph = ConvexBipartite.generate_random(10, 10)
plot(graph)

#import cProfile
#cProfile.run('booleandim(graph)')

#bw, booldim, decomposition = booleanwidth(graph)
#print('booleanwidth: ' + str(bw))
#print('decomposition: ' + '\n'.join('({}, {}): {},{}'.format(
    #graph[a], graph[b], booldim[a], booldim[b]) for a, b in decomposition))

#lbw, lbooldim, ldecomposition = linearbooleanwidth(graph)
#print('linear booleanwidth: ' + str(lbw))
#print('linear decomposition: ' + '\n'.join('({}, {}): {},{}'.format(
    #graph[a], graph[b], lbooldim[a], lbooldim[b]) for a, b in ldecomposition))

#size = (512, 512)
#im = Image.new('RGB', size, 'white')
#plot_graph(im, graph, color=(178, 0, 0))
#im.save('output/test.png', 'png')
