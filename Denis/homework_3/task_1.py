import re
from unittest import *
import unittest
import itertools
import math
import collections
from itertools import islice, tee
from collections import Counter
from collections import OrderedDict
from pattern.web import Wikipedia, plaintext
from nltk.collocations import *
from nltk import regexp_tokenize
from nltk.tokenize import sent_tokenize

class WikiParser:
    def __init__(self):
        pass
    
    def text_cleaning(self, article):
        text = article.plaintext()
        text = text.lower()
        final = re.sub('[\s]{1,25}', ' ', text)
        return final
    
    def get_articles(self, start):
        arr = []
        wiki = Wikipedia(language="en")
        article = wiki.article(start)
        arr.append(self.text_cleaning(article))
        for title in article.links:
            article = wiki.article(title)
            arr.append(self.text_cleaning(article))
        return arr

class TextStatistics:
    def __init__(self, articles):
        self.articles = articles

    def compute_idf(self, word, corpus):
        return math.log(len(corpus)/sum([1.0 for i in corpus if word in i]))
    
    def make_ngrams(self,text):
        N = 3 # задаем длину n-граммы
        ngrams = zip(*(islice(seq, index, None) for index, seq in enumerate(tee(text, N))))
        ngrams = [''.join(x) for x in ngrams]
        return ngrams

    def get_top_3grams(self,n,use_idf=False):
        if n == 0:
            return "No ngrams needed"
        elif n < 0:
            return 'Operation is not possible'
        elif n>0:
            list_of_3grams_in_descending_order_by_freq = []
            list_of_their_corresponding_freq = []
            freqs = collections.defaultdict(lambda: 0)
            list_sent = []
            for article in self.articles:
                sentences = article.split('.')
                list_sent = [x for x in sentences]
            for sent in list_sent:
                for ngram in self.make_ngrams(sent):
                    if len(ngram)>2:
                        freqs[ngram] += 1
            if use_idf is True:
                for ngram in freqs:
                    freqs[ngram] = freqs[ngram]*self.compute_idf(ngram, list_sent)
                for ngram in sorted(freqs, key=lambda n: freqs[n], reverse=True):
                    list_of_3grams_in_descending_order_by_freq.append(ngram)
                    list_of_their_corresponding_freq.append(freqs[ngram])  
            else:       
                for ngram in sorted(freqs, key=lambda n: freqs[n], reverse=True):
                    list_of_3grams_in_descending_order_by_freq.append(ngram)
                    list_of_their_corresponding_freq.append(freqs[ngram])  
            return (list_of_3grams_in_descending_order_by_freq[:n], list_of_their_corresponding_freq[:n])
            
    def get_top_words(self, n, use_idf=False):
        list_of_top_words_in_descending_order_by_freq = []
        list_of_their_corresponding_freq = []
        freqs = collections.defaultdict(lambda: 0)
        for_idf = collections.defaultdict(lambda: 0)
        list_of_top_words_in_descending_order_by_freq = []
        stop_words = ['on', 'in', 'at', 'near', 'over', 'under', 
                      'between', 'to', 'from','into', 'out', 'of', 
                      'off', 'with', 'since', 'by', 'as', 'for',
                      'on', 'a', 'the', 'an']
        tokens = regexp_tokenize(' '.join(self.articles), r'[\w]*', gaps=False)        
        draft = ' '.join(tokens)
        corpus_size = len(self.articles)
        remove_numbers = re.sub('[\d]{1,4}', '', draft)
        corpus = remove_numbers.split()
        new_corpus = []
        for token in corpus:
            if token not in stop_words:
                new_corpus.append(token)
        for token in new_corpus:
            if token != '':
                freqs[token] += 1
        if use_idf is True:
            for element in freqs:
                for article in self.articles:
                    if element in article:
                        for_idf[element] += 1
            for entity in for_idf:
                for_idf[entity] = for_idf[entity]*(math.log(corpus_size/for_idf[entity]))
                #for_idf[entity] = for_idf[entity] *(math.log(corpus_size/for_idf[entity]))
            for entity in sorted(for_idf, key=lambda n: for_idf[n], reverse=True):
                list_of_top_words_in_descending_order_by_freq.append(entity)
                list_of_their_corresponding_freq.append(for_idf[entity])
        else:       
            for word in sorted(freqs, key=lambda n: freqs[n], reverse=True):
                list_of_top_words_in_descending_order_by_freq.append(word)
                list_of_their_corresponding_freq.append(freqs[word])
                    
        return (list_of_top_words_in_descending_order_by_freq[:n], list_of_their_corresponding_freq[:n])

