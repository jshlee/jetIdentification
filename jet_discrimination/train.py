from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time

import numpy as np
import tensorflow as tf

from input_pipeline import inputs
import convnet
from drawer import get_date, make_dirs
from layer import convolutional_layer, fully_connected_layer 

NUM_EPOCHS = 100
BATCH_SIZE = 300
TFRECORDS_PATH = '../data/tfrecords/jet15_rgb_train.tfrecords'
TFEVENTS_PATH = '../data/tfevents/run1/train'
CKPT_PATH = '../data/ckpt/run1'
make_dirs([TFEVENTS_PATH, CKPT_PATH])

#######################################################################3

with tf.Graph().as_default():
    with tf.name_scope('input'):
        images, labels = inputs(path=TFRECORDS_PATH,
                                batch_size=BATCH_SIZE,
                                num_epochs=NUM_EPOCHS)
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
    writer = tf.summary.FileWriter(TFEVENTS_PATH, sess.graph)

    # Add ops to save and restore all the variables.
    saver = tf.train.Saver(max_to_keep=100000)

    sess.run(init_op)

    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)

    try:
        step = 0
        while not coord.should_stop():
            start_time = time.time()
            # training
            _ = sess.run(train_op, feed_dict={keep_prob: 0.5})
            duration = time.time() - start_time

            # write summary and print loss
            if step % 100 == 0:
                summary, acc_value, loss_value = sess.run([merged, accuracy, loss],
                                                 feed_dict={keep_prob: 1.0})
                writer.add_summary(summary, step)
                print('Step %d: loss = %.2f, accuracy = %.3f (%.3f sec)' % (step, loss_value, acc_value, duration))
            if step % 1000 == 0:
                saver.save(sess, CKPT_PATH+'/run', global_step=step)
            step += 1
    except tf.errors.OutOfRangeError:
        print('Done training for %d epochs, %d steps.' % (NUM_EPOCHS, step))
    finally:
        writer.close()
        # When done, ask the threads to stop.
        coord.request_stop()
    # Wait for threads to finish.
    coord.join(threads)
    sess.close()
