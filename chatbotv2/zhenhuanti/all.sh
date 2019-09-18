#!/bin/bash

# 1 下载甄嬛小说

# 2 切词
python ./word_segment.py zhenhuanzhuan.txt zhenhuanzhuan.segment

# 3 生成词向量
./word2vec -train ./zhenhuanzhuan.segment -output vectors.bin -cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 20 -binary 1 -iter 15
