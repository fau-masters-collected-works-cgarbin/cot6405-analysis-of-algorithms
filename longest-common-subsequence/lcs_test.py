'''Verify that the the LCS implementations are working correctly.

Run this code after making changes to the algorithms.
'''
import lcs_brute_force
import lcs_dynamic_programming
import lcs_dynamic_programming_v2
import lcs_hirschberg
import lcs_recursive
import lcs_utils


def _test_lcs(alg, xs, ys, expected=None):
    '''Tests the LCS algorithm against the given input.'''
    lcs = alg(xs, ys)
    if expected is not None and lcs != expected:
        print('X: {}, Y: {} - expected {}, got {}'.format(
            xs, ys, expected, lcs))
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
    _test_lcs_algorithm(lcs_brute_force.lcs)
    _test_lcs_algorithm(lcs_recursive.lcs)
    _test_lcs_algorithm(lcs_dynamic_programming.lcs)
    _test_lcs_algorithm(lcs_dynamic_programming_v2.lcs)
    _test_lcs_algorithm(lcs_hirschberg.lcs)

    print('All basic tests passed')


def _test_dna_strand():
    '''Runs all tests in all LCS algorithms using simulated DNA sequences.

    These tests use large(ish) DNA sequences. With large input, the LCS that
    each algorithm finds is not necessarily the same, so there is predefined
    LCS to test against.
    '''
    dna = lcs_utils.random_dna_sequence(1_000)
    dna_strand = lcs_utils.random_dna_sequence(100)

    lcs_bf = lcs_brute_force.lcs(dna, dna_strand)
    assert(lcs_utils.is_subsequence(dna, lcs_bf))

    lcs_r = lcs_recursive.lcs(dna, dna_strand)
    assert(lcs_utils.is_subsequence(dna, lcs_r))

    lcs_dp = lcs_dynamic_programming.lcs(dna, dna_strand)
    assert(lcs_utils.is_subsequence(dna, lcs_dp))

    lcs_dpv2 = lcs_dynamic_programming_v2.lcs(dna, dna_strand)
    assert(lcs_utils.is_subsequence(dna, lcs_dpv2))

    lcs_h = lcs_hirschberg.lcs(dna, dna_strand)
    assert(lcs_utils.is_subsequence(dna, lcs_h))

    # Besides finding the correct subsequence, all algorithms must find a
    # subsqequence of the same length to ensure they are indeed finding an LCS,
    # not just any common subsequence
    assert(len(lcs_bf) == len(lcs_r))
    assert(len(lcs_bf) == len(lcs_dp))
    assert(len(lcs_bf) == len(lcs_dpv2))
    assert(len(lcs_bf) == len(lcs_h))

    print('All DNA tests passed')


def test():
    _test_basic_cases()
    _test_dna_strand()
