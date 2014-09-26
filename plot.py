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
        r = i * 2 * math.pi / (nr_vertices)
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
