from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import tensorflow as tf

import model
from pipeline import inputs
from eval_utils import ROC
from eval_utils import QGHisto
from vis_cnn import visualize_kernels
from drawer import ckpt_parser


def eval_once(ckpt_path,
              tfrecords_path,
              tfevents_dir,
              roc_dir,
              qg_histo_dir,
              training_step,
              is_training_data=False):
    with tf.Graph().as_default():
        with tf.device('/cpu:0'): 
            with tf.name_scope('input'):
                images, labels = inputs(data_path_list=tfrecords_path,
                                        batch_size=500, num_epochs=1)
        with tf.name_scope('dropout'):
            keep_prob = tf.placeholder(tf.float32)
        logits = model.inference(images, keep_prob)
        prediction = tf.nn.softmax(logits)
        loss = model.loss(logits, labels)
        accuracy = model.evaluation(logits, labels)
        if not is_training_data:
            visualize_kernels()
        # Session
        with tf.Session() as sess:
            merged = tf.summary.merge_all()
            writer = tf.summary.FileWriter(tfevents_dir)
            saver = tf.train.Saver()
            init_op = tf.group(tf.global_variables_initializer(),
                               tf.local_variables_initializer())
            sess.run(init_op)
            saver.restore(sess, ckpt_path)
            # Start the queue runners.
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(sess=sess, coord=coord)
            roc = ROC(dpath=roc_dir,
                      step=training_step,
                      title='Quark/Gluon Discrimination')
            qg_histo = QGHisto(dpath=qg_histo_dir,
                               step=training_step,
                               is_training_data=is_training_data)
            step = 0
            try:
                while not coord.should_stop():
                    labels_np, preds_np, loss_value, acc_value = sess.run(
                        [labels, prediction, loss, accuracy],
                        feed_dict={keep_prob: 1.0}
                    )
                    # roc curve
                    roc.append_data(labels=labels_np[:, 0], preds=preds_np[:, 0])
                    # quark gluon histogram
                    qg_histo.fill(labels=labels_np, preds=preds_np)
                    if step % 20 == 0:
                        summary = sess.run(merged, feed_dict={keep_prob: 1.0})
                        writer.add_summary(summary, step)
                        print('(step: %d) loss = %.3f, acc = %.3f' % (step, loss_value, acc_value))
                    step += 1
            except tf.errors.OutOfRangeError:
                print('%d steps' % step)
            finally:
                roc.finish()
                qg_histo.finish()
                coord.request_stop()
                coord.join(threads)


def evaluate(ckpt_dir,
             training_data,
             validation_data,
             tfevents_dir,
             roc_dir,
             qg_histo_dir,):
    ckpt_list = ckpt_parser(ckpt_dir)
    # writer = tf.summary.FileWriter(tfevents_path)
    for ckpt in ckpt_list:
        # on training set
        eval_once(
            training_step=ckpt['step'],
            ckpt_path=ckpt['path'],
            tfrecords_path=training_data,
            tfevents_dir=tfevents_dir.training,
            is_training_data=True,
            roc_dir=roc_dir.training,
            histogram
        )
        # on validation set
        eval_once(
            training_step=ckpt['step'],
            ckpt_path=ckpt['path'],
            tfrecords_path=validation_data,
            tfevents_dpath=os.path.join(tfevents_dpath, 'validation'),
            is_training_data=False,
            roc_dpath=os.path.join(roc_dpath, 'validation'),
            qg_histo_dpath=os.path.join(qg_histo_dpath, 'validation'),
        )


