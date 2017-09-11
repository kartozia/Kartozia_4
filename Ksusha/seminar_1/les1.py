from collections import defaultdict
import nltk
from nltk import word_tokenize

for root, dirs, files in os.walk('.'):
    for i in files:
        if i[-4:] == '.txt':
            file = open(root + '/' + i, 'r', encoding='utf-8')
            f = file.read()                  
file.close()
#with open('text1.txt', 'r') as f:
doc1 = open('text1.txt', 'r', encoding="utf-8")
doc2 = open('text2.txt', 'r', encoding="utf-8")
doc3 = open('text3.txt', 'r', encoding="utf-8")

def token(file):
    text = file.read()
    arr = word_tokenize(text)
    return arr

file1 = token(doc1)
file2 = token(doc2)
file3 = token(doc3)

list_of_docs = [doc1, doc2, doc3]    
list_of_tokens = [file1, file2, file3]


def reversed_index(list_of_tokens):
    reverse = defaultdict(set)
    for i,doc in enumerate(list_of_tokens):
        for token in doc:
            reverse[token].add(i)
    return reverse
print(reversed_index(list_of_tokens))
doc1.close()
doc2.close()
doc3.close()
