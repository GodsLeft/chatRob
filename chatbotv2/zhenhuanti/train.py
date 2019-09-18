#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import tflearn
import chardet
import numpy as np
import struct

seq = []                    # 存储所有词向量的序列，正片文章的向量

max_w = 50
float_size = 4
word_vector_dict = {}       # 存储词和对应的向量

def load_vectors(input):
    """从vectors.bin加载词向量，返回一个word_vector_dict的词典，key是词，value是200维的向量
    """
    print "begin load vectors"

    input_file = open(input, "rb")

    # 获取词表数目及向量维度
    words_and_size = input_file.readline()
    words_and_size = words_and_size.strip()
    words = long(words_and_size.split(' ')[0])
    size = long(words_and_size.split(' ')[1])
    print "words =", words
    print "size =", size

    for b in range(0, words):
        a = 0
        word = ''
        # 读取一个词
        while True:
            c = input_file.read(1)
            word = word + c
            if False == c or c == ' ':
                break
            if a < max_w and c != '\n':
                a = a + 1
        word = word.strip()

        vector = []
        for index in range(0, size):
            m = input_file.read(float_size)
            (weight,) = struct.unpack('f', m)
            vector.append(weight)

        # 将词及其对应的向量存到dict中
        word_vector_dict[word.decode('utf-8')] = vector

    input_file.close()
    print "load vectors finish"

def init_seq():
    """读取切好词的文本文件，加载全部词序列
    """
    file_object = open('zhenhuanzhuan.segment', 'r')
    vocab_dict = {}
    while True:
        line = file_object.readline()
        if line:
            for word in line.decode('utf-8').split(' '):
                if word_vector_dict.has_key(word):
                    seq.append(word_vector_dict[word])
        else:
            break
    file_object.close()

def vector_sqrtlen(vector):
    """
    求每个向量的长度
    """
    len = 0
    for item in vector:
        len += item * item
    len = math.sqrt(len)
    return len

def vector_cosine(v1, v2):
    """
    两个向量的余弦相似度
    """
    if len(v1) != len(v2):
        sys.exit(1)
    sqrtlen1 = vector_sqrtlen(v1)
    sqrtlen2 = vector_sqrtlen(v2)
    value = 0
    for item1, item2 in zip(v1, v2):
        value += item1 * item2
    return value / (sqrtlen1*sqrtlen2)


def vector2word(vector):
    """
    从词表当中返回最相近的词
    """
    max_cos = -10000
    match_word = ''
    for word in word_vector_dict:
        v = word_vector_dict[word]
        cosine = vector_cosine(vector, v)
        if cosine > max_cos:
            max_cos = cosine
            match_word = word
    return (match_word, max_cos)

def main():
    load_vectors("./vectors.bin")
    init_seq()
    xlist = []      # 样本
    ylist = []      # 预测值
    test_X = None
    #for i in range(len(seq)-100):
    for i in range(10):
        sequence = seq[i:i+20]      # 选取20个词向量
        xlist.append(sequence)
        ylist.append(seq[i+20])     # 添加第21个词向量

        if test_X is None:
            test_X = np.array(sequence)
            (match_word, max_cos) = vector2word(seq[i+20])
            print "right answer=", match_word, max_cos

    X = np.array(xlist)
    Y = np.array(ylist)

    net = tflearn.input_data([None, 20, 200])
    net = tflearn.lstm(net, 200)
    net = tflearn.fully_connected(net, 200, activation='linear')
    net = tflearn.regression(net, optimizer='sgd', learning_rate=0.1,
                                     loss='mean_square')
    model = tflearn.DNN(net)
    model.fit(X, Y, n_epoch=500, batch_size=10,snapshot_epoch=False,show_metric=True)
    model.save("model")

    predict = model.predict([test_X])

    #print predict
    #for v in test_X:
    #    print vector2word(v)
    (match_word, max_cos) = vector2word(predict[0])
    print "predict=", match_word, max_cos

main()