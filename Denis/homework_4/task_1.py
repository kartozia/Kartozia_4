import unittest
from unittest import *

def poly_hash(s, x=31, p=997):
    h = 0
    for j in range(len(s)-1, -1, -1):
        h = (h * x + ord(s[j]) + p) % p
    return h

def search_rabin_multi(text, patterns, x=31, p=997):
    indices = []
    checked_patterns = []
    
    if len(patterns)== 0:
        return 'Search cannot be completed, an empty string was given'
    
    for pattern in patterns:
        if type(pattern) is str:
            checked_patterns.append(pattern)
        else:
            print(str(pattern) + ' is not a string and was excluded from the search')
            
    for pattern in checked_patterns:
        pattern_indices = []
            
        if len(text) < len(pattern):
            indices.append([])
    
    # precompute hashes
        precomputed = [0] * (len(text) - len(pattern) + 1)
        precomputed[-1] = poly_hash(text[-len(pattern):], x, p)
    
        factor = 1
        for i in range(len(pattern)):
            factor = (factor*x + p) % p
        
        for i in range(len(text) - len(pattern)-1, -1, -1):
            precomputed[i] = (precomputed[i+1] * x + ord(text[i]) - factor * ord(text[i+len(pattern)]) + p) % p
    
        pattern_hash = poly_hash(pattern, x, p)
        
        for i in range(len(precomputed)):
            if precomputed[i] == pattern_hash:
                if text[i: i + len(pattern)] == pattern:
                    pattern_indices.append(i)
        
        indices.append(pattern_indices)       
    return indices

class search_rabin_multi_TestCase(unittest.TestCase):
    def test_result(self):
        text = 'Lets see if the algorithm works'
        patterns = ['th', 'if', 'or', 3]
        self.assertEqual(search_rabin_multi(text,patterns), [[12, 22], [9], [19, 27]])
    def test_emptylist(self):
        text = 'Lets see if the algorithm works'
        patterns = []
        self.assertEqual(search_rabin_multi(text,patterns), 'Search cannot be completed, an empty string was given')
    def test_notstrings(self):
        text = 'Lets see if the algorithm works'
        patterns = [list('p'), 3]
        self.assertEqual(search_rabin_multi(text,patterns), [])
    
        
case = search_rabin_multi_TestCase()
suite = TestLoader().loadTestsFromModule(case)
TextTestRunner().run(suite)
