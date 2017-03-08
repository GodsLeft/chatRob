# chatbot
- 关于chatbot的php网页部分不太懂

# 其他
- nltk.corpus.words.words()：所有英文单词，可以用来识别语法错误
- nltk.corpus.stopwords.words：停用词语料库，用来识别最频繁出现的没有意义的单词
- nltk.corpus.cmudict.dict():用来输出每个英文单词的发音
- nltk.corpus.swadesh:多种语言核心200多个词的对照，可以作为语言翻译的基础
- WordNet:同义词集，面向语义的英语词典，由同义词集组成，并组成一个网络


# 证书过期问题
- 下载github上NLPIR的证书
- 替换安装目录下的Data/NLPIR.user文件
- 我使用的是anaconda 安装目录在 $HOME/.pyenv/versions/anaconda2-4.1.1/lib/python2.7/site-packages/pynlpir/Data

# scrapy
## 全局命令
- startproject:生成一个爬虫项目
- settings:
- runspider
- shell:
- fetch:使用scrapy下载器下载给定的URL，并将获取到的内容送到标准输出
- view
- version:显示scrapy版本

## 项目命令
- crawl:使用spider进行爬取
- check:运行contract检查
- list:显示可用的爬虫
- edit:使用EDITOR设置的编辑器编辑给定的spider
- parse
- genspider:生成爬虫样本代码
- deploy
- bench


## 算法相关，以后合并到算法的文件里
- 偏差:描述的是预测值（估计值）的期望$E'$与真实值$Y$之间的差距，偏差越大，越偏离真实数据
$$Bias[\hat{f}(x)] = E[\hat{f} (x)] - f(x)$$
- 方差:描述的是预测值$P$的变化范围，离散程度，是预测值的方差，也就是离其期望值$E$的距离。方差越大，数据分布越分散
$$Var[\hat{f} (x)] = E[(\hat{f} (x) - E[\hat{f} (x)])^2]$$
- 高偏差：欠拟合
- 高方差：

## 模型有其固有的缺陷
生成模型和判别式模型，主要还是在于是否是要求联合分布

### 朴素贝叶斯模型
- 生成模型
- 简单假设了各个数据之间是无关的，是一个严重简化了的模型
- 所以大部分场合都会Bias部分大于Variance部分，也就是说高偏差而低方差
- 主要缺点:不能学习特征间的相互作用
- 例子：你喜欢成龙的电影，你喜欢李连杰的电影，但是他不能学习出他们在一起的电影

#### 优点
- 源于古典数学理论，有坚实的数学基础，稳定的分类效率
- 小规模数据表现好，能够处理多分类任务，适合增量式训练
- 对缺失数据不太敏感，算法简单，常用于文本分类

#### 缺点
- 需要计算先验概率
- 分类决策存在错误率
- 对输入数据的表达形式很敏感

### 逻辑回归
- 判别式模型
- 有很多正则化模型的方法(L0, L1, L2, etc)
- 不必像在用朴素贝叶斯那样担心你的特征是否相关
- 与决策树和svm相比，还会得到一个不错的概率解释
- 可以使用在线梯度下降算法

#### 优点
- 实现简单，广泛应用于工业问题上
- 分类时计算量非常小，速度很快，存储资源低
- 便利的观测样本概率分布
#### 缺点
- 特征空间很大时，逻辑回归的性能不是很好
- 容易欠拟合，一般准确度不太高
- 不能很好的处理大量多类特征或变量
- 只能处理两分类的问题，且必须线性可分
- 对于非线性特征，需要进行转换

### 线性回归
是解决回归问题，并非分类
#### 优点
- 实现简单，计算简单
#### 缺点
- 不能拟合非线性数据

### KNN
#### 优点
- 理论成熟，思想简单，即可以用来做分类也可以用来做回归
- 可用于非线性分类
- 训练时间复杂度为O(n)
- 对数据没有假设，准确度高

#### 缺点
- 计算量大
- 样本不平衡问题
- 需要大量的内存

### 决策树
- 易于解释，毫无压力的处理特征间的交互关系并且是非参数化的
- 不支持在线学习，新的样本来了之后，决策树需要全部重建
- 容易出现过拟合，随机森林或者提升树可解决这个问题
#### 优点
- 计算简单，易于理解，可解释性强
- 比较适合处理有缺失属性的样本
- 能处理不想关的特征
- 在短时间内能够处理大型数据源并且效果良好
#### 缺点
- 容易过拟合（随机森林）
- 忽略了数据之间的相关性
- 对于各类别样本数量不一致的数据，在决策树当中信息增益结果偏向于那些具有更多数值的特征（只要使用了信息增益，都有这个缺点）

### SVM
高准确率，避免过拟合，而且就算数据线性不可分，只要给个合适的核函数，就能运行的很好。在超高维度的文本分类问题中特别受欢迎。可惜内存消耗大，难以解释，运行调参也有些烦人，而随机森林确刚好避开了这些缺点
#### 优点
- 解决高维问题，大型特征空间
- 处理非线性特征的相互作用
- 无需依赖整个数据
- 可以提高泛化能力
#### 缺点
- 当观测样本很多的时候，效率并不是很高
- 对非线性问题没有通用的解决方案，有时候很难找到一个合适的核函数
- 对缺失数据敏感

### 人工神经网络优缺点
#### 优点
- 分类的准确度高
- 并行分布处理能力强，分布存储及学习能力强
- 对噪声神经有较强的鲁棒性和容错能力，能充分逼近复杂的非线性关系
- 具备联想记忆的功能
#### 缺点
- 需要大量的参数，如网络的拓扑结构，权值和阀值的初始值
- 不能观察之间的学习过程，输出结果难以解释，会影响到结果的可信度和可接受程度
- 学习时间过长，甚至可能达不到学习的目的

### K-Means
#### 优点
- 算法简单，容易实现
- 对处理大数据集，该算法是相对可伸缩和高效率的
- 算法尝试找出使平方误差函数值最小的k个划分。当簇是密集的/球状/团状的，且簇与簇之间有明显区别时，聚类效果较好
#### 缺点
- 数据类型要求较高，适合数值型数据
- 可能收敛到局部最小值，在大规模数据上收敛较慢
- K值比较难以选取
- 对初值的簇心值敏感，对不同的初始值，可能会导致不同的聚类结果
- 不适合于发现非凸面形状的簇，或者大小差别很大的簇
- 对于噪声和孤立点数据敏感，少量的该类数据能够对平局值产生极大的影响

### 算法选择
- 首当其冲的选择是逻辑回归，如果他的效果不怎么样，那么可以将它的结果作为基准来参考
- 然后试试决策树（随机森林）看看是否能够大幅度提升你的模型性能。即便最后你并没有把它作为最终模型，你也可以使用随机森林来移除噪声变量，做特征选择
- 如果特征的数量和观测样本特别多，那么当资源和时间充足时，SVM不失为一种选择
- 通常情况下【GBDT >= SVM >= RF >= Adaboost >= other...】
- 算法固然重要，但是好的数据却要优于好的算法
- 假如你有一个超大数据集，那么无论你使用哪种算法可能对分类性能都没有太大影响（此时可根据速度和易用性来进行抉择）
