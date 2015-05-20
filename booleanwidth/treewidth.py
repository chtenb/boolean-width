from .graph import Graph
from sage.all import Matrix, Graph as SageGraph

def treewidth(graph):
    M = Matrix(graph.adjacency_matrix())
    G = SageGraph(M)
    #input("Press Enter to continue...")
    return G.treewidth()

def run():
    #graph = Graph.generate_random(20, 0.25)
    #graph = Graph.load('input/alarm.dgf')
    graph = Graph.load('input/barley.dgf')
    print(treewidth(graph))

run()

