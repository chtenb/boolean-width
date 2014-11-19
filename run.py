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

from linearbooleanwidth import linearbooleanwidth
from linearbooleanwidth64 import linearbooleanwidth as linearbooleanwidth64

from bitset import BitSet

#x = BitSet(15)
#for s in x.subsets(0, -3):
    #print('{}, {}'.format(s, len(s)))
#print(len(x.subsets()))
#exit()
graph = Graph.generate_random(17, 20)
#graph = Graph.load('input/R.dgf')
def run(graph):
    return linearbooleanwidth(graph)
def crun(graph):
    return linearbooleanwidth64(graph)

#print(run(graph))
#print(crun(to64(graph)))
#cProfile.run('run(graph)')
cProfile.run('print(crun(to64(graph)))')
#run(graph)



#from mytest import run, runcint

#print('Run python')
#cProfile.run('run()')

#print('Run cython int')
#cProfile.run('runcint()')
