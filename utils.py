import itertools


def powerlist(l):
    result = []
    for k in range(len(l)):
        result.append(itertools.combinations(l, k))

    return itertools.chain.from_iterable(result)

