from generator import generate_random
from plot import plot_graph

graph = generate_random(10, 10)
print(graph)
assert len(graph.vertices) == 10
assert len(graph.edges) == 10

plot_graph(graph)
