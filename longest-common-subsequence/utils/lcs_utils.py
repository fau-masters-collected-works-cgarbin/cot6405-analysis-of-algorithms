'''Utility functions for the LCS algorithms tests.'''
import random


def _test_subseqence_match():
    '''Tests if the subsequence check is working correctly.

    This is crucial for the tests. Run this code after modifying the
    subsequence checker code.'''
    assert(is_subsequence('AB', ['A']))
    assert(is_subsequence('AB', ['B']))
    assert(is_subsequence('ABC', ['A', 'B']))
    assert(is_subsequence('ABC', ['B']))
    assert(is_subsequence('ABC', ['B', 'C']))
    assert(is_subsequence('ABC', ['A', 'B', 'C']))
    assert(is_subsequence('CHIMPANZEE', ['H', 'M', 'A', 'N']))
    # Empty sequence is a subsequence
    assert(is_subsequence('CHIMPANZEE', []))

    # Negative test cases
    assert(is_subsequence('AB', ['C']) is False)
    assert(is_subsequence('ABC', ['B', 'A']) is False)
    assert(is_subsequence(
        'CHIMPANZEE', ['E', 'M', 'A', 'N']) is False)


def print_subsequence(seq, subseq, prefix='', show_seq=True):
    '''Prints a subsequence aligned with the matches in the sequence.

    IMPORTANT: the subsequence must indeed be a subsequence. The code will
    fail miserably if it's not.
    '''
    lcs_aligned = list()
    i = 0
    # Go through the subsequence elements in the order they are specified
    for j in range(len(seq)):
        if i < len(subseq) and seq[j] == subseq[i]:
            lcs_aligned.append(subseq[i])
            i += 1
        else:
            lcs_aligned.append('.')

    if show_seq:
        print('{} {}'.format(prefix, seq))
    print('{} {} size={}'.format(
        prefix, ''.join(lcs_aligned), len(subseq)))


def is_subsequence(seq, subseq):
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


def random_dna_sequence(length):
    '''Generates a random DNA sequence of the given length.'''
    return ''.join(random.choice('ACTG') for _ in range(length))


def is_outlier(s):
    """Filter out outliers from a Pandas Seriers.

    Outliers are defined as "outside of a specific standard deviation range".
    This leaves still a large number of data points, while removing the ones
    that are truly way out there and could skew the calculations.

    Arguments:
        s {Pandas Series of floats} -- The range to be inspected.

    Returns:
        Array of bools -- For each member of `s`, True if it's an outlier,
            or False if not.
    """
    if len(s) >= 2:
        boundary = s.std() * 3
        lower_limit = s.mean() - boundary
        upper_limit = s.mean() + boundary
    else:
        # Smaller series don't have outliers by definition
        lower_limit = s.min()
        upper_limit = s.max()

    return ~ s.between(lower_limit, upper_limit)


# Subsequence matching code is crucial for this module to work
# Test it every time this module is imported
_test_subseqence_match()
