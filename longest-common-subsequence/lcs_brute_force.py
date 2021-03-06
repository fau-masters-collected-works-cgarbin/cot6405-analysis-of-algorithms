'''LCS brute force:.

Generate substrings, starting with the largest ones, and check if they are a
common subsequence.

This is not the "extreme" brute force case, where all possible subsequences are
generated ahead of time. It uses itertools, which does generate all
combinations up front. It will yield one when asked. This saves memory.

Optimization note: Numba is not used here because it slowed down the code.
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
        # Yield one sequence at a time to save memory
        for c in itertools.combinations(small, i):
            if _is_subsequence(c, large):
                # Stop on the first common subsequence we find
                return list(c)
    return []
