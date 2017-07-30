from __future__ import absolute_import
from __future__ import division 
from __future__ import print_function

import os

import tensorflow as tf

from train import train
from eval import evaluate
from drawer import LogDirs, name_logdir 

flags = tf.app.flags
FLAGS = flags.FLAGS
# flags.DEFINE_<TYPE>(flag_name, default_value, docstring)
flags.DEFINE_integer('batch_size', 500, 'batch_size')
flags.DEFINE_integer('num_epochs', 30, 'epochs')
flags.DEFINE_boolean('only_eval', False, 'only evaluation')

tr_data_path = '../data/tfrecords/jet_images_163086_NCHW_training.tfrecords'
val_data_path = '../data/tfrecords/jet_images_54362_NCHW_validation.tfrecords'


# Make log dir
if FLAGS.only_eval:
    logdir = LogDirs(dpath='/home/slowmoyang/Lab/jetIdentification/labmeeting/logs/labmeeting-GPU-01')
    # Evaluate the model
    evaluate(
        training_data=tr_data_path,
        validation_data=val_data_path,
        tfevents_dpath=logdir.tfevents_validation,
        ckpt_dpath=logdir.ckpt,
        roc_dpath=logdir.roc,
        qg_histo_dpath=logdir.qg_histo,
    )

else:
    log_path = os.path.join('./logs/', log_dname)
    logdir = LogDirs(dpath=log_path)
    logdir.mkdirs()
    # Train the model
    train(
        tfrecords_path=tr_data_path,
	tfevents_dpath=logdir.tfevents_training,
        ckpt_dpath=logdir.ckpt,
        benchmark_path=os.path.join(logdir.dpath, 'benchmark.csv'),
        batch_size=FLAGS.batch_size,
        num_epochs=FLAGS.num_epochs,
        )

    # Evaluate the model
    evaluate(
        training_data=tr_data_path,
        validation_data=val_data_path,
        tfevents_dpath=logdir.tfevents_validation,
        ckpt_dpath=logdir.ckpt,
        roc_dpath=logdir.roc,
        qg_histo_dpath=logdir.qg_histo,
    )


