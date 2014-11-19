# Enable importing Cython modules
import pyximport
pyximport.install()

import cProfile
#from tree import Tree
from graph import Graph

import mis
import mis64

from graph64 import to64
#exit()

#graph = Tree.generate_random_binary(60)
graph = Graph.load('input/R.dgf')
def run(graph):
    print(mis.mis_count(graph))
G = to64(graph)
def crun(graph):
    print(mis64.mis_count(G.N, G.V))
#cProfile.run('run(graph)')
cProfile.run('crun(graph)')
#run(graph)



#from mytest import run, runcint

#print('Run python')
#cProfile.run('run()')

#print('Run cython int')
#cProfile.run('runcint()')
