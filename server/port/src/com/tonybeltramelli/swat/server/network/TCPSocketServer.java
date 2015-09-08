package com.tonybeltramelli.swat.server.network;

import com.tonybeltramelli.swat.server.Const;
import com.tonybeltramelli.swat.server.data.DataStore;
import com.tonybeltramelli.swat.server.data.SensorDataPoint;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * @author Tony Beltramelli www.tonybeltramelli.com - created 23/07/15
 */
public class TCPSocketServer extends Thread implements IServer
{
    private ServerSocket _listener;
    private DataStore _dataStore;

    public TCPSocketServer(int port, DataStore dataStore) throws IOException
    {
        _dataStore = dataStore;

        _listener = new ServerSocket(port);
        _listener.setReuseAddress(true);

        System.out.println("Start TCP Socket Server on port " + port);
    }

    @Override
    public void run()
    {
        super.run();

        try
        {
            try
            {
                while(true)
                {
                    listen();
                }
            } catch(IOException e)
            {
                e.printStackTrace();
            } finally
            {
                close();
            }
        } catch(IOException e)
        {
            e.printStackTrace();
        }
    }

    @Override
    public void listen() throws IOException
    {
        Socket socket = _listener.accept();

        try {
            BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String data = input.readLine();

            System.out.println(Const.getDataSnapshot(data));

            if(data.equals(Const.START_SESSION))
            {
                _dataStore.generateSessionID();
            }else if(data.equals(Const.END_SESSION))
            {
                _dataStore.save();
            }else{
                _dataStore.store(data, SensorDataPoint.class);
            }
        } catch(Exception e) {
            e.printStackTrace();
        } finally {
            socket.close();
        }
    }

    @Override
    public void close() throws IOException
    {
        _listener.close();
    }
}
