#java -cp target/chatbotv1-1.0-SNAPSHOT.jar com.left.Indexer ../README.md ./zhuindex
# mvn package assembly:single
java -cp target/chatbotv1-1.0-SNAPSHOT-jar-with-dependencies.jar com.left.Indexer ../corpus/srt.out ./zhuindex
