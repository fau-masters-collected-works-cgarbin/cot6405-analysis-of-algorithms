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
import lcs_empty
import gc


# The algorithms to collect metrics for
Algorithm = namedtuple('Algorithm', ['function', 'description'])
algorithms = [
    Algorithm(lcs_brute_force.lcs, 'Brute force'),
    Algorithm(lcs_dynamic_programming_matrix_numpy.lcs,
              'Dynamic programming NumPy'),
    Algorithm(lcs_hirschberg_numpy.lcs, 'Hirschberg NumPy'),
]

# The tests to execute
tests = [(1_000, 100), (10_000, 1_000),  (100_000, 1_000)]


def runtime(repeat=2, verbose=True):
    '''Measures algorithms' runtime.'''
    for dna_size, dna_strand_size in tests:
        # Create the test strings only once to correcly compare algorithms
        dna = lcs_utils.random_dna_sequence(dna_size)
        dna_strand = lcs_utils.random_dna_sequence(dna_strand_size)

        if verbose:
            print('\nTimes for DNA {:,}, DNA strand {:,}'.format(
                len(dna), len(dna_strand)))

        for alg in algorithms:
            for _ in range(repeat):
                start = time.process_time()
                lcs = alg.function(dna, dna_strand)
                total_time = time.process_time() - start

                if verbose:
                    print('  {:>30}: {:.3f}'.format(
                        alg.description, total_time))

                # Make that the algorithm is working correctly
                assert(lcs_utils.is_subsequence(dna, lcs))


def memory(repeat=2, verbose=True):
    '''Measures algorithms' memory usage.

    Memory usage has to be done separately from runtime meaurement because
    tracking memory usage affects runtime. It is more notieable in the cases
    where the algorithm finishes quickly, e.g. fast algorithms or small input.
    '''
    # Run all algorithms once to load all we need in teh Python environemtn.
    # creating a baseline for memory usage
    for dna_size, dna_strand_size in tests:
        dna = lcs_utils.random_dna_sequence(dna_size)
        dna_strand = lcs_utils.random_dna_sequence(dna_strand_size)
        for alg in algorithms:
            print('Warming up - {} {},{}'.format(alg.description,
                                                 dna_size, dna_strand_size))
            alg.function(dna, dna_strand)

    for dna_size, dna_strand_size in tests:
        # Create the test strings only once to correcly compare algorithms
        dna = lcs_utils.random_dna_sequence(dna_size)
        dna_strand = lcs_utils.random_dna_sequence(dna_strand_size)

        if verbose:
            print('\nMemory and time for DNA {:,}, DNA strand {:,}'.format(
                len(dna), len(dna_strand)))

        for alg in algorithms:
            for _ in range(repeat):
                # Run garbage collection so we don't measure memory left over
                # from other algorithm runs
                gc.collect()

                # Get the current memory usage of the Python environment
                mem_baseline = min([min(memory_usage(
                    (lcs_empty.lcs), interval=0.01)) for _ in range(3)])

                start = time.process_time()
                mem_usage = memory_usage((alg.function, (dna, dna_strand)),
                                         interval=0.01)
                total_time = time.process_time() - start

                if verbose:
                    print('  {:>30}: {:.6f} {:.6f} {:.3f} {}'.format(
                        alg.description, max(mem_usage), mem_baseline,
                        total_time, mem_usage[:5]))


# Use this to measure the current memory consumption
for _ in range(5):
    mem_usage = memory_usage((lcs_empty.lcs), interval=0.01)
    print(mem_usage)


memory()
