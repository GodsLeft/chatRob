# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import nltk

my_train_set = [
    ({'feature1':u'a'}, '1'),
    ({'feature1':u'a'}, '2'),
    ({'feature1':u'a'}, '3'),
    ({'feature1':u'a'}, '3'),
    ({'feature1':u'b'}, '2'),
    ({'feature1':u'b'}, '2'),
    ({'feature1':u'b'}, '2'),
    ({'feature1':u'b'}, '2'),
    ({'feature1':u'b'}, '2'),
    ({'feature1':u'b'}, '2'),
    ]
classifier = nltk.NaiveBayesClassifier.train(my_train_set)
print classifier.classify({'feature1':u'a'})
print classifier.classify({'feature1':u'b'})

# 特征提取
from nltk.corpus import movie_reviews
all_words = nltk.FreqDist(w.lower() for w in movie_reviews())
word_features = all_words.keys()[:2000]
def document_features(document):
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

# 训练过程
featuresets = [(document_features(d), c) for (d, c) in documents]
classifier = nltk.NaiveBayesClassifier.train(featuresets)

# 预测新的文档
classifier.classify(document_features(d))

classifier.show_most_informative_features(5)
