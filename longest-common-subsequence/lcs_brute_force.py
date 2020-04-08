'''LCS brute force:.

Generate substrings, starting with the largest ones, and check if they are a
common subsequence.

This is the "extreme" brute force case. It does not attempt any simplification,
e.g. first use a set to first check if the characters are all present.

The only optimziation we get is from the use of itertools. It will not generate
all combinations up front. It will yield one when asked. This saves memory.
'''

import itertools


def _is_subsequence(sequence, string):
    '''Checks if the sequence is a subsequence of the string.'''
    len_sequence = len(sequence)
    len_string = len(string)

    seq = 0
    str = 0

    while seq < len_sequence and str < len_string:
        if sequence[seq] == string[str]:
            seq += 1
        str += 1

    return seq == len_sequence


def lcs(xs, ys):
    '''Returns a longest common subsequence of xs, ys.'''
    # Pick the smallest of the two to generate subsequences
    small, large = (xs, ys) if len(xs) < len(ys) else (ys, xs)
    print('------')
    print('Using small={} large={}'.format(small, large))

    # Try all subsequences, starting with the longest one
    for i in range(len(small), 0, -1):
        combinations = [''.join(p) for p in itertools.combinations(small, i)]
        for c in combinations:
            print('  {}'.format(c))
            if _is_subsequence(c, large):
                print('     {} is subseqeunce'.format(c))
                return list(c)
    return []
