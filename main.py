from graph import Graph
from bipartite import Bipartite
from tree import Tree
from convexbipartite import ConvexBipartite

from linearbooleanwidth import linearbooleanwidth, compare_linear_balanced, preprocess
from booleanwidth import booleanwidth, booleandim
from plot import plot_bipartite, plot_circle, plot

#graph = Graph.load('input/petersen.dgf')
#graph = Bipartite.generate_random(10, 10)
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
graph = Tree.generate_random_binary(13)
def run(graph):
    print(linearbooleanwidth(graph)[0])
cProfile.run('run(graph)')
#run(graph)
exit()

graph = Tree.generate_random_binary(22)
preprocess(graph)
plot(graph)
lbw, lbooldim, ldecomposition = linearbooleanwidth(graph)
#print('linear booleanwidth tree: ' + str(linearbooleanwidth_trees(graph)))
print('linear booleanwidth: ' + str(lbw))
#print('linear decomposition: ' + '\n'.join('({}, {}): {},{}'.format(
    #a, b, lbooldim[a], lbooldim[b]) for a, b in ldecomposition))
print('linear decomposition: ' + ', '.join('({}: {})'.format(
    a, lbooldim[b]) for a, b in ldecomposition))


#plot_graph(im, graph, color=(178, 0, 0))
#im.save('output/test.png', 'png')
