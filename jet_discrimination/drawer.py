import os
import datetime
import tensorflow as tf

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

def make_dirs(dirpath_list, del_recur=True):
    for dirpath in dirpath_list:
        make_dir(dirpath, del_recur)

def ckpt_parser(path):
    with open(os.path.join(path, 'checkpoint')) as f:
        lines = f.readlines()
    result = []
    for l in lines:
        name = l.split('"')[1]
        result.append(os.path.join(path, name))
    return result[1:]
