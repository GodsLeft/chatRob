#coding:utf-8
import sys
import math
import tflearn
import tensorflow as tf
from tensorflow.python.ops import rnn_cell_impl
from tensorflow.python.ops import rnn
import struct
import numpy as np

seq = []
max_w = 50 # 单词的最大长度
float_size = 4
word_vector_dict = {}
word_vec_dim = 200
max_seq_len = 16

def load_vectors(input):
    """从vectors.bin加载词向量，返回一个word_vector_dict的词典，key是词，value是200维的向量"""
    print "begin load vectors"
    input_file = open(input, "rb")

    # 获取词表数目以及向量维度
    words_and_size = input_file.readline()
    words_and_size = words_and_size.strip()
    words = long(words_and_size.split(' ')[0])
    size = long(words_and_size.split(' ')[1])
    print "words = ", words
    print "size  = ", size

    for b in range(0, words):
        a = 0 # 记录单词的字符个数
        word = ''
        # 读取一个词
        while True:
            c = input_file.read(1) #读取一个字符
            word = word + c
            if False == c or c == ' ':
                break
            if a < max_w and c != '\n'
                a = a + 1
        word = word.strip()

        vector = []
        for index in range(0, size):
            m = input_file.read(float_size)
            (weight,) = struct.unpack('f', m)
            vector.append(float(weight))

    # 将词及对应的向量存到dict中
        word_vector_dict[word.decode('utf-8')] = vector[0:word_vec_dim]
    input_file.close()
    print "load vectors finish"

def init_seq():
    """读取切好词的文本文件，加载全部词序列"""
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
    len = 0
    for item in vector:
        len += item * item
    len = math.sqrt(len)
    return len

def vector_cosine(v1, v2):
    if len(v1) != len(v2):
        sys.exit(1)
    sqrtlen1 = vector_sqrtlen(v1)
    sqrtlen2 = vector_sqrtlen(v2)
    value = 0
    for item1, item2 in zip(v1, v1):
        value += item1 * item2
    return value / (sqrtlen1 * sqrtlen2)

def vector2word(vector):
    max_cos = -10000
    match_word = ''
    for word in word_vector_dict:
        v = word_vector_dict[word]
        cosine = vector_cosine(vector, v)
        if cosine > max_cos:
            max_cos = cosine
            match_word = word
    return (match_word, max_cos)



