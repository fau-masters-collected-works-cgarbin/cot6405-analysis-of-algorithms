'''LCS Hirschberg Linear Space.

It requires a linear amount of memory, compared to the quadratic amount of
memory used by the dynamic programming version.

Code based on http://wordaligned.org/articles/longest-common-subsequence.

Algorithm reference:
https://www.cs.princeton.edu/~wayne/kleinberg-tardos/pdf/06DynamicProgrammingII.pdf
'''
import itertools


def _lcs_lens(xs, ys):
    '''Calculates the cost for the sequences.

    This cost is used to decide where to split the sequences.'''
    # Start with zero costs
    curr = list(itertools.repeat(0, 1 + len(ys)))
    # Go through the sequences and adjust costs
    for x in xs:
        prev = list(curr)
        for i, y in enumerate(ys):
            if x == y:
                curr[i + 1] = prev[i] + 1
            else:
                curr[i + 1] = max(curr[i], prev[i + 1])
    return curr


def lcs(xs, ys):
    '''Returns a longest common subsequence of xs, ys.'''
    nx, ny = len(xs), len(ys)
    if nx == 0:
        # Empty input - got to the end of the sequence
        return []
    elif nx == 1:
        # Only one character in the sequence
        # If it is in the other sequence, it's part of the LCS
        return [xs[0]] if xs[0] in ys else []
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

        # Choose the ys split based on cost (now we have "q")
        _, k = max((ll_b[j] + ll_e[ny - j], j)
                   for j in range(ny + 1))
        yb, ye = ys[:k], ys[k:]

        # Solve each part of the split matrix
        return lcs(xb, yb) + lcs(xe, ye)
