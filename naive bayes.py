# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 23:09:08 2018

@author: sagar
"""


from sklearn import datasets

from sklearn import metrics

from sklearn.naive_bayes import GaussianNB



dataset=datasets.load_iris()

model=GaussianNB()

model.fit(dataset.data,dataset.target)

print(model)

expected=dataset.target

predicted=model.predict(dataset.data)

print(metrics.classification_report(expected,predicted))

print(metrics.confusion_matrix(expected, predicted))

