#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import jieba
from jieba import analyse

def segment(input, output):
    """对输入文件进行切词，并输出到output"""
    with open(input, 'r') as INPUT, open(output, 'w') as OUTPUT:
        for line in INPUT:
            line = line.strip()
            OUTPUT.write(' '.join(jieba.cut(line)))

if __name__ == '__main__':
    if 3 != len(sys.argv):
        print "Usage: ", sys.argv[0], "input output"
        sys.exit(-1)
    segment(sys.argv[1], sys.argv[2])