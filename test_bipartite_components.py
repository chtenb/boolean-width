from bipartite import Bipartite
from plot import plot, plot_bipartite
from math import log
from graph import Graph
from booleanwidth import cut


def is_connected_component(graph, subset):
    complement = graph.group1 - subset
    return not graph(subset) & graph(complement)

def is_un_component(graph, subset):
    complement = graph.group1 - subset
    return all(not graph(a) or graph(a) not in graph(complement) for a in subset)

    #if not graph(subset):
        #return True

    #for a in subset:
        #if graph(a) & graph.group2 in graph(complement) & graph.group2:
            #return False
    #return True


# Count number of minimal components in random graphs
while 1:
    graph = Graph.generate_random(10)

    for subset in graph.vertices.subsets(1, -2):
        cut_graph = cut(graph, subset)
        un_components = []
        connected_components = []


        for subset in cut_graph.group1.subsets():
            complement = cut_graph.group1 - subset
            if is_un_component(cut_graph, subset) and is_un_component(cut_graph, complement):
                un_components.append(subset)
            if is_connected_component(cut_graph, subset):
                connected_components.append(subset)

        if len(connected_components) > len(un_components):
            plot_bipartite(cut_graph).save('output/test.png')
            print(un_components)
            print(connected_components)
            exit()

        print(int(log(len(un_components), 2)) - int(log(len(connected_components), 2)))
