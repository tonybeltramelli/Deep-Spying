package com.tonybeltramelli.swat.server;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * @author Tony Beltramelli www.tonybeltramelli.com - created 23/07/15
 */
public class Server
{
    private ServerSocket _listener;

    public Server(int port) throws IOException
    {
        _listener = new ServerSocket(port);
        _listener.setReuseAddress(true);
    }

    public void listen() throws IOException
    {
        Socket socket = _listener.accept();

        try {
            BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String data = input.readLine();
            System.out.println(data);
        } finally {
            socket.close();
        }
    }

    public void close() throws IOException
    {
        _listener.close();
    }
}
