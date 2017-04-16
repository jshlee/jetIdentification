from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import datetime

import numpy as np
import tensorflow as tf

def get_time():
    return datetime.datetime.now().strftime('%H:%M:%S')

def merge(red_arr, green_arr, blue_arr):
    return np.array( map(None, red_arr, green_arr, blue_arr))

def onehot_encoding(labels):
    labels = labels.astype(np.int64)
    onehot = np.zeros(shape = (len(labels), 2), dtype=np.int64)
    for idx in xrange(len(labels)):
        if labels[idx] == 21:
            onehot[idx][1] = 1
        else:
            onehot[idx][0] = 1
    return onehot

def csv2ndarr(path):
    data = np.loadtxt(path, delimiter=',', unpack=False, dtype=np.float32)
    labels = onehot_encoding( data[:, 0:1] )
    size = 33
    pixels = size * size
    # color channels
    cpt   = data[:, 1:1+pixels]
    npt   = data[:, 1+pixels: 1+2*pixels]
    cmul  = data[:, 1+2*pixels:]
    # merge
    flats = np.array( map(merge, cpt, npt, cmul) )
    # reshape
    images = np.array( map(lambda x: x.reshape((size,size,3)), flats) )
    return images, labels

# def _int64_feature(value):
#     return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def ndarr2tfrecords(data_set, name):
    """Converts a dataset to tfrecords."""
    images = data_set[0]
    labels = data_set[1]
    filename = os.path.join("../data/tfrecords", name + '.tfrecords')
    print('Writing', filename)
    writer = tf.python_io.TFRecordWriter(filename)
    for idx in xrange(images.shape[0]):
        # only length-1 array can be converted to Python scalars.
        image_raw = images[idx].tostring()
        label_raw = labels[idx].tostring()
        example = tf.train.Example(features = tf.train.Features(feature={
            'label_raw': _bytes_feature(label_raw),
            'image_raw': _bytes_feature(image_raw)}))
        writer.write(example.SerializeToString())
    writer.close()

if __name__ == '__main__':
    print('START : .csv file ----> np.ndarray object', '(', get_time(), ')')
    path_to_load = '../data/csv/jet15_rgb.csv'
    images, labels = csv2ndarr(path=path_to_load)
    print('END : .csv file ----> np.ndarray object', '(', get_time(), ')')
    num_train = int(images.shape[0] * 0.6)
    train_set = ( images[:num_train], labels[:num_train] )
    validation_set = ( images[num_train:], labels[num_train:] )
    print('START : train set', '(', get_time(), ')')
    ndarr2tfrecords(train_set, 'jet15_rgb_train')
    print('START : validation set', '(', get_time(), ')')
    ndarr2tfrecords(validation_set, 'jet15_rgb_validation')
