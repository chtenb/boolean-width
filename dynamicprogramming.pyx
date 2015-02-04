from bitset64 import iterate, subsets, tostring, size
from mis64 import mis_count


def cut(long V, N, long vertices):
    """Return the neighborhoods of the cut induced by given vertex subset."""
    complement = V - vertices

    newN = {}

    for v in iterate(vertices):
        newN[v] = N[v] & complement

    for v in iterate(complement):
        newN[v] = N[v] & vertices

    return newN

def booldim_onthefly(graph, subset):
    return mis_count(cut(graph.V, graph.N, subset), graph.V)

def booleandim(graph):
    """Compute booldim function."""
    V = graph.V
    N = graph.N
    booldim = {}
    #for subset in subsets(V, 1, -2):
    for subset in subsets(V):
        if not subset in booldim:
            complement = V - subset
            result = mis_count(cut(V, N, subset), V)
            booldim[subset] = result
            booldim[complement] = result

    # Don't count universal cuts
    booldim[V] = 0L

    # Verify size
    assert len(booldim) == 2 ** size(V)

    # Verify symmetry
    #print('Verify booldim symmetry')
    #for subset in subsets(V, 1, -2):
        #complement = V - subset
        #assert booldim[subset] == booldim[complement]

    return booldim

# TODO: this reconstruction doesn't work for cost!!


def print_decomposition(result, decomposition):
    print(result)
    for x, y, bd in decomposition:
        print(tostring(x), tostring(y), bd)


def bw_from_decomposition(booldim, decomposition):
    return max(max(booldim[A], booldim[B]) for A, B in decomposition)


def bc_from_decomposition(booldim, decomposition):
    return sum(booldim[A] + booldim[B] for A, B in decomposition)
