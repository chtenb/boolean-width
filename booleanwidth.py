from mis import bron_kerbosch_mis
from utils import powerlist

def booleanwidth(graph):
    booldim = {}

    # Precompute all values of booldim
    for subset in powerlist(graph.vertices):
        booldim[subset] = bron_kerbosch_mis(graph.subgraph(subset))

