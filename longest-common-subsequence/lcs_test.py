'''Verify that the the LCS implementations are working correctly.

Run this code after making changes to the algorithms.
'''
import lcs_brute_force
import lcs_dynamic_programming
import lcs_dynamic_programming_v2
import lcs_dynamic_programming_numpy
import lcs_hirschberg
import lcs_hirschberg_numpy
import lcs_recursive
import lcs_utils

algorithms = [
    lcs_brute_force.lcs,
    lcs_recursive.lcs,
    lcs_dynamic_programming.lcs,
    lcs_dynamic_programming_v2.lcs,
    lcs_dynamic_programming_numpy.lcs,
    lcs_hirschberg.lcs,
    lcs_hirschberg_numpy.lcs,
]


def _test_lcs(alg, xs, ys, expected=None):
    '''Tests the LCS algorithm against the given input.'''
    lcs = alg(xs, ys)
    if expected is not None and lcs != expected:
        print('{}: X={}, Y={} - expected {}, got {}'.format(
            alg.__module__, xs, ys, expected, lcs))
        assert(False)
    else:
        assert(lcs_utils.is_subsequence(xs, lcs))
        assert(lcs_utils.is_subsequence(ys, lcs))


def _test_lcs_algorithm(alg):
    '''Tests the LCS algoritm `alg` with controlled input to check if the
    algorithm is working correctly.'''

    _test_lcs(alg, 'HUMAN', 'CHIMPANZEE')

    # No match case
    _test_lcs(alg, 'ABC', 'XYZ', [])

    # All posible combinations of a short case
    _test_lcs(alg, 'AB', 'A', ['A'])
    _test_lcs(alg, 'AB', 'B', ['B'])
    _test_lcs(alg, 'ABC', 'A', ['A'])
    _test_lcs(alg, 'ABC', 'AB', ['A', 'B'])
    _test_lcs(alg, 'ABC', 'B', ['B'])
    _test_lcs(alg, 'ABC', 'BC', ['B', 'C'])
    _test_lcs(alg, 'ABC', 'C', ['C'])
    _test_lcs(alg, 'ABC', 'AC', ['A', 'C'])
    _test_lcs(alg, 'ABC', 'ABC', ['A', 'B', 'C'])

    # A bit longer case
    _test_lcs(alg, 'ABC', 'ABCD', ['A', 'B', 'C'])
    _test_lcs(alg, 'DABC', 'ABC', ['A', 'B', 'C'])
    _test_lcs(alg, 'DABC', 'ABCD', ['A', 'B', 'C'])

    # And a larger one
    _test_lcs(alg, 'HUMAN', 'CHIMPANZEE', ['H', 'M', 'A', 'N'])


def _test_basic_cases():
    '''Runs all tests in all LCS algorithms using controlled input.

    Run these tests first. If they fail, they are easier to debug.
    '''
    for alg in algorithms:
        _test_lcs_algorithm(alg)

    print('All basic tests passed')


def _test_dna_strand():
    '''Runs all tests in all LCS algorithms using simulated DNA sequences.

    These tests use large(ish) DNA sequences. With large input, the LCS that
    each algorithm finds is not necessarily the same, so there is predefined
    LCS to test against.
    '''
    dna = lcs_utils.random_dna_sequence(1_000)
    dna_strand = lcs_utils.random_dna_sequence(100)

    # Calculate the LCSs
    lcs = [alg(dna, dna_strand) for alg in algorithms]

    # Check if they are indeed LCSs
    for seq in lcs:
        assert(lcs_utils.is_subsequence(dna, seq))

    # Besides finding the correct subsequence, all algorithms must find a
    # subsqequence of the same length to ensure they are indeed finding an LCS,
    # not just any common subsequence
    seqlen = [len(seq) for seq in lcs]
    assert(all(x == seqlen[0] for x in seqlen))

    print('All DNA tests passed')


def test(visualize=False):
    '''Tests if the algorithms are working correctly.

    Two tests are executed:

    1. A test with short sequences, to help debug basic failures.
    2. A test with large sequence, to account for possible corner cases
       with large sequences.

    Keyword Arguments:
        visualize {bool} -- set to True to see examples of subsequences found
            found by the algorithms. This is an extra check, to visualize
            inspect the results, in case the test code itself is under
            suspicion.
    '''
    _test_basic_cases()
    _test_dna_strand()

    if visualize:
        print('Visual inspection:')
        dna = lcs_utils.random_dna_sequence(30)
        dna_strand = lcs_utils.random_dna_sequence(20)
        for alg in algorithms:
            lcs = alg(dna, dna_strand)
            lcs_utils.print_subsequence(dna, lcs, '{:>30}: '.format(
                alg.__module__))
