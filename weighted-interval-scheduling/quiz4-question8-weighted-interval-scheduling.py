'''
Calculates the p(i) values for a scheduling problem.

p(i) is the first non-overlapping request to the left of the current request.
'''


def find_p(s, f):
    assert (len(s) == len(f))
    print('--------------------------')

    # visualize the requests
    for i, p in enumerate(zip(s, f)):
        print('{}: {}, {}'.format(i, p[0], p[1]))
    for x, p in enumerate(zip(s, f)):
        i, j = p
        print('{}: {}{}'.format(x, i * ' ', (j - i + 1) * 'X'))

    # Calculate p(i)
    n = len(s)
    p = [0] * n
    for i in range(n - 1, 0 - 1, -1):
        p[i] = -1  # assume can't find non-overlapping interval
        print('i = {}'.format(i))
        for j in range(i - 1, 0-1, -1):
            print('   j={} f[{}]={}, s[{}]={} non-overlapping={}'.format(
                j, j, f[j], i, s[i], f[j] <= s[i]))
            if f[j] <= s[i]:
                p[i] = j
                break
    print(p)


# Start and finish times
s = [1, 2, 6, 3, 9, 10]
f = [3, 7, 8, 10, 12, 13]
find_p(s, f)


s = [1, 2, 3]
f = [2, 3, 4]
find_p(s, f)

s = [1, 3, 5]
f = [2, 4, 6]
find_p(s, f)

s = [1, 3, 2]
f = [5, 8, 7]
find_p(s, f)
