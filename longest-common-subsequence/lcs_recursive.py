'''LCS with recursion.

This is the simplest recursive solution, with memoization. It is not an
efficient implementation. It is here to illustrate conceptually how to solve
the problem.

Even with memoization, this solution hits the number of recursive calls in the
Python environment for input strings around 10,000 characters.

Based on http://wordaligned.org/articles/longest-common-subsequence.
According to it, this solution is based on the CLRS book.
'''


def memoize(fn):
    '''Return a memoized version of the input function.

    The returned function caches the results of previous calls.
    Useful if a function call is expensive, and the function
    is called repeatedly with the same arguments.
    '''
    cache = dict()

    def wrapped(*v):
        key = tuple(v)  # tuples are hashable, and can be used as dict keys
        if key not in cache:
            cache[key] = fn(*v)
        return cache[key]
    return wrapped


@memoize
def lcs(xs, ys):
    '''Returns the longest subsequence common to xs and ys.'''
    @memoize
    def lcs_(i, j):
        if i and j:
            xe, ye = xs[i-1], ys[j-1]
            if xe == ye:
                return lcs_(i-1, j-1) + [xe]
            else:
                return max(lcs_(i, j), lcs_(i-1, j), key=len)
        else:
            return []
    return lcs_(len(xs), len(ys))
