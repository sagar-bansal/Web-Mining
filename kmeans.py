# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 00:03:39 2018

@author: sagar
"""

import pandas as pd
import numpy as np

data=pd.read_excel('data.xlsx') #Include your data file instead of data.xlsx
idea=data.iloc[:,0:1] #Selecting the first column that has text.

corpus=[]
for index,row in idea.iterrows():
    corpus.append(row['Idea'])

from sklearn.feature_extraction.text import CountVectorizer 
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data['Idea'].values.astype(str))

from sklearn.feature_extraction.text import TfidfTransformer

transformer = TfidfTransformer(smooth_idf=False)
tfidf = transformer.fit_transform(X)
print(tfidf.shape )

from sklearn.cluster import KMeans

num_clusters = 5 #Change it according to your data.
km = KMeans(n_clusters=num_clusters) 
km.fit(tfidf)

clusters = km.labels_.tolist()

idea={'Content':corpus, 'Cluster':clusters} #Creating dict having doc with the corresponding cluster number.
frame=pd.DataFrame(idea,index=[clusters], columns=['Content','Cluster']) # Converting it into a dataframe.

print("\n")
print(frame) #Print the doc with the labeled cluster number.
print("\n")
print(frame['Cluster'].value_counts())
