# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

number = [12, 37, 5, 42, 8, 3]
even = []
odd = []
while len(number):    # () could emit
    t = number.pop()
    if t%2 == 0 :
        even += [t]
    else:
        odd += [t]
print even
print odd

#  .pop  .append