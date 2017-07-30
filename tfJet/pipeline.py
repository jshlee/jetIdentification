from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf


'''
ref. https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/how_tos/reading_data/fully_connected_reader.py

ref. https://github.com/visipedia/tfrecords/blob/master/stat_tfrecords.py
    - tf.VarLenFeature(
    - 
'''

def read_and_decode(filename_queue, image_shape=(3, 33, 33), label_shape=(2)):
    # Define a reader
    reader = tf.TFRecordReader()

    # Read the next record
    _, serialized_example = reader.read(queue=filename_queue)

    # Decode the record read by the reader
    features = tf.parse_single_example(
        serialized = serialized_example,
        features = {
            'image': tf.FixedLenFeature([], tf.string),
            'label': tf.FixedLenFeature([], tf.string),
            'jetpT': tf.VarLenFeature(dtype=tf.float32),
            'nMatchedJets': tf.FixedLenFeature([], tf.int64),
            'partonId': tf.FixedLenFeature([], tf.int64),
            # unused vars..
            'nJets': tf.FixedLenFeature([], tf.int64),
            'nGenJets': tf.FixedLenFeature([], tf.int64),
        }
    )

    # images 
    # Convert the image data from string back to the numbers
    image = tf.decode_raw(bytes=features['image'], out_type=tf.float32) # shape=(?,)
    # The image tensor is flattened out, so we have to reconstruct the shape
    image = tf.reshape(tensor = image, shape = image_shape)

    # images
    label = tf.decode_raw(bytes=features['label'], out_type=tf.int64)
    label.set_shape(label_shape)

    jetpT = tf.sparse_tensor_to_dense(features['jetpT'])
    jetpT.set_shape(1)

    infos = {
        'jetpT': jetpT,
        'nMatchedJets': features['nMatchedJets'],
        'partonId': features['partonId'],
        'nJets': features['nJets'],
        'nGenJets': features['nGenJets'],
    }

    return image, label, infos

def inputs(data_path_list, batch_size, num_epochs):
    with tf.name_scope('input'):
        if isinstance(data_path_list, str):
            data_path_list = [data_path_list]
        
        # Create a queue that produces the filenames to read
        # the type of filename_queue is FIFOQueue object
        filename_queue = tf.train.string_input_producer(
            string_tensor=data_path_list,
            num_epochs=num_epochs
        )

        _image, _label, _infos = read_and_decode(filename_queue)

        images, labels, jetpT, nMatchedJets, partonId, nJets, nGenJets = tf.train.shuffle_batch(
            tensors=[ _image, _label, _infos['jetpT'], _infos['nMatchedJets'], _infos['partonId'], _infos['nJets'], _infos['nGenJets']],  # The list or dictionary of tensors to enqueue
            batch_size = batch_size,
            num_threads = 2,  # The number of threads enque
            capacity = 1000 + 3 * batch_size,  # The capacity argument controls the how long the prefetching is allowed to grow the queues.
            min_after_dequeue = 1000  # Minimum number elements in the queue after a dequeue, used to ensure a level of mixing of elements.
        )

    infos = {
        'jetpT': tf.reshape(jetpT, [-1]), # reshape from (500, 1) to (500,)
        'nMatchedJets': nMatchedJets,
        'partonId': partonId,
        'nJets': nJets,
        'nGenJets': nGenJets,
    }

    return images, labels, infos


def main():
    FLAGS = tf.app.flags.FLAGS
    tf.app.flags.DEFINE_string('input_path','../data/tfrecords/jet_training_13503_pT-ALL_eta-ALL_Pythia.tfrecords', 'the path of input data file (.tfrecords format)') 
    with tf.Graph().as_default(), tf.device('/cpu:0'):
        images, labels, infos  = inputs(
            data_path_list=[FLAGS.input_path],
            batch_size=500,
            num_epochs=1
        )
        print('images: ', images)
        print('labels: ', labels)
        print('jetpT: ', infos['jetpT'])
        print('nMatchedJets: ', infos['nMatchedJets'])
        print('partonId: ', infos['partonId'])
        print('\n\n\n\n')

        step = 0
        with tf.Session() as sess:
            init_op = tf.group(tf.global_variables_initializer(),
                               tf.local_variables_initializer())
            sess.run(init_op)
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(sess=sess, coord=coord)
            try:
                while not coord.should_stop():
                    jetpT_np, nMatchedJets_np, partonId_np = sess.run([infos['jetpT'], infos['nMatchedJets'], infos['partonId']])
                    print('jetpT:', jetpT_np[0])
                    print('nMatchedJets:', nMatchedJets_np[0])
                    print('partonId:', partonId_np[0])
                    # break
                    step += 1
            except tf.errors.OutOfRangeError:
                print('%d steps' % step)
            finally:
                coord.request_stop()
                coord.join(threads)

if __name__ == '__main__':
    main()