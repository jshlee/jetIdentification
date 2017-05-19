from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys 

import time

import numpy as np
import tensorflow as tf

from layer import conv3, max_pooling_layer, fully_connected_layer 
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from drawer import get_date


def inference(images, keep_prob):
    conv_1 = conv3(images, 3, 64, '1st_conv_layer')
    conv_2 = conv3(conv_1, 64, 64, '2nd_conv_layer')
    pool_1 = max_pooling_layer(conv_2, '1st_max_pool_layer')
    print('1st conv: ', conv_1.get_shape())
    print('2nd conv: ', conv_2.get_shape())
    print('1st pool: ', pool_1.get_shape())

    conv_3 = conv3(pool_1, 64, 128, '3rd_conv_layer')
    conv_4 = conv3(conv_3, 128, 128, '4th_conv_layer')
    pool_2 = max_pooling_layer(conv_4, '2nd_max_pool_layer')
    print('3rd conv: ', conv_3.get_shape())
    print('4th conv: ', conv_4.get_shape())
    print('2nd pool: ', pool_2.get_shape())

    conv_5 = conv3(pool_2, 128, 256, '5th_conv_layer')
    conv_6 = conv3(conv_5, 256, 256, '6th_conv_layer')
    pool_3 = max_pooling_layer(conv_6, '3rd_max_pool_layer')
    print('5th conv: ', conv_5.get_shape())
    print('6th conv: ', conv_6.get_shape())
    print('3rd pool: ', pool_3.get_shape())

    conv_7 = conv3(pool_3, 256, 512, '7th_conv_layer')
    conv_8 = conv3(conv_7, 512, 512, '8th_conv_layer')
    pool_4 = max_pooling_layer(conv_8, '4th_max_pool_layer')
    print('7th conv: ', conv_7.get_shape())
    print('8th conv: ', conv_8.get_shape())
    print('4th pool: ', pool_4.get_shape())

    flat = tf.reshape(pool_4, [-1, 3*3*512]) 

    fc1 = fully_connected_layer(input_tensor=flat, input_dim=3*3*512, output_dim=512, layer_name='fc1')
    fc2 = fully_connected_layer(input_tensor=fc1, input_dim=512, output_dim=256, layer_name='fc2')
    fc3 = fully_connected_layer(input_tensor=fc2, input_dim=256, output_dim=128, layer_name='fc3')

    with tf.name_scope('dropout'):
        dropped = tf.nn.dropout(fc3, keep_prob)

    logits = fully_connected_layer(input_tensor = dropped,
                                   input_dim=128, output_dim=2,
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
