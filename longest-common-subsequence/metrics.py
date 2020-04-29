#!../env/bin/python
'''Run the experiments and collect metrics.
'''
from collections import namedtuple
from memory_profiler import memory_usage
import pandas as pd
import random
import time
import lcs_empty
import gc
import os
import sys
import lcs_brute_force
import lcs_dynamic_programming_dict
import lcs_dynamic_programming_matrix_python
import lcs_dynamic_programming_matrix_numpy
import lcs_hirschberg
import lcs_hirschberg_numpy
import lcs_hirschberg_numpy_slices
import lcs_recursive
import lcs_test
import lcs_utils

# DataFrame columns - collected data
DF_ALGORITHM = 'Algorithm'
DF_SEQ_SIZE = 'Sequence size'
DF_SUBSEQ_SIZE = 'Subsequence size'
DF_TEST_NUMBER = 'Test number'
DF_EMPIRICAL_RT = 'Empirical RT (ms)'
DF_MEMORY = 'Memory (KiB)'
# DataFrame columns - calculated data
DF_THEORETICAL_COMPLEXITY = 'Theoretical complexity'
DF_RATIO = 'Ratio'
DF_PREDICTED_RT = 'Predicted RT'


# Algorithm names
ALG_BRUTE_FORCE = 'Brute-force'
ALG_DYNAMIC_PROGRAMMING = 'Dynamic programming'
ALG_HIRSCHBERG = 'Hirschberg'

# The algorithms to collect metrics for
Algorithm = namedtuple('Algorithm', ['function', 'description'])
algorithms = [
    Algorithm(lcs_brute_force.lcs, ALG_BRUTE_FORCE),
    Algorithm(lcs_dynamic_programming_matrix_numpy.lcs,
              ALG_DYNAMIC_PROGRAMMING),
    Algorithm(lcs_hirschberg_numpy.lcs, ALG_HIRSCHBERG),
]

seq_phase1 = [
    (1_000, 100), (2_000, 200), (3_000, 300),
    (4_000, 300), (4_000, 500), (4_000, 1_000),
    (5_000, 900), (5_000, 1_000), (5_000, 1_200),
]

seq_phase2 = [
    (10_000, 500), (10_000, 800), (10_000, 1_000),
    (20_000, 1_000), (20_000, 2_000), (20_000, 2_500),
    (30_000, 2_000), (30_000, 3_000), (30_000, 4_000),
]


