from PIL import Image
from random import randint

from plot import plot_bipartite_graph, plot_graph
from bipartite import Bipartite, Graph
from mis import bron_kerbosch_mis, bron_kerbosch_mc


def mc_vs_mis():
    for _ in range(20):
        nr_vertices = 20
        nr_edges = randint(0, int(nr_vertices * (nr_vertices - 1) / 2))
        graph = Graph.generate_random(nr_vertices, nr_edges)

        mis = list(bron_kerbosch_mis(graph))
        nr_mis = len(mis)
        mc = list(bron_kerbosch_mc(graph))
        nr_mc = len(mc)
        print('{} - {} = {}'.format(nr_mis, nr_mc, abs(nr_mis - nr_mc)))


def mc_vs_mis_bipartite():
    for _ in range(20):
        nr_vertices = 20
        nr_edges = randint(0, int((nr_vertices / 2) ** 2))
        graph = Bipartite.generate_random(nr_vertices, nr_edges)

        mis = list(bron_kerbosch_mis(graph))
        nr_mis = len(mis)
        mc = list(bron_kerbosch_mc(graph))
        nr_mc = len(mc)
        print('{} - {} = {}'.format(nr_mis, nr_mc, abs(nr_mis - nr_mc)))

mc_vs_mis()

#size = (512, 512)
#im = Image.new('RGB', size, 'white')
#plot_graph(im, graph, color=(178, 0, 0))
#plot_graph(im, complement, color=(0, 0, 178))
#im.save('output/test.png', 'png')
