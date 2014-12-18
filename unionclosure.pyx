from itertools import chain, combinations
from bitset64 import join, tostring, contains


def powerset(iterable, minsize=0, maxsize=-1):
    """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    s = list(iterable)
    if minsize < 0:
        minsize = len(s) + 1 + minsize
    if maxsize < 0:
        maxsize = len(s) + 1 + maxsize
    return list(set(c) for r in range(len(s) + 1) for c in combinations(s, r))


def union(collection):
    result = set()
    for X in collection:
        result.update(X)
    return result


def union_closure(collection):
    return {join(S) for S in powerset(collection)}


def list_union_closure(collection):
    result = []
    for subcollection in powerset(collection):
        result.append(f(collection, subcollection))

    return result


def f(collection, subcollection):
    if is_uniquely_irreducible(collection, subcollection):
        supercollection = uniquely_irreducible_superset(collection, subcollection)
        return {X for X in collection.difference(supercollection)
                if contains(join(subcollection), X)}
    elif is_irreducible(collection, subcollection):
        return {X for X in collection.difference(subcollection)
                if contains(join(subcollection), X)}
    else:
        return {}


def is_irreducible(collection, subcollection):
    return len(reduce(collection, subcollection)) == 1
    # for S in powerset(collection, minsize=1, maxsize=-2):
    # if S <= union(collection.difference({S})):
    # return False
    # return True


def is_uniquely_irreducible(collection, subcollection):
    return subcollection == uniquely_irreducible_superset(collection, subcollection)


def uniquely_irreducible_superset(collection, subcollection):
    U = join(subcollection)
    result = subcollection

    for candidate in collection:
        if contains(U, candidate):
            result = result.union({candidate})

    return reduce_uniquely(collection, result)


def reduce(collection, subcollection):
    """Return a list of all possible reductions."""
    result = []
    candidates = [subcollection]

    # Keep a set of candidates, report them if they can't be reduced further
    while candidates:
        candidate = candidates.pop()
        reduced = False

        # Try to remove a set
        for S in candidate:
            if join(S) == join( # TODO
            complement = candidate.difference({S})
            if contains(join(complement), S) and not complement in candidates:
                candidates.append(complement)
                reduced = True

        # If not possible we found a reduced collection
        if not reduced and not candidate in result:
            result.append(candidate)

    return result


def reduce_uniquely(collection, subcollection):
    """Return a set of all possible reductions."""
    return union(reduce(collection, subcollection))


#
# TESTING
#
def printcollection(collection):
    print('{{{}}}'.format(', '.join(tostring(x) for x in collection)))

A = [3L, 5L, 6L]
print(union_closure(A))
printcollection(A)
printcollection(list_union_closure(A))
