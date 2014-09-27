from PIL import ImageDraw
import math


def draw_vertex(draw, vertex, coords, color=128):
    """Draw a single vertex."""
    uppercoords = (coords[0] - 5, coords[1] - 5)
    lowercoords = (coords[0] + 5, coords[1] + 5)
    box = [uppercoords, lowercoords]
    draw.ellipse(box, fill=128)
    draw.text(lowercoords, str(vertex.identifier), fill=color)


def plot_graph(im, graph, color=128):
    """Draw given graph on given draw object."""
    size = im.size
    margin = 10
    draw = ImageDraw.Draw(im)

    radius = min(size) / 2 - margin
    vertexcoords = {}
    nr_vertices = graph.count_vertices()
    for i, v in enumerate(graph.vertices):
        r = i * 2 * math.pi / nr_vertices
        vertexcoords[v.identifier] = (radius * (1 + math.cos(r)) + margin,
                                      radius * (1 + math.sin(r)) + margin)

    for v in graph.vertices:
        coords = vertexcoords[v.identifier]
        draw_vertex(draw, v, coords)

        for w in v.neighbours:
            draw.line([vertexcoords[v.identifier], vertexcoords[w.identifier]],
                      fill=color)


def plot_bipartite_graph(im, graph, color=128):
    """Draw given graph on given draw object."""
    size = im.size
    margin = 30
    draw = ImageDraw.Draw(im)

    xcoord_group1 = margin
    xcoord_group2 = size[0] - margin

    vertexcoords1 = {}
    size_group1 = len(graph.group1)
    for i, v in enumerate(graph.group1):
        ycoord = i * (size[1] - 2 * margin) / (size_group1 - 1) + margin
        vertexcoords1[v.identifier] = (xcoord_group1, ycoord)

    vertexcoords2 = {}
    size_group2 = len(graph.group2)
    for i, v in enumerate(graph.group2):
        ycoord = i * (size[1] - 2 * margin) / (size_group2 - 1) + margin
        vertexcoords2[v.identifier] = (xcoord_group2, ycoord)

    for v in graph.group1:
        coords = vertexcoords1[v.identifier]
        draw_vertex(draw, v, coords, color)

    for v in graph.group2:
        coords = vertexcoords2[v.identifier]
        draw_vertex(draw, v, coords, color)

    for e in graph.edges:
        i = e.v.identifier
        j = e.w.identifier
        draw.line([vertexcoords1[i], vertexcoords2[j]], fill=color)
