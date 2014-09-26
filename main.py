from plot import plot_bipartite_graph, plot_graph
from bipartite import Bipartite

graph = Bipartite.generate_random(10, 10)
print(graph)

plot_bipartite_graph(graph)
