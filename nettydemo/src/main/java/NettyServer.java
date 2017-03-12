import io.netty.bootstrap.ServerBootstrap;
import io.netty.channel.*;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import io.netty.channel.socket.nio.NioSocketChannel;
import io.netty.handler.codec.DelimiterBasedFrameDecoder;
import io.netty.handler.codec.Delimiters;
import io.netty.handler.codec.string.StringDecoder;
import io.netty.handler.codec.string.StringEncoder;

import java.net.Inet4Address;
import java.net.InetAddress;

/**
 * Created by left on 17-3-12.
 * netty 服务端建立
 * 1.设置线程池
 * 2.设置处理器
 * 3.绑定端口
 */
public class NettyServer {
    public static void main(String[] args) {
        int port = 8081; //服务器监听端口
        EventLoopGroup bossGroup = new NioEventLoopGroup(); //boss线程池
        EventLoopGroup workerGroup = new NioEventLoopGroup(); //worker线程池
        try {
            ServerBootstrap bootstrap = new ServerBootstrap(); // 服务启动器
            bootstrap.group(bossGroup, workerGroup); //指定Netty的Boss线程和worker线程
            bootstrap.channel(NioServerSocketChannel.class); //设置服务器通道类
            bootstrap.childHandler(new ChannelInitializer<NioSocketChannel>() { // 设置处理器
                @Override
                protected void initChannel(NioSocketChannel channel) throws Exception {
                    // 以("\n")为结尾分割的解码器，用于消息识别
                    channel.pipeline().addLast("split", new DelimiterBasedFrameDecoder(1000, Delimiters.lineDelimiter()));
                    channel.pipeline().addLast("decoder", new StringDecoder()); //对字符串进行处理 解码器
                    channel.pipeline().addLast("encoder", new StringEncoder()); //对字符串进行处理 编码器
                    channel.pipeline().addLast("hander", new FirstServerHandler()); // 自定义的处理器
                }
            });
            ChannelFuture future = bootstrap.bind(port).sync();//设置绑定的端口
            future.channel().closeFuture().sync();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            bossGroup.shutdownGracefully();
            workerGroup.shutdownGracefully();
        }
    }
}

/**
 * 自定义处理类
 *
 */
class FirstServerHandler extends SimpleChannelInboundHandler<String>{
    /**
     * 消息过来后执行此方法
     */
    @Override
    protected void channelRead0(ChannelHandlerContext ctx, String msg) throws Exception {
        System.out.println(ctx.channel().remoteAddress() + " : " + msg);
        ctx.writeAndFlush("received your message: " + msg);
    }

    /**
     * 通道被客户端激活时执行此方法
     * @param ctx
     * @throws Exception
     */

    @Override
    public void channelActive(ChannelHandlerContext ctx) throws Exception {
        System.out.println("RemoteAddress : " + ctx.channel().remoteAddress() + " active !"); //通道激活
        ctx.writeAndFlush("Welcome to " + InetAddress.getLocalHost().getHostName() + " service!\n"); //回送进服务系统
    }
}