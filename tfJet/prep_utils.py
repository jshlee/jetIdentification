from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from sklearn import preprocessing

from pipeline import inputs

def load_npz(path):
    container = np.load(path)
    return [container[key] for key in container]


def fill(ndarr, deta, dphi, entry, bin=33, deta_max=0.4, dphi_max=0.4):
    if deta == deta_max:
        x_idx = bin - 1
    else:
        x = deta + deta_max
        dx = 2 * deta_max / bin
        x_idx = int(x/dx)
    
    if dphi == dphi_max:
        y_idx = bin - 1
    else:
        y = (dphi + dphi_max)
        dy = 2 * dphi_max / bin
        y_idx = int(y/dy)
    ndarr[x_idx][y_idx] += entry


def fill_v2(ndarr, deta, dphi, entry, bin_num, deta_max=0.4, dphi_max=0.4):
    def _bar(dx, dx_max):
        if dx == dx_max:
            return bin_num - 1
        else:
            return int((dx+dx_max) / (2*dx_max/bin_num))
    row = _bar(deta, deta_max)
    col = _bar(dphi, dphi_max)
    ndarr[row][col] += entry


def _decompose(img):
    c, h, w = img.shape[1:]
    return [img[:, i, :].reshape(-1, h*w) for i in range(c)]


def normalize(img):
    c, h, w = img.shape[1:]
    img_norm = None
    for x in _decompose(img):
        temp = preprocessing.normalize(x, norm='l1', axis=1).reshape(-1, 1, h*w) 
        if img_norm is None:
            img_norm = temp
        else:
            img_norm = np.c_[img_norm, temp]
    return img_norm.reshape(-1, c, h, w)


def standardize(img, noise=1e-5):
    n, c, h, w = img.shape
    img_stdzn = None
    for x in _decompose(img):
        mean = x.mean(axis=1)
        std = x.std(axis=1)
        x_stdzn = np.array(map(lambda _x, _mean, _std: (_x-_mean)/(_std+noise), x, mean, std))
        if img_stdzn is None:
            img_stdzn = x_stdzn
        else:
            img_stdzn = np.c_[img_stdzn, x_stdzn]
    return img_stdzn.reshape(-1, c, h, w)


def test_tfrecords(path):
    with tf.Graph().as_default(), tf.device('/cpu:0'):
        images, labels, _ = inputs
