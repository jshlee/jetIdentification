import tensorflow as tf

'''
ref. https://www.tensorflow.org/api_docs/python/tf/summary/image

tf.summary.image(
    name,
    tensor,
    max_output=3,
    collections=None

Outputs a Summary protocol buffer with images.

The images are built from tensor
which must be 4-D with shape [batch_size, height, width, channels] and where channels can be:
    - 1: tensor is interpreted as Grayscale.
    - 3: tensor is interpreted as RGB.
    - 4: tensor is interpreted as RGBA.

    - If the input values are all positive, they are rescaled so the largest one is 255.
    - If any input value is negative, the values are shifted so input value 0.0 is at 127.
      They are then rescaled so that either the smallest value is 0, or the largest one is 255.
'''


def visualize_kernels(vis_tag='VK'):
    kernels = filter(lambda kernel: vis_tag in kernel.name, tf.trainable_variables())
    # Transpose kernels
    #
    # original kernel shape, [k, k, i, o] ---> transposed kernel shape, [o, k, k, i]
    transposed = map(lambda kernel: tf.transpose(kernel, [3, 0, 1, 2]), kernels)
    for i in range(len(transposed)):
        summ_name = transposed[i].name + '_image_summary'
        output_channels = transposed[i].get_shape().as_list()[0]
        tf.summary.image(name=summ_name, tensor=[i], max_outputs=output_channels)


def visualize_jet_image():
    pass
