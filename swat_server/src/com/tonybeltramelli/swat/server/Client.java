package com.tonybeltramelli.swat.server;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;

/**
 * @author Tony Beltramelli www.tonybeltramelli.com - created 23/07/15
 */
public class Client
{
    public Client()
    {
    }

    public void connect() throws IOException
    {
        Socket socket = new Socket("192.168.52.231", 25500);

        System.out.println("connect");

        try
        {
            String data = "client message";
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            out.println(data);
        } finally {
            socket.close();
        }

        System.out.println("send");
    }
}
