from .graph import Graph
from .plot import plot
from .lboolw import compute_lboolw_decomposition

def run():
    while 1:
        vertices = 8
        graph = Graph.generate_random(vertices)
        lbw, decomposition, _ = compute_lboolw_decomposition(graph)
        complement = graph.complement()
        lbwc, decompositionc, _ = compute_lboolw_decomposition(complement)

        if abs(lbw - lbwc) > 1:
            print('linearbooleanwidth: ' + str(lbw))
            print(list(decomposition))
            print('linearbooleanwidth complement: ' + str(lbwc))
            print(list(decompositionc))
            plot(graph)
            plot(complement, filename='output/test2')
            break

        print('try next')

