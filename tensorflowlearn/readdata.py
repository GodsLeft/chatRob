# coding:utf-8

import tensorflow as tf
import numpy as np

def readmyfile(filenamequeue):
    reader = tf.TextLineReader()
    key, value = reader.read(filenamequeue)  # key表征输入的文件和其中的记录
    record_defaults = [[1.0], [1.0], [1.0], [1.0]]  # 指定矩阵格式以及数据类型
    col1, col2, col3, col4 = tf.decode_csv(value, record_defaults=record_defaults)
    # features = tf.pack([col1, col2])
    features = tf.concat([[col1], [col2], [col4]], 0)
    label = col3
    return features, label

def inputpipeline(filenames=["1.csv", "2.csv"], batchSize=4, numEpochs=None):
    # 如果多次迭代，会产生均匀的文件名列表，背后有QueueRunner作用
    filenamequeue = tf.train.string_input_producer(filenames, num_epochs=numEpochs)  # 生成文件名队列,epoch过几遍训练数据

    # 在这里选择合适的阅读器，并调用read方法
    example, label = readmyfile(filenamequeue)
    min_after_dequeue = 8
    capacity = min_after_dequeue + 3*batchSize

    # 创建一批数据
    examplebatch, labelbatch = tf.train.shuffle_batch([example, label],
                                                      batch_size=batchSize,
                                                      num_threads=3,
                                                      capacity=capacity,
                                                      min_after_dequeue=min_after_dequeue)
    return examplebatch, labelbatch

featurebatch, labelbatch = inputpipeline(["./1.csv", "./2.csv"], batchSize=4)

with tf.Session() as sess:  #
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)  # 将文件名填充到队列，将会启动输入管道线程

    try:
        # while True:
        while not coord.should_stop():
            example, label = sess.run([featurebatch, labelbatch])
            print example, label
    except tf.errors.OutOfRangeError:
        print 'Done reading'
    finally:
        coord.request_stop()  # 请求该线程停止

    coord.join(threads)
    sess.close()
