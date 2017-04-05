# coding:utf-8

import tensorflow.python.platform
import tensorflow as tf

from tensorflow.python.platform import gfile

IMAGE_SIZE = 24  # 和原始图片的大小是不一样的

# 描述数据集的全局常量
NUM_CLASSES = 10
NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN = 50000
NUM_EXAMPLES_PER_EPOCH_FOR_EVAL = 10000

def read_cifar10(filename_queue):
    """读取并解析examples
    Args:
        filename_queue: 文件名的字符串队列
    :returns
        代表了一个样本的对象：
        height: number of rows in the result(32)
        width: number of columns in the result 32
        depth: number of color channels in the result 3
        key: a scalar string Tensor describing the filename & record number for this example.
        label: an int32 Tensor with the label in the range 0..9
        uint8image: a [height, width, depth] uint Tensor with the image data
    """
    class CIFAR10Record(object):
        pass
    result = CIFAR10Record()

    label_bytes = 1
    result.height = 32
    result.width = 32
    result.depth = 3
    image_bytes = result.height * result.width * result.depth
    record_bytes = label_bytes + image_bytes

    reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)
    result.key, value = reader.read(filename_queue)

    record_bytes = tf.decode_raw(value, tf.uint8)  # 将读到的字符串转化为数字
    result.label = tf.cast(tf.slice(record_bytes, [0], [label_bytes]), tf.int32)

    depth_major = tf.reshape(tf.slice(record_bytes, [label_bytes], [image_bytes]), [result.depth, result.height, result.width])
    result.uint8image = tf.transpose(depth_major, [1, 2, 0])  # [depth, height, width] to [height, width, depth].
    return result

def _generate_image_and_label_batch(image, label, min_queue_examples, batch_size):
    """
    构造images and labels的队列
    :param image: 3-D Tensor of [height, width, 3] of type. float32
    :param label: 1-D Tensor of type.int32
    :param min_queue_examples: int32, minimum number of samples to retain in the queue that provides of batches of examples.
    :param batch_size: Number of images per batch
    :return:
        images: Images. 4D tensor of [batch_size, height, width, 3] size.
        labels: Labels. 1D tensor of [batch_size] size
    """
    num_preprocess_threads = 16
    images, label_batch = tf.train.shuffle_batch([image, label], batch_size=batch_size, num_threads=num_preprocess_threads, capacity=min_queue_examples + 3*batch_size, min_after_dequeue=min_queue_examples)
    tf.image_summary('images', images)
    return images, tf.reshape(label_batch, [batch_size])

