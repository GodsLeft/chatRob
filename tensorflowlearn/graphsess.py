#coding:utf-8
import tensorflow as tf

with tf.Graph().as_default() as g:
    with g.name_scope("myscope") as scope: # 有了这个scope，下面的op的name都是类似myscope/Placeholder这样的前缀
        sess = tf.Session(target='', graph=g, config=None) #target表示要连接的tf执行引擎
        print "graph version:", g.version
        a = tf.placeholder("float")
        print a.op # 输出整个operation信息，跟下面g.get_operations返回结果一样
        print "graph version:", g.version

        b = tf.placeholder("float")
        print "graph version:", g.version

        c = tf.placeholder("float")
        print "graph version:", g.version

        y1 = tf.multiply(a, b)
        print "graph version:", g.version

        y2 = tf.multiply(y1, c)
        print "graph version:", g.version

        operations = g.get_operations()
        for (i, op) in enumerate(operations):
            print "=========== operation", i+1, "=========="
            print op # 一个结构，包括：name op attr input等，不同op不一样
        assert y1.graph is g
        assert sess.graph is g
        print "========== graph object address =========="
        print sess.graph
        print "========== graph define =========="
        print sess.graph_def
        print "========== sess str =========="
        print sess.sess_str
        print sess.run(y1, feed_dict={a:3, b:3}) #
        print sess.run(fetches=[b, y1], feed_dict={a:3, b:3}, options=None, run_metadata=None)
        print sess.run({'ret_name':y1}, feed_dict={a:3, b:3})

        assert tf.get_default_session() is not sess
        with sess.as_default():
            assert  tf.get_default_session() is sess

        h = sess.partial_run_setup([y1, y2], [a, b, c])
        res = sess.partial_run(h, y1, feed_dict={a:3, b:4})
        res = sess.partial_run(h, y2, feed_dict={c: res})
        print "partial_run res:", res
        sess.close()