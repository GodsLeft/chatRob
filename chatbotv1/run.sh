#!/usr/bin/env bash
#java -cp target/chatbotv1-1.0-SNAPSHOT.jar com.left.Indexer ../README.md ./zhuindex
# mvn package assembly:single

# 将语料库转化为索引
# java -cp target/chatbotv1-1.0-SNAPSHOT-jar-with-dependencies.jar com.left.Indexer ../corpus/srt.out ./zhuindex

# 运行netty服务器
java -cp ./target/chatbotv1-1.0-SNAPSHOT-jar-with-dependencies.jar com.left.Searcher
