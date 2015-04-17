from bitset128 import iterate, subsets, tostring, size
from bitset128 cimport uint128
from mis128 import mis_count


def cut(uint128 V, N, uint128 vertices):
    """Return the neighborhoods of the cut induced by given vertex subset."""
    complement = V - vertices

    newN = {}

    for v in iterate(vertices):
        newN[v] = N[v] & complement

    for v in iterate(complement):
        newN[v] = N[v] & vertices

    return newN


def compute_booldim(graph, subset):
    return mis_count(cut(graph.vertices, graph.neighborhoods, subset), graph.vertices)


def booldimtable(graph):
    """Compute booldim function."""
    booldim = {}
    #for subset in subsets(V, 1, -2):
    for subset in subsets(graph.vertices):
        if not subset in booldim:
            complement = graph.vertices - subset
            result = compute_booldim(graph, subset)
            booldim[subset] = result
            booldim[complement] = result

    # Don't count universal cuts
    booldim[graph.vertices] = 0L

    # Verify size
    assert len(booldim) == 2 ** size(graph.vertices)

    # Verify symmetry
    #print('Verify booldim symmetry')
    #for subset in subsets(graph.vertices, 1, -2):
        #complement = graph.vertices - subset
        #assert booldim[subset] == booldim[complement]

    return booldim


def print_decomposition(result, decomposition):
    print(result)
    for bd, (x, y) in decomposition:
        print(tostring(x), tostring(y), bd)


def print_linear_decomposition(result, decomposition):
    print(result)
    for bd, (x, y) in decomposition:
        print(tostring(x), bd)


def bw_from_decomposition(booldim, decomposition):
    return max(max(booldim[A], booldim[B]) for A, B in decomposition)


def bc_from_decomposition(booldim, decomposition):
    return sum(booldim[A] + booldim[B] for A, B in decomposition)