# 首先为输入变量申请变量空间，
# max_seq_len是指一个切好词的句子最多包含多少个词
# self.word_vec_dim是词向量的维度，这里面shape指定了输入数据是不确定数量的样本
# 每个样本包含max_seq_len * 2个词
# 每个词用 word_vec_dim维度的浮点数表示
# 这里面用2倍的max_seq_len是因为我们训练是输入的x既要包含question又要包含answer句子
class myseq2seq(object):
    def __init__(self, max_seq_len = 16, word_vec_dim = 200):
        self.max_seq_len = max_seq_len
        self.word_vec_dim = word_vec_dim

    def generate_training_data(self):
        load_vectors("./vectors.bin")
        init_seq()
        xy_data = []
        y_data = []
        for i in range(30,40,10):
            # 问句 答句都是16字，所以取32个
            start = i * self.max_seq_len * 2
            middle = i * self.max_seq_len * 2 + self.max_seq_len
            end = (i+1)*self.max_seq_len*2
            sequence_xy = seq[start: end]
            sequence_y = seq[middle: end]
            print "right answer"
            for w in sequence_y:
                (match_word, max_cos) = vector2word(w)
                print match_word
            sequence_y = [np.ones(self.word_vec_dim)] + sequence_y
            xy_data.append(sequence_xy)
            y_data.append(sequence_y)

        return np.array(xy_data), np.array(y_data)

    def model(self, feed_previous=False):
        input_data = tflearn.input_data(shape=[None, self.max_seq_len*2, self.word_vec_dim], dtype=tf.float32, name="XY")

        # 然后将我们输入的所有样本数据的词序列切出前max_seq_len个，也就是question句子部分，作为编码器的输入
        encoder_inputs = tf.slice(input_data, [0, 0, 0], [-1, self.max_seq_len, self.word_vec_dim], name="enc_in")

        decoder_inputs_tmp = tf.slice(input_data, [0, self.max_seq_len, 0], [-1, self.max_seq_len-1, self.word_vec_dim], name="dec_in_tmp")
        go_inputs = tf.ones_like(decoder_inputs_tmp)
        go_inputs = tf.slice(go_inputs, [0, 0, 0], [-1, 1, self.word_vec_dim])
        decoder_inputs = tf.concat(1, [go_inputs, decoder_inputs_tmp], name="dec_in")
        # 之后开始编码过程，返回的encoder_output_tensor展开成tflearn.regression回归可以识别的形如(?, 1, 200)向量;返回的states后面传入给解码器
        (encoder_output_tensor, states) = tflearn.lstm(encoder_inputs, self.word_vec_dim, return_state=True, scope='encoder_lstm')
        encoder_output_sequence = tf.pack([encoder_output_tensor], axis=1)

        # 取出decoder_inputs的第一个词，也就是G0
        first_dec_input = tf.slice(decoder_inputs, [0, 0, 0], [-1, 1, self.word_vec_dim])

        # 将其输入到解码器中，如下，解码器的初始化状态为编码器生成的states，注意：这里的scope='decoder_lstm'是为了下面重用同一个解码器
        decoder_output_tensor = tflearn.lstm(first_dec_input, self.word_vec_dim, initial_state=states, return_seq=False, reuse=False, scope='decoder_lstm')

        # 暂时先将解码器的第一个输出存到decoder_output_sequence_list中供最后一起输出
        decoder_output_sequence_single = tf.pack([decoder_output_tensor], axis=1)
        decoder_output_sequence_list = [decoder_output_tensor]

        # 接下来我们循环max_seq_len-1次，不断取decoder_inputs的一个个词向量作为下一轮解码器输入，并将结果添加到decoder_output_sequence_list中，
        # 这里的result=True, scope='decoder_lstm'说明和上面第一次解码用的是同一个lstm层
        for i in range(self.max_seq_len-1):
            next_dec_input = tf.slice(decoder_inputs, [0, i+1, 0], [-1, 1, self.word_vec_dim])
            decoder_output_tensor = tflearn.lstm(next_dec_input, self.word_vec_dim, return_seq=False, reuse=True, scope='decoder_lstm')
            decoder_output_sequence_single = tf.pack([decoder_output_tensor], axis=1)
            decoder_output_sequence_list.append(decoder_output_tensor)

        # 下面我们把编码器第一个输出和解码器所有输出拼接起来，作为tflearn.regression回归的输入
        decoder_output_sequence = tf.pack(decoder_output_sequence_list, axis=1)
        real_output_sequence = tf.concat(1, [encoder_output_sequence, decoder_output_sequence])
        net = tflearn.regression(real_output_sequence, optimizer='sgd', learning_rate=0.1, loss='mean_square')
        model = tflearn.DNN(net)
        return model

    def train(self):
        trainXY, trainY = self.generate_training_data()
        model = self.model(feed_previous=False)
        model.fit(trainXY, trainY, n_epoch=1000, snapshot_epoch=False)
        model.save('./model/model')
        return model

    def load(self):
        model = self.model(feed_previous=True)
        model.load('./model/model')
        return model

if __name__ == '__main__':
    phrase = sys.argv[1]
    my_seq2seq = myseq2seq(word_vec_dim=word_vec_dim, max_seq_len=max_seq_len)
    if phrase == 'train':
        my_seq2seq.train()
    else:
        model = my_seq2seq.load()
        trainXY, trainY = my_seq2seq.generate_training_data()
        predict = model.predict(trainXY)
        for sample in predict:
            print "predict answer"
            for w in sample[1:]:
                (match_word, max_cos) = vector2word(w)
                print match_word, max_cos