from ..graph import Graph

import shutil
import os
import math
import glob
import time

import numpy as np
from scipy.interpolate import pchip
import matplotlib.pyplot as plt

from .. import heuristic # HACK

def generate_random_graphs(graphsize, p_values, samples, outputdir):
    # Remove all existing graphs
    shutil.rmtree(outputdir)
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    # Generate new graphs
    i = 0
    for p in p_values:
        for _ in range(samples):
            graph = Graph.generate_random(graphsize, p)
            graph.save('{}{}-{}.dgf'.format(outputdir, p, i))
            i += 1

    print('{} graphs generated in directory {}'.format(i, outputdir))


def compute_data(inputdir, outputdir, name, compute, total_nr):
    start_time = time.time()

    outputfile = name + '_raw_results'

    # Read which graphs are already done
    done = []
    try:
        open(outputdir + outputfile, 'x')
    except FileExistsError:
        pass

    with open(outputdir + outputfile, 'r') as f:
        for line in f:
            graphname = line.split(':')[0]
            done.append(graphname)

    for filename in glob.iglob(inputdir + '*.dgf'):
        graphname = filename.split('/')[-1][:-len('.dgf')]
        if graphname in done:
            print('Skipping graph ' + graphname)
            continue

        print('Processing graph ' + graphname)
        graph = Graph.load(filename)
        value = compute(graph)

        with open(outputdir + outputfile, 'a') as f:
            f.write('{}:{}\n'.format(graphname, value))

        done.append(graphname)
        print('{}/{}'.format(len(done), total_nr))
        print('--- {} seconds ---'.format(time.time() - start_time))


def compute_avg_data(outputdir, experiment_name, avg, total_nr):
    data = {}
    raw_file = experiment_name + '_raw_results'
    result_file = experiment_name + '_results'
    count = 0
    with open(outputdir + raw_file, 'r') as f:
        for line in f:
            graphname, value = line.split(':')
            p = float(graphname.split('-')[0])
            value = float(value)
            if not p in data:
                data[p] = []
            data[p].append(value)
            count += 1

    if count != total_nr:
        print('WARNING: not all graphs have been processed yet for ' + experiment_name)

    avg_data = []
    for p, values in data.items():
        avg_data.append((p, avg(values)))

    with open(outputdir + result_file, 'w') as f:
        for p, value in avg_data:
            f.write('{}:{}\n'.format(p, value))


def plot_data(outputdir, filenames, labels, graphsize, codomain):
    data = []
    for i, filename in enumerate(filenames):
        data.append([])
        with open(outputdir + filename + '_results', 'r') as f:
            for line in f:
                p, value = [float(s) for s in line.split(':')]
                data[i].append((p, value))

    plt.subplot(121)
    colors = ['r', 'g', 'b', 'c', 'm', 'k', 'k', 'k']
    styles = ['ro', 'g^', 'bs', 'cD', 'mh', 'kd', 'k+', 'kx']
    for i in range(len(data)):
        points = sorted(data[i])
        points.insert(0, (0, 0))
        points.append((1, 0))
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        # Create the interpolator
        interp = pchip(x, y)
        # Dense x for the smooth curve
        xx = np.linspace(0, 1.0, 101)
        plt.plot(xx, interp(xx), color=colors[i])
        plt.plot(x, y, styles[i], label=labels[i])

    plt.axis([0, 1, 1, codomain])
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., numpoints=1)
    plt.title('Parameter behaviour on random graphs of size n = ' + str(graphsize))
    plt.xlabel('Edge probability')
    plt.ylabel('Average parameter value')
    plt.grid(True)
    plt.show()

