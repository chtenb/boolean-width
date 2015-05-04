from ..graph import Graph

import shutil
import os
import math
import glob
import time

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


def compute_data(inputdir, outputdir, name, compute, total_nr):
    start_time = time.time()

    outputfile = name + '_raw_results'

    # Read which graphs are already done
    done = []
    try:
        open(inputdir + outputfile, 'x')
    except FileExistsError:
        pass

    with open(inputdir + outputfile, 'r') as f:
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


def compute_avg_data(outputdir, experiment_name, avg):
    data = {}
    raw_file = experiment_name + '_raw_results'
    result_file = experiment_name + '_results'
    with open(outputdir + raw_file, 'r') as f:
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
        avg_data.append((p, avg(values)))

    with open(outputdir + result_file, 'w') as f:
        for p, value in avg_data:
            f.write('{}:{}\n'.format(p, value))
