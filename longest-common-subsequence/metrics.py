'''Run the experiments and collect metrics.
'''
from collections import namedtuple
from memory_profiler import memory_usage
import random
import lcs_brute_force
import lcs_dynamic_programming_dict
import lcs_dynamic_programming_matrix_python
import lcs_dynamic_programming_matrix_numpy
import lcs_hirschberg
import lcs_hirschberg_numpy
import lcs_recursive
import lcs_test
import lcs_utils
import time


Algorithm = namedtuple('Algorithm', ['function', 'description'])
algorithms = [
    Algorithm(lcs_brute_force.lcs, 'Brute force'),
    Algorithm(lcs_hirschberg.lcs, 'Hirschberg'),
    Algorithm(lcs_hirschberg_numpy.lcs, 'Hirschberg NumPy'),
    Algorithm(lcs_dynamic_programming_dict.lcs, 'Dynamic programming dict'),
    Algorithm(lcs_dynamic_programming_matrix_numpy.lcs,
              'Dynamic programming NumPy'),
]

#tests = [(10_000, 1_000), (100_000, 10_000)]
tests = [(10_000, 1_000), (100_000, 1_000)]
#tests = [(10_000, 1_000)]

for dna_size, dna_strand_size in tests:
    dna = lcs_utils.random_dna_sequence(dna_size)
    dna_strand = lcs_utils.random_dna_sequence(dna_strand_size)

    print('\nTimes for DNA {:,}, DNA strand {:,}'.format(
        len(dna), len(dna_strand)))
    for alg in algorithms:
        start = time.process_time()

        alg.function(dna, dna_strand)
        total_time = time.process_time() - start

        print('  {:>30}: {:.3f}'.format(alg.description, total_time))

# Measure memory and time again
# Measuring in a separate loop to check the performance impact of
# memory profiling
for dna_size, dna_strand_size in tests:
    dna = lcs_utils.random_dna_sequence(dna_size)
    dna_strand = lcs_utils.random_dna_sequence(dna_strand_size)

    print('\nMemory and time for DNA {:,}, DNA strand {:,}'.format(
        len(dna), len(dna_strand)))
    for alg in algorithms:
        start = time.process_time()

        memory = memory_usage((alg.function, (dna, dna_strand)))
        total_time = time.process_time() - start

        print('  {:>30}: {:.3f} {:.3f} {}'.format(
            alg.description, max(memory), total_time, memory[:5]))


# Memory profiling
# See the "API" section in https://pypi.org/project/memory-profiler/
#   example of how to monitor mem usage for a function
# https://stackoverflow.com/a/15682871/336802
# https://stackoverflow.com/a/26195843/336802 seem easier and less intrusive
# https://stackoverflow.com/a/44619638/336802 also a simple one