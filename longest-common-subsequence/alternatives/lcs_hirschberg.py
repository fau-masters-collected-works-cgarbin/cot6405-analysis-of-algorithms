w'''LCS Hirschberg Linear Space.

It requires a linear amount of memory, compared to the quadratic amount of
memory used by the dynamic programming version.

Code based on http://wordaligned.org/articles/longest-common-subsequence.

Algorithm reference:
https://www.cs.princeton.edu/~wayne/kleinberg-tardos/pdf/06DynamicProgrammingII.pdf
'''
from numba import njit


@njit
def _lcs_lens(xs, ys):
    '''Calculates the cost for the sequences.

    This cost is used to decide where to split the sequences.'''
    # Start with zero costs
    curr = [0] * (1 + len(ys))
    # Go through the sequences and adjust costs
    for x in xs:
        prev = list(curr)
        for i, y in enumerate(ys):
            if x == y:
                curr[i + 1] = prev[i] + 1
            else:
                curr[i + 1] = max(curr[i], prev[i + 1])
    return curr


@njit
def lcs(xs, ys):
    '''Returns a longest common subsequence of xs, ys.'''
    # Empty array of strings, to let numba infer the type
    empty_string_list = [str('X') for _ in range(0)]
    nx = len(xs)
    if nx == 0:
        # Empty input - got to the end of the sequence
        return empty_string_list
    elif nx == 1:
        # Only one character in the sequence
        # If it is in the other sequence, it's part of the LCS
        return [xs[0]] if xs[0] in ys else empty_string_list
    else:
        # Find the node to split the xs/ys matrix and split it into two
        # This is the "q" node referred to in algorithms

        # Split xs into two halves
        i = nx // 2
        xb, xe = xs[:i], xs[i:]

        # Cost for the top-left part (first half of xs + ys)
        ll_b = _lcs_lens(xb, ys)
        # Cost for the bottom-right part (inverted second half of xs, ys)
        ll_e = _lcs_lens(xe[::-1], ys[::-1])
        # Invert the costs (of the inverted second half) to align it
        # with the costs of the first half
        ll_e_r = ll_e[::-1]

        # Choose the ys split based on cost (now we have "q")
        # Find the max is done with a loop to allow numba optimization
        cost = [x + y for x, y in zip(ll_b, ll_e_r)]
        max_so_far = 0
        k = 0
        for i, x in enumerate(cost):
            if x > max_so_far:
                max_so_far = x
                k = i

        yb, ye = ys[:k], ys[k:]

        # Solve each part of the split matrix
        return lcs(xb, yb) + lcs(xe, ye)
