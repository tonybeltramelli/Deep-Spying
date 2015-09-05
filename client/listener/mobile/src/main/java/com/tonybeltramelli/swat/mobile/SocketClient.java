package com.tonybeltramelli.swat.mobile;

import android.content.Context;

import com.google.android.gms.wearable.PutDataMapRequest;
import com.google.android.gms.wearable.PutDataRequest;
import com.tonybeltramelli.swat.mobile.common.AThreadedClient;
import com.tonybeltramelli.swat.mobile.common.Const;
import com.tonybeltramelli.swat.mobile.common.Out;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Created by Tony Beltramelli www.tonybeltramelli.com on 12/08/15.
 */
public class SocketClient
{
    private ExecutorService _threadPool;

    public SocketClient()
    {
        _threadPool = Executors.newCachedThreadPool();
    }

    public void send(final String address, final int port, final String data)
    {
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

