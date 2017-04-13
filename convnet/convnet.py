from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time

import numpy as np
import tensorflow as tf

from drawer import get_date
from layer import convolutional_layer, fully_connected_layer 

def inference(images, keep_prob):
    conv1 = convolutional_layer(images,[5, 5,  3, 16], layer_name='conv1') # out_pool = 17
    conv2 = convolutional_layer(conv1, [5, 5, 16, 32], layer_name='conv2') # out_pool = 9
    conv3 = convolutional_layer(conv2, [5, 5, 32, 64], layer_name='conv3') # out_pool = 5

    flat = tf.reshape(conv3, [-1, 5*5*64]) 

    fc = fully_connected_layer(input_tensor=flat, input_dim=5*5*64, output_dim=512, layer_name='fc1')

    with tf.name_scope('dropout'):
        tf.summary.scalar('dropout_keep_probability', keep_prob)
        dropped = tf.nn.dropout(fc, keep_prob)

    logits = fully_connected_layer(input_tensor = dropped,
                                   input_dim=512, output_dim=2,
                                   layer_name='logits',
                                   act_ftn=tf.identity)
    return logits

def loss(logits, labels):
    with tf.name_scope("cross_entropy"):
        diff = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=labels)
        with tf.name_scope('total'):
            cross_entropy = tf.reduce_mean(diff)
    tf.summary.scalar('cross_entropy', cross_entropy)
    return cross_entropy

def training(loss, learning_rate):
    with tf.name_scope("train"):
        train_op = tf.train.AdamOptimizer(learning_rate=1e-4).minimize(loss)
    return train_op

def evaluation(logits, labels):
    with tf.name_scope('accuracy'):
        with tf.name_scope('correct_prediction'):
            correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(labels, 1))
        with tf.name_scope('num_correct'):
            num_correct = tf.reduce_sum(tf.cast(correct_prediction, tf.float32))
        with tf.name_scope('accuracy'):
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    tf.summary.scalar('accuracy', accuracy)
    return accuracy
