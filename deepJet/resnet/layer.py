from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math

import tensorflow as tf

'''
/www.tensorflow.org/get_started/summaries_and_tensorboard This Variable will hold the state of the weights for the layer
'''
def get_xavier(shape, is_conv2d=True, var_name='xaiver_weights'):
    # get_variable(name, shape=None, dtype=None, initializer=None, regularizer=None, trainable=True,
    #              collections=None, caching_device=None, partitioner=None, validate_shape=True, custom_getter=None)
    if is_conv2d:
        W = tf.get_variable(var_name, shape, initializer=tf.contrib.layers.xavier_initializer_conv2d())
    else:
        W = tf.get_variable(var_name, shape, initializer=tf.contrib.layers.xavier_initializer())
    return W


def convolution(input_feature, out_channels, kernel_size, stride, name='convolution'):
    in_channels = input_feature.get_shape().as_list()[-1]
    with tf.variable_scope(name):
        kernels_shape = [kernel_size, kernel_size, in_channels, out_channels]
        kernels_strides = [1, stride, stride, 1]
        kernels = get_xavier(kernels_shape)
        # conv2d(input, filter, strides, padding, use_cudnn_on_gpu=None, data_format=None, name=None)
        output_feature = tf.nn.conv2d(input_feature, kernels, kernels_strides, padding='SAME')
    return output_feature

def max_pooling(input_tensor, k=2, s=2, name='max_pooling'):
    with tf.name_scope(lname):
        pool = tf.nn.max_pool(input_tensor, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    return pool

def batch_normalization(input_layer, dimension, name, bn_epsilon=0.001):
    '''
    Helper function to do batch normalziation
    :param input_layer: 4D tensor
    :param dimension: input_layer.get_shape().as_list()[-1]. The depth of the 4D tensor
    :return: the 4D tensor after being normalized
    '''
    with tf.variable_scope(name):
        mean, variance = tf.nn.moments(input_layer, axes=[0, 1, 2])
        beta = tf.get_variable('beta', dimension, tf.float32,
                               initializer=tf.constant_initializer(0.0, tf.float32))
        gamma = tf.get_variable('gamma', dimension, tf.float32,
                                initializer=tf.constant_initializer(1.0, tf.float32))
        bn_layer = tf.nn.batch_normalization(input_layer, mean, variance, beta, gamma, bn_epsilon)
    return bn_layer

def fc_layer(input_tensor, output_dim, layer_name, act_ftn=tf.nn.relu):
    input_dim = input_tensor.get_shape().as_list()[-1]
    with tf.variable_scope(layer_name):
        W = get_xavier([input_dim, output_dim], is_conv2d=False, var_name='weight')
        b = get_xavier([output_dim], is_conv2d=False, var_name='bias')
        preactivate = tf.matmul(input_tensor, W) + b
        activations = act_ftn(preactivate, name='activation')
    return activations

def residual_function(input_feature, output_channels, s1):
    u1 = convolution(input_feature, output_channels, kernel_size=3, stride=s1, name='conv1')
    u2 = batch_normalization(u1, output_channels,'bn1')
    u3 = tf.nn.relu(u2)
    u4 = convolution(u3, output_channels, kernel_size=3, stride=1, name='conv2')
    F = batch_normalization(u4, output_channels, 'bn2')
    return F

def residual_unit(input_feature, downsampling, unit_name, identity_mapping_opt='zero_padding'):
    input_channels = input_feature.get_shape().as_list()[-1]
    if downsampling:
        output_channels = input_channels * 2
        s1 = 2
        unit_name += '_downsampling'
    else:
        output_channels = input_channels
        s1 = 1
        
    with tf.variable_scope(unit_name):
        with tf.variable_scope('residual_function'):
            u1 = convolution(input_feature, output_channels, kernel_size=3, stride=s1, name='conv1')
            u2 = batch_normalization(u1, output_channels,'bn1')
            u3 = tf.nn.relu(u2)
            u4 = convolution(u3, output_channels, kernel_size=3, stride=1, name='conv2')
            F = batch_normalization(u4, output_channels, 'bn2')
        with tf.variable_scope('identity_mapping'):
            if downsampling:
                if identity_mapping_opt == 'zero_padding':
                    h_temp = tf.nn.avg_pool(input_feature, [1, 2, 2, 1], [1, 2, 2, 1], 'SAME')
                    h = tf.pad(h_temp, [[0,0], [0,0], [0,0], [ int(math.ceil(input_channels/2)), int(math.floor(input_channels/2)) ]] )
                elif identity_mapping_opt == 'projection_shortcut':
                    h = convolution(input_feature, output_channels, kernel_size=1, stride=2)
            else:
                h = input_feature
        with tf.name_scope('addition'):
            y = tf.add(h, F)
        with tf.name_scope('post_activation'):
            output_feature = tf.nn.relu(y)
    return output_feature
