#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 19:10:52 2018

@author: Jet


instant note
1. with tf.Session() as sess:
    
2. .eval()

3. tf.convert_to_tensor()

4. tf.placeholder

5. feed_dict





"""






import tensorflow as tf
import numpy as np
#a = tf.constant(4)
#b = tf.constant(3)
#
#with tf.Session() as sess:
#    print "a=",sess.run(a), ", b=" , sess.run(b)
#    print "a+b=" , sess.run(a+b)
#    print "a*b=" , sess.run(a*b)
#################################################

# auto complete

        
#a = tf.constant(5)
#b = tf.constant(6)
#c = a*b
#
#with tf.Session() as sess:
#    print sess.run(c)
#    print c.eval()
#    
#d = c.eval()  # kind of conversion  # ! must in sess
#print d
#################################################


# type notice more details
# blind type with symbol/ shortkey
#  
#W1 = tf.ones((2,2))
#W2 = tf.Variable(tf.ones((2,2)), name="weights")
#with tf.Session() as sess:
#    print sess.run(W1)  # ?
#    print W1
#    print W1.eval()
##    sess.run(tf.initialize_all_variables())
#    #sess.run(tf.global_variables_initializer())
##    tf.global_variables_initializer()  # must sees.run
#    #FailedPreconditionError: Attempting to use uninitialized value weights_9
#    print sess.run(W2)
#################################################
    

#state = tf.Variable(0, name="counter")    
#new_value = tf.add(state, tf.constant(1))    
#update = tf.assign(state, new_value)  # damn poor assign
#
#with tf.Session() as sess:
#    sess.run(tf.initialize_all_variables())
#    print(sess.run(state))
#    for _ in range(3):   # _ for nothing
#        sess.run(update)
#        print(sess.run(state)

# shortkey cmd+D delete line    
#################################################
#
#input1 = tf.constant(3.0)    
#input2 = tf.constant(2.0)
#input3 = tf.constant(5.0)
#intermed = tf.add(input2, input3)  
#mul = tf.multiply(input1, intermed)
#with tf.Session() as sess:
#     result = sess.run([mul, intermed])
#     print(result)
##################################################
    
#input1 = tf.placeholder(tf.float32)
#input2 = tf.placeholder(tf.float32)
#output = tf.multiply(input1, input2) 
#with tf.Session() as sess:  
#     print(sess.run([output], \
#                    feed_dict={input1:[7.], input2:[2.]}))
#    
###################################################



################# variable scope #######################
#with tf.variable_scope("foo"):
#    with tf.variable_scope("bar"):
#        v = tf.get_variable("v", [1])
#        # ValueError: Variable foo/bar/v already exists, disallowed. Did you mean to set reuse=True or reuse=tf.AUTO_REUSE in VarScope? Originally defined at:
##assert v.name == "foo/bar/v:0"
##print v.name


################# variable scope #######################
#with tf.variable_scope("foo"):
#    v = tf.get_variable("v", [1])
#    tf.get_variable_scope().reuse_variables()
#    v1 = tf.get_variable("v", [1])
#assert v1 == v    

    

with tf.variable_scope("foo"):
    v = tf.get_variable("v", [1])    
    