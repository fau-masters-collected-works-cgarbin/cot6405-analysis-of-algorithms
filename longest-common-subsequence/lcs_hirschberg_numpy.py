'''LCS Hirschberg Linear Space.

It requires a linear amount of memory, compared to the quadratic amount of
memory used by the dynamic programming version.

Code based on http://wordaligned.org/articles/longest-common-subsequence.

This version has two modifications:

1. Uses NumPy for the arrays to save even more memory and faster performance.
2. Uses indices into the original sequences, instead of slicing the sequences
   in each function call. This reduces the amount of memory that needs to be
   copied around.

IMPORTANT: this version is faster only when used with Numba. Without Numba it
is much slower than the version that uses Python arrays. This is caused by
the conversion of NumPy internal representation to Python objects while
performing loops. Numba seems to avoid it.

Algorithm reference:
https://www.cs.princeton.edu/~wayne/kleinberg-tardos/pdf/06DynamicProgrammingII.pdf
'''
import numpy as np
from numba import njit


@njit
def _lcs_lens(xs, x_start, x_end, ys, y_start, y_end):
    '''Calculates the cost for the sequences.

    This cost is used to decide where to split the sequences.'''
    # Start with zero costs
    len_ys = abs(y_end - y_start)
    curr = np.zeros(1 + len_ys, dtype=np.int32)

    step = 1 if x_start <= x_end else -1

    # Go through the sequences and adjust costs
    for i in range(x_start, x_end, step):
        prev = curr.copy()
        x = xs[i]
        c = 0
        for j in range(y_start, y_end, step):
            curr[c + 1] = prev[c] + 1 if x == ys[j] \
                else max(curr[c], prev[c + 1])
            c += 1

    return curr


@njit
def _lcs(xs, x_start, x_end, ys, y_start, y_end):
    '''Returns a longest common subsequence of
        xs[x_start:x_end], ys[y_start:y_end].
    '''
    # Empty array of strings, to let numba infer the type
    empty_string_list = [str('X') for _ in range(0)]
    nx = x_end - x_start
    if nx == 0:
        # Empty input - got to the end of the sequence
        return empty_string_list
    elif nx == 1:
        # Only one character in the sequence
        # If it is in the other sequence, it's part of the LCS
        return [xs[x_start]] if xs[x_start] in ys[y_start:y_end] \
            else empty_string_list
    else:
        # Find the node to split the xs/ys matrix and split it into two
        # This is the "q" node referred to in algorithms

        # Split the xs range into two halves
        i = nx // 2

        # Since we are working with indices inside the full sequence, the split
        # needs to be adjusted to split the full sequence
        i += x_start

        # Cost for the top-left part (first half of xs + ys)
        # ll_b = _lcs_lens(xb, ys)
        ll_b = _lcs_lens(xs, x_start, i, ys, y_start, y_end)
        # Cost for the bottom-right part (inverted second half of xs, ys)
        # ll_e = _lcs_lens(xe[::-1], ys[::-1])
        ll_e = _lcs_lens(xs, x_end-1, i-1, ys, y_end-1, y_start-1)
        # Invert the costs (of the inverted second half) to align it
        # with the costs of the first half
        ll_e_r = ll_e[::-1]

        # Choose the ys split based on cost (now we have "q")
        cost = ll_b + ll_e_r
        k = np.argmax(cost)

        # Since we are working with indices inside the full sequence, k needs
        # to be adjusted to split the full sequence
        k += y_start

        # Solve each part of the split matrix
        # return lcs(xb, yb) + lcs(xe, ye)
        return _lcs(xs, x_start, i, ys, y_start, k) + \
            _lcs(xs, i, x_end, ys, k, y_end)


@njit
def lcs(xs, ys):
    return _lcs(xs, 0, len(xs), ys, 0, len(ys))
