package com.tonybeltramelli.swat.server;

import com.tonybeltramelli.swat.server.data.DataStore;
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
        boolean useLiveMode = args.length == 1 && args[0].equals("live");

        System.out.println(InetAddress.getLocalHost().getHostAddress());

        DataStore dataStore = new DataStore(useLiveMode);

        TCPSocketServer tcpSocketServer = new TCPSocketServer(Const.TCP_SOCKET_SERVER_PORT, dataStore);
        tcpSocketServer.start();

        HTTPServer httpServer = new HTTPServer(Const.HTTP_SERVER_PORT, dataStore);
        httpServer.start();
    }
}