class Experiment(TextStatistics, WikiParser):
    def __init__(self):
        self.articles = 'Natural language processing'
    def show_result(self):
        corpus = self.get_articles(self.articles)
        freq = TextStatistics(corpus)
        trigram = freq.get_top_3grams(20, use_idf=True)
        print('Топ-20 3-грамм по корпусу текстов с idf:\n')
        for ngram in zip(*trigram):
            output = '"{}" — {}'.format(ngram[0], ngram[1])
            print(output)
        word_top = freq.get_top_words(20, use_idf=True)
        print('\nТоп-20 слов по корпусу текстов с idf:\n')
        for top in zip(*word_top):
            output = '"{}" — {}'.format(top[0], top[1])
            print(output)


##Топ-20 3-грамм по корпусу текстов с idf:
##
##" th" — 558.6318324755408
##"the" — 521.4156209527775
##"he " — 475.01871640208003
##" in" — 367.9124357495185
##" we" — 348.5047852099454
##"e w" — 344.1751865421481
##"ed " — 333.19983066732317
##"web" — 333.18995781923394
##" an" — 316.27863805308954
##"er " — 308.55846952879256
##" re" — 307.2905176722422
##"ing" — 301.73455149733536
##"and" — 295.3643388496807
##"ent" — 292.1993853551956
##"nd " — 291.28813190084026
##"eb " — 288.0433890581565
##"ion" — 283.73731415713166
##" of" — 278.8186073897319
##"of " — 271.91344276005185
##" to" — 265.6202234633475
##
##Топ-20 слов по корпусу текстов с idf:
##
##"contains" — 68.05767215335084
##"identify" — 68.05767215335084
##"cannot" — 68.05767215335084
##"derived" — 68.05767215335084
##"relationship" — 68.05767215335084
##"referred" — 68.05767215335084
##"ii" — 68.05767215335084
##"situ" — 68.05767215335084
##"aspect" — 68.05767215335084
##"down" — 68.05767215335084
##"meet" — 68.05767215335084
##"june" — 68.05767215335084
##"artin" — 68.05767215335084
##"abu" — 68.05767215335084
##"ots" — 68.05767215335084
##"frequent" — 68.05767215335084
##"fas" — 68.05767215335084
##"pass" — 68.05767215335084
##"fram" — 68.05767215335084
##"elle" — 68.05767215335084

class TextStatistics_TestCase(unittest.TestCase):
    def test_trigram_zero(self):
        stat = TextStatistics(['I like Python. Hello, world!', 'But I dont know', 'How to write tests'])
        self.assertEqual(stat.get_top_3grams(0),("No ngrams needed"))
    def test_trigram_negative(self):
        stat = TextStatistics(['I like Python. Hello, world!', 'But I dont know', 'How to write tests'])
        self.assertEqual(stat.get_top_3grams(-10), ('Operation is not possible'))
    def test_trigram_n(self):
        stat = TextStatistics(['I like Python. Hello, world!', 'But I dont know', 'How to write tests'])
        result = ['How', 'ow ', 'w t', ' to', 'to ', 'o w', ' wr', 'wri', 'rit', 'ite', 'te ', 'e t', ' te', 'tes', 'est', 'sts']
        self.assertListEqual(stat.get_top_3grams(20)[0], result)  
    def test_except(self):
        stat = TextStatistics(['I like Python. Hello, world!', 'But I dont know', 'How to write tests'])
        try:
            stat.get_top_3grams(0)
        except YourException as ex:
            self.assertTrue(True)
        else:
            self.assertFalse(False)
            
#assert almost Equal
case = TextStatistics_TestCase()
suite = TestLoader().loadTestsFromModule(case)
TextTestRunner().run(suite)
