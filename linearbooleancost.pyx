from bitset64 import iterate, subsets, size, invert, tostring
from dynamicprogramming import booleandim, booldim_onthefly


def linearboolcosttable(graph):
    """
    bctable[A] contains the booleancost of the subgraph induced by A
    """
    booldim = booleandim(graph)

    cdef long v, A, B

    # Init table
    bctable = {}
    for v in iterate(graph.V):
        if graph.N[v] == 0L:
            bctable[v] = 1
        else:
            bctable[v] = 2

    # Solve recurrence
    for A in subsets(graph.V, 2):
        bctable[A] = booldim[A] + min(bctable[v] + bctable[A - v] for v in iterate(A))

    return bctable, booldim


def linear_decomposition(table, booldim, long A):
    """Reconstruct optimal linear decomposition from DP table."""
    bound = table[A]
    if size(A) > 1:
        for v in iterate(A):
            if table[v] + table[A - v] + booldim[A] == bound:
                yield (v, A - v, booldim[A - v])
                yield from linear_decomposition(table, booldim, A - v)

                break


def linearbooleancost(graph):
    bctable, booldim = linearboolcosttable(graph)
    return (bctable[graph.V],
            list(linear_decomposition(bctable, booldim, graph.V)))


def greedy_lbc(graph):
    """Assumption: no islets"""
    todo = graph.V
    def booldim(v):
        return booldim_onthefly(graph, v)

    cost = 0
    decomposition = []
    while size(todo) > 1:
        bd, x = min(((booldim(todo - v), v) for v in iterate(todo)))
        decomposition.append((x, todo - x, bd))
        cost += bd + 2
        todo -= x

    return cost, decomposition

