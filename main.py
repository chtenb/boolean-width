from PIL import Image
import cProfile

from plot import plot_bipartite, plot_circle, plot
from bipartite import Bipartite
from graph import Graph
from bitset import BitSet
from tree import Tree
from linearbooleanwidth import linearbooleanwidth

#from random import choice
#b = BitSet.from_identifier(1,2,3)
#print(b)
#print(choice(list(b)))

#from booleanwidth import booleanwidth, booleandim
#from linearbooleanwidth import linearbooleanwidth

# mis_bipartite_complement()
#graph = Bipartite.load('output/10,10.graph')


graph = Graph.load('input/petersen.dgf')
plot(graph)
print(list(linearbooleanwidth(graph)))

#cProfile.run('booleandim(graph)')
#booleandim(graph)

#graph = Tree.generate_random(9)
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
