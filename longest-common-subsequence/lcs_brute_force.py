'''LCS brute force:.

Generate substrings, starting with the largest ones, and check if they are a
common subsequence.

This is the "extreme" brute force case. It does not attempt any simplification,
e.g. first use a set to first check if the characters are all present.

The only optimization we get is from the use of itertools. It will not generate
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
    # Pick the smallest of the two to generate subsequences and check against
    # the largest of the two
    small, large = (xs, ys) if len(xs) < len(ys) else (ys, xs)

    # Try all subsequences, starting with the longest ones
    for i in range(len(small), 0, -1):
        # Yield one sequence at at time to save memory
        for c in itertools.combinations(small, i):
            if _is_subsequence(c, large):
                # Stop on the first common subsequence we find
                return list(c)
    return []
