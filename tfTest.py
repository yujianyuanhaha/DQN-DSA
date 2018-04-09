#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 17:59:24 2018

@author: Jet
"""

import tensorflow as tf
import numpy as np

# create data
x_data = np.random.rand(100).astype(np.float32)
y_data = x_data*0.1 + 0.3

Weights = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
biases  = tf.Variable(tf.zeros([1]))

y = Weights*x_data + biases

loss = tf.reduce_mean(tf.square(y-y_data))

optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

init = tf.global_variables_initializer()  # 替换成这样就好

sess = tf.Session()
sess.run(init)   # ??

for step in range(201):
    sess.run(train)   # ??
    if step % 20 == 0:
        print(step, sess.run(Weights), sess.run(biases))

################################################################


matrix1 = tf.constant([[3,3]])
matrix2 = tf.constant([[2],
                       [2]])
product = tf.matmul(matrix1,matrix2)  # name of operation

#product 不是直接计算的步骤, 所以我们会要使用 Session 来激活 product 并得到计算结果. 
#有两种形式使用会话控制 Session

# method 1
sess = tf.Session()
result = sess.run(product)
print(result)
sess.close()
# [[12]]

# method 2
with tf.Session() as sess:
    result2 = sess.run(product)
    print(result2)
# more common
    
    
################################################################
#在 Tensorflow 中，定义了某字符串是变量，它才是变量，这一点是与 Python 所不同的。
import tensorflow as tf

state = tf.Variable(0, name='counter')

# 定义常量 one
one = tf.constant(1)

# 定义加法步骤 (注: 此步并没有直接计算)
new_value = tf.add(state, one)

# 将 State 更新成 new_value
update = tf.assign(state, new_value)

# 如果定义 Variable, 就一定要 initialize
# init = tf.initialize_all_variables() # tf 马上就要废弃这种写法
init = tf.global_variables_initializer()  # 替换成这样就好
 
# 使用 Session
with tf.Session() as sess:
    sess.run(init)
    for _ in range(3):
        sess.run(update)
        print(sess.run(state))
        
        
################################################################
import tensorflow as tf

#在 Tensorflow 中需要定义 placeholder 的 type ，一般为 float32 形式
input1 = tf.placeholder(tf.float32)
input2 = tf.placeholder(tf.float32)

# mul = multiply 是将input1和input2 做乘法运算，并输出为 output 
ouput = tf.multiply(input1, input2)

with tf.Session() as sess:
    print(sess.run(ouput, feed_dict={input1: [7.], input2: [2.]}))
# [ 14.]


################################################################


xs = tf.placeholder(tf.float32, [None, 1])
ys = tf.placeholder(tf.float32, [None, 1])



xs= tf.placeholder(tf.float32, [None, 1],name='x_in')
ys= tf.placeholder(tf.loat32, [None, 1],name='y_in')


with tf.name_scope('inputs'):
    # define placeholder for inputs to network
    xs = tf.placeholder(tf.float32, [None, 1])
    ys = tf.placeholder(tf.float32, [None, 1])






























    

