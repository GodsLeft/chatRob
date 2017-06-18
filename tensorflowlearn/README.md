# tensorflow学习
- 极客学院tensorflow教程学习笔记

## softmax regression
### 一些概念
- one-hot vectors:除了某一位的数字是1以外，其余各维度的数字都是0

### softmax
- 给不同的对象分配概率
- $W_i$代表权重
- $b_i$代表数字i类的偏移量
- $j$代表给定图片x的像素索引
- 给定输入图片x它代表的数字i的证据表示为：$evidence_i = \sum_j W_{i,j}x_j + b_i$
- 使用softmax函数将上式子转化成概率y：$y = softmax(evidence)$
    + softmax(x) = normalize(exp(x))
- 其本质就是逻辑回归模型

### 交叉熵
- 成本函数评估模型好坏
- $H_{y'} (y) = - \sum_i y_i' log(y_i)$
    + $y$:是我们预测的概率分布
    + $y'$:是实际的分布（one-hot vector）
    
### 前馈神经网络
- mnist
- ffnn.py:这个文件运行时出错
   
## readdata.py
- 学习如何加载数据

## flat2d
- 拟合线性方程

## readflat3d
- 从csv文件中加载数据，并拟合平面
- 注意feed_dict只能狗使用非tensor的数据，如果直接是tensor，那么直接带入进行训练

# kerasdemo
- 这个文件夹主要是keras学习，神经网络简化库

## 我的问题
- sess.run的时候开始执行tensorflow
- 图是在run的时候自动构成的
- 多个run会构成多个图？
- 在卷积的过程时传入的参数[5, 5, 1, 32]中的32解释为输出的通道数目并不合适，我觉得解释为有32套卷积核比较合适
- 卷积的过程中为什么通道会变厚

## 参考文章
- 关于卷积网络较为浅显的解释:http://www.voidcn.com/blog/pirage/article/p-6309109.html
- 一文读懂卷积神经网络：http://dataunion.org/11692.html
- 数据集划分：http://www.cnblogs.com/bourneli/archive/2013/03/11/2954060.html
    + 验证集通常用来辅助模型构建，这是它与测试集的本质区别