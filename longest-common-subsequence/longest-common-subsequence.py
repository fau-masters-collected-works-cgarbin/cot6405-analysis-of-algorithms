'''Find the longest common sunsequence of two strings.

Examples:

     X = ABCBDAB
     Y = BDCABA
   LCS = BCBA or BDAB (there may be more than one)

     X = HUMAN
     Y = CHIMPANZEE
   LCS = HMAN

References:

  - http://wordaligned.org/articles/longest-common-subsequence
'''
from collections import defaultdict, namedtuple
from itertools import product
import random
import itertools
import functools


def lcs_recursive(xs, ys):
    '''Returns a longest common subsequence of xs and ys using the recursive
    approach.

    This is the simplest recursive solution, with no memoization. It is not an
    efficient implementation. It is here to illustrate conceptually how to
    solve the problem.

    Note that it returns one of the LCS, not all of them.

    Based on http://wordaligned.org/articles/longest-common-subsequence.
    According to it, this solution is based on the CLRS book.
    '''
    if xs and ys:
        # Split into the prefix and the last character
        *xb, xe = xs
        *yb, ye = ys
        if xe == ye:
            # If the last character is the same, it's part of the LCS
            # Add it to the LCS and continue with the prefix
            return lcs_recursive(xb, yb) + [xe]
        else:
            # Last character is not the same, so not part of the LCS
            # Continue with the largest prefix pair
            return max(lcs_recursive(xs, yb), lcs_recursive(xb, ys), key=len)
    else:
        return []


def lcs_dp(xs, ys):
    '''Returns a longest common subsequence of xs, ys.

    This is the bottom-up, non-recursive dynamic programming approach: first
    calculate the LCSes of all prefix pairs of xs and ys, from shortest to
    longest.

    This is done by filling out a grid with that has the information to "walk"
    through the pairss

    '''

    def lcs_grid(xs, ys):
        r'''Creates a grid for longest common subsequence calculations.

        Returns a grid where grid[(j, i)] is a pair (n, move) such that
        - n is the length of the LCS of prefixes xs[:i], ys[:j]
        - move is \, ^, <, or e, depending on whether the best move
        to (j, i) was diagonal, downwards, or rightwards, or None.

        Example:
        T  A  R  O  T
        A 0< 1\ 1< 1< 1<
        R 0< 1^ 2\ 2< 2<
        T 1\ 1< 2^ 2< 3\
        '''
        # The cell in each grid
        #   - length: the length of the move to make
        #   - move: the move (direction) for `length`
        Cell = namedtuple('Cell', ['length', 'move'])
        # The grid, modeled as a dictionary that returns "empty" if we didn't
        # set a move for a cell (to simplify corner cases)
        grid = defaultdict(lambda: Cell(0, 'e'))
        # All pairwise combinations of xs and ys and their indices
        # If xs='XYZ' and ys='ABC':
        #     ((0,'X'),(0,'A')), ((0,'X'),(1,'B')), ((0,'X'),(2,'C')),
        #     ((1,'Y'),(0,'A')), ((1,'Y'),(1,'B')), ((1,'Y'),(2,'C')),...
        sqs = product(enumerate(ys), enumerate(xs))
        # Loop through all those pairs and their indices to build the grid
        for (j, y), (i, x) in sqs:
            if x == y:
                # A match - move diagonally
                cell = Cell(grid[(j-1, i-1)].length + 1, '\\')
            else:
                left = grid[(j, i-1)].length
                over = grid[(j-1, i)].length
                if left < over:
                    cell = Cell(over, '^')
                else:
                    cell = Cell(left, '<')
            grid[(j, i)] = cell
        return grid

    # Create the LCS grid
    grid = lcs_grid(xs, ys)
    # Will accumulate the LCS, in reverse order
    lcs = list()
    # Walk back the grid, from the bottom-right to the top-left corner
    # (we know we reached the top-left when `iter` returns the sentinel `e`)
    i, j = len(xs) - 1, len(ys) - 1
    for move in iter(lambda: grid[(j, i)].move, 'e'):
        if move == '\\':
            # A match - accumulate and move diagonally (top, left)
            lcs.append(xs[i])
            i -= 1
            j -= 1
        elif move == '^':
            # Move up
            j -= 1
        elif move == '<':
            # Move left
            i -= 1

    lcs.reverse()
    return lcs


def lcs_hirschberg(xs, ys):
    '''Returns a longest common subsequence of xs, ys.

    This is Hirschberg’s Linear Space Algorithm. It requires a linear amount
    of memory, compared to the quadratic amount of memory used by the dynamic
    programming version.
    '''
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
        return []
    elif nx == 1:
        return [xs[0]] if xs[0] in ys else []
    else:
        i = nx // 2
        xb, xe = xs[:i], xs[i:]
        ll_b = lcs_lens(xb, ys)
        ll_e = lcs_lens(xe[::-1], ys[::-1])
        _, k = max((ll_b[j] + ll_e[ny - j], j)
                   for j in range(ny + 1))
        yb, ye = ys[:k], ys[k:]
        return lcs_hirschberg(xb, yb) + lcs_hirschberg(xe, ye)


def test(fn):
    '''Tests the LCS function `fn` with controlled input to check if the
    function is correct. '''

    def _test(fn, xs, ys, expected):
        result = fn(xs, ys)
        if result != expected:
            print('X: {}, Y: {} - expected {}, got {}'.format(
                xs, ys, expected, result))
            assert(False)

    # No match case
    _test(fn, 'ABC', 'XYZ', [])

    # All posible combinations of a short case
    _test(fn, 'AB', 'A', ['A'])
    _test(fn, 'AB', 'B', ['B'])
    _test(fn, 'ABC', 'A', ['A'])
    _test(fn, 'ABC', 'AB', ['A', 'B'])
    _test(fn, 'ABC', 'B', ['B'])
    _test(fn, 'ABC', 'BC', ['B', 'C'])
    _test(fn, 'ABC', 'C', ['C'])
    _test(fn, 'ABC', 'AC', ['A', 'C'])
    _test(fn, 'ABC', 'ABC', ['A', 'B', 'C'])

    # A bit longer case
    _test(fn, 'ABC', 'ABCD', ['A', 'B', 'C'])
    _test(fn, 'DABC', 'ABC', ['A', 'B', 'C'])
    _test(fn, 'DABC', 'ABCD', ['A', 'B', 'C'])

    # And a larger one
    _test(fn, 'HUMAN', 'CHIMPANZEE', ['H', 'M', 'A', 'N'])


test(lcs_recursive)
test(lcs_dp)
test(lcs_hirschberg)

print(lcs_recursive('ABCABC', 'ABC'))
print(lcs_dp('ABCABC', 'ABC'))
print(lcs_hirschberg('HUMAN', 'CHIMPANZEE'))


random.seed(42)


def random_dna_sequence(length):
    '''Generates a random DNA sequece of the given length.'''
    return ''.join(random.choice('ACTG') for _ in range(length))


dna1 = random_dna_sequence(1_000)
dna2 = random_dna_sequence(1_000)
print(lcs_hirschberg(dna1, dna2))
