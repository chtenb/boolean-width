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
    bound = table[A]
    if size(A) > 1:
        for B in iterate(A):
            if (table[B] <= bound and booldim[B] <= bound
                    and booldim[A - B] <= bound and table[A - B] <= bound):
                yield (B, A - B)
                yield from linear_decomposition(table, booldim, B) # Obsolete?
                yield from linear_decomposition(table, booldim, A - B)

                break


def print_decomposition(result, booldim, decomposition):
    print(result)
    for x, y in decomposition:
        print(tostring(x), tostring(y), booldim[y])


def bw_from_decomposition(booldim, decomposition):
    return max(booldim[A] for _, A in decomposition)


def bc_from_decomposition(booldim, decomposition):
    return sum(booldim[A] for _, A in decomposition)
