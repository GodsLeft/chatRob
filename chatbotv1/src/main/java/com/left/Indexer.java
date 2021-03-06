package com.left;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StoredField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;
import org.wltea.analyzer.lucene.IKAnalyzer;

import java.io.*;
import java.nio.charset.Charset;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HashSet;

/**
 * Hello world!
 *
 */
public class Indexer
{
    public static final Charset UTF8 = Charset.forName("utf8");

    // 用来将md5值变为字符串
    public static String hexString(byte[] b){
        String ret = "";
        for(int i=0; i<b.length; i++){
            String hex = Integer.toHexString(b[i] & 0xF);
            ret += hex.toUpperCase();
        }
        return ret;
    }

    public static void main( String[] args ) throws IOException, NoSuchAlgorithmException
    {
        if(args.length != 2){
            System.err.println("Usage: " + Indexer.class.getSimpleName() + " corpus_path index_path");
            System.exit(-1);
        }
        //语料库的路径，索引路径
        String corpusPath = args[0];
        String indexPath = args[1];

        Analyzer analyzer = new IKAnalyzer(true);
        IndexWriterConfig iwc = new IndexWriterConfig(Version.LUCENE_4_9, analyzer);
        iwc.setOpenMode(IndexWriterConfig.OpenMode.CREATE);
        iwc.setUseCompoundFile(true);
        IndexWriter indexWriter = new IndexWriter(FSDirectory.open(new File(indexPath)), iwc);

        BufferedReader br = new BufferedReader(new InputStreamReader(
                new FileInputStream(corpusPath), "UTF-8"));

        String line = "";
        String last = ""; //保存上一行的文本
        long lineNum = 0;
        MessageDigest md = MessageDigest.getInstance("MD5");
        HashSet<String> mc = new HashSet<String>();
        int dupCount = 0;
        int totalCount = 0;
        long last_t = 0;
        while((line = br.readLine()) != null) {
            totalCount ++;
            if(totalCount % 15000000 == 0) { //每经过1500 0000行就要HashSet清空
                System.out.println("clear set");
                mc.clear();
            }
            line = line.trim();
            if(0 == line.length()) continue;

            if(!last.equals("")){
                String pair = last + line; //上一行文本+本行文本构成一个(question anwser)对
                byte[] md5 = md.digest(pair.getBytes(UTF8));
                String md5_str = hexString(md5);

                //检查这个pair是否已经存储过了
                if(mc.contains(md5_str)){
                    dupCount ++;
                    continue;
                }else {
                    mc.add(md5_str);
                }
                Document doc = new Document();
                doc.add(new TextField("question", last, Field.Store.YES));
                doc.add(new StoredField("answer", line));
                indexWriter.addDocument(doc);
            }
            last = line;
            lineNum ++;
            if(lineNum % 100000 == 0){ //每计算10万行，就输出所耗费的时间
                long t = System.currentTimeMillis();
                System.out.println("elapse second: " + (t - last_t)/1000 + " add doc " + lineNum + " totalCount:" + totalCount + " dup:" + dupCount);
                last_t = t;
            }
        }
        br.close();
        indexWriter.forceMerge(1);
        indexWriter.close();

        System.out.println( "Hello World!" );
    }
}
