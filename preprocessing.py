
#
# Trees
#


def preprocess(graph):
    # Remove pendants with parent of degree > 2
    change = True
    while change:
        change = False
        for v in graph:
            if len(graph(v)) == 1 and len(graph(graph(v))) > 2:
                print('Removing ' + str(v))
                graph.remove(v)
                change = True

    # Contract chains with length > 2
    for v in graph:
        if len(graph(v)) == 2:
            w1, w2 = graph(v)
            if graph(w1) - v and graph(w2) - v:
                print('Contracting ' + str(v))
                graph.contract(v)

    # Remove reduced leaves if parent has degree > 3
    for v in graph:
        if len(graph(v)) == 1 and len(graph(graph(v))) == 2:
            parent = graph(graph(v)) - v
            if len(graph(parent)) > 3:
                print('Removing ' + str(graph(v)))
                graph.remove(graph(v))
                print('Removing ' + str(v))
                graph.remove(v)


def secondmax(iterable):
    largest = -float('inf')
    secondlargest = -float('inf')
    for i in iterable:
        if i > largest:
            secondlargest = largest
            largest = i
        elif i > secondlargest:
            secondlargest = i

    if secondlargest == -float('inf'):
        raise ValueError('Iterable must have length > 1')

    return secondlargest

