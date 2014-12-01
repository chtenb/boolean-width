from itertools import chain, combinations


def powerset(iterable, minsize=0, maxsize=-1):
    """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    s = list(iterable)
    if minsize < 0:
        minsize = len(s) + 1 + minsize
    if maxsize < 0:
        maxsize = len(s) + 1 + maxsize
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def union(collection):
    U = set()
    for X in collection:
        U.update(X)
    return U


def union_closure(collection):
    return {union(S) for S in powerset(collection)}


def count_union_closure(collection):
    pass


def f(collection, subcollection):
    if is_uniquely_irreducible(collection, subcollection):
        supercollection = uniquely_irreducible_superset(collection, subcollection)
        return len({X for X in collection.difference(supercollection)
                    if X <= union(subcollection)})
    elif is_irreducible(subcollection):
        return len({X for X in collection.difference(subcollection)
                    if X <= union(subcollection)})
    else:
        return 0


def is_irreducible(collection):
    for S in powerset(collection, minsize=1, maxsize=-2):
        if S <= union(collection.difference({S})):
            return False
    return True


def is_uniquely_irreducible(collection, subcollection):
    return collection == uniquely_irreducible_superset(collection, subcollection)


def uniquely_irreducible_superset(collection, subcollection):
    U = union(subcollection)
    result = subcollection

    for candidate in collection:
        if candidate <= U:
            result = result.add({candidate})
    return reduce_uniquely(collection, result)


def reduce(collection, subcollection):
    """Return a set of all possible reductions."""
    result = set()
    candidates = {subcollection}

    # Keep a set of candidates, report them if they can't be reduced further
    while candidates:
        candidate = candidates.pop()
        reduced = False

        # Try to remove a set
        for S in candidate:
            if S <= union(candidate.difference({S})):
                candidates.add(candidate.difference(S))
                reduced = True
        if not reduced:
            result.add(candidate)

    return result


def reduce_uniquely(collection, subcollection):
    """Return a set of all possible reductions."""
    return union(reduce(collection, subcollection))


# TEST
