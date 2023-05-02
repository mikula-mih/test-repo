from enum import IntEnum
from typing import Tuple, List

Nucleotide: IntEnum = IntEnum('Nucleotide', ('A', 'C', 'G', 'T'))

Codon = Tuple[Nucleotide, Nucleotide, Nucleotide] # type alias for codons
Gene = List[Codon] # type alias for genes

gene_str: str = "ACGTGGCTCTCTAACGTACGTACGTACGGGGTTTATATATACCCTAGGACTCCCTTT"

def string_to_gene(s: str) -> Gene:
    gene: Gene = []
    for i in range(0, len(s), 3):
        if (i + 2) >= len(s):
            return gene
        # initialize codon out of 3 nucleotides
        codon: Codon = (
            Nucleotide[s[i]],
            Nucleotide[s[i + 1]],
            Nucleotide[s[i + 2]]
        )
        gene.append(codon) # add codon to gene
    return gene


my_gene: Gene = string_to_gene(gene_str)

# Linear Search: O(n) complexity
# Python built-in sequence type(list, tuple, range) all implement __contains__()
# method, `in` operator for searching;
def linear_contains(gene: Gene, key_codon: Codon) -> bool:
    for codon in gene:
        if codon == key_codon:
            return True
    return False
# Binary search
# worst-case runtime of O(lg n).
# sorting takes O(n lg n) time for the best sorting algorithms;
def binary_contains(gene: Gene, key_codon: Codon) -> bool:
    low: int = 0
    high: int = len(gene) - 1
    while low <= high:
        mid: int = (low + high) // 2
        if gene[mid] < key_codon:
            low = mid + 1
        elif gene[mid] > key_codon:
            high = mid - 1
        else:
            return True
    return False
# the Python standard library’s bisect module:
# https://docs.python.org/3/library/bisect.html

my_sorted_gene: Gene = sorted(my_gene)

print(binary_contains(my_sorted_gene,
    (Nucleotide['A'], Nucleotide['C'], Nucleotide['G'])
)) # True
print(binary_contains(my_sorted_gene,
    (Nucleotide['G'], Nucleotide['A'], Nucleotide['T'])
)) # False
