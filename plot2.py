from graphviz import Graph

def plot_graph(graph, engine='dot'):
    g = Graph(format='png', engine=engine)
    for v in graph:
        g.node(str(v))

    for v, w in graph.edges:
        g.edge(str(v), str(w))

    g.render('output/test')
