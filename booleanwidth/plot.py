from PIL import Image, ImageDraw, ImageFont
import math
from .bitset import BitSet

from graphviz import Graph


def plot(graph, engine='dot', filename='output/test'):
    """Possible engines: dot, neato, fdp, sfdp, twopi, circo"""
    g = Graph(format='png', engine=engine)
    for v in graph:
        g.node(str(v))

    for v, w in graph.edges:
        g.edge(str(v), str(w))

    g.render(filename)


def plot_circle(graph, im=None, color=128):
    """Draw given graph on given draw object."""
    if im == None:
        size = (512, 512)
        im = Image.new('RGB', size, 'white')
    else:
        size = im.size

    margin = 30
    draw = ImageDraw.Draw(im)

    radius = min(size) / 2 - margin
    vertexcoords = {}
    nr_vertices = len(graph.vertices)
    for i, v in enumerate(sorted(graph.vertices, key=lambda v: v.identifier)):
        r = i * 2 * math.pi / nr_vertices
        vertexcoords[BitSet(v)] = (radius * (1 + math.cos(r)) + margin,
                                   radius * (1 + math.sin(r)) + margin)

    for b, v in graph.vertices.items():
        coords = vertexcoords[b]
        draw_vertex(draw, graph.vertices[b], coords, color)

        for w in v.neighbors:
            draw.line([vertexcoords[b], vertexcoords[w]],
                      fill=color, width=1)

    return im


def plot_bipartite(graph, im=None, color=128):
    """Draw given graph on given draw object."""
    if im == None:
        size = (512, 512)
        im = Image.new('RGB', size, 'white')
    else:
        size = im.size

    margin = 30
    draw = ImageDraw.Draw(im)

    # For each vertex we assign a vertical interval
    # The vertex is drawn in the center of that interval
    xcoord = margin
    vertexcoords1 = {}
    interval_length = size[1] / len(graph.group1)
    for i, v in enumerate(graph.group1):
        ycoord = i * interval_length + interval_length / 2
        vertexcoords1[v] = (xcoord, ycoord)

    vertexcoords2 = {}
    xcoord = size[0] - margin
    interval_length = size[1] / len(graph.group2)
    for i, v in enumerate(graph.group2):
        ycoord = i * interval_length + interval_length / 2
        vertexcoords2[v] = (xcoord, ycoord)

    for v in graph.group1:
        coords = vertexcoords1[v]
        draw_vertex(draw, v, coords, color)

    for v in graph.group2:
        coords = vertexcoords2[v]
        draw_vertex(draw, v, coords, color)

    for v in graph.group1:
        for w in graph(v):
            try:
                draw.line([vertexcoords1[v], vertexcoords2[w]], fill=color)
            except KeyError:
                draw.line([vertexcoords1[w], vertexcoords2[v]], fill=color)

    return im


def draw_vertex(draw, vertex, coords, color=128):
    """Draw a single vertex."""
    radius = 5
    uppercoords = (coords[0] - radius, coords[1] - radius)
    lowercoords = (coords[0] + radius, coords[1] + radius)
    box = [uppercoords, lowercoords]
    draw.ellipse(box, fill=color)

    font = ImageFont.truetype("resources/FreeMono.ttf", 30)
    draw.text(lowercoords, str(vertex.identifier), fill=color, font=font)
