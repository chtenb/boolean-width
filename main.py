from PIL import Image

from plot import plot_bipartite_graph, plot_graph
from bipartite import Bipartite, Graph
from mis import bron_kerbosch


size = (512, 512)
im = Image.new('RGB', size, 'white')


graph = Graph.generate_random(3, 2)
complement = graph.complement()

plot_graph(im, graph, color=(178, 0, 0))
#plot_graph(im, complement, color=(0, 0, 178))

print(graph)
print(list(bron_kerbosch(graph)))


#graph = Bipartite.generate_random(5, 3)
#bipartite_complement = graph.bipartite_complement()

#plot_bipartite_graph(im, graph)
#plot_bipartite_graph(im, bipartite_complement, color=(0, 0, 128))

im.save('output/test.png', 'png')
