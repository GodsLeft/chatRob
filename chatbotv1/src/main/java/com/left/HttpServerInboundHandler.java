package com.left;

import io.netty.channel.ChannelFuture;
import io.netty.channel.ChannelFutureListener;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import io.netty.handler.codec.http.FullHttpRequest;
import io.netty.handler.codec.http.HttpResponseStatus;
import io.netty.handler.codec.http.HttpVersion;

/**
 * Created by left on 17-3-6.
 */
//拦截消息，并做出回应的入口
public class HttpServerInboundHandler extends SimpleChannelInboundHandler<FullHttpRequest> {
    @Override
    protected void messageReceived(ChannelHandlerContext ctx, FullHttpRequest msg) throws Exception{
        NettyHttpServletResponse res = new NettyHttpServletResponse(HttpVersion.HTTP_1_1, HttpResponseStatus.OK);
        Action.doServlet(msg, res);
        ChannelFuture future = ctx.channel().writeAndFlush(res);
        future.addListener(ChannelFutureListener.CLOSE);
    }
}
