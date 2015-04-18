from sage.all import *
from sage.graphs.graph_decompositions.vertex_separation import path_decomposition


def pathwidth(graph):
    M = Matrix(graph.adjacency_matrix())
    G = Graph(M)
    #plot(G).show()
    #input("Press Enter to continue...")
    return path_decomposition(G)

