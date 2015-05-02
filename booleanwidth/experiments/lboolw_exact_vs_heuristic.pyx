from ..graph import Graph
from ..graph128 import to128
from ..lboolw import compute_lboolw
from ..lboolc import compute_lboolc
from ..heuristic import greedy, greedy_cost

from numpy import arange, mean
import matplotlib.pyplot as plt

import math
import shutil
import os
import glob
import time

graphsize = 20
p_values = [round(p, 5) for p in arange(0.05, 1, 0.05)]
samples = 20
directory = 'output/lboolw-exact-vs-heuristic/' # Must end with slash
total_nr = samples * len(p_values)

def run():
    #generate_random_graphs(graphsize, p_values, samples, directory)
    #compute_data(directory)
    #compute_avg_data(directory)
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

    output_file = 'lboolc_raw_results'

    # Read which graphs are already done
    done = []
    try:
        open(input_dir + output_file, 'x')
    except FileExistsError:
        pass

    with open(input_dir + output_file, 'r') as f:
        for line in f:
            graphname = line.split(':')[0]
            done.append(graphname)

    for filename in glob.iglob(input_dir + '*.dgf'):
        graphname = filename.split('/')[-1][:-len('.dgf')]
        if graphname in done:
            print('Skipping graph ' + graphname)
            continue

        print('Processing graph ' + graphname)
        graph = Graph.load(filename)
        graph128 = to128(graph)
        #lboolw_table, _ = compute_lboolw(graph128)
        #lboolw = math.log(lboolw_table[graph128.vertices], 2)

        lboolc = compute_lboolc(graph128)[0][graph128.vertices]
        #lboolc = greedy_cost(graph128)[0]

        with open(input_dir + output_file, 'a') as f:
            f.write('{}:{}\n'.format(graphname, lboolc))

        done.append(graphname)
        print('{}/{}'.format(len(done), total_nr))
        print('--- {} seconds ---'.format(time.time() - start_time))


def compute_avg_data(input_dir):
    data = {}
    results_file = 'lboolc_raw_results'
    with open(input_dir + results_file, 'r') as f:
        for line in f:
            graphname, value = line.split(':')
            p = float(graphname.split('-')[0])
            value = float(value)
            if not p in data:
                data[p] = []
            data[p].append(value)

    print(data)
    avg_data = []
    for p, values in data.items():
        avg_data.append((p, math.log(mean(values)/graphsize, 2)))
        #avg_data.append((p, math.log(mean(values), 2)))

    with open(input_dir + 'lboolc_divn_log_values', 'w') as f:
        for p, value in avg_data:
            f.write('{}:{}\n'.format(p, value))


def plot_data(input_dir):
    filenames = ['heuristicvalues', 'lboolwvalues', 'lboolc_divn_log_values',
            'heuristic_lboolc_values']
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
    labels = ['greedy lboolw', 'exact lboolw', 'exact log(lboolc / n)', 'greedy lboolc']
    for i in range(len(data)):
        plt.plot([p[0] for p in data[i]], [p[1] for p in data[i]], styles[i], label=labels[i])

    plt.axis([-.05, 1, -1, 5])
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., numpoints=1)
    plt.title('Parameters on random graphs of size n = ' + str(graphsize))
    plt.xlabel('Edge probability')
    plt.ylabel('Average parameter value')
    plt.grid(True)
    plt.show()

