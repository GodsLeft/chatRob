# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import pynlpir

pynlpir.open()
s = '聊天机器人到底该怎么做呢？'
segments = pynlpir.segment(s)

for segment in segments:
    print segment[0], '\t', segment[1]

# 提取关键词
key_words = pynlpir.get_key_words(s, weighted=True)
for key_word in key_words:
    print key_word[0], '\t', key_word[1]

# 将分析功能全部打开
s = '海洋是如何形成的'
segments = pynlpir.segment(s, pos_names='all', pos_english=False)
for segment in segments:
    print segment[0], '\t', segment[1]

pynlpir.close()
