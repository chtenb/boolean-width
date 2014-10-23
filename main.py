from PIL import Image
import cProfile

from plot import plot_bipartite_graph, plot_graph
from bipartite import Bipartite
from graph import Graph
from tree import Tree

from booleanwidth import booleanwidth, booleandim
from linearbooleanwidth import linearbooleanwidth

# mis_bipartite_complement()
#graph = Bipartite.load('output/10,10.graph')


#graph = Graph.load('input/petersen.dgf')
def compare_linear_balanced():
    while 1:
        graph = Bipartite.generate_random(6, 6)
        bw, booldim, decomposition = booleanwidth(graph)
        lbw, lbooldim, ldecomposition = linearbooleanwidth(graph)

        if bw < lbw:
            print('booleanwidth: ' + str(bw))
            print('d: ' + str(decomposition))
            print('decomposition: ' + '\n'.join('({}, {}): {},{}'.format(
                graph[a], graph[b], booldim[a], booldim[b]) for a, b in decomposition))

            print('linear booleanwidth: ' + str(lbw))
            print('linear decomposition: ' + '\n'.join('({}, {}): {},{}'.format(
                graph[a], graph[b], lbooldim[a], lbooldim[b]) for a, b in ldecomposition))

            size = (512, 512)
            im = Image.new('RGB', size, 'white')
            plot_graph(im, graph, color=(178, 0, 0))
            im.save('output/test.png', 'png')
            break

compare_linear_balanced()

def compare_lbw_branches():
    global graph
    for _ in range(1):
        #graph = Tree.generate_random(12, 3)
        graph = Tree.generate_random_binary(12)
        lbw, lbooldim, ldecomposition = linearbooleanwidth(graph)
        print('linear booleanwidth: ' + str(lbw))
        print('depth: ' + str(graph.depth()))
        print('number of branches: ' + str(graph.count_branches()))
        print('number of branching nodes: ' + str(graph.count_branching_nodes()))
        #print('linear decomposition: ' + '\n'.join('({}, {}): {},{}'.format(
            #graph[a], graph[b], lbooldim[a], lbooldim[b]) for a, b in ldecomposition))

#graph = Graph.generate_random(10, 10)
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
