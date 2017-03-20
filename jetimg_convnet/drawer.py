from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import cPickle

import tensorflow as tf

def get_date():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M')[2:]


def unpickle( path ):
    f = open(path, 'r')
    print("The file was opened.")
    data = cPickle.load(f)
    print("The file is loaded.")
    f.close()
    print("The file was closed.")
    return data

def onehot_encoding(labels):
    return tf.one_hot(indices=labels, depth=2, on_value=1, off_value=0)

def input_data(path):
    data = unpickle( path )
    data_set = {'training': dict(), 'validation': dict(), 'test': dict() }

    sess = tf.InteractiveSession()
    data_set['training']['images'] = data[0][0]
    data_set['training']['labels'] = sess.run(onehot_encoding(data[0][1]))
    data_set['training']['num'] = len(data[0][0])
    data_set['validation']['images'] = data[1][0]
    data_set['validation']['labels'] = sess.run(onehot_encoding(data[1][1]))
    data_set['validation']['num'] = len(data[1][0])
    data_set['test']['images'] = data[2][0]
    data_set['test']['labels'] = sess.run(onehot_encoding(data[2][1]))
    data_set['test']['num'] = len(data[2][0])
    sess.close()
    return data_set

def get_batch(data, batch_size=100): 
    for idx in range(0, data['num'], batch_size):
        images_batch = data['images'][idx: idx + batch_size]
        labels_batch = data['labels'][idx: idx + batch_size]
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
    

