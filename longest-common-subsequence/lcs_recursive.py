'''LCS with recursion.

This is the simplest recursive solution, with no memoization. It is not an
efficient implementation. It is here to illustrate conceptually how to solve
the problem.

Note that it returns one of the LCS, not all of them.

Based on http://wordaligned.org/articles/longest-common-subsequence.
According to it, this solution is based on the CLRS book.
'''


def lcs(xs, ys):
    '''Returns a longest common subsequence of xs and ys.'''
    if xs and ys:
        # Split into the prefix and the last character
        *xb, xe = xs
        *yb, ye = ys
        if xe == ye:
            # If the last character is the same, it's part of the LCS
            # Add it to the LCS and continue with the prefix
            return lcs(xb, yb) + [xe]
        else:
            # Last character is not the same, so not part of the LCS
            # Continue with the largest prefix pair
            return max(lcs(xs, yb), lcs(xb, ys), key=len)
    else:
        return []
