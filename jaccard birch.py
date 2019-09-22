# Libraries

import os
import re
import operator

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from pprint import pprint

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from collections import Counter

from sklearn.cluster import Birch
from sklearn.metrics import jaccard_similarity_score

# Data

data = pd.read_csv('Documents.csv')

print('Documents')
print(data.shape)

print('\nColumns')
print(data.columns)
print()

data.head()

# Parse data

all_words = []

# Removing special characters
# Parameters:
# data - data to be cleaned
# Return:
# data - cleaned data using regex
def remove_special_chars(data):
    data = data.lower()
    return re.sub('[^A-Za-z0-9]+', '', data)

# Parsing document string
# Parameter:
# data - document string
# Return:
# words - tokenized and cleaned document
def parse_document(data):
    
    stop_words = set(stopwords.words('english'))
    words = [remove_special_chars(each) for each in data.split()[1:]]
    words.pop()
    words = [word for word in words if not word in stop_words and len(word)>1]
    all_words.extend(words)
    return words

# Tokenize document

documents_tokens = {}
for i in range(data.shape[0]):
    each = data.iloc[i]
    documents_tokens[each['Doc']] = parse_document(each['Data'])

# Word2Vec

print('Total number of words: ', len(all_words))
all_words = list(set(all_words))
all_words.sort()
print('Total unique words: ', len(all_words))

# Create tf matrix

matrix = []
for doc in documents_tokens.keys():
    w2v = Counter(documents_tokens[doc])
    row = []
    for idx in all_words:
        if idx in w2v:
            row.append(w2v[idx])
        else:
            row.append(0)
    matrix.append(row)

print('Matrix shape')
print(len(matrix), 'x', len(matrix[0]))

# Birch clustering

brc = Birch(
    branching_factor=20,
    n_clusters=7,
    threshold=0.5,
    compute_labels=True
)

# Clustering

brc.fit(matrix)
document_labels = brc.predict(matrix)

print('Document labels: ', document_labels)

# Countplot

sns.countplot(document_labels)

# Jaccard similarity measure

query = '[ Who is the better palyer, Lebron or Jordan ]'

data = parse_document(query)

print('Parsed data: ')
print(data)

# Matrix notation

val = []
w2v = Counter(documents_tokens[doc])
for idx in all_words[:-len(data)]:
    if idx in w2v:
        val.append(w2v[idx])
    else:
        val.append(0)
        
print('Matrix notation')
print('Shape: ', len(val))

# Jaccard similarity with all documents

score = {}
for idx, row in enumerate(matrix):
    score['Document_' + str(idx)] = jaccard_similarity_score(row, val)

# Top 10 similar documents

document_sort = sorted(score.items(), key=operator.itemgetter(1))

print('Top 10 documnets with highest jaccard similarity\n')
print('Documnet name     | Jaccard similarity\n--------------------------------------')
for idx, doc_name in enumerate(reversed(document_sort)):
    
    print(doc_name[0], '         ', doc_name[1])
    if idx == 9:
        break