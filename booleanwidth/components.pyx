from bitset import iterate, contains, subtract, first
#from bitset128 import iterate, contains, subtract, first

def bfs(graph, root):
    """Return vertices of a component of graph in some bfs order, starting with root."""
    done = 0L
    front = root
    while front:
        v = first(front)
        yield v
        done |= v
        front |= graph.neighborhoods[v]
        front = subtract(front, done)

def components(graph):
    """Return a list of the connected components of in the graph."""
    done = 0L
    for v in iterate(graph.vertices):
        if contains(done, v):
            continue
        component = sum(bfs(graph, v))
        yield component
        done |= component

