from ..lboolw import compute_lboolw
from ..lboolc import compute_lboolc
from ..heuristic import greedy, greedy_cost, check_decomposition, random_decomposition
from .common import generate_random_graphs, compute_data, compute_avg_data

from numpy import mean, arange
import matplotlib.pyplot as plt
import math

graphsize = 20
p_values = [round(p, 5) for p in arange(0.05, 1, 0.05)]
samples = 20
total_nr = samples * len(p_values)


def run():
    inputdir = 'input/random20/' # Must end with slash
    outputdir = 'experiment-data/lboolw-exact-vs-heuristic/' # Must end with slash

    experiment_name = 'random'
    def compute(graph):
        decomposition = random_decomposition(graph)
        value = check_decomposition(graph, decomposition)
        return value
    def avg(values):
        #return math.log(mean(values)/graphsize, 2)
        return math.log(mean(values), 2)

    #generate_random_graphs(graphsize, p_values, samples, inputdir)
    #compute_data(inputdir, outputdir, experiment_name, compute, total_nr)
    #compute_avg_data(outputdir, experiment_name, avg, total_nr)
    plot_data(outputdir)


def plot_data(outputdir):
    filenames = ['lboolw', 'lboolc', 'greedy_lboolw', 'greedy_lboolc', 'random']
    labels = ['exact lboolw', 'exact lboolc', 'greedy lboolw', 'greedy lboolc', 'random']
    data = []
    for i, filename in enumerate(filenames):
        data.append([])
        with open(outputdir + filename + '_results', 'r') as f:
            for line in f:
                p, value = [float(s) for s in line.split(':')]
                data[i].append((p, value))

    plt.subplot(121)
    #styles = ['ro', 'g^', 'bs', 'cD', 'mh', 'k+']
    styles = ['ro', 'g^', 'bs', 'cD', 'mh', 'k+']
    for i in range(len(data)):
        plt.plot([p[0] for p in data[i]], [p[1] for p in data[i]], styles[i], label=labels[i])

    plt.axis([-.05, 1, -1, 10])
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., numpoints=1)
    plt.title('Parameters on random graphs of size n = ' + str(graphsize))
    plt.xlabel('Edge probability')
    plt.ylabel('Average parameter value')
    plt.grid(True)
    plt.show()

