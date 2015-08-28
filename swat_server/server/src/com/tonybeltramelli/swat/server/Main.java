package com.tonybeltramelli.swat.server;

import com.tonybeltramelli.swat.server.network.Server;

import java.io.IOException;
import java.net.InetAddress;

/**
 * @author Tony Beltramelli www.tonybeltramelli.com - created 23/07/15
 */
public class Main {

    public static void main(String[] args) throws IOException
    {
        Server server = new Server(Const.SERVER_PORT);

        System.out.println(InetAddress.getLocalHost().getHostAddress());

        try {
            while(true)
            {
                server.listen();
            }
        } finally {
            server.close();
        }
    }
}
