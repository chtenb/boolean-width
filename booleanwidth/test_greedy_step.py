from .linearbooleanwidth import (linear_decomposition,
                                linearbooleanwidth_decomposition_greedy,
                                linearbooleanwidth_from_decomposition,
                                linearboolwidthtable)
from .dynamicprogramming import booleandim
from .graph import Graph
from .graph64 import to64
from .bitset64 import tostring, size, invert
from .plot import plot

s = 8
n = 2 ** (s * (s - 1) / 2)
i = 0
# for graph in Graph.enumerate(s):
#print('{}/{}'.format(i, n))
#i += 1
while 1:
    graph = Graph.generate_random(13)
    G = to64(graph)

    bwtable, booldim = linearboolwidthtable(G)
    decomposition = list(linearbooleanwidth_decomposition(bwtable, booldim, G.V))
    lboolw = linearbooleanwidth_from_decomposition(booldim, decomposition)

    decomposition_greedy = list(
        linearbooleanwidth_decomposition_greedy(bwtable, booldim, G.V, size(G.V)))
    lboolw_greedy = linearbooleanwidth_from_decomposition(booldim, decomposition_greedy)
    print('width: {}, greedy width: {}'.format(lboolw, lboolw_greedy))

    try:
        if lboolw != lboolw_greedy:
            normal, greedy = next((decomposition[i][1], decomposition_greedy[i][1])
                                  for i in range(len(decomposition))
                                  if decomposition[i] != decomposition_greedy[i])
            if booldim[greedy] - booldim[normal] >= 2:
                print('\n'.join(('({}, {}): {}'.format(tostring(a), tostring(b), booldim[b])
                                 for a, b in decomposition)))
                print('\n'.join(('({}, {}): {}'.format(tostring(a), tostring(b), booldim[b])
                                 for a, b in decomposition_greedy)))

                plot(graph)
                break
    except StopIteration:
        pass
