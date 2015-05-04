from libc.stdlib cimport rand, srand
from libc.time cimport time


# Seed the random number generator
srand(time(NULL))


cdef extern from "stdlib.h":
    int RAND_MAX


cdef int randomint(int upperbound):
    """Upperbound is exclusive."""
    return <int> ((rand() / <float>RAND_MAX) * upperbound)


def shuffle(list l):
    """Shuffle list using fisher-yates shuffle."""
    cdef int j

    for i in range(len(l) - 1, -1 ,-1):
        j = randomint(i + 1)
        try:
            l[i], l[j] = l[j], l[i]
        except IndexError:
            print(l, i, j)


def shuffled(l):
    """Shuffle list using fisher-yates shuffle."""
    result = l[:]
    shuffle(result)
    return result



import itertools


def powerlist(l):
    for k in range(len(l)):
        yield from itertools.combinations(l, k)


class DictChain:

    def __init__(self, *dicts):
        self.dicts = dicts

    def __getitem__(self, index):
        """
        Return all occurrances of index.
        Return iterables in a chained manner.
        """
        resultlist = []
        for d in self.dicts:
            try:
                result = d[index]
            except KeyError:
                pass
            else:
                try:
                    resultlist.extend(result)
                except TypeError:
                    resultlist.append(result)

        if not resultlist:
            raise KeyError
        if len(resultlist) == 1:
            return resultlist[0]
        return resultlist

    def __len__(self):
        """Return sum of all lengths."""
        return sum(len(d) for d in self.dicts)

    def __contains__(self, thing):
        """Return True of any dict contains thing."""
        for d in self.dicts:
            if thing in d:
                return True
        return False

    def __iter__(self):
        """Return an iterator over all dicts."""
        for d in self.dicts:
            for x in d:
                yield x

    def keys(self):
        return itertools.chain.from_iterable(d.keys() for d in self.dicts)

    def values(self):
        return itertools.chain.from_iterable(d.values() for d in self.dicts)

    def items(self):
        return itertools.chain.from_iterable(d.items() for d in self.dicts)
