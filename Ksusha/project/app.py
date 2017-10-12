from collections import defaultdict
import nltk
import os
import re
import json
from pymystem3 import Mystem
from nltk import word_tokenize
import string
from nltk.corpus import stopwords
from flask import Flask, request, render_template
from math import log

def lemmatize_me(text):
    m = Mystem()
    lemma = m.lemmatize(text)

    #let's delete punctuation symbols
    lemma = [i for i in lemma if ( i not in string.punctuation )]

    #deleting stop_words
    stop_words = stopwords.words('russian')
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '–', 'к', 'на', '\n', '\t', ' '])
    lemma = [i.strip() for i in lemma if ( i not in stop_words )]

    #cleaning words
    #tokens = [i.replace("«", "").replace("»", "") for i in tokens]

    return lemma

def compute_tf(word, text):
    tf_text = 0
    for i in text:
        if i == word:
            tf_text += 1
    tf_text = tf_text/float(len(text))
    return tf_text

def score_BM25(n, qf, N, dl, avdl):
    K = compute_K(dl, avdl)
    IDF = log((N - n + 0.5) / (n + 0.5))
    frac = ((k1 + 1) * qf) / (K + qf)
    return IDF * frac
#N=24, avdl=2791.125, k1=2.0, b=0,75
k1 = 2.0
b = 0.75

def compute_K(dl, avdl):
    return k1 * ((1-b) + b * (float(dl)/float(avdl)))

#query = 'из Москвы в Салехард'
#print(search(query,data))

def extract_info(text, key):
    url = re.search('@url (.+)', text).group(1)
    title = re.search('@ti (.+)', text).group(1)
    content = text.split("html",1)[1] 
    dl = len(content.split())
    qf = compute_tf(key, lemmatize_me(content))
    return url, title, content, dl, qf

def metrics(result, N='24', avdl='289.2083333333333', k1='2.0', b='0.75'):
    output = {}
    for key, value in result.items():
        n = len(value)
        for file in value:
            f = open('./text/' + file, 'r', encoding='utf-8')
            text = f.read()
            url, title, content, dl, qf = extract_info(text, key)
            metric = score_BM25(n, qf, N, dl, avdl)
            link = '<a href="' + url + '">' + title + '</a>'
            if file not in output:
                output[link] = metric
            else:
                output[link] += metric
            f.close()

    return sorted(output, key=output.get, reverse=True)[:10]        
    #for key in sorted(output, key=output.get, reverse=True)[:10]:
 #       link = '{} — {}'.format(key, output[key])
        #print(display(HTML(str(link))))
     #   print(key,value)

def search(query):
    json_data=open('reversed_index.json', 'r', encoding='utf-8')
    j = json_data.read()
    data = json.loads(j)
    lem_query = lemmatize_me(query)
    result = defaultdict(set)
    for key, value in data.items():
        for word in lem_query:
            if word == key:
                result[word] = set(value)
    output = metrics(result, N=24, avdl=289.2083333333333, k1=2.0, b=0.75)
    return output

app = Flask(__name__)


@app.route('/', methods=['get', 'post'])
def index():
    if request.form:
        query = request.form['query']
        links = search(query)
        return render_template('index.html',links=links)
    return render_template('index.html',links=[])

if __name__ == '__main__':
    app.run(debug=True)

#print(search('Из Салехарда в Москву'))

