package com.tonybeltramelli.swat.server.data;

import com.tonybeltramelli.swat.server.AnalyticsProcess;
import com.tonybeltramelli.swat.server.Const;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.lang.reflect.Constructor;
import java.security.SecureRandom;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;

/**
 * @author Tony Beltramelli www.tonybeltramelli.com - created 28/08/15
 */
public class DataStore
{
    private HashMap<String, LinkedList<ADataPoint>> _data;

    private int _sessionID;
    private boolean _isRecording;
    private boolean _useLiveMode;

    public DataStore(boolean useLiveMode)
    {
        _useLiveMode = useLiveMode;

        _init();
    }

    private void _init()
    {
        _isRecording = false;

        if(_data != null)
        {
            for (Map.Entry<String, LinkedList<ADataPoint>> entry: _data.entrySet())
            {
                String key = entry.getKey();
                _data.get(key).clear();
            }
        }

        _data = null;
        _data = new HashMap<String, LinkedList<ADataPoint>>();
    }

    private void _push(String filePath, ADataPoint dataPoint)
    {
        if (!_data.containsKey(filePath))
        {
            _data.put(filePath, new LinkedList<ADataPoint>());
        }

        _data.get(filePath).addLast(dataPoint);
    }

    public void save() throws Exception
    {
        for (Map.Entry<String, LinkedList<ADataPoint>> entry: _data.entrySet())
        {
            String filePath = entry.getKey();
            LinkedList<ADataPoint> dataPoints = entry.getValue();
            Collections.sort(dataPoints);

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
                bufferedWriter.write(dataPoints.element().getCSVHeader());
                bufferedWriter.newLine();
            }

            for(ADataPoint dataPoint: dataPoints)
            {
                bufferedWriter.write(dataPoint.getCSVLine());
                bufferedWriter.newLine();
            }

            bufferedWriter.close();
            fileWriter.close();

            System.out.println("Save data in "+filePath);
        }

        _init();

        if(_useLiveMode) AnalyticsProcess.run("session_" + _sessionID);
    }

    public void generateSessionID()
    {
        SecureRandom random = new SecureRandom();
        random.setSeed(new Date().getTime());

        _sessionID = (int) Math.pow(8, 8) + random.nextInt(99999999 - (int) Math.pow(8, 8));

        _isRecording = true;
    }

    public void store(String data, Class<?> dataPointType) throws Exception
    {
        if (!_isRecording) return;

        JSONParser parser = new JSONParser();
        JSONObject json = (JSONObject) parser.parse(data);

        String sensorName = (String) json.get(Const.SENSOR_NAME);
        String filePath = Const.DATA_OUT_PATH.replace(Const.SESSION_ID, Integer.toString(_sessionID)).replace(Const.SENSOR_NAME, sensorName);

        JSONArray dataPoints = (JSONArray) json.get(Const.DATA_POINTS);

        for(int i = 0; i < dataPoints.size(); i ++)
        {
            JSONObject values = (JSONObject) dataPoints.get(i);

            Constructor<?> constructor = dataPointType.getConstructor(JSONObject.class);
            ADataPoint dataPoint = (ADataPoint) constructor.newInstance(values);

            _push(filePath, dataPoint);
        }
    }

    @Override
    public String toString()
    {
        String string = super.toString() + "\n";

        for (Map.Entry<String, LinkedList<ADataPoint>> entry: _data.entrySet())
        {
            String key = entry.getKey();
            LinkedList<ADataPoint> value = entry.getValue();

            string += key + "[\n";

            for (ADataPoint dataPoint: value)
            {
                string += " " + dataPoint + "\n";
            }

            string += "]\n";
        }

        return string;
    }
}
