from linearbooleanwidth64 import (linearbooleanwidth_decomposition,
        linearbooleanwidth_decomposition_greedy,
        linearbooleanwidth_from_decomposition,
        linearboolwidthtable)
from booleanwidth64 import booleandim
from graph import Graph
from graph64 import to64
from bitset64 import tostring, size, invert
from plot import plot

while 1:
    graph = Graph.generate_random(7)
    G = to64(graph)
    #print(G.V)
    #print(size(G.V))
    #print(invert(1, size(G.V)))
    #break

    bwtable, booldim = linearboolwidthtable(G)
    decomposition = list(linearbooleanwidth_decomposition(bwtable, booldim, G.V))
    lboolw = linearbooleanwidth_from_decomposition(booldim, decomposition)

    decomposition_greedy = list(linearbooleanwidth_decomposition_greedy(bwtable, booldim, G.V, size(G.V)))
    lboolw_greedy = linearbooleanwidth_from_decomposition(booldim, decomposition_greedy)
    print('width: {}, greedy width: {}'.format(lboolw, lboolw_greedy))

    if lboolw != lboolw_greedy:
        print('\n'.join(('({}, {}): {}'.format(tostring(a), tostring(b), booldim[b]) for a,b in decomposition)))
        print('\n'.join(('({}, {}): {}'.format(tostring(a), tostring(b), booldim[b]) for a,b in decomposition_greedy)))

        plot(graph)
        break
