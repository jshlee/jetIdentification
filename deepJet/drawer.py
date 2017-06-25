from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import datetime
import numpy as np
import tensorflow as tf


def get_date():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M')[2:]


def look_at(obj):
    obj_type = type(obj)
    print(obj_type)
    if obj_type == np.ndarray:
        print(obj.shape)
        print(obj.dtype)
    elif obj_type == tf.Tensor:
        print(obj.get_shape())
        print(obj.dtype)
    elif obj_type == str:
        print(len(obj))
    elif obj_type == tuple:
        print(len(obj))
    elif obj_type == list:
        print(len(obj))
    elif obj_type == dict:
        print(obj.keys())
    else:
        print(":P")


def make_dir(dirpath, del_recur=True):
    if del_recur:
        if tf.gfile.Exists(dirpath):
            print('Delete the existing directory.')
            tf.gfile.DeleteRecursively(dirpath)
    print('Create a directory with the following path.')
    print(dirpath)
    tf.gfile.MakeDirs(dirpath)

class LogDirs:
    def __init__(self, dpath):
        self.dpath = dpath
        self.tfevents = os.path.join(self.dpath, 'tfevents')
        self.tfevents_train = os.path.join(self.tfevents, 'train')
        self.tfevents_test = os.path.join(self.tfevents, 'test')
        self.ckpt = os.path.join(self.dpath, 'ckpt')
        self.roc_curve = os.path.join(self.dpath, 'roc_curve')
    def mkdirs(self):
        make_dir(self.dpath)
        make_dir(self.tfevents)
        make_dir(self.tfevents_train)
        make_dir(self.tfevents_test)
        make_dir(self.ckpt)
        make_dir(self.roc_curve)        


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
