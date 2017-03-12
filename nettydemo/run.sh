#!/usr/bin/env bash

# 编译
mvn package assembly:single

# 运行服务器端
java -cp ./target/nettydemo-1.0-SNAPSHOT-jar-with-dependencies.jar NettyServer

# 运行客户端
java -cp ./target/nettydemo-1.0-SNAPSHOT-jar-with-dependencies.jar NettyClient
