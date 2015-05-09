from ..lboolw import compute_lboolw
from ..lboolc import compute_lboolc
from ..heuristic import (greedy, greedy_cost, check_decomposition, random_decomposition,
                         greedy_light, lun, min_cover_size, new_lun, relative_neighborhood,
                         minfront, new_lun, neighborhood_size, greedy_light_single_start,
                          min_cover_front, rn_mincover, lun_mincover,
                         relative_neighborhood1, relative_neighborhood2,
                         relative_neighborhood3, relative_neighborhood4,
                         relative_neighborhood5, relative_neighborhood6,
                         relative_neighborhood7, minfront2, minfront3, minfront4
                         )
from .common import generate_random_graphs, compute_data, compute_avg_data, plot_data

from numpy import arange, mean, linspace, logspace
import matplotlib.pyplot as plt
import math

graphsize = 50
p_values = [round(p, 5) for p in arange(0.05, 1, 0.05)] # Linear
#p_values = list(logspace(-10, 0, 19, endpoint=False)) # Logarithmic
#print(p_values)
samples = 20
total_nr = samples * len(p_values)

def run():
    inputdir = 'input/random50/' # Must end with slash
    outputdir = 'experiment-data/heuristics/' # Must end with slash

    #experiments = [('mf', minfront), ('rn', relative_neighborhood), ('lun', lun)]
    #experiments = [
            #('rn_mincover', rn_mincover),
            #('lun_mincover', lun_mincover)
            #]
    experiments = [
            ('N_size', neighborhood_size),
            ('rn1', relative_neighborhood1),
            ('rn2', relative_neighborhood2),
            ('rn3', relative_neighborhood3),
            ('rn4', relative_neighborhood4),
            #('rn5', relative_neighborhood5),
            ('rn6', relative_neighborhood6),
            ('rn7', relative_neighborhood7),
            ('mf2', minfront2),
            ('mf3', minfront3),
            ('mf4', minfront4),
            ]
    for experiment_name, score_function in experiments:
        def compute(graph):
            decomposition = greedy_light_single_start(graph, score_function)
            value = check_decomposition(graph, decomposition)
            #value = greedy(graph)[0]
            return value
        def avg(values):
            #return math.log(mean(values)/graphsize, 2)
            return math.log(mean(values), 2)

        #generate_random_graphs(graphsize, p_values, samples, inputdir)
        compute_data(inputdir, outputdir, experiment_name, compute, total_nr)
        compute_avg_data(outputdir, experiment_name, avg, total_nr)

    filenames = [
            #'random',
            #'N_size',
            #'rn1',
            'rn2',
            #'rn6',
            #'rn7',
            #'rn3',
            #'rn4',
            #'rn5'
            'greedy_lboolw',
            #'lun',
            #'rn', 'mf',
            #'frank_lun',
            #'frank_rn',
            #'new_lun',
            'lun_single',
            #'rn_single',
            #'rn2',
            'minfront_single',
            'mf2',
            'mf3',
            'mf4',
            #'lun_mincover', 'rn_mincover',
            #'min_cover_front_single', 'minfront_single', 'mincover_single'
            ]
    plot_data(outputdir, filenames, filenames, graphsize)
