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


def booleandim(graph):
    """Compute booldim function."""
    V = graph.V
    N = graph.N
    booldim = {}
    for subset in subsets(V, 1, -2):
        if not subset in booldim:
            complement = V - subset
            result = mis_count(cut(V, N, subset), V)
            booldim[subset] = result
            booldim[complement] = result

    # Verify size
    assert len(booldim) == 2 ** size(V) - 2

    # Verify symmetry
    #print('Verify booldim symmetry')
    #for subset in subsets(V, 1, -2):
        #complement = V - subset
        #assert booldim[subset] == booldim[complement]

    return booldim


def decomposition(table, booldim, long A):
    """Reconstruct optimal tree decomposition from DP table."""
    bound = table[A]
    if size(A) > 1:
        for B in subsets(A, 1, -2):
            if (table[B] <= bound and booldim[B] <= bound
                    and booldim[A - B] <= bound and table[A - B] <= bound):
                yield (B, A - B)
                yield from decomposition(table, booldim, B)
                yield from decomposition(table, booldim, A - B)

                break


def linear_decomposition(table, booldim, long A):
    """Reconstruct optimal linear decomposition from DP table."""
    bound = table[A]
    if size(A) > 1:
        for v in iterate(A):
            if (table[v] <= bound and booldim[v] <= bound
                    and booldim[A - v] <= bound and table[A - v] <= bound):
                yield (v, A - v)
                yield from linear_decomposition(table, booldim, A - v)

                break


def print_decomposition(result, booldim, decomposition):
    print(result)
    for x, y in decomposition:
        print(tostring(x), tostring(y), booldim[y])


def bw_from_decomposition(booldim, decomposition):
    return max(max(booldim[A], booldim[B]) for A, B in decomposition)


def bc_from_decomposition(booldim, decomposition):
    return sum(booldim[A] + booldim[B] for A, B in decomposition)
