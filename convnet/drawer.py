from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import cPickle
import numpy as np
import tensorflow as tf

def get_date():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M')[2:]

def lookAt(obj):
    obj_type = type(obj)
    if obj_type == np.ndarray:
        print(obj_type)
        print(obj.shape)
        print(obj.dtype)
    else:
        print(":P")

def unpickle( path ):
    print("path: %s" % path)
    f = open(path, 'r')
    print("The file was opened.")
    data = cPickle.load(f)
    print("The file is loaded.")
    f.close()
    print("The file was closed.")
    return data

def onehot_encoding(labels):
    onehot = np.zeros(( len(labels), 2))
    for i in xrange(len(labels)):
        if labels[i] == 21:
            onehot[i][1] = 1
        else:
            onehot[i][0] = 1
    return onehot

def input_data(path):
    images, labels = unpickle( path )
    labels = onehot_encoding( labels )
    # 
    data_set = {'training': dict(), 'validation': dict(), 'test': dict() }
    # rename please
    total = len(images)
    a = int( total * 0.6 )
    b = int( total * 0.2 ) 
    data_set['training']['images'] = images[:a]
    data_set['training']['labels'] = labels[:a]
    data_set['training']['num'] = len(data_set['training']['images'])
    data_set['validation']['images'] = images[a:a+b]
    data_set['validation']['labels'] = labels[a:a+b]
    data_set['validation']['num'] = len(data_set['validation']['images'])
    data_set['test']['images'] = images[a+b:]
    data_set['test']['labels'] = labels[a+b:]
    data_set['test']['num'] = len(data_set['test']['images'])
    return data_set

def get_batch(data_set, batch_size=100): 
    for idx in xrange(0, data_set['num'], batch_size):
        images_batch = data_set['images'][idx: idx + batch_size]
        labels_batch = data_set['labels'][idx: idx + batch_size]
        yield images_batch, labels_batch

def save_cpickle(data, name=None):
    if not name:
        name = get_now()
    if ''.join([name, 'p']) in os.listdir('.'):
        name = ''.join([name, '_', get_date()])
    path = ''.join(['./', name, '.p'])
    #
    with open(path, 'w') as f:
        cPickle.dump(data, f)
        



'''
def check_acc(data, sess=sess):
    batches = get_batch( data, batch_size = 200 )
    total = 0
    for img, lab in batches:
        num_correct, _ = sess.run([num_correct, accuracy], feed_dict={images : img, labels : lab, keep_prob : 1.0})
        total += num_correct
    accuracy = total / data['num']
    return accuracy
'''
    

