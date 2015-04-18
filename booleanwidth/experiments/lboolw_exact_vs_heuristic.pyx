from ..graph import Graph
from ..graph128 import to128
from ..lboolw import compute_lboolw

from numpy import arange, mean
import matplotlib.pyplot as plt

import shutil
import os
import glob
import pickle


def run():
    graphsize = 10
    p_values = [round(p, 5) for p in arange(0.05, 1, 0.05)]
    samples = 20
    directory = 'output/lboolw-exact-vs-heuristic/'

    #generate_random_graphs(graphsize, p_values, samples, directory)
    #compute_data(directory)
    plot_data(directory)


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

    avg_data = []
    for p, lboolw_values in data.items():
        avg_data.append((p, mean(lboolw_values)))

    pickle.dump(avg_data, open(input_dir + 'data', 'wb'))


def plot_data(input_dir):
    data = pickle.load(open(input_dir + 'data', 'rb'))

    plt.subplot(121)
    #styles = ['ro', 'g^', 'bs', 'cD', 'mh', 'k+']
    plt.plot([p[0] for p in data], [p[1] for p in data], 'ro', label='lboolw')

    plt.axis([-.05, 1, -1, 50])
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., numpoints=1)
    plt.title('Title')
    plt.xlabel('Edge probability')
    plt.ylabel('Average linear boolean width')
    plt.grid(True)
    plt.show()

