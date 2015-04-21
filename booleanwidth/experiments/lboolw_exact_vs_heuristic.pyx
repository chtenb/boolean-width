from ..graph import Graph
from ..graph128 import to128
from ..lboolw import compute_lboolw
from ..lboolc import compute_lboolc

from numpy import arange, mean
import matplotlib.pyplot as plt

import math
import shutil
import os
import glob
import pickle
import time

graphsize = 20
p_values = [round(p, 5) for p in arange(0.05, 1, 0.05)]
samples = 20
directory = 'output/lboolw-exact-vs-heuristic/'
total_nr = samples * len(p_values)

def run():
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
            graph.save('{}{}-{}.dgf'.format(outputdir, p, i))
            i += 1

    print('{} graphs generated in directory {}'.format(i, outputdir))


def compute_data(input_dir):
    start_time = time.time()
    #data = [{},{},{}]
    data = [{}]
    done = 0

    for filename in glob.iglob(input_dir + '*.dgf'):
        p = float(filename.split('/')[-1].split('-')[0])
        print(p)
        graph = Graph.load(filename)
        graph128 = to128(graph)
        lboolw_table, _ = compute_lboolw(graph128)
        lboolw = math.log(lboolw_table[graph128.vertices], 2)

        #lboolc_table, _ = compute_lboolc(graph128)
        #lboolc = lboolc_table[graph128.vertices]

        if p not in data[0]:
            data[0][p] = []
            #data[1][p] = []
            #data[2][p] = []

        data[0][p].append(lboolw)
        #data[1][p].append(lboolc)
        #data[2][p].append(lboolc/graphsize)

        done += 1
        print('{}/{}'.format(done, total_nr))
        print('--- {} seconds ---'.format(time.time() - start_time))

        if done > 10:
            break

    avg_data = []
    for i in range(len(data)):
        avg_data.append([])
        for p, values in data[i].items():
            avg_data[i].append((p, mean(values)))

    with open(input_dir + 'lboolwvalues', 'w') as f:
        for p, value in avg_data[0]:
            f.write('{}:{}\n'.format(p, value))

    #pickle.dump(avg_data, open(input_dir + 'data', 'wb'))


def plot_data(input_dir):
    #data = pickle.load(open(input_dir + 'data', 'rb'))
    filenames = ['heuristicvalues', 'lboolwvalues']
    data = []
    for i, filename in enumerate(filenames):
        data.append([])
        with open(input_dir + filename, 'r') as f:
            for line in f:
                p, value = [float(s) for s in line.split(':')]
                data[i].append((p, value))

    plt.subplot(121)
    #styles = ['ro', 'g^', 'bs', 'cD', 'mh', 'k+']
    styles = ['g^', 'bs', 'cD', 'mh', 'k+']
    labels = ['heuristic lboolw', 'lboolw', 'lboolc', 'lboolc / n']
    for i in range(len(data)):
        plt.plot([p[0] for p in data[i]], [p[1] for p in data[i]], styles[i], label=labels[i])

    plt.axis([-.05, 1, -1, 10])
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., numpoints=1)
    plt.title('Parameters on random graphs of size n = ' + str(graphsize))
    plt.xlabel('Edge probability')
    plt.ylabel('Average parameter value')
    plt.grid(True)
    plt.show()

