from booleanwidth import booleandim, booleanwidth
from bitset import BitSet
from bipartite import Bipartite
from tree import Tree
from plot import plot


def linearboolwidthtable(graph):
    """
    bwtable[A] contains the booleanwidth of the subtree of all cuts inside A.
    The cut which produced A itself is thus not included.
    """
    booldim = booleandim(graph)

    bwtable = {}
    for v in graph:
        bwtable[v] = 2

    print('Solving recurrence')

    for A in graph.vertices.subsets(2):
        bwtable[A] = min(max(booldim[B], booldim[A - B],
                             bwtable[B], bwtable[A - B])
                         for B in A)

    return bwtable, booldim


def linearbooleanwidth_decomposition(bwtable, booldim, A, rec=0):
    assert isinstance(A, BitSet)
    bound = bwtable[A]
    if len(A) > 1:
        for B in A.subsets(1, 1):
            assert B in A
            if (bwtable[B] <= bound and booldim[B] <= bound
                    and booldim[A - B] <= bound and bwtable[A - B] <= bound):
                #print(bound, bwtable[B], bwtable[A - B])
                yield (B, A - B)
                yield from linearbooleanwidth_decomposition(bwtable, booldim, B)
                yield from linearbooleanwidth_decomposition(bwtable, booldim, A - B)
                # print(B)
                #booleanwidth_decomposition(bwtable, B, rec+1)
                #booleanwidth_decomposition(bwtable, A - B, rec+1)

                break


def linearbooleanwidth(graph):
    bwtable, booldim = linearboolwidthtable(graph)
    return bwtable[graph.vertices]
    #print('Computing decomposition')
    #return (bwtable[graph.vertices],
            #booldim,
            #list(linearbooleanwidth_decomposition(bwtable, booldim, graph.vertices)))


#
# Trees
#


def preprocess(graph):
    # Remove pendants with parent of degree > 2
    change = True
    while change:
        change = False
        for v in graph:
            if len(graph(v)) == 1 and len(graph(graph(v))) > 2:
                print('Removing ' + str(v))
                graph.remove(v)
                change = True

    # Contract chains with length > 2
    for v in graph:
        if len(graph(v)) == 2:
            w1, w2 = graph(v)
            if graph(w1) - v and graph(w2) - v:
                print('Contracting ' + str(v))
                graph.contract(v)

    # Remove reduced leaves if parent has degree > 3
    for v in graph:
        if len(graph(v)) == 1 and len(graph(graph(v))) == 2:
            parent = graph(graph(v)) - v
            if len(graph(parent)) > 3:
                print('Removing ' + str(graph(v)))
                graph.remove(graph(v))
                print('Removing ' + str(v))
                graph.remove(v)


def secondmax(iterable):
    largest = -float('inf')
    secondlargest = -float('inf')
    for i in iterable:
        if i > largest:
            secondlargest = largest
            largest = i
        elif i > secondlargest:
            secondlargest = i

    if secondlargest == -float('inf'):
        raise ValueError('Iterable must have length > 1')

    return secondlargest


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

    solutions = ((root, depthfirst(graph, root, BitSet(), BitSet())) for root in graph)
    return min(solutions, key=lambda x: x[1])


#
# Comparisons
#


def compare_linear_balanced():
    while 1:
        graph = Bipartite.generate_random(6, 6)
        bw, booldim, decomposition = booleanwidth(graph)
        lbw, lbooldim, ldecomposition = linearbooleanwidth(graph)
        print('bw: {}, lbw: {}'.format(bw, lbw))

        if bw != lbw:
            print('booleanwidth: ' + str(bw))
            print('decomposition: ' + '\n'.join('({}, {}): {},{}'.format(
                a, b, booldim[a], booldim[b]) for a, b in decomposition))

            print('linear booleanwidth: ' + str(lbw))
            print('linear decomposition: ' + '\n'.join('({}, {}): {},{}'.format(
                a, b, lbooldim[a], lbooldim[b]) for a, b in ldecomposition))

            plot(graph)
            break


def compare_lbw_branches():
    for _ in range(1):
        #graph = Tree.generate_random(12, 3)
        graph = Tree.generate_random_binary(12)
        lbw, lbooldim, ldecomposition = linearbooleanwidth(graph)
        print('linear booleanwidth: ' + str(lbw))
        print('depth: ' + str(graph.depth()))
        print('number of branches: ' + str(graph.count_branches()))
        print('number of branching nodes: ' + str(graph.count_branching_nodes()))
        # print('linear decomposition: ' + '\n'.join('({}, {}): {},{}'.format(
        # graph[a], graph[b], lbooldim[a], lbooldim[b]) for a, b in ldecomposition))
