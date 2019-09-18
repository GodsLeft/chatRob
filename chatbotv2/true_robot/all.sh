#!/bin/bash

# 1 切词
python word_segment.py ./corpus.raw ./corpus.segment

# 2 切好词之后的文件分为问答对
cat ./corpus.segment | awk '{if(last!="")print last"|"$0;last=$0}' | sed 's/| /|/g' > ./corpus.segment.pair

# 3 训练词向量
word2vec -train ./corpus.segment -output vectors.bin -cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-5 -threads 20 -binary 1 -iter 15