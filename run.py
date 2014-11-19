# Enable importing Cython modules
import pyximport
pyximport.install()

from sage.all import *

import cProfile

from tree import Tree
#from graph import Graph

from graph64 import to64
from bitset64 import subsets, tostring

from linearbooleanwidth64 import linearbooleanwidth as linearbooleanwidth64
from pathwidth import pathwidth

def preprocess(graph):
    # Remove pendants with parent of degree > 2
    change = True
    while change:
        change = False
        for v in graph:
            if len(graph(v)) == 1 and len(graph(graph(v))) > 2:
                #print('Removing ' + str(v))
                graph.remove(v)
                change = True

    # Contract chains with length > 2
    for v in graph:
        if len(graph(v)) == 2:
            w1, w2 = graph(v)
            if graph(w1) - v and graph(w2) - v:
                #print('Contracting ' + str(v))
                graph.contract(v)

    # Remove reduced leaves if parent has degree > 3
    for v in graph:
        if len(graph(v)) == 1 and len(graph(graph(v))) == 2:
            parent = graph(graph(v)) - v
            if len(graph(parent)) > 3:
                #print('Removing ' + str(graph(v)))
                graph.remove(graph(v))
                #print('Removing ' + str(v))
                graph.remove(v)

while 1:
    graph = Tree.generate_random(25)
    graph.verify_symmetry()
    preprocess(graph)
    graph.verify_symmetry()

    pw = pathwidth(graph)[0] + 1
    lbw = linearbooleanwidth64(to64(graph))
    print('With size {}, {} == {}: {}'.format(len(graph), pw, lbw, pw == lbw))
    if lbw != pw and lbw - pw != 1:
        M = Matrix(graph.adjacency_matrix())
        plot(Graph(M)).show()
        input("Press Enter to continue...")


#graph = Graph.load('input/R.dgf')

#def run(graph):
    #return linearbooleanwidth(graph)
#def crun(graph):
    #return linearbooleanwidth64(graph)

#print(run(graph))
#print(crun(to64(graph)))
#cProfile.run('run(graph)')
#cProfile.run('print(crun(to64(graph)))')
#run(graph)

