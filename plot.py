from PIL import Image, ImageDraw
import math


def plot_graph(graph):
    """Draw given graph on image and export as png."""
    size = (512, 512)
    margin = 10
    im = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(im)

    radius = min(size) / 2 - margin
    vertexcoords = []
    nr_vertices = graph.count_vertices()
    for i in range(nr_vertices):
        r = i * 2 * math.pi / nr_vertices
        vertexcoords.append((radius * (1 + math.cos(r)) + margin,
                             radius * (1 + math.sin(r)) + margin))

    for v in graph.vertices:
        i = v.identifier
        coords = vertexcoords[i]
        uppercoords = (coords[0] - 5, coords[1] - 5)
        lowercoords = (coords[0] + 5, coords[1] + 5)
        box = [uppercoords, lowercoords]
        draw.ellipse(box, fill=128)

        for w in v.neighbours:
            j = w.identifier
            draw.line([vertexcoords[i], vertexcoords[j]], fill=128)

    im.save('output/test.png', 'png')


def plot_bipartite_graph(graph):
    """Draw given graph on image and export as png."""
    size = (512, 512)
    margin = 30
    im = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(im)

    xcoord_group1 = margin
    xcoord_group2 = size[0] - margin

    vertexcoords1 = []
    vertexcoords2 = []
    size_group1 = len(graph.group1)
    size_group2 = len(graph.group2)
    for i in range(size_group1):
        ycoord = i * (size[1] - 2 * margin) / (size_group1 - 1) + margin
        vertexcoords1.append((xcoord_group1, ycoord))
    for i in range(size_group2):
        ycoord = i * (size[1] - 2 * margin) / (size_group2 - 1) + margin
        vertexcoords2.append((xcoord_group2, ycoord))

    for v in graph.group1:
        i = v.identifier
        coords = vertexcoords1[i]
        uppercoords = (coords[0] - 5, coords[1] - 5)
        lowercoords = (coords[0] + 5, coords[1] + 5)
        box = [uppercoords, lowercoords]
        draw.ellipse(box, fill=128)

    for v in graph.group2:
        i = v.identifier
        coords = vertexcoords2[i - size_group1]
        uppercoords = (coords[0] - 5, coords[1] - 5)
        lowercoords = (coords[0] + 5, coords[1] + 5)
        box = [uppercoords, lowercoords]
        draw.ellipse(box, fill=128)

    for e in graph.edges:
        i = e.v.identifier
        j = e.w.identifier
        draw.line([vertexcoords1[i], vertexcoords2[j - size_group1]], fill=128)

    im.save('output/test.png', 'png')
