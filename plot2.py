from graphviz import Graph

def plot_graph(graph, engine='dot'):
    g = Graph(format='png', engine=engine)
    for v in graph.vertices:
        g.node(str(v))
        for w in v.neighbors:
            w = graph[w]
            # Add an edge exactly 1 time
            if w.identifier < v.identifier:
                g.edge(str(v), str(w))

    g.render('output/test')
