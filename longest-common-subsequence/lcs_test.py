'''Verify that the the LCS implementations are working correctly.

Run this code after making changes to the algorithms.
'''
import random
import lcs_brute_force
import lcs_dynamic_programming
import lcs_hirschberg
import lcs_recursive


def _print_subsequence(seq, subseq, prefix=None):
    '''Prints a subsequence aligned with the matches in the sequence.

    IMPORTANT: the subsequence must indeed be a subsequence. The code will
    fail miserably if it's not.'''
    lcs_aligned = list()
    i = 0
    # Go through the subsequence elements in the order they are specified
    for j in range(len(seq)):
        if i < len(subseq) and seq[j] == subseq[i]:
            lcs_aligned.append(subseq[i])
            i += 1
        else:
            lcs_aligned.append('.')

    # Successfully found all subseqeuece elements
    print('{} {}'.format(prefix, seq))
    print('{} {}'.format(prefix, ''.join(lcs_aligned)))


def _is_subsequence(seq, subseq):
    '''Checks if the given subsequence is indeed a subsequence of the
    sequence. '''
    j = 0
    # Go through the subsequence elements in the order they are specified
    for i in range(len(subseq)):
        # Look for the subsequence element in the sequence
        while j < len(seq) and subseq[i] != seq[j]:
            j += 1
        # If we couldn't find the element, it's not a subsequence
        if j >= len(seq):
            return False

    # Successfully found all subseqeuece elements
    return True


def _test_subseqence_match():
    '''Tests if the subsequence check is working correctly.

    This is crucial for the tests. Run this code after modifying the
    subsequence checker code.'''
    assert(_is_subsequence('AB', ['A']))
    assert(_is_subsequence('AB', ['B']))
    assert(_is_subsequence('ABC', ['A', 'B']))
    assert(_is_subsequence('ABC', ['B']))
    assert(_is_subsequence('ABC', ['B', 'C']))
    assert(_is_subsequence('ABC', ['A', 'B', 'C']))
    assert(_is_subsequence('CHIMPANZEE', ['H', 'M', 'A', 'N']))
    # Empty sequence is a subsequence
    assert(_is_subsequence('CHIMPANZEE', []))

    # Negative test cases
    assert(_is_subsequence('AB', ['C']) is False)
    assert(_is_subsequence('ABC', ['B', 'A']) is False)
    assert(_is_subsequence('CHIMPANZEE', ['E', 'M', 'A', 'N']) is False)


def _test_lcs(alg, xs, ys, expected=None):
    '''Tests the LCS algorithm against the given input.'''
    lcs = alg(xs, ys)
    if expected is not None and lcs != expected:
        print('X: {}, Y: {} - expected {}, got {}'.format(
            xs, ys, expected, lcs))
        assert(False)
    else:
        assert(_is_subsequence(xs, lcs))
        assert(_is_subsequence(ys, lcs))


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
    _test_lcs_algorithm(lcs_hirschberg.lcs)

    print('All basic tests passed')


def _test_dna_strand():
    '''Runs all tests in all LCS algorithms using simulated DNA sequences.

    These tests use large(ish) DNA sequences. With large input, the LCS that
    each algorithm finds is not necessarily the same, so there is predefined
    LCS to test against.
    '''

    def random_dna_sequence(length):
        '''Generates a random DNA sequence of the given length.'''
        return ''.join(random.choice('ACTG') for _ in range(length))

    print('Running DNA strand tests')

    dna = random_dna_sequence(100)
    dna_strand = random_dna_sequence(50)
    print(dna_strand)

    print('   Starting brute-force LCS (1/4)')
    lcs_bf = lcs_brute_force.lcs(dna, dna_strand)
    _print_subsequence(dna, lcs_bf, '     ')
    assert(_is_subsequence(dna, lcs_bf))

    print('   Starting recursive LCS (2/4)')
    lcs_r = lcs_recursive.lcs(dna, dna_strand)
    _print_subsequence(dna, lcs_r, '     ')
    assert(_is_subsequence(dna, lcs_r))

    print('   Starting dynamic programming LCS (3/4)')
    lcs_dp = lcs_dynamic_programming.lcs(dna, dna_strand)
    _print_subsequence(dna, lcs_dp, '     ')
    assert(_is_subsequence(dna, lcs_dp))

    print('   Starting Hirschberg LCS (4/4)')
    lcs_h = lcs_hirschberg.lcs(dna, dna_strand)
    _print_subsequence(dna, lcs_h, '     ')
    assert(_is_subsequence(dna, lcs_h))

    # Besides finding the correct subsequence, all algorithms must find a
    # subsqequence of the same length to ensure they are indeed finding an LCS,
    # not just any common subsequence
    assert(len(lcs_bf) == len(lcs_r))
    assert(len(lcs_bf) == len(lcs_dp))
    assert(len(lcs_bf) == len(lcs_h))

    print('All DNA tests passed')


def test():
    _test_basic_cases()
    _test_dna_strand()


def main():
    '''Subsequence matching code is crucial for this module to work.

    Test it every time this module is imported.'''
    _test_subseqence_match()
