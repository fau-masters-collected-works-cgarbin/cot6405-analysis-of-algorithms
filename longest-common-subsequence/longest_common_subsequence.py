'''Find the longest common sunsequence of two strings.

Examples:

     X = ABCBDAB
     Y = BDCABA
   LCS = BCBA or BDAB (there may be more than one)

     X = HUMAN
     Y = CHIMPANZEE
   LCS = HMAN

References:

  - https://www.cs.princeton.edu/~wayne/kleinberg-tardos/pdf/06DynamicProgrammingII.pdf: # noqa
    lecture on the topic, using slides from Algorithm Design, Kleinber and
    Tardos.
'''
import random
import lcs_brute_force
import lcs_dynamic_programming
import lcs_dynamic_programming_v2
import lcs_hirschberg
import lcs_recursive
import lcs_test

# To ensure repeteability
random.seed(42)

# Make sure the algorithms work
# lcs_test._test_subseqence_match()
lcs_test.test()
