import re
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
        # почему-то не ищет в корпусе top_words
        return math.log10(len(corpus)/sum([1.0 for i in corpus if word in i]))
    
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
            freqs = collections.defaultdict(lambda: 0)
            sentences = []
            for article in self.articles:
                sentences.append(sent_tokenize(article))
            flat_list = [item for sublist in sentences for item in sublist]
            for sent in flat_list:
                for ngram in self.make_ngrams(sent.replace('\n', '').lower()):
                    if len(ngram)>2:
                        freqs[ngram] += 1
            if use_idf is True:
                for ngram in freqs:
                    freqs[ngram] = freqs[ngram]*self.compute_idf(ngram, sentences)
                for ngram in sorted(freqs, key=lambda n: freqs[n], reverse=True):
                    list_of_3grams_in_descending_order_by_freq.append('"{}" — {}'.format(ngram, freqs[ngram]))
            else:       
                for ngram in sorted(freqs, key=lambda n: freqs[n], reverse=True):
                    list_of_3grams_in_descending_order_by_freq.append('"{}" — {}'.format(ngram, freqs[ngram]))
            return list_of_3grams_in_descending_order_by_freq[:n]
            
    def get_top_words(self, n, use_idf=False):
        freqs = collections.defaultdict(lambda: 0)
        list_of_top_words_in_descending_order_by_freq = []
        stop_words = ['on', 'in', 'at', 'near', 'over', 'under', 
                      'between', 'to', 'from','into', 'out', 'of', 
                      'off', 'with', 'since', 'by', 'as', 'for',
                      'on', 'a', 'the', 'an']
        tokens = regexp_tokenize(' '.join(self.articles), r'[\w]*', gaps=False)        
        draft = ' '.join(tokens)
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
                #freqs[element] = freqs[element]*self.compute_idf(str(element), corpus = self.articles)
                freqs[element] = self.compute_idf(str(element), corpus = self.articles)
            for element in sorted(freqs, key=lambda n: freqs[n], reverse=True):
                list_of_top_words_in_descending_order_by_freq.append('"{}" — {}'.format(element, freqs[element]))
            return list_of_top_words_in_descending_order_by_freq   
        else:
            for element in sorted(freqs, key=lambda n: freqs[n], reverse=True):
                list_of_top_words_in_descending_order_by_freq.append('"{}" — {}'.format(element, freqs[element]))
            return list_of_top_words_in_descending_order_by_freq[:n]

class Experiment(TextStatistics, WikiParser):
    def __init__(self):
        self.articles = 'Natural language processing'
    def show_result(self):
        corpus = self.get_articles(self.articles)
        freq = TextStatistics(corpus)
        trigram = freq.get_top_3grams(20)
        word_top = freq.get_top_words(20)
        result = 'Топ-20 3-грамм по корпусу текстов:\n%s\n\nТоп-20 слов по корпусу текстов:\n%s\n\n'
        print(result % ('\n'.join(trigram),'\n'.join(word_top)))
##use_idf=False        
##Топ-20 3-грамм по корпусу текстов:
##" th" — 45453
##"the" — 45183
##"he " — 35084
##"ion" — 24991
##" in" — 24346
##"ing" — 23431
##" of" — 23249
##"of " — 22270
##"ed " — 22060
##"tio" — 21973
##" an" — 21730
##"and" — 19394
##"nd " — 18806
##"on " — 17919
##"ati" — 17812
##"ng " — 17310
##" co" — 16969
##"in " — 16810
##"al " — 15860
##"ent" — 14666
##
##Топ-20 слов по корпусу текстов:
##"and" — 16260
##"is" — 8669
##"that" — 4880
##"are" — 4327
##"language" — 3822
##"or" — 3767
##"s" — 3466
##"be" — 3390
##"it" — 2724
##"this" — 2371
##"which" — 2182
##"can" — 1984
##"not" — 1937
##"was" — 1775
##"speech" — 1759
##"such" — 1746
##"i" — 1727
##"english" — 1712
##"retrieved" — 1710
##"p" — 1708


class TextStatistics_TestCase(unittest.TestCase):
    def test_trigram_zero(self):
        stat = TextStatistics(['I like Python', 'But I dont know', 'How to write tests'])
        self.assertEqual(("No ngrams needed"), stat.get_top_3grams(0))
    def test_trigram_negative(self):
        stat = TextStatistics(['I like Python', 'But I dont know', 'How to write tests'])
        self.assertEqual(('Operation is not possible'), stat.get_top_3grams(-10))
    def test_trigram_n(self):
        stat = TextStatistics(['I like Python', 'But I dont know', 'How to write tests'])
        self.assertEqual(['"i l" — 1', '" li" — 1', '"lik" — 1', '"ike" — 1', '"ke " — 1', '"e p" — 1', '" py" — 1', '"pyt" — 1', '"yth" — 1', '"tho" — 1', '"hon" — 1', '"but" — 1', '"ut " — 1', '"t i" — 1', '" i " — 1', '"i d" — 1', '" do" — 1', '"don" — 1', '"ont" — 1', '"nt " — 1']), stat.get_top_3grams(20))   
if __name__ == "__main__":
    unittest.main()
