from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys 

import time

import numpy as np
import tensorflow as tf

from layer import convolution, residual_unit, fc_layer 
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from drawer import get_date


def inference(images, keep_prob):
    # size / channels
    # images : 33 / 3

    u0 = tf.nn.avg_pool(images, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID') # 17

    # convolution(input_feature, out_channels, kernel_size, stride, name='convolution')
    u0_1 = convolution(u0, out_channels=64, kernel_size=5, stride=2, name='u0_1')

    # residual_unit(input_feature, downsampling, unit_name, identity_mapping_opt='zero_padding')
    u1 = residual_unit(u0_1, False, 'res_unit1') # 
    u2 = residual_unit(u1, False, 'res_unit2')
    u3 = residual_unit(u2, False, 'res_unit3')
    u4 = residual_unit(u3, False, 'res_unit4')
    u5 = residual_unit(u4, False, 'res_unit5')

    u6 = residual_unit(u5, True, 'res_unit6')  #5
    u7 = residual_unit(u6, False, 'res_unit7')
    u8 = residual_unit(u7, False, 'res_unit8')
    u9 = residual_unit(u8, False, 'res_uni9') # 3 / 512
    u10 = residual_unit(u9, False, 'res_unit10')
    u11 = residual_unit(u10, False, 'res_unit11')
    u12 = residual_unit(u11, False, 'res_unit12')

    u13 = residual_unit(u12, True, 'res_unit13') # 9 /128
    u14 = residual_unit(u13, False, 'res_unit14')
    u15 = residual_unit(u14, False, 'res_unit15')
    u16 = residual_unit(u15, False, 'res_unit16')
    u17 = residual_unit(u16, False, 'res_unit17')

    # avg_pool = tf.nn.avg_pool(u11, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME') # 2 / 512
   
    flat_dim = reduce(lambda x,y: x * y, u17.get_shape().as_list()[1:], 1)
    flat = tf.reshape(u17, [-1, flat_dim]) # 2048

    # fc_layer(input_tensor, output_dim, layer_name, act_ftn=tf.nn.relu)
    fc1 = fc_layer(flat, 512, 'fc1')
    with tf.name_scope('drop1'):
        drop1 = tf.nn.dropout(fc1, keep_prob)

    fc2 = fc_layer(drop1, 128, 'fc2')
    with tf.name_scope('dropout'):
        drop2 = tf.nn.dropout(fc2, keep_prob)

    logits = fc_layer(drop2, 2, 'logits', tf.identity)
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
        train_op = tf.train.AdamOptimizer(learning_rate=1e-2).minimize(loss)
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
