# 使用jieba对语料库进行切词
# python word_segment.py ../corpus/srt.out ./segment_result

# 使用word2vec生成词向量
# ./word2vec/word2vec -train ./segment_result -output vectors.bin -cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 -thread 20 -binary 1 -iter 15

# 加载向量
# python word_vectors_loader.py vectors.bin
python loadvec.py vectors.bin
