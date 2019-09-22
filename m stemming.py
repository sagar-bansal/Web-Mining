# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 00:24:59 2018

@author: sagar
"""
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

ps = PorterStemmer()
example_words = ["python","pythoner","pythoning","pythoned","pythonly"]
for w in example_words:
    print(ps.stem(w))

