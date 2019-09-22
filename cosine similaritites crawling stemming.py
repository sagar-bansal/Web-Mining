# -*- coding: utf-8 -*-

# Libraries

import os
import re 
import math
import operator
import requests

from bs4 import BeautifulSoup as soup
from bs4.element import Comment

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from collections import Counter
from pprint import pprint

# Parameters

HOME = 'https://en.wikipedia.org/'
SEED = 'wiki/Human_Genome_Project'
QUERY = 'What are the Key findings of the draft (2001)'
ITER = 1
DOCUMENTS = 50
URL_LIST = [SEED]
urlname=[]

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# Crawler

print('Starting crawler ...\n')

for url in URL_LIST:
    
    print('URL: ', HOME + url)
    urlname.append(HOME+url)
    print("first url is "+urlname[0])
    html = requests.get(HOME + url)
    
    f = open('./Pages/Web_page_' + str(ITER) + '.txt', 'w',encoding='utf-8')
    f.write(html.text)
    f.close()
    
    s = soup(html.text, 'html.parser')
    
    FOUND = 0
    for tag in s.find_all('a', href=True):
        new_url = tag['href']
        if new_url[:5] == '/wiki' and new_url[-4] != '.' and new_url not in URL_LIST:
            URL_LIST.append(new_url)
            FOUND += 1
    print('New urls found: ', FOUND)
    print()
    
    texts = s.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    text = u" ".join(t.strip() for t in visible_texts)
    text = re.sub("[\(\[].*?[\)\]]", "",text)
    
    f = open('./Documents/Doc_' + str(ITER) + '.txt', 'w',encoding='utf-8')
    f.write(text)
    f.close()
    
    if ITER >= DOCUMENTS:
        break
        
    ITER += 1


print('Crawler end ...')

# Files

print('Web pages: ')
print(os.listdir('./Pages'))

print('\nDocuments: ')
print(os.listdir('./Documents'))

# Read text from Documents

words = []
stop_words = set(stopwords.words('english'))
doc_text = []

documents = os.listdir('./Documents')
#documents.remove('.ipynb_checkpoints')

for doc in documents:
    
    f = open('./Documents/' + doc,encoding='utf-8')
    text = f.readlines()[0]
    
    # Tokenize
    
    tokens = word_tokenize(text)
    filtered_words = [w for w in tokens if not w in stop_words]
    
    new_words = []
    for w in filtered_words:
        if len(w) != 1:
            new_words.append(w)
    doc_text.append(new_words)
    
    for w in new_words:
        words.append(w)
        
print('Word count: ', len(words))

# Word frequency

frequency = Counter(words)
print('Word frequency: ')
pprint(frequency)

# Cosine similarity

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
    
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
    
    words = WORD.findall(text)
    return Counter(words)

# Document wise similarity

cosine_similarities = {}
for idx, data in enumerate(doc_text):
    
    data = ' '.join(data)
    
    vector1 = text_to_vector(QUERY)
    vector2 = text_to_vector(data)
    
    cosine_similarities['Doc_' + str(idx)] = get_cosine(vector1, vector2)

print('Cosine similarities: ')
pprint(cosine_similarities)

# Top 10 Documents

cosine_sim_sort = sorted(cosine_similarities.items(), key=operator.itemgetter(1))

for idx, doc_name in enumerate(reversed(cosine_sim_sort)):

    
    print('Document name: ', doc_name[0], 'Cosine similarity: ', doc_name[1])
    
    if idx == 9:
        break

