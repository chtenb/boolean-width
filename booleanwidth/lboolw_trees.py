from .bitset import BitSet
from .bipartite import Bipartite
from .tree import Tree
from .plot import plot



#def linearbooleanwidth_decomposition_trees(graph):
    #def depthfirst(graph, node, parent, parent_chosen):
        #children = graph(node) - parent

        #if not children:
            ##if 
            #return 2

        #child_results = []
        #for child in graph(node) - parent:
            #child_results.append(depthfirst(graph, child, node))

        #return max(max(child_results), 2 * secondmax(child_results))

        ## Look ahead for leaves of length 2
        #specialcase = 0
        #specialcases = BitSet()
        #for child in children:
            #if len(graph(child)) == 2 and len(graph(graph(child) - node)) == 1:
                #specialcase = 3
                #specialcases |= child

        #a = max(depthfirst(graph, child, node) for child in children - specialcases) if children - specialcases else 0
        #b = 2 * secondmax(depthfirst(graph, child, node) for child in children - specialcases) if len(children - specialcases) > 1 else 0
        #return max(a, b, specialcase)

    #def depthfirst(graph, node, parent):
        #children = graph(node) - parent
        #if not children:
            #return 2
        #if len(children) == 1:
            #return depthfirst(graph, children, node)

        ## Look ahead for leaves of length 2
        #specialcase = 0
        #specialcases = BitSet()
        #for child in children:
            #if len(graph(child)) == 2 and len(graph(graph(child) - node)) == 1:
                #specialcase = 3
                #specialcases |= child

        #a = max(depthfirst(graph, child, node) for child in children - specialcases) if children - specialcases else 0
        #b = 2 * secondmax(depthfirst(graph, child, node) for child in children - specialcases) if len(children - specialcases) > 1 else 0
        #return max(a, b, specialcase)

    #solutions = ((root, depthfirst(graph, root, BitSet(), BitSet())) for root in graph)
    #return min(solutions, key=lambda x: x[1])

