package com.tonybeltramelli.swat.server.network;

import com.tonybeltramelli.swat.server.Const;
import com.tonybeltramelli.swat.server.data.DataPoint;
import com.tonybeltramelli.swat.server.data.DataStore;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

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
    private DataStore _dataStore;

    public Server(int port) throws IOException
    {
        _dataStore = new DataStore();

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

            if(!data.equals(Const.END_SIGNAL))
            {
                _store(data);
            } else {
                _dataStore.save();
            }
        } catch(Exception e) {
            e.printStackTrace();
        } finally {
            socket.close();
        }
    }

    private void _store(String data) throws Exception
    {
        JSONParser parser = new JSONParser();
        JSONObject json = (JSONObject) parser.parse(data);

        int sessionID = ((Number) json.get(Const.SESSION_ID)).intValue();
        String sensorName = (String) json.get(Const.SENSOR_NAME);
        String filePath = Const.DATA_OUT_PATH.replace(Const.SESSION_ID, Integer.toString(sessionID)).replace(Const.SENSOR_NAME, sensorName);

        JSONArray dataPoints = (JSONArray) json.get(Const.DATA_POINTS);

        for(int i = 0; i < dataPoints.size(); i ++)
        {
            JSONObject values = (JSONObject) dataPoints.get(i);
            DataPoint dataPoint = new DataPoint(values);

            _dataStore.push(filePath, dataPoint);
        }
    }

    public void close() throws IOException
    {
        _listener.close();
    }
}
