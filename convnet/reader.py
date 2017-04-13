from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import tensorflow as tf

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

def inputs(filename, batch_size=100, num_epochs=2):
    with tf.name_scope('input'):
        filename_queue = tf.train.string_input_producer(
            [filename], num_epochs=num_epochs)
        image, label = read_and_decode(filename_queue)
        images, sparse_labels = tf.train.shuffle_batch(
            [image, label], batch_size=batch_size, num_threads=2,
            capacity=1000 + 3 * batch_size,
            min_after_dequeue=1000)
    return images, sparse_labels
