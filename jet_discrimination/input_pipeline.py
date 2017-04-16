from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import tensorflow as tf

# https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/how_tos/reading_data/fully_connected_reader.py

def read_and_decode(filename_queue):
    """
    Args:

    """
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(
        serialized_example,
        features={
              'image_raw': tf.FixedLenFeature([], tf.string),
              'label_raw': tf.FixedLenFeature([], tf.string),
        })
    # image
    image = tf.decode_raw(features['image_raw'], tf.float32)
    image.set_shape([33*33*3])
    image = tf.reshape(tensor=image, shape=(33,33,3))
    # label
    label = tf.decode_raw(features['label_raw'], tf.int64)
    label.set_shape([2])
    return image, label

def inputs(is_train, filename, batch_size=100, num_epochs=10000):
    if is_train:
        filename = ''.join([filename, '_train','.tfrecords'])
    else:
        filename = ''.join([filename, '_validation', '.tfrecords'])
    path = os.path.join('../data/tfrecords/', filename)
    with tf.name_scope('input'):
        filename_queue = tf.train.string_input_producer(
            [path], num_epochs=num_epochs)
        image, label = read_and_decode(filename_queue)
        images, sparse_labels = tf.train.shuffle_batch(
            [image, label], batch_size=batch_size, num_threads=2,
            capacity=1000 + 3 * batch_size,
            min_after_dequeue=1000)
    return images, sparse_labels

# http://stackoverflow.com/questions/39187764/tensorflow-efficient-feeding-of-eval-train-data-using-queue-runners

def get_train_inputs(is_training):
    return inputs(is_train=True, filename='jet15_rgb')

def get_eval_inputs(is_training):
    return inputs(is_train=False, filename='jet15_rgb')

def get_mixed_inputs(is_training):
    train_inputs = get_train_inputs(None)
    eval_inputs = get_eval_inputs(None)
    return tf.cond(is_training, lambda: train_inputs, lambda: eval_inputs)

