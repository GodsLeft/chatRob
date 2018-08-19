# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import nltk

# 默认标注器
print '===='
default_tagger = nltk.DefaultTagger('NN')
raw = '我 累 个 去'
tokens = nltk.word_tokenize(raw)
tags = default_tagger.tag(tokens)
print tags

# 正则表达式标注器
print '===='
pattern = [(r'.*们$', 'PRO')]
tagger = nltk.RegexpTagger(pattern)
print tagger.tag(nltk.word_tokenize('我们 累 个 去 你们 和 他们 啊'))

# 查询标注器：一元标注
print '===='
tagged_sents = [[(u'我', u'PRO'), (u'小兔', u'NN')]]
unigram_tagger = nltk.UnigramTagger(tagged_sents)
sents = nltk.corpus.brown.sents(categories='news')
sents = [[u'我', u'你', u'小兔']]
tags = unigram_tagger.tag(sents[0])
print tags
