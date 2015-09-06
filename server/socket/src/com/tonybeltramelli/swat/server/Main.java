package com.tonybeltramelli.swat.server;

import com.tonybeltramelli.swat.server.network.TCPSocketServer;

import java.io.IOException;
import java.net.InetAddress;

/**
 * @author Tony Beltramelli www.tonybeltramelli.com - created 23/07/15
 */
public class Main {

    public static void main(String[] args) throws IOException
    {
        System.out.println(InetAddress.getLocalHost().getHostAddress());

        TCPSocketServer tcpSocketServer = new TCPSocketServer(Const.TCP_SOCKET_SERVER_PORT);
        tcpSocketServer.start();

        //HTTPServer httpServer = new HTTPServer(Const.HTTP_SERVER_PORT);
        //httpServer.start();
    }
}
