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
#tests = [(1_000, 100), (10_000, 1_000), (100_000, 10_000)]
# tests = [(1_000, 100), (10_000, 1_000), (100_000, 1_000)]
tests = [(1_000, 100), (10_000, 1_000)]


def runtime(repeat=2, verbose=1):
    '''Measures algorithms' runtime.

    Keyword Arguments:
        repeat {int} -- How many times to measure each algorithm.
        verbose {int} -- Set to > 0 for different levels of outputs while
            testing.

    Returns:
        list -- A list of measurements. Each entry is an array with:
            - The algorithm description
            - The size of the first sequence used in the test
            - The size of the second sequence used in the test
            - The repetition number (to identify each run)
            - The time to complete the run in milliseconds
    '''
    results = []
    for dna_size, dna_strand_size in tests:
        # Create the test strings only once to correcly compare algorithms
        dna = lcs_utils.random_dna_sequence(dna_size)
        dna_strand = lcs_utils.random_dna_sequence(dna_strand_size)

        if verbose >= 1:
            print('\nTimes for DNA {:,}, DNA strand {:,}'.format(
                len(dna), len(dna_strand)))

        for alg in algorithms:
            if verbose == 1:
                print('\n{}: '.format(alg.description), end='', flush=True)
            for i in range(repeat):
                start = time.process_time()
                lcs = alg.function(dna, dna_strand)
                total_time = time.process_time() - start
                results.append([alg.description, dna_size, dna_strand_size,
                                i+1, total_time])

                if verbose >= 2:
                    print('  {:>30}: {:.3f}'.format(
                        alg.description, total_time))
                elif verbose >= 1:
                    print('{}/{},'.format(i+1, repeat), end='', flush=True)

                    # Make that the algorithm is working correctly
                assert(lcs_utils.is_subsequence(dna, lcs))

    return results


def memory(repeat=2, verbose=1):
    '''Measures algorithms' memory usage.

    Memory usage has to be done separately from runtime measurement because
    tracking memory usage affects runtime. It is more notieable in the cases
    where the algorithm finishes quickly, e.g. fast algorithms or small input.

    Having said that, measuring memory usage has been tricky. It varies from
    one run to the next. To help stabilize the numbers, there techniques were
    used in this code:

    1. Call gc.collect() to not measure any left over from previous runs.
    2. Call an empty function to get a memory usage basline.

    Also, call this function right after calling the time measurement function.
    This allows the environment to reach a stable memory usage state (e.g. load
    all modules it needs), so a better baseline can be measured.

    Keyword Arguments:
        repeat {int} -- How many times to measure each algorithm.
        verbose {int} -- Set to > 0 for different levels of outputs while
            testing.

    Returns:
        list -- A list of measurements. Each entry is an array with:
            - The algorithm description
            - The size of the first sequence used in the test
            - The size of the second sequence used in the test
            - The repetition number (to identify each run)
            - The amount of memory used in KiB.
            - The time to execute to the algorithm, but note that measuring
              memory usage affects runtime, especially for the faster
              case (fast algorithms and/or small input size).
    '''
    results = []
    for dna_size, dna_strand_size in tests:
        # Create the test strings only once to correcly compare algorithms
        dna = lcs_utils.random_dna_sequence(dna_size)
        dna_strand = lcs_utils.random_dna_sequence(dna_strand_size)

        if verbose >= 1:
            print('\nMemory and time for DNA {:,}, DNA strand {:,}'.format(
                len(dna), len(dna_strand)))

        for alg in algorithms:
            if verbose == 1:
                print('\n{}: '.format(alg.description), end='', flush=True)
            for i in range(repeat):
                # Run garbage collection so we don't measure memory left over
                # from other algorithm runs
                gc.collect()

                # Get the current memory usage of the Python environment
                mem_baseline = min([min(memory_usage(
                    (lcs_empty.lcs, (dna, dna_strand)), interval=0.01))
                    for _ in range(3)])

                start = time.process_time()
                mem_usage = memory_usage((alg.function, (dna, dna_strand)),
                                         interval=0.01)
                total_time = time.process_time() - start
                results.append([alg.description, dna_size, dna_strand_size,
                                i + 1, max(mem_usage) - mem_baseline,
                                total_time])

                if verbose >= 2:
                    print('  {:>30}: {:.6f} {:.6f} {:.3f} {}'.format(
                        alg.description, max(mem_usage), mem_baseline,
                        total_time, mem_usage[:5]))
                elif verbose >= 1:
                    print('{}/{},'.format(i+1, repeat), end='', flush=True)

    return results
