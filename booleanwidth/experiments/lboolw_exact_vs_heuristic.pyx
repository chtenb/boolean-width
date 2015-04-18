from ..graph import Graph
from ..graph128 import to128
from ..lboolw import compute_lboolw

from numpy import arange
import shutil
import os
import glob


def run():
    graphsize = 10
    p_values = [round(p, 5) for p in arange(0.05, 1, 0.05)]
    samples = 2
    directory = 'output/lboolw-exact-vs-heuristic/'

    generate_random_graphs(graphsize, p_values, samples, directory)
    data = compute_data(directory)

    print(data)


def generate_random_graphs(graphsize, p_values, samples, outputdir):
    shutil.rmtree(outputdir)
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    i = 0
    for p in p_values:
        for _ in range(samples):
            graph = Graph.generate_random(graphsize, p)
            graph.save('{}{}|{}.dgf'.format(outputdir, p, i))
            i += 1

    print('{} graphs generated in directory {}'.format(i, outputdir))


def compute_data(input_dir):
    data = {}

    for filename in glob.iglob(input_dir + '*.dgf'):
        p = float(filename.split('/')[-1].split('|')[0])
        graph = Graph.load(filename)
        graph128 = to128(graph)
        print(p)
        lboolw_table, _ = compute_lboolw(graph128)
        lboolw = lboolw_table[graph128.vertices]

        if p not in data:
            data[p] = []

        data[p].append(lboolw)

    return data


def plot_data():
    ...

