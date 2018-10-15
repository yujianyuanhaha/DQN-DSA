#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 20:37:42 2018

@author: Jet
"""


from sklearn import datasets, preprocessing
from sklearn.model_selection import train_test_split
from neupy import algorithms, estimators, environment

environment.reproducible()

dataset = datasets.load_diabetes()
x_train, x_test, y_train, y_test = train_test_split(
        preprocessing.minmax_scale(dataset.data),
        preprocessing.minmax_scale(dataset.target.reshape((-1, 1))),
        test_size=0.3,
 )

nw = algorithms.GRNN(std=0.1, verbose=False)
nw.train(x_train, y_train)

y_predicted = nw.predict(x_test)
estimators.rmse(y_predicted, y_test)