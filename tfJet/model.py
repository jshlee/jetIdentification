from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from layer import conv_layer
from layer import max_pooling_layer
from layer import gap_layer
from layer import fc_layer
from layer_utils import flatten


def inference(images, keep_prob):
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
    
    pool4 = max_pooling_layer(conv8, layer_name='max_pool_4') 
    '''
    Global average pooling
    gap = gap_layer(conv8, layer_name='global_avg_pool')
    fc = fc_layer(gap, 128, 'fc', use_DW=True)
    with tf.name_scope('dropout'):
        dropped = tf.nn.dropout(fc, keep_prob)
    logits = fc_layer(input_tensor=dropped, output_dim=2, layer_name='logits', act_ftn=tf.identity, use_DW=True)
    return logits
    '''
    flat = flatten(pool4)
    fc1 = fc_layer(input_tensor = flat, output_dim = 512, layer_name = 'fc1')
    fc2 = fc_layer(input_tensor = fc1, output_dim = 256, layer_name = 'fc2')
    fc3 = fc_layer(input_tensor = fc2, output_dim = 128, layer_name = 'fc3')

    with tf.name_scope('dropout'):
        dropped = tf.nn.dropout(fc3, keep_prob)

    logits = fc_layer(input_tensor=dropped, output_dim=2, layer_name='logits', act_ftn=tf.identity)
    return logits


def loss(logits, labels, DW=False):
    with tf.name_scope("loss"):
        with tf.name_scope("cross_entropy"):
            diff = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=labels)
            cross_entropy = tf.reduce_mean(diff)
            loss = cross_entropy
        if DW:
            with tf.name_scope("l2_weight_decay"):
                weight_decay = l2_weight_decay(weight_decay_rate=0.01)
            loss += weight_decay
            tf.summary.scalar('cross_entropy', cross_entropy)
            tf.summary.scalar('weight_decay', weight_decay)
    tf.summary.scalar('loss', loss)
    return loss

def l2_weight_decay(weight_decay_rate):
    '''ref. https://github.com/tensorflow/models/blob/master/resnet/resnet_model.py ''' 
    costs = []
    for var in tf.trainable_variables():
        if var.op.name.find(r'DW') > 0:
            costs.append(tf.nn.l2_loss(var))
    return tf.multiply(weight_decay_rate, tf.add_n(costs))


def training(loss, lr, optimizer=tf.train.AdamOptimizer):
    with tf.name_scope("train"):
        global_step = tf.Variable(0, name='global_step', trainable=False)
        train_op = optimizer(learning_rate=lr).minimize(loss, global_step=global_step)
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
