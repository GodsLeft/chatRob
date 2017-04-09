#coding:utf-8

import tensorflow as tf
import tensorflow.examples.tutorials.mnist.input_data as input_data

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

x = tf.placeholder(tf.float32, [None, 784])  # 这里的None表示第一个维度可以是任意长度
W = tf.Variable(tf.zeros([784, 10]))  # Variable代表一个可以修改的张量
b = tf.Variable(tf.zeros([10]))

y = tf.nn.softmax(tf.matmul(x, W) + b)

y_ = tf.placeholder("float", [None, 10])  # 用于输入正确值
cross_entropy = -tf.reduce_sum(y_ * tf.log(y))  # 计算交叉熵作为损失函数
tf.summary.scalar('cross_entropy', cross_entropy)
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)  # 0.01是学习速率

init = tf.initialize_all_variables()  # 添加一个操作来初始化我们创建的变量

summary = tf.summary.merge_all()  # 添加绘图
sess = tf.Session()
summary_writer = tf.summary.FileWriter('/tmp/tensorflow/softmax', sess.graph)
sess.run(init)  # 启动模型并初始化向量

# 模型循环执行1000次，每次随机抓取100个数据点，用这些数据点替换原来的占位符，来运行train_step
for i in range(10000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
    if (i+1) % 100 == 0:
        summary_str = sess.run(summary, feed_dict={x: batch_xs, y_: batch_ys})
        summary_writer.add_summary(summary_str, i)
        summary_writer.flush()

# Test trained model
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
print sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels})