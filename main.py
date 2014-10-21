from PIL import Image

from plot import plot_bipartite_graph, plot_graph
from bipartite import Bipartite
from graph import Graph
#from convexbipartite import ConvexBipartite

from booleanwidth import booleanwidth  # , booleancost, cut
from linearbooleanwidth import linearbooleanwidth  # , booleancost, cut

# mis_bipartite_complement()
#graph = Bipartite.load('output/10,10.graph')


graph = Graph.load('input/petersen.dgf')
#graph = Graph.generate_random(7, 10)
#subvertices = [graph.vertices[BitSet(2 ** i)] for i in range(4)]
#subgraph = graph.subgraph(subvertices)
#graph = Bipartite.generate_random(10, 10)
#subset = VertexSet(graph.vertices[i] for i in range(1))
#subgraph = cut(graph, subset)
bw, booldim, decomposition = linearbooleanwidth(graph)
#bw, booldim, decomposition = booleanwidth(graph)
print('booleanwidth: ' + str(bw))
print('decomposition: ' + '\n'.join('({}, {}): {},{}'.format(
    graph[a], graph[b], booldim[a], booldim[b]) for a, b in decomposition))
#print('booldim: ' + ''.join('{}: {}\n'.format(graph[b], booldim[b]) for a, b in decomposition))
# print(booleancost(graph))
#vs = set(v for v in graph.vertices)
#vs = set(graph.vertices)
# print(vs)
#complement = graph.complement()
#complement = graph.subgraph(sample(list(graph.vertices.values()), 7))
#bipartite = Bipartite.generate_random(10, 10)
#graph = ConvexBipartite.generate_random(10, 10)
#complement = graph.bipartite_complement()

size = (512, 512)
im = Image.new('RGB', size, 'white')
plot_graph(im, graph, color=(178, 0, 0))
#plot_graph(im, subgraph, color=(178, 0, 0))
#plot_bipartite_graph(im, bipartite, color=(178, 0, 0))
#plot_graph(im, complement, color=(0, 178, 0))
im.save('output/test.png', 'png')
