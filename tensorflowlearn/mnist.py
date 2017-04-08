# coding:utf-8

import tensorflow as tf
import math

NUM_CLASSES = 10
IMAGE_SIZE = 28
IMAGE_PIXELS = IMAGE_SIZE * IMAGE_SIZE

def inference(images, hidden1_units, hidden2_units):
    """构建模型
    :param images: Images placeholder, from inputs()
    :param hidden1_units: 第一个隐藏层的大小
    :param hidden2_units: 第二个隐藏层的大小
    :return: 逻辑回归的输出张量
    """
    # 隐藏层1
    with tf.name_scope('hidden1'):
        weights = tf.Variable(tf.truncated_normal([IMAGE_PIXELS, hidden1_units], stddev=1.0 / math.sqrt(float(IMAGE_PIXELS))), name='weights')
        biases = tf.Variable(tf.zeros([hidden1_units]), name='biases')
        hidden1 = tf.nn.relu(tf.matmul(images, weights) + biases)

    # 隐藏层2
    with tf.name_scope('hidden2'):
        weights = tf.Variable(tf.truncated_normal([hidden1_units, hidden2_units], stddev=1.0 / math.sqrt(float(hidden1_units))), name='weights')
        biases = tf.Variable(tf.zeros([hidden2_units]), name='biases')
        hidden2 = tf.nn.relu(tf.matmul(hidden1, weights) + biases)

    # softmax linear
    with tf.name_scope('softmax_linear'):
        weights = tf.Variable(tf.truncated_normal([hidden2_units, NUM_CLASSES], stddev=1.0 / math.sqrt(float(hidden2_units))), name='weights')
        biases = tf.Variable(tf.zeros([NUM_CLASSES]), name='biases')
        logits = tf.matmul(hidden2_units, weights) + biases

    return logits

# logits是预测的输出，labels是原始数据的label
def loss(logits, labels):
    """
    计算损失
    :param logits: Logits tensor, float - [batch_size, NUM_CLASSES]
    :param labels: Labels tensor, int32 - [batch_size]
    :return: 损失张量 float
    """
    labels = tf.to_int64(labels)
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=labels, logits=logits, name='xentropy')  # 直接计算交叉熵
    return tf.reduce_mean(cross_entropy, name='xentropy_mean')

# loss是损失函数
def training(loss, learning_rate):
    """设置训练参数
    :param loss: 损失函数
    :param learning_rate: 学习速率
    :return: 返回的是训练op
    """
    tf.summary.scalar('loss', loss)  # 可以向事件文件中生成汇总值
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    global_step = tf.Variable(0, name='global_step', trainable=False)
    train_op = optimizer.minimize(loss, global_step=global_step)
    return train_op  # 返回的是训练操作，需要在sess中运行

def evaluation(logits, labels):
    correct = tf.nn.in_top_k(logits, labels, 1)
    return tf.reduce_sum(tf.cast(correct, tf.int32))
