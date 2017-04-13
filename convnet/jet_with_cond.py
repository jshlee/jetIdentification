from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time

import numpy as np
import tensorflow as tf

from reader import inputs
import convnet
from drawer import get_date
from layer import convolutional_layer, fully_connected_layer 

NUM_EPOCHS = 100

with tf.Graph().as_default():
    with tf.name_scope('input'):
        images, labels = inputs(filename = '../data/tfrecords/jet01.tfrecords',
                                batch_size = 5,
                                num_epochs = NUM_EPOCHS)
    with tf.name_scope('dropout'):
        keep_prob = tf.placeholder(tf.float32)

    logits = convnet.inference(images, keep_prob)

    loss = convnet.loss(logits, labels)

    accuracy = convnet.evaluation(logits, labels)

    train_op = convnet.training(loss, learning_rate=0.001)

    init_op = tf.group(tf.global_variables_initializer(),
                       tf.local_variables_initializer())

    # Create a session for running operations in the Graph.
    sess = tf.Session()

    merged = tf.summary.merge_all()
    log_path = '/tmp/kps/jet_logs_' + get_date()
    train_writer = tf.summary.FileWriter(log_path + '/train', sess.graph)
    test_writer = tf.summary.FileWriter(log_path + '/test')

    sess.run(init_op)

    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)

    try:
        step = 0
        while not coord.should_stop():
            start_time = time.time()
            # training
            summary, _ = sess.run([merged, train_op], feed_dict={keep_prob: 0.5})
            train_writer.add_summary(summary, step)

            duration = time.time() - start_time

            # validation
            if step % 100 == 0:
                summary, acc_value, loss_value = sess.run([merged, accuracy, loss], feed_dict={keep_prob: 1.0})
                test_writer.add_summary(summary, step)
                print('Step %d: loss = %.2f, accuracy = %.3f (%.3f sec)' % (step, loss_value, acc_value, duration))
            step += 1
    except tf.errors.OutOfRangeError:
        print('Done training for %d epochs, %d steps.' % (NUM_EPOCHS, step))
    finally:
        train_writer.close()
        test_writer.close()
        # When done, ask the threads to stop.
        coord.request_stop()
 
    # Wait for threads to finish.
    coord.join(threads)
    sess.close()
