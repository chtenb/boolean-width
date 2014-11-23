from random import sample
from bitset64 import iterate
#from libcpp.unordered_map cimport unordered_map
#from libcpp.vector cimport vector

cpdef to64(graph):
    N = {}
    for key in graph.vertices:
        N[<long>key] = <long>graph.neighborhoods[key]

    V = <long>graph.vertices
    return Graph(V, N)


class Graph:

    def __init__(self, long V=0L, N=None):
        self.V = V
        self.N = N or {}

    #def edges(self):
        #"""Iterate over each pair of connected vertices exactly once."""
        #for v in self:
            #for w in self(v):
                #if w < v:
                    #yield v | w

    #def add(self, v):
        #"""Add new vertices to the graph."""
        #assert self.V & v == 0L
        #self.V |= v
        #self.N[v] = 0L

    #def remove(self, v):
        #"""Remove vertices from the graph."""
        #assert self.V & v == v
        #self.V -= v
        #self.N[v] = 0L

    #def connect(self, v, w):
        #"""Connect two vertices."""
        #if not v in self:
            #raise ValueError
        #if not w in self:
            #raise ValueError

        #if w == v:
            #raise ValueError('{} and {} are the same vertex.'.format(v, w))

        #if w in self(v):
            #raise ValueError('{} and {} already connected.'.format(v, w))

        ## Only support undirected edges
        #assert not v in self(w)

        #self.neighborhoods[v] |= w
        #self.neighborhoods[w] |= v

    #def disconnect(self, v, w):
        #"""Disconnect two vertices."""
        #if not v in self:
            #raise ValueError
        #if not w in self:
            #raise ValueError

        #if w == v:
            #raise ValueError('{} and {} are the same vertex.'.format(v, w))

        #if not w in self(v):
            #raise ValueError('{} and {} are not connected.'.format(v, w))

        ## Only support undirected edges
        #assert v in self(w)

        #self.neighborhoods[v] -= w
        #self.neighborhoods[w] -= v

    #def contract(self, v):
        #"""Contract a vertex."""
        #if not v in self:
            #raise ValueError

        #neighbors = self(v)
        #self.remove(v)

        #for w1 in neighbors:
            #for w2 in neighbors:
                #if w1 < w2:
                    #self.connect(w1, w2)

    #def complement(self):
        #"""Construct a graph representing the complement of self."""
        #setlength = len(self.vertices)
        #neighborhoods = {v: self[v].invert(setlength) for v in self}
        #return Graph(self.vertices, neighborhoods)

    #def subgraph(self, vertices):
        #"""Return a graph which is the subgraph of self induced by given vertex subset."""
        #neighborhoods = {v: self(v) & vertices for v in self}
        #return Graph(self.vertices, neighborhoods)

    #def save(self, filename):
        #with open(filename, 'w') as f:
            #f.write('p edges {} {}\n'.format(len(self.vertices), len(list(self.edges))))
            #f.writelines(
                #'n {}\n'.format(v.identifier) for v in self
            #)
            #f.writelines(
                #'e {} {}\n'.format(v.identifier, w. identifier) for v, w in self.edges
            #)

    #@staticmethod
    #def load(filename):
        #graph = Graph()
        #with open(filename, 'r') as f:
            #while 1:
                #line = f.readline()
                #print('Parsing `{}`'.format(line[:-1]))
                #if line == '':
                    #break
                #if line == '\n':
                    #continue

                #if line[0] == 'n':
                    #v = BitSet.from_identifier(int(line[1:]))
                    #graph.add(v)
                #elif line[0] == 'e':
                    #edge = line[1:].split()
                    #v, w = BitSet.from_identifier(int(edge[0]), int(edge[1]))
                    #if v not in graph:
                        #graph.add(v)
                    #if w not in graph:
                        #graph.add(w)
                    #graph.connect(v, w)
        #return graph

    #@staticmethod
    #def generate_random(nr_vertices, nr_edges):
        #if not nr_edges <= nr_vertices * (nr_vertices - 1) / 2:
            #raise ValueError

        #graph = Graph()
        #graph.add(BitSet.from_identifier(*range(nr_vertices)))

        #vertex_list = list(graph.vertices)
        #for _ in range(nr_edges):
            #while 1:
                #v, w = sample(vertex_list, 2)
                ## Don't connect vertices twice
                #if not w in graph[v]:
                    #break
            #graph.connect(v, w)

        #return graph
