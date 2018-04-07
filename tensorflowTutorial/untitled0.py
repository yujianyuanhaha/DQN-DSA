#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 11:45:19 2018

@author: Jet
"""

def greet(name):
 #   print "Hello, {0}!".format(name)
     print "Hello, " + name + "!"
print "What's your name?"
name = raw_input()
greet(name)