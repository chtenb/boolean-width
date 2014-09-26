from PIL import Image, ImageDraw
from random import randint
import sys

def plot_graph(graph):
    im = Image.new('RGB', (512, 512), 'white')
    draw = ImageDraw.Draw(im)

    for v in graph.vertices:
        coords = (randint(0, 512), randint(0, 512))
        draw.point(coords)

    #del draw
    im.save('output/test.png', 'png')
