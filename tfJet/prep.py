from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import time
import ROOT
import numpy as np
import tensorflow as tf

from prep_utils import fill


def root_to_np(input_path, tree_name="jetAnalyser/jetAnalyser",
               C=3, H=33, W=33, deta_max=0.4, dphi_max=0.4):
    '''
    NCHW format
    N : the number of jet
    C : channel (0: cpt, 1: npt, 2: cmu)
    H : height (~
    W : width (~the number of column)

    info = [pT, nJets, nGenJets]


    '''
    tfile = ROOT.TFile(input_path, "READ")
    jet = tfile.Get(tree_name)
    entries = jet.GetEntriesFast()
    images = []
    labels = []
    jetpT = []
    nMatchedJets = []
    nJets = []
    nGenJets = []
    partonId = []
    for j in xrange(entries):
        if j % 1000 == 0:
            print('( %s ) %dth jet' % (time.asctime(), j))
        jet.GetEntry(j)

        # label (onehot encoding)
        # gluon: background
        if jet.partonId == 21:
            labels.append([[0, 1]])
        # light quark ~ signal
        elif jet.partonId in [1, 2, 3]:
            labels.append([[1, 0]])
        else:
            continue

        # make a jet images
        img = np.zeros(shape=(C, H, W), dtype=np.float32)
        for d in xrange(len(jet.dau_pt)):
            ''' if False not in (-0.4 < jet.deta[d], jet.dphi[d] < 0.4) '''
            if (-deta_max < jet.dau_deta[d] < deta_max) and (-dphi_max < jet.dau_dphi[d] < dphi_max):
                # neutral particle
                if jet.dau_charge[d]:
                    # pT
                    fill(img[1], jet.dau_deta[d], jet.dau_dphi[d], jet.dau_pt[d], H)
                # charged particle
                else:
                    # pT
                    fill(img[0], jet.dau_deta[d], jet.dau_dphi[d], jet.dau_pt[d], H)
                    # multiplicity
                    fill(img[2], jet.dau_deta[d], jet.dau_dphi[d], 1, H)
        images.append(img)

        # jet information
        jetpT.append(jet.pt)
        nMatchedJets.append(jet.nMatchedJets)
        nJets.append(jet.nJets)
        nGenJets.append(jet.nGenJets)
        partonId.append(jet.partonId)
 
    images = np.array(images, dtype=np.float32)
    labels = np.array(labels, dtype=np.int64)
    info = {
        'jetpT': np.array(jetpT, dtype=np.float64),
        'nMatchedJets': np.array(nMatchedJets, dtype=np.int64),
        'nJets': np.array(nJets, dtype=np.int64),
        'nGenJets': np.array(nGenJets, dtype=np.int64),
        'partonId': np.array(partonId, dtype=np.int64)
    }
    return images, labels, info


def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _float_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def np_to_tfrecords(images, labels, info, output_path):
    # Open the TFRecords file
    writer = tf.python_io.TFRecordWriter(output_path)
    for i in xrange(images.shape[0]):
        # only length-1 array can be converted to Python scalars.
        image_raw = images[i].tostring()
        label_raw = labels[i].tostring()
        feature = {
            # Convert data into the proper data type of the feature using tf.traid.<DATA_TYPE>List
            'image': _bytes_feature(tf.compat.as_bytes(image_raw)),
            'label': _bytes_feature(tf.compat.as_bytes(label_raw)),
            'jetpT': _float_feature(info['jetpT'][i]),
            'nMatchedJets': _int64_feature(info['nMatchedJets'][i]),
            'partonId': _int64_feature(info['partonId'][i]),
            'nJets': _int64_feature(info['nJets'][i]),
            'nGenJets': _int64_feature(info['nGenJets'][i]),
        }
        # Create a feature using tf.train.Feature and pass the converted data to it.
        # Create an Example protocol buffer using tf.train.Example and pass the converted data to it.
        example = tf.train.Example(features=tf.train.Features(feature=feature))
        # Serialize the Example to string using example.SerializeToString()
        # Write the serialized example to TFRecords file using writer.write
        writer.write(example.SerializeToString())
    # Close the file
    writer.close()


'''
def _pt_binning(images, labels, info, range_list, fname, output_dir='./data'):
    fname_format = '%s_%d_to_%d'
    path = os.path.join(output_dir, fname_format)
    for lower, upper in range_list:
        cond = np.logical_and(
            info[qgjic.INFO_NAMES=='pT'] > lower,
            info[qgjic.INFO_NAMES=='pT'] < upper
        )
        np.savez(
            path % (fname, lower, upper),
            images=images[cond],
            labels=labels[cond],
            info=info[cond]
        )
'''
def split_dataset():
    FLAGS = tf.app.flags.FLAGS
    tf.app.flags.DEFINE_string('input_path', '../data/root/jet_pythia_1.root', 'the path of input file (.root format file)')
    images, labels, info = root_to_np(FLAGS.input_path)

    total = images.shape[0]
    # start index for each dataset
    # i.e. training_idx = o
    val_idx = int(total*0.6)
    test_idx = int(total*0.8)

    idx_list = [(0, val_idx), (val_idx, test_idx), (test_idx, None)]
    tag_list = ['training', 'validation', 'test']

    for (start_idx, end_idx), tag in zip(idx_list, tag_list):
        images_to_save = images[start_idx: end_idx]
        labels_to_save = labels[start_idx: end_idx]

        info_to_save = {
            'jetpT': info['jetpT'][start_idx: end_idx],
            'nJets': info['nJets'][start_idx: end_idx],
            'nMatchedJets': info['nMatchedJets'][start_idx: end_idx],
            'nGenJets': info['nGenJets'][start_idx: end_idx],
            'partonId': info['partonId'][start_idx: end_idx],

        }

        num_example = images_to_save.shape[0]

        fname = 'jet_%s_%d_pT-ALL_eta-ALL_Pythia' % (tag, num_example)

        npz_path = os.path.join('../data/npz', fname)
        np.savez(
            npz_path,
            images=images_to_save,
            labels=labels_to_save,
            jetpT=info_to_save['jetpT'],
            nMatchedJets=info_to_save['nMatchedJets'],
            partonId=info_to_save['partonId'],
            nJets=info_to_save['nJets'],
            nGenJets=info_to_save['nGenJets'],
        )

        # Convert numpy array (ndarray object) to .tfrecords
        tfrecords_path = os.path.join('../data/tfrecords', fname+'.tfrecords')
        np_to_tfrecords(images_to_save, labels_to_save, info_to_save, output_path=tfrecords_path)


def main():
    FLAGS = tf.app.flags.FLAGS
    tf.app.flags.DEFINE_string('input_path', '../data/root/jet_pythia_1.root', 'the path of input file (.root format file)')
    images, labels, info = root_to_np(FLAGS.input_path)

    fname = 'jet_training_%d_pT-ALL_eta-ALL_Pythia' % images.shape[0]

    npz_path = os.path.join('../data/npz', fname)
    np.savez(
        npz_path,
        images=images,
        labels=labels,
        jetpT=info['jetpT'],
        nJets=info['nJets'],
        nMatchedJets=info['nMatchedJets'],
        nGenJets=info['nGenJets'],
        partonId=info['partonId']
    )

    # Convert numpy array (ndarray object) to .tfrecords
    tfrecords_path = os.path.join('../data/tfrecords', fname+'.tfrecords')
    np_to_tfrecords(images, labels, info, output_path=tfrecords_path)


if __name__ == '__main__':
    split_dataset()
