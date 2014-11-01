from booleanwidth import booleandim, subbitsets
from bitset import BitSet

def linearboolwidthtable(graph):
    """
    bwtable[A] contains the booleanwidth of the subtree of all cuts inside A.
    The cut which produced A itself is thus not included.
    """
    booldim = booleandim(graph)
    vertices = BitSet(graph.vertices)

    bwtable = {}
    for b in vertices:
        bwtable[b] = 2

    print('Solving recurrence')

    for A in subbitsets(vertices, 2):
        bwtable[A] = min(max(booldim[B], booldim[A - B],
                             bwtable[B], bwtable[A - B])
                         for B in subbitsets(A, 1, 1))

    return bwtable, booldim


def linearbooleanwidth_decomposition(bwtable, booldim, A, rec=0):
    assert isinstance(A, BitSet)
    bound = bwtable[A]
    if len(A) > 1:
        for B in subbitsets(A, 1, 1):
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
    vbitset = BitSet(graph.vertices)
    print('Computing decomposition')
    return bwtable[vbitset], booldim, list(linearbooleanwidth_decomposition(bwtable, booldim, vbitset))

def compare_linear_balanced():
    while 1:
        graph = Bipartite.generate_random(10, 10)
        bw, booldim, decomposition = booleanwidth(graph)
        lbw, lbooldim, ldecomposition = linearbooleanwidth(graph)

        if bw < lbw - 1:
            print('booleanwidth: ' + str(bw))
            print('decomposition: ' + '\n'.join('({}, {}): {},{}'.format(
                graph[a], graph[b], booldim[a], booldim[b]) for a, b in decomposition))

            print('linear booleanwidth: ' + str(lbw))
            print('linear decomposition: ' + '\n'.join('({}, {}): {},{}'.format(
                graph[a], graph[b], lbooldim[a], lbooldim[b]) for a, b in ldecomposition))

            plot(graph)
            break


def compare_lbw_branches():
    global graph
    for _ in range(1):
        #graph = Tree.generate_random(12, 3)
        graph = Tree.generate_random_binary(12)
        lbw, lbooldim, ldecomposition = linearbooleanwidth(graph)
        print('linear booleanwidth: ' + str(lbw))
        print('depth: ' + str(graph.depth()))
        print('number of branches: ' + str(graph.count_branches()))
        print('number of branching nodes: ' + str(graph.count_branching_nodes()))
        #print('linear decomposition: ' + '\n'.join('({}, {}): {},{}'.format(
            #graph[a], graph[b], lbooldim[a], lbooldim[b]) for a, b in ldecomposition))
