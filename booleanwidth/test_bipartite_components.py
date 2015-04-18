from .bipartite import Bipartite
from .plot import plot, plot_bipartite
from .graph import Graph
from .booleanwidth import cut

from math import log

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
    n = 8
    graph = Graph.generate_random(n)

    connected_components = []
    un_components = []
    for subset in graph.vertices.subsets(1, -2):
        cut_graph = cut(graph, subset)


        new_un_components = []
        while 1:
            found = False
            for candidate in cut_graph.group1.subsets(1, -2):
                complement = cut_graph.group1 - candidate
                if is_un_component(cut_graph, candidate) and is_un_component(cut_graph, complement):
                    found = True
                    break

            if found:
                new_un_components.append(candidate)
                cut_graph.remove(candidate)
            else:
                break

        largest_un_component = max([len(s) for s in new_un_components] or [0])
        print(largest_un_component, 'instead of', len(subset))
        un_components.extend(new_un_components)
        #if len(connected_components) > len(un_components):
            #plot_bipartite(cut_graph).save('output/test.png')
            #print(un_components)
            #print(connected_components)
            #exit()

    count = sum(len(s) for s in un_components) #int(log(len(un_components), 2))
    #count = int(log(len(connected_components), 2))
    #print(count)
    #if count < n:
        #plot(graph)
        #break
    #print(int(log(len(un_components), 2)) - int(log(len(connected_components), 2)))
