"""This module contains algorithms for computing the maximal independent sets."""

def bron_kerbosch(graph):
    def recursion(include, rest, exclude):
        assert include or exclude or rest
        assert include.isdisjoint(rest)
        assert include.isdisjoint(exclude)
        assert rest.isdisjoint(exclude)

        #print('{}, {}, {}'.format(include, rest, exclude))

        if not exclude and not rest:
            yield include

        for v in list(rest):
            assert not v in v.neighbours
            yield from recursion(include.union({v}),
                                 rest.intersection(set(v.neighbours)),
                                 exclude.intersection(set(v.neighbours)))
            rest.difference_update({v})
            exclude.update({v})

    yield from recursion(set(), set(graph.vertices), set())

