#from sage.graphs.graph_decompositions.vertex_separation import path_decomposition
from graph import Graph as MyGraph
from bitset import BitSet
from plot import plot

x = BitSet(999)
l = len(x)
print(l)
print(x.tolist(l))

graph = MyGraph.generate_random(5, 5)
plot(graph)
#M = Matrix(graph.adjacency_matrix())
#print(M)
#G = Graph(M)
#print(G)
