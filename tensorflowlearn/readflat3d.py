# coding:utf-8

import os
import numpy as np
import pandas as pd
import tensorflow as tf

# 首先生成数据，然后进行保存
def gendata(datafile):
    if not os.path.exists(datafile):
        df = pd.DataFrame(np.random.rand(1000, 2))
        df[2] = df[0]*0.1 + df[1]*0.2 + 0.3
        df.to_csv(datafile, index=False, header=False)
        print "make data done!"

# 从文件中读取数据，然后进行训练
def inputdatabatch(filenames, batchsize=4):
    filenamequeues = tf.train.string_input_producer(filenames, num_epochs=None)

    reader = tf.TextLineReader()
    key, value = reader.read(filenamequeues)
    record_defaults = [[0.0], [0.0], [0.0]]
    col1, col2, col3 = tf.decode_csv(value, record_defaults=record_defaults)
    feature = tf.concat([[col1], [col2]], 0)
    label = col3

    min_after_queue = 8
    capacity = min_after_queue + 3*batchsize
    featurebatch, labelbatch = tf.train.shuffle_batch([feature, label],
                                                      batch_size=batchsize,
                                                      num_threads=3,  # 要搞明白这个线程个数，指的是那些线程
                                                      capacity=capacity,
                                                      min_after_dequeue=min_after_queue)
    return featurebatch, labelbatch

# x = tf.placeholder(tf.float32, [None, 2])
# y = tf.matmul(x, W)
# y_ = tf.placeholder(tf.float32, [None, 1])
# loss = tf.reduce_mean(tf.square(y - y_))
# optimizer = tf.train.GradientDescentOptimizer(0.5)
# train = optimizer.minimize(loss)
# init = tf.initialize_all_variables()

gendata("testfile.csv")
b = tf.Variable(tf.zeros([1]))
W = tf.Variable(tf.random_uniform([2, 1], -1, 1))
feabatch, labbatch = inputdatabatch(["./testfile.csv"])
yy = tf.matmul(feabatch, W) + b
y_ = labbatch

loss = tf.reduce_mean(tf.square(yy - y_))
optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess, coord=coord)

tf.summary.scalar("loss", loss)
summary = tf.summary.merge_all()
summarywriter = tf.summary.FileWriter("/tmp/tensorflow/readflat3d", sess.graph)

saver = tf.train.Saver()

for i in xrange(10000):
    sess.run(train)
    if i % 100 == 0:
        sess.run(loss), sess.run(b)
        summary_str = sess.run(summary)
        summarywriter.add_summary(summary_str, i)
        summarywriter.flush()
        checkpointfile = os.path.join("/tmp/tensorflow/readflat3d", "model.ckpt")
        saver.save(sess, checkpointfile, global_step=i)
    # 其中的feed_dict必须不是tensor
    # sess.run(train, feed_dict={x: tf.convert_to_tensor(feabatch),y_: tf.convert_to_tensor(labbatch)})
print sess.run(W), sess.run(b)
