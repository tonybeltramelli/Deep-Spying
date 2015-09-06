package com.tonybeltramelli.swat.mobile.socket;

import com.tonybeltramelli.swat.mobile.common.Out;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Created by Tony Beltramelli www.tonybeltramelli.com on 12/08/15.
 */
public class SocketClient
{
    private ExecutorService _threadPool;
    private SocketClientThreadFactory _threadFactory;

    public SocketClient()
    {
        _threadPool = Executors.newCachedThreadPool();
        _threadFactory = new SocketClientThreadFactory();
    }

    public void send(final String address, final int port, final String data)
    {
        send(address, port, data, Thread.NORM_PRIORITY);
    }

    public void send(final String address, final int port, final String data, int priority)
    {
        _threadFactory.setPriority(priority);
        _threadPool.submit(new Runnable()
        {
            @Override
            public void run()
            {
                try
                {
                    Socket socket = new Socket(address, port);
                    try
                    {
                        PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                        out.println(data);
                    } finally
                    {
                        socket.close();
                    }
                    Out.print("Send data to "+address+":"+port);
                } catch (IOException e)
                {
                    Out.report(e.getMessage());
                }
            }
        });
    }
}

