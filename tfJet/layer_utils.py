import tensorflow as tf


def _get_weight(input_dim, output_dim, var_name, initializer):
    if initializer == None:
        initializer = tf.contrib.layers.xavier_initializer
    shape = [input_dim, output_dim]
    return tf.get_variable(var_name, shape, initializer=initializer())


def _get_bias(output_dim, var_name, initializer):
    if initializer == None:
        initializer = tf.contrib.layers.xavier_initializer
    shape = [output_dim]
    return tf.get_variable(var_name, shape, initializer=initializer())


def _get_kernel(input_channels, output_channels, kernel_size, var_name, initializer):
    shape = [kernel_size, kernel_size, input_channels, output_channels]
    if initializer == None:
        initializer = tf.contrib.layers.xavier_initializer_conv2d
    return tf.get_variable(var_name, shape, initializer=initializer())


def create_var(var_type, **kargs):
    '''
    '''
    if 'use_DW' in kargs.keys():
        if kargs['use_DW']:
            kargs['var_name'] += '_DW'

    if 'initializer' not in kargs.keys():
        kargs['initializer'] = None
            
    if var_type == 'weight':
        var = _get_weight(input_dim = kargs['input_dim'],
                          output_dim = kargs['output_dim'],
                          var_name = kargs['var_name'],
                          initializer = kargs['initializer'])
    elif var_type == 'bias':
        var = _get_bias(output_dim = kargs['output_dim'],
                        var_name = kargs['var_name'],
                        initializer = kargs['initializer'])
    elif var_type == 'kernel':
        var = _get_kernel(input_channels = kargs['input_channels'],
                          output_channels = kargs['output_channels'],
                          kernel_size = kargs['kernel_size'],
                          var_name = kargs['var_name'],
                          initializer = kargs['initializer'])
    else:
        raise ValueError(':p')
    return var


def flatten(input_tensor):
    input_shape = input_tensor.get_shape().as_list()
    output_dim = reduce(lambda x, y: x*y, input_shape[1:])
    output_tensor = tf.reshape(tensor=input_tensor, shape=(-1, output_dim))
    return output_tensor


