'''Run the experiments and collect metrics.
'''
from collections import namedtuple
from memory_profiler import memory_usage
import pandas as pd
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

# DataFrame columns
DF_ALGORITHM = 'Algorithm'
DF_SEQ_SIZE = 'Sequence size'
DF_SUBSEQ_SIZE = 'Subsequence size'
DF_TEST_NUMBER = 'Test number'
DF_RUNTIME = 'Runtime (s)'
DF_MEMORY = 'Memory (KiB)'


# The tests to execute
#tests = [(1_000, 100), (10_000, 1_000), (100_000, 10_000)]
# tests = [(1_000, 100), (10_000, 1_000), (100_000, 1_000)]
tests = [(1_000, 100), (10_000, 1_000)]


def _runtime(repeat=2, verbose=1):
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

    # Run one test
    def _run_test(alg, seq_size, subseq_size):
        start = time.process_time()
        lcs = alg.function(dna, dna_strand)
        total_time = time.process_time() - start
        results.append([alg.description, dna_size, dna_strand_size,
                        i+1, total_time])
        # Make that the algorithm is working correctly
        assert(lcs_utils.is_subsequence(dna, lcs))
        if verbose >= 2:
            print('  {:>30}: {:.3f}'.format(alg.description, results[-1][4]))

    # Run all tests
    for dna_size, dna_strand_size in tests:
        # Create the test strings only once to correcly compare algorithms
        dna = lcs_utils.random_dna_sequence(dna_size)
        dna_strand = lcs_utils.random_dna_sequence(dna_strand_size)

        for alg in algorithms:
            if verbose == 1:
                print('\n{}: '.format(alg.description), end='', flush=True)
            for i in range(repeat):
                _run_test(alg, dna, dna_size)
                if verbose >= 1:
                    print('{}/{},'.format(i+1, repeat), end='', flush=True)

    return results


def _memory(repeat=2, verbose=1):
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

    # Run one test
    def _run_test(alg, seq_size, subseq_size):
        # Garbage-collec to not measure memory left over from other runs
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
                alg.description, max(mem_usage), mem_baseline, total_time,
                mem_usage[:5]))

    # Run all tests
    for dna_size, dna_strand_size in tests:
        # Create the test strings only once to correcly compare algorithms
        dna = lcs_utils.random_dna_sequence(dna_size)
        dna_strand = lcs_utils.random_dna_sequence(dna_strand_size)

        for alg in algorithms:
            if verbose == 1:
                print('\n{}: '.format(alg.description), end='', flush=True)
            for i in range(repeat):
                _run_test(alg, dna, dna_strand)
                if verbose >= 1:
                    print('{}/{},'.format(i+1, repeat), end='', flush=True)

    return results


def runtime(repeat=2, verbose=1):
    """Runs runtime tests and returns raw and summary statistics.

    Keyword Arguments:
        repeat {int} -- How many times to measure each algorithm.
        verbose {int} -- Set to > 0 for different levels of outputs while
            testing.

    Returns:
        DataFrame -- Raw results of all runs, as documented in the internal
            function.
        DataFrame -- Summary results, with average runtime for each experiment.
    """
    results_raw = _runtime(repeat, verbose)

    # Raw results - all data points
    results_raw_pd = pd.DataFrame(results_raw)
    results_raw_pd.columns = [DF_ALGORITHM, DF_SEQ_SIZE, DF_SUBSEQ_SIZE,
                              DF_TEST_NUMBER, DF_RUNTIME]

    # Summary results - average runtime for each experiment
    results_summary_pd = results_raw_pd.groupby(
        [DF_ALGORITHM, DF_SEQ_SIZE, DF_SUBSEQ_SIZE]).mean()
    # Average of test number doesn't make sense, so drop it
    results_summary_pd.drop([DF_TEST_NUMBER], axis='columns', inplace=True)
    # Flatten the results to make it easier to understand and use in graphs
    results_summary_pd.reset_index(inplace=True)

    return results_raw_pd, results_summary_pd


def memory(repeat=2, verbose=1):
    """Runs memory usage tests and returns raw and summary statistics.

    Keyword Arguments:
        repeat {int} -- How many times to measure each algorithm.
        verbose {int} -- Set to > 0 for different levels of outputs while
            testing.

    Returns:
        DataFrame -- Raw results of all runs, as documented in the internal
            function.
        DataFrame -- Summary results, with average memory usage for each
            experiment.
    """
    results_raw = _memory(repeat, verbose)

    # Raw results - all data points
    results_raw_pd = pd.DataFrame(results_raw)
    results_raw_pd.columns = [DF_ALGORITHM, DF_SEQ_SIZE, DF_SUBSEQ_SIZE,
                              DF_TEST_NUMBER, DF_MEMORY, DF_RUNTIME]

    # Despite all tricks to set a memory baseline, it still returns a baseline
    # that is larger than the memory used by the algorithm. This results in
    # negative memory usage in some cases. To prevent those results from
    # affecting the average, they are ignored for the computations.
    # Summary results - average runtime for each experiment
    non_negative = results_raw_pd[results_raw_pd[DF_MEMORY] >= 0]
    results_summary_pd = non_negative.groupby([DF_ALGORITHM, DF_SEQ_SIZE,
                                               DF_SUBSEQ_SIZE]).mean()
    # Average of test number doesn't make sense, so drop it
    results_summary_pd.drop([DF_TEST_NUMBER], axis='columns', inplace=True)
    # Flatten the results to make it easier to understand and use in graphs
    results_summary_pd.reset_index(inplace=True)

    return results_raw_pd, results_summary_pd
