"""Radial Basis Function Network for aproximating non-linear functions
for stewart platform forward kinematics"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import tempfile

import tensorflow as tf
import numpy as np
sess = tf.Session()

m = None


x = tf.placeholder(tf.float32, [m, 6])
c = tf.Variable(tf.ones([m, 6]))
b = tf.Variable(tf.ones([6]))
W = tf.Variable(tf.ones([6, m]))
model = tf.matmul(tf.exp(-1 * tf.square(tf.abs(tf.subtract(x,c)) / b)),W)


init = tf.global_variables_initializer()
sess.run(init)

print(sess.run(model, {x: [1, 2, 3, 4, 5, 6]}))

y = tf.placeholder(tf.float32)
squared_deltas = tf.square(model - y)
loss = tf.reduce_sum(squared_deltas)
print(sess.run(loss, {x: [1, 2, 3, 4, 5, 6], y: [0, -1, -2, -3, -4, -5]}))

optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(loss)

sess.run(init) # reset values to incorrect defaults.
for i in range(1000):
  sess.run(train, {x: [1, 2, 3, 4, 5, 6], y: [0, -1, -2, -3, -4, -5]})

print(sess.run([W, b]))


x_train = [1, 2, 3, 4, 5, 6]
y_train = [0, -1, -2, -3, -4, -5]

# evaluate training accuracy
curr_W, curr_b, curr_loss = sess.run([W, b, loss], {x: x_train, y: y_train})
print("W: %s b: %s loss: %s"%(curr_W, curr_b, curr_loss))
# FLAGS = None
# 
# def main(_):
#   # Import data
#   data = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)
# 
#   # Create the model
#   x = tf.placeholder(tf.float32, [None, 6])
#   W = tf.Variable(tf.zeros([6, None]))
#   b = tf.Variable(tf.zeros([6]))
#   y = tf.matmul(x, W) + b
# 
#   # Define loss and optimizer
#   y_ = tf.placeholder(tf.float32, [None, 6])
# 
#   # The raw formulation of cross-entropy,
#   #
#   #   tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.nn.softmax(y)),
#   #                                 reduction_indices=[1]))
#   #
#   # can be numerically unstable.
#   #
#   # So here we use tf.nn.softmax_cross_entropy_with_logits on the raw
#   # outputs of 'y', and then average across the batch.
#   cross_entropy = tf.reduce_mean(
#       tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
#   train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
# 
#   sess = tf.InteractiveSession()
#   tf.global_variables_initializer().run()
#   # Train
#   for _ in range(1000):
#     # batch_xs, batch_ys = mnist.train.next_batch(100)
#     sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
# 
#   # Test trained model
#   # correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
#   # accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
#   # print(sess.run(accuracy, feed_dict={x: mnist.test.images,
#   #                                     y_: mnist.test.labels}))
# 
# if __name__ == '__main__':
#   parser = argparse.ArgumentParser()
#   parser.add_argument('--data_dir', type=str,
#                       default='./LUT.txt', # to be finalized
#                       help='Directory for storing input data')
#   FLAGS, unparsed = parser.parse_known_args()
#   tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)