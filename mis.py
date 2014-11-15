"""This module contains algorithms for computing the maximal independent sets."""

from bitset import BitSet


def bron_kerbosch_mis_count(graph):
    """Compute all maximal independent sets."""
    def recursion(include, rest, exclude):
        assert include or exclude or rest
        assert not include & rest
        assert not include & exclude
        assert not rest & exclude

        if not exclude and not rest:
            return 1

        minsize = float('inf')
        for u in rest | exclude:
            size = len(rest & graph(u))
            if size < minsize:
                pivot = u
                minsize = size

        count = 0
        for v in rest & (graph[pivot]):
            count += recursion(include | v, rest - (graph[v]), exclude - graph(v))
            rest -= v
            exclude |= v

        return count

    return recursion(BitSet(), graph.vertices, BitSet())


def bron_kerbosch_mc(graph):
    """Compute all maximal cliques."""
    def recursion(include, rest, exclude):
        assert include or exclude or rest
        assert not include & rest
        assert not include & exclude
        assert not rest & exclude

        if not exclude and not rest:
            yield include
            return

        for v in rest:
            yield from recursion(include | v, rest & graph(v), exclude & graph(v))
            rest -= v
            exclude |= v

    yield from recursion(BitSet(), graph.vertices, BitSet())


def bron_kerbosch_mis(graph):
    """Compute all maximal independent sets."""
    def recursion(include, rest, exclude):
        assert include or exclude or rest
        assert not include & rest
        assert not include & exclude
        assert not rest & exclude

        if not exclude and not rest:
            yield include
            return

        minsize = float('inf')
        for u in rest | exclude:
            size = len(rest & graph(u))
            if size < minsize:
                pivot = u
                minsize = size

        for v in rest & (graph[pivot]):
            yield from recursion(include | v, rest - (graph[v]), exclude - graph(v))
            rest -= v
            exclude |= v

    yield from recursion(BitSet(), graph.vertices, BitSet())


#
# Comparisons and Misc
#


from random import randint
from graph import Graph
from bipartite import Bipartite


def mul_abs(x):
    return max(x, 1 / x)


def mc_vs_mis():
    """
    Compare the number of maximal cliques to the number of
    maximal independent sets.
    """
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
    bound = 10
    nr_vertices = 10

    while 1:
        max_nr_edges = int((nr_vertices / 2) ** 2)
        nr_edges = randint(1, max_nr_edges - 1)
        nr_edges_compl = max_nr_edges - nr_edges
        graph = Bipartite.generate_random(nr_vertices, nr_edges)
        bipartite_compl = graph.bipartite_complement()

        mis = list(bron_kerbosch_mis(graph))
        nr_mis = len(mis)
        # print(mis)

        vertices = set(graph.vertices)
        edges = set((v, w) for v in graph.vertices for w in graph.vertices)
        compl_mis = [vertices.difference(s) for s in mis]
        # print(compl_mis)

        mis_compl = list(bron_kerbosch_mis(bipartite_compl))
        nr_mis_compl = len(mis_compl)
        #print('MIS: {}\n<-->\nMBC: {}'.format(mis, mis_compl))
        #print('MIS: {}\nMIS_compl: {}\nMBC: {}'.format(mis, compl_mis, mis_compl))
        # print('---------------------------------------')

        difference = abs(nr_mis - nr_mis_compl)
        if difference >= bound:
            print('Edges: {}, #MIS: {} | Edges_c: {}, #MIS_c : {}'.format(
                nr_edges, nr_mis,
                nr_edges_compl, nr_mis_compl
            ))

            graph.save('output/{},{}.graph'.format(nr_vertices, difference))

            #size = (512, 512)
            #im = Image.new('RGB', size, 'white')
            #plot_bipartite_graph(im, graph, color=(178, 0, 0))
            #im.save('output/test.png', 'png')

            break

        # print('{}, {}, {}, {}'.format(
            #nr_mis - nr_mis_compl,
            #round(nr_mis / nr_mis_compl, 1),
            #round((nr_mis / nr_edges) / (nr_mis_compl / nr_edges_compl), 1),
            #round((nr_mis * nr_edges) / (nr_mis_compl * nr_edges_compl), 1)
        #))
