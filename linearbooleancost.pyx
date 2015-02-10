from bitset64 import iterate, subsets, size, invert, tostring
from dynamicprogramming import booldimtable, booldim


def linearboolcosttable(graph):
    """
    bctable[A] contains the booleancost of the subgraph induced by A
    """
    booldim = booldimtable(graph)

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


def greedy_lbc(graph, depth=1):
    """Assumption: no islets"""
    todo = graph.V
    cost = 0
    decomposition = []
    while size(todo) > 1:
        _, x = min((booldim(graph, todo - v) + greedy_lookahead(graph, todo - v, depth - 1), v) for v in iterate(todo))
        bd = booldim(graph, todo - x)
        decomposition.append((bd, (x, todo - x)))
        cost += bd + 2
        todo -= x

    return cost, decomposition


def greedy_lookahead(graph, todo, depth):
    if size(todo) < 2 or depth < 1:
        return 0

    return min(booldim(graph, todo - v) + greedy_lookahead(graph, todo - v, depth - 1) for v in iterate(todo))


def relative_neighborhood(graph, depth=1):
    """Assumption: no islets"""
    todo = graph.V
    cost = 0
    decomposition = []
    while size(todo) > 1:
        # Compute neighbor hood of Left
        N_left = 0L
        for v in iterate(graph.V - todo):
            N_left |= graph.N[v]

        # Pick x with best ratio
        _, x = min((neighborhood_ratio(graph, N_left, v)
                    + relative_neighborhood_lookahead(graph, todo - v, depth - 1), v)
                    for v in iterate(todo))
        bd = booldim(graph, todo - x)
        decomposition.append((bd, (x, todo - x)))
        cost += bd + 2
        todo -= x

    return cost, decomposition

def neighborhood_ratio(graph, N_left, v):
    internal = graph.N[v] & N_left
    external = graph.N[v] - internal
    try:
        return size(external) / size(internal)
    except ZeroDivisionError:
        #return float('infty')
        return 999999999


def relative_neighborhood_lookahead(graph, todo, depth):
    if size(todo) < 2 or depth < 1:
        return 0

    # Compute neighbor hood of Left
    N_left = 0L
    for v in iterate(graph.V - todo):
        N_left |= graph.N[v]

    return min(neighborhood_ratio(graph, N_left, v) + greedy_lookahead(graph, todo - v, depth - 1) for v in iterate(todo))

