from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import datetime
import tensorflow as tf
from tensorflow.python.client import device_lib


def get_date():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M')[2:]


def make_dir(dirpath, del_recur=True):
    if del_recur:
        if tf.gfile.Exists(dirpath):
            print('Delete the existing directory.')
            tf.gfile.DeleteRecursively(dirpath)
    print('Create a directory with the following path.')
    print(dirpath)
    tf.gfile.MakeDirs(dirpath)



class Directory(object):
    def __init__(self, path, creation=True):
        self.path = path
        if creation:
            tf.gfile.MakeDirs(path)

    def make_subdir(self, dname, creation=True):
        subdpath = os.path.join(self.path, dname)
        setattr(self, dname, Directory(subdpath))
        if creation:
            tf.gfile.MakeDirs(subdpath)

    def __repr__(self):
        return self.path


def get_log_dir(dname, creation=True, logs_dpath='./logs'):
    # numbering
    dlist = os.listdir('./logs')
    dlist.sort()
    if len(dlist) == 0:
        dname = '%s_01' % dname
    else:
        latest_dir = dlist[-1]
        latest_num = latest_dir.split('_')[-1]
        latest_num = int(latest_num) + 1
        dname = '%s_%s'% (dname, str(latest_num).zfill(2))
    dpath = os.path.join(logs_dpath, dname)
    # mkdir
    log = Directory(dpath)
    log.make_subdir('tfevents', creation)
    log.make_subdir('ckpt', creation)
    log.make_subdir('roc', creation)
    log.make_subdir('qg_histogram', creation)
    for sub in [log.tfevents, log.roc, log.qg_histogram]:
        sub.make_subdir('training', creation)
        sub.make_subdir('validation', creation)
    return log


def ckpt_parser(path, with_step=True):
    with open(os.path.join(path, 'checkpoint')) as f:
        lines = f.readlines()[1:]
    result = []
    if with_step:
        for l in lines:
            name = l.split('"')[1]
            step = int(name.split('-')[1])
            result.append({'path': os.path.join(path, name), 'step': step})
        return result
    else:
        for l in lines:
            name = l.split('"')[1]
            result.append(os.path.join(path, name))
        return result


def get_available_device(device_type=None):
    ''' ref. https://stackoverflow.com/questions/38559755/how-to-get-current-available-gpus-in-tensorflow '''
    local_device_protos = device_lib.list_local_devices()
    if device_type:
        device_list = [x.name for x in local_device_protos if x.device_type == device_type]
    else:
        device_list = [x.name for x in local_device_protos]
    return device_list 



def parse_tfrecords_fname(path):
    fname = os.path.split(path)[1]
    splitted = fname.split('_')
    info = {}
    info['num'] = splitted[1]
    info['format'] = splitted[2]
    info['preprocessing'] = splitted[3].split('-')
    info['tag'] = splitted[4].split('.')[0]
    return info
