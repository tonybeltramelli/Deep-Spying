package com.tonybeltramelli.swat.server;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
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
            _save(data);
        } catch(Exception e) {
            e.printStackTrace();
        } finally {
            socket.close();
        }
    }

    private void _save(String data) throws Exception
    {
        JSONParser parser = new JSONParser();
        JSONObject json = (JSONObject) parser.parse(data);

        int sessionID = ((Number) json.get(Config.SESSION_ID)).intValue();
        String sensorName = (String) json.get(Config.SENSOR_NAME);

        String filePath = Config.DATA_OUT_PATH.replace(Config.SESSION_ID, Integer.toString(sessionID)).replace(Config.SENSOR_NAME, sensorName);
        File file = new File(filePath);

        boolean isCreated = false;
        if(!file.exists())
        {
            file.createNewFile();
            isCreated = true;
        }

        FileWriter fileWriter = new FileWriter(file.getAbsoluteFile(), true);
        BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);

        if(isCreated)
        {
            bufferedWriter.write(Config.TIMESTAMP+","+Config.X+","+Config.Y+","+Config.Z);
            bufferedWriter.newLine();
        }

        JSONArray dataPoints = (JSONArray) json.get(Config.DATA_POINTS);

        for(int i = 0; i < dataPoints.size(); i ++)
        {
            JSONObject values = (JSONObject) dataPoints.get(i);
            long timestamp = ((Number) values.get(Config.TIMESTAMP)).longValue();
            double x = ((Number) values.get(Config.X)).doubleValue();
            double y = ((Number) values.get(Config.Y)).doubleValue();
            double z = ((Number) values.get(Config.Z)).doubleValue();

            bufferedWriter.write(timestamp + "," + x + "," + y + "," + z);
            bufferedWriter.newLine();
        }

        bufferedWriter.close();
        fileWriter.close();
    }

    public void close() throws IOException
    {
        _listener.close();
    }
}