def _runtime_tests(sequences, repeat=2, verbose=1):
    '''Measures algorithms' runtime.

    Arguments:
        sequences {list} -- The pairs of sequences/subsequence sizes to test.

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
        total_time = (time.process_time() - start) * 1000
        results.append([alg.description, dna_size, dna_strand_size,
                        i+1, total_time])
        # Make that the algorithm is working correctly
        assert(lcs_utils.is_subsequence(dna, lcs))
        if verbose >= 2:
            print('  {:>30}: {:.3f}'.format(alg.description, results[-1][4]))

    # Run all tests
    for dna_size, dna_strand_size in sequences:
        # Create the test strings only once to correcly compare algorithms
        dna = lcs_utils.random_dna_sequence(dna_size)
        dna_strand = lcs_utils.random_dna_sequence(dna_strand_size)
        if verbose >= 1:
            print('\n\nSequence {:,}, subsequence {:,}: '.format(
                len(dna), len(dna_strand), end='', flush=True))

        for alg in algorithms:
            if verbose == 1:
                print('\n   {}: '.format(alg.description),
                      end='', flush=True)
            for i in range(repeat):
                _run_test(alg, dna, dna_size)
                if verbose == 1:
                    print('{}/{},'.format(i+1, repeat), end='', flush=True)

    return results


def _memory_tests(sequences, repeat=2, verbose=1):
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
    This allows the environment to reach a stable memory usage state(e.g. load
    all modules it needs), so a better baseline can be measured.

    Arguments:
        sequences {list} -- The pairs of sequences/subsequence sizes to test.

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
              case(fast algorithms and/or small input size).
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
        total_time = (time.process_time() - start) * 1000
        results.append([alg.description, dna_size, dna_strand_size,
                        i + 1, max(mem_usage) - mem_baseline,
                        total_time])
        if verbose >= 2:
            print('  {:>30}: {:.6f} {:.6f} {:.3f} {}'.format(
                alg.description, max(mem_usage), mem_baseline, total_time,
                mem_usage[:5]))

    # Run all tests
    for dna_size, dna_strand_size in sequences:
        # Create the test strings only once to correcly compare algorithms
        dna = lcs_utils.random_dna_sequence(dna_size)
        dna_strand = lcs_utils.random_dna_sequence(dna_strand_size)
        if verbose >= 1:
            print('\n\nSequence {:,}, subsequence {:,}: '.format(
                len(dna), len(dna_strand), end='', flush=True))

        for alg in algorithms:
            if verbose == 1:
                print('\n   {}: '.format(alg.description),
                      end='', flush=True)
            for i in range(repeat):
                _run_test(alg, dna, dna_strand)
                if verbose == 1:
                    print('{}/{},'.format(i+1, repeat), end='', flush=True)

    return results


def _runtime(sequences, repeat=2, verbose=1):
    '''Runs runtime tests and returns raw and summary statistics.

    Arguments:
        sequences {list} -- The pairs of sequences/subsequence sizes to test.

    Keyword Arguments:
        repeat {int} -- How many times to measure each algorithm.
        verbose {int} -- Set to > 0 for different levels of outputs while
            testing.

    Returns:
        DataFrame -- Raw results of all runs, as documented in the internal
            function.
        DataFrame -- Summary results, with average runtime for each experiment.
    '''
    results_raw = _runtime_tests(sequences, repeat, verbose)

    # Raw results - all data points
    results_raw_pd = pd.DataFrame(results_raw)
    results_raw_pd.columns = [DF_ALGORITHM, DF_SEQ_SIZE, DF_SUBSEQ_SIZE,
                              DF_TEST_NUMBER, DF_EMPIRICAL_RT]

    # Summary results - average runtime for each experiment
    results_summary_pd = results_raw_pd.groupby(
        [DF_ALGORITHM, DF_SEQ_SIZE, DF_SUBSEQ_SIZE]).mean()
    # Average of test number doesn't make sense, so drop it
    results_summary_pd.drop([DF_TEST_NUMBER], axis='columns', inplace=True)
    # Flatten the results to make it easier to understand and use in graphs
    results_summary_pd.reset_index(inplace=True)

    return results_raw_pd, results_summary_pd


def _memory(sequences, repeat=2, verbose=1):
    '''Runs memory usage tests and returns raw and summary statistics.

    Arguments:
        sequences {list} -- The pairs of sequences/subsequence sizes to test.

    Keyword Arguments:
        repeat {int} -- How many times to measure each algorithm.
        verbose {int} -- Set to > 0 for different levels of outputs while
            testing.

    Returns:
        DataFrame -- Raw results of all runs, as documented in the internal
            function.
        DataFrame -- Summary results, with average memory usage for each
            experiment.
    '''
    results_raw = _memory_tests(sequences, repeat, verbose)

    # Raw results - all data points
    results_raw_pd = pd.DataFrame(results_raw)
    results_raw_pd.columns = [DF_ALGORITHM, DF_SEQ_SIZE, DF_SUBSEQ_SIZE,
                              DF_TEST_NUMBER, DF_MEMORY, DF_EMPIRICAL_RT]

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


def _run_experiment(experiment, sequences, repeat=2, verbose=1, file=None):
    '''Run the experiment or load from the cached file, if one is given.

    Arguments:
        experiment {function} -- The experiment to run, runtime or memory
            measurements.
        sequences {list} -- The pairs of sequences/subsequence sizes to test.

    Keyword Arguments:
        repeat {int} -- How many times to measure each algorithm.
        verbose {int} -- Set to > 0 for different levels of outputs while
            testing.
        file {[strung]} -- Name of the file to read from (from a previous run),
            or cached the results to if the experiment is executed.

    Returns:
        DataFrame -- Raw results of all runs, as documented in the internal
            function.
        DataFrame -- Summary results, with average memory usage for each
            experiment.
    '''
    # Load from file, if there is one
    if file is not None:
        raw_file = file + '-raw.csv'
        summary_file = file + '-summary.csv'

        if os.path.isfile(raw_file) and os.path.isfile(summary_file):
            print('Loading from file')
            raw = pd.read_csv(raw_file, index_col=0)
            summary = pd.read_csv(summary_file, index_col=0)
            return raw, summary

    # Can't load from files or file name was not provided
    # Run the experiments
    raw, summary = experiment(sequences, repeat=repeat, verbose=verbose)

    # Save to file, for the next time the function is called
    if file is not None:
        raw.to_csv(file + '-raw.csv')
        summary.to_csv(file + '-summary.csv')

    return raw, summary


def runtime(sequences, repeat=2, verbose=1, file=None):
    return _run_experiment(_runtime, sequences, repeat, verbose, file)


def memory(sequences, repeat=2, verbose=1, file=None):
    return _run_experiment(_memory, sequences, repeat, verbose, file)


def add_analysis(summary, alg):
    '''Add analysis to a summary dataframe.

    The following columns are added to the dataframe:

    - Theoretical complexity
    - Empirical / theoretical ratio
    - Predicted RT, calculated as c * theoretical complexity
    - % error, calculated as (empirical RT - predicted RT)/empiricial RT * 100

    Arguments:
        summary {DataFrame} -- A summary dataframe, created by running the
            experiments.
        alg {string} -- What algorithm to analyze in the summary dataframe

    Returns:
        DataFrame -- A dataframe with entries for `alg`, augmented with the new
            columns.
        int -- The constant c calculated from the `alg` entries.
    '''
    filter = summary[DF_ALGORITHM] == alg
    df = summary[filter].copy()  # copy because we will change it

    if alg == ALG_BRUTE_FORCE:
        # "/1" is a trick to force Pandas/NumPy to calculate with maximum
        # precision - without it, it overflows and sets the value to zero
        df[DF_THEORETICAL_COMPLEXITY] = 2 ** (df[DF_SUBSEQ_SIZE] / 1)
    else:
        df[DF_THEORETICAL_COMPLEXITY] = df[DF_SEQ_SIZE] * df[DF_SUBSEQ_SIZE]

    df[DF_RATIO] = df[DF_EMPIRICAL_RT] / df[DF_THEORETICAL_COMPLEXITY]
    c = max(df[DF_RATIO])
    df[DF_PREDICTED_RT] = c * df[DF_THEORETICAL_COMPLEXITY]
    df['% error'] = (df[DF_EMPIRICAL_RT] - df[DF_PREDICTED_RT]) / \
        df[DF_EMPIRICAL_RT] * 100

    return df, c


if __name__ == "__main__":
    if len(sys.argv) is not 2:
        print('Specify phase1 or phase2')
        exit()

    # For consistency across runs
    random.seed(42)
    lcs_test.test(visualize=True)

    test = sys.argv[1]
    if test == "phase1":
        print('Running phase 1 tests')
        runtime(seq_phase1, repeat=1, verbose=2, file='runtime-phase1')
        memory(seq_phase1, repeat=1, verbose=2, file='memory-phase1')
    elif test == "phase2":
        print('Running phase 2 tests')
        runtime(seq_phase2, repeat=10, verbose=2, file='runtime-phase2')
        memory(seq_phase2, repeat=10, verbose=2, file='memory-phase2')
    else:
        print('Specify phase1 or phase2')
