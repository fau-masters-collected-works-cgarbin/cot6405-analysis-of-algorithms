'''LCS dynamic programming: solve smaller problems only once, combine the
subproblems to build the solution.

This is the bottom-up, non-recursive dynamic programming approach: first
calculate the LCSes of all prefix pairs of xs and ys, from shortest to
longest.

This is done by filling out a grid with that has the information to "walk"
through the pairs.
'''
from collections import defaultdict, namedtuple
from itertools import product


def _lcs_grid(xs, ys):
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


def lcs(xs, ys):
    '''Returns a longest common subsequence of xs, ys.'''
    grid = _lcs_grid(xs, ys)

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
