from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time

import numpy as np
import tensorflow as tf
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

from input_pipeline import inputs
import convnet
from drawer import get_date, make_dir

class ROC:
    def __init__(self):
        self.labels = np.array([])
        self.preds = np.array([]) # predictions
        fig = plt.figure()
    def append_data(self, labels, preds):
        self.labels = np.append(self.labels, labels)
        self.preds = np.append(self.preds, preds)
    def eval_roc(self):
        self.fpr, self.tpr, _ = roc_curve(self.labels, self.preds)
        self.fnr = 1 - self.fpr
        self.auc = auc(self.fpr, self.tpr)
    def plot_roc_curve(self, step, save_path='../data/roc_curve/'):
        plt.plot(self.tpr, self.fnr, color='darkorange',
                 lw=2, label='ROC curve (area = %0.2f)' % self.auc)
        plt.plot([0,1], [1,1], color='navy', lw=2, linestyle='--')
        plt.plot([1,1], [0,1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.1])
        plt.ylim([0.0, 1.1])
        plt.xlabel('Quark Jet Efficiency (TPR)')
        plt.ylabel('Gluon Jet Rejection (FNR)')
        plt.title('ROC curve')
        plt.legend(loc='lower left')
        filename = save_path + 'run-' + str(step) + '.png'
        print(filename)
        plt.show()
        plt.savefig(filename) 


def eval_once(global_step, ckpt_file, writer, tfrecord_file):
    with tf.Graph().as_default() as g:
        with tf.name_scope('input'):
            images, labels = inputs(path=tfrecord_file,
                                    batch_size=300, num_epochs=1)
        with tf.name_scope('dropout'):
            keep_prob = tf.placeholder(tf.float32)
        logits = convnet.inference(images, keep_prob)
        prediction = tf.nn.softmax(logits)
        loss = convnet.loss(logits, labels)
        accuracy = convnet.evaluation(logits, labels)
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
            try:
                step = 0
                while not coord.should_stop():
                    y, y_, loss_value, acc_value = sess.run([labels, prediction, loss, accuracy], feed_dict={keep_prob:1.0})
                    roc.append_data(y[:,0], y_[:,0])
                    if step % 20 == 0:
                        print('(step: %d) loss = %.2f, acc = %.3f' % (step, loss_value, acc_value))
                    step += 1
            except tf.errors.OutOfRangeError:
                print('%d steps' % step)
            finally:
                roc.eval_roc()
                roc.plot_roc_curve(global_step)
                coord.request_stop()
                coord.join(threads)


def evaluate(ckpt_list, tfevent_file, tfrecord_file):
    writer = tf.summary.FileWriter(tfevent_file)
    global_step = 1
    for ckpt in ckpt_list:
        eval_once(global_step, ckpt, writer, tfrecord_file)
        global_step += 1
    else:
        writer.close()
