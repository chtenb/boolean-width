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
                         for B in A.subsets(1, 1))

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
    print('Computing decomposition')
    return (bwtable[graph.vertices],
            booldim,
            list(linearbooleanwidth_decomposition(bwtable, booldim, graph.vertices)))

#
# Trees
#


def preprocess(graph):
    # Remove all pendant with parent of degree > 2
    change = True
    while change:
        change = False
        for v in graph:
            if len(graph(v)) == 1 and len(graph(graph(v))) > 2:
                print('Removing ' + str(v))
                graph.remove(v)
                change = True


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


def linearbooleanwidth_trees(graph):

    def depthfirst(graph, node, parent):
        children = graph(node) - parent
        if not children:
            return 2
        if len(children) == 1:
            return depthfirst(graph, children, node)
        return max(
            max(depthfirst(graph, child, node) for child in children),
            2 * secondmax(depthfirst(graph, child, node) for child in children)
        )

    return min(depthfirst(graph, root, BitSet()) for root in graph)


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
