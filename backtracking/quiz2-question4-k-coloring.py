'''
Solves the k-colorig problem with backtracking: given a graph and a number of
colors (k), checks if the vertices in the graph can be colored with that
number of colors (k), such that no connected vertices have the same color.

From http://stephanie-w.github.io/brainscribble/m-coloring-problem.html, plus
correction for code that stops the recurring function (see comment in the
code).
'''


def is_safe(n, graph, colors, c):
    # Iterate trough adjacent vertices
    # and check if the vertex color is different from c
    for i in range(n):
        if graph[n][i] and c == colors[i]:
            return False
    return True


def graphColoringUtil(graph, color_nb, colors, n):
    print('\ngraphColoringUtil color_nb={} colors={}, n={}'.format(
        color_nb, colors, n))
    # Check if all vertices are assigned a color
    # NOTE: different from the original code. I think the stopping condition
    # in the original code was incorrect.
    if n >= vertex_nb:
        print('   All vertices are assigned a color')
        return True

    # Trying differents color for the vertex n
    for c in range(1, color_nb+1):
        print('   Trying color {} for n={}'.format(c, n))
        # Check if assignment of color c to n is possible
        if is_safe(n, graph, colors, c):
            print('      Color {} is safe'.format(c))
            # Assign color c to n
            colors[n] = c
            # Recursively assign colors to the rest of the vertices
            print('Recursive call for n+1={}'.format(n+1))
            if graphColoringUtil(graph, color_nb, colors, n+1):
                print('      Returning true for n={}'.format(n))
                return True
            # If there is no solution, remove color (BACKTRACK)
            # NOTE: this does not seem to affect the code itself, just the
            # data structure (by not leaving behind a color that didn't work),
            # this colors[] has the partial solution that worked up to that
            # point
            print('      Remove color for n={} - backtrack'.format(n))
            colors[n] = 0

    print('      Returning FALSE for n={}'.format(n))
    return False


#    (3)---(2)
#     |   / |
#     |  /  |
#     | /   |
#    (0)---(1)
# graph = [
#     [0, 1, 1, 1],
#     [1, 0, 1, 0],
#     [1, 1, 0, 1],
#     [1, 0, 1, 0],
# ]
# vertex_nb = 4


graph = [
    [0, 1, 1, 1, 1, 0],
    [1, 0, 1, 1, 0, 1],
    [1, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 1],
    [1, 0, 1, 1, 0, 1],
    [0, 1, 1, 1, 1, 0],
]
vertex_nb = 6

# nb of colors
# set to 2 to make it fail in most graphs, to see backtracking taking place
color_nb = 2
# Initiate vertex colors
colors = [0] * vertex_nb

# beginning with vertex 0
if graphColoringUtil(graph, color_nb, colors, 0):
    print(colors)
else:
    print("No solutions")
