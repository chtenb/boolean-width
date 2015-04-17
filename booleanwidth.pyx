from bitset128 import iterate, subsets, tostring, size
from dynamicprogramming import booldimtable, compute_booldim

def boolwidthtable(graph):
    """
    bwtable[A] contains the booleanwidth of the subtree of all cuts inside A.
    The cut which produced A itself is thus not included.
    """
    booldim = booldimtable(graph)

    # Init table
    bwtable = {}
    for v in iterate(graph.vertices):
        if graph.neighborhoods[v] == 0L:
            bwtable[v] = 1
        else:
            bwtable[v] = 2

    # Solve recurrence
    for A in subsets(graph.vertices, 2):
        try:
            bwtable[A] = min(max(booldim[B],
                booldim[A - B],
                                 bwtable[B],
                                 bwtable[A - B])
                             for B in subsets(A, 1, -2))
        except KeyError:
            for B in subsets(A):#, 1, -1):
                print(tostring(B))
            exit()

    return bwtable, booldim


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


def booleanwidth(graph):
    bwtable, booldim = boolwidthtable(graph)
    return (bwtable[graph.vertices],
            booldim,
            list(decomposition(bwtable, booldim, graph.vertices)))


def bw_from_decomposition(graph, decomposition):
    return max(max(compute_booldim(graph, A), compute_booldim(graph, B)) for A, B in decomposition)


def greedy_bw(graph, depth=1):
    decomposition = list(greedy_bw_helper(graph, graph.vertices, depth))
    width = max(decomposition)[0]
    return width, decomposition


def greedy_bw_helper(graph, subset, depth):
    """Assumption: no islets"""
    if size(subset) == 1:
        return
    #print(size(subset))
    assert size(subset) > 1

    # Find a sequence of candidate cuts
    todo = subset
    candidates = []
    def penalty(A):
        return max(compute_booldim(graph, A), compute_booldim(graph, subset - A))
    while size(todo) > 1:
    #while size(todo) >= int(size(subset) / 3):
        new_candidate = min((penalty(todo - v), todo - v) for v in iterate(todo))
        candidates.append(new_candidate)
        todo = new_candidate[1]

    # Return best candidate
    bestwidth, bestcut = min(candidates)
    yield bestwidth, (bestcut, subset - bestcut)
    yield from greedy_bw_helper(graph, bestcut, depth)
    yield from greedy_bw_helper(graph, subset - bestcut, depth)

