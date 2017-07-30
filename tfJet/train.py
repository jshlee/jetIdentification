from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import time

import tensorflow as tf
import pandas as pd

import model
from pipeline import inputs
from evaluation import evaluate
from eval_utils import draw_all_qg_histograms
from utils import get_log_dir

def train(tfrecords_path,
          tfevents_dir,
          ckpt_dir,
          benchmark_path,
          batch_size=500,
          num_epochs=20):
    """
    ref. https://www.tensorflow.org/get_started/mnist/mechanics
    ref. https://github.com/tensorflow/models/blob/master/tutorials/image/cifar10/cifar10_train.py

    """
    with tf.Graph().as_default():
        # Get images and labels for jet discrimination
        # Force input pipeline to CPU:0 to avoid operations sometimes ending up on GPU and resulting in a slow down.
        with tf.device('/cpu:0'):
            images, labels, _ = inputs(
                data_path_list=tfrecords_path,
                batch_size=batch_size,
                num_epochs=num_epochs
            )
        with tf.name_scope('dropout'):
            keep_prob = tf.placeholder(tf.float32)

        # Build a Graph that computes the logits predictions from the inference model.
        logits = model.inference(images, keep_prob)
        # Bulid a Graph that computes the softmax predictions
        # to computes ROC curves.
        prediction = tf.nn.softmax(logits)

        # Calculate loss and accuracy
        loss = model.loss(logits, labels)
        accuracy = model.evaluation(logits, labels)

        train_op = model.training(loss, lr=0.001)
        init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
        # Create a session for running operations in the Graph.
        sess = tf.Session()
        merged = tf.summary.merge_all()
        writer = tf.summary.FileWriter(tfevents_dir, sess.graph)
        # Add ops to save and restore all the variables.
        saver = tf.train.Saver(max_to_keep=100000)
        sess.run(init_op)
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)
        step = 0
        benchmark = pd.DataFrame(columns=['training_time'])
        print('\n\n\n', time.asctime())
        try:
            while not coord.should_stop():
                start_time = time.time()
                # training
                _ = sess.run(train_op, feed_dict={keep_prob: 0.5})
                duration = time.time() - start_time
                benchmark.loc[step] = {'training_time': duration}
                # write summary and print loss
                if step % 100 == 0:
                    # Record execution stats
                    run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
                    run_metadata = tf.RunMetadata()
                    summary, acc_value, loss_value, labels_np, preds_np = sess.run(
                        [merged, accuracy, loss, labels, prediction],
                        feed_dict={keep_prob: 1.0}, options=run_options, run_metadata=run_metadata
                    )
                    writer.add_summary(summary, step)
                    writer.add_run_metadata(run_metadata, 'step%d' % step)
                    print('Step %d: loss = %.2f, accuracy = %.3f (%.3f sec)' % (step, loss_value, acc_value, duration))
            
                if step % 1000 == 0:
                    ckpt_path = os.path.join(ckpt_dir, 'step')
                    saver.save(sess, ckpt_path, global_step=step)
                step += 1
        except tf.errors.OutOfRangeError:
            print('Done training for %d epochs, %d steps.' % (num_epochs, step))
        finally:
            writer.close()
            # When done, ask the threads to stop.
            coord.request_stop()
            # 
            benchmark.to_csv(os.path.join(benchmark_path, 'benchmark.csv'), index_label='#step')
        # Wait for threads to finish.
        coord.join(threads)
        sess.close()


def main(argv=None):
    FLAGS = tf.app.flags.FLAGS
    tf.app.flags.DEFINE_string(
        'training_data',
        '../data/tfrecords/jet_training_8101_pT-ALL_eta-ALL_Pythia.tfrecords',
        'the training data set'
    )
    tf.app.flags.DEFINE_string(
        'validation_data',
        '../data/tfrecords/jet_validation_2701_pT-ALL_eta-ALL_Pythia.tfrecords',
        'the validation data set'
    )
    tf.app.flags.DEFINE_integer('batch_size', 500, 'batch size')
    tf.app.flags.DEFINE_integer('num_epochs', 30, 'the number of epochs')

    log_dir = get_log_dir(dname='test', creation=True)

    train(
        tfrecords_path=FLAGS.training_data,
        tfevents_dir=log_dir.tfevents.training.path,
        ckpt_dir=log_dir.ckpt.path,
        benchmark_path=log_dir.path,
        batch_size=FLAGS.batch_size,
        num_epochs=FLAGS.num_epochs
    )
   
    evaluate(
        training_data=FLAGS.training_data,
        validation_data=FLAGS.validation_data,
        log_dir=log_dir
    )

    draw_all_qg_histograms(qg_histogram_dir=log_dir.qg_histogram)
 

if __name__ == '__main__':
    main()
