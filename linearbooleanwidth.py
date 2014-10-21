from booleanwidth import booleandim, subbitsets
from vertex import BitSet

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
