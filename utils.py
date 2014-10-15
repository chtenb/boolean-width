import itertools


def powerlist(l):
    result = []
    for k in range(len(l)):
        result.append(itertools.combinations(l, k))

    return itertools.chain.from_iterable(result)

class DictChain:
    def __init__(self, *dicts):
        self.dicts = dicts

    def __getitem__(self, index):
        """Return first occurrance of index."""
        for d in self.dicts:
            try:
                return d[index]
            except KeyError:
                pass

        raise KeyError

    def __delitem__(self, index):
        """Delete all occurrances of index."""
        for d in self.dicts:
            try:
                del d[index]
            except KeyError:
                pass

        raise KeyError

    def __len__(self):
        """Return sum of all lengths."""
        return sum(len(d) for d in self.dicts)

    def keys(self):
        return itertools.chain.from_iterable(d.keys() for d in self.dicts)

    def values(self):
        return itertools.chain.from_iterable(d.values() for d in self.dicts)

    def items(self):
        return itertools.chain.from_iterable(d.items() for d in self.dicts)

d1 = {'ab' : 2}
d2 = {'cd' : 5}
d3 = DictChain(d1, d2)

for i in d3.keys():
    print(i)
for i in d3.values():
    print(i)
for i in d3.items():
    print(i)

