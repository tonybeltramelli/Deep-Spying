package com.tonybeltramelli.swat.server;

import com.tonybeltramelli.swat.server.network.HTTPServer;
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

        TCPSocketServerThread tcpSocketServerThread = new TCPSocketServerThread();
        tcpSocketServerThread.start();

        HTTPServerThread httpServerThread = new HTTPServerThread();
        httpServerThread.start();
    }

    static private class TCPSocketServerThread extends Thread
    {
        @Override
        public void run()
        {
            super.run();

            try
            {
                TCPSocketServer tcpSocketServer = new TCPSocketServer(Const.TCP_SOCKET_SERVER_PORT);
                try
                {
                    while(true)
                    {
                        tcpSocketServer.listen();
                    }
                } finally
                {
                    tcpSocketServer.close();
                }
            } catch(IOException e)
            {
                e.printStackTrace();
            }
        }
    }

    static private class HTTPServerThread extends Thread
    {
        @Override
        public void run()
        {
            super.run();

            try
            {
                HTTPServer httpServer = new HTTPServer(Const.HTTP_SERVER_PORT);
                try
                {
                    while(true)
                    {
                        httpServer.listen();
                    }
                } finally
                {
                    httpServer.close();
                }
            } catch(IOException e)
            {
                e.printStackTrace();
            }
        }
    }
}
