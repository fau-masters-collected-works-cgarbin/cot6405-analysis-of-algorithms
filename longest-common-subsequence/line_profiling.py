'''Line profiling driver code.

Use this file to line-profile other pieces of code.

- Install line_profiler
- import line_profile in the module that has the function to profile
- Add @profile to the function declaration
- Run `kernprof --view -l profiling.py`

See https://github.com/pyutils/line_profiler.
'''
import random
import lcs_utils
import lcs_dynamic_programming_v2
import lcs_test

# IMPORTANT
# Make sure we didn't break the code when optimzing it
# Uncomment and run once so the tests are not profiled
# lcs_test.test()

random.seed(42)

dna = lcs_utils.random_dna_sequence(10_000)
dna_strand = lcs_utils.random_dna_sequence(1_000)

# Change this line to call the function to bre profiled
# Remember to import line_profiler in that file and add @profile
lcs_dynamic_programming_v2.lcs(dna, dna_strand)
