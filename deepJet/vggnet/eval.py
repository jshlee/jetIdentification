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
from roc import ROC
from drawer import get_date, make_dir, ckpt_parser

def eval_once(global_step, ckpt_file, writer, tfrecord_file, roc_path):
    with tf.Graph().as_default() as g:
        with tf.name_scope('input'):
            images, labels = inputs(path=tfrecord_file,
                                    batch_size=300, num_epochs=1)
        with tf.name_scope('dropout'):
            keep_prob = tf.placeholder(tf.float32)
        logits = model.inference(images, keep_prob)
        prediction = tf.nn.softmax(logits)
        loss = model.loss(logits, labels)
        accuracy = model.evaluation(logits, labels)
        # Session
        with tf.Session() as sess:
            saver = tf.train.Saver()
            init_op = tf.group(tf.global_variables_initializer(),
                               tf.local_variables_initializer())
            sess.run(init_op)
            saver.restore(sess, ckpt_file)
            # Start the queue runners.
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(sess=sess, coord=coord)
            roc = ROC()
            step = 0
            try:
                while not coord.should_stop():
                    y, y_, loss_value, acc_value = sess.run([labels, prediction, loss, accuracy],
                                                            feed_dict={keep_prob:1.0})
                    roc.append_data(y[:,0], y_[:,0])
                    if step % 20 == 0:
                        print('(step: %d) loss = %.2f, acc = %.3f' % (step, loss_value, acc_value))
                    step += 1
            except tf.errors.OutOfRangeError:
                print('%d steps' % step)
            finally:
                roc.eval_roc()
                roc.plot_roc_curve(step=global_step, title='VGGNet', save_path=roc_path)
                coord.request_stop()
                coord.join(threads)

def evaluate(ckpt_path, tfevents_path, tfrecords_path, roc_path):
    ckpt_list = ckpt_parser(ckpt_path)
    writer = tf.summary.FileWriter(tfevents_path)
    for ckpt in ckpt_list:
        eval_once(global_step = ckpt['step'],
                  ckpt_file = ckpt['path'],
                  writer = writer,
                  tfrecord_file = tfrecords_path,
                  roc_path = roc_path)
    else:
        writer.close()

if __name__ == '__main__':
    log = LogDirs(dpath = '../../logs/vggnet-0')
    evalutate(ckpt_path = log.ckpt,
              tfevents_path = log.tfevents,
              tfrecords_path = '../../data/tfrecords/jet15_rgb_validation.tfrecords',
              roc_path = log.roc_curve)
