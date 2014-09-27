from plot import plot_bipartite_graph, plot_graph
from bipartite import Bipartite
from PIL import Image


graph = Bipartite.generate_random(10, 10)
bipartite_complement = graph.bipartite_complement()
print(graph)

size = (512, 512)
im = Image.new('RGB', size, 'white')
plot_bipartite_graph(im, graph)
plot_bipartite_graph(im, bipartite_complement, color=(0, 0, 128))
#plot_graph(im, graph)
im.save('output/test.png', 'png')
