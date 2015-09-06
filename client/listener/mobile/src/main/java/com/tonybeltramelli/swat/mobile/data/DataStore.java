package com.tonybeltramelli.swat.mobile.data;

import com.tonybeltramelli.swat.mobile.common.Const;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;

/**
 * Created by Tony Beltramelli www.tonybeltramelli.com on 12/08/15.
 */
public class DataStore
{
    private HashMap<String, LinkedList<DataPoint>> _data;

    private final int BUFFER_SIZE = 100;

    public DataStore()
    {
        _data = new HashMap<String, LinkedList<DataPoint>>();
    }

    public boolean push(String sensorName, DataPoint dataPoint)
    {
        if (!_data.containsKey(sensorName))
        {
            _data.put(sensorName, new LinkedList<DataPoint>());
        }

        boolean isFull = false;

        if(_data.get(sensorName).size() == BUFFER_SIZE)
        {
            _data.get(sensorName).clear();
        }else if(_data.get(sensorName).size() == BUFFER_SIZE - 1)
        {
            isFull = true;
        }

        _data.get(sensorName).addLast(dataPoint);

        return isFull;
    }

    public String getJSONString(String sensorName) throws JSONException
    {
        LinkedList<DataPoint> value = _data.get(sensorName);

        JSONObject root = new JSONObject();
        JSONArray dataPoints = new JSONArray();

        for (DataPoint dataPoint: value)
        {
            dataPoints.put(dataPoint.getJSONObject());
        }

        root.put(Const.SENSOR_NAME, sensorName);
        root.put(Const.DATA_POINTS, dataPoints);

        return root.toString();
    }

    public String[] getJSONStrings() throws JSONException
    {
        String[] sensorJSONs = new String[_data.size()];

        int i = 0;
        for (Map.Entry<String, LinkedList<DataPoint>> entry: _data.entrySet())
        {
            String sensorName = entry.getKey();
            sensorJSONs[i++] = getJSONString(sensorName);
        }

        return sensorJSONs;
    }

    public void clear()
    {
        for (Map.Entry<String, LinkedList<DataPoint>> entry: _data.entrySet())
        {
            String key = entry.getKey();
            _data.get(key).clear();
        }
    }

    public String getSizeReport()
    {
        String size = _data.size() + "( ";
        for (Map.Entry<String, LinkedList<DataPoint>> entry: _data.entrySet())
        {
            size += "[ "+entry.getKey() + " : " + entry.getValue().size() + " ] ";
        }
        size += ")";
        return size;
    }

    @Override
    public String toString()
    {
        String string = super.toString() + "\n";

        for (Map.Entry<String, LinkedList<DataPoint>> entry: _data.entrySet())
        {
            String key = entry.getKey();
            LinkedList<DataPoint> value = entry.getValue();

            string += key + "[\n";

            for (DataPoint dataPoint: value)
            {
                string += " " + dataPoint + "\n";
            }

            string += "]\n";
        }

        return string;
    }
}
