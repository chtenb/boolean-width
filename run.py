# Enable importing Cython modules
import pyximport
pyximport.install()

import cProfile
#from tree import Tree
from graph import Graph

import mis
import mis64

from graph64 import to64
from bitset64 import subsets, tostring

from booleanwidth import booleandim
from booleanwidth64 import booleandim as booleandim64

from bitset import BitSet

#x = BitSet(15)
#for s in x.subsets(0, -3):
    #print('{}, {}'.format(s, len(s)))
#print(len(x.subsets()))
#exit()
graph = Graph.generate_random(10, 10)
#graph = Graph.load('input/R.dgf')
def run(graph):
    return booleandim(graph)
G = to64(graph)
def crun(graph):
    return booleandim64(G)

print(run(graph) == crun(graph))
#cProfile.run('run(graph)')
#cProfile.run('crun(graph)')
#run(graph)



#from mytest import run, runcint

#print('Run python')
#cProfile.run('run()')

#print('Run cython int')
#cProfile.run('runcint()')
