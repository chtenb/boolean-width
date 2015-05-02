from .bitset128 import (iterate, subsets, size, invert, tostring, subtract, subsets_of_size,
                        subsets_by_size)
from .dynamicprogramming import booldimtable, compute_booldim
from .lboolw import compute_next_un


# New fast exact algos

# NOTE: lbc(X) does not take booldim(X) into account

def compute_lboolc_with_upperbound(G, k):
    print('Upperbound: {}'.format(k))
    V = G.vertices

    lboolc = {}
    lboolc[0L] = 0

    booldim = {}
    un = {}
    #for v in iterate(G.vertices):
        #if G.neighborhoods[v]:
            #un[v] = {G.neighborhoods[v], 0L}
            #booldim[v] = 2
        #else:
            #un[v] = {0L}
            #booldim[v] = 1
    booldim[0L] = 1 # NOTE THIS!!!!
    un[0L] = {0L}
    booldim[G.vertices] = 0
    un[G.vertices] = {0L}


    ss = subsets_by_size(V)
    for i in range(1, size(V) + 1):
        #for X in subsets(V, i, i): # Improve filtering
        #for X in subsets_of_size(V, i):
        for X in ss[i]:
            for v in iterate(X):
                X_v = subtract(X, v)
                if X_v in lboolc and lboolc[X_v] <= k:
                    if X not in booldim:
                        un[X] = compute_next_un(G, un, X, v)
                        booldim[X] = len(un[X])

                    # What if X == v?
                    #new_lboolc = booldim[X] + booldim[v] + lboolc[X_v]
                    #new_lboolc = booldim[v] + booldim[X_v] + lboolc[X_v]
                    new_lboolc = booldim[X_v] + lboolc[X_v]
                    if X not in lboolc:
                        lboolc[X] = new_lboolc
                    else:
                        lboolc[X] = min(lboolc[X], new_lboolc)

    if V in lboolc:
        return lboolc, booldim
    else:
        return False


def compute_lboolc(G):
    k = 1
    while 1:
        result = compute_lboolc_with_upperbound(G, k)
        if result == False:
            k *= 2
        else:
            return result


def construct_lboolc_decomposition(lboolc, booldim, subset, bound=None):
    if bound == None:
        bound = lboolc[subset]

    #print('bound: {}'.format(bound))
    #print(booldim[subset])
    for v in iterate(subset):
        #print(lboolc[v])
        #print(lboolc[subtract(subset, v)])
        #if booldim[v] + lboolc[subtract(subset, v)] + booldim[subset] <= bound:
        if lboolc[subtract(subset, v)] + booldim[subtract(subset, v)] <= bound:
            #yield booldim[subset - v], (v, subset - v)
            yield v
            yield from construct_lboolc_decomposition(lboolc, booldim, subset - v,
                    bound - booldim[subtract(subset, v)])
            break


def print_un(un):
    print('{{{}}}'.format(', '.join(tostring(s) for s in un)))









#
# Old algos
#

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
                yield booldim[A - v], (v, A - v)
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


from lboolw import neighborhood_ratio

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

