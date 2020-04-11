'''Verify that the the LCS implementations are working correctly.

Run this code after making changes to the algorithms.

IMPORTANT: this code assumes that all algorithms will returnt the same longest
common subsequence. There may be more than one LCS. This assumption is safe
for the code we have here, but may not be true for other cases.
'''
import lcs_brute_force
import lcs_dynamic_programming
import lcs_hirschberg
import lcs_recursive


def _is_subsequence(seq, subseq):
    '''Checks if the given subsequence is indeed a subsequence of the
    sequence.'''
    j = 0
    for i in range(len(subseq)):
        while subseq[i] != seq[j] and j < len(seq):
            j += 1
    # To be a subsequence we must not to past the length of the sequence
    return j < len(seq)


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
    assert(_is_subsequence('ABC', ['A', 'B', 'C']))
    assert(_is_subsequence('CHIMPANZEE', ['H', 'M', 'A', 'N']))

    # Negative test cases
    assert(_is_subsequence('AB', ['C']) is False)
    assert(_is_subsequence('ABC', ['B', 'A']) is False)
    assert(_is_subsequence('CHIMPANZEE', ['E', 'M', 'A', 'N']) is False)


def _test_lcs(fn, xs, ys, expected=None):
    '''Test the LCS algorithm from `fn`.'''
    lcs = fn(xs, ys)
    if expected is not None and lcs != expected:
        print('X: {}, Y: {} - expected {}, got {}'.format(
            xs, ys, expected, lcs))
        assert(False)
    else:
        assert(_is_subsequence(xs, lcs))
        assert(_is_subsequence(ys, lcs))


def _test_all(fn):
    '''Tests the LCS function `fn` with controlled input to check if the
    function is correct. '''

    _test_lcs(fn, 'HUMAN', 'CHIMPANZEE')

    # No match case
    _test_lcs(fn, 'ABC', 'XYZ', [])

    # All posible combinations of a short case
    _test_lcs(fn, 'AB', 'A', ['A'])
    _test_lcs(fn, 'AB', 'B', ['B'])
    _test_lcs(fn, 'ABC', 'A', ['A'])
    _test_lcs(fn, 'ABC', 'AB', ['A', 'B'])
    _test_lcs(fn, 'ABC', 'B', ['B'])
    _test_lcs(fn, 'ABC', 'BC', ['B', 'C'])
    _test_lcs(fn, 'ABC', 'C', ['C'])
    _test_lcs(fn, 'ABC', 'AC', ['A', 'C'])
    _test_lcs(fn, 'ABC', 'ABC', ['A', 'B', 'C'])

    # A bit longer case
    _test_lcs(fn, 'ABC', 'ABCD', ['A', 'B', 'C'])
    _test_lcs(fn, 'DABC', 'ABC', ['A', 'B', 'C'])
    _test_lcs(fn, 'DABC', 'ABCD', ['A', 'B', 'C'])

    # And a larger one
    _test_lcs(fn, 'HUMAN', 'CHIMPANZEE', ['H', 'M', 'A', 'N'])


def test():
    _test_all(lcs_brute_force.lcs)
    _test_all(lcs_recursive.lcs)
    _test_all(lcs_dynamic_programming.lcs)
    _test_all(lcs_hirschberg.lcs)

    print('All tests passed')
