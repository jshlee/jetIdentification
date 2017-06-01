from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import time

import tensorflow as tf

import model
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from input_pipeline import inputs
from drawer import LogDirs

def train(tfrecords_path, tfevents_path, ckpt_path, batch_size, num_epochs):
    with tf.Graph().as_default():
        with tf.name_scope('input'):
            images, labels = inputs(path=tfrecords_path,
                                    batch_size=batch_size,
                                    num_epochs=num_epochs)
        with tf.name_scope('dropout'):
            keep_prob = tf.placeholder(tf.float32)
        logits = model.inference(images, keep_prob)
        prediction = tf.nn.softmax(logits)
        loss = model.loss(logits, labels)
        accuracy = model.evaluation(logits, labels)
        train_op = model.training(loss, learning_rate=0.01)
        init_op = tf.group(tf.global_variables_initializer(),
                           tf.local_variables_initializer())
        # Create a session for running operations in the Graph.
        sess = tf.Session()
        merged = tf.summary.merge_all()
        writer = tf.summary.FileWriter(tfevents_path, sess.graph)
        # Add ops to save and restore all the variables.
        saver = tf.train.Saver(max_to_keep=100000)
        sess.run(init_op)
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)
        step=0
        try:
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
                    saver.save(sess, ckpt_path + '/run', global_step=step)
                step += 1
        except tf.errors.OutOfRangeError:
            print('Done training for %d epochs, %d steps.' % (num_epochs, step))
        finally:
            writer.close()
            # When done, ask the threads to stop.
            coord.request_stop()
        # Wait for threads to finish.
        coord.join(threads)
        sess.close()


if __name__ == '__main__':
    log = LogDirs(dpath = '../../logs/vggnet-0')
    log.mkdirs()
    train(tfrecords_path = '../../data/tfrecords/jet15_rgb_train.tfrecords',
          tfevents_path = log.tfevents_train,
          ckpt_path = log.ckpt,
          batch_size = 100,
          num_epochs=10)
