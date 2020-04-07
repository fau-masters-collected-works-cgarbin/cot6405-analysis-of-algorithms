'''LCS Hirschberg Linear Space.

It requires a linear amount of memory, compared to the quadratic amount of
memory used by the dynamic programming version.

Code based on http://wordaligned.org/articles/longest-common-subsequence.

Algorithm reference:
https://www.cs.princeton.edu/~wayne/kleinberg-tardos/pdf/06DynamicProgrammingII.pdf
'''
import itertools


def lcs(xs, ys):
    '''Returns a longest common subsequence of xs, ys.'''
    def lcs_lens(xs, ys):
        curr = list(itertools.repeat(0, 1 + len(ys)))
        for x in xs:
            prev = list(curr)
            for i, y in enumerate(ys):
                if x == y:
                    curr[i + 1] = prev[i] + 1
                else:
                    curr[i + 1] = max(curr[i], prev[i + 1])
        return curr

    nx, ny = len(xs), len(ys)
    if nx == 0:
        # Empty input - got to the end of the sequence
        return []
    elif nx == 1:
        # Only one character in the sequence
        # If it is in the other sequence, it's part of the LCS
        return [xs[0]] if xs[0] in ys else []
    else:
        # More than one character - split xs into two halves
        i = nx // 2
        xb, xe = xs[:i], xs[i:]

        # Find the node to split the xs/ys matrix and split it into two
        ll_b = lcs_lens(xb, ys)
        ll_e = lcs_lens(xe[::-1], ys[::-1])
        _, k = max((ll_b[j] + ll_e[ny - j], j)
                   for j in range(ny + 1))
        yb, ye = ys[:k], ys[k:]

        # Solve each part of the split matrix
        return lcs(xb, yb) + lcs(xe, ye)
