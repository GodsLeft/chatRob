# coding=utf-8
# 来源：http://magicly.me/2017/03/09/iamtrask-anyone-can-code-lstm/?hmsr=toutiao.io&amp;utm_medium=toutiao.io&amp;utm_source=toutiao.io
import copy, numpy as np
np.random.seed(0)

# 激活函数
def sigmoid(x):
    output = 1 / (1 + np.exp(-x))
    return output

# 激活函数的导数
def sigmoid_output_to_derivative(output):
    return output * (1 - output)

# 产生训练数据
int2binary = {} # 整数到其二进制表示的映射
binary_dim = 8 # 暂时制作256以内的加法，可以调大

## 以下5行代码计算0-256的二进制表示
largest_number = pow(2, binary_dim)
binary = np.unpackbits(np.array([range(largest_number)], dtype=np.uint8).T, axis=1)
for i in range(largest_number):
    int2binary[i] = binary[i]

# 输入变量
alpha = 0.1 # 学习速率
input_dim = 2 # 因为是做两个数相加，每次喂给神经网络两个bit，所以维度是2
hidden_dim = 16 # 隐藏层神经元节点数，理论上应给一个就可以，但是貌似不行
output_dim = 1 # 输出是一个数，维度是1

# 初始化神经网络权重
synapse_0 = 2 * np.random.random((input_dim, hidden_dim)) - 1 # 输入层到隐藏层的转化矩阵，维度为2×16, 2是输入维度，16是隐藏层维度
synapse_1 = 2 * np.random.random((hidden_dim, output_dim)) - 1
synapse_h = 2 * np.random.random((hidden_dim, hidden_dim)) - 1
# np.random.random产生的是[0,1)的随机数， 2×[0,1) - 1 => [-1, 1),
# 为了有正有负更快收敛

# 以下三个分别对应三个矩阵的变化
synapse_0_update = np.zeros_like(synapse_0)
synapse_1_update = np.zeros_like(synapse_1)
synapse_h_update = np.zeros_like(synapse_h)

# 训练逻辑
# 学习10000个例子
for j in range(100000):
    # 下面6行，随机产生两个0-128的数字，并查出他们的二进制表示。为了避免相加之和超过256,这里选择两个0-128的数子
    a_int = np.random.randint(largest_number/2)
    a = int2binary[a_int] # a的二进制编码

    b_int = np.random.randint(largest_number/2)
    b = int2binary[b_int]

    # 真正的结果
    c_int = a_int + b_int
    c = int2binary[c_int]

    # 存储神经网络的预测值
    d = np.zeros_like(c)

    overallError = 0 # 每次把总误差清零

    layer_2_deltas = list() # 存储每个时间点输出层的误差
    layer_1_values = list() # 存储每个时间点隐藏层的值
    layer_1_values.append(np.zeros(hidden_dim)) # 一开始没有隐藏层，所以里面都是0

    # 循环遍历每一个二进制位
    for position in range(binary_dim):
        # 生成输入和输出
        X = np.array([[a[binary_dim - position - 1], b[binary_dim - position - 1]]]) # 从右到左，每次取两个输入数字的一个bit位
        y = np.array([[c[binary_dim - position - 1]]]).T # 正确答案

        # 隐藏层
        layer_1 = sigmoid(np.dot(X, synapse_0) + np.dot(layer_1_values[-1], synapse_h)) # （输入层 + 之前的隐藏层）-> 新的隐藏层，这是体现循环神经网络最核心的地方！！

        # 输出层
        layer_2 = sigmoid(np.dot(layer_1, synapse_1)) # 隐藏层 × 隐藏层到输出层的转化矩阵synapse_1 -> 输出层

        # 我们错了么？
        layer_2_error = y - layer_2 # 预测误差是多少
        layer_2_deltas.append((layer_2_error) * sigmoid_output_to_derivative(layer_2)) # 我们把每一个时间点的误差倒数都记录下来
        overallError += np.abs(layer_2_error[0]) # 总误差？ zhu：我觉得有问题

        # 记录每一个预测bit位
        d[binary_dim - position - 1] = np.round(layer_2[0][0])

        # 记录隐藏层的值，在下一个时间点用
        layer_1_values.append(copy.deepcopy(layer_1))

    future_layer_1_delta = np.zeros(hidden_dim)

    # 前面的代码我们完成了所有时间点的正向传播以及计算最后一层的误差，现在我们要做的是反向传播
    # 从最后一个时间点到第一个时间点
    for position in range(binary_dim):
        X = np.array([[a[position], b[position]]]) # 最后一次的两个输入
        layer_1 = layer_1_values[-position - 1] # 当前时间点的隐藏层
        prev_layer_1 = layer_1_values[-position - 2] # 前一个时间点的隐藏层

        # 当前时间点输出层导数
        layer_2_delta = layer_2_deltas[-position - 1]
        # 通过后一个时间点的隐藏层误差和当前时间点的输出层误差，计算当前时间点隐藏层误差
        layer_1_delta = (future_layer_1_delta.dot(synapse_h.T) + layer_2_delta.dot(synapse_1.T)) * sigmoid_output_to_derivative(layer_1)

        # 已经完成了当前时间点的反向传播误差计算，可以构建更新矩阵了。但是我们并不会现在就更新权重矩阵，因为我们还要用他们计算前一个时间点的更新矩阵呢
        # 所以要等我们完成了所有反向传播误差计算，才会真正的去更新权重矩阵，我们暂时把更新矩阵存起来
        synapse_1_update += np.atleast_2d(layer_1).T.dot(layer_2_delta)
        synapse_h_update += np.atleast_2d(prev_layer_1).T.dot(layer_1_delta)
        synapse_0_update += X.T.dot(layer_1_delta)

        future_layer_1_delta = layer_1_delta

    # 完成所有反向传播，可以更新几个转换矩阵了。并把更新矩阵变量清零
    synapse_0 += synapse_0_update * alpha
    synapse_1 += synapse_1_update * alpha
    synapse_h += synapse_h_update * alpha

    synapse_0_update *= 0
    synapse_1_update *= 0
    synapse_h_update *= 0

    # 输出执行程度
    if (j % 1000 == 0):
        print("Error: " + str(overallError))
        print("Pred:  " + str(d))
        print("True:  " + str(c))
        out = 0
        for index, x in enumerate(reversed(d)):
            out += x * pow(2, index)
        print(str(a_int) + " + " + str(b_int) + " = " + str(out))
        print("------------------------")