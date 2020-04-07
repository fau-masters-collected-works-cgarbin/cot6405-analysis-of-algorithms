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
import random
import lcs_dynamic_programming
import lcs_hirschberg
import lcs_recursive
import lcs_test

lcs_test.test()


print(lcs_recursive.lcs('ABCABC', 'ABC'))
print(lcs_dynamic_programming.lcs('ABCABC', 'ABC'))
print(lcs_hirschberg.lcs('HUMAN', 'CHIMPANZEE'))

# To ensure repeteability
random.seed(42)


def random_dna_sequence(length):
    '''Generates a random DNA sequence of the given length.'''
    return ''.join(random.choice('ACTG') for _ in range(length))


dna1 = random_dna_sequence(1_000)
dna2 = random_dna_sequence(1_000)
print(lcs_hirschberg.lcs(dna1, dna2))
