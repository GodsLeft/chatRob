# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import nltk

for word in nltk.corpus.sinica_treebank.tagged_words():
    print word[0], word[1]
