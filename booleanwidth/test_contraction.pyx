from random import choice
from .graph64 import to64
from .graph import Graph

#import test_greedy_step

from linearbooleanwidth64 import linearbooleanwidth

counter = 0
while 1:
    graph = Graph.generate_random(13)
    original = to64(graph)
    graph.contract(choice(list(graph.vertices)))
    reduced = to64(graph)

    lbw_original = linearbooleanwidth(original)
    lbw_reduced = linearbooleanwidth(reduced)

    if lbw_reduced[0] > lbw_original[0]:
        print(lbw_original)
        print(lbw_reduced)
        break

    counter += 1
    print(counter)

