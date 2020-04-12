'''Run the experiments and collect metrics.
'''
from collections import namedtuple
import random
import lcs_brute_force
import lcs_dynamic_programming
import lcs_dynamic_programming_v2
import lcs_hirschberg
import lcs_recursive
import lcs_test
import lcs_utils
import time

# To ensure repeatability
random.seed(42)

# IMPORTANT: make sure the algorithms work before using them
lcs_test.test()

dna = lcs_utils.random_dna_sequence(1_000)
dna_strand = lcs_utils.random_dna_sequence(100)

Algorithm = namedtuple('Algorithm', ['function', 'description'])
algorithms = [
    Algorithm(lcs_brute_force.lcs, 'Brute force'),
    Algorithm(lcs_dynamic_programming_v2.lcs, 'Dynamic programming'),
    Algorithm(lcs_hirschberg.lcs, 'Hirschberg'),
]

for alg in algorithms:
    start = time.process_time()

    alg.function(dna, dna_strand)
    total_time = time.process_time() - start

    print('{:>20}: {:.3f}'.format(alg.description, total_time))
