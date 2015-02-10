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


def booldim(graph, subset):
    return mis_count(cut(graph.V, graph.N, subset), graph.V)


def booldimtable(graph):
    """Compute booldim function."""
    booldim = {}
    #for subset in subsets(V, 1, -2):
    for subset in subsets(graph.V):
        if not subset in booldim:
            complement = graph.V - subset
            result = booldim(graph, subset)
            booldim[subset] = result
            booldim[complement] = result

    # Don't count universal cuts
    booldim[graph.V] = 0L

    # Verify size
    assert len(booldim) == 2 ** size(graph.V)

    # Verify symmetry
    #print('Verify booldim symmetry')
    #for subset in subsets(graph.V, 1, -2):
        #complement = graph.V - subset
        #assert booldim[subset] == booldim[complement]

    return booldim


def print_decomposition(result, decomposition):
    print(result)
    for bd, (x, y) in decomposition:
        print(tostring(x), tostring(y), bd)


def bw_from_decomposition(booldim, decomposition):
    return max(max(booldim[A], booldim[B]) for A, B in decomposition)


def bc_from_decomposition(booldim, decomposition):
    return sum(booldim[A] + booldim[B] for A, B in decomposition)

