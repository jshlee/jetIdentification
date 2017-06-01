from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

'''
/www.tensorflow.org/get_started/summaries_and_tensorboard This Variable will hold the state of the weights for the layer
'''
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def xavier_init(name, shape, is_conv2d=True):
    if is_conv2d:
        weight = tf.get_variable(name, shape, initializer=tf.contrib.layers.xavier_initializer_conv2d())
    else:
        weight = tf.get_variable(name, shape, initializer=tf.contrib.layers.xavier_initializer())
    return weight 

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def variable_summaries(var):
    with tf.name_scope('summaries'):
        mean = tf.reduce_mean(var)
        tf.summary.scalar('mean', mean)
        with tf.name_scope('stddev'):
            stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
        tf.summary.scalar('stddev', stddev)
        tf.summary.scalar('max', tf.reduce_max(var))
        tf.summary.scalar('min', tf.reduce_min(var))
        tf.summary.histogram('histogram', var)

def conv3(input_tensor, in_channels, out_channels, layer_name):
    with tf.name_scope(layer_name):
        # Convolution stage: Affine transform
        with tf.name_scope('kernel'):
            kernel_name = 'kernel_xavier_' + layer_name
            kernel_shape = [3, 3, in_channels, out_channels]
            kernel = xavier_init(name=kernel_name, shape=kernel_shape, is_conv2d=True) 
        with tf.name_scope('convolution'):
            conv = tf.nn.conv2d(input_tensor, kernel, strides=[1, 1, 1, 1], padding='SAME')
        with tf.name_scope('biases'):
            biases = bias_variable([out_channels])
        with tf.name_scope('plus_biases'):
            preactivate = tf.nn.bias_add(conv, biases)
        # Detector stage: Nonlinearity (e.g. rectified linear unit)
        with tf.name_scope('activations'):
            activations = tf.nn.relu(preactivate)
        return activations


def max_pooling_layer(input_tensor, layer_name):
    with tf.name_scope(layer_name):
        # Pooling stage 
        with tf.name_scope('max_pool'):
            pool = tf.nn.max_pool(input_tensor, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        return pool


def fully_connected_layer(input_tensor, input_dim, output_dim, layer_name, act_ftn=tf.nn.relu):
    with tf.name_scope(layer_name):
        with tf.name_scope('weights'):
            weights = xavier_init(name='fc'+layer_name, shape=[input_dim, output_dim], is_conv2d=False)
            variable_summaries(weights)
        with tf.name_scope('biases'):
            biases = bias_variable([output_dim])
            variable_summaries(biases)
        with tf.name_scope('affine_transformation'):
            preactivate = tf.matmul(input_tensor, weights) + biases
            tf.summary.histogram('pre_activations', preactivate)
        activations = act_ftn(preactivate, name='activation')
        tf.summary.histogram('activations', activations)
        return activations
