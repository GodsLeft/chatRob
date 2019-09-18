#!/bin/bash

# 使用分词好的文件生成词向量
./word2vec -train ../segment_result -output vectors.bin -cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 20 -binary 1 -iter 15

# 交互式的验证过程
./distance vectors.bin