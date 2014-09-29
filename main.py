from PIL import Image
from random import randint

from plot import plot_bipartite_graph, plot_graph
from bipartite import Bipartite, Graph
from mis import bron_kerbosch_mis, bron_kerbosch_mc


def mul_abs(x):
    return max(x, 1 / x)


def mc_vs_mis():
    """Compare the number of maximal cliques to the number of maximal independent sets."""
    for _ in range(20):
        nr_vertices = 20
        nr_edges = randint(0, int(nr_vertices * (nr_vertices - 1) / 2))
        graph = Graph.generate_random(nr_vertices, nr_edges)

        mis = list(bron_kerbosch_mis(graph))
        nr_mis = len(mis)
        mc = list(bron_kerbosch_mc(graph))
        nr_mc = len(mc)
        #print('{} - {} = {}'.format(nr_mis, nr_mc, abs(nr_mis - nr_mc)))
        print('{} / {} = {}'.format(nr_mis, nr_mc, mul_abs(nr_mis / nr_mc)))


def mis_bipartite_complement():
    """
    Compare the number of maximal independent sets to the number of maximal
    independent sets in the bipartite complement.
    """
    for _ in range(20):
        nr_vertices = 20
        nr_edges = randint(0, int((nr_vertices / 2) ** 2))
        graph = Bipartite.generate_random(nr_vertices, nr_edges)
        bipartite_complement = graph.bipartite_complement()

        mis = list(bron_kerbosch_mis(graph))
        nr_mis = len(mis)
        mis_complement = list(bron_kerbosch_mis(bipartite_complement))
        nr_mis_complement = len(mis_complement)
        #print('{} - {} = {}'.format(nr_mis, nr_mis_complement, abs(nr_mis - nr_mis_complement)))
        print('{} / {} = {}'.format(nr_mis, nr_mis_complement, mul_abs(nr_mis / nr_mis_complement)))


nr_vertices = 5
nr_edges = randint(0, int((nr_vertices / 2) ** 2))
graph = Bipartite.generate_random(nr_vertices, nr_edges)
size = (512, 512)
im = Image.new('RGB', size, 'white')
#plot_graph(im, graph, color=(178, 0, 0))
plot_bipartite_graph(im, graph, color=(178, 0, 0))
#plot_graph(im, complement, color=(0, 0, 178))
im.save('output/test.png', 'png')
