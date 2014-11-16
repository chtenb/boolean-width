# Enable importing Cython modules
import pyximport
pyximport.install()

import cProfile
from tree import Tree

import mis
import mis64

from bitset64 import to64

graph = Tree.generate_random_binary(40)
def run(graph):
    print(mis.mis_count(graph))
def crun(graph):
    print(mis64.mis_count(to64(graph), graph.vertices))
cProfile.run('run(graph)')
cProfile.run('crun(graph)')
#run(graph)



#from mytest import run, runcint

#print('Run python')
#cProfile.run('run()')

#print('Run cython int')
#cProfile.run('runcint()')
