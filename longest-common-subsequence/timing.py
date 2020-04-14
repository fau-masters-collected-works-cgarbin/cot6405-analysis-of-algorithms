'''Run the experiments and collect metrics.
'''
from collections import namedtuple
import random
import lcs_brute_force
import lcs_dynamic_programming
import lcs_dynamic_programming_v2
import lcs_dynamic_programming_numpy
import lcs_hirschberg
import lcs_hirschberg_numpy
import lcs_recursive
import lcs_test
import lcs_utils
import time

# To ensure repeatability
random.seed(42)

# IMPORTANT: make sure the algorithms work before using them
lcs_test.test(visualize=True)

Algorithm = namedtuple('Algorithm', ['function', 'description'])
# algorithms = [
#     Algorithm(lcs_brute_force.lcs, 'Brute force'),
#     Algorithm(lcs_dynamic_programming_v2.lcs, 'Dynamic programming'),
#     Algorithm(lcs_hirschberg.lcs, 'Hirschberg'),
# ]
algorithms = [
    Algorithm(lcs_hirschberg.lcs, 'Hirschberg'),
    Algorithm(lcs_hirschberg_numpy.lcs, 'Hirschberg NumPy'),
    Algorithm(lcs_dynamic_programming_v2.lcs, 'Dynamic programming'),
    Algorithm(lcs_dynamic_programming_numpy.lcs, 'Dynamic programming NumPy'),
]

#tests = [(10_000, 1_000), (100_000, 10_000)]
tests = [(10_000, 1_000)]

for dna_size, dna_strand_size in tests:
    dna = lcs_utils.random_dna_sequence(dna_size)
    dna_strand = lcs_utils.random_dna_sequence(dna_strand_size)

    print('\nTimes for {:,}, {:,}'.format(len(dna), len(dna_strand)))
    for alg in algorithms:
        start = time.process_time()

        alg.function(dna, dna_strand)
        total_time = time.process_time() - start

        print('{:>30}: {:.3f}'.format(alg.description, total_time))
