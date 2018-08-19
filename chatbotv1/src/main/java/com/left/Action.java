package com.left;

/**
 * Created by left on 17-3-6.
 */
import java.io.File;
import java.io.IOException;
import java.util.HashSet;
import java.util.List;
import java.util.Map;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;
import io.netty.handler.codec.http.FullHttpRequest;
import io.netty.handler.codec.http.QueryStringDecoder;
import org.apache.log4j.Logger;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.AtomicReader;
import org.apache.lucene.index.AtomicReaderContext;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.*;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.PriorityQueue;
import org.apache.lucene.util.Version;
import org.wltea.analyzer.lucene.IKAnalyzer;

public class Action {
    private static final Logger log = Logger.getLogger(Action.class);
    private static final Logger logChat = Logger.getLogger("chat");

    private static final int MAX_RESULT = 10;
    private static final int MAX_TOTAL_HITS = 1000000;
    private static IndexSearcher indexSearcher = null;

    //生成索引读取器
    static {
        IndexReader reader = null;
        try {
            reader = DirectoryReader.open(FSDirectory.open(new File("./zhuindex")));
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(-1);
        }
        indexSearcher = new IndexSearcher(reader);
    }

    // 解析http请求，并做出回应
    public static void doServlet(FullHttpRequest req, NettyHttpServletResponse res) throws IOException, ParseException{
        ByteBuf buf = null;
        QueryStringDecoder qsd = new QueryStringDecoder(req.uri());
        Map<String, List<String>> mapParameters = qsd.parameters();
        List<String> l = mapParameters.get("q");

        if(null != l && l.size() == 1) {
            String q = l.get(0);
            //如果是监控程序
            if(q.equals("monitor")){
                JSONObject ret = new JSONObject();
                ret.put("total", 1);
                JSONObject item = new JSONObject();
                item.put("answer", "alive");
                JSONArray result = new JSONArray();
                result.add(item);
                ret.put("result", result);
                buf = Unpooled.copiedBuffer(ret.toJSONString().getBytes());
                res.setContent(buf);
                return;
            }

            log.info("question=" + q);

            //获取客户端的IP地址
            List<String> clientIps = mapParameters.get("clientIp");
            String clientIp = "";
            if(null != clientIps && clientIps.size() == 1){
                clientIp = clientIps.get(0);
                log.info("clientIp = " + clientIp);
            }

            Query query = null;
            PriorityQueue<ScoreDoc> pq = new PriorityQueue<ScoreDoc>(MAX_RESULT) {
                @Override
                protected boolean lessThan(ScoreDoc a, ScoreDoc b) {
                    return a.score < b.score;
                }
            };

            MyCollector collector = new MyCollector(pq);

            JSONObject ret = new JSONObject();
            TopDocs topDocs = collector.topDocs();

            //检索关键词，并获得相应的答案
            //查询建好的索引，通过query词做切词，并lucene query，然后检索索引的question字段，匹配上的返回answer字段
            //的值作为候选集，使用时挑出候选集中的一条作为答案
            Analyzer analyzer = new IKAnalyzer(true);
            QueryParser qp = new QueryParser(Version.LUCENE_4_9, "question", analyzer);
            if(topDocs.totalHits == 0){
                qp.setDefaultOperator(QueryParser.Operator.AND);
                query = qp.parse(q);
                log.info("lucene query = " + query.toString());
                topDocs = indexSearcher.search(query, 20);
                log.info("elapse " + collector.getElapse() + " " + collector.getElapse2());
            }

            if(topDocs.totalHits == 0){
                qp.setDefaultOperator(QueryParser.Operator.OR);
                query = qp.parse(q);
                log.info("lucene query = " + query.toString());
                topDocs = indexSearcher.search(query, 20);
                log.info("elapse " + collector.getElapse() + " " + collector.getElapse2());
            }

            //获取question的答案和评分
            ret.put("total", topDocs.totalHits);
            ret.put("q", q);
            JSONArray result = new JSONArray();
            String firstAnswer = "";
            for(ScoreDoc d : topDocs.scoreDocs){
                Document doc = indexSearcher.doc(d.doc);
                String question = doc.get("question");
                String answer = doc.get("answer");
                JSONObject item = new JSONObject();
                item.put("question", question);
                if (firstAnswer.equals("")){
                    firstAnswer = answer;
                }
                item.put("answer", answer);
                item.put("score", d.score);
                item.put("doc", d.doc);
                result.add(item);
            }
            ret.put("result", result);
            log.info("response="+ret);
            logChat.info(clientIp + " [" + q + "] [" + firstAnswer + "]");
            buf = Unpooled.copiedBuffer(ret.toJSONString().getBytes());
        }else {
            buf = Unpooled.copiedBuffer("error".getBytes());
        }
        res.setContent(buf);
    }

    public static class MyCollector extends TopDocsCollector<ScoreDoc> {
        protected Scorer scorer;
        protected AtomicReader reader;
        protected int baseDoc;
        protected HashSet<Integer> set = new HashSet<Integer>();
        protected long elapse = 0;
        protected long elapse2 = 0;

        public long getElapse2(){return elapse2;}
        public void setElapse2(long elapse2){this.elapse2 = elapse2;}

        public long getElapse(){return elapse;}
        public void setElapse(long elapse){this.elapse = elapse;}

        protected MyCollector(PriorityQueue<ScoreDoc> pq){super(pq);}

        @Override
        public void setScorer(Scorer scorer) throws IOException{this.scorer = scorer;}

        @Override
        public void collect(int doc) throws IOException{
            long t1 = System.currentTimeMillis();
            if(this.totalHits > MAX_TOTAL_HITS)
                return;

            String answer = this.getAnswer(doc);
            long t3 = System.currentTimeMillis();
            this.elapse2 += t3 - t1;
            if(set.contains(answer.hashCode())){
                return;
            }else{
                set.add(answer.hashCode());
                ScoreDoc sd = new ScoreDoc(doc, this.scorer.score());
                if(this.pq.size() >= MAX_RESULT){
                    this.pq.updateTop();
                    this.pq.pop();
                }
                this.pq.add(sd);
                this.totalHits ++;
            }
            long t2 = System.currentTimeMillis();
            this.elapse += t2 - t1;
        }

        @Override
        public void setNextReader(AtomicReaderContext context) throws IOException{
            this.reader = context.reader();
            this.baseDoc = context.docBase;
        }

        @Override
        public boolean acceptsDocsOutOfOrder(){
            return false;
        }

        private String getAnswer(int doc) throws IOException{
            Document d = indexSearcher.doc(doc);
            return d.get("answer");
        }
    }
}