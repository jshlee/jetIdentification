from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np

from drawer import input_data, get_batch
from layer import convolutional_layer, fully_connected_layer 

images = tf.placeholder(tf.float32, shape=[None, 48*48], name="images")
labels = tf.placeholder(tf.float32, shape=[None, 2], name="labels")

images_rehape = tf.reshape(images, [-1, 48, 48, 1])

# convolutional_layer(input_tensor, kernel_shape, layer_name)
# kernel_shape = [kernel_size, kernel_size, input_channel, output_channel]
conv1 = convolutional_layer(images_rehape, [5, 5, 1, 32], layer_name='conv1')
conv2 = convolutional_layer(conv1, [5, 5, 32, 64], layer_name='conv1')
conv3 = convolutional_layer(conv2, [5, 5, 64, 128], layer_name='conv3')

flat = tf.reshape(conv3, [-1, 6*6*128]) 

fc = fully_connected_layer(input_tensor=flat, input_dim=6*6*128, output_dim=512, layer_name='fc1')

with tf.name_scope('dropout'):
    keep_prob = tf.placeholder(tf.float32, name="keep_prob")
    tf.summary.scalar('dropout_keep_probability', keep_prob)
    dropped = tf.nn.dropout(fc, keep_prob)

logits = fully_connected_layer(input_tensor=dropped, input_dim=512, output_dim=2, layer_name='logits', act_ftn=tf.identity)

###########################################################################################################

with tf.name_scope("cross_entropy"):
    # tf.nn.softmax_cross_entropy_with_logits
    # WARNING: This op expects unscaled logits, since it performs a softmax on logits internally for efficiency.
    # Do not call this op with the output of softmax, as it will produce incorrect results.
    diff = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=labels)
    with tf.name_scope('total'):
        cross_entropy = tf.reduce_mean(diff)
tf.summary.scalar('cross_entropy', cross_entropy)

with tf.name_scope("train"):
    train_step = tf.train.AdamOptimizer(learning_rate=1e-4).minimize(cross_entropy)

with tf.name_scope('accuracy'):
    with tf.name_scope('correct_prediction'):
        correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(labels, 1))
    with tf.name_scope('num_correct'):
        num_correct = tf.reduce_sum(tf.cast(correct_prediction, tf.float32))
    with tf.name_scope('accuracy'):
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

tf.summary.scalar('accuracy', accuracy)

###############################################################################################################

sess= tf.Session()

merged = tf.summary.merge_all()
log_path = '/tmp/jet_logs'
train_writer = tf.summary.FileWriter(log_path + '/train', sess.graph)
test_writer = tf.summary.FileWriter(log_path + '/test')

sess.run( tf.global_variables_initializer() )

# load data
data_path = '../data/ttbar_jetshape_Eta2.4_gt50GeV_R0.5_logPt_Zfactor10_48X48_data.pkl'
data_set = input_data(data_path)

for epoch in range(10): #epoch
    print("=============== EPOCH: %d ===============" % (epoch+1))

    # validation accuracy
    # To prevent ResourceExhaustedError, use batches.
    val_batches = get_batch(data=data_set['validation'], batch_size=200)
    val_total = 0
    for val_img, val_lab in val_batches:
        summary, val_num_correct, _ = sess.run([merged, num_correct, accuracy], feed_dict={images : val_img,
                                                                                           labels : val_lab,
                                                                                           keep_prob: 1.0})
        val_total += val_num_correct
        test_writer.add_summary(summary)
    val_acc = val_total / data_set['validation']['num']
    print("epoch ", epoch + 1, "validation accuracy: ", val_acc)
    

    # batch training
    tr_batches = get_batch(data = data_set['training'], batch_size = 200)
    for tr_img, tr_lab in tr_batches:
        summary, _, acc = sess.run([merged, train_step, accuracy], feed_dict = {images : tr_img,
                                                                                labels : tr_lab,
                                                                                keep_prob: 0.5})
        train_writer.add_summary(summary)
        print("training accuracy: ", acc)
train_writer.close()
print("============= E N D ===============")

#################################################################################################################

test_batches = get_batch(data=data_set['test'], batch_size=200)
test_total = 0
for val_img, val_lab in val_batches:
    test_num, _, summary = sess.run([num_correct, accuracy, merged], feed_dict={images : val_img,
                                                                               labels : val_lab,
                                                                               keep_prob: 1.0})
    test_total += test_num
    test_acc = test_total / data_set['test']['num']
    print('test accuracy: ', test_acc)
    test_writer.add_summary(summary)
    
test_writer.close()

sess.close()

