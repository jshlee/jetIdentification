from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf

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


