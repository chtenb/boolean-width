from PIL import Image
from random import randint

from plot import plot_bipartite_graph, plot_graph
from bipartite import Bipartite, Graph
from mis import bron_kerbosch_mc


#graph = Graph.generate_random(10, 10)
#complement = graph.complement()

# print(graph)
# print(len(list(bron_kerbosch(graph))))
# print(len(list(bron_kerbosch(complement))))

for _ in range(10):
    nr_vertices = 15
    nr_edges = randint(10, 50)
    graph = Bipartite.generate_random(nr_vertices, nr_edges)
    bipartite_complement = graph.bipartite_complement()

    # print(graph)
    booldim1 = len(list(bron_kerbosch_mc(graph)))
    booldim2 = len(list(bron_kerbosch_mc(bipartite_complement)))
    #print('{}, {}'.format(booldim1, booldim2))
    print(abs(booldim1 - booldim2))
    #if abs(booldim1 - booldim2) > 1:
        #print('!!!!')

#size = (512, 512)
#im = Image.new('RGB', size, 'white')

#plot_graph(im, graph, color=(178, 0, 0))
#plot_graph(im, complement, color=(0, 0, 178))
#plot_bipartite_graph(im, graph)
#plot_bipartite_graph(im, bipartite_complement, color=(0, 0, 128))

#im.save('output/test.png', 'png')
