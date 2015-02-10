from bitset64 import iterate, subsets, size, invert, tostring
from dynamicprogramming import booldimtable, booldim


def linearboolwidthtable(graph):
    """
    bwtable[A] contains the booleanwidth of the subtree of all cuts inside A.
    The cut which produced A itself is thus not included.
    """
    booldim = booldimtable(graph)

    cdef long v, A, B

    # Init table
    bwtable = {}
    for v in iterate(graph.V):
        if graph.N[v] == 0L:
            bwtable[v] = 1
        else:
            bwtable[v] = 2

    # Solve recurrence
    for A in subsets(graph.V, 2):
        bwtable[A] = min(max(booldim[B], booldim[A - B],
                             bwtable[B], bwtable[A - B])
                         for B in iterate(A))

    return bwtable, booldim


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


def linearbooleanwidth(graph):
    bwtable, booldim = linearboolwidthtable(graph)
    return (bwtable[graph.V],
            booldim,
            list(linear_decomposition(bwtable, booldim, graph.V)))


def dp_greedy_lbw(bwtable, booldim, long A, int universe):
    """A is unprocessed."""
    bound = bwtable[A]
    if size(A) > 1:
        print('trying greedy')
        # Try greedy step
        for B in iterate(A):
            if size(A) == universe:
                greedybound = 1
            else:
                greedybound = booldim[A]

            print('Current booldim', greedybound)
            print(tostring(B), booldim[A - B])
            if booldim[A - B] < greedybound:
                print('choosing {} greedy'.format(tostring(B)))
                yield (B, A - B)
                yield from dp_greedy_lbw(bwtable, booldim, B, universe)
                yield from dp_greedy_lbw(bwtable, booldim, A - B, universe)
                return
        print('No greedy step found, trying nongreedy')
        # Perform normal reconstruction
        for B in iterate(A):
            if (bwtable[B] <= bound and booldim[B] <= bound
                    and booldim[A - B] <= bound and bwtable[A - B] <= bound):
                print('choosing {} nongreedy'.format(tostring(B)))
                yield (B, A - B)
                yield from dp_greedy_lbw(bwtable, booldim, B, universe)
                yield from dp_greedy_lbw(bwtable, booldim, A - B, universe)
                return


def greedy_lbw(graph, depth=1):
    """Assumption: no islets"""
    todo = graph.V
    width = 0
    decomposition = []
    while size(todo) > 1:
        _, x = min((min(booldim(graph, todo - v), greedy_lookahead(graph, todo - v, depth - 1)), v) for v in iterate(todo))
        bd = booldim(graph, todo - x)
        decomposition.append((bd, (x, todo - x)))
        width = max(bd, width)
        todo -= x

    return width, decomposition


def greedy_lookahead(graph, todo, depth):
    if size(todo) < 2 or depth < 1:
        return 0

    return min(min(booldim(graph, todo - v), greedy_lookahead(graph, todo - v, depth - 1))
                   for v in iterate(todo))


def relative_neighborhood_lbw(graph, depth=1):
    """Assumption: no islets"""
    todo = graph.V
    width = 0
    decomposition = []
    while size(todo) > 1:
        # Compute neighbor hood of Left
        N_left = 0L
        for v in iterate(graph.V - todo):
            N_left |= graph.N[v]

        # Pick x with best ratio
        _, x = min((min(neighborhood_ratio(graph, N_left, v),
                    relative_neighborhood_lookahead(graph, todo - v, depth - 1)), v)
                    for v in iterate(todo))
        bd = booldim(graph, todo - x)
        decomposition.append((bd, (x, todo - x)))
        width = max(bd, width)
        todo -= x

    return width, decomposition


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

    return min(min(neighborhood_ratio(graph, N_left, v), relative_neighborhood_lookahead(graph, todo - v, depth - 1)) for v in iterate(todo))
