from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

from layer import *

def vgg8(images, keep_prob):
    conv1 = conv_layer(images, 64, 'conv1')
    conv2 = conv_layer(conv1, 64, 'conv2')
    pool1 = max_pooling_layer(conv2, layer_name='max_pool_1') 

    conv3 = conv_layer(pool1, 128, 'conv3')
    conv4 = conv_layer(conv3, 128, 'conv4')
    pool2 = max_pooling_layer(conv4, layer_name='max_pool_2') 

    conv5 = conv_layer(pool2, 256, 'conv5')
    conv6 = conv_layer(conv5, 256, 'conv6')
    pool3 = max_pooling_layer(conv6, layer_name='max_pool_3')

    conv7 = conv_layer(pool3, 512, 'conv7')
    conv8 = conv_layer(conv7, 512, 'conv8')
    pool4 = max_pooling_layer(conv8, layer_name='max_pool_4') 

    flat = flatten(pool4)

    fc1 = fc_layer(input_tensor = flat, output_dim = 512, layer_name = 'fc1')
    fc2 = fc_layer(input_tensor = fc1, output_dim = 256, layer_name = 'fc2')
    fc3 = fc_layer(input_tensor = fc2, output_dim = 128, layer_name = 'fc3')

    with tf.name_scope('dropout'):
        dropped = tf.nn.dropout(fc3, keep_prob)

    logits = fc_layer(input_tensor=dropped, output_dim=2, layer_name='logits', act_ftn=tf.identity)
    return logits

def vgg11_full_preactivation(input_tensor, keep_prob):
    u0 = conv_layer(input_tensor, 64, 'conv') # [N, 64, 17, 17]
    u1 = vgg_module(u0, num_block=3, module_name='vgg_module_1') # [N, 128, 9, 9]
    u2 = vgg_module(u1, num_block=4, module_name='vgg_module_2') # [N, 256, 5, 5]
    u3 = vgg_module(u2, num_block=3, module_name='vgg_module_3') # [N, 512, 3, 3]

    u3_flattened = flatten(u3)

    fc1 = fc_layer(input_tensor = u3_flattened, output_dim = 512, layer_name = 'fc1')
    fc2 = fc_layer(input_tensor = fc1, output_dim = 256, layer_name = 'fc2')
    fc3 = fc_layer(input_tensor = fc2, output_dim = 128, layer_name = 'fc3')

    with tf.name_scope('dropout'):
        dropped = tf.nn.dropout(fc3, keep_prob)

    logits = fc_layer(input_tensor=dropped, output_dim=2, layer_name='logits', act_ftn=tf.identity)
    return logits

def vgg8_gap(images, keep_prob):
    # images [N, 3, 33, 33]
    conv1 = conv_layer(images, 64, 'conv1')
    conv2 = conv_layer(conv1, 64, 'conv2')
    pool1 = max_pooling_layer(conv2, layer_name='max_pool_1') 

    conv3 = conv_layer(pool1, 128, 'conv3')
    conv4 = conv_layer(conv3, 128, 'conv4')
    pool2 = max_pooling_layer(conv4, layer_name='max_pool_2') 

    conv5 = conv_layer(pool2, 256, 'conv5')
    conv6 = conv_layer(conv5, 256, 'conv6')
    pool3 = max_pooling_layer(conv6, layer_name='max_pool_3')

    conv7 = conv_layer(pool3, 512, 'conv7')
    conv8 = conv_layer(conv7, 512, 'conv8')
    
    # Global average pooling
    gap = gap_layer(conv8, layer_name='global_avg_pool')

    fc = fc_layer(gap, 128, 'fc')

    with tf.name_scope('dropout'):
        dropped = tf.nn.dropout(fc, keep_prob)

    logits = fc_layer(input_tensor=dropped, output_dim=2, layer_name='logits', act_ftn=tf.identity)
    return logits
