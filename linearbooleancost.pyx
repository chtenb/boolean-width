from bitset128 import iterate, subsets, size, invert, tostring
from dynamicprogramming import booldimtable, compute_booldim


def linearboolcosttable(graph):
    """
    bctable[A] contains the booleancost of the subgraph induced by A
    """
    booldim = booldimtable(graph)

    cdef long v, A, B

    # Init table
    bctable = {}
    for v in iterate(graph.vertices):
        if graph.neighborhoods[v] == 0L:
            bctable[v] = 1
        else:
            bctable[v] = 2

    # Solve recurrence
    for A in subsets(graph.vertices, 2):
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
    return (bctable[graph.vertices],
            list(linear_decomposition(bctable, booldim, graph.vertices)))


def greedy_lbc(graph, depth=1):
    """Assumption: no islets"""
    todo = graph.vertices
    cost = 0
    decomposition = []
    while size(todo) > 1:
        _, x = min((compute_booldim(graph, todo - v) + greedy_lookahead(graph, todo - v, depth - 1), v) for v in iterate(todo))
        bd = compute_booldim(graph, todo - x)
        decomposition.append((bd, (x, todo - x)))
        cost += bd + 2
        todo -= x

    return cost, decomposition


def greedy_lookahead(graph, todo, depth):
    if size(todo) < 2 or depth < 1:
        return 0

    return min(compute_booldim(graph, todo - v) + greedy_lookahead(graph, todo - v, depth - 1) for v in iterate(todo))


from linearbooleanwidth import neighborhood_ratio

def relative_neighborhood_lbc(graph, depth=1):
    """Assumption: no islets"""
    todo = graph.vertices
    cost = 0
    decomposition = []
    while size(todo) > 1:
        # Compute neighbor hood of Left
        N_left = 0L
        for v in iterate(graph.vertices - todo):
            N_left |= graph.neighborhoods[v]

        # Pick x with best ratio
        _, x = min((neighborhood_ratio(graph, N_left, v)
                    + relative_neighborhood_lookahead(graph, todo - v, depth - 1), v)
                    for v in iterate(todo))
        bd = compute_booldim(graph, todo - x)
        decomposition.append((bd, (x, todo - x)))
        cost += bd + 2
        todo -= x

    return cost, decomposition


def relative_neighborhood_lookahead(graph, todo, depth):
    if size(todo) < 2 or depth < 1:
        return 0

    # Compute neighbor hood of Left
    N_left = 0L
    for v in iterate(graph.vertices - todo):
        N_left |= graph.neighborhoods[v]

    return min(neighborhood_ratio(graph, N_left, v) + relative_neighborhood_lookahead(graph, todo - v, depth - 1) for v in iterate(todo))

