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


def _test_one_input(fn, xs, ys, expected):
    '''Test the LCS algorithm from `fn`.'''
    result = fn(xs, ys)
    if result != expected:
        print('X: {}, Y: {} - expected {}, got {}'.format(
            xs, ys, expected, result))
        assert(False)


def _test_lcs(fn):
    '''Tests the LCS function `fn` with controlled input to check if the
    function is correct. '''

    # No match case
    _test_one_input(fn, 'ABC', 'XYZ', [])

    # All posible combinations of a short case
    _test_one_input(fn, 'AB', 'A', ['A'])
    _test_one_input(fn, 'AB', 'B', ['B'])
    _test_one_input(fn, 'ABC', 'A', ['A'])
    _test_one_input(fn, 'ABC', 'AB', ['A', 'B'])
    _test_one_input(fn, 'ABC', 'B', ['B'])
    _test_one_input(fn, 'ABC', 'BC', ['B', 'C'])
    _test_one_input(fn, 'ABC', 'C', ['C'])
    _test_one_input(fn, 'ABC', 'AC', ['A', 'C'])
    _test_one_input(fn, 'ABC', 'ABC', ['A', 'B', 'C'])

    # A bit longer case
    _test_one_input(fn, 'ABC', 'ABCD', ['A', 'B', 'C'])
    _test_one_input(fn, 'DABC', 'ABC', ['A', 'B', 'C'])
    _test_one_input(fn, 'DABC', 'ABCD', ['A', 'B', 'C'])

    # And a larger one
    _test_one_input(fn, 'HUMAN', 'CHIMPANZEE', ['H', 'M', 'A', 'N'])


def test():
    _test_lcs(lcs_brute_force.lcs)
    _test_lcs(lcs_recursive.lcs)
    _test_lcs(lcs_dynamic_programming.lcs)
    _test_lcs(lcs_hirschberg.lcs)
