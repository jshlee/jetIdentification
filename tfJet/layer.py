import tensorflow as tf
from layer_utils import create_var
from layer_utils import flatten

def fc_layer(input_tensor, output_dim, layer_name, DW=True, act_ftn=tf.nn.relu):
    input_dim = input_tensor.get_shape().as_list()[-1]

    with tf.variable_scope(layer_name):
        W = create_var(var_type='weight', input_dim=input_dim, output_dim=output_dim, var_name='weight', DW=DW)
        b = create_var(var_type='bias', output_dim=output_dim, var_name='bias')
        preactivate = tf.nn.bias_add(tf.matmul(input_tensor, W), b)
        output_tensor = act_ftn(preactivate, name='activation')

    return output_tensor


def conv_layer(input_tensor, output_channels, layer_name,
               stride=1,kernel_size=3, DW=False, VK=True):
    input_channels = input_tensor.get_shape().as_list()[1]

    with tf.variable_scope(layer_name):
        kernel = create_var(var_type='kernel', input_channels=input_channels, output_channels=output_channels, kernel_size=kernel_size, var_name='kernel', DW=DW)
        strides = [1, 1, stride, stride]
        preactivate = tf.nn.conv2d(input = input_tensor, filter = kernel, strides = strides, padding = 'SAME', data_format='NCHW')
        output_tensor = tf.nn.relu(preactivate)

    return output_tensor


def bn_layer(input_tensor, output_dim, name, bn_epsilon=0.001, data_format='NCHW'):
    with tf.variable_scope(name):
        mean, variance = tf.nn.moments(input_tensor, axes=[0, 2, 3])
        beta = tf.get_variable('beta', output_dim, tf.float32,
                               initializer=tf.constant_initializer(0.0, tf.float32))
        gamma = tf.get_variable('gamma', output_dim, tf.float32,
                                initializer=tf.constant_initializer(1.0, tf.float32))
        bn_layer = tf.nn.batch_normalization(input_tensor, mean, variance, beta, gamma, bn_epsilon)

    return bn_layer

 
def max_pooling_layer(input_tensor, layer_name, k=2, s=2):
    """

    """
    ksize = [1, 1, k, k]
    strides = [1, 1, s, s]

    with tf.name_scope(layer_name):
        output_tensor = tf.nn.max_pool(input_tensor, ksize=ksize , strides=strides, padding='SAME', data_format='NCHW')
    return output_tensor

def gap_layer(input_tensor, layer_name):
    """
    global average pooling
    ref. Min Lin, Qiang Chen, Shuicheng Yan. Network In Network. arXiv:1312.4400
    """
    shape = input_tensor.get_shape().as_list()
    H, W = shape[2:]
    ksize = strides = [1, 1, H, W]

    with tf.variable_scope(layer_name):
        unflattened = tf.nn.avg_pool(input_tensor, ksize=ksize, strides=strides, padding='SAME', data_format='NCHW')
        output_tensor = flatten(unflattened)

    return output_tensor

def maxout(input_tensor, layer_name):
    input_dim = input_tensor.get_shape().as_list()[-1]
    with tf.variable_scope():
        pass
        


def vgg_module(input_tensor, num_block, module_name):
    '''
      full pre-activation
      NCHW format

      cin = the channels of the input tensor
      cout = the channels of the output tensor

      tin = the input tensor
      tout = the output tensor
    '''
    input_channels = input_tensor.get_shape().as_list()[1]
    output_channels = 2 * input_channels
    output_tensor = input_tensor

    with tf.variable_scope(module_name):
        for i in range(num_block):
            # batch normalization
            bn_name = 'bn-%d_in_%s' %(i, module_name)
            output_tensor = tf.contrib.layers.batch_norm(output_tensor, fused=True, data_format='NCHW')
            print(bn_name, output_tensor.get_shape())
            # activation
            output_tensor = tf.nn.relu(output_tensor)
            # convolution
            conv_name = 'conv-%d_in_%s' % (i, module_name)
            output_tensor = conv_layer(output_tensor, output_channels,layer_name=conv_name)
            print(conv_name, output_tensor.get_shape())
        # pooling layer
        output_tensor = tf.nn.max_pool(output_tensor, ksize=[1, 1, 2, 2] , strides=[1, 1, 2, 2], padding='SAME', data_format='NCHW')
        print('max_pooling in ', module_name, output_tensor.get_shape())

    return output_tensor


def resnet_module(input_tensor):
    pass


# inception module, naive version
def inception_module_naive(input_tensor, channels, module_name):
    with tf.variable_scope(module_name):
        conv1x1 = conv_layer(input_tensor=input_tensor, kernel_size=1, output_channels=channels['conv1x1'], layer_name='conv1x1')
        conv3x3 = conv_layer(input_tensor=input_tensor, kernel_size=3, output_channels=channels['conv3x3'], layer_name='conv3x3')
        conv5x5 = conv_layer(input_tensor=input_tensor, kernel_size=5, output_channels=channels['conv5x5'], layer_name='conv5x5')
        pool3x3 = max_pooling_layer(input_tensor, layer_name='max_pool3x3', k=3, s=1)

        # axis: channels
        output_tensor = tf.concat(values=[conv1x1, conv3x3, conv5x5, pool3x3], axis=1)

    return output_tensor


# Inception module with dimension reductions
def inception_module_v1(input_tensor, channels, module_name):
    with tf.variable_scope(module_name):
        with tf.variable_scope('branch1x1'):
            branch1x1 = conv_layer(input_tensor=input_tensor, kernel_size=1, output_channels=channels['#1x1'], layer_name='conv1x1')
        with tf.variable_scope('branch3x3'):
            branch3x3 = conv_layer(input_tensor=input_tensor, kernel_size=1, output_channels=channels['#3x3_reduce'], layer_name='conv1x1')
            branch3x3 = conv_layer(input_tensor=branch3x3, kernel_size=3, output_channels=channels['#3x3'], layer_name='conv3x3')
        with tf.variable_scope('branch5x5'):
            branch5x5 = conv_layer(input_tensor=input_tensor, kernel_size=1, output_channels=channels['#5x5_reduce'], layer_name='conv1x1')
            branch5x5 = conv_layer(input_tensor=branch5x5, kernel_size=5, output_channels=channels['#5x5'], layer_name='conv5x5')
        with tf.variable_scope('branch1x1'):
            branch_pool = max_pooling_layer(input_tensor, layer_name='max_pool3x3', k=3, s=1)
        output_tensor = tf.concat([branch1x1, branch3x3, branch5x5, branch_pool], axis=1)
    return output_tensor


# factorizing inception module
def inception_module_v2(input_tensor, channels, module_name):
    pass

def dense_net_module():
    pass