'''LCS dynamic programming: solve smaller problems only once, combine the
subproblems to build the solution.

This is the bottom-up, non-recursive dynamic programming approach: first
calculate the LCSes of all prefix pairs of xs and ys, from shortest to
longest.

This is done by filling out a grid with that has the information to "walk"
through the pairs.

Code based on http://wordaligned.org/articles/longest-common-subsequence,
adapted to use a matrix and combine length and move into one integer to
save memory. The original code is extremely slow for anything over 1,000
characters.

This version also uses NumPy for the arrays to save even more memory. The
version that uses Python arrays runs out of memory with large strings (failed
with 1,000,000 + 100,000 strings).

IMPORTANT: this version is faster only whne used wiht Numba. Without Numba it
is much slower than the version that uses Python arrays. This is caused by
the conversion of NumPy internal representation to Python objects while
performing loops. Numba seems to avoid it.

Algorithm reference:
https://www.cs.princeton.edu/~wayne/kleinberg-tardos/pdf/06DynamicProgrammingII.pdf
'''
import numpy as np
from numba import njit


# To save memory and speed-up the code, the move is stored
# in the upper bits of a cell and the length in the lower bits
MOVE_START = 25  # leaves 24 bits for the length
MOVE_DIAGONAL = 1 << (MOVE_START)
MOVE_UP = 1 << (MOVE_START+1)
MOVE_LEFT = 1 << (MOVE_START+2)
EXCLUDE_LENGTH = (MOVE_DIAGONAL + MOVE_UP + MOVE_LEFT)
EXCLUDE_MOVE = ~EXCLUDE_LENGTH


@njit
def _lcs_grid(xs, ys):
    '''Creates a grid for longest common subsequence calculations.

    Returns a grid where grid[i][j] is a pair (n, move) such that
    - n is the length of the LCS of prefixes xs[:i], ys[:j]
    - move is diagonal, up, left, encoded in the top-most bits

    Example:
      T      A      R      O      T
    A 0|left 1|diag 1|left 1|left 1|left
    R 0|left 1|up   2|diag 2|left 2|left
    T 1|diag 1|left 2|up   2|left 3|diag
    '''

    # A grid of xs columns and ys rows
    # Note that we start with 1, not the traditional 0 because the first
    # column and first row are used as sentinels to avoid special cases
    # in the code (sentinel = length is zero, no move)
    grid = np.zeros(shape=(len(xs)+1, len(ys)+1), dtype=np.int32)

    for i in range(1, len(xs) + 1):
        x = xs[i-1]  # Remember that we use index 0 as a sentinel
        for j in range(1, len(ys)+1):
            y = ys[j-1]
            if x == y:
                # A match - move diagonally
                length = grid[i-1][js] & EXCLUDE_MOVE
                grid[i][j] = (length + 1) | MOVE_DIAGONAL
            else:
                left_length = grid[i][j-1] & EXCLUDE_MOVE
                above_length = grid[i-1][j] & EXCLUDE_MOVE
                if left_length < above_length:
                    grid[i][j] = above_length | MOVE_UP
                else:
                    grid[i][j] = left_length | MOVE_LEFT
    return grid


@njit
def lcs(xs, ys):
    '''Returns a longest common subsequence of xs, ys.'''
    grid = _lcs_grid(xs, ys)

    # Will accumulate the LCS, in reverse order
    lcs = list()

    # Start that bottom-right corner
    i = len(xs)
    j = len(ys)

    # Follow the moves to the top
    while i > 0 and j > 0:
        move = grid[i][j] & EXCLUDE_LENGTH
        if move == MOVE_DIAGONAL:
            # A match - accumulate and move diagonally (top, left)
            lcs.append(xs[i-1])  # Remeber that 0 is a sentinel
            i -= 1
            j -= 1
        elif move == MOVE_UP:
            i -= 1
        elif move == MOVE_LEFT:
            j -= 1

    lcs.reverse()
    return lcs
